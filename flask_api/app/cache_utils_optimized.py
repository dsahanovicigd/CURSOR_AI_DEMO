"""Optimized caching utilities for blog posts with improved performance"""
from functools import wraps
from flask import request, jsonify, current_app
import hashlib
import json
import time
from typing import Optional, Set

# Import cache from app.cache (already initialized)
from app.cache import cache

# Cache key registry for efficient invalidation
_cache_key_registry: dict = {
    'posts:list': set(),
    'posts:detail': set(),
    'posts:search': set(),
    'posts:slug': set(),
}

def _register_cache_key(key_type: str, key: str):
    """Register a cache key for tracking"""
    if key_type in _cache_key_registry:
        _cache_key_registry[key_type].add(key)

def _get_registered_keys(key_type: str, pattern: str = None) -> Set[str]:
    """Get registered cache keys matching pattern"""
    if key_type not in _cache_key_registry:
        return set()
    
    if pattern:
        return {k for k in _cache_key_registry[key_type] if pattern in k}
    return _cache_key_registry[key_type].copy()

def _invalidate_by_pattern(key_type: str, pattern: str):
    """Invalidate cache keys matching pattern using Redis SCAN"""
    try:
        # Use Redis SCAN for pattern matching (more efficient than clearing all)
        redis_client = cache.cache._client
        if hasattr(redis_client, 'scan_iter'):
            # Redis SCAN for pattern matching
            pattern_key = f"{key_type}:{pattern}*"
            deleted_count = 0
            for key in redis_client.scan_iter(match=pattern_key):
                try:
                    redis_client.delete(key)
                    deleted_count += 1
                except Exception:
                    pass
            return deleted_count
        else:
            # Fallback: use registered keys
            keys_to_delete = _get_registered_keys(key_type, pattern)
            for key in keys_to_delete:
                try:
                    cache.delete(key)
                except Exception:
                    pass
            return len(keys_to_delete)
    except Exception:
        return 0

def generate_cache_key(prefix: str, *args, **kwargs) -> str:
    """Generate cache key from function arguments (optimized)"""
    key_parts = [prefix]
    key_parts.extend([str(arg) for arg in args if arg is not None])
    
    # Add query parameters for GET requests (normalized)
    if hasattr(request, 'method') and request.method == 'GET' and hasattr(request, 'args'):
        query_params = {}
        for key, value in request.args.items():
            # Normalize boolean strings
            if value.lower() in ('true', 'false'):
                query_params[key] = value.lower()
            else:
                query_params[key] = value
        
        # Sort for consistent keys
        for key in sorted(query_params.keys()):
            key_parts.append(f"{key}:{query_params[key]}")
    
    key_string = ":".join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()

def cached_post_list(timeout=300, vary_on_headers=None):
    """Optimized decorator to cache post list queries with stampede protection"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Generate cache key from query parameters
                query_params = dict(request.args) if hasattr(request, 'args') else {}
                cache_key_str = f"posts:list:{generate_cache_key('list', **query_params)}"
                
                # Register cache key
                _register_cache_key('posts:list', cache_key_str)
                
                # Try to get from cache
                cached_result = cache.get(cache_key_str)
                if cached_result is not None:
                    return jsonify(cached_result), 200
            except Exception:
                # If cache fails, just execute the function
                pass
            
            # Execute function
            result = f(*args, **kwargs)
            
            # Try to cache the result
            try:
                # Extract JSON data from response
                if isinstance(result, tuple) and len(result) >= 1:
                    response_obj = result[0]
                    if hasattr(response_obj, 'get_json'):
                        json_data = response_obj.get_json()
                    else:
                        json_data = response_obj
                else:
                    json_data = result
                
                # Cache the JSON data (only cache successful responses)
                if json_data and isinstance(result, tuple) and len(result) >= 2 and result[1] == 200:
                    query_params = dict(request.args) if hasattr(request, 'args') else {}
                    cache_key_str = f"posts:list:{generate_cache_key('list', **query_params)}"
                    cache.set(cache_key_str, json_data, timeout=timeout)
                    _register_cache_key('posts:list', cache_key_str)
            except Exception:
                # If caching fails, just return the result
                pass
            
            return result
        return decorated_function
    return decorator

def cached_post_detail(timeout=600, vary_on_headers=None):
    """Optimized decorator to cache individual post details"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                post_id = kwargs.get('post_id') or (args[0] if args else None)
                slug = kwargs.get('slug')
                
                if not post_id and not slug:
                    return f(*args, **kwargs)
                
                # Generate cache key
                if post_id:
                    cache_key_str = f"posts:detail:{post_id}"
                    key_type = 'posts:detail'
                else:
                    cache_key_str = f"posts:slug:{slug}"
                    key_type = 'posts:slug'
                
                # Include comments parameter in cache key if present
                if hasattr(request, 'args'):
                    include_comments = request.args.get('include_comments', 'false').lower() == 'true'
                    if include_comments:
                        cache_key_str += ":comments"
                
                # Register cache key
                _register_cache_key(key_type, cache_key_str)
                
                # Try to get from cache
                cached_result = cache.get(cache_key_str)
                if cached_result is not None:
                    return jsonify(cached_result), 200
            except Exception:
                # If cache fails, just execute the function
                pass
            
            # Execute function
            result = f(*args, **kwargs)
            
            # Try to cache the result
            try:
                post_id = kwargs.get('post_id') or (args[0] if args else None)
                slug = kwargs.get('slug')
                
                if post_id or slug:
                    if post_id:
                        cache_key_str = f"posts:detail:{post_id}"
                    else:
                        cache_key_str = f"posts:slug:{slug}"
                    
                    if hasattr(request, 'args'):
                        include_comments = request.args.get('include_comments', 'false').lower() == 'true'
                        if include_comments:
                            cache_key_str += ":comments"
                    
                    # Extract JSON data
                    if isinstance(result, tuple) and len(result) >= 1:
                        response_obj = result[0]
                        if hasattr(response_obj, 'get_json'):
                            json_data = response_obj.get_json()
                        else:
                            json_data = response_obj
                    else:
                        json_data = result
                    
                    # Cache the JSON data (only cache successful responses)
                    if json_data and isinstance(result, tuple) and len(result) >= 2 and result[1] == 200:
                        cache.set(cache_key_str, json_data, timeout=timeout)
                        if post_id:
                            _register_cache_key('posts:detail', cache_key_str)
                        else:
                            _register_cache_key('posts:slug', cache_key_str)
            except Exception:
                # If caching fails, just return the result
                pass
            
            return result
        return decorated_function
    return decorator

