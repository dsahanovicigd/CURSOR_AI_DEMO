# Swagger UI Logout Fix

## 🔧 How to Logout/Clear Authorization in Swagger UI

### Method 1: Using Swagger UI's Logout Button

1. **Click the "Authorize" button** (🔒) at the top right of Swagger UI
2. In the popup, you'll see your authorized token(s)
3. **Click "Logout"** or **"Unauthorize"** button next to each token
4. Click **"Close"**

### Method 2: Clear All Authorizations

1. Click **"Authorize"** button
2. Click **"Logout"** or **"Clear"** button (if available)
3. Or manually delete the token value and click **"Authorize"** with empty field
4. Click **"Close"**

### Method 3: Browser Method (Most Reliable)

If Swagger UI's logout button isn't working:

1. **Open Browser DevTools** (F12 or Right-click → Inspect)
2. Go to **Application** tab (Chrome) or **Storage** tab (Firefox)
3. Expand **Local Storage**
4. Find the entry for `http://localhost:5001`
5. Look for keys like:
   - `authorized`
   - `swagger_auth`
   - `auth_token`
6. **Delete these entries** or clear all Local Storage
7. **Refresh the page** (F5)

### Method 4: Use the Logout Endpoint

1. In Swagger UI, find `POST /api/auth/logout`
2. Click **"Try it out"**
3. Make sure you're authorized (token is set)
4. Click **"Execute"**
5. This will call the logout endpoint
6. Then manually clear authorization using Method 1 or 3

---

## 🐛 Troubleshooting

### Problem: Logout button doesn't appear

**Solution:**
- Make sure you've authorized at least once
- Try refreshing the page
- Check browser console for JavaScript errors

### Problem: Logout button doesn't work

**Solution:**
- Use Method 3 (Browser DevTools) to manually clear storage
- Or refresh the page and don't authorize again

### Problem: Token still works after logout

**Note:** JWT tokens are stateless, so they remain valid until they expire. The logout endpoint is mainly for:
- Client-side cleanup
- API consistency
- Future token blacklisting implementation

To truly invalidate tokens, you would need to implement token blacklisting (storing revoked tokens in a database/Redis).

---

## ✅ Quick Fix: Clear Authorization

**Fastest way:**

1. Open Swagger UI: http://localhost:5001/api/docs
2. Press **F12** (open DevTools)
3. Go to **Console** tab
4. Run this command:
   ```javascript
   localStorage.clear(); sessionStorage.clear(); location.reload();
   ```
5. This will clear all stored data and refresh the page

---

## 📝 Summary

**To logout in Swagger UI:**

1. **Click "Authorize"** → **"Logout"** → **"Close"**
   OR
2. **Clear browser Local Storage** (most reliable)
   OR
3. **Use the logout endpoint** then clear authorization

The logout functionality in Swagger UI is client-side only - it just clears the stored token from your browser. The token itself remains valid until it expires (1 hour for access tokens).
