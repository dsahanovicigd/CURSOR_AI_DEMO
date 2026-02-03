"""Redis caching utilities for task management API"""
from flask_caching import Cache
from flask_jwt_extended import get_jwt_identity
from functools import wraps
import hashlib
import json

cache = Cache()

def cache_key(*args, **kwargs):
    """Generate cache key from function arguments"""
    key_parts = [str(arg) for arg in args]
    key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
    key_string = ":".join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()

def cached_task_list(timeout=300):
    """Decorator to cache task list queries"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request
            
            # Generate cache key from query parameters and user
            query_params = dict(request.args)
            user_id = kwargs.get('current_user_id') or (get_jwt_identity() if hasattr(f, '__wrapped__') else None)
            cache_key_str = f"tasks:list:{cache_key(user_id, **query_params)}"
            
            # Try to get from cache
            cached_result = cache.get(cache_key_str)
            if cached_result is not None:
                from flask import jsonify
                return jsonify(cached_result), 200
            
            # Execute function and cache JSON data (not response object)
            result = f(*args, **kwargs)
            # Extract JSON data from response
            if hasattr(result, 'get_json'):
                json_data = result.get_json()
            elif isinstance(result, tuple) and len(result) == 2:
                json_data = result[0].get_json() if hasattr(result[0], 'get_json') else result[0]
            else:
                json_data = result
            
            # Cache the JSON data
            if json_data:
                cache.set(cache_key_str, json_data, timeout=timeout)
            
            return result
        return decorated_function
    return decorator

def cached_task_detail(timeout=600):
    """Decorator to cache individual task details"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            task_id = kwargs.get('task_id') or (args[0] if args else None)
            if not task_id:
                # If no task_id, just execute without caching
                return f(*args, **kwargs)
            
            cache_key_str = f"tasks:detail:{task_id}"
            
            cached_result = cache.get(cache_key_str)
            if cached_result is not None:
                from flask import jsonify
                return jsonify(cached_result), 200
            
            result = f(*args, **kwargs)
            # Extract JSON data from response
            if hasattr(result, 'get_json'):
                json_data = result.get_json()
            elif isinstance(result, tuple) and len(result) == 2:
                json_data = result[0].get_json() if hasattr(result[0], 'get_json') else result[0]
            else:
                json_data = result
            
            # Cache the JSON data
            if json_data:
                cache.set(cache_key_str, json_data, timeout=timeout)
            
            return result
        return decorated_function
    return decorator

def invalidate_task_cache(task_id=None, user_id=None):
    """Invalidate task-related cache entries"""
    if task_id:
        # Invalidate specific task cache
        cache.delete(f"tasks:detail:{task_id}")
    
    # Invalidate all task list caches
    # Since we can't pattern match, clear common cache patterns
    try:
        # Clear cache for common pagination patterns
        for page in range(1, 11):
            for per_page in [20, 50, 100]:
                # Try to clear with different filter combinations
                patterns = [
                    f"tasks:list:{user_id}:{page}:{per_page}:None:None:None:None",
                    f"tasks:list:{user_id}:{page}:{per_page}:*:*:*:*"
                ]
                for pattern in patterns:
                    try:
                        cache.delete(pattern)
                    except:
                        pass
        # Also try clearing all cache if user_id provided
        if user_id:
            # Clear all variations for this user
            for page in range(1, 6):
                for per_page in [20, 50]:
                    cache.delete(f"tasks:list:{user_id}:{page}:{per_page}:None:None:None:None")
    except:
        # If pattern deletion fails, clear entire cache (for testing)
        try:
            cache.clear()
        except:
            pass
    
    # Clear user task count cache
    if task_id:
        from app.models.task import Task
        task = Task.query.get(task_id)
        if task and task.assigned_to_id:
            cache.delete(f"users:{task.assigned_to_id}:task_count")

def cached_user_task_count(user_id, timeout=300):
    """Cache user's task count"""
    cache_key_str = f"users:{user_id}:task_count"
    
    cached_result = cache.get(cache_key_str)
    if cached_result is not None:
        return cached_result
    
    from app.models.task import Task
    count = Task.query.filter_by(assigned_to_id=user_id).count()
    cache.set(cache_key_str, count, timeout=timeout)
    return count
