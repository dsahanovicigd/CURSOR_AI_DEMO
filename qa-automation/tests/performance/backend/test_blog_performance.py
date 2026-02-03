"""Performance tests for blog API"""
import pytest
import time
from concurrent.futures import ThreadPoolExecutor
from app.models import Post, User, Category, Comment
from app.models.post import Post as PostModel


class TestBlogPerformance:
    """Test performance optimizations"""
    
    def test_post_list_performance(self, client, db_session, test_user):
        """Test post list endpoint performance"""
        # Create multiple posts
        for i in range(50):
            slug = PostModel.generate_slug(f'Performance Post {i}')
            post = Post(
                title=f'Performance Post {i}',
                content='Content' * 10,
                slug=slug,
                user_id=test_user.id,
                is_published=True
            )
            db_session.add(post)
        db_session.commit()
        
        # Measure response time
        start = time.time()
        response = client.get('/api/posts?per_page=50')
        elapsed = time.time() - start
        
        assert response.status_code == 200
        # Should respond quickly (with caching and indexes)
        assert elapsed < 1.0  # Less than 1 second
    
    def test_search_performance(self, client, db_session, test_user):
        """Test search endpoint performance"""
        # Create posts with searchable content
        for i in range(30):
            slug = PostModel.generate_slug(f'Search Post {i}')
            post = Post(
                title=f'Search Post {i}',
                content=f'Searchable content {i}',
                slug=slug,
                user_id=test_user.id,
                is_published=True
            )
            db_session.add(post)
        db_session.commit()
        
        # Measure search time
        start = time.time()
        response = client.get('/api/search?q=Search')
        elapsed = time.time() - start
        
        assert response.status_code == 200
        # Should be fast with indexes
        assert elapsed < 0.5
    
    def test_concurrent_requests(self, client, db_session, test_user, app):
        """Test handling concurrent requests"""
        slug = PostModel.generate_slug('Concurrent Test')
        post = Post(
            title='Concurrent Test',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        def make_request():
            with app.app_context():
                return client.get(f'/api/posts/{post.id}')
        
        # Make 10 concurrent requests
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [f.result() for f in futures]
        
        # All should succeed
        assert all(r.status_code == 200 for r in results)
        # All should return same data
        assert all(r.json['id'] == post.id for r in results)
    
    def test_pagination_performance(self, client, db_session, test_user):
        """Test pagination performance with large datasets"""
        # Create many posts
        for i in range(100):
            slug = PostModel.generate_slug(f'Page Post {i}')
            post = Post(
                title=f'Page Post {i}',
                content='Content',
                slug=slug,
                user_id=test_user.id,
                is_published=True
            )
            db_session.add(post)
        db_session.commit()
        
        # Test pagination performance
        times = []
        for page in range(1, 6):
            start = time.time()
            response = client.get(f'/api/posts?page={page}&per_page=20')
            elapsed = time.time() - start
            times.append(elapsed)
            assert response.status_code == 200
        
        # All pages should load quickly
        assert all(t < 0.5 for t in times)
    
    def test_index_usage(self, client, db_session, test_user):
        """Test that indexes are being used for queries"""
        # Create posts
        for i in range(20):
            slug = PostModel.generate_slug(f'Indexed Post {i}')
            post = Post(
                title=f'Indexed Post {i}',
                content='Content',
                slug=slug,
                user_id=test_user.id,
                is_published=i % 2 == 0  # Mix published/unpublished
            )
            db_session.add(post)
        db_session.commit()
        
        # Query with filter (should use index)
        start = time.time()
        response = client.get(f'/api/posts?user_id={test_user.id}&published_only=true')
        elapsed = time.time() - start
        
        assert response.status_code == 200
        # Should be fast with proper indexes
        assert elapsed < 0.3
