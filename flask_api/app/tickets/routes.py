from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.tickets import tickets_bp
from app.models.ticket import Ticket
from app.models.user import User
from app.models.ticket_assignment import TicketAssignment
from app.models.ticket_status_history import TicketStatusHistory
from app.models.notification import Notification
from app.schemas.ticket import (
    TicketSchema, TicketCreateSchema, TicketUpdateSchema,
    TicketStatusUpdateSchema, TicketPriorityUpdateSchema, TicketAssignSchema
)
from app.services.email_service import EmailService
from app.utils.sanitize import sanitize_user_input
from sqlalchemy import or_, and_, func
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
import re
import logging

logger = logging.getLogger(__name__)

ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)
ticket_create_schema = TicketCreateSchema()
ticket_update_schema = TicketUpdateSchema()
ticket_status_schema = TicketStatusUpdateSchema()
ticket_priority_schema = TicketPriorityUpdateSchema()
ticket_assign_schema = TicketAssignSchema()

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

def check_ticket_access(ticket, current_user):
    """Check if user has access to ticket"""
    if current_user.is_admin_user():
        return True
    if current_user.is_agent():
        # Agents can see assigned tickets or unassigned tickets
        return ticket.assigned_to_id == current_user.id or ticket.assigned_to_id is None
    # Customers can only see their own tickets
    return ticket.customer_email == current_user.email

def auto_assign_ticket(ticket, category=None):
    """Auto-assign ticket to agent based on workload and expertise"""
    # Get available agents
    agents = User.query.filter_by(
        role=User.ROLE_AGENT,
        is_active=True,
        availability_status=User.AVAILABILITY_AVAILABLE
    ).all()
    
    if not agents:
        # If no available agents, get any active agent
        agents = User.query.filter_by(role=User.ROLE_AGENT, is_active=True).all()
    
    if not agents:
        return None
    
    # Find agent with least open tickets
    best_agent = None
    min_tickets = float('inf')
    
    for agent in agents:
        # Check if agent has expertise in this category
        if category and agent.expertise_areas:
            if category not in agent.expertise_areas:
                continue
        
        open_count = agent.get_open_ticket_count()
        if open_count < min_tickets:
            min_tickets = open_count
            best_agent = agent
    
    return best_agent if best_agent else agents[0]

