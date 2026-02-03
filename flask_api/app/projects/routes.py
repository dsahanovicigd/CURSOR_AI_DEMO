from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from sqlalchemy import or_
from app.projects import projects_bp
from app.models.project import Project
from app.models.user import User
from app.models.notification import Notification
from app.schemas.project import ProjectSchema, ProjectCreateSchema, ProjectUpdateSchema, ProjectMemberSchema

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)
project_create_schema = ProjectCreateSchema()
project_update_schema = ProjectUpdateSchema()
project_member_schema = ProjectMemberSchema()

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

@projects_bp.route('', methods=['GET'])
@jwt_required()
def get_projects():
    """
    Get all projects
    ---
    tags:
      - Projects
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
        name: status
        type: string
        enum: [active, archived, completed]
    responses:
      200:
        description: List of projects
    """
    current_user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    per_page = min(per_page, 100)
    
    current_user = User.query.get(current_user_id)
    
    # Get projects where user is owner or member
    project_ids = [p.id for p in current_user.projects.all()]
    if project_ids:
        query = Project.query.filter(
            or_(
                Project.owner_id == current_user_id,
                Project.id.in_(project_ids)
            )
        )
    else:
        query = Project.query.filter_by(owner_id=current_user_id)
    
    if status:
        query = query.filter_by(status=status)
    
    projects = query.order_by(Project.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'projects': projects_schema.dump(projects.items),
        'pagination': {
            'page': projects.page,
            'pages': projects.pages,
            'per_page': projects.per_page,
            'total': projects.total
        }
    }), 200

