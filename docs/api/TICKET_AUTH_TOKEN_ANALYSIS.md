# Ticket Endpoints Authentication Token Analysis

## Overview

This document analyzes how authentication tokens are used across all ticket-related endpoints in the Flask API.

## Authentication Methods Used

### 1. Required Authentication (`@jwt_required()`)
Most endpoints require a valid JWT token in the `Authorization` header:
```
Authorization: Bearer <token>
```

### 2. Optional Authentication (`verify_jwt_in_request(optional=True)`)
Some endpoints allow both authenticated and unauthenticated requests.

---

## Ticket Endpoints (`/api/tickets`)

### ✅ **GET `/api/tickets`** - List Tickets
**Authentication:** Required (`@jwt_required()`)

**Token Usage:**
```python
current_user_id = get_jwt_identity()  # Extract user ID from token
current_user = User.query.get(current_user_id)  # Load user from DB
```

**Access Control:**
- **Admin:** Can see all tickets
- **Agent:** Can see assigned tickets + unassigned queue
- **Customer:** Can only see own tickets (filtered by `customer_email`)

**Token Validation:** ✅ Validated via `@jwt_required()` decorator

---

### ⚠️ **POST `/api/tickets`** - Create Ticket
**Authentication:** Optional (Public endpoint)

**Token Usage:**
```python
try:
    from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
    verify_jwt_in_request(optional=True)  # Optional - won't fail if no token
    current_user_id = get_jwt_identity()
    if current_user_id:
        created_by_id = current_user_id  # Link ticket to user if authenticated
except:
    pass  # Continue without authentication
```

**Access Control:**
- **Authenticated users:** Ticket linked to user account (`created_by_id`)
- **Unauthenticated users:** Can create ticket with `customer_email` only

**Token Validation:** ⚠️ Optional - endpoint works without token

**Security Note:** Rate limiting applied (100/min via Flask-Limiter)

---

### ✅ **GET `/api/tickets/<id>`** - Get Ticket Details
**Authentication:** Required (`@jwt_required()`)

**Token Usage:**
```python
current_user_id = get_jwt_identity()
current_user = User.query.get(current_user_id)
ticket = Ticket.query.get_or_404(ticket_id)

# Check access based on role
if not check_ticket_access(ticket, current_user):
    return 403  # Forbidden
```

**Access Control:**
- **Admin:** Full access to all tickets
- **Agent:** Can access assigned tickets or unassigned tickets
- **Customer:** Can only access own tickets (`customer_email` match)

**Token Validation:** ✅ Validated via `@jwt_required()` decorator

---

### ✅ **PUT `/api/tickets/<id>`** - Update Ticket
**Authentication:** Required (`@jwt_required()`)

**Token Usage:**
```python
current_user_id = get_jwt_identity()
current_user = User.query.get(current_user_id)

# Only agents and admins can update
if not (current_user.is_agent() or current_user.is_admin_user()):
    return 403  # Forbidden
```

**Access Control:**
- **Admin:** ✅ Can update any ticket
- **Agent:** ✅ Can update tickets
- **Customer:** ❌ Cannot update tickets

**Token Validation:** ✅ Validated via `@jwt_required()` decorator

---

### ✅ **DELETE `/api/tickets/<id>`** - Delete Ticket
**Authentication:** Required (`@jwt_required()`)

**Token Usage:**
```python
current_user_id = get_jwt_identity()
current_user = User.query.get(current_user_id)

# Only admins can delete
if not current_user.is_admin_user():
    return 403  # Forbidden
```

**Access Control:**
- **Admin:** ✅ Can delete tickets
- **Agent:** ❌ Cannot delete tickets
- **Customer:** ❌ Cannot delete tickets

**Token Validation:** ✅ Validated via `@jwt_required()` decorator

---

### ✅ **PUT `/api/tickets/<id>/status`** - Update Status
**Authentication:** Required (`@jwt_required()`)

