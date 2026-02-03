# Redis Activity Investigation - Root Cause Found

## 🔍 Investigation Results

### Root Cause: Flask-Limiter Using Redis by Default

**Problem:**
- Flask-Limiter is configured **without** an explicit `storage_uri`
- When `storage_uri` is not specified, Flask-Limiter **defaults to using Redis**
- Flask-Limiter checks Redis on **EVERY API request** (including health checks)
- Even when the app appears idle, any health checks or monitoring tools trigger Redis operations

**Evidence:**
- ✅ Flask-Limiter configured: `limiter = Limiter(key_func=get_remote_address, default_limits=["100 per minute"])`
- ⚠️ No `storage_uri` parameter specified
- ⚠️ Health check endpoint exists at `/api/health`
- ⚠️ 10 Redis connections from Python process (Flask app)
- ✅ No Celery workers running (not the issue)

### Current Configuration

```python
# flask_api/app/__init__.py line 18
limiter = Limiter(key_func=get_remote_address, default_limits=["100 per minute"])
```

**This defaults to Redis storage**, which means:
- Every API request triggers Redis GET/SET operations
- Health checks trigger Redis operations
- Rate limiting state is stored in Redis

---

## ✅ Solution: Use In-Memory Storage for Development

For development, you can switch Flask-Limiter to use in-memory storage instead of Redis. This eliminates Redis activity from rate limiting.

### Option 1: Change to In-Memory Storage (Recommended for Development)

**Edit `flask_api/app/__init__.py`:**

```python
# Change line 18 from:
limiter = Limiter(key_func=get_remote_address, default_limits=["100 per minute"])

# To:
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per minute"],
    storage_uri="memory://"  # Use in-memory instead of Redis
)
```

**Pros:**
- ✅ Eliminates Redis activity from rate limiting
- ✅ Faster (no network calls)
- ✅ Perfect for development/single-server setups

**Cons:**
- ⚠️ Won't work across multiple server instances
- ⚠️ Rate limits reset on server restart

### Option 2: Keep Redis but Disable Rate Limiting (Development Only)

If you don't need rate limiting in development:

```python
# Comment out or conditionally disable limiter
if os.environ.get('FLASK_ENV') != 'development':
    limiter = Limiter(key_func=get_remote_address, default_limits=["100 per minute"])
else:
    # Create a no-op limiter for development
    limiter = None

# Then update limiter.init_app(app) to:
if limiter:
    limiter.init_app(app)
```

### Option 3: Keep Redis but Exclude Health Checks

Exclude health checks from rate limiting:

```python
# In flask_api/app/__init__.py, after limiter.init_app(app):
limiter.exempt(lambda: request.endpoint == 'health_check')
```

---

## 📊 Expected Impact

### Before Fix:
- Redis operations on every API request
- Health checks trigger Redis operations
- Multiple Redis connections maintained

### After Fix (Option 1):
- ✅ Zero Redis operations from Flask-Limiter
- ✅ Health checks don't hit Redis
- ✅ Redis only used for caching (if needed)

---

## 🧪 Verification

After applying the fix, verify:

1. **Check Redis activity:**
   ```bash
   redis-cli MONITOR
   # Should see no limiter-related commands
   ```

2. **Test health endpoint:**
   ```bash
   curl http://localhost:5001/api/health
   # Should work without Redis operations
   ```

3. **Check connections:**
   ```bash
   lsof -i :6379
   # Should see fewer connections
   ```

---

## 🚀 Recommended Action

**For Development:** Use Option 1 (in-memory storage)
**For Production:** Keep Redis storage (it's correct for multi-server setups)

Would you like me to implement Option 1 (in-memory storage for development)?
