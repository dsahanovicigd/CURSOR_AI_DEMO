from datetime import datetime
from app import db
import re

class Post(db.Model):
    """Post model for blogging platform"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(250), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text, nullable=True)  # Short summary for previews
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    is_published = db.Column(db.Boolean, default=True, nullable=False, index=True)
    view_count = db.Column(db.Integer, default=0, nullable=False)
    tags = db.Column(db.String(500), nullable=True)  # Comma-separated tags
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Indexes for better query performance
    __table_args__ = (
        db.Index('idx_user_created', 'user_id', 'created_at'),
        db.Index('idx_published_created', 'is_published', 'created_at'),
        db.Index('idx_slug', 'slug'),
        db.Index('idx_title_search', 'title'),  # For search queries
        db.Index('idx_published_user', 'is_published', 'user_id'),  # For user's published posts
        db.Index('idx_created_desc', 'created_at'),  # For ordering
    )
    
    @staticmethod
    def generate_slug(title):
        """Generate URL-friendly slug from title"""
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug[:250]
    
    def to_dict(self, include_comments=False):
        """Convert post to dictionary"""
        result = {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'content': self.content,
            'excerpt': self.excerpt,
            'user_id': self.user_id,
            'author': self.author.username if self.author else None,
            'author_name': self.author.full_name if self.author else None,
            'is_published': self.is_published,
            'view_count': self.view_count,
            'tags': self.tags.split(',') if self.tags else [],
            'category_ids': [cat.id for cat in self.categories] if hasattr(self, 'categories') and self.categories else [],
            'category_names': [cat.name for cat in self.categories] if hasattr(self, 'categories') and self.categories else [],
            'comment_count': len([c for c in self.comments if c.is_approved]) if hasattr(self, 'comments') and self.comments else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_comments:
            from app.models.comment import Comment
            approved_comments = [c for c in self.comments if c.is_approved and c.parent_id is None] if hasattr(self, 'comments') and self.comments else []
            result['comments'] = [
                comment.to_dict() 
                for comment in sorted(approved_comments, key=lambda x: x.created_at, reverse=True)
            ]
        
        return result
    
    def __repr__(self):
        return f'<Post {self.title}>'
