from datetime import datetime
from app import db

class TicketStatusHistory(db.Model):
    """Status change history model for tickets"""
    __tablename__ = 'ticket_status_history'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    old_status = db.Column(db.String(20), nullable=True)
    new_status = db.Column(db.String(20), nullable=False)
    changed_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    notes = db.Column(db.Text, nullable=True)  # Reason for status change
    
    # Relationships
    changed_by = db.relationship('User', backref='ticket_status_changes', lazy=True)
    
    # Indexes
    __table_args__ = (
        db.Index('idx_status_history_ticket', 'ticket_id'),
        db.Index('idx_status_history_changed_at', 'changed_at'),
    )
    
    def to_dict(self):
        """Convert status history to dictionary"""
        return {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'old_status': self.old_status,
            'new_status': self.new_status,
            'changed_by_id': self.changed_by_id,
            'changed_by_name': self.changed_by.name if self.changed_by else None,
            'changed_at': self.changed_at.isoformat() if self.changed_at else None,
            'notes': self.notes
        }
    
    def __repr__(self):
        return f'<TicketStatusHistory {self.id}>'
