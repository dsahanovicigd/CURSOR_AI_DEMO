# Celery Worker - How to Run

## Fixed Issue
The `celery_worker.py` script now properly handles command-line arguments for Celery.

## Method 1: Using Python Script (Fixed)

```bash
cd flask_api
source venv/bin/activate
python celery_worker.py
```

This will start the worker with default settings (info log level).

## Method 2: Using Celery CLI Directly (Recommended)

```bash
cd flask_api
source venv/bin/activate
celery -A celery_worker:celery worker --loglevel=info
```

## Method 3: With Custom Options

```bash
cd flask_api
source venv/bin/activate

# With custom log level
celery -A celery_worker:celery worker --loglevel=debug

# With concurrency settings
celery -A celery_worker:celery worker --loglevel=info --concurrency=4

# In background
celery -A celery_worker:celery worker --loglevel=info --detach
```

## Prerequisites

1. **Redis must be running:**
   ```bash
   # Check if Redis is running
   redis-cli ping
   # Should return: PONG
   
   # If not running, start it:
   brew services start redis  # macOS
   ```

2. **Flask app must be initialized** (handled automatically by the script)

## Expected Output

When running correctly, you should see:

```
-------------- celery@hostname v5.x.x
--- ***** ----- 
-- ******* ---- macOS-26.2-arm64-arm-64bit-Mach-O
- *** --- * --- 
- ** ---------- [config]
- ** ---------- .> app:         flask_api:0x...
- ** ---------- .> transport:   redis://localhost:6379/0    ← Redis!
- ** ---------- .> results:     redis://localhost:6379/0     ← Redis!
- *** --- * --- .> concurrency: 14 (prefork)
-- ******* ---- .> task events: OFF
--- ***** ----- 

[tasks]
  . celery_worker.task_name_here

[2026-01-30 13:XX:XX,XXX: INFO/MainProcess] Connected to redis://localhost:6379/0
[2026-01-30 13:XX:XX,XXX: INFO/MainProcess] celery@hostname ready.
```

## Troubleshooting

### If you see "Cannot connect to redis":
1. Make sure Redis is running: `redis-cli ping`
2. Check Redis URL in `.env`: `CELERY_BROKER_URL=redis://localhost:6379/0`

### If you see "No such command" error:
- Use Method 2 (Celery CLI) instead of the Python script
- Or make sure you're using the updated `celery_worker.py`

### Verify Configuration:
```bash
cd flask_api
source venv/bin/activate
python -c "from app import create_app; app = create_app(); print('Broker:', app.config['CELERY_BROKER_URL'])"
```

## Summary

✅ Fixed `celery_worker.py` to handle CLI arguments correctly
✅ Can now run with: `python celery_worker.py`
✅ Or use standard Celery CLI: `celery -A celery_worker:celery worker --loglevel=info`
