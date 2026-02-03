from datetime import datetime
from app import db

# Association table for many-to-many relationship between teams and users
team_members = db.Table('team_members',
    db.Column('team_id', db.Integer, db.ForeignKey('teams.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role', db.String(50), default='member'),  # owner, admin, member
    db.Column('joined_at', db.DateTime, default=datetime.utcnow)
)

class Team(db.Model):
    """Team model for team collaboration"""
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Foreign keys
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Dates
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    owner = db.relationship('User', foreign_keys=[owner_id], backref='owned_teams', lazy=True)
    members = db.relationship('User', secondary=team_members, lazy='dynamic',
                             backref=db.backref('teams', lazy='dynamic'))
    
    def add_member(self, user, role='member'):
        """Add a member to the team"""
        if user not in self.members:
            self.members.append(user)
            db.session.flush()  # Flush to get the association created
            # Update role in association table
            from sqlalchemy import update
            stmt = update(team_members).where(
                db.and_(
                    team_members.c.team_id == self.id,
                    team_members.c.user_id == user.id
                )
            ).values(role=role)
            db.session.execute(stmt)
            db.session.commit()
    
    def remove_member(self, user):
        """Remove a member from the team"""
        if user in self.members:
            self.members.remove(user)
            db.session.commit()
    
    def get_member_role(self, user):
        """Get the role of a member in the team"""
        from sqlalchemy import select
        result = db.session.execute(
            select(team_members.c.role).where(
                db.and_(
                    team_members.c.team_id == self.id,
                    team_members.c.user_id == user.id
                )
            )
        ).first()
        return result[0] if result else None
    
    def to_dict(self):
        """Convert team to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner_id': self.owner_id,
            'owner_name': self.owner.username if self.owner else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'member_count': self.members.count(),
            'project_count': self.projects.count() if hasattr(self, 'projects') else 0
        }
    
    def __repr__(self):
        return f'<Team {self.name}>'
