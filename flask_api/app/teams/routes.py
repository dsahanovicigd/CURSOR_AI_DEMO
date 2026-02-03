from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from sqlalchemy import or_
from app.teams import teams_bp
from app.models.team import Team
from app.models.user import User
from app.models.notification import Notification
from app.schemas.team import TeamSchema, TeamCreateSchema, TeamUpdateSchema, TeamMemberSchema

team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)
team_create_schema = TeamCreateSchema()
team_update_schema = TeamUpdateSchema()
team_member_schema = TeamMemberSchema()

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

@teams_bp.route('', methods=['GET'])
@jwt_required()
def get_teams():
    """
    Get all teams
    ---
    tags:
      - Teams
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
    responses:
      200:
        description: List of teams
    """
    current_user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    per_page = min(per_page, 100)
    
    current_user = User.query.get(current_user_id)
    
    # Get teams where user is owner or member
    team_ids = [t.id for t in current_user.teams.all()]
    if team_ids:
        query = Team.query.filter(
            or_(
                Team.owner_id == current_user_id,
                Team.id.in_(team_ids)
            )
        )
    else:
        query = Team.query.filter_by(owner_id=current_user_id)
    
    teams = query.order_by(Team.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'teams': teams_schema.dump(teams.items),
        'pagination': {
            'page': teams.page,
            'pages': teams.pages,
            'per_page': teams.per_page,
            'total': teams.total
        }
    }), 200

@teams_bp.route('', methods=['POST'])
@jwt_required()
def create_team():
    """
    Create a new team
    ---
    tags:
      - Teams
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
    responses:
      201:
        description: Team created successfully
    """
    current_user_id = get_jwt_identity()
    
    try:
        data = team_create_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    team = Team(
        name=data['name'],
        description=data.get('description'),
        owner_id=current_user_id
    )
    
    db.session.add(team)
    db.session.commit()
    
    return jsonify(team_schema.dump(team)), 201

@teams_bp.route('/<int:team_id>', methods=['GET'])
@jwt_required()
def get_team(team_id):
    """
    Get a specific team
    ---
    tags:
      - Teams
    security:
      - Bearer: []
    parameters:
      - in: path
        name: team_id
        type: integer
        required: true
    responses:
      200:
        description: Team details
      403:
        description: Access denied
      404:
        description: Team not found
    """
    current_user_id = get_jwt_identity()
    team = Team.query.get_or_404(team_id)
    
    # Check access
    current_user = User.query.get(current_user_id)
    if team.owner_id != current_user_id and current_user not in team.members:
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify(team_schema.dump(team)), 200

@teams_bp.route('/<int:team_id>', methods=['PUT'])
@jwt_required()
def update_team(team_id):
    """
    Update a team
    ---
    tags:
      - Teams
    security:
      - Bearer: []
    parameters:
      - in: path
        name: team_id
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
    responses:
      200:
        description: Team updated successfully
      403:
        description: Access denied
    """
    current_user_id = get_jwt_identity()
    team = Team.query.get_or_404(team_id)
    
    # Only owner or admin can update
    current_user = User.query.get(current_user_id)
    role = team.get_member_role(current_user) if current_user in team.members else None
    if team.owner_id != current_user_id and role not in ['owner', 'admin']:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        data = team_update_schema.load(request.json, partial=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    if 'name' in data:
        team.name = data['name']
    if 'description' in data:
        team.description = data['description']
    
    db.session.commit()
    
    return jsonify(team_schema.dump(team)), 200

@teams_bp.route('/<int:team_id>', methods=['DELETE'])
@jwt_required()
def delete_team(team_id):
    """
    Delete a team
    ---
    tags:
      - Teams
    security:
      - Bearer: []
    parameters:
      - in: path
        name: team_id
        type: integer
        required: true
    responses:
      204:
        description: Team deleted successfully
      403:
        description: Access denied
    """
    current_user_id = get_jwt_identity()
    team = Team.query.get_or_404(team_id)
    
    # Only owner can delete
    if team.owner_id != current_user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    db.session.delete(team)
    db.session.commit()
    
    return '', 204

@teams_bp.route('/<int:team_id>/members', methods=['GET'])
@jwt_required()
def get_team_members(team_id):
    """
    Get team members
    ---
    tags:
      - Teams
    security:
      - Bearer: []
    parameters:
      - in: path
        name: team_id
        type: integer
        required: true
    responses:
      200:
        description: List of team members
    """
    current_user_id = get_jwt_identity()
    team = Team.query.get_or_404(team_id)
    
    # Check access
    current_user = User.query.get(current_user_id)
    if team.owner_id != current_user_id and current_user not in team.members:
        return jsonify({'error': 'Access denied'}), 403
    
    members = []
    for member in team.members.all():
        role = team.get_member_role(member)
        members.append({
            'id': member.id,
            'username': member.username,
            'email': member.email,
            'first_name': member.first_name,
            'last_name': member.last_name,
            'role': role
        })
    
    # Add owner
    if team.owner not in team.members.all():
        members.append({
            'id': team.owner.id,
            'username': team.owner.username,
            'email': team.owner.email,
            'first_name': team.owner.first_name,
            'last_name': team.owner.last_name,
            'role': 'owner'
        })
    
    return jsonify({'members': members}), 200

@teams_bp.route('/<int:team_id>/members', methods=['POST'])
@jwt_required()
def add_team_member(team_id):
    """
    Add a member to team
    ---
    tags:
      - Teams
    security:
      - Bearer: []
    parameters:
      - in: path
        name: team_id
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
    team = Team.query.get_or_404(team_id)
    
    # Only owner or admin can add members
    current_user = User.query.get(current_user_id)
    role = team.get_member_role(current_user) if current_user in team.members else None
    if team.owner_id != current_user_id and role not in ['owner', 'admin']:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        data = team_member_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    user = User.query.get_or_404(data['user_id'])
    member_role = data.get('role', 'member')
    
    # Don't allow changing owner role
    if member_role == 'owner' and team.owner_id != current_user_id:
        return jsonify({'error': 'Only current owner can assign owner role'}), 403
    
    team.add_member(user, member_role)
    
    # Create notification
    create_notification(
        user_id=user.id,
        type=Notification.TYPE_TEAM_INVITE,
        title=f'Added to team: {team.name}',
        message=f'You have been added to team "{team.name}"',
        team_id=team.id
    )
    db.session.commit()
    
    return jsonify({'message': 'Member added successfully'}), 201

@teams_bp.route('/<int:team_id>/members/<int:user_id>', methods=['DELETE'])
@jwt_required()
def remove_team_member(team_id, user_id):
    """
    Remove a member from team
    ---
    tags:
      - Teams
    security:
      - Bearer: []
    parameters:
      - in: path
        name: team_id
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
    team = Team.query.get_or_404(team_id)
    
    # Only owner or admin can remove members
    current_user = User.query.get(current_user_id)
    role = team.get_member_role(current_user) if current_user in team.members else None
    if team.owner_id != current_user_id and role not in ['owner', 'admin']:
        return jsonify({'error': 'Access denied'}), 403
    
    # Cannot remove owner
    if team.owner_id == user_id:
        return jsonify({'error': 'Cannot remove team owner'}), 400
    
    user = User.query.get_or_404(user_id)
    team.remove_member(user)
    
    return '', 204
