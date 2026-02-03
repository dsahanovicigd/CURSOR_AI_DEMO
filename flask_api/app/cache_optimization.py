"""Cache optimization utilities and monitoring"""
from flask import current_app
from app.cache import cache
import time
from typing import Dict, Optional

class CacheMetrics:
    """Track cache performance metrics"""
    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.invalidations = 0
        self.errors = 0
    
    def record_hit(self):
        self.hits += 1
    
    def record_miss(self):
        self.misses += 1
    
    def record_invalidation(self):
        self.invalidations += 1
    
    def record_error(self):
        self.errors += 1
    
    def get_hit_rate(self) -> float:
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return (self.hits / total) * 100
    
    def get_stats(self) -> Dict:
        return {
            'hits': self.hits,
            'misses': self.misses,
            'invalidations': self.invalidations,
            'errors': self.errors,
            'hit_rate': self.get_hit_rate(),
            'total_requests': self.hits + self.misses
        }

# Global metrics instance
_cache_metrics = CacheMetrics()

def get_cache_metrics() -> Dict:
    """Get cache performance metrics"""
    return _cache_metrics.get_stats()

def optimize_cache_ttl_based_on_popularity(post_id: int, view_count: int) -> int:
    """Dynamically adjust cache TTL based on post popularity"""
    # More popular posts get longer cache TTL
    if view_count > 1000:
        return 3600  # 1 hour for very popular posts
    elif view_count > 500:
        return 1800  # 30 minutes for popular posts
    elif view_count > 100:
        return 900   # 15 minutes for moderately popular posts
    else:
        return 600   # 10 minutes default

def should_cache_response(response_data: dict) -> bool:
    """Determine if response should be cached based on content"""
    # Don't cache error responses
    if 'error' in response_data:
        return False
    
    # Don't cache empty results (might be temporary)
    if isinstance(response_data, dict):
        if 'posts' in response_data and len(response_data.get('posts', [])) == 0:
            return False
        if 'comments' in response_data and len(response_data.get('comments', [])) == 0:
            return False
    
    return True

def get_optimal_cache_timeout(endpoint_type: str, data_size: int = 0) -> int:
    """Get optimal cache timeout based on endpoint type and data size"""
    base_timeouts = {
        'list': 300,      # 5 minutes for lists
        'detail': 600,    # 10 minutes for details
        'search': 300,    # 5 minutes for search
    }
    
    base_timeout = base_timeouts.get(endpoint_type, 300)
    
    # Adjust based on data size (larger responses cached longer)
    if data_size > 100000:  # > 100KB
        return base_timeout * 2
    elif data_size > 50000:  # > 50KB
        return int(base_timeout * 1.5)
    
    return base_timeout

def check_cache_health() -> Dict:
    """Check cache health and connectivity"""
    try:
        redis_client = cache.cache._client
        if hasattr(redis_client, 'ping'):
            ping_result = redis_client.ping()
            if ping_result:
                info = redis_client.info('memory') if hasattr(redis_client, 'info') else {}
                return {
                    'status': 'healthy',
                    'connected': True,
                    'memory_used': info.get('used_memory_human', 'unknown'),
                    'keys': redis_client.dbsize() if hasattr(redis_client, 'dbsize') else 0
                }
        return {'status': 'unknown', 'connected': False}
    except Exception as e:
        return {'status': 'unhealthy', 'connected': False, 'error': str(e)}
