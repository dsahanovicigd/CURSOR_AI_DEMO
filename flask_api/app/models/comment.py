from datetime import datetime
from app import db

class Comment(db.Model):
    """Comment model for blog posts"""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id', ondelete='CASCADE'), nullable=True)  # For nested comments/replies
    is_approved = db.Column(db.Boolean, default=True, nullable=False)  # For moderation
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    post = db.relationship('Post', backref='comments', lazy=True)
    author = db.relationship('User', backref='comments', lazy=True)
    parent = db.relationship('Comment', remote_side=[id], backref='replies', lazy=True)
    
    # Indexes for better query performance
    __table_args__ = (
        db.Index('idx_comment_post_created', 'post_id', 'created_at'),
        db.Index('idx_comment_user_created', 'user_id', 'created_at'),
        db.Index('idx_comment_post_approved', 'post_id', 'is_approved'),  # For filtering approved comments
        db.Index('idx_comment_parent', 'parent_id'),  # For nested comments
    )
    
    def to_dict(self):
        """Convert comment to dictionary"""
        return {
            'id': self.id,
            'content': self.content,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'author': self.author.username if self.author else None,
            'author_name': self.author.full_name if self.author else None,
            'parent_id': self.parent_id,
            'is_approved': self.is_approved,
            'reply_count': len(self.replies) if self.replies else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Comment {self.id} on Post {self.post_id}>'
