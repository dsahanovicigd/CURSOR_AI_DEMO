from datetime import datetime
from app import db
import re
from sqlalchemy import event

class Ticket(db.Model):
    """Ticket model for customer support system"""
    __tablename__ = 'tickets'
    
    # Status options
    STATUS_OPEN = 'open'
    STATUS_ASSIGNED = 'assigned'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_WAITING = 'waiting'
    STATUS_RESOLVED = 'resolved'
    STATUS_CLOSED = 'closed'
    STATUS_REOPENED = 'reopened'
    
    # Priority options
    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'
    PRIORITY_URGENT = 'urgent'
    
    # Category options
    CATEGORY_TECHNICAL = 'technical'
    CATEGORY_BILLING = 'billing'
    CATEGORY_GENERAL = 'general'
    CATEGORY_FEATURE_REQUEST = 'feature_request'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default=STATUS_OPEN, nullable=False)
    priority = db.Column(db.String(20), default=PRIORITY_MEDIUM, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    customer_email = db.Column(db.String(255), nullable=False, index=True)
    
    # Foreign keys
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    resolved_at = db.Column(db.DateTime, nullable=True)
    closed_at = db.Column(db.DateTime, nullable=True)
    reopened_at = db.Column(db.DateTime, nullable=True)
    
    # SLA tracking
    first_response_at = db.Column(db.DateTime, nullable=True)
    sla_response_deadline = db.Column(db.DateTime, nullable=True)
    sla_resolution_deadline = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id], backref='assigned_tickets', lazy=True)
    created_by = db.relationship('User', foreign_keys=[created_by_id], backref='created_tickets', lazy=True)
    comments = db.relationship('TicketComment', backref='ticket', lazy='dynamic', cascade='all, delete-orphan')
    attachments = db.relationship('TicketAttachment', backref='ticket', lazy='dynamic', cascade='all, delete-orphan')
    assignment_history = db.relationship('TicketAssignment', backref='ticket', lazy='dynamic', cascade='all, delete-orphan')
    status_history = db.relationship('TicketStatusHistory', backref='ticket', lazy='dynamic', cascade='all, delete-orphan')
    
    # Indexes
    __table_args__ = (
        db.Index('idx_ticket_status_priority', 'status', 'priority'),
        db.Index('idx_ticket_assigned', 'assigned_to_id', 'status'),
        db.Index('idx_ticket_category', 'category'),
        db.Index('idx_ticket_created', 'created_at'),
        db.Index('idx_ticket_customer', 'customer_email'),
    )
    
    @staticmethod
    def generate_ticket_number():
        """Generate unique ticket number: TICK-YYYYMMDD-XXXX"""
        today = datetime.utcnow().strftime('%Y%m%d')
        # Get the last ticket number for today
        last_ticket = Ticket.query.filter(
            Ticket.ticket_number.like(f'TICK-{today}-%')
        ).order_by(Ticket.ticket_number.desc()).first()
        
        if last_ticket:
            # Extract sequence number
            match = re.search(r'-(\d+)$', last_ticket.ticket_number)
            if match:
                sequence = int(match.group(1)) + 1
            else:
                sequence = 1
        else:
            sequence = 1
        
        return f'TICK-{today}-{sequence:04d}'
    
    def calculate_sla_deadlines(self):
        """Calculate SLA deadlines based on priority"""
        from datetime import timedelta
        
        created = self.created_at or datetime.utcnow()
        
        if self.priority == self.PRIORITY_URGENT:
            self.sla_response_deadline = created + timedelta(hours=2)
            self.sla_resolution_deadline = created + timedelta(hours=24)
        elif self.priority == self.PRIORITY_HIGH:
            self.sla_response_deadline = created + timedelta(hours=4)
            self.sla_resolution_deadline = created + timedelta(hours=48)
        elif self.priority == self.PRIORITY_MEDIUM:
            self.sla_response_deadline = created + timedelta(hours=8)
            self.sla_resolution_deadline = created + timedelta(days=5)
        else:  # LOW
            self.sla_response_deadline = created + timedelta(hours=24)
            self.sla_resolution_deadline = created + timedelta(days=10)
    
    def is_sla_breached(self):
        """Check if SLA deadlines are breached"""
        now = datetime.utcnow()
        if self.sla_response_deadline and not self.first_response_at:
            return now > self.sla_response_deadline
        if self.sla_resolution_deadline and self.status not in [self.STATUS_RESOLVED, self.STATUS_CLOSED]:
            return now > self.sla_resolution_deadline
        return False
    
    def can_transition_to(self, new_status):
        """Check if status transition is allowed"""
        valid_transitions = {
            self.STATUS_OPEN: [self.STATUS_ASSIGNED, self.STATUS_CLOSED],
            self.STATUS_ASSIGNED: [self.STATUS_IN_PROGRESS, self.STATUS_CLOSED],
            self.STATUS_IN_PROGRESS: [self.STATUS_WAITING, self.STATUS_RESOLVED, self.STATUS_CLOSED],
            self.STATUS_WAITING: [self.STATUS_IN_PROGRESS],
            self.STATUS_RESOLVED: [self.STATUS_CLOSED, self.STATUS_REOPENED],
            self.STATUS_CLOSED: [self.STATUS_REOPENED],  # Only within 7 days
            self.STATUS_REOPENED: [self.STATUS_IN_PROGRESS]
        }
        return new_status in valid_transitions.get(self.status, [])
    
    def can_reopen(self):
        """Check if closed ticket can be reopened (within 7 days)"""
        if self.status != self.STATUS_CLOSED or not self.closed_at:
            return False
        days_since_closed = (datetime.utcnow() - self.closed_at).days
        return days_since_closed <= 7
    
    def to_dict(self):
        """Convert ticket to dictionary"""
        return {
            'id': self.id,
            'ticket_number': self.ticket_number,
            'subject': self.subject,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'category': self.category,
            'customer_email': self.customer_email,
            'assigned_to_id': self.assigned_to_id,
            'assigned_to_name': self.assigned_to.name if self.assigned_to else None,
            'created_by_id': self.created_by_id,
            'created_by_name': self.created_by.name if self.created_by else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'closed_at': self.closed_at.isoformat() if self.closed_at else None,
            'reopened_at': self.reopened_at.isoformat() if self.reopened_at else None,
            'first_response_at': self.first_response_at.isoformat() if self.first_response_at else None,
            'sla_response_deadline': self.sla_response_deadline.isoformat() if self.sla_response_deadline else None,
            'sla_resolution_deadline': self.sla_resolution_deadline.isoformat() if self.sla_resolution_deadline else None,
            'is_sla_breached': self.is_sla_breached(),
            'comment_count': self.comments.filter_by(is_internal=False).count(),
            'attachment_count': self.attachments.count()
        }
    
    def __repr__(self):
        return f'<Ticket {self.ticket_number}>'


@event.listens_for(Ticket, 'before_insert')
def generate_ticket_number_before_insert(mapper, connection, target):
    """Ensure ticket_number is always generated before insert (FR-002)"""
    if not target.ticket_number:
        target.ticket_number = Ticket.generate_ticket_number()
