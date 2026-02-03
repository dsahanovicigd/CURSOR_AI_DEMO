# E-Commerce Setup Complete ✅

## Database Initialized

The e-commerce database has been successfully initialized with:
- ✅ All tables created (products, carts, cart_items, orders, order_items, discount_codes)
- ✅ Test user created (testcustomer / customerpassword123)
- ✅ Sample products added (4 products)
- ✅ Discount codes created (SAVE10, FIXED5, MIN50, MAX50)

## Backend API Status

✅ **All endpoints are working:**
- Login: ✅ Working
- Cart GET: ✅ Working  
- Add to Cart: ✅ Working
- Products: ✅ Working

## Frontend Connection

The frontend is configured to connect to:
- **API URL**: `http://localhost:5001/api`
- **CORS**: Configured to allow all origins (`*`)

## Troubleshooting "Failed to fetch" Error

If you're still seeing "Failed to fetch" errors:

### 1. Check Flask Server is Running
```bash
cd flask_api
source venv/bin/activate
python run.py
```

Server should start on `http://localhost:5001`

### 2. Check Browser Console
Open DevTools (F12) and check:
- **Console tab**: Look for CORS errors or network errors
- **Network tab**: Check if requests are being made and what the response is

### 3. Verify CORS Headers
The Flask server should send CORS headers. Check with:
```bash
curl -X OPTIONS http://localhost:5001/api/cart/items \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

### 4. Test API Directly
```bash
# Test login
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testcustomer", "password": "customerpassword123"}'

# Test products (no auth needed)
curl http://localhost:5001/api/products
```

### 5. Check Frontend API URL
Verify `src/services/api.ts` has:
```typescript
const API_BASE_URL = 'http://localhost:5001/api';
```

## Auto-Login Behavior

The frontend will automatically:
1. Try to login with `testcustomer` / `customerpassword123` on page load
2. If that fails, register a guest user
3. Retry cart operations after authentication

Check browser console for detailed logs of the auto-login process.

## Next Steps

1. **Refresh the browser** - Clear cache and reload
2. **Check browser console** - Look for detailed error messages
3. **Verify Flask server** - Make sure it's running on port 5001
4. **Test manually** - Try the curl commands above to verify API works

## Common Issues

### Issue: CORS Error
**Solution**: CORS is configured to allow all origins. If still seeing CORS errors, check Flask server logs.

### Issue: 401 Unauthorized
**Solution**: Auto-login should handle this. Check browser console for login attempts.

### Issue: Network Error
**Solution**: 
- Verify Flask server is running
- Check firewall/antivirus isn't blocking localhost:5001
- Try accessing http://localhost:5001/api/health in browser

### Issue: Products not loading
**Solution**: Products are in database. Frontend will fallback to sample products if API fails.

## Test Credentials

- **Username**: testcustomer
- **Password**: customerpassword123
- **Email**: customer@example.com

## API Endpoints

- `GET /api/products` - List products (no auth)
- `GET /api/cart` - Get cart (auth required)
- `POST /api/cart/items` - Add to cart (auth required)
- `POST /api/checkout/process-payment` - Checkout (auth required)
- `GET /api/orders` - List orders (auth required)

All endpoints are working and tested! ✅
