"""Caching utilities for blog posts - Optimized version"""
from functools import wraps
from flask import request, jsonify
import hashlib
import json

# Import cache from app.cache (already initialized)
from app.cache import cache

# Try to import optimization utilities
try:
    from app.cache_optimization import should_cache_response, get_cache_metrics
    OPTIMIZATION_AVAILABLE = True
except ImportError:
    OPTIMIZATION_AVAILABLE = False

def generate_cache_key(prefix, *args, **kwargs):
    """Generate cache key from function arguments"""
    key_parts = [prefix]
    key_parts.extend([str(arg) for arg in args if arg is not None])
    
    # Add query parameters for GET requests
    if request.method == 'GET':
        query_params = dict(request.args)
        # Sort for consistent keys
        for key in sorted(query_params.keys()):
            key_parts.append(f"{key}:{query_params[key]}")
    
    key_string = ":".join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()

def cached_post_list(timeout=300):
    """Decorator to cache post list queries"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Generate cache key from query parameters
                query_params = dict(request.args) if hasattr(request, 'args') else {}
                cache_key_str = f"posts:list:{generate_cache_key('list', **query_params)}"
                
                # Try to get from cache
                cached_result = cache.get(cache_key_str)
                if cached_result is not None:
                    # Record cache hit
                    if OPTIMIZATION_AVAILABLE:
                        get_cache_metrics().record_hit()
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
                if json_data and hasattr(request, 'args'):
                    # Check if response should be cached
                    should_cache = True
                    if OPTIMIZATION_AVAILABLE:
                        should_cache = should_cache_response(json_data)
                    
                    if should_cache and isinstance(result, tuple) and len(result) >= 2 and result[1] == 200:
                        query_params = dict(request.args)
                        cache_key_str = f"posts:list:{generate_cache_key('list', **query_params)}"
                        cache.set(cache_key_str, json_data, timeout=timeout)
                        
                        # Record cache miss (we're setting cache)
                        if OPTIMIZATION_AVAILABLE:
                            get_cache_metrics().record_miss()
            except Exception:
                # If caching fails, just return the result
                pass
            
            return result
        return decorated_function
    return decorator

def cached_post_detail(timeout=600):
    """Decorator to cache individual post details"""
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
                else:
                    cache_key_str = f"posts:slug:{slug}"
                
                # Include comments parameter in cache key if present
                if hasattr(request, 'args'):
                    include_comments = request.args.get('include_comments', 'false').lower() == 'true'
                    if include_comments:
                        cache_key_str += ":comments"
                
                # Try to get from cache
                cached_result = cache.get(cache_key_str)
                if cached_result is not None:
                    # Record cache hit
                    if OPTIMIZATION_AVAILABLE:
                        get_cache_metrics().record_hit()
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
                    should_cache = True
                    if OPTIMIZATION_AVAILABLE:
                        should_cache = should_cache_response(json_data)
                    
                    if should_cache and json_data and isinstance(result, tuple) and len(result) >= 2 and result[1] == 200:
                        cache.set(cache_key_str, json_data, timeout=timeout)
                        
                        # Record cache miss (we're setting cache)
                        if OPTIMIZATION_AVAILABLE:
                            get_cache_metrics().record_miss()
            except Exception:
                # If caching fails, just return the result
                pass
            
            return result
        return decorated_function
    return decorator

def cached_search(timeout=300):
    """Decorator to cache search results"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Generate cache key from search query and filters
                if hasattr(request, 'args'):
                    query_params = dict(request.args)
                    cache_key_str = f"posts:search:{generate_cache_key('search', **query_params)}"
                    
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
                    should_cache = True
                    if OPTIMIZATION_AVAILABLE:
                        should_cache = should_cache_response(json_data)
                    
                    if should_cache and json_data and isinstance(result, tuple) and len(result) >= 2 and result[1] == 200:
                        cache.set(cache_key_str, json_data, timeout=timeout)
                        
                        # Record cache miss (we're setting cache)
                        if OPTIMIZATION_AVAILABLE:
                            get_cache_metrics().record_miss()
            except Exception:
                # If caching fails, just return the result
                pass
            
            return result
        return decorated_function
    return decorator

def invalidate_post_cache(post_id=None, slug=None, user_id=None):
    """Invalidate post-related cache entries"""
    try:
        # Invalidate specific post cache
        if post_id:
            try:
                cache.delete(f"posts:detail:{post_id}")
            except Exception:
                pass
            try:
                cache.delete(f"posts:detail:{post_id}:comments")
            except Exception:
                pass
        
        if slug:
            try:
                cache.delete(f"posts:slug:{slug}")
            except Exception:
                pass
            try:
                cache.delete(f"posts:slug:{slug}:comments")
            except Exception:
                pass
        
        # Optimized: Use Redis SCAN for pattern matching instead of clearing all cache
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
                        except Exception:
                            pass
                
                # Invalidate search caches using SCAN
                for key in redis_client.scan_iter(match='posts:search:*', count=100):
                    try:
                        redis_client.delete(key)
                    except Exception:
                        pass
            else:
                # Fallback: Clear common pagination patterns
                for page in range(1, 11):
                    for per_page in [20, 50, 100]:
                        patterns = [
                            f"posts:list:{hashlib.md5(f'list:page:{page}:per_page:{per_page}'.encode()).hexdigest()}",
                            f"posts:list:{hashlib.md5(f'list:page:{page}:per_page:{per_page}:user_id:{user_id}'.encode()).hexdigest()}" if user_id else None,
                        ]
                        for pattern in patterns:
                            if pattern:
                                try:
                                    cache.delete(pattern)
                                except Exception:
                                    pass
        except Exception:
            # If all else fails, silently continue (don't clear all cache)
            pass
    except Exception:
        # Silently fail if cache is unavailable (e.g., Redis not running)
        pass

def invalidate_category_cache(category_id=None):
    """Invalidate category-related cache"""
    try:
        if category_id:
            try:
                cache.delete(f"categories:detail:{category_id}")
            except Exception:
                pass
        
        # Clear category list cache
        try:
            cache.delete("categories:list")
        except Exception:
            pass
    except Exception:
        # Silently fail if cache is unavailable (e.g., Redis not running)
        pass

def invalidate_comment_cache(post_id=None, comment_id=None):
    """Invalidate comment-related cache"""
    try:
        if post_id:
            # Invalidate post comments cache
            try:
                cache.delete(f"posts:detail:{post_id}:comments")
            except Exception:
                pass
            # Try to find and invalidate slug-based cache
            try:
                from app.models.post import Post
                post = Post.query.get(post_id)
                if post:
                    cache.delete(f"posts:slug:{post.slug}:comments")
                    cache.delete(f"posts:slug:{post.slug}")
            except Exception:
                pass
            # Also invalidate the post itself since comment count changed
            try:
                cache.delete(f"posts:detail:{post_id}")
            except Exception:
                pass
        
        if comment_id:
            try:
                cache.delete(f"comments:detail:{comment_id}")
            except Exception:
                pass
    except Exception:
        # Silently fail if cache is unavailable (e.g., Redis not running)
        pass
