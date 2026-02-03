# API Connection Troubleshooting Guide

## "Failed to fetch" Error

If you're seeing "Failed to fetch" when adding products to cart, it means the frontend cannot connect to the Flask API server.

## Quick Fixes

### 1. Start the Flask API Server

Make sure the Flask API is running:

```bash
cd flask_api
source venv/bin/activate
python run.py
```

The server should start on `http://localhost:5001` (or check `run.py` for the actual port).

### 2. Verify API URL

Check that the frontend is pointing to the correct API URL:
- Frontend API URL: `http://localhost:5001/api` (in `src/services/api.ts`)
- Flask server should be running on port `5001`

### 3. Check CORS Configuration

The Flask API should allow requests from `http://localhost:5173` (Vite dev server).

Current CORS config allows all origins (`*`), so this should work.

### 4. Create Test User

Run the seed script to create a test user:

```bash
cd flask_api
source venv/bin/activate
python seed_test_user.py
```

This creates:
- Username: `testcustomer`
- Password: `customerpassword123`
- Email: `customer@example.com`

### 5. Check Browser Console

Open browser DevTools (F12) and check:
- **Console tab**: Look for detailed error messages
- **Network tab**: Check if requests are being made and what the response is

## Common Issues

### Issue: Flask server not running
**Solution**: Start the Flask server with `python run.py`

### Issue: Wrong port
**Solution**: 
- Check `flask_api/run.py` for the port number
- Update `src/services/api.ts` if the port is different

### Issue: CORS blocking
**Solution**: 
- Check `flask_api/config.py` - CORS_ORIGINS should include your frontend URL
- Default is `*` which allows all origins

### Issue: Database not initialized
**Solution**: 
```bash
cd flask_api
source venv/bin/activate
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('✅ Database initialized')"
```

### Issue: Products not in database
**Solution**: Products need to be created. The frontend will fallback to sample products if API fails.

## Testing the Connection

### Test API Health
```bash
curl http://localhost:5001/api/health
```

Should return: `{"status": "healthy", "message": "API is running"}`

### Test Products Endpoint
```bash
curl http://localhost:5001/api/products
```

### Test Cart Endpoint (requires auth)
```bash
# First login to get token
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testcustomer", "password": "customerpassword123"}'

# Then use the token
curl http://localhost:5001/api/cart \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Frontend Error Messages

The frontend now shows specific error messages:

- **"Unable to connect to server"**: Flask API is not running
- **"401 Unauthorized"**: User needs to login (auto-login will attempt)
- **"Failed to add item to cart"**: Other error (check console for details)

## Auto-Login Behavior

The frontend will automatically:
1. Try to login with `testcustomer` / `customerpassword123`
2. If that fails, register a new guest user
3. Retry the cart operation after authentication

Check the browser console for detailed logs of the auto-login process.