**Token Usage:**
```python
current_user_id = get_jwt_identity()
current_user = User.query.get(current_user_id)

# Check ticket access
if not check_ticket_access(ticket, current_user):
    return 403

# Only agents and admins can change status
if not (current_user.is_agent() or current_user.is_admin_user()):
    return 403
```

**Access Control:**
- **Admin:** ✅ Can change status of any accessible ticket
- **Agent:** ✅ Can change status of assigned/unassigned tickets
- **Customer:** ❌ Cannot change status

**Token Validation:** ✅ Validated via `@jwt_required()` decorator

---

### ✅ **PUT `/api/tickets/<id>/priority`** - Update Priority
**Authentication:** Required (`@jwt_required()`)

**Token Usage:**
```python
current_user_id = get_jwt_identity()
current_user = User.query.get(current_user_id)

# Only agents and admins can change priority
if not (current_user.is_agent() or current_user.is_admin_user()):
    return 403
```

**Access Control:**
- **Admin:** ✅ Can change priority
- **Agent:** ✅ Can change priority
- **Customer:** ❌ Cannot change priority

**Token Validation:** ✅ Validated via `@jwt_required()` decorator

---

### ✅ **POST `/api/tickets/<id>/assign`** - Assign Ticket
**Authentication:** Required (`@jwt_required()`)

**Token Usage:**
```python
current_user_id = get_jwt_identity()
current_user = User.query.get(current_user_id)

# Only admins can assign tickets
if not current_user.is_admin_user():
    return 403
```

**Access Control:**
- **Admin:** ✅ Can assign tickets
- **Agent:** ❌ Cannot assign tickets
- **Customer:** ❌ Cannot assign tickets

**Token Validation:** ✅ Validated via `@jwt_required()` decorator

---

### ✅ **GET `/api/tickets/<id>/history`** - Get Ticket History
**Authentication:** Required (`@jwt_required()`)

**Token Usage:**
```python
current_user_id = get_jwt_identity()
current_user = User.query.get(current_user_id)

# Check ticket access
if not check_ticket_access(ticket, current_user):
    return 403
```

**Access Control:**
- **Admin:** ✅ Can view history of all tickets
- **Agent:** ✅ Can view history of assigned/unassigned tickets
- **Customer:** ✅ Can view history of own tickets

**Token Validation:** ✅ Validated via `@jwt_required()` decorator

---

## Ticket Comment Endpoints (`/api/tickets/<id>/comments`)

### ✅ **GET `/api/tickets/<id>/comments`** - Get Comments
**Authentication:** Required (`@jwt_required()`)

**Token Usage:**
```python
current_user_id = get_jwt_identity()
current_user = User.query.get(current_user_id)

# Check ticket access
if not check_ticket_access(ticket, current_user):
    return 403

# Customers can't see internal comments
if current_user.is_customer():
    query = TicketComment.query.filter_by(is_internal=False)
```

**Access Control:**
- **Admin:** ✅ Can see all comments (including internal)
- **Agent:** ✅ Can see all comments (including internal)
- **Customer:** ✅ Can see only public comments (no internal)

**Token Validation:** ✅ Validated via `@jwt_required()` decorator

---

### ⚠️ **POST `/api/tickets/<id>/comments`** - Create Comment
**Authentication:** Optional (Public endpoint)

**Token Usage:**
```python
try:
    from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
    verify_jwt_in_request(optional=True)
    current_user_id = get_jwt_identity()
    if current_user_id:
        current_user = User.query.get(current_user_id)
        user_id = current_user_id
        customer_email = current_user.email
        
        # Agents/admins can create internal comments
        if data.get('is_internal') and not (current_user.is_agent() or current_user.is_admin_user()):
            return 403
except:
    # Customer comment without account
    customer_email = data.get('customer_email') or ticket.customer_email
```

