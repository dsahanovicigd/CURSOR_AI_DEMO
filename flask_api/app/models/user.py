from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import json

class User(db.Model):
    """User model for customer support system"""
    __tablename__ = 'users'
    
    # Role options
    ROLE_CUSTOMER = 'customer'
    ROLE_AGENT = 'agent'
    ROLE_ADMIN = 'admin'
    
    # Availability status (for agents)
    AVAILABILITY_AVAILABLE = 'available'
    AVAILABILITY_BUSY = 'busy'
    AVAILABILITY_OFFLINE = 'offline'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(200), nullable=True)  # Full name
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(20), default=ROLE_CUSTOMER, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)  # Legacy field, use role instead
    
    # Agent-specific fields
    availability_status = db.Column(db.String(20), default=AVAILABILITY_AVAILABLE, nullable=True)
    expertise_areas = db.Column(db.JSON, nullable=True)  # Array of expertise categories
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def full_name(self):
        """Get full name"""
        if self.name:
            return self.name
        if self.first_name or self.last_name:
            return f"{self.first_name or ''} {self.last_name or ''}".strip()
        return self.username
    
    def is_customer(self):
        """Check if user is a customer"""
        return self.role == self.ROLE_CUSTOMER
    
    def is_agent(self):
        """Check if user is an agent"""
        return self.role == self.ROLE_AGENT
    
    def is_admin_user(self):
        """Check if user is an admin"""
        return self.role == self.ROLE_ADMIN or self.is_admin
    
    def get_open_ticket_count(self):
        """Get count of open tickets assigned to this agent"""
        if not self.is_agent():
            return 0
        from app.models.ticket import Ticket
        from sqlalchemy import or_
        return Ticket.query.filter(
            Ticket.assigned_to_id == self.id,
            or_(
                Ticket.status == Ticket.STATUS_ASSIGNED,
                Ticket.status == Ticket.STATUS_IN_PROGRESS
            )
        ).count()
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.full_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'is_active': self.is_active,
            'is_admin': self.is_admin or self.is_admin_user(),
            'availability_status': self.availability_status if self.is_agent() else None,
            'expertise_areas': self.expertise_areas if self.is_agent() else None,
            'open_ticket_count': self.get_open_ticket_count() if self.is_agent() else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'
