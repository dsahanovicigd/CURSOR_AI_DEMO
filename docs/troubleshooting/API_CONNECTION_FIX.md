# API Connection Fix

## Issue
Frontend cannot connect to Flask API running on `http://localhost:5001`, even though the API is running.

## Changes Made

### 1. Improved CORS Configuration (`flask_api/config.py`)
- Enhanced CORS_ORIGINS parsing to handle whitespace properly
- Ensures origins are properly formatted as a list

### 2. Enhanced CORS Settings (`flask_api/app/__init__.py`)
- Added PATCH method to allowed methods
- Added X-Requested-With to allowed headers
- Added expose_headers for better CORS support
- Added max_age for preflight caching

## Solution: Restart the API Server

The API server **must be restarted** to pick up the CORS configuration changes.

### Steps to Restart:

1. **Stop the current API server:**
   - Press `Ctrl+C` in the terminal where the API is running
   - Or run: `cd flask_api && ./stop.sh` (if available)

2. **Start the API server again:**
   ```bash
   cd /Users/dsahanovici/CURSOR_AI_DEMO/flask_api
   ./start.sh
   ```

   Or manually:
   ```bash
   cd /Users/dsahanovici/CURSOR_AI_DEMO/flask_api
   source venv/bin/activate
   python run.py
   ```

3. **Verify the API is accessible:**
   - Open browser: http://localhost:5001/api/health
   - Should return: `{"status": "healthy"}`
   - Swagger UI: http://localhost:5001/api/docs

## Verify CORS Configuration

After restarting, check that CORS is working:

1. Open browser DevTools (F12)
2. Go to Network tab
3. Try to login from the frontend
4. Check the OPTIONS preflight request - it should return 200 OK
5. Check the actual POST request - it should succeed

## Current CORS Configuration

From `.env`:
```
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

This allows:
- Frontend running on `http://localhost:5173` (Vite default)
- Frontend running on `http://localhost:3000` (alternative)

## Troubleshooting

### If still can't connect:

1. **Check API is actually running:**
   ```bash
   curl http://localhost:5001/api/health
   ```

2. **Check CORS headers in browser:**
   - Open DevTools → Network tab
   - Look for `Access-Control-Allow-Origin` header in response
   - Should be: `Access-Control-Allow-Origin: http://localhost:5173`

3. **Check browser console for errors:**
   - CORS errors will show: "CORS policy: No 'Access-Control-Allow-Origin' header"
   - Network errors will show: "Failed to fetch" or "NetworkError"

4. **Verify frontend URL matches CORS origins:**
   - Frontend must be running on exactly `http://localhost:5173`
   - Not `http://127.0.0.1:5173` (different origin!)

5. **Try accessing API directly:**
   ```bash
   curl -X POST http://localhost:5001/api/auth/login \
     -H "Content-Type: application/json" \
     -H "Origin: http://localhost:5173" \
     -d '{"username":"test","password":"test"}'
   ```

## Expected Behavior After Fix

- ✅ Frontend can make API requests
- ✅ CORS preflight (OPTIONS) requests succeed
- ✅ Login/Register endpoints work
- ✅ No CORS errors in browser console
