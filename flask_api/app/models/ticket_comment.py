from datetime import datetime
from app import db

class TicketComment(db.Model):
    """Comment model for tickets"""
    __tablename__ = 'ticket_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Nullable for customer comments
    content = db.Column(db.Text, nullable=False)
    is_internal = db.Column(db.Boolean, default=False, nullable=False)  # False = public, True = internal
    customer_email = db.Column(db.String(255), nullable=True)  # For customer comments without user account
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='ticket_comments', lazy=True)
    attachments = db.relationship('TicketAttachment', backref='comment', lazy='dynamic', cascade='all, delete-orphan')
    
    # Indexes
    __table_args__ = (
        db.Index('idx_comment_ticket_created', 'ticket_id', 'created_at'),
        db.Index('idx_comment_internal', 'is_internal'),
    )
    
    def to_dict(self):
        """Convert comment to dictionary"""
        return {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'user_email': self.user.email if self.user else self.customer_email,
            'content': self.content,
            'is_internal': self.is_internal,
            'customer_email': self.customer_email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'attachment_count': self.attachments.count()
        }
    
    def __repr__(self):
        return f'<TicketComment {self.id}>'
