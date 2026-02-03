# Redis Activity Investigation - Summary

## 🔍 Root Cause Identified

**Problem:** Flask-Limiter was using Redis by default, causing Redis operations on every API request.

**Evidence:**
- Flask-Limiter configured without `storage_uri` parameter
- Defaults to Redis storage when not specified
- Every API request (including health checks) triggers Redis GET/SET operations
- 10 Redis connections from Flask app process

## ✅ Solution Implemented

Changed Flask-Limiter to use **in-memory storage** by default (configurable via environment variable).

### Changes Made:

**File:** `flask_api/app/__init__.py`

**Before:**
```python
limiter = Limiter(key_func=get_remote_address, default_limits=["100 per minute"])
```

**After:**
```python
import os
limiter_storage = os.environ.get('LIMITER_STORAGE_URI', 'memory://')
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per minute"],
    storage_uri=limiter_storage
)
```

### Configuration Options:

1. **Development (Default):** Uses in-memory storage (`memory://`)
   - No Redis operations from rate limiting
   - Perfect for single-server development

2. **Production:** Set environment variable to use Redis
   ```bash
   export LIMITER_STORAGE_URI="redis://localhost:6379/1"
   ```
   - Works across multiple server instances
   - Persistent rate limiting state

## 📊 Expected Impact

### Before:
- ❌ Redis operations on every API request
- ❌ Health checks trigger Redis operations
- ❌ Multiple Redis connections for rate limiting

### After:
- ✅ Zero Redis operations from Flask-Limiter (in development)
- ✅ Health checks don't hit Redis
- ✅ Redis only used for caching (if configured)

## 🧪 Verification

After restarting your Flask app:

1. **Check Redis activity:**
   ```bash
   redis-cli MONITOR
   # Should see no limiter-related commands when idle
   ```

2. **Test the change:**
   ```bash
   # Make some API requests
   curl http://localhost:5001/api/health
   # Redis activity should be minimal
   ```

3. **For production, use Redis:**
   ```bash
   export LIMITER_STORAGE_URI="redis://localhost:6379/1"
   # Restart Flask app
   ```

## 📝 Notes

- **Development:** In-memory storage is perfect (no Redis activity)
- **Production:** Use Redis storage for multi-server setups
- **Redis is still used for:** Caching (if configured), Celery (if running)
- **Rate limiting still works:** Just uses in-memory instead of Redis

## 🔄 Next Steps

1. Restart your Flask application
2. Monitor Redis activity - should be significantly reduced
3. For production, set `LIMITER_STORAGE_URI` environment variable
