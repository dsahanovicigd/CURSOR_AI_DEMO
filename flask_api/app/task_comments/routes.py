from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.task_comments import task_comments_bp
from app.models.task_comment import TaskComment
from app.models.task import Task
from app.models.user import User
from app.models.notification import Notification
from app.schemas.task_comment import TaskCommentSchema, TaskCommentCreateSchema, TaskCommentUpdateSchema

comment_schema = TaskCommentSchema()
comments_schema = TaskCommentSchema(many=True)
comment_create_schema = TaskCommentCreateSchema()
comment_update_schema = TaskCommentUpdateSchema()

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

@task_comments_bp.route('/tasks/<int:task_id>/comments', methods=['GET'])
@jwt_required()
def get_task_comments(task_id):
    """
    Get all comments for a task
    ---
    tags:
      - Task Comments
    security:
      - Bearer: []
    parameters:
      - in: path
        name: task_id
        type: integer
        required: true
      - in: query
        name: page
        type: integer
        default: 1
      - in: query
        name: per_page
        type: integer
        default: 20
    responses:
      200:
        description: List of comments
      403:
        description: Access denied
    """
    current_user_id = get_jwt_identity()
    task = Task.query.get_or_404(task_id)
    
    # Check access
    current_user = User.query.get(current_user_id)
    if task.created_by_id != current_user_id and \
       task.assigned_to_id != current_user_id and \
       (not task.project_id or current_user not in task.project.members):
        return jsonify({'error': 'Access denied'}), 403
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    per_page = min(per_page, 100)
    
    comments = TaskComment.query.filter_by(task_id=task_id).order_by(
        TaskComment.created_at.asc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'comments': comments_schema.dump(comments.items),
        'pagination': {
            'page': comments.page,
            'pages': comments.pages,
            'per_page': comments.per_page,
            'total': comments.total
        }
    }), 200

@task_comments_bp.route('/tasks/<int:task_id>/comments', methods=['POST'])
@jwt_required()
def create_task_comment(task_id):
    """
    Create a comment on a task
    ---
    tags:
      - Task Comments
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
          required:
            - content
          properties:
            content:
              type: string
    responses:
      201:
        description: Comment created successfully
      403:
        description: Access denied
    """
    current_user_id = get_jwt_identity()
    task = Task.query.get_or_404(task_id)
    
    # Check access
    current_user = User.query.get(current_user_id)
    if task.created_by_id != current_user_id and \
       task.assigned_to_id != current_user_id and \
       (not task.project_id or current_user not in task.project.members):
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        data = comment_create_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    comment = TaskComment(
        content=data['content'],
        task_id=task_id,
        user_id=current_user_id
    )
    
    db.session.add(comment)
    db.session.commit()
    
    # Notify task assignee and creator (if different from commenter)
    notify_users = set()
    if task.assigned_to_id and task.assigned_to_id != current_user_id:
        notify_users.add(task.assigned_to_id)
    if task.created_by_id != current_user_id:
        notify_users.add(task.created_by_id)
    
    # Notify project members if task is in a project
    if task.project_id:
        for member in task.project.members:
            if member.id != current_user_id:
                notify_users.add(member.id)
    
    for user_id in notify_users:
        create_notification(
            user_id=user_id,
            type=Notification.TYPE_TASK_COMMENT,
            title=f'New comment on task: {task.title}',
            message=f'{current_user.username} commented on task "{task.title}"',
            task_id=task.id,
            project_id=task.project_id
        )
    
    db.session.commit()
    
    return jsonify(comment_schema.dump(comment)), 201

@task_comments_bp.route('/comments/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update_task_comment(comment_id):
    """
    Update a task comment
    ---
    tags:
      - Task Comments
    security:
      - Bearer: []
    parameters:
      - in: path
        name: comment_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          required:
            - content
          properties:
            content:
              type: string
    responses:
      200:
        description: Comment updated successfully
      403:
        description: Access denied
    """
    current_user_id = get_jwt_identity()
    comment = TaskComment.query.get_or_404(comment_id)
    
    # Only comment author can update
    if comment.user_id != current_user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        data = comment_update_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    comment.content = data['content']
    db.session.commit()
    
    return jsonify(comment_schema.dump(comment)), 200

@task_comments_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_task_comment(comment_id):
    """
    Delete a task comment
    ---
    tags:
      - Task Comments
    security:
      - Bearer: []
    parameters:
      - in: path
        name: comment_id
        type: integer
        required: true
    responses:
      204:
        description: Comment deleted successfully
      403:
        description: Access denied
    """
    current_user_id = get_jwt_identity()
    comment = TaskComment.query.get_or_404(comment_id)
    
    # Only comment author or task creator can delete
    task = comment.task
    if comment.user_id != current_user_id and task.created_by_id != current_user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    db.session.delete(comment)
    db.session.commit()
    
    return '', 204
