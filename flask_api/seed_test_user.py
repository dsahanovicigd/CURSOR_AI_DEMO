"""
Script to seed a test user for e-commerce testing
Run this script to create a test user that can be used for auto-login
"""
from app import create_app, db
from app.models import User

def seed_test_user():
    """Create test user if it doesn't exist"""
    app = create_app()
    with app.app_context():
        # Check if test user already exists
        test_user = User.query.filter_by(username='testcustomer').first()
        
        if test_user:
            print(f"✅ Test user 'testcustomer' already exists (ID: {test_user.id})")
            return test_user
        
        # Create test user
        test_user = User(
            username='testcustomer',
            email='customer@example.com',
            role=User.ROLE_CUSTOMER,
            is_active=True,
            first_name='Test',
            last_name='Customer'
        )
        test_user.set_password('customerpassword123')
        
        db.session.add(test_user)
        db.session.commit()
        
        print(f"✅ Test user 'testcustomer' created successfully (ID: {test_user.id})")
        print(f"   Username: testcustomer")
        print(f"   Password: customerpassword123")
        print(f"   Email: customer@example.com")
        
        return test_user

if __name__ == '__main__':
    seed_test_user()
