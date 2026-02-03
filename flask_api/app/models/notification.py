from datetime import datetime
from app import db

class Notification(db.Model):
    """Notification model for real-time notifications"""
    __tablename__ = 'notifications'
    
    # Notification types
    TYPE_TASK_ASSIGNED = 'task_assigned'
    TYPE_TASK_COMPLETED = 'task_completed'
    TYPE_TASK_COMMENT = 'task_comment'
    TYPE_PROJECT_INVITE = 'project_invite'
    TYPE_TEAM_INVITE = 'team_invite'
    TYPE_MENTION = 'mention'
    TYPE_DUE_DATE_REMINDER = 'due_date_reminder'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    related_task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=True)
    related_project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    related_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)
    
    # Metadata (renamed to avoid SQLAlchemy reserved word conflict)
    meta_data = db.Column(db.JSON, nullable=True)  # Store additional data as JSON
    
    # Dates
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    read_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', backref='notifications', lazy=True)
    related_task = db.relationship('Task', foreign_keys=[related_task_id], lazy=True)
    related_project = db.relationship('Project', foreign_keys=[related_project_id], lazy=True)
    related_team = db.relationship('Team', foreign_keys=[related_team_id], lazy=True)
    
    # Indexes
    __table_args__ = (
        db.Index('idx_notification_user_read', 'user_id', 'is_read'),
        db.Index('idx_notification_created', 'created_at'),
    )
    
    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.read_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert notification to dictionary"""
        return {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'message': self.message,
            'is_read': self.is_read,
            'user_id': self.user_id,
            'related_task_id': self.related_task_id,
            'related_project_id': self.related_project_id,
            'related_team_id': self.related_team_id,
            'metadata': self.meta_data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None
        }
    
    def __repr__(self):
        return f'<Notification {self.title}>'
