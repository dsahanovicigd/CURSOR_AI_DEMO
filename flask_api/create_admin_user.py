#!/usr/bin/env python3
"""
Script to create an admin user for ticket assignment
"""
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Check if admin already exists
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        print(f"✅ Admin user already exists: {admin.username}")
        print(f"   Email: {admin.email}")
        print(f"   Role: {admin.role}")
        print(f"   is_admin_user(): {admin.is_admin_user()}")
        
        # Update to admin role if not already
        if admin.role != User.ROLE_ADMIN:
            admin.role = User.ROLE_ADMIN
            db.session.commit()
            print(f"   ✅ Updated role to admin")
    else:
        # Create admin user
        admin = User(
            username='admin',
            email='admin@example.com',
            name='System Administrator',
            role=User.ROLE_ADMIN,
            is_admin=True
        )
        admin.set_password('admin123')
        
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Admin user created successfully!")
        print(f"   Username: admin")
        print(f"   Email: admin@example.com")
        print(f"   Password: admin123")
        print(f"   Role: {admin.role}")
        print("\n⚠️  Please change the password after first login!")
