"""
Initialize E-Commerce Database
Creates all tables and seeds initial data
"""
from app import create_app, db
from app.models import (
    User, Product, Cart, CartItem, Order, OrderItem, DiscountCode
)
from datetime import datetime, timedelta
from decimal import Decimal

def init_database():
    """Initialize database with all tables"""
    app = create_app()
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✅ All tables created successfully")
        
        # Create test user if it doesn't exist
        test_user = User.query.filter_by(username='testcustomer').first()
        if not test_user:
            print("Creating test user...")
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
            print("✅ Test user created")
        else:
            print("✅ Test user already exists")
        
        # Create sample products if none exist
        if Product.query.count() == 0:
            print("Creating sample products...")
            products = [
                Product(
                    title='Wireless Noise-Cancelling Headphones',
                    description='Premium over-ear headphones with active noise cancellation, 30-hour battery life, and studio-quality sound.',
                    price=Decimal('249.99'),
                    original_price=Decimal('349.99'),
                    currency='USD',
                    image='https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                    stock=100,
                    in_stock=True,
                    category='Electronics',
                    sku='PROD-001',
                    colors=['#000000', '#C0C0C0', '#1E3A8A'],
                    rating_average=Decimal('4.8'),
                    rating_count=2847,
                    badge_type='bestseller',
                    badge_text='Bestseller'
                ),
                Product(
                    title='Smart Watch Pro Series 8',
                    description='Advanced fitness tracking, heart rate monitoring, GPS, and water resistance.',
                    price=Decimal('399.99'),
                    original_price=Decimal('499.99'),
                    currency='USD',
                    image='https://images.unsplash.com/photo-1523275335684-37898b6baf30?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                    stock=50,
                    in_stock=True,
                    category='Wearables',
                    sku='PROD-002',
                    colors=['#000000', '#FFFFFF', '#FF6B6B'],
                    rating_average=Decimal('4.6'),
                    rating_count=1523,
                    badge_type='new',
                    badge_text='New Arrival'
                ),
                Product(
                    title='Ultra-Light Running Shoes',
                    description='Breathable mesh upper with responsive cushioning. Perfect for long-distance runs.',
                    price=Decimal('129.99'),
                    original_price=Decimal('179.99'),
                    currency='USD',
                    image='https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                    stock=75,
                    in_stock=True,
                    category='Footwear',
                    sku='PROD-003',
                    colors=['#000000', '#FFFFFF', '#FF0000'],
                    rating_average=Decimal('4.7'),
                    rating_count=892,
                    badge_type='sale',
                    badge_text='On Sale'
                ),
                Product(
                    title='Premium Coffee Maker',
                    description='Programmable coffee maker with thermal carafe. Makes 12 cups.',
                    price=Decimal('89.99'),
                    currency='USD',
                    image='https://images.unsplash.com/photo-1517668808823-f8c76b6e3b8a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                    stock=0,
                    in_stock=False,
                    category='Appliances',
                    sku='PROD-004',
                    rating_average=Decimal('4.5'),
                    rating_count=456
                ),
            ]
            
            for product in products:
                db.session.add(product)
            
            db.session.commit()
            print(f"✅ Created {len(products)} sample products")
        else:
            print(f"✅ Products already exist ({Product.query.count()} products)")
        
        # Create discount codes if none exist
        if DiscountCode.query.count() == 0:
            print("Creating discount codes...")
            discount_codes = [
                DiscountCode(
                    code='SAVE10',
                    discount_type='percentage',
                    discount_percent=Decimal('10.00'),
                    min_purchase=Decimal('0.00'),
                    expires_at=datetime.utcnow() + timedelta(days=30),
                    is_active=True
                ),
                DiscountCode(
                    code='FIXED5',
                    discount_type='fixed',
                    discount_amount=Decimal('5.00'),
                    min_purchase=Decimal('0.00'),
                    is_active=True
                ),
                DiscountCode(
                    code='MIN50',
                    discount_type='percentage',
                    discount_percent=Decimal('10.00'),
                    min_purchase=Decimal('50.00'),
                    is_active=True
                ),
                DiscountCode(
                    code='MAX50',
                    discount_type='percentage',
                    discount_percent=Decimal('20.00'),
                    min_purchase=Decimal('0.00'),
                    max_discount=Decimal('50.00'),
                    is_active=True
                ),
            ]
            
            for code in discount_codes:
                db.session.add(code)
            
            db.session.commit()
            print(f"✅ Created {len(discount_codes)} discount codes")
        else:
            print(f"✅ Discount codes already exist ({DiscountCode.query.count()} codes)")
        
        print("\n🎉 Database initialization complete!")
        print("\nTest User Credentials:")
        print("  Username: testcustomer")
        print("  Password: customerpassword123")
        print("  Email: customer@example.com")

if __name__ == '__main__':
    init_database()
