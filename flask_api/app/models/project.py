from datetime import datetime
from app import db

# Association table for many-to-many relationship between projects and users
project_members = db.Table('project_members',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role', db.String(50), default='member'),  # owner, admin, member
    db.Column('joined_at', db.DateTime, default=datetime.utcnow)
)

class Project(db.Model):
    """Project model for project management"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='active', nullable=False)  # active, archived, completed
    
    # Foreign keys
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)
    
    # Dates
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    owner = db.relationship('User', foreign_keys=[owner_id], backref='owned_projects', lazy=True)
    team = db.relationship('Team', backref='projects', lazy=True)
    members = db.relationship('User', secondary=project_members, lazy='dynamic',
                             backref=db.backref('projects', lazy='dynamic'))
    
    # Indexes
    __table_args__ = (
        db.Index('idx_project_owner_status', 'owner_id', 'status'),
        db.Index('idx_project_team', 'team_id'),
    )
    
    def add_member(self, user, role='member'):
        """Add a member to the project"""
        if user not in self.members:
            self.members.append(user)
            db.session.flush()  # Flush to get the association created
            # Update role in association table
            from sqlalchemy import update
            stmt = update(project_members).where(
                db.and_(
                    project_members.c.project_id == self.id,
                    project_members.c.user_id == user.id
                )
            ).values(role=role)
            db.session.execute(stmt)
            db.session.commit()
    
    def remove_member(self, user):
        """Remove a member from the project"""
        if user in self.members:
            self.members.remove(user)
            db.session.commit()
    
    def get_member_role(self, user):
        """Get the role of a member in the project"""
        from sqlalchemy import select
        result = db.session.execute(
            select(project_members.c.role).where(
                db.and_(
                    project_members.c.project_id == self.id,
                    project_members.c.user_id == user.id
                )
            )
        ).first()
        return result[0] if result else None
    
    def to_dict(self):
        """Convert project to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'owner_id': self.owner_id,
            'owner_name': self.owner.username if self.owner else None,
            'team_id': self.team_id,
            'team_name': self.team.name if self.team else None,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'member_count': self.members.count(),
            'task_count': self.tasks.count() if hasattr(self, 'tasks') else 0
        }
    
    def __repr__(self):
        return f'<Project {self.name}>'
