from datetime import datetime
from app import db

class TicketAssignment(db.Model):
    """Assignment history model for tickets"""
    __tablename__ = 'ticket_assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    unassigned_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    notes = db.Column(db.Text, nullable=True)  # Reason for assignment
    
    # Relationships
    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id], backref='ticket_assignments', lazy=True)
    assigned_by = db.relationship('User', foreign_keys=[assigned_by_id], lazy=True)
    
    # Indexes
    __table_args__ = (
        db.Index('idx_assignment_ticket', 'ticket_id'),
        db.Index('idx_assignment_agent', 'assigned_to_id'),
        db.Index('idx_assignment_active', 'is_active'),
    )
    
    def to_dict(self):
        """Convert assignment to dictionary"""
        return {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'assigned_to_id': self.assigned_to_id,
            'assigned_to_name': self.assigned_to.name if self.assigned_to else None,
            'assigned_by_id': self.assigned_by_id,
            'assigned_by_name': self.assigned_by.name if self.assigned_by else None,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None,
            'unassigned_at': self.unassigned_at.isoformat() if self.unassigned_at else None,
            'is_active': self.is_active,
            'notes': self.notes
        }
    
    def __repr__(self):
        return f'<TicketAssignment {self.id}>'