@tickets_bp.route('', methods=['GET'])
@jwt_required()
def get_tickets():
    """
    Get all tickets with filters
    ---
    tags:
      - Tickets
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
      - in: query
        name: priority
        type: string
      - in: query
        name: category
        type: string
      - in: query
        name: assigned_to_id
        type: integer
      - in: query
        name: customer_email
        type: string
      - in: query
        name: search
        type: string
      - in: query
        name: date_from
        type: string
        format: date
      - in: query
        name: date_to
        type: string
        format: date
    responses:
      200:
        description: List of tickets
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    priority = request.args.get('priority')
    category = request.args.get('category')
    assigned_to_id = request.args.get('assigned_to_id', type=int)
    customer_email = request.args.get('customer_email')
    search = request.args.get('search')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    per_page = min(per_page, 100)
    
    # Build query based on user role
    if current_user.is_admin_user():
        query = Ticket.query
    elif current_user.is_agent():
        # Agents see assigned tickets + unassigned queue
        query = Ticket.query.filter(
            or_(
                Ticket.assigned_to_id == current_user_id,
                Ticket.assigned_to_id.is_(None)
            )
        )
    else:
        # Customers see only their own tickets
        query = Ticket.query.filter_by(customer_email=current_user.email)
    
    # Apply filters
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if category:
        query = query.filter_by(category=category)
    if assigned_to_id:
        query = query.filter_by(assigned_to_id=assigned_to_id)
    if customer_email:
        query = query.filter_by(customer_email=customer_email)
    
    # Search
    if search:
        search_term = f'%{search}%'
        query = query.filter(
            or_(
                Ticket.ticket_number.like(search_term),
                Ticket.subject.like(search_term),
                Ticket.description.like(search_term),
                Ticket.customer_email.like(search_term)
            )
        )
    
    # Date range
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(Ticket.created_at >= date_from_obj)
        except ValueError:
            pass
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(Ticket.created_at < date_to_obj)
        except ValueError:
            pass
    
    # Use eager loading to prevent N+1 queries
    query = query.options(
        joinedload(Ticket.assigned_to),
        joinedload(Ticket.created_by)
    )
    
    tickets = query.order_by(Ticket.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'tickets': tickets_schema.dump(tickets.items),
        'pagination': {
            'page': tickets.page,
            'pages': tickets.pages,
            'per_page': tickets.per_page,
            'total': tickets.total
        }
    }), 200

@tickets_bp.route('', methods=['POST'])
def create_ticket():
    # Rate limiting applied via Flask-Limiter default limits (100/min)
    # Can be customized per endpoint if needed
    """
    Create a new support ticket
    ---
    tags:
      - Tickets
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - subject
            - description
            - category
            - customer_email
          properties:
            subject:
              type: string
            description:
              type: string
            priority:
              type: string
              enum: [low, medium, high, urgent]
            category:
              type: string
              enum: [technical, billing, general, feature_request]
            customer_email:
              type: string
              format: email
    responses:
      201:
        description: Ticket created successfully
      400:
        description: Validation error
    """
    if not request.json:
        return jsonify({
            'status': 'error',
            'message': 'Request body is required',
            'code': 'VALIDATION_ERROR',
            'errors': {'body': ['Request body cannot be empty']}
        }), 400
    
    # Sanitize user input to prevent XSS
    sanitized_data = sanitize_user_input(request.json, ['subject', 'description'])
    
    try:
        data = ticket_create_schema.load(sanitized_data)
    except Exception as e:
        error_messages = {}
        if hasattr(e, 'messages'):
            error_messages = e.messages
        else:
            error_messages = {'general': [str(e)]}
        
        return jsonify({
            'status': 'error',
            'message': 'Validation failed',
            'code': 'VALIDATION_ERROR',
            'errors': error_messages
        }), 400
    
    # Generate ticket number
    ticket_number = Ticket.generate_ticket_number()
    
    # Get created_by if user is authenticated
    created_by_id = None
    current_user_id = None
    try:
        from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
        verify_jwt_in_request(optional=True)
        current_user_id = get_jwt_identity()
        if current_user_id:
            created_by_id = current_user_id
    except:
        pass
    
    ticket = Ticket(
        ticket_number=ticket_number,
        subject=data['subject'],
        description=data['description'],
        priority=data.get('priority', Ticket.PRIORITY_MEDIUM),
        category=data['category'],
        customer_email=data['customer_email'],
        created_by_id=created_by_id,
        status=Ticket.STATUS_OPEN
    )
    
    # Calculate SLA deadlines
    ticket.calculate_sla_deadlines()
    
    db.session.add(ticket)
    db.session.flush()
    
    # Auto-assign if enabled
    assigned_agent = auto_assign_ticket(ticket, ticket.category)
    if assigned_agent:
        ticket.assigned_to_id = assigned_agent.id
        ticket.status = Ticket.STATUS_ASSIGNED
        
        # Create assignment record
        assignment = TicketAssignment(
            ticket_id=ticket.id,
            assigned_to_id=assigned_agent.id,
            assigned_by_id=None,  # Auto-assigned
            notes='Auto-assigned based on workload'
        )
        db.session.add(assignment)
        
        # Create notification
        create_notification(
            user_id=assigned_agent.id,
            type=Notification.TYPE_TASK_ASSIGNED,
            title=f'New ticket assigned: {ticket.ticket_number}',
            message=f'You have been assigned ticket "{ticket.ticket_number}: {ticket.subject}"',
            metadata={'ticket_id': ticket.id, 'ticket_number': ticket.ticket_number}
        )
    
    # Create status history
    status_history = TicketStatusHistory(
        ticket_id=ticket.id,
        old_status=None,
        new_status=ticket.status,
        changed_by_id=created_by_id,
        notes='Ticket created'
    )
    db.session.add(status_history)
    
    db.session.commit()
    
    # Send email confirmation to customer (FR-003, FR-035)
    try:
        EmailService.send_ticket_created_notification(ticket)
    except Exception as e:
        logger.error(f"Failed to send ticket creation email: {str(e)}")
        # Don't fail the request if email fails
    
    # Send assignment notification if auto-assigned (FR-007, FR-035)
    if assigned_agent:
        try:
            EmailService.send_ticket_assigned_notification(ticket, assigned_agent)
        except Exception as e:
            logger.error(f"Failed to send assignment email: {str(e)}")
    
    return jsonify(ticket_schema.dump(ticket)), 201

@tickets_bp.route('/<int:ticket_id>', methods=['GET'])
@jwt_required()
def get_ticket(ticket_id):
    """
    Get a specific ticket
    ---
    tags:
      - Tickets
    security:
      - Bearer: []
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
    responses:
      200:
        description: Ticket details
      403:
        description: Access denied
      404:
        description: Ticket not found
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    ticket = Ticket.query.get_or_404(ticket_id)
    
    # Check access
    if not check_ticket_access(ticket, current_user):
        return jsonify({
            'status': 'error',
            'message': 'Access denied',
            'code': 'FORBIDDEN'
        }), 403
    
    return jsonify(ticket_schema.dump(ticket)), 200

