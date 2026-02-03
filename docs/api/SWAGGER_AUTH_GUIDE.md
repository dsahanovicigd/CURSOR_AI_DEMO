# How to Add Auth Token in Swagger UI

## 🎯 Quick Guide

### Step 1: Open Swagger UI
Navigate to: **http://localhost:5001/api/docs**

---

### Step 2: Get Your Access Token

**Option A: Use Swagger UI to Login**

1. Find the **Authentication** section in Swagger UI
2. Click on `POST /api/auth/login`
3. Click **"Try it out"**
4. Enter your credentials:
   ```json
   {
     "username": "johndoe",
     "password": "securepass123"
   }
   ```
5. Click **"Execute"**
6. Copy the `access_token` from the response

**Option B: Use curl/Postman**
```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "password": "securepass123"}'
```

---

### Step 3: Authorize in Swagger UI

1. Look for the **"Authorize"** button (🔒) at the top right of Swagger UI
2. Click the **"Authorize"** button
3. In the popup, you'll see a field for **"Bearer"** or **"Value"**
4. Enter your token in this format (required):

   **Required Format (with Bearer prefix):**
   ```
   Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY...
   ```
   
   **Important:** You must include the word "Bearer" followed by a space, then your token.

5. Click **"Authorize"**
6. Click **"Close"**

---

### Step 4: Test Protected Endpoints

Now all protected endpoints will automatically include your token!

1. Find any endpoint (e.g., `GET /api/tasks`)
2. Click **"Try it out"**
3. Click **"Execute"**
4. The request will automatically include: `Authorization: Bearer <your_token>`

---

## 📸 Visual Guide

```
┌─────────────────────────────────────────┐
│  Swagger UI                            │
│                                         │
│  [🔒 Authorize]  ← Click this button!  │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ Available authorizations        │   │
│  │                                  │   │
│  │ Bearer (apiKey)                 │   │
│  │ ┌─────────────────────────────┐ │   │
│  │ │ Bearer <your_token_here>    │ │   │
│  │ └─────────────────────────────┘ │   │
│  │                                  │   │
│  │  [Authorize]  [Close]           │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

---

## 🔄 Refreshing Your Token

If your token expires:

1. Use `POST /api/auth/refresh` endpoint
2. Use your `refresh_token` (not access_token) in the Authorization header
3. Get a new `access_token`
4. Update Swagger UI authorization with the new token

---

## ✅ Verify Authorization is Working

After authorizing, you should see:

1. A **green 🔒 icon** next to protected endpoints
2. The **"Authorize"** button shows your token is active
3. When you click **"Try it out"** → **"Execute"**, requests succeed (not 401 errors)

---

## 🐛 Troubleshooting

### Problem: "401 Unauthorized" after authorizing

**Solutions:**
- Make sure you copied the **entire** token (they're long!)
- Check if token has expired (tokens expire after 1 hour)
- Try logging in again to get a fresh token
- Make sure you entered the token correctly (no extra spaces)

### Problem: Can't find "Authorize" button

**Solution:**
- Make sure you're viewing Swagger UI at `/api/docs`
- Try refreshing the page
- Check browser console for errors

### Problem: Token works in curl but not Swagger

**Solution:**
- In Swagger, you must enter the token with "Bearer " prefix: `Bearer <your_token>`
- Make sure there's exactly one space between "Bearer" and your token
- Make sure there are no extra spaces before/after
- Example: `Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...`

---

## 💡 Pro Tips

1. **Copy token from login response** - The easiest way is to login via Swagger UI and copy the token directly from the response

2. **Token format** - You must include "Bearer " prefix: `Bearer <your_token>` (with space between Bearer and token)

3. **Multiple tokens** - You can authorize with multiple tokens if needed (though usually one is enough)

4. **Token expiration** - Access tokens expire after 1 hour. You'll need to refresh or login again

5. **Save your token** - Keep your token handy in a text file or password manager for quick access

---

## 📝 Example Workflow

```bash
# 1. Login and get token
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "password": "securepass123"}'

# Response:
# {
#   "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
#   "refresh_token": "...",
#   "user": {...}
# }

# 2. Copy the access_token

# 3. In Swagger UI:
#    - Click "Authorize" button
#    - Paste token in the Bearer field
#    - Click "Authorize"
#    - Click "Close"

# 4. Now test any endpoint!
```

---

## 🎓 Summary

1. **Login** → Get `access_token`
2. **Click "Authorize"** → Enter token
3. **Test endpoints** → Token automatically included!

That's it! Once authorized, all your Swagger requests will include the authentication token automatically.
