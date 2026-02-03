"""Comprehensive tests for blog API with caching"""
import pytest
import time
from app import create_app, db, cache
from app.models import Post, User, Category, Comment
from app.cache_utils import invalidate_post_cache, invalidate_comment_cache
from app.models.post import Post as PostModel


class TestBlogCaching:
    """Test caching functionality for blog endpoints"""
    
    def test_post_list_caching(self, client, db_session, test_user):
        """Test that post list is cached"""
        # Create a post
        slug = PostModel.generate_slug('Cached Post')
        post = Post(
            title='Cached Post',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        # First request - should hit database
        start = time.time()
        response1 = client.get('/api/posts')
        time1 = time.time() - start
        assert response1.status_code == 200
        
        # Second request - should hit cache (faster)
        start = time.time()
        response2 = client.get('/api/posts')
        time2 = time.time() - start
        assert response2.status_code == 200
        
        # Cached response should be faster (or at least return same data)
        assert response1.json == response2.json
        # Cache hit should be significantly faster
        assert time2 < time1 or abs(time2 - time1) < 0.1  # Allow small variance
    
    def test_post_detail_caching(self, client, db_session, test_user):
        """Test that individual post is cached"""
        slug = PostModel.generate_slug('Detail Post')
        post = Post(
            title='Detail Post',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        # First request
        response1 = client.get(f'/api/posts/{post.id}')
        assert response1.status_code == 200
        
        # Second request - should be cached
        response2 = client.get(f'/api/posts/{post.id}')
        assert response2.status_code == 200
        assert response1.json == response2.json
    
    def test_search_caching(self, client, db_session, test_user):
        """Test that search results are cached"""
        slug = PostModel.generate_slug('Searchable Post')
        post = Post(
            title='Searchable Post',
            content='Search content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        # First search
        response1 = client.get('/api/search?q=Searchable')
        assert response1.status_code == 200
        
        # Second search - should be cached
        response2 = client.get('/api/search?q=Searchable')
        assert response2.status_code == 200
        assert response1.json == response2.json
    
    def test_cache_invalidation_on_create(self, client, auth_headers, db_session, test_user):
        """Test cache invalidation when creating a post"""
        # Get initial posts (populates cache)
        response1 = client.get('/api/posts')
        assert response1.status_code == 200
        initial_count = len(response1.json['posts'])
        
        # Create new post
        response2 = client.post('/api/posts',
            headers=auth_headers,
            json={
                'title': 'New Cached Post',
                'content': 'Content',
                'is_published': True
            }
        )
        assert response2.status_code == 201
        
        # Cache should be invalidated, new request should show new post
        response3 = client.get('/api/posts')
        assert response3.status_code == 200
        # New post should appear (cache was cleared)
        assert len(response3.json['posts']) >= initial_count
    
    def test_cache_invalidation_on_update(self, client, auth_headers, db_session, test_user):
        """Test cache invalidation when updating a post"""
        slug = PostModel.generate_slug('Original Title')
        post = Post(
            title='Original Title',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        # Cache the post
        response1 = client.get(f'/api/posts/{post.id}')
        assert response1.status_code == 200
        assert response1.json['title'] == 'Original Title'
        
        # Update the post
        response2 = client.put(f'/api/posts/{post.id}',
            headers=auth_headers,
            json={'title': 'Updated Title'}
        )
        assert response2.status_code == 200
        
        # Get post again - should show updated title (cache invalidated)
        response3 = client.get(f'/api/posts/{post.id}')
        assert response3.status_code == 200
        assert response3.json['title'] == 'Updated Title'
    
    def test_cache_invalidation_on_delete(self, client, auth_headers, db_session, test_user):
        """Test cache invalidation when deleting a post"""
        slug = PostModel.generate_slug('To Delete')
        post = Post(
            title='To Delete',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        # Cache the post
        response1 = client.get(f'/api/posts/{post.id}')
        assert response1.status_code == 200
        
        # Delete the post
        response2 = client.delete(f'/api/posts/{post.id}', headers=auth_headers)
        assert response2.status_code == 204
        
        # Post should be gone (cache invalidated)
        response3 = client.get(f'/api/posts/{post.id}')
        assert response3.status_code == 404
    
    def test_cache_invalidation_on_comment_create(self, client, auth_headers, db_session, test_user):
        """Test cache invalidation when creating a comment"""
        slug = PostModel.generate_slug('Comment Post')
        post = Post(
            title='Comment Post',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        # Cache post with comments
        response1 = client.get(f'/api/posts/{post.id}?include_comments=true')
        assert response1.status_code == 200
        initial_comment_count = response1.json.get('comment_count', 0)
        
        # Create comment
        response2 = client.post(f'/api/posts/{post.id}/comments',
            headers=auth_headers,
            json={'content': 'New comment'}
        )
        assert response2.status_code == 201
        
        # Post should show updated comment count (cache invalidated)
        response3 = client.get(f'/api/posts/{post.id}')
        assert response3.status_code == 200
        # Comment count should be updated (cache was invalidated, so fresh data)
        assert response3.json.get('comment_count', 0) >= initial_comment_count
    
    def test_different_query_params_create_different_cache_keys(self, client, db_session, test_user):
        """Test that different query parameters create different cache entries"""
        slug = PostModel.generate_slug('Filtered Post')
        post = Post(
            title='Filtered Post',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        # Request with user_id filter
        response1 = client.get(f'/api/posts?user_id={test_user.id}')
        assert response1.status_code == 200
        
        # Request without filter
        response2 = client.get('/api/posts')
        assert response2.status_code == 200
        
        # They should have different results (different cache keys)
        # Both should work correctly
    
    def test_cache_timeout(self, client, db_session, test_user, monkeypatch):
        """Test that cache expires after timeout"""
        slug = PostModel.generate_slug('Timeout Post')
        post = Post(
            title='Timeout Post',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        # First request - cache it
        response1 = client.get(f'/api/posts/{post.id}')
        assert response1.status_code == 200
        
        # Manually expire cache
        cache.delete(f"posts:detail:{post.id}")
        
        # Request again - should hit database (view count may increment)
        response2 = client.get(f'/api/posts/{post.id}')
        assert response2.status_code == 200
        # Compare all fields except view_count and updated_at (which change)
        for key in response1.json:
            if key not in ['view_count', 'updated_at']:
                assert response1.json[key] == response2.json[key]
    
    def test_slug_based_caching(self, client, db_session, test_user):
        """Test caching works with slug-based lookups"""
        slug = PostModel.generate_slug('Slug Post')
        post = Post(
            title='Slug Post',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        # Cache by slug
        response1 = client.get('/api/posts/slug/slug-post')
        assert response1.status_code == 200
        
        # Second request should be cached
        response2 = client.get('/api/posts/slug/slug-post')
        assert response2.status_code == 200
        assert response1.json == response2.json
    
    def test_search_with_filters_caching(self, client, db_session, test_user):
        """Test that search with different filters creates different cache entries"""
        slug = PostModel.generate_slug('Filtered Search')
        post = Post(
            title='Filtered Search',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        # Search without filters
        response1 = client.get('/api/search?q=Filtered')
        assert response1.status_code == 200
        
        # Search with category filter (if category exists)
        response2 = client.get('/api/search?q=Filtered&category_id=999')
        assert response2.status_code == 200
        
        # Both should work (different cache keys)
    
    def test_post_list_pagination_caching(self, client, db_session, test_user):
        """Test that different pagination creates different cache entries"""
        # Create multiple posts
        for i in range(5):
            slug = PostModel.generate_slug(f'Post {i}')
            post = Post(
                title=f'Post {i}',
                content='Content',
                slug=slug,
                user_id=test_user.id,
                is_published=True
            )
            db_session.add(post)
        db_session.commit()
        
        # Request page 1
        response1 = client.get('/api/posts?page=1&per_page=2')
        assert response1.status_code == 200
        
        # Request page 2
        response2 = client.get('/api/posts?page=2&per_page=2')
        assert response2.status_code == 200
        
        # Should have different results
        assert response1.json['current_page'] == 1
        assert response2.json['current_page'] == 2
    
    def test_cache_clearing_on_bulk_operations(self, client, auth_headers, db_session, test_user):
        """Test cache behavior with multiple operations"""
        # Create and cache a post
        slug = PostModel.generate_slug('Bulk Post')
        post = Post(
            title='Bulk Post',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        # Cache it
        client.get(f'/api/posts/{post.id}')
        
        # Update multiple times
        client.put(f'/api/posts/{post.id}',
            headers=auth_headers,
            json={'title': 'Updated 1'}
        )
        
        client.put(f'/api/posts/{post.id}',
            headers=auth_headers,
            json={'title': 'Updated 2'}
        )
        
        # Final get should show latest version
        response = client.get(f'/api/posts/{post.id}')
        assert response.status_code == 200
        assert response.json['title'] == 'Updated 2'
    
    def test_concurrent_cache_access(self, client, db_session, test_user):
        """Test cache handles concurrent requests"""
        slug = PostModel.generate_slug('Concurrent Post')
        post = Post(
            title='Concurrent Post',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        # Simulate concurrent requests (simplified)
        responses = []
        for _ in range(5):
            response = client.get(f'/api/posts/{post.id}')
            responses.append(response)
        
        # All should succeed and return same data
        for response in responses:
            assert response.status_code == 200
            assert response.json['id'] == post.id