@tickets_bp.route('/<int:ticket_id>', methods=['PUT'])
@jwt_required()
def update_ticket(ticket_id):
    """
    Update a ticket
    ---
    tags:
      - Tickets
    security:
      - Bearer: []
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            subject:
              type: string
            description:
              type: string
            priority:
              type: string
            category:
              type: string
    responses:
      200:
        description: Ticket updated successfully
      403:
        description: Access denied
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    ticket = Ticket.query.get_or_404(ticket_id)
    
    # Only agents and admins can update tickets
    if not (current_user.is_agent() or current_user.is_admin_user()):
        return jsonify({
            'status': 'error',
            'message': 'Access denied',
            'code': 'FORBIDDEN'
        }), 403
    
    try:
        data = ticket_update_schema.load(request.json, partial=True)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Validation failed',
            'code': 'VALIDATION_ERROR',
            'errors': str(e)
        }), 400
    
    # Update fields
    if 'subject' in data:
        ticket.subject = data['subject']
    if 'description' in data:
        ticket.description = data['description']
    if 'category' in data:
        ticket.category = data['category']
    if 'priority' in data:
        old_priority = ticket.priority
        ticket.priority = data['priority']
        ticket.calculate_sla_deadlines()  # Recalculate SLA
    
    db.session.commit()
    
    return jsonify(ticket_schema.dump(ticket)), 200

@tickets_bp.route('/<int:ticket_id>', methods=['DELETE'])
@jwt_required()
def delete_ticket(ticket_id):
    """
    Delete a ticket (admin only)
    ---
    tags:
      - Tickets
    security:
      - Bearer: []
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
    responses:
      204:
        description: Ticket deleted successfully
      403:
        description: Access denied
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Only admins can delete tickets
    if not current_user.is_admin_user():
        return jsonify({
            'status': 'error',
            'message': 'Access denied',
            'code': 'FORBIDDEN'
        }), 403
    
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    
    return '', 204

