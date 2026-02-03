# Role Update Security - Implementation Guide

## Overview

The user update endpoint has been secured to ensure only administrators can change user roles. Non-admin users cannot update roles even if they attempt to send the field in the request.

## Security Implementation

### 1. Schema Separation
- **`UserUpdateSchema`**: Regular users can update basic fields (email, name, password, etc.)
- **`UserAdminUpdateSchema`**: Admins can update all fields including `role` and `is_active`

### 2. Route-Level Protection
The `/api/users/<id>` PUT endpoint now:
- Checks if the current user is an admin
- Blocks role/is_active updates from non-admin users
- Validates admin-only fields separately
- Prevents admins from removing their own admin role
- Prevents admins from deactivating themselves

### 3. Request Validation
```python
# Non-admin users cannot update role
if not is_admin and 'role' in request_data:
    return 403 Forbidden

# Non-admin users cannot update is_active
if not is_admin and 'is_active' in request_data:
    return 403 Forbidden
```

## Usage Examples

### ✅ Admin Updating User Role
```bash
# Login as admin
TOKEN=$(curl -s -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# Update user role to agent
curl -X PUT http://localhost:5001/api/users/2 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "agent",
    "availability_status": "available",
    "expertise_areas": ["technical", "billing"]
  }'
```

### ❌ Non-Admin Attempting to Update Role
```bash
# Login as regular user
TOKEN=$(curl -s -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"johndoe","password":"password123"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# Attempt to update own role (will fail)
curl -X PUT http://localhost:5001/api/users/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "admin"
  }'

# Response: 403 Forbidden
# {
#   "status": "error",
#   "message": "Access denied. Only administrators can update user role or active status.",
#   "code": "FORBIDDEN"
# }
```

### ✅ Regular User Updating Own Profile (Without Role)
```bash
# Login as regular user
TOKEN=$(curl -s -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"johndoe","password":"password123"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# Update own profile (allowed)
curl -X PUT http://localhost:5001/api/users/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe Updated",
    "email": "newemail@example.com"
  }'
```

## Security Features

### 1. Role Update Protection
- ✅ Only admins can change user roles
- ✅ Non-admin requests with `role` field are rejected
- ✅ Field is filtered out before validation for non-admins

### 2. Self-Protection
- ✅ Admins cannot remove their own admin role
- ✅ Admins cannot deactivate their own account
- ✅ Prevents accidental lockout

### 3. Access Control
- ✅ Users can only update their own profile
- ✅ Admins can update any user
- ✅ Clear error messages for unauthorized attempts

## API Behavior

### Admin Updating User
```json
PUT /api/users/2
Authorization: Bearer <admin_token>
{
  "role": "agent",
  "availability_status": "available"
}
```
✅ **Allowed** - Admin can update role

### Regular User Updating Own Profile
```json
PUT /api/users/1
Authorization: Bearer <user_token>
{
  "name": "New Name",
  "email": "new@example.com"
}
```
✅ **Allowed** - User can update own profile (without role)

### Regular User Attempting Role Update
```json
PUT /api/users/1
Authorization: Bearer <user_token>
{
  "role": "admin"
}
```
❌ **Forbidden** - Returns 403 error

### Regular User Updating Another User
```json
PUT /api/users/2
Authorization: Bearer <user_token>
{
  "name": "Changed Name"
}
```
❌ **Forbidden** - Users can only update themselves

## Testing

### Test Cases
1. ✅ Admin can update any user's role
2. ✅ Admin cannot remove own admin role
3. ✅ Admin cannot deactivate own account
4. ✅ Regular user cannot update role
5. ✅ Regular user cannot update is_active
6. ✅ Regular user can update own profile (without role)
7. ✅ Regular user cannot update other users

### Test Script
```bash
# Test admin role update
./test_role_update.sh
```

## Summary

- ✅ Role updates restricted to admins only
- ✅ Non-admin users cannot change roles
- ✅ Field filtering prevents role updates from non-admins
- ✅ Self-protection prevents admin lockout
- ✅ Clear error messages for unauthorized attempts
- ✅ Maintains backward compatibility for other fields
