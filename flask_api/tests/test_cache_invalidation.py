"""Test cache invalidation functionality"""
import pytest
from app import db
from app.models.post import Post
from app.models.comment import Comment
from app.models.category import Category
from app.cache import cache
from app.cache_utils import invalidate_post_cache, invalidate_comment_cache, invalidate_category_cache


class TestPostCacheInvalidation:
    """Test post cache invalidation functions"""
    
    def test_invalidate_post_cache_by_id(self, db_session):
        """Test invalidating post cache by ID"""
        cache.clear()
        
        # Set some cache entries
        cache.set("posts:detail:1", {"id": 1, "title": "Test"})
        cache.set("posts:detail:1:comments", {"comments": []})
        
        # Invalidate
        invalidate_post_cache(post_id=1)
        
        # Cache should be cleared
        assert cache.get("posts:detail:1") is None
        assert cache.get("posts:detail:1:comments") is None
    
    def test_invalidate_post_cache_by_slug(self, db_session):
        """Test invalidating post cache by slug"""
        cache.clear()
        
        # Set cache entries
        cache.set("posts:slug:test-post", {"id": 1, "slug": "test-post"})
        cache.set("posts:slug:test-post:comments", {"comments": []})
        
        # Invalidate
        invalidate_post_cache(slug="test-post")
        
        # Cache should be cleared
        assert cache.get("posts:slug:test-post") is None
        assert cache.get("posts:slug:test-post:comments") is None
    
    def test_invalidate_post_cache_handles_missing_keys(self, db_session):
        """Test that invalidation handles missing cache keys gracefully"""
        cache.clear()
        
        # Should not raise exception
        invalidate_post_cache(post_id=999)
        invalidate_post_cache(slug="non-existent")
    
    def test_invalidate_comment_cache_by_post_id(self, db_session):
        """Test invalidating comment cache by post ID"""
        cache.clear()
        
        # Set cache entries
        cache.set("posts:detail:1:comments", {"comments": []})
        cache.set("posts:detail:1", {"id": 1})
        
        # Invalidate
        invalidate_comment_cache(post_id=1)
        
        # Comment cache should be cleared
        assert cache.get("posts:detail:1:comments") is None
        # Post detail should also be invalidated
        assert cache.get("posts:detail:1") is None
    
    def test_invalidate_comment_cache_by_comment_id(self, db_session):
        """Test invalidating comment cache by comment ID"""
        cache.clear()
        
        # Set cache entry
        cache.set("comments:detail:1", {"id": 1, "content": "Test"})
        
        # Invalidate
        invalidate_comment_cache(comment_id=1)
        
        # Cache should be cleared
        assert cache.get("comments:detail:1") is None
    
    def test_invalidate_category_cache(self, db_session):
        """Test invalidating category cache"""
        cache.clear()
        
        # Set cache entries
        cache.set("categories:detail:1", {"id": 1, "name": "Tech"})
        cache.set("categories:list", [{"id": 1}])
        
        # Invalidate
        invalidate_category_cache(category_id=1)
        
        # Cache should be cleared
        assert cache.get("categories:detail:1") is None
        assert cache.get("categories:list") is None


class TestCacheInvalidationIntegration:
    """Test cache invalidation in real scenarios"""
    
    def test_create_post_invalidates_user_list_cache(self, client, auth_headers, test_user, db_session):
        """Test that creating a post invalidates user's post list cache"""
        cache.clear()
        
        # Pre-populate cache with user's posts
        response = client.get(f'/api/posts?user_id={test_user.id}')
        assert response.status_code == 200
        
        # Create new post
        response = client.post('/api/posts', json={
            'title': 'New Post',
            'content': 'New content',
            'is_published': True
        }, headers=auth_headers)
        assert response.status_code == 201
        
        # New request should show updated count
        response2 = client.get(f'/api/posts?user_id={test_user.id}')
        assert response2.status_code == 200
        data = response2.get_json()
        assert len(data['posts']) >= 1
    
    def test_update_post_invalidates_all_related_caches(self, client, auth_headers, test_user, db_session):
        """Test that updating a post invalidates all related caches"""
        post = Post(
            title="Original",
            slug="original",
            content="Content",
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        cache.clear()
        
        # Cache post detail
        response = client.get(f'/api/posts/{post.id}')
        assert response.status_code == 200
        
        # Cache post by slug
        response = client.get(f'/api/posts/slug/{post.slug}')
        assert response.status_code == 200
        
        # Verify caches exist
        cached_detail = cache.get(f"posts:detail:{post.id}")
        cached_slug = cache.get(f"posts:slug:{post.slug}")
        assert cached_detail is not None or cached_slug is not None
        
        # Update post (slug is auto-generated from title, don't pass it)
        response = client.put(f'/api/posts/{post.id}', json={
            'title': 'Updated Title'
        }, headers=auth_headers)
        assert response.status_code == 200
        
        # Refresh post to get new slug
        db_session.refresh(post)
        new_slug = post.slug
        
        # New request should get fresh data (cache invalidated)
        response2 = client.get(f'/api/posts/{post.id}')
        assert response2.status_code == 200
        data = response2.get_json()
        assert data['title'] == 'Updated Title'
    
    def test_delete_post_invalidates_all_caches(self, client, auth_headers, test_user, db_session):
        """Test that deleting a post invalidates all related caches"""
        post = Post(
            title="To Delete",
            slug="to-delete",
            content="Content",
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        post_id = post.id
        post_slug = post.slug
        cache.clear()
        
        # Cache various entries
        cache.set(f"posts:detail:{post_id}", {"id": post_id})
        cache.set(f"posts:slug:{post_slug}", {"id": post_id})
        cache.set(f"posts:detail:{post_id}:comments", {"comments": []})
        
        # Verify caches exist
        assert cache.get(f"posts:detail:{post_id}") is not None
        
        # Delete post
        response = client.delete(f'/api/posts/{post_id}', headers=auth_headers)
        assert response.status_code == 204
        
        # Post should not be accessible (cache invalidated or post deleted)
        response2 = client.get(f'/api/posts/{post_id}')
        assert response2.status_code == 404
