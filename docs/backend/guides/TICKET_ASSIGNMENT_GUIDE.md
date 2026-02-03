# Ticket Assignment Guide

## Issue: "Access denied" when assigning tickets

The ticket assignment endpoint requires **admin** role. If you're getting a FORBIDDEN error, you're likely logged in as a customer or agent.

## Solution: Use an Admin Account

### Option 1: Use the Pre-created Admin User

An admin user has been created with these credentials:
- **Username**: `admin`
- **Email**: `admin@example.com`
- **Password**: `admin123`
- **Role**: `admin`

⚠️ **Important**: Change the password after first login!

### Option 2: Create Your Own Admin User

#### Via API (Register + Update Role)
```bash
# 1. Register a new user
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "myadmin",
    "email": "myadmin@example.com",
    "password": "securepassword123",
    "role": "admin"
  }'

# 2. Login to get token
TOKEN=$(curl -s -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"myadmin","password":"securepassword123"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# 3. Now you can assign tickets
curl -X POST http://localhost:5001/api/tickets/1/assign \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assigned_to_id": 2,
    "notes": "Assigned to technical support"
  }'
```

#### Via Python Script
```bash
cd flask_api
source venv/bin/activate
python3 create_admin_user.py
```

### Option 3: Update Existing User to Admin

If you want to make an existing user an admin:

```bash
# Login as the user you want to promote
TOKEN=$(curl -s -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"yourusername","password":"yourpassword"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# Update user role (requires admin endpoint or direct DB update)
# Or use Python:
python3 -c "
from app import create_app, db
from app.models import User
app = create_app()
with app.app_context():
    user = User.query.filter_by(username='yourusername').first()
    if user:
        user.role = 'admin'
        user.is_admin = True
        db.session.commit()
        print(f'✅ {user.username} is now an admin')
"
```

## Testing Assignment

Once you have an admin account:

```bash
# 1. Login as admin
TOKEN=$(curl -s -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# 2. List agents
curl http://localhost:5001/api/agents \
  -H "Authorization: Bearer $TOKEN"

# 3. Assign ticket to agent (replace 1 with ticket_id, 2 with agent_id)
curl -X POST http://localhost:5001/api/tickets/1/assign \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assigned_to_id": 2,
    "notes": "Assigned to technical support team"
  }'
```

## Role Requirements (Per PRD)

According to the PRD:
- **FR-005**: Administrator can manually assign tickets to support agents
- **FR-009**: Administrators can reassign tickets to different agents
- **Permission Matrix**: Only admins can assign tickets

So the current implementation is correct - only admins can assign tickets.

## Troubleshooting

### Check Your Current Role
```bash
# Get your user info
curl http://localhost:5001/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Verify Admin Status
```python
from app import create_app, db
from app.models import User
app = create_app()
with app.app_context():
    user = User.query.filter_by(username='yourusername').first()
    print(f"Role: {user.role}")
    print(f"is_admin: {user.is_admin}")
    print(f"is_admin_user(): {user.is_admin_user()}")
```

## Summary

- ✅ Admin user created: `admin` / `admin123`
- ✅ Assignment requires admin role (per PRD)
- ✅ Use admin account to assign tickets
- ✅ Change default password after first login