**Access Control:**
- **Authenticated Admin/Agent:** ✅ Can create public or internal comments
- **Authenticated Customer:** ✅ Can create public comments only
- **Unauthenticated:** ✅ Can create public comments with `customer_email`

**Token Validation:** ⚠️ Optional - endpoint works without token

**Security Note:** Internal comments require authentication + agent/admin role

---

## Ticket Attachment Endpoints (`/api/tickets/<id>/attachments`)

### ✅ **POST `/api/tickets/<id>/attachments`** - Upload Attachment
**Authentication:** Required (`@jwt_required()`)

**Token Usage:**
```python
current_user_id = get_jwt_identity()
current_user = User.query.get(current_user_id)

# Check ticket access
if not check_ticket_access(ticket, current_user):
    return 403
```

**Access Control:**
- **Admin:** ✅ Can upload to any accessible ticket
- **Agent:** ✅ Can upload to assigned/unassigned tickets
- **Customer:** ✅ Can upload to own tickets

**Token Validation:** ✅ Validated via `@jwt_required()` decorator

---

### ✅ **GET `/api/tickets/<id>/attachments`** - List Attachments
**Authentication:** Required (`@jwt_required()`)

**Token Usage:**
```python
current_user_id = get_jwt_identity()
current_user = User.query.get(current_user_id)

# Check ticket access
if not check_ticket_access(ticket, current_user):
    return 403
```

**Access Control:**
- **Admin:** ✅ Can view attachments of all tickets
- **Agent:** ✅ Can view attachments of assigned/unassigned tickets
- **Customer:** ✅ Can view attachments of own tickets

**Token Validation:** ✅ Validated via `@jwt_required()` decorator

---

### ✅ **GET `/api/tickets/attachments/<id>`** - Download Attachment
**Authentication:** Required (`@jwt_required()`)

**Token Usage:**
```python
current_user_id = get_jwt_identity()
current_user = User.query.get(current_user_id)
attachment = TicketAttachment.query.get_or_404(attachment_id)
ticket = attachment.ticket

# Check ticket access
if not check_ticket_access(ticket, current_user):
    return 403
```

**Access Control:**
- **Admin:** ✅ Can download attachments from all tickets
- **Agent:** ✅ Can download attachments from assigned/unassigned tickets
- **Customer:** ✅ Can download attachments from own tickets

**Token Validation:** ✅ Validated via `@jwt_required()` decorator

---

### ✅ **DELETE `/api/tickets/attachments/<id>`** - Delete Attachment
**Authentication:** Required (`@jwt_required()`)

**Token Usage:**
```python
current_user_id = get_jwt_identity()
current_user = User.query.get(current_user_id)

# Only admins or uploader can delete
if not (current_user.is_admin_user() or 
        (attachment.uploaded_by_id == current_user_id) or
        check_ticket_access(ticket, current_user)):
    return 403
```

**Access Control:**
- **Admin:** ✅ Can delete any attachment
- **Uploader:** ✅ Can delete own attachments
- **Agent/Customer:** ✅ Can delete if they have ticket access

**Token Validation:** ✅ Validated via `@jwt_required()` decorator

---

## Summary Table

