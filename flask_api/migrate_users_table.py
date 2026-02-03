#!/usr/bin/env python3
"""
Migration script to add new columns to users table
Adds: name, role, availability_status, expertise_areas
"""
import sqlite3
import os
from pathlib import Path

# Get database path
db_path = Path(__file__).parent / 'instance' / 'flask_api_dev.db'

if not db_path.exists():
    print(f"❌ Database not found at {db_path}")
    exit(1)

print(f"📦 Connecting to database: {db_path}")

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

try:
    # Check existing columns
    cursor.execute("PRAGMA table_info(users)")
    existing_columns = [row[1] for row in cursor.fetchall()]
    print(f"📋 Existing columns: {existing_columns}")
    
    # Add name column if it doesn't exist
    if 'name' not in existing_columns:
        print("➕ Adding 'name' column...")
        cursor.execute("ALTER TABLE users ADD COLUMN name VARCHAR(200)")
        print("✅ Added 'name' column")
    else:
        print("✓ 'name' column already exists")
    
    # Add role column if it doesn't exist
    if 'role' not in existing_columns:
        print("➕ Adding 'role' column...")
        cursor.execute("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'customer'")
        # Update existing users to have customer role
        cursor.execute("UPDATE users SET role = 'customer' WHERE role IS NULL")
        print("✅ Added 'role' column")
    else:
        print("✓ 'role' column already exists")
    
    # Add availability_status column if it doesn't exist
    if 'availability_status' not in existing_columns:
        print("➕ Adding 'availability_status' column...")
        cursor.execute("ALTER TABLE users ADD COLUMN availability_status VARCHAR(20)")
        print("✅ Added 'availability_status' column")
    else:
        print("✓ 'availability_status' column already exists")
    
    # Add expertise_areas column if it doesn't exist
    if 'expertise_areas' not in existing_columns:
        print("➕ Adding 'expertise_areas' column...")
        cursor.execute("ALTER TABLE users ADD COLUMN expertise_areas JSON")
        print("✅ Added 'expertise_areas' column")
    else:
        print("✓ 'expertise_areas' column already exists")
    
    # Commit changes
    conn.commit()
    print("\n✅ Migration completed successfully!")
    
    # Verify
    cursor.execute("PRAGMA table_info(users)")
    final_columns = [row[1] for row in cursor.fetchall()]
    print(f"\n📋 Final columns: {final_columns}")
    
except sqlite3.Error as e:
    print(f"❌ Error during migration: {e}")
    conn.rollback()
    raise
finally:
    conn.close()
