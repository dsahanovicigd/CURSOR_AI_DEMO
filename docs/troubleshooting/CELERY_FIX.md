# Celery Configuration Fix

## Issue
Celery worker was trying to connect to RabbitMQ (AMQP) on port 5672 instead of Redis.

## Root Cause
The `celery_worker.py` script was importing the placeholder Celery instance before the Flask app configuration was applied.

## Fix Applied

### 1. Updated `celery_worker.py`
Changed to properly initialize Flask app first, then get the configured Celery instance:

```python
from app import create_app

# Create Flask app to initialize Celery with proper configuration
app = create_app()

# Get the configured Celery instance from the Flask app
celery = app.celery
```

### 2. Added Redis Configuration to `.env`
Added explicit Redis URLs for Celery:
```
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## How to Run Celery Worker

### Prerequisites
1. **Redis must be running:**
   ```bash
   # macOS
   brew services start redis
   
   # Verify Redis is running
   redis-cli ping
   # Should return: PONG
   ```

### Start Celery Worker

**Option 1: Using the worker script (Recommended)**
```bash
cd flask_api
source venv/bin/activate
python celery_worker.py
```

**Option 2: Using Celery CLI directly**
```bash
cd flask_api
source venv/bin/activate

# Make sure Flask app is loaded first
export FLASK_APP=run.py
export FLASK_ENV=development

# Start worker with explicit broker URL
celery -A app.celery_app:celery worker \
  --broker=redis://localhost:6379/0 \
  --result-backend=redis://localhost:6379/0 \
  --loglevel=info
```

**Option 3: Using the updated command (after fix)**
```bash
cd flask_api
source venv/bin/activate

# This should now work correctly
celery -A celery_worker:celery worker --loglevel=info
```

## Expected Output

After the fix, you should see:
```
-------------- celery@hostname v5.x.x
--- ***** ----- 
-- ******* ---- macOS-26.2-arm64-arm-64bit-Mach-O
- *** --- * --- 
- ** ---------- [config]
- ** ---------- .> app:         flask_api:0x...
- ** ---------- .> transport:   redis://localhost:6379/0    ← Should show Redis, not AMQP
- ** ---------- .> results:     redis://localhost:6379/0   ← Should show Redis
- *** --- * --- .> concurrency: 14 (prefork)
-- ******* ---- .> task events: OFF
--- ***** ----- 
```

## Troubleshooting

### If Redis connection fails:
```bash
# Check if Redis is running
redis-cli ping

# If not running, start it:
brew services start redis  # macOS
# or
redis-server  # Manual start
```

### If still connecting to AMQP:
1. Make sure you're using the updated `celery_worker.py`
2. Verify `.env` has `CELERY_BROKER_URL=redis://localhost:6379/0`
3. Restart the Celery worker

### Verify Configuration:
```bash
cd flask_api
source venv/bin/activate
python -c "from app import create_app; app = create_app(); print('Broker:', app.config['CELERY_BROKER_URL']); print('Backend:', app.config['CELERY_RESULT_BACKEND'])"
```

Should output:
```
Broker: redis://localhost:6379/0
Backend: redis://localhost:6379/0
```

## Summary

✅ Fixed `celery_worker.py` to properly load Flask app configuration
✅ Added Redis URLs to `.env` file
✅ Celery now uses Redis instead of RabbitMQ

**Next Steps:**
1. Make sure Redis is running: `brew services start redis`
2. Restart Celery worker using one of the methods above
3. Verify it connects to Redis (check the transport line in output)
