from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.agents import agents_bp
from app.models.user import User
from app.models.ticket import Ticket
from app.schemas.user import UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@agents_bp.route('', methods=['GET'])
@jwt_required()
def get_agents():
    """
    Get all agents
    ---
    tags:
      - Agents
    security:
      - Bearer: []
    responses:
      200:
        description: List of agents
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Only admins and agents can view agents list
    if not (current_user.is_admin_user() or current_user.is_agent()):
        return jsonify({
            'status': 'error',
            'message': 'Access denied',
            'code': 'FORBIDDEN'
        }), 403
    
    agents = User.query.filter_by(role=User.ROLE_AGENT, is_active=True).all()
    
    return jsonify({
        'agents': users_schema.dump(agents)
    }), 200

@agents_bp.route('/<int:agent_id>/tickets', methods=['GET'])
@jwt_required()
def get_agent_tickets(agent_id):
    """
    Get tickets assigned to an agent
    ---
    tags:
      - Agents
    security:
      - Bearer: []
    parameters:
      - in: path
        name: agent_id
        type: integer
        required: true
      - in: query
        name: status
        type: string
      - in: query
        name: page
        type: integer
        default: 1
    responses:
      200:
        description: List of agent's tickets
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    agent = User.query.get_or_404(agent_id)
    
    # Verify agent is actually an agent
    if not agent.is_agent():
        return jsonify({
            'status': 'error',
            'message': 'User is not an agent',
            'code': 'NOT_FOUND'
        }), 404
    
    # Only admins or the agent themselves can view
    if not (current_user.is_admin_user() or current_user_id == agent_id):
        return jsonify({
            'status': 'error',
            'message': 'Access denied',
            'code': 'FORBIDDEN'
        }), 403
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    per_page = min(per_page, 100)
    
    query = Ticket.query.filter_by(assigned_to_id=agent_id)
    
    if status:
        query = query.filter_by(status=status)
    
    tickets = query.order_by(Ticket.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    from app.schemas.ticket import TicketSchema
    ticket_schema = TicketSchema(many=True)
    
    return jsonify({
        'tickets': ticket_schema.dump(tickets.items),
        'pagination': {
            'page': tickets.page,
            'pages': tickets.pages,
            'per_page': tickets.per_page,
            'total': tickets.total
        }
    }), 200

@agents_bp.route('/<int:agent_id>/availability', methods=['PUT'])
@jwt_required()
def update_agent_availability(agent_id):
    """
    Update agent availability status
    ---
    tags:
      - Agents
    security:
      - Bearer: []
    parameters:
      - in: path
        name: agent_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          required:
            - availability_status
          properties:
            availability_status:
              type: string
              enum: [available, busy, offline]
    responses:
      200:
        description: Availability updated successfully
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    agent = User.query.get_or_404(agent_id)
    
    # Only admins or the agent themselves can update
    if not (current_user.is_admin_user() or current_user_id == agent_id):
        return jsonify({
            'status': 'error',
            'message': 'Access denied',
            'code': 'FORBIDDEN'
        }), 403
    
    if not agent.is_agent():
        return jsonify({
            'status': 'error',
            'message': 'User is not an agent',
            'code': 'VALIDATION_ERROR'
        }), 400
    
    availability_status = request.json.get('availability_status')
    if availability_status not in [User.AVAILABILITY_AVAILABLE, User.AVAILABILITY_BUSY, User.AVAILABILITY_OFFLINE]:
        return jsonify({
            'status': 'error',
            'message': 'Invalid availability status',
            'code': 'VALIDATION_ERROR'
        }), 400
    
    agent.availability_status = availability_status
    db.session.commit()
    
    return jsonify(user_schema.dump(agent)), 200
