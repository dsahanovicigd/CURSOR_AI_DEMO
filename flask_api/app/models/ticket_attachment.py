from datetime import datetime
from app import db

class TicketAttachment(db.Model):
    """Attachment model for tickets and comments"""
    __tablename__ = 'ticket_attachments'
    
    # Allowed file types
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('ticket_comments.id'), nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # Size in bytes
    file_type = db.Column(db.String(50), nullable=False)  # MIME type
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    customer_email = db.Column(db.String(255), nullable=True)  # For customer uploads
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    uploaded_by = db.relationship('User', backref='ticket_attachments', lazy=True)
    
    # Indexes
    __table_args__ = (
        db.Index('idx_attachment_ticket', 'ticket_id'),
        db.Index('idx_attachment_comment', 'comment_id'),
    )
    
    @staticmethod
    def is_allowed_file(filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in TicketAttachment.ALLOWED_EXTENSIONS
    
    def to_dict(self):
        """Convert attachment to dictionary"""
        return {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'comment_id': self.comment_id,
            'filename': self.filename,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'uploaded_by_id': self.uploaded_by_id,
            'uploaded_by_name': self.uploaded_by.name if self.uploaded_by else None,
            'customer_email': self.customer_email,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }
    
    def __repr__(self):
        return f'<TicketAttachment {self.filename}>'