@tickets_bp.route('/<int:ticket_id>/status', methods=['PUT'])
@jwt_required()
def update_ticket_status(ticket_id):
    """
    Update ticket status
    ---
    tags:
      - Tickets
    security:
      - Bearer: []
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          required:
            - status
          properties:
            status:
              type: string
            notes:
              type: string
    responses:
      200:
        description: Status updated successfully
      400:
        description: Invalid status transition
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    ticket = Ticket.query.get_or_404(ticket_id)
    
    # Check access
    if not check_ticket_access(ticket, current_user):
        return jsonify({
            'status': 'error',
            'message': 'Access denied',
            'code': 'FORBIDDEN'
        }), 403
    
    # Only agents and admins can change status
    if not (current_user.is_agent() or current_user.is_admin_user()):
        return jsonify({
            'status': 'error',
            'message': 'Access denied',
            'code': 'FORBIDDEN'
        }), 403
    
    try:
        data = ticket_status_schema.load(request.json)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Validation failed',
            'code': 'VALIDATION_ERROR',
            'errors': str(e)
        }), 400
    
    new_status = data['status']
    
    # Check if transition is allowed
    if not ticket.can_transition_to(new_status):
        return jsonify({
            'status': 'error',
            'message': f'Invalid status transition from {ticket.status} to {new_status}',
            'code': 'VALIDATION_ERROR'
        }), 400
    
    # Special handling for reopened
    if new_status == Ticket.STATUS_REOPENED:
        if not ticket.can_reopen():
            return jsonify({
                'status': 'error',
                'message': 'Cannot reopen ticket closed more than 7 days ago',
                'code': 'VALIDATION_ERROR'
            }), 400
        ticket.reopened_at = datetime.utcnow()
    
    # Track first response
    if not ticket.first_response_at and new_status in [Ticket.STATUS_ASSIGNED, Ticket.STATUS_IN_PROGRESS]:
        ticket.first_response_at = datetime.utcnow()
    
    # Track resolution
    if new_status == Ticket.STATUS_RESOLVED and not ticket.resolved_at:
        ticket.resolved_at = datetime.utcnow()
    
    # Track closure
    if new_status == Ticket.STATUS_CLOSED and not ticket.closed_at:
        ticket.closed_at = datetime.utcnow()
    
    old_status = ticket.status
    ticket.status = new_status
    
    # Create status history
    status_history = TicketStatusHistory(
        ticket_id=ticket.id,
        old_status=old_status,
        new_status=new_status,
        changed_by_id=current_user_id,
        notes=data.get('notes')
    )
    db.session.add(status_history)
    
    db.session.commit()
    
    # Send status change notifications (FR-014, FR-035)
    try:
        EmailService.send_status_change_notification(ticket, old_status, current_user)
    except Exception as e:
        logger.error(f"Failed to send status change email: {str(e)}")
    
    return jsonify(ticket_schema.dump(ticket)), 200

@tickets_bp.route('/<int:ticket_id>/priority', methods=['PUT'])
@jwt_required()
def update_ticket_priority(ticket_id):
    """
    Update ticket priority
    ---
    tags:
      - Tickets
    security:
      - Bearer: []
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          required:
            - priority
            - reason
          properties:
            priority:
              type: string
            reason:
              type: string
    responses:
      200:
        description: Priority updated successfully
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    ticket = Ticket.query.get_or_404(ticket_id)
    
    # Only agents and admins can change priority
    if not (current_user.is_agent() or current_user.is_admin_user()):
        return jsonify({
            'status': 'error',
            'message': 'Access denied',
            'code': 'FORBIDDEN'
        }), 403
    
    try:
        data = ticket_priority_schema.load(request.json)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Validation failed',
            'code': 'VALIDATION_ERROR',
            'errors': str(e)
        }), 400
    
    old_priority = ticket.priority
    ticket.priority = data['priority']
    ticket.calculate_sla_deadlines()  # Recalculate SLA
    
    # Create comment with priority change reason
    from app.models.ticket_comment import TicketComment
    comment = TicketComment(
        ticket_id=ticket.id,
        user_id=current_user_id,
        content=f"Priority changed from {old_priority} to {ticket.priority}. Reason: {data['reason']}",
        is_internal=True
    )
    db.session.add(comment)
    
    db.session.commit()
    
    return jsonify(ticket_schema.dump(ticket)), 200

