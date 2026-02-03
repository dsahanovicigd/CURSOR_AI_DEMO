# Swagger UI Troubleshooting

## Server Status ✅
The server is running and Swagger is configured correctly. Here's how to access it:

## Access Swagger UI

### Correct URL:
```
http://localhost:5001/api/docs
```

**NOT:**
- ❌ `http://localhost:5001/docs`
- ❌ `http://localhost:5001/swagger`
- ❌ `http://127.0.0.1:5001/api/docs` (should work but try localhost first)

## Troubleshooting Steps

### 1. Clear Browser Cache
- Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows/Linux)
- Or clear browser cache completely

### 2. Try Different Browser
- Chrome
- Firefox
- Safari
- Edge

### 3. Check Browser Console
Open browser developer tools (F12) and check for errors:
- Network tab: Look for failed requests
- Console tab: Look for JavaScript errors

### 4. Verify Server is Running
```bash
# Check if server is running
curl http://localhost:5001/api/health

# Should return: {"status": "healthy", "message": "API is running"}
```

### 5. Check Swagger Spec
```bash
# Verify Swagger spec is accessible
curl http://localhost:5001/api/apispec.json

# Should return JSON with API definitions
```

### 6. Restart the Server
If Swagger still doesn't load:

```bash
# Stop the server (Ctrl+C)
# Then restart:
cd flask_api
source venv/bin/activate
python run.py
```

### 7. Check Flask Logs
Look at the terminal where the server is running for any errors.

### 8. Alternative: Use Swagger JSON Directly
You can use the Swagger spec with external tools:
- Import `http://localhost:5001/api/apispec.json` into Postman
- Use Swagger Editor: https://editor.swagger.io/
  - File → Import URL → `http://localhost:5001/api/apispec.json`

## Common Issues

### Issue: "404 Not Found"
**Solution:** Make sure you're using `/api/docs` (not `/docs`)

### Issue: Blank Page
**Possible causes:**
- JavaScript disabled in browser
- CORS issues (unlikely for localhost)
- Browser compatibility

**Solution:** 
- Enable JavaScript
- Try a different browser
- Check browser console for errors

### Issue: "Swagger UI not loading"
**Solution:**
- Check if `/api/apispec.json` is accessible
- Verify Flasgger is installed: `pip list | grep flasgger`
- Reinstall if needed: `pip install flasgger`

### Issue: "Connection refused"
**Solution:**
- Server is not running
- Start it: `python run.py`
- Check if port 5001 is available

## Verify Installation

```bash
cd flask_api
source venv/bin/activate

# Check Flasgger is installed
pip show flasgger

# Should show version and location
```

## Manual Test

Test the endpoints directly without Swagger:

```bash
# Health check
curl http://localhost:5001/api/health

# Get posts
curl http://localhost:5001/api/posts

# Get categories
curl http://localhost:5001/api/categories
```

## If All Else Fails

1. **Check server logs** - Look for errors in the terminal
2. **Reinstall Flasgger**:
   ```bash
   pip uninstall flasgger
   pip install flasgger==0.9.7.1
   ```
3. **Check Flask version compatibility**
4. **Try accessing via IP**: `http://127.0.0.1:5001/api/docs`

## Quick Verification Script

Run this to verify everything is set up correctly:

```bash
python3 << EOF
import requests

base_url = "http://localhost:5001/api"

# Test health endpoint
try:
    r = requests.get(f"{base_url}/health")
    print(f"✅ Health check: {r.status_code} - {r.json()}")
except Exception as e:
    print(f"❌ Health check failed: {e}")

# Test Swagger spec
try:
    r = requests.get(f"{base_url}/apispec.json")
    print(f"✅ Swagger spec: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"   Found {len(data.get('paths', {}))} endpoints")
except Exception as e:
    print(f"❌ Swagger spec failed: {e}")

# Test Swagger UI
try:
    r = requests.get(f"{base_url}/docs")
    print(f"✅ Swagger UI: {r.status_code}")
    if r.status_code == 200:
        print("   Swagger UI is accessible!")
except Exception as e:
    print(f"❌ Swagger UI failed: {e}")
EOF
```

## Still Having Issues?

If Swagger UI still doesn't work, you can:
1. Use Postman to import the API spec
2. Use curl commands (see QUICK_START.md)
3. Use the API directly from your application
4. Check the server terminal for detailed error messages
