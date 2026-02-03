#!/bin/bash

# Redis Activity Investigation Script

echo "=========================================="
echo "Redis Activity Investigation"
echo "=========================================="
echo ""

# Check if Redis is running
if ! lsof -i :6379 > /dev/null 2>&1; then
    echo "❌ Redis is not running on port 6379"
    exit 1
fi

echo "✅ Redis is running"
echo ""

# Check connections
echo "1. Redis Connections:"
echo "   -----------------"
lsof -i :6379 | grep -E "COMMAND|Python|node|celery" | head -15
echo ""

# Check Flask-Limiter configuration
echo "2. Flask-Limiter Configuration:"
echo "   ----------------------------"
if grep -q "limiter = Limiter" flask_api/app/__init__.py 2>/dev/null; then
    echo "   ✅ Flask-Limiter is configured"
    if grep -q "storage_uri" flask_api/app/__init__.py 2>/dev/null; then
        echo "   ⚠️  Using explicit storage (check config)"
    else
        echo "   ⚠️  No storage_uri specified - defaults to Redis!"
        echo "   This means Flask-Limiter checks Redis on EVERY request"
    fi
else
    echo "   ❌ Flask-Limiter not found"
fi
echo ""

# Check for Celery
echo "3. Celery Worker Status:"
echo "   --------------------"
if pgrep -f "celery.*worker" > /dev/null 2>&1; then
    echo "   ⚠️  Celery worker is running"
    echo "   Celery workers poll Redis every few seconds (normal behavior)"
    pgrep -f "celery.*worker" | while read pid; do
        echo "   PID: $pid"
    done
else
    echo "   ✅ No Celery workers running"
fi
echo ""

# Check for health checks
echo "4. Health Check Endpoints:"
echo "   ----------------------"
if grep -q "/api/health" flask_api/app/__init__.py 2>/dev/null; then
    echo "   ⚠️  Health check endpoint exists at /api/health"
    echo "   If something is polling this endpoint, it triggers Flask-Limiter"
    echo "   Each health check = Redis operations"
fi
echo ""

echo "=========================================="
echo "Root Cause Analysis"
echo "=========================================="
echo ""
echo "Most likely causes of Redis activity when idle:"
echo ""
echo "1. Flask-Limiter (MOST LIKELY)"
echo "   - Flask-Limiter uses Redis by default when no storage_uri is specified"
echo "   - Checks Redis on EVERY API request (including health checks)"
echo "   - Even if you're not using the app, health checks or monitoring tools"
echo "     might be hitting your API"
echo ""
echo "2. Celery Worker Polling"
echo "   - If Celery worker is running, it polls Redis every few seconds"
echo "   - This is normal behavior but causes Redis activity"
echo ""
echo "3. Multiple Redis Connections"
echo "   - Flask app creates multiple connections (connection pooling)"
echo "   - Each connection may do keep-alive pings"
echo ""

echo "=========================================="
echo "Solutions"
echo "=========================================="
echo ""
echo "Option 1: Change Flask-Limiter to use in-memory storage (Development)"
echo "   Edit flask_api/app/__init__.py:"
echo "   Change: limiter = Limiter(key_func=get_remote_address, ...)"
echo "   To:     limiter = Limiter(key_func=get_remote_address, storage_uri='memory://', ...)"
echo ""
echo "Option 2: Stop Celery worker (if not needed)"
echo "   pkill -f 'celery.*worker'"
echo ""
echo "Option 3: Monitor Redis activity to see exact commands"
echo "   redis-cli MONITOR"
echo ""
