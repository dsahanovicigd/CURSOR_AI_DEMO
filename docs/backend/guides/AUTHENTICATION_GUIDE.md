# Authentication Guide

## 🔐 How to Use JWT Authentication

All API endpoints (except `/api/auth/*` and `/api/health`) require JWT authentication via the `Authorization` header.

---

## 📋 Step-by-Step Guide

### 1. Register a New User

```bash
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

**Response:**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  ...
}
```

---

### 2. Login to Get Access Token

```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepass123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "johndoe",
    ...
  }
}
```

**⚠️ IMPORTANT:** Save the `access_token` - you'll need it for all authenticated requests!

---

### 3. Make Authenticated Requests

Include the token in the `Authorization` header using the `Bearer` scheme:

```bash
# Example: Get all tasks
curl http://localhost:5001/api/tasks \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**Full Example:**
```bash
# Set your token as a variable (bash/zsh)
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# Use it in requests
curl http://localhost:5001/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"
```

---

## 🔧 Common Authentication Errors

### Missing Authorization Header

**Error Response:**
```json
{
  "error": "Authorization header is missing or invalid.",
  "message": "Please include a valid JWT token in the Authorization header.",
  "format": "Authorization: Bearer <your_access_token>",
  "hint": "First, login at POST /api/auth/login to get an access_token"
}
```

**Solution:** Add the `Authorization` header to your request.

---

### Expired Token

**Error Response:**
```json
{
  "error": "Token has expired. Please refresh your token."
}
```

**Solution:** Use the refresh token to get a new access token:

```bash
curl -X POST http://localhost:5001/api/auth/refresh \
  -H "Authorization: Bearer <your_refresh_token>"
```

---

### Invalid Token

**Error Response:**
```json
{
  "error": "Invalid token. ..."
}
```

**Solution:** 
1. Make sure you copied the entire token
2. Ensure the token hasn't been tampered with
3. Login again to get a new token

---

## 📝 Complete Examples

### Example 1: Create a Task

```bash
# 1. Login first
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepass123"
  }')

# 2. Extract token (using jq if available)
TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access_token')

# 3. Create task with token
curl -X POST http://localhost:5001/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive API documentation",
    "priority": "high",
    "status": "pending"
  }'
```

---

### Example 2: Get User's Tasks

```bash
TOKEN="your_access_token_here"

curl http://localhost:5001/api/tasks \
  -H "Authorization: Bearer $TOKEN"
```

---

### Example 3: Create a Project

```bash
TOKEN="your_access_token_here"

curl -X POST http://localhost:5001/api/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Website Redesign",
    "description": "Complete redesign of company website",
    "status": "active"
  }'
```

---

### Example 4: Update a Task

```bash
TOKEN="your_access_token_here"

curl -X PUT http://localhost:5001/api/tasks/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress",
    "priority": "urgent"
  }'
```

---

## 🌐 Using in JavaScript/Fetch

```javascript
// Login
const loginResponse = await fetch('http://localhost:5001/api/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'johndoe',
    password: 'securepass123'
  })
});

const { access_token } = await loginResponse.json();

// Use token in subsequent requests
const tasksResponse = await fetch('http://localhost:5001/api/tasks', {
  headers: {
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json'
  }
});

const tasks = await tasksResponse.json();
```

---

## 🐍 Using in Python/Requests

```python
import requests

BASE_URL = "http://localhost:5001/api"

# Login
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={
        "username": "johndoe",
        "password": "securepass123"
    }
)

access_token = login_response.json()["access_token"]

# Use token in subsequent requests
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Get tasks
tasks_response = requests.get(
    f"{BASE_URL}/tasks",
    headers=headers
)

tasks = tasks_response.json()
```

---

## 🔄 Token Refresh

Access tokens expire after 1 hour. Use the refresh token to get a new access token:

```bash
curl -X POST http://localhost:5001/api/auth/refresh \
  -H "Authorization: Bearer <your_refresh_token>"
```

**Response:**
```json
{
  "access_token": "new_access_token_here"
}
```

---

## ✅ Quick Test Script

Save this as `test_auth.sh`:

```bash
#!/bin/bash

API_URL="http://localhost:5001/api"

# Login
echo "🔐 Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepass123"
  }')

TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "❌ Login failed!"
    echo $LOGIN_RESPONSE
    exit 1
fi

echo "✅ Login successful!"
echo "Token: ${TOKEN:0:50}..."

# Test authenticated endpoint
echo ""
echo "📋 Getting tasks..."
TASKS_RESPONSE=$(curl -s -X GET "$API_URL/tasks" \
  -H "Authorization: Bearer $TOKEN")

echo "Response:"
echo $TASKS_RESPONSE | python3 -m json.tool 2>/dev/null || echo $TASKS_RESPONSE
```

Make it executable and run:
```bash
chmod +x test_auth.sh
./test_auth.sh
```

---

## 📚 Swagger UI Testing

1. Go to http://localhost:5001/api/docs
2. Click "Authorize" button (top right)
3. Enter: `Bearer your_access_token_here` (must include "Bearer " prefix with space)
4. Click "Authorize"
5. Now you can test all endpoints directly from Swagger UI!

**Note:** Swagger UI requires the full format: `Bearer <token>` (not just the token alone)

---

## 🎯 Summary

1. **Login** → Get `access_token`
2. **Include header** → `Authorization: Bearer <token>`
3. **Make requests** → All protected endpoints work
4. **Refresh when expired** → Use refresh token

**Remember:** Always include the `Authorization: Bearer <token>` header for protected endpoints!
