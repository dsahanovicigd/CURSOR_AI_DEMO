from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from sqlalchemy import or_
from app.tasks import tasks_bp
from app.models.task import Task
from app.models.user import User
from app.models.project import Project
from app.models.notification import Notification
from app.schemas.task import TaskSchema, TaskCreateSchema, TaskUpdateSchema
from app.cache import cache, cached_task_list, cached_task_detail, invalidate_task_cache
from app.tasks.background_tasks import send_task_notification

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
task_create_schema = TaskCreateSchema()
task_update_schema = TaskUpdateSchema()

def create_notification(user_id, type, title, message, **kwargs):
    """Helper function to create notifications"""
    notification = Notification(
        user_id=user_id,
        type=type,
        title=title,
        message=message,
        related_task_id=kwargs.get('task_id'),
        related_project_id=kwargs.get('project_id'),
        related_team_id=kwargs.get('team_id'),
        meta_data=kwargs.get('metadata')
    )
    db.session.add(notification)
    return notification

@tasks_bp.route('', methods=['GET'])
@jwt_required()
def get_tasks():
    """
    Get all tasks
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - in: query
        name: page
        type: integer
        default: 1
      - in: query
        name: per_page
        type: integer
        default: 20
      - in: query
        name: project_id
        type: integer
      - in: query
        name: assigned_to_id
        type: integer
      - in: query
        name: status
        type: string
        enum: [pending, in_progress, completed, cancelled]
      - in: query
        name: priority
        type: string
        enum: [low, medium, high, urgent]
    responses:
      200:
        description: List of tasks
    """
    current_user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    project_id = request.args.get('project_id', type=int)
    assigned_to_id = request.args.get('assigned_to_id', type=int)
    status = request.args.get('status')
    priority = request.args.get('priority')
    per_page = min(per_page, 100)
    
    # Check cache first
    cache_key_str = f"tasks:list:{current_user_id}:{page}:{per_page}:{project_id}:{assigned_to_id}:{status}:{priority}"
    cached_result = cache.get(cache_key_str)
    if cached_result is not None:
        return jsonify(cached_result), 200
    
    query = Task.query
    
    # Filter by project if user is a member
    if project_id:
        project = Project.query.get_or_404(project_id)
        current_user = User.query.get(current_user_id)
        # Check if user is project owner or member
        if project.owner_id != current_user_id and current_user not in project.members:
            return jsonify({'error': 'Access denied'}), 403
        query = query.filter_by(project_id=project_id)
    
    # Filter by assigned user
    if assigned_to_id:
        query = query.filter_by(assigned_to_id=assigned_to_id)
    
    # Filter by status
    if status:
        query = query.filter_by(status=status)
    
    # Filter by priority
    if priority:
        query = query.filter_by(priority=priority)
    
    # If no project filter, show only user's tasks or tasks in their projects
    if not project_id:
        current_user = User.query.get(current_user_id)
        # Get user's project IDs
        project_ids = [p.id for p in current_user.projects.all()]
        if project_ids:
            query = query.filter(
                or_(
                    Task.created_by_id == current_user_id,
                    Task.assigned_to_id == current_user_id,
                    Task.project_id.in_(project_ids)
                )
            )
        else:
            query = query.filter(
                or_(
                    Task.created_by_id == current_user_id,
                    Task.assigned_to_id == current_user_id
                )
            )
    
    tasks = query.order_by(Task.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    result = {
        'tasks': tasks_schema.dump(tasks.items),
        'pagination': {
            'page': tasks.page,
            'pages': tasks.pages,
            'per_page': tasks.per_page,
            'total': tasks.total
        }
    }
    
    # Cache the result
    cache.set(cache_key_str, result, timeout=300)
    
    return jsonify(result), 200

@tasks_bp.route('', methods=['POST'])
@jwt_required()
def create_task():
    """
    Create a new task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - title
          properties:
            title:
              type: string
            description:
              type: string
            status:
              type: string
              enum: [pending, in_progress, completed, cancelled]
            priority:
              type: string
              enum: [low, medium, high, urgent]
            project_id:
              type: integer
            assigned_to_id:
              type: integer
            due_date:
              type: string
              format: date-time
    responses:
      201:
        description: Task created successfully
      400:
        description: Validation error
    """
    current_user_id = get_jwt_identity()
    
    try:
        data = task_create_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    # Validate project access if project_id provided
    if data.get('project_id'):
        project = Project.query.get_or_404(data['project_id'])
        current_user = User.query.get(current_user_id)
        if project.owner_id != current_user_id and current_user not in project.members:
            return jsonify({'error': 'Access denied to project'}), 403
    
    # Validate assigned user if provided
    if data.get('assigned_to_id'):
        assigned_user = User.query.get_or_404(data['assigned_to_id'])
        if not assigned_user.is_active:
            return jsonify({'error': 'Cannot assign to inactive user'}), 400
    
    task = Task(
        title=data['title'],
        description=data.get('description'),
        status=data.get('status', Task.STATUS_PENDING),
        priority=data.get('priority', Task.PRIORITY_MEDIUM),
        project_id=data.get('project_id'),
        assigned_to_id=data.get('assigned_to_id'),
        created_by_id=current_user_id,
        due_date=data.get('due_date')
    )
    
    db.session.add(task)
    db.session.commit()
    
    # Invalidate cache
    invalidate_task_cache(user_id=current_user_id)
    
    # Create notification if task is assigned (background task)
    if task.assigned_to_id and task.assigned_to_id != current_user_id:
        # Send notification via background task
        send_task_notification.delay(
            task.id,
            task.assigned_to_id,
            Notification.TYPE_TASK_ASSIGNED,
            f'You have been assigned to task "{task.title}"'
        )
        
        # Also send email notification
        if task.assigned_to:
            from app.tasks.background_tasks import send_task_assignment_email
            send_task_assignment_email.delay(task.id, task.assigned_to.email)
    
    return jsonify(task_schema.dump(task)), 201

@tasks_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """
    Get a specific task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - in: path
        name: task_id
        type: integer
        required: true
    responses:
      200:
        description: Task details
      404:
        description: Task not found
    """
    current_user_id = get_jwt_identity()
    
    # Check cache first
    cache_key_str = f"tasks:detail:{task_id}"
    cached_result = cache.get(cache_key_str)
    if cached_result is not None:
        return jsonify(cached_result), 200
    
    task = Task.query.get_or_404(task_id)
    
    # Check access
    current_user = User.query.get(current_user_id)
    if task.created_by_id != current_user_id and \
       task.assigned_to_id != current_user_id and \
       (not task.project_id or (task.project and current_user not in task.project.members)):
        return jsonify({'error': 'Access denied'}), 403
    
    result = task_schema.dump(task)
    
    # Cache the result
    cache.set(cache_key_str, result, timeout=600)
    
    return jsonify(result), 200

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """
    Update a task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - in: path
        name: task_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
            status:
              type: string
            priority:
              type: string
            assigned_to_id:
              type: integer
            due_date:
              type: string
    responses:
      200:
        description: Task updated successfully
      403:
        description: Access denied
      404:
        description: Task not found
    """
    current_user_id = get_jwt_identity()
    task = Task.query.get_or_404(task_id)
    
    # Check permissions
    current_user = User.query.get(current_user_id)
    is_owner = task.created_by_id == current_user_id
    is_assigned = task.assigned_to_id == current_user_id
    is_project_admin = False
    
    if task.project_id:
        project = task.project
        role = project.get_member_role(current_user) if current_user in project.members else None
        is_project_admin = project.owner_id == current_user_id or role in ['owner', 'admin']
    
    if not (is_owner or is_assigned or is_project_admin):
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        data = task_update_schema.load(request.json, partial=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    # Track status change for notifications
    old_status = task.status
    old_assigned_to = task.assigned_to_id
    
    # Update fields
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        task.status = data['status']
        if task.status == Task.STATUS_COMPLETED and old_status != Task.STATUS_COMPLETED:
            task.mark_completed()
            # Notify project members
            if task.project_id:
                for member in task.project.members:
                    if member.id != current_user_id:
                        create_notification(
                            user_id=member.id,
                            type=Notification.TYPE_TASK_COMPLETED,
                            title=f'Task completed: {task.title}',
                            message=f'Task "{task.title}" has been marked as completed',
                            task_id=task.id,
                            project_id=task.project_id
                        )
    if 'priority' in data:
        task.priority = data['priority']
    if 'assigned_to_id' in data:
        task.assigned_to_id = data['assigned_to_id']
        # Notify new assignee if changed
        if task.assigned_to_id and task.assigned_to_id != old_assigned_to and task.assigned_to_id != current_user_id:
            create_notification(
                user_id=task.assigned_to_id,
                type=Notification.TYPE_TASK_ASSIGNED,
                title=f'Task assigned: {task.title}',
                message=f'You have been assigned to task "{task.title}"',
                task_id=task.id,
                project_id=task.project_id
            )
    if 'due_date' in data:
        task.due_date = data['due_date']
    if 'project_id' in data:
        task.project_id = data['project_id']
    
    db.session.commit()
    
    # Invalidate cache
    invalidate_task_cache(task_id)
    
    # Send notification if status changed (background task)
    if 'status' in data and task.assigned_to_id:
        send_task_notification.delay(
            task.id,
            task.assigned_to_id,
            Notification.TYPE_TASK_ASSIGNED,
            f'Task "{task.title}" status changed to {task.status}'
        )
    
    return jsonify(task_schema.dump(task)), 200

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """
    Delete a task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - in: path
        name: task_id
        type: integer
        required: true
    responses:
      204:
        description: Task deleted successfully
      403:
        description: Access denied
      404:
        description: Task not found
    """
    current_user_id = get_jwt_identity()
    task = Task.query.get_or_404(task_id)
    
    # Only creator or project admin can delete
    current_user = User.query.get(current_user_id)
    is_owner = task.created_by_id == current_user_id
    is_project_admin = False
    
    if task.project_id:
        project = task.project
        role = project.get_member_role(current_user) if current_user in project.members else None
        is_project_admin = project.owner_id == current_user_id or role in ['owner', 'admin']
    
    if not (is_owner or is_project_admin):
        return jsonify({'error': 'Access denied'}), 403
    
    task_id = task.id
    db.session.delete(task)
    db.session.commit()
    
    # Invalidate cache
    invalidate_task_cache(task_id)
    
    return '', 204

@tasks_bp.route('/<int:task_id>/complete', methods=['POST'])
@jwt_required()
def complete_task(task_id):
    """
    Mark a task as completed
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - in: path
        name: task_id
        type: integer
        required: true
    responses:
      200:
        description: Task marked as completed
      403:
        description: Access denied
    """
    current_user_id = get_jwt_identity()
    task = Task.query.get_or_404(task_id)
    
    # Check if user can complete this task
    if task.assigned_to_id != current_user_id and task.created_by_id != current_user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    task.mark_completed()
    db.session.commit()
    
    # Invalidate cache
    invalidate_task_cache(task_id)
    
    # Notify project members (background task)
    if task.project_id:
        for member in task.project.members:
            if member.id != current_user_id:
                send_task_notification.delay(
                    task.id,
                    member.id,
                    Notification.TYPE_TASK_COMPLETED,
                    f'Task "{task.title}" has been completed'
                )
    
    return jsonify(task_schema.dump(task)), 200
