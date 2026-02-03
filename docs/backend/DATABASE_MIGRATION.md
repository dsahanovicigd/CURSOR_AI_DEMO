# Database Migration Guide

## Issue Fixed
The `users` table was missing new columns added to support the customer support ticket system:
- `name` - Full name field
- `role` - User role (customer/agent/admin)
- `availability_status` - Agent availability status
- `expertise_areas` - Agent expertise areas (JSON)

## Migration Script
A migration script (`migrate_users_table.py`) was created and executed to add these columns to the existing database.

## Migration Results
✅ Successfully added all missing columns:
- `name VARCHAR(200)` - Added
- `role VARCHAR(20) DEFAULT 'customer'` - Added (existing users set to 'customer')
- `availability_status VARCHAR(20)` - Added
- `expertise_areas JSON` - Added

## Verification
After migration:
- ✅ Database queries work correctly
- ✅ Authentication endpoints function properly
- ✅ All User model fields are accessible

## If You Need to Re-run Migration
```bash
cd flask_api
source venv/bin/activate
python3 migrate_users_table.py
```

The script is idempotent - it checks if columns exist before adding them, so it's safe to run multiple times.

## For Fresh Installations
If starting fresh, simply run:
```bash
python3 -c "from app import create_app, db; from app.models import *; app = create_app(); app.app_context().push(); db.create_all()"
```

This will create all tables with the correct schema from the start.
