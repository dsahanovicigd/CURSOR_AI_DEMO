from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.ticket_comments import ticket_comments_bp
from app.models.ticket import Ticket
from app.models.ticket_comment import TicketComment
from app.models.user import User
from app.models.notification import Notification
from app.schemas.ticket_comment import TicketCommentSchema, TicketCommentCreateSchema
from app.services.email_service import EmailService
from app.utils.sanitize import sanitize_user_input
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

comment_schema = TicketCommentSchema()
comments_schema = TicketCommentSchema(many=True)
comment_create_schema = TicketCommentCreateSchema()

def check_ticket_access(ticket, current_user):
    """Check if user has access to ticket"""
    if current_user.is_admin_user():
        return True
    if current_user.is_agent():
        return ticket.assigned_to_id == current_user.id or ticket.assigned_to_id is None
    return ticket.customer_email == current_user.email

def create_notification(user_id, type, title, message, **kwargs):
    """Helper function to create notifications"""
    notification = Notification(
        user_id=user_id,
        type=type,
        title=title,
        message=message,
        meta_data=kwargs.get('metadata')
    )
    db.session.add(notification)
    return notification

@ticket_comments_bp.route('/tickets/<int:ticket_id>/comments', methods=['GET'])
@jwt_required()
def get_ticket_comments(ticket_id):
    """
    Get all comments for a ticket
    ---
    tags:
      - Ticket Comments
    security:
      - Bearer: []
    parameters:
      - in: path
        name: ticket_id
        type: integer
        required: true
      - in: query
        name: include_internal
        type: boolean
        default: false
    responses:
      200:
        description: List of comments
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
    
    include_internal = request.args.get('include_internal', 'false').lower() == 'true'
    
    # Customers can't see internal comments
    if current_user.is_customer():
        query = TicketComment.query.filter_by(ticket_id=ticket_id, is_internal=False)
    elif include_internal or current_user.is_agent() or current_user.is_admin_user():
        query = TicketComment.query.filter_by(ticket_id=ticket_id)
    else:
        query = TicketComment.query.filter_by(ticket_id=ticket_id, is_internal=False)
    
    comments = query.order_by(TicketComment.created_at.asc()).all()
    
    return jsonify({
        'comments': comments_schema.dump(comments)
    }), 200

@ticket_comments_bp.route('/tickets/<int:ticket_id>/comments', methods=['POST'])
def create_ticket_comment(ticket_id):
    """
    Create a comment on a ticket
    ---
    tags:
      - Ticket Comments
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
            - content
          properties:
            content:
              type: string
            is_internal:
              type: boolean
            customer_email:
              type: string
    responses:
      201:
        description: Comment created successfully
    """
    ticket = Ticket.query.get_or_404(ticket_id)
    
    # Sanitize user input to prevent XSS
    sanitized_data = sanitize_user_input(request.json, ['content'])
    
    try:
        data = comment_create_schema.load(sanitized_data)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Validation failed',
            'code': 'VALIDATION_ERROR',
            'errors': str(e)
        }), 400
    
    # Determine user_id and customer_email
    user_id = None
    customer_email = None
    
    try:
        from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
        verify_jwt_in_request(optional=True)
        current_user_id = get_jwt_identity()
        if current_user_id:
            current_user = User.query.get(current_user_id)
            user_id = current_user_id
            customer_email = current_user.email
            
            # Agents/admins can create internal comments
            if data.get('is_internal') and not (current_user.is_agent() or current_user.is_admin_user()):
                return jsonify({
                    'status': 'error',
                    'message': 'Only agents and admins can create internal comments',
                    'code': 'FORBIDDEN'
                }), 403
    except:
        # Customer comment without account
        customer_email = data.get('customer_email') or ticket.customer_email
        if not customer_email:
            return jsonify({
                'status': 'error',
                'message': 'customer_email required for unauthenticated comments',
                'code': 'VALIDATION_ERROR'
            }), 400
    
    comment = TicketComment(
        ticket_id=ticket_id,
        user_id=user_id,
        content=data['content'],
        is_internal=data.get('is_internal', False),
        customer_email=customer_email
    )
    
    db.session.add(comment)
    
    # Update ticket updated_at
    ticket.updated_at = datetime.utcnow()
    
    # Track first response
    if not ticket.first_response_at:
        ticket.first_response_at = datetime.utcnow()
    
    db.session.commit()
    
    # Get commenter name for notifications
    commenter_name = "Customer"
    if user_id:
        commenter = User.query.get(user_id)
        commenter_name = commenter.full_name if commenter else "User"
    else:
        commenter_name = customer_email or "Customer"
    
    # Create notifications
    # Notify assigned agent if comment is from customer
    if ticket.assigned_to_id and not user_id:  # Customer comment
        create_notification(
            user_id=ticket.assigned_to_id,
            type=Notification.TYPE_TASK_COMMENT,
            title=f'New comment on ticket: {ticket.ticket_number}',
            message=f'New comment added to ticket "{ticket.ticket_number}: {ticket.subject}"',
            metadata={'ticket_id': ticket.id, 'comment_id': comment.id}
        )
    
    db.session.commit()
    
    # Send email notifications (FR-018, FR-035)
    try:
        EmailService.send_comment_notification(ticket, comment, commenter_name)
    except Exception as e:
        logger.error(f"Failed to send comment notification email: {str(e)}")
    
    return jsonify(comment_schema.dump(comment)), 201
