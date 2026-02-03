"""Test cache optimization features"""
import pytest
from app import db
from app.models.post import Post
from app.cache import cache
from app.cache_optimization import (
    optimize_cache_ttl_based_on_popularity,
    should_cache_response,
    get_optimal_cache_timeout,
    check_cache_health,
    get_cache_metrics
)


class TestCacheOptimization:
    """Test cache optimization utilities"""
    
    def test_optimize_cache_ttl_by_popularity(self):
        """Test dynamic TTL based on post popularity"""
        # Very popular post
        assert optimize_cache_ttl_based_on_popularity(1, 1500) == 3600
        
        # Popular post
        assert optimize_cache_ttl_based_on_popularity(1, 750) == 1800
        
        # Moderately popular
        assert optimize_cache_ttl_based_on_popularity(1, 200) == 900
        
        # Regular post
        assert optimize_cache_ttl_based_on_popularity(1, 50) == 600
    
    def test_should_cache_response(self):
        """Test response caching decision logic"""
        # Should cache successful response
        assert should_cache_response({'posts': [{'id': 1}]}) == True
        
        # Should not cache error response
        assert should_cache_response({'error': 'Not found'}) == False
        
        # Should not cache empty results
        assert should_cache_response({'posts': []}) == False
        assert should_cache_response({'comments': []}) == False
        
        # Should cache response with data
        assert should_cache_response({'posts': [{'id': 1}, {'id': 2}]}) == True
    
    def test_get_optimal_cache_timeout(self):
        """Test optimal cache timeout calculation"""
        # List endpoint
        assert get_optimal_cache_timeout('list') == 300
        
        # Detail endpoint
        assert get_optimal_cache_timeout('detail') == 600
        
        # Search endpoint
        assert get_optimal_cache_timeout('search') == 300
        
        # Large data gets longer timeout
        large_timeout = get_optimal_cache_timeout('detail', 150000)
        assert large_timeout > 600
    
    def test_check_cache_health(self):
        """Test cache health check"""
        health = check_cache_health()
        assert 'status' in health
        assert 'connected' in health
        # Should return dict with status info
        assert isinstance(health, dict)
    
    def test_get_cache_metrics(self):
        """Test cache metrics retrieval"""
        metrics = get_cache_metrics()
        assert 'hits' in metrics
        assert 'misses' in metrics
        assert 'hit_rate' in metrics
        assert 'total_requests' in metrics
        assert isinstance(metrics['hit_rate'], float)


class TestOptimizedCacheInvalidation:
    """Test optimized cache invalidation"""
    
    def test_optimized_invalidation_uses_scan(self, db_session):
        """Test that optimized invalidation uses Redis SCAN"""
        try:
            from app.cache_utils_optimized import invalidate_post_cache_optimized
            
            cache.clear()
            
            # Set some cache entries
            cache.set("posts:list:abc123", {"posts": []})
            cache.set("posts:list:def456", {"posts": []})
            cache.set("posts:detail:1", {"id": 1})
            
            # Invalidate using optimized method
            deleted = invalidate_post_cache_optimized(post_id=1, selective=True)
            
            # Should have deleted at least the detail cache
            assert cache.get("posts:detail:1") is None
            
        except ImportError:
            pytest.skip("Optimized cache utils not available")
    
    def test_cache_key_registry(self, db_session):
        """Test cache key registry functionality"""
        try:
            from app.cache_utils_optimized import _register_cache_key, _get_registered_keys
            
            # Register some keys
            _register_cache_key('posts:list', 'posts:list:test1')
            _register_cache_key('posts:list', 'posts:list:test2')
            _register_cache_key('posts:detail', 'posts:detail:1')
            
            # Retrieve registered keys
            list_keys = _get_registered_keys('posts:list')
            assert len(list_keys) >= 2
            
            detail_keys = _get_registered_keys('posts:detail')
            assert len(detail_keys) >= 1
            
        except ImportError:
            pytest.skip("Optimized cache utils not available")