| Endpoint | Method | Auth Required | Token Usage | Role-Based Access |
|----------|--------|---------------|-------------|-------------------|
| `/api/tickets` | GET | ✅ Yes | `get_jwt_identity()` | Admin: All, Agent: Assigned+Queue, Customer: Own |
| `/api/tickets` | POST | ⚠️ Optional | `verify_jwt_in_request(optional=True)` | Public (with optional user linking) |
| `/api/tickets/<id>` | GET | ✅ Yes | `get_jwt_identity()` | Admin: All, Agent: Assigned+Queue, Customer: Own |
| `/api/tickets/<id>` | PUT | ✅ Yes | `get_jwt_identity()` | Admin/Agent only |
| `/api/tickets/<id>` | DELETE | ✅ Yes | `get_jwt_identity()` | Admin only |
| `/api/tickets/<id>/status` | PUT | ✅ Yes | `get_jwt_identity()` | Admin/Agent only |
| `/api/tickets/<id>/priority` | PUT | ✅ Yes | `get_jwt_identity()` | Admin/Agent only |
| `/api/tickets/<id>/assign` | POST | ✅ Yes | `get_jwt_identity()` | Admin only |
| `/api/tickets/<id>/history` | GET | ✅ Yes | `get_jwt_identity()` | Admin: All, Agent: Assigned+Queue, Customer: Own |
| `/api/tickets/<id>/comments` | GET | ✅ Yes | `get_jwt_identity()` | Admin/Agent: All, Customer: Public only |
| `/api/tickets/<id>/comments` | POST | ⚠️ Optional | `verify_jwt_in_request(optional=True)` | Public (internal requires auth+role) |
| `/api/tickets/<id>/attachments` | POST | ✅ Yes | `get_jwt_identity()` | Admin: All, Agent: Assigned+Queue, Customer: Own |
| `/api/tickets/<id>/attachments` | GET | ✅ Yes | `get_jwt_identity()` | Admin: All, Agent: Assigned+Queue, Customer: Own |
| `/api/tickets/attachments/<id>` | GET | ✅ Yes | `get_jwt_identity()` | Admin: All, Agent: Assigned+Queue, Customer: Own |
| `/api/tickets/attachments/<id>` | DELETE | ✅ Yes | `get_jwt_identity()` | Admin or Uploader |

---

## Key Findings

### ✅ **Properly Protected Endpoints**
- Most endpoints correctly use `@jwt_required()` decorator
- Token validation happens before any business logic
- User identity extracted via `get_jwt_identity()`

### ⚠️ **Public Endpoints (Intentional)**
- **POST `/api/tickets`** - Allows ticket creation without account (customer support use case)
- **POST `/api/tickets/<id>/comments`** - Allows customers to comment without account

### 🔒 **Access Control Implementation**
- Role-based access control implemented via `check_ticket_access()` helper
- Admin: Full access
- Agent: Assigned tickets + unassigned queue
- Customer: Own tickets only (by email)

### 📝 **Token Extraction Pattern**
```python
# Standard pattern for required auth
@jwt_required()
def endpoint():
    current_user_id = get_jwt_identity()  # Extract user ID from JWT
    current_user = User.query.get(current_user_id)  # Load user from DB
    # ... business logic ...
```

### 🔄 **Optional Auth Pattern**
```python
# Pattern for optional auth
def endpoint():
    try:
        from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
        verify_jwt_in_request(optional=True)  # Won't fail if no token
        current_user_id = get_jwt_identity()
        if current_user_id:
            # Use authenticated user
    except:
        # Handle unauthenticated case
        pass
```

---

## Security Recommendations

1. ✅ **Current Implementation is Good:**
   - Most endpoints properly protected
   - Role-based access control enforced
   - Token validation happens early

2. ⚠️ **Consider Adding:**
   - Rate limiting on public endpoints (already has 100/min default)
   - Token refresh mechanism for long sessions
   - Token revocation checking (if needed)

3. 📋 **Best Practices Followed:**
   - Token extraction happens after validation
   - User lookup happens after token validation
   - Access checks happen before data operations
   - Error messages don't leak sensitive information

---

## Testing Recommendations

When testing ticket endpoints:

1. **Test with valid token:**
   ```bash
   curl -H "Authorization: Bearer <token>" http://localhost:5000/api/tickets
   ```

2. **Test without token (should fail for protected endpoints):**
   ```bash
   curl http://localhost:5000/api/tickets  # Should return 401
   ```

3. **Test with invalid token:**
   ```bash
   curl -H "Authorization: Bearer invalid_token" http://localhost:5000/api/tickets  # Should return 401
   ```

4. **Test role-based access:**
   - Test as admin, agent, and customer
   - Verify each role sees appropriate tickets
   - Verify access denied for unauthorized actions
