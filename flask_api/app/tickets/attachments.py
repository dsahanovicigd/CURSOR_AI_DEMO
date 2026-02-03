from flask import request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app import db
from app.tickets import tickets_bp
from app.models.ticket import Ticket
from app.models.ticket_comment import TicketComment
from app.models.ticket_attachment import TicketAttachment
from app.models.user import User
import os
import uuid

UPLOAD_FOLDER = 'uploads/tickets'
MAX_FILE_SIZE = TicketAttachment.MAX_FILE_SIZE
ALLOWED_EXTENSIONS = TicketAttachment.ALLOWED_EXTENSIONS

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_ticket_access(ticket, current_user):
    """Check if user has access to ticket"""
    if current_user.is_admin_user():
        return True
    if current_user.is_agent():
        return ticket.assigned_to_id == current_user.id or ticket.assigned_to_id is None
    return ticket.customer_email == current_user.email

@tickets_bp.route('/<int:ticket_id>/attachments', methods=['POST'])
@jwt_required()
def upload_ticket_attachment(ticket_id):
    """
    Upload attachment to a ticket
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
      - in: formData
        name: file
        type: file
        required: true
      - in: formData
        name: comment_id
        type: integer
    responses:
      201:
        description: Attachment uploaded successfully
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
    
    # Check if file is present
    if 'file' not in request.files:
        return jsonify({
            'status': 'error',
            'message': 'No file provided',
            'code': 'VALIDATION_ERROR'
        }), 400
    
    file = request.files['file']
    comment_id = request.form.get('comment_id', type=int)
    
    if file.filename == '':
        return jsonify({
            'status': 'error',
            'message': 'No file selected',
            'code': 'VALIDATION_ERROR'
        }), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            'status': 'error',
            'message': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}',
            'code': 'VALIDATION_ERROR'
        }), 400
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        return jsonify({
            'status': 'error',
            'message': f'File size exceeds maximum of {MAX_FILE_SIZE / (1024*1024)}MB',
            'code': 'VALIDATION_ERROR'
        }), 400
    
    # Check max attachments per ticket (3 per ticket)
    existing_count = TicketAttachment.query.filter_by(ticket_id=ticket_id).count()
    if existing_count >= 3:
        return jsonify({
            'status': 'error',
            'message': 'Maximum 3 attachments per ticket',
            'code': 'VALIDATION_ERROR'
        }), 400
    
    # Create upload directory if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Generate unique filename
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    
    # Save file
    file.save(file_path)
    
    # Get MIME type
    import mimetypes
    mime_type, _ = mimetypes.guess_type(filename)
    if not mime_type:
        mime_type = 'application/octet-stream'
    
    # Create attachment record
    attachment = TicketAttachment(
        ticket_id=ticket_id,
        comment_id=comment_id,
        filename=filename,
        file_path=file_path,
        file_size=file_size,
        file_type=mime_type,
        uploaded_by_id=current_user_id if current_user else None,
        customer_email=current_user.email if current_user else ticket.customer_email
    )
    
    db.session.add(attachment)
    db.session.commit()
    
    return jsonify(attachment.to_dict()), 201

@tickets_bp.route('/<int:ticket_id>/attachments', methods=['GET'])
@jwt_required()
def get_ticket_attachments(ticket_id):
    """
    Get all attachments for a ticket
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
        description: List of attachments
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
    
    attachments = TicketAttachment.query.filter_by(ticket_id=ticket_id).all()
    
    return jsonify({
        'attachments': [a.to_dict() for a in attachments]
    }), 200

@tickets_bp.route('/attachments/<int:attachment_id>', methods=['GET'])
@jwt_required()
def download_attachment(attachment_id):
    """
    Download an attachment
    ---
    tags:
      - Tickets
    security:
      - Bearer: []
    parameters:
      - in: path
        name: attachment_id
        type: integer
        required: true
    responses:
      200:
        description: File download
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    attachment = TicketAttachment.query.get_or_404(attachment_id)
    ticket = attachment.ticket
    
    # Check access
    if not check_ticket_access(ticket, current_user):
        return jsonify({
            'status': 'error',
            'message': 'Access denied',
            'code': 'FORBIDDEN'
        }), 403
    
    if not os.path.exists(attachment.file_path):
        return jsonify({
            'status': 'error',
            'message': 'File not found',
            'code': 'NOT_FOUND'
        }), 404
    
    return send_file(
        attachment.file_path,
        as_attachment=True,
        download_name=attachment.filename,
        mimetype=attachment.file_type
    )

@tickets_bp.route('/attachments/<int:attachment_id>', methods=['DELETE'])
@jwt_required()
def delete_attachment(attachment_id):
    """
    Delete an attachment
    ---
    tags:
      - Tickets
    security:
      - Bearer: []
    parameters:
      - in: path
        name: attachment_id
        type: integer
        required: true
    responses:
      204:
        description: Attachment deleted successfully
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    attachment = TicketAttachment.query.get_or_404(attachment_id)
    ticket = attachment.ticket
    
    # Check access - only admins or uploader can delete
    if not (current_user.is_admin_user() or 
            (attachment.uploaded_by_id == current_user_id) or
            check_ticket_access(ticket, current_user)):
        return jsonify({
            'status': 'error',
            'message': 'Access denied',
            'code': 'FORBIDDEN'
        }), 403
    
    # Delete file
    if os.path.exists(attachment.file_path):
        os.remove(attachment.file_path)
    
    db.session.delete(attachment)
    db.session.commit()
    
    return '', 204
