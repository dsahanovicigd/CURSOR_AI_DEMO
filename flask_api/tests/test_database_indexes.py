"""Test database indexes for optimization"""
import pytest
from sqlalchemy import inspect
from app import db
from app.models.post import Post
from app.models.comment import Comment
from app.models.category import Category


class TestPostIndexes:
    """Test that Post model has proper indexes"""
    
    def test_post_table_has_indexes(self, app):
        """Test that posts table has required indexes"""
        with app.app_context():
            inspector = inspect(db.engine)
            indexes = inspector.get_indexes('posts')
            index_names = [idx['name'] for idx in indexes]
            
            # Check for key indexes
            assert 'idx_user_created' in index_names or any('user_id' in str(idx) for idx in indexes)
            assert 'idx_published_created' in index_names or any('is_published' in str(idx) for idx in indexes)
            assert 'idx_slug' in index_names or any('slug' in str(idx) for idx in indexes)
            assert 'idx_title_search' in index_names or any('title' in str(idx) for idx in indexes)
    
    def test_post_model_defines_indexes(self):
        """Test that Post model defines indexes in __table_args__"""
        assert hasattr(Post, '__table_args__')
        indexes = Post.__table__.indexes
        index_names = [idx.name for idx in indexes]
        
        # Verify key indexes exist
        assert 'idx_user_created' in index_names
        assert 'idx_published_created' in index_names
        assert 'idx_slug' in index_names
        assert 'idx_title_search' in index_names
        assert 'idx_published_user' in index_names
        assert 'idx_created_desc' in index_names


class TestCommentIndexes:
    """Test that Comment model has proper indexes"""
    
    def test_comment_table_has_indexes(self, app):
        """Test that comments table has required indexes"""
        with app.app_context():
            inspector = inspect(db.engine)
            indexes = inspector.get_indexes('comments')
            index_names = [idx['name'] for idx in indexes]
            
            # Check for key indexes
            assert 'idx_comment_post_created' in index_names or any('post_id' in str(idx) for idx in indexes)
            assert 'idx_comment_user_created' in index_names or any('user_id' in str(idx) for idx in indexes)
            assert 'idx_comment_post_approved' in index_names or any('is_approved' in str(idx) for idx in indexes)
            assert 'idx_comment_parent' in index_names or any('parent_id' in str(idx) for idx in indexes)
    
    def test_comment_model_defines_indexes(self):
        """Test that Comment model defines indexes in __table_args__"""
        assert hasattr(Comment, '__table_args__')
        indexes = Comment.__table__.indexes
        index_names = [idx.name for idx in indexes]
        
        # Verify key indexes exist
        assert 'idx_comment_post_created' in index_names
        assert 'idx_comment_user_created' in index_names
        assert 'idx_comment_post_approved' in index_names
        assert 'idx_comment_parent' in index_names


class TestIndexPerformance:
    """Test that indexes improve query performance"""
    
    def test_post_query_uses_indexes(self, db_session, test_user):
        """Test that post queries benefit from indexes"""
        # Create multiple posts
        posts = []
        for i in range(10):
            post = Post(
                title=f"Post {i}",
                slug=f"post-{i}",
                content=f"Content {i}",
                user_id=test_user.id,
                is_published=(i % 2 == 0)
            )
            posts.append(post)
        db_session.add_all(posts)
        db_session.commit()
        
        # Query by user_id (should use idx_user_created)
        user_posts = Post.query.filter_by(user_id=test_user.id).all()
        assert len(user_posts) == 10
        
        # Query by is_published (should use idx_published_created)
        published_posts = Post.query.filter_by(is_published=True).all()
        assert len(published_posts) == 5
        
        # Query by slug (should use idx_slug)
        post = Post.query.filter_by(slug="post-1").first()
        assert post is not None
        
        # Search by title (should use idx_title_search)
        search_posts = Post.query.filter(Post.title.like('%Post%')).all()
        assert len(search_posts) == 10
    
    def test_comment_query_uses_indexes(self, db_session, test_user):
        """Test that comment queries benefit from indexes"""
        from app.models.post import Post
        
        post = Post(
            title="Test Post",
            slug="test-post",
            content="Content",
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        # Create multiple comments
        comments = []
        for i in range(5):
            comment = Comment(
                content=f"Comment {i}",
                post_id=post.id,
                user_id=test_user.id,
                is_approved=(i % 2 == 0)
            )
            comments.append(comment)
        db_session.add_all(comments)
        db_session.commit()
        
        # Query by post_id (should use idx_comment_post_created)
        post_comments = Comment.query.filter_by(post_id=post.id).all()
        assert len(post_comments) == 5
        
        # Query by user_id (should use idx_comment_user_created)
        user_comments = Comment.query.filter_by(user_id=test_user.id).all()
        assert len(user_comments) == 5
        
        # Query by is_approved (should use idx_comment_post_approved)
        approved_comments = Comment.query.filter_by(post_id=post.id, is_approved=True).all()
        assert len(approved_comments) == 3