@tickets_bp.route('/<int:ticket_id>/assign', methods=['POST'])
@jwt_required()
def assign_ticket(ticket_id):
    """
    Assign ticket to agent
    ---
    tags:
      - Tickets
    security:
      - Bearer: []
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          required:
            - assigned_to_id
          properties:
            assigned_to_id:
              type: integer
            notes:
              type: string
    responses:
      200:
        description: Ticket assigned successfully
      403:
        description: Access denied
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Only admins can assign tickets (per PRD FR-005, FR-009)
    if not current_user.is_admin_user():
        return jsonify({
            'status': 'error',
            'message': 'Access denied. Only administrators can assign tickets. Please login with an admin account.',
            'code': 'FORBIDDEN'
        }), 403
    
    ticket = Ticket.query.get_or_404(ticket_id)
    
    try:
        data = ticket_assign_schema.load(request.json)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Validation failed',
            'code': 'VALIDATION_ERROR',
            'errors': str(e)
        }), 400
    
    agent = User.query.get_or_404(data['assigned_to_id'])
    
    # Verify agent is actually an agent
    if not agent.is_agent():
        return jsonify({
            'status': 'error',
            'message': 'User is not an agent',
            'code': 'VALIDATION_ERROR'
        }), 400
    
    # Deactivate previous assignments
    TicketAssignment.query.filter_by(ticket_id=ticket.id, is_active=True).update({'is_active': False, 'unassigned_at': datetime.utcnow()})
    
    # Update ticket
    old_assigned_to = ticket.assigned_to_id
    ticket.assigned_to_id = agent.id
    if ticket.status == Ticket.STATUS_OPEN:
        ticket.status = Ticket.STATUS_ASSIGNED
    
    # Create assignment record
    assignment = TicketAssignment(
        ticket_id=ticket.id,
        assigned_to_id=agent.id,
        assigned_by_id=current_user_id,
        notes=data.get('notes')
    )
    db.session.add(assignment)
    
    # Create status history
    status_history = TicketStatusHistory(
        ticket_id=ticket.id,
        old_status=ticket.status,
        new_status=ticket.status,
        changed_by_id=current_user_id,
        notes=f'Ticket assigned to {agent.name or agent.username}'
    )
    db.session.add(status_history)
    
    # Create notification
    create_notification(
        user_id=agent.id,
        type=Notification.TYPE_TASK_ASSIGNED,
        title=f'Ticket assigned: {ticket.ticket_number}',
        message=f'You have been assigned ticket "{ticket.ticket_number}: {ticket.subject}"',
        metadata={'ticket_id': ticket.id, 'ticket_number': ticket.ticket_number}
    )
    
    db.session.commit()
    
    # Send assignment notification (FR-007, FR-035)
    try:
        EmailService.send_ticket_assigned_notification(ticket, agent)
    except Exception as e:
        logger.error(f"Failed to send assignment email: {str(e)}")
    
    return jsonify(ticket_schema.dump(ticket)), 200

@tickets_bp.route('/<int:ticket_id>/history', methods=['GET'])
@jwt_required()
def get_ticket_history(ticket_id):
    """
    Get ticket history (status changes and assignments)
    ---
    tags:
      - Tickets
    security:
      - Bearer: []
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
    responses:
      200:
        description: Ticket history
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    ticket = Ticket.query.get_or_404(ticket_id)
    
    # Check access
    if not check_ticket_access(ticket, current_user):
        return jsonify({
            'status': 'error',
            'message': 'Access denied',
            'code': 'FORBIDDEN'
        }), 403
    
    # Get status history
    status_history = TicketStatusHistory.query.filter_by(ticket_id=ticket_id).order_by(TicketStatusHistory.changed_at.desc()).all()
    
    # Get assignment history
    assignment_history = TicketAssignment.query.filter_by(ticket_id=ticket_id).order_by(TicketAssignment.assigned_at.desc()).all()
    
    return jsonify({
        'status_history': [h.to_dict() for h in status_history],
        'assignment_history': [a.to_dict() for a in assignment_history]
    }), 200
