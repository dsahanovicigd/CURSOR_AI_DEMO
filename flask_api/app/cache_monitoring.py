"""Cache monitoring and analytics endpoints"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.cache import cache
from app.cache_optimization import get_cache_metrics, check_cache_health

cache_monitoring_bp = Blueprint('cache_monitoring', __name__)

@cache_monitoring_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_cache_stats():
    """Get cache statistics (admin only)"""
    from app.models.user import User
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user or not current_user.is_admin_user():
        return jsonify({'error': 'Forbidden: Admin access required'}), 403
    
    try:
        # Get Redis stats
        redis_client = cache.cache._client
        redis_info = {}
        
        if hasattr(redis_client, 'info'):
            redis_info = redis_client.info('stats')
            redis_info['memory'] = redis_client.info('memory')
            redis_info['keyspace'] = redis_client.info('keyspace')
        
        # Get application-level metrics
        app_metrics = get_cache_metrics()
        
        # Get cache health
        health = check_cache_health()
        
        # Count keys by pattern
        key_counts = {}
        if hasattr(redis_client, 'scan_iter'):
            patterns = ['posts:list:*', 'posts:detail:*', 'posts:search:*', 'posts:slug:*']
            for pattern in patterns:
                count = sum(1 for _ in redis_client.scan_iter(match=pattern, count=100))
                key_counts[pattern.replace('*', '')] = count
        
        return jsonify({
            'redis_stats': {
                'keyspace_hits': redis_info.get('keyspace_hits', 0),
                'keyspace_misses': redis_info.get('keyspace_misses', 0),
                'total_keys': redis_info.get('db0', {}).get('keys', 0) if 'db0' in redis_info.get('keyspace', {}) else 0,
                'memory_used': redis_info.get('memory', {}).get('used_memory_human', 'unknown'),
            },
            'app_metrics': app_metrics,
            'health': health,
            'key_counts': key_counts
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to get cache stats: {str(e)}'}), 500

@cache_monitoring_bp.route('/clear', methods=['POST'])
@jwt_required()
def clear_cache():
    """Clear all cache (admin only)"""
    from app.models.user import User
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user or not current_user.is_admin_user():
        return jsonify({'error': 'Forbidden: Admin access required'}), 403
    
    try:
        cache.clear()
        return jsonify({'message': 'Cache cleared successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to clear cache: {str(e)}'}), 500

@cache_monitoring_bp.route('/health', methods=['GET'])
def cache_health():
    """Check cache health (public endpoint)"""
    health = check_cache_health()
    return jsonify(health), 200
