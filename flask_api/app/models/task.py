from datetime import datetime
from app import db

class Task(db.Model):
    """Task model for task management"""
    __tablename__ = 'tasks'
    
    # Task status options
    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    
    # Priority options
    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'
    PRIORITY_URGENT = 'urgent'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default=STATUS_PENDING, nullable=False)
    priority = db.Column(db.String(20), default=PRIORITY_MEDIUM, nullable=False)
    
    # Foreign keys
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Dates
    due_date = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    project = db.relationship('Project', backref='tasks', lazy=True)
    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id], backref='assigned_tasks', lazy=True)
    created_by = db.relationship('User', foreign_keys=[created_by_id], backref='created_tasks', lazy=True)
    comments = db.relationship('TaskComment', backref='task', lazy='dynamic', cascade='all, delete-orphan')
    attachments = db.relationship('TaskAttachment', backref='task', lazy='dynamic', cascade='all, delete-orphan')
    
    # Indexes for performance optimization
    __table_args__ = (
        db.Index('idx_task_project_status', 'project_id', 'status'),
        db.Index('idx_task_assigned_status', 'assigned_to_id', 'status'),
        db.Index('idx_task_due_date', 'due_date'),
        db.Index('idx_task_created_by', 'created_by_id'),
        db.Index('idx_task_priority', 'priority'),
        db.Index('idx_task_created_at', 'created_at'),
        db.Index('idx_task_status_priority', 'status', 'priority'),
        db.Index('idx_task_project_assigned', 'project_id', 'assigned_to_id'),
    )
    
    def mark_completed(self):
        """Mark task as completed"""
        self.status = self.STATUS_COMPLETED
        self.completed_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert task to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'project_id': self.project_id,
            'project_name': self.project.name if self.project else None,
            'assigned_to_id': self.assigned_to_id,
            'assigned_to_name': self.assigned_to.username if self.assigned_to else None,
            'created_by_id': self.created_by_id,
            'created_by_name': self.created_by.username if self.created_by else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'comment_count': self.comments.count(),
            'attachment_count': self.attachments.count()
        }
    
    def __repr__(self):
        return f'<Task {self.title}>'