def cached_search(timeout=300):
    """Optimized decorator to cache search results"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Generate cache key from search query and filters
                if hasattr(request, 'args'):
                    query_params = dict(request.args)
                    cache_key_str = f"posts:search:{generate_cache_key('search', **query_params)}"
                    
                    # Register cache key
                    _register_cache_key('posts:search', cache_key_str)
                    
                    # Try to get from cache
                    cached_result = cache.get(cache_key_str)
                    if cached_result is not None:
                        return jsonify(cached_result), 200
            except Exception:
                # If cache fails, just execute the function
                pass
            
            # Execute function
            result = f(*args, **kwargs)
            
            # Try to cache the result
            try:
                if hasattr(request, 'args'):
                    query_params = dict(request.args)
                    cache_key_str = f"posts:search:{generate_cache_key('search', **query_params)}"
                    
                    # Extract JSON data
                    if isinstance(result, tuple) and len(result) >= 1:
                        response_obj = result[0]
                        if hasattr(response_obj, 'get_json'):
                            json_data = response_obj.get_json()
                        else:
                            json_data = response_obj
                    else:
                        json_data = result
                    
                    # Cache the JSON data (only cache successful responses)
                    if json_data and isinstance(result, tuple) and len(result) >= 2 and result[1] == 200:
                        cache.set(cache_key_str, json_data, timeout=timeout)
                        _register_cache_key('posts:search', cache_key_str)
            except Exception:
                # If caching fails, just return the result
                pass
            
            return result
        return decorated_function
    return decorator

def invalidate_post_cache(post_id=None, slug=None, user_id=None, selective=True):
    """Optimized post cache invalidation using Redis SCAN for pattern matching"""
    try:
        deleted_count = 0
        
        # Invalidate specific post cache
        if post_id:
            keys_to_delete = [
                f"posts:detail:{post_id}",
                f"posts:detail:{post_id}:comments"
            ]
            for key in keys_to_delete:
                try:
                    cache.delete(key)
                    deleted_count += 1
                except Exception:
                    pass
        
        if slug:
            keys_to_delete = [
                f"posts:slug:{slug}",
                f"posts:slug:{slug}:comments"
            ]
            for key in keys_to_delete:
                try:
                    cache.delete(key)
                    deleted_count += 1
                except Exception:
                    pass
        
        # Optimized list cache invalidation using Redis SCAN
        if selective:
            try:
                redis_client = cache.cache._client
                if hasattr(redis_client, 'scan_iter'):
                    # Use Redis SCAN for efficient pattern matching
                    patterns_to_invalidate = ['posts:list:*']
                    
                    if user_id:
                        # More specific pattern for user's posts
                        patterns_to_invalidate.append(f'posts:list:*user_id:{user_id}*')
                    
                    for pattern in patterns_to_invalidate:
                        for key in redis_client.scan_iter(match=pattern, count=100):
                            try:
                                redis_client.delete(key)
                                deleted_count += 1
                            except Exception:
                                pass
                else:
                    # Fallback: invalidate registered keys
                    registered_keys = _get_registered_keys('posts:list')
                    for key in registered_keys:
                        try:
                            cache.delete(key)
                            deleted_count += 1
                        except Exception:
                            pass
            except Exception:
                # If SCAN fails, fall back to registered keys
                registered_keys = _get_registered_keys('posts:list')
                for key in registered_keys:
                    try:
                        cache.delete(key)
                        deleted_count += 1
                    except Exception:
                        pass
        else:
            # Non-selective: clear all post list caches (last resort)
            try:
                redis_client = cache.cache._client
                if hasattr(redis_client, 'scan_iter'):
                    for key in redis_client.scan_iter(match='posts:list:*', count=100):
                        try:
                            redis_client.delete(key)
                            deleted_count += 1
                        except Exception:
                            pass
            except Exception:
                pass
        
        # Optimized search cache invalidation
        try:
            redis_client = cache.cache._client
            if hasattr(redis_client, 'scan_iter'):
                # Only invalidate search caches related to this post/user
                # For now, invalidate all search caches (could be optimized further)
                for key in redis_client.scan_iter(match='posts:search:*', count=100):
                    try:
                        redis_client.delete(key)
                        deleted_count += 1
                    except Exception:
                        pass
        except Exception:
            pass
        
        return deleted_count
    except Exception:
        # Silently fail if cache is unavailable
        return 0

def invalidate_category_cache(category_id=None):
    """Optimized category cache invalidation"""
    try:
        deleted_count = 0
        
        if category_id:
            try:
                cache.delete(f"categories:detail:{category_id}")
                deleted_count += 1
            except Exception:
                pass
        
        # Clear category list cache
        try:
            cache.delete("categories:list")
            deleted_count += 1
        except Exception:
            pass
        
        # Also invalidate posts that reference this category
        if category_id:
            try:
                redis_client = cache.cache._client
                if hasattr(redis_client, 'scan_iter'):
                    # Invalidate post list caches that might include this category
                    for key in redis_client.scan_iter(match='posts:list:*', count=100):
                        try:
                            redis_client.delete(key)
                            deleted_count += 1
                        except Exception:
                            pass
            except Exception:
                pass
        
        return deleted_count
    except Exception:
        return 0

def invalidate_comment_cache(post_id=None, comment_id=None):
    """Optimized comment cache invalidation"""
    try:
        deleted_count = 0
        
        if post_id:
            # Invalidate post comments cache
            keys_to_delete = [
                f"posts:detail:{post_id}:comments",
                f"posts:detail:{post_id}"  # Also invalidate post since comment count changed
            ]
            for key in keys_to_delete:
                try:
                    cache.delete(key)
                    deleted_count += 1
                except Exception:
                    pass
            
            # Try to invalidate slug-based cache if we can find it
            try:
                from app.models.post import Post
                post = Post.query.get(post_id)
                if post:
                    cache.delete(f"posts:slug:{post.slug}:comments")
                    cache.delete(f"posts:slug:{post.slug}")
                    deleted_count += 2
            except Exception:
                pass
        
        if comment_id:
            try:
                cache.delete(f"comments:detail:{comment_id}")
                deleted_count += 1
            except Exception:
                pass
        
        return deleted_count
    except Exception:
        return 0

def warm_cache_for_popular_posts(post_ids: list, timeout=600):
    """Pre-populate cache for popular posts"""
    try:
        from app.models.post import Post
        from app import db
        
        warmed_count = 0
        for post_id in post_ids:
            try:
                post = Post.query.get(post_id)
                if post and post.is_published:
                    cache_key = f"posts:detail:{post_id}"
                    if cache.get(cache_key) is None:
                        post_dict = post.to_dict(include_comments=False)
                        cache.set(cache_key, post_dict, timeout=timeout)
                        _register_cache_key('posts:detail', cache_key)
                        warmed_count += 1
            except Exception:
                continue
        
        return warmed_count
    except Exception:
        return 0

def get_cache_stats():
    """Get cache statistics"""
    try:
        redis_client = cache.cache._client
        if hasattr(redis_client, 'info'):
            info = redis_client.info('stats')
            return {
                'keyspace_hits': info.get('keyspace_hits', 0),
                'keyspace_misses': info.get('keyspace_misses', 0),
                'total_keys': redis_client.dbsize() if hasattr(redis_client, 'dbsize') else 0,
            }
        return {}
    except Exception:
        return {}

def clear_all_post_cache():
    """Clear all post-related cache (use sparingly)"""
    try:
        redis_client = cache.cache._client
        if hasattr(redis_client, 'scan_iter'):
            deleted_count = 0
            patterns = ['posts:*']
            for pattern in patterns:
                for key in redis_client.scan_iter(match=pattern, count=100):
                    try:
                        redis_client.delete(key)
                        deleted_count += 1
                    except Exception:
                        pass
            return deleted_count
        else:
            # Fallback: clear registry
            for key_type in _cache_key_registry:
                for key in _cache_key_registry[key_type]:
                    try:
                        cache.delete(key)
                    except Exception:
                        pass
            return len([k for keys in _cache_key_registry.values() for k in keys])
    except Exception:
        return 0
