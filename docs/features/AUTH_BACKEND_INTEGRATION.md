# Authentication Backend Integration - Complete Guide

## ✅ Integration Complete

Successfully integrated frontend authentication with Flask backend JWT authentication system.

---

## 🔐 Backend Endpoints

### Available Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/api/auth/register` | POST | No | Register new user |
| `/api/auth/login` | POST | No | Login and get JWT tokens |
| `/api/auth/refresh` | POST | Refresh Token | Refresh access token |
| `/api/auth/me` | GET | Access Token | Get current user info |
| `/api/auth/logout` | POST | Access Token | Logout (client-side cleanup) |

### Request/Response Formats

#### Register
```typescript
POST /api/auth/register
Body: {
  username: string
  email: string
  password: string
  first_name?: string
  last_name?: string
  name?: string
}

Response: {
  id: number
  username: string
  email: string
  name?: string
  ...
}
```

#### Login
```typescript
POST /api/auth/login
Body: {
  username: string
  password: string
}

Response: {
  access_token: string      // JWT access token (1 hour expiry)
  refresh_token: string     // JWT refresh token (30 days expiry)
  user: {
    id: number
    username: string
    email: string
    name?: string
    ...
  }
}
```

#### Refresh Token
```typescript
POST /api/auth/refresh
Headers: {
  Authorization: "Bearer <refresh_token>"
}

Response: {
  access_token: string
}
```

#### Get Current User
```typescript
GET /api/auth/me
Headers: {
  Authorization: "Bearer <access_token>"
}

Response: {
  id: number
  username: string
  email: string
  name?: string
  first_name?: string
  last_name?: string
  role?: string
  ...
}
```

#### Logout
```typescript
POST /api/auth/logout
Headers: {
  Authorization: "Bearer <access_token>"
}

Response: {
  message: string
}
```

---

## 🔄 Token Management Flow

### Token Storage
- **Access Token**: Stored in `localStorage` as `auth_token`
- **Refresh Token**: Stored in `localStorage` as `refresh_token`

### Token Lifecycle

```
1. User logs in
   ↓
2. Backend returns access_token + refresh_token
   ↓
3. Tokens stored in localStorage
   ↓
4. Access token used for API requests (1 hour expiry)
   ↓
5. When access token expires:
   a. Frontend detects expiration
   b. Automatically calls /auth/refresh with refresh_token
   c. Gets new access_token
   d. Updates localStorage
   ↓
6. If refresh fails → User redirected to login
```

### Automatic Token Refresh

**Features:**
- ✅ Checks token expiration before each API request
- ✅ Automatically refreshes if token expires in < 5 minutes
- ✅ Periodic check every 5 minutes
- ✅ Retries failed requests after token refresh
- ✅ Handles 401 errors by attempting refresh

**Implementation:**
- `src/utils/tokenManager.ts` - Token utility functions
- `src/services/api.ts` - API request interceptor with auto-refresh
- `src/context/AuthContext.tsx` - Automatic refresh setup

---

## 📝 Frontend Integration

### AuthContext Usage

```typescript
import { useAuth } from '../context/AuthContext'

const MyComponent = () => {
  const { user, isAuthenticated, login, logout, isLoading } = useAuth()
  
  // Check authentication status
  if (isLoading) {
    return <div>Loading...</div>
  }
  
  if (!isAuthenticated) {
    return <LoginForm />
  }
  
  return <div>Welcome, {user?.name}!</div>
}
```

### Login Flow

```typescript
const handleLogin = async () => {
  try {
    await login(username, password)
    // User is now authenticated
    // Token stored automatically
    // User info loaded from backend
  } catch (error) {
    // Handle login error
    console.error('Login failed:', error)
  }
}
```

### Logout Flow

```typescript
const handleLogout = async () => {
  await logout()
  // Tokens cleared
  // User state cleared
  // Redirected to login (via ProtectedRoute)
}
```

### Protected Routes

```typescript
import ProtectedRoute from '../components/auth/ProtectedRoute'

<ProtectedRoute>
  <Dashboard />
</ProtectedRoute>
```

---

## 🔧 API Service Features

### Enhanced Features

1. **Automatic Token Refresh**
   - Checks token expiration before requests
   - Refreshes automatically if needed
   - Retries failed requests after refresh

2. **401 Error Handling**
   - Detects 401 Unauthorized responses
   - Attempts token refresh
   - Retries original request
   - Falls back to login if refresh fails

3. **Token Expiration Checking**
   - Validates token expiration client-side
   - Proactive refresh before expiration
   - Handles expired tokens gracefully