@projects_bp.route('', methods=['POST'])
@jwt_required()
def create_project():
    """
    Create a new project
    ---
    tags:
      - Projects
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
            description:
              type: string
            status:
              type: string
            team_id:
              type: integer
            start_date:
              type: string
              format: date-time
            end_date:
              type: string
              format: date-time
    responses:
      201:
        description: Project created successfully
    """
    current_user_id = get_jwt_identity()
    
    try:
        data = project_create_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    # Validate team access if team_id provided
    if data.get('team_id'):
        from app.models.team import Team
        team = Team.query.get_or_404(data['team_id'])
        current_user = User.query.get(current_user_id)
        if team.owner_id != current_user_id and current_user not in team.members:
            return jsonify({'error': 'Access denied to team'}), 403
    
    project = Project(
        name=data['name'],
        description=data.get('description'),
        status=data.get('status', 'active'),
        owner_id=current_user_id,
        team_id=data.get('team_id'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date')
    )
    
    db.session.add(project)
    db.session.commit()
    
    return jsonify(project_schema.dump(project)), 201

@projects_bp.route('/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    """
    Get a specific project
    ---
    tags:
      - Projects
    security:
      - Bearer: []
    parameters:
      - in: path
        name: project_id
        type: integer
        required: true
    responses:
      200:
        description: Project details
      403:
        description: Access denied
      404:
        description: Project not found
    """
    current_user_id = get_jwt_identity()
    project = Project.query.get_or_404(project_id)
    
    # Check access
    current_user = User.query.get(current_user_id)
    if project.owner_id != current_user_id and current_user not in project.members:
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify(project_schema.dump(project)), 200

@projects_bp.route('/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    """
    Update a project
    ---
    tags:
      - Projects
    security:
      - Bearer: []
    parameters:
      - in: path
        name: project_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
            status:
              type: string
            start_date:
              type: string
            end_date:
              type: string
    responses:
      200:
        description: Project updated successfully
      403:
        description: Access denied
    """
    current_user_id = get_jwt_identity()
    project = Project.query.get_or_404(project_id)
    
    # Only owner or admin can update
    current_user = User.query.get(current_user_id)
    role = project.get_member_role(current_user) if current_user in project.members else None
    if project.owner_id != current_user_id and role not in ['owner', 'admin']:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        data = project_update_schema.load(request.json, partial=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    if 'name' in data:
        project.name = data['name']
    if 'description' in data:
        project.description = data['description']
    if 'status' in data:
        project.status = data['status']
    if 'start_date' in data:
        project.start_date = data['start_date']
    if 'end_date' in data:
        project.end_date = data['end_date']
    if 'team_id' in data:
        project.team_id = data['team_id']
    
    db.session.commit()
    
    return jsonify(project_schema.dump(project)), 200

@projects_bp.route('/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    """
    Delete a project
    ---
    tags:
      - Projects
    security:
      - Bearer: []
    parameters:
      - in: path
        name: project_id
        type: integer
        required: true
    responses:
      204:
        description: Project deleted successfully
      403:
        description: Access denied
    """
    current_user_id = get_jwt_identity()
    project = Project.query.get_or_404(project_id)
    
    # Only owner can delete
    if project.owner_id != current_user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    db.session.delete(project)
    db.session.commit()
    
    return '', 204

@projects_bp.route('/<int:project_id>/members', methods=['GET'])
@jwt_required()
def get_project_members(project_id):
    """
    Get project members
    ---
    tags:
      - Projects
    security:
      - Bearer: []
    parameters:
      - in: path
        name: project_id
        type: integer
        required: true
    responses:
      200:
        description: List of project members
    """
    current_user_id = get_jwt_identity()
    project = Project.query.get_or_404(project_id)
    
    # Check access
    current_user = User.query.get(current_user_id)
    if project.owner_id != current_user_id and current_user not in project.members:
        return jsonify({'error': 'Access denied'}), 403
    
    members = []
    for member in project.members.all():
        role = project.get_member_role(member)
        members.append({
            'id': member.id,
            'username': member.username,
            'email': member.email,
            'first_name': member.first_name,
            'last_name': member.last_name,
            'role': role
        })
    
    # Add owner
    if project.owner not in project.members.all():
        members.append({
            'id': project.owner.id,
            'username': project.owner.username,
            'email': project.owner.email,
            'first_name': project.owner.first_name,
            'last_name': project.owner.last_name,
            'role': 'owner'
        })
    
    return jsonify({'members': members}), 200

@projects_bp.route('/<int:project_id>/members', methods=['POST'])
@jwt_required()
def add_project_member(project_id):
    """
    Add a member to project
    ---
    tags:
      - Projects
    security:
      - Bearer: []
    parameters:
      - in: path
        name: project_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          required:
            - user_id
          properties:
            user_id:
              type: integer
            role:
              type: string
              enum: [owner, admin, member]
    responses:
      201:
        description: Member added successfully
      403:
        description: Access denied
    """
    current_user_id = get_jwt_identity()
    project = Project.query.get_or_404(project_id)
    
    # Only owner or admin can add members
    current_user = User.query.get(current_user_id)
    role = project.get_member_role(current_user) if current_user in project.members else None
    if project.owner_id != current_user_id and role not in ['owner', 'admin']:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        data = project_member_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    user = User.query.get_or_404(data['user_id'])
    member_role = data.get('role', 'member')
    
    # Don't allow changing owner role
    if member_role == 'owner' and project.owner_id != current_user_id:
        return jsonify({'error': 'Only current owner can assign owner role'}), 403
    
    project.add_member(user, member_role)
    
    # Create notification
    create_notification(
        user_id=user.id,
        type=Notification.TYPE_PROJECT_INVITE,
        title=f'Added to project: {project.name}',
        message=f'You have been added to project "{project.name}"',
        project_id=project.id
    )
    db.session.commit()
    
    return jsonify({'message': 'Member added successfully'}), 201

@projects_bp.route('/<int:project_id>/members/<int:user_id>', methods=['DELETE'])
@jwt_required()
def remove_project_member(project_id, user_id):
    """
    Remove a member from project
    ---
    tags:
      - Projects
    security:
      - Bearer: []
    parameters:
      - in: path
        name: project_id
        type: integer
        required: true
      - in: path
        name: user_id
        type: integer
        required: true
    responses:
      204:
        description: Member removed successfully
      403:
        description: Access denied
    """
    current_user_id = get_jwt_identity()
    project = Project.query.get_or_404(project_id)
    
    # Only owner or admin can remove members
    current_user = User.query.get(current_user_id)
    role = project.get_member_role(current_user) if current_user in project.members else None
    if project.owner_id != current_user_id and role not in ['owner', 'admin']:
        return jsonify({'error': 'Access denied'}), 403
    
    # Cannot remove owner
    if project.owner_id == user_id:
        return jsonify({'error': 'Cannot remove project owner'}), 400
    
    user = User.query.get_or_404(user_id)
    project.remove_member(user)
    
    return '', 204