4. **Refresh Token Management**
   - Stores refresh token securely
   - Uses refresh token for token renewal
   - Clears tokens on logout

---

## 🎯 Usage Examples

### Login Example

```typescript
import { useAuth } from '../context/AuthContext'

const LoginPage = () => {
  const { login } = useAuth()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await login(username, password)
      // Redirect handled by ProtectedRoute
    } catch (error) {
      alert('Login failed: ' + error.message)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input value={username} onChange={(e) => setUsername(e.target.value)} />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button type="submit">Login</button>
    </form>
  )
}
```

### Making Authenticated API Calls

```typescript
import { apiRequest } from '../services/api'

// Token is automatically included in headers
const fetchTasks = async () => {
  try {
    const tasks = await apiRequest('/tasks', {
      method: 'GET'
    })
    return tasks
  } catch (error) {
    if (error.status === 401) {
      // Token refresh attempted automatically
      // If refresh fails, user will be redirected to login
    }
    throw error
  }
}
```

---

## 🔒 Security Features

### Token Security
- ✅ Tokens stored in localStorage (consider httpOnly cookies for production)
- ✅ Access token expiration: 1 hour
- ✅ Refresh token expiration: 30 days
- ✅ Automatic token refresh before expiration
- ✅ Token validation on client-side
- ✅ Secure token transmission via HTTPS (in production)

### Error Handling
- ✅ Network error detection
- ✅ 401 Unauthorized handling with auto-refresh
- ✅ Token expiration detection
- ✅ Graceful fallback to login

---

## 📊 Token Refresh Strategy

### Proactive Refresh
- Checks token expiration before each API request
- Refreshes if token expires within 5 minutes
- Periodic check every 5 minutes

### Reactive Refresh
- Detects 401 Unauthorized responses
- Attempts token refresh automatically
- Retries original request with new token

### Fallback
- If refresh fails → Clear tokens → Redirect to login
- User must login again

---

## 🧪 Testing

### Test Credentials
```
Username: testcustomer
Password: customerpassword123
```

### Test Flow
1. **Login**
   ```typescript
   await login('testcustomer', 'customerpassword123')
   ```

2. **Check Authentication**
   ```typescript
   const { isAuthenticated, user } = useAuth()
   console.log('Authenticated:', isAuthenticated)
   console.log('User:', user)
   ```

3. **Make Authenticated Request**
   ```typescript
   const tasks = await apiRequest('/tasks')
   ```

4. **Logout**
   ```typescript
   await logout()
   ```

---

## 🔄 Integration Checklist

- [x] Backend auth endpoints verified
- [x] Frontend API service updated
- [x] AuthContext integrated with backend
- [x] Token storage (access + refresh)
- [x] Automatic token refresh implemented
- [x] 401 error handling with auto-refresh
- [x] Token expiration checking
- [x] Protected routes working
- [x] Login form integrated
- [x] Logout functionality
- [x] User info from backend
- [x] Token refresh utility created
- [x] Periodic token refresh setup

---

## 📝 Files Modified/Created

### Created
- ✅ `src/utils/tokenManager.ts` - Token management utilities
- ✅ `AUTH_BACKEND_INTEGRATION.md` - This documentation

### Modified
- ✅ `src/services/api.ts` - Enhanced with token refresh, 401 handling
- ✅ `src/context/AuthContext.tsx` - Integrated with backend, auto-refresh
- ✅ `src/components/auth/LoginForm.tsx` - Uses AuthContext
- ✅ `src/pages/Dashboard.tsx` - Uses authenticated user info

---

## 🚀 Production Considerations

### Security Improvements Needed
1. **Use httpOnly Cookies** instead of localStorage for tokens
2. **Implement CSRF protection**
3. **Add token blacklisting** on logout
4. **Use secure, sameSite cookies**
5. **Implement rate limiting** on auth endpoints

### Performance Optimizations
1. **Cache user info** to reduce `/auth/me` calls
2. **Batch token refresh** requests
3. **Implement request queuing** during token refresh

---

## ✅ Integration Status

**Backend Integration**: ✅ Complete
- All endpoints connected
- Token management working
- User info fetching working

**Token Management**: ✅ Complete
- Access token storage
- Refresh token storage
- Automatic refresh
- Expiration handling

**Error Handling**: ✅ Complete
- 401 error handling
- Network error handling
- Token refresh failures
- Graceful fallbacks

**User Experience**: ✅ Complete
- Seamless login/logout
- Automatic token refresh
- Protected routes
- User info display

**The authentication system is fully integrated with the backend and ready for use!** 🎉
