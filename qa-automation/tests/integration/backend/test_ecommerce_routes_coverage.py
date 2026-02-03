"""
Comprehensive E-Commerce Routes Coverage Tests
This test suite ensures all e-commerce routes are tested to achieve 80%+ coverage
"""

import unittest
from app import create_app, db
from app.models import User, Product, Cart, CartItem, Order, OrderItem, DiscountCode
from decimal import Decimal
from datetime import datetime, timedelta
from unittest.mock import patch
from app.models import Cart, CartItem, Order


class EcommerceRoutesCoverageTestCase(unittest.TestCase):
    """Test suite for comprehensive e-commerce route coverage"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        
        # Create database tables
        db.create_all()
        
        # Create test user
        self.user = User(
            username='testuser',
            email='test@example.com',
            role=User.ROLE_CUSTOMER,
            is_active=True
        )
        self.user.set_password('password123')
        db.session.add(self.user)
        db.session.commit()
        
        # Get auth token
        login_response = self.client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        self.token = login_response.json['access_token']
        self.headers = {'Authorization': f'Bearer {self.token}'}
        
        # Create test products
        self.product1 = Product(
            title='Test Product 1',
            description='Description 1',
            price=Decimal('29.99'),
            stock=100,
            in_stock=True,
            sku='PROD-001',
            category='Electronics'
        )
        self.product2 = Product(
            title='Test Product 2',
            description='Description 2',
            price=Decimal('49.99'),
            stock=50,
            in_stock=True,
            sku='PROD-002',
            category='Clothing'
        )
        self.product3 = Product(
            title='Out of Stock Product',
            description='Description 3',
            price=Decimal('99.99'),
            stock=0,
            in_stock=False,
            sku='PROD-003',
            category='Electronics'
        )
        db.session.add_all([self.product1, self.product2, self.product3])
        
        # Create discount codes
        self.discount1 = DiscountCode(
            code='SAVE10',
            discount_type='percentage',
            discount_percent=Decimal('10.00'),
            min_purchase=Decimal('0.00'),
            expires_at=datetime.utcnow() + timedelta(days=30),
            is_active=True
        )
        self.discount2 = DiscountCode(
            code='FIXED5',
            discount_type='fixed',
            discount_amount=Decimal('5.00'),
            min_purchase=Decimal('0.00'),
            is_active=True
        )
        self.discount3 = DiscountCode(
            code='EXPIRED',
            discount_type='percentage',
            discount_percent=Decimal('10.00'),
            expires_at=datetime.utcnow() - timedelta(days=1),
            is_active=True
        )
        db.session.add_all([self.discount1, self.discount2, self.discount3])
        db.session.commit()
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class TestProductsRoutes(EcommerceRoutesCoverageTestCase):
    """Test products routes for coverage"""
    
    def test_get_all_products(self):
        """Test GET /api/products"""
        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn('products', response.json)
        self.assertIn('pagination', response.json)
        self.assertEqual(len(response.json['products']), 3)
    
    def test_get_products_with_pagination(self):
        """Test GET /api/products with pagination"""
        response = self.client.get('/api/products?page=1&per_page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['products']), 2)
        self.assertEqual(response.json['pagination']['page'], 1)
        self.assertEqual(response.json['pagination']['per_page'], 2)
    
    def test_get_products_filter_by_category(self):
        """Test GET /api/products?category=Electronics"""
        response = self.client.get('/api/products?category=Electronics')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(p['category'] == 'Electronics' for p in response.json['products']))
    
    def test_get_products_search(self):
        """Test GET /api/products?search=Product"""
        response = self.client.get('/api/products?search=Product')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json['products']), 0)
    
    def test_get_products_in_stock_only(self):
        """Test GET /api/products?in_stock_only=true"""
        response = self.client.get('/api/products?in_stock_only=true')
        self.assertEqual(response.status_code, 200)
        # Filter out out-of-stock products - Product.to_dict() returns 'inStock' (camelCase)
        products = response.json['products']
        if products:
            self.assertTrue(all(p.get('inStock', False) for p in products))
    
    def test_get_product_by_id(self):
        """Test GET /api/products/<id>"""
        response = self.client.get(f'/api/products/{self.product1.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('product', response.json)
        # Product ID is returned as string in to_dict()
        self.assertEqual(int(response.json['product']['id']), self.product1.id)
    
    def test_get_nonexistent_product(self):
        """Test GET /api/products/99999"""
        response = self.client.get('/api/products/99999')
        self.assertEqual(response.status_code, 404)


class TestCartRoutes(EcommerceRoutesCoverageTestCase):
    """Test cart routes for coverage"""
    
    def test_get_cart_empty(self):
        """Test GET /api/cart when empty"""
        response = self.client.get('/api/cart', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('cart', response.json)
        self.assertEqual(len(response.json['cart']['items']), 0)
    
    def test_add_item_to_cart(self):
        """Test POST /api/cart/items"""
        response = self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product1.id,
            'quantity': 2
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('cart', response.json)
        self.assertEqual(len(response.json['cart']['items']), 1)
        self.assertEqual(response.json['cart']['items'][0]['quantity'], 2)
    
    def test_add_item_to_cart_invalid_product(self):
        """Test POST /api/cart/items with invalid product"""
        response = self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': 99999,
            'quantity': 1
        })
        self.assertEqual(response.status_code, 404)
    
    def test_add_item_to_cart_out_of_stock(self):
        """Test POST /api/cart/items with out of stock product"""
        response = self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product3.id,
            'quantity': 1
        })
        self.assertEqual(response.status_code, 400)
    
    def test_add_item_to_cart_exceeds_stock(self):
        """Test POST /api/cart/items with quantity exceeding stock"""
        response = self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product1.id,
            'quantity': 200
        })
        self.assertEqual(response.status_code, 400)
    
    def test_add_same_product_twice(self):
        """Test adding same product twice increases quantity"""
        self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product1.id,
            'quantity': 2
        })
        response = self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product1.id,
            'quantity': 3
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['cart']['items']), 1)
        self.assertEqual(response.json['cart']['items'][0]['quantity'], 5)
    
    def test_update_cart_item(self):
        """Test PUT /api/cart/items/<id>"""
        # Add item first
        add_response = self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product1.id,
            'quantity': 2
        })
        item_id = add_response.json['cart']['items'][0]['id']
        
        # Update item
        response = self.client.put(f'/api/cart/items/{item_id}', headers=self.headers, json={
            'quantity': 5
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['cart']['items'][0]['quantity'], 5)
    
    def test_update_cart_item_to_zero(self):
        """Test PUT /api/cart/items/<id> with quantity 0 removes item"""
        add_response = self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product1.id,
            'quantity': 2
        })
        item_id = add_response.json['cart']['items'][0]['id']
        
        response = self.client.put(f'/api/cart/items/{item_id}', headers=self.headers, json={
            'quantity': 0
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['cart']['items']), 0)
    
    def test_remove_cart_item(self):
        """Test DELETE /api/cart/items/<id>"""
        add_response = self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product1.id,
            'quantity': 2
        })
        item_id = add_response.json['cart']['items'][0]['id']
        
        response = self.client.delete(f'/api/cart/items/{item_id}', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['cart']['items']), 0)
    
    def test_clear_cart(self):
        """Test DELETE /api/cart"""
        # Add items
        self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product1.id,
            'quantity': 2
        })
        self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product2.id,
            'quantity': 1
        })
        
        # Clear cart
        response = self.client.delete('/api/cart', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['cart']['items']), 0)
    
    def test_apply_discount_code(self):
        """Test POST /api/cart/apply-discount"""
        # Add items first
        self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product1.id,
            'quantity': 2
        })
        
        # Apply discount
        response = self.client.post('/api/cart/apply-discount', headers=self.headers, json={
            'discount_code': 'SAVE10'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json['cart'].get('discount_code'))
    
    def test_apply_discount_empty_cart(self):
        """Test POST /api/cart/apply-discount with empty cart"""
        response = self.client.post('/api/cart/apply-discount', headers=self.headers, json={
            'discount_code': 'SAVE10'
        })
        self.assertEqual(response.status_code, 400)
    
    def test_apply_invalid_discount_code(self):
        """Test POST /api/cart/apply-discount with invalid code"""
        self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product1.id,
            'quantity': 1
        })
        
        response = self.client.post('/api/cart/apply-discount', headers=self.headers, json={
            'discount_code': 'INVALID'
        })
        self.assertEqual(response.status_code, 400)
    
    def test_apply_expired_discount_code(self):
        """Test POST /api/cart/apply-discount with expired code"""
        self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product1.id,
            'quantity': 1
        })
        
        response = self.client.post('/api/cart/apply-discount', headers=self.headers, json={
            'discount_code': 'EXPIRED'
        })
        # Expired code should return 400, but might return different error message
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
    
    def test_remove_discount_code(self):
        """Test DELETE /api/cart/discount"""
        # Add items and apply discount
        self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product1.id,
            'quantity': 1
        })
        self.client.post('/api/cart/apply-discount', headers=self.headers, json={
            'discount_code': 'SAVE10'
        })
        
        # Remove discount
        response = self.client.delete('/api/cart/discount', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json['cart'].get('discount_code'))


class TestCheckoutRoutes(EcommerceRoutesCoverageTestCase):
    """Test checkout routes for coverage"""
    
    def test_process_payment_empty_cart(self):
        """Test POST /api/checkout/process-payment with empty cart"""
        # Ensure cart exists but is empty
        cart = Cart.query.filter_by(user_id=self.user.id).first()
        if cart:
            CartItem.query.filter_by(cart_id=cart.id).delete()
            db.session.commit()
        
        response = self.client.post('/api/checkout/process-payment', headers=self.headers, json={
            'payment': {
                'card_number': '4111111111111111',
                'cardholder_name': 'John Doe',
                'expiry_month': 12,
                'expiry_year': datetime.now().year + 1,
                'cvv': '123'
            },
            'shipping_address': {
                'full_name': 'John Doe',
                'street': '123 Main St',
                'city': 'New York',
                'state': 'NY',
                'zip': '10001',
                'country': 'US'
            }
        })
        self.assertEqual(response.status_code, 400)
    
    def test_process_payment_valid(self):
        """Test POST /api/checkout/process-payment with valid data"""
        # Add items
        self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product1.id,
            'quantity': 2
        })
        
        # Ensure cart exists
        cart = Cart.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(cart)
        self.assertGreater(cart.items.count(), 0)
        
        response = self.client.post('/api/checkout/process-payment', headers=self.headers, json={
            'payment': {
                'card_number': '4111111111111111',
                'cardholder_name': 'John Doe',
                'expiry_month': 12,
                'expiry_year': datetime.now().year + 1,
                'cvv': '123'
            },
            'shipping_address': {
                'full_name': 'John Doe',
                'street': '123 Main St',
                'city': 'New York',
                'state': 'NY',
                'zip': '10001',
                'country': 'US'
            }
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('order', response.json)
        self.assertIn('transaction_id', response.json)
    
    def test_process_payment_invalid_card(self):
        """Test POST /api/checkout/process-payment with invalid card"""
        self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product1.id,
            'quantity': 1
        })
        
        future_year = datetime.now().year + 1
        response = self.client.post('/api/checkout/process-payment', headers=self.headers, json={
            'payment': {
                'card_number': '4111111111111112',  # Invalid Luhn
                'cardholder_name': 'John Doe',
                'expiry_month': 12,
                'expiry_year': future_year,
                'cvv': '123'
            },
            'shipping_address': {
                'full_name': 'John Doe',
                'street': '123 Main St',
                'city': 'New York',
                'state': 'NY',
                'zip': '10001',
                'country': 'US'
            }
        })
        self.assertEqual(response.status_code, 400)
    
    def test_process_payment_expired_card(self):
        """Test POST /api/checkout/process-payment with expired card"""
        self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product1.id,
            'quantity': 1
        })
        
        response = self.client.post('/api/checkout/process-payment', headers=self.headers, json={
            'payment': {
                'card_number': '4111111111111111',
                'cardholder_name': 'John Doe',
                'expiry_month': 1,
                'expiry_year': 2020,  # Expired
                'cvv': '123'
            },
            'shipping_address': {
                'full_name': 'John Doe',
                'street': '123 Main St',
                'city': 'New York',
                'state': 'NY',
                'zip': '10001',
                'country': 'US'
            }
        })
        self.assertEqual(response.status_code, 400)
    
    def test_process_payment_with_discount(self):
        """Test POST /api/checkout/process-payment with discount applied"""
        # Add items and apply discount
        self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product1.id,
            'quantity': 2
        })
        discount_response = self.client.post('/api/cart/apply-discount', headers=self.headers, json={
            'discount_code': 'SAVE10'
        })
        self.assertEqual(discount_response.status_code, 200)
        
        # Verify discount is applied
        cart = Cart.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(cart.discount_code)
        
        # Use future year for expiry
        future_year = datetime.now().year + 1
        
        response = self.client.post('/api/checkout/process-payment', headers=self.headers, json={
            'payment': {
                'card_number': '4111111111111111',
                'cardholder_name': 'John Doe',
                'expiry_month': 12,
                'expiry_year': future_year,
                'cvv': '123'
            },
            'shipping_address': {
                'full_name': 'John Doe',
                'street': '123 Main St',
                'city': 'New York',
                'state': 'NY',
                'zip': '10001',
                'country': 'US'
            }
        })
        self.assertEqual(response.status_code, 200)
        order = response.json['order']
        # With discount, total should be less than subtotal (after tax and shipping)
        self.assertGreater(float(order['discount_amount']), 0)


class TestOrdersRoutes(EcommerceRoutesCoverageTestCase):
    """Test orders routes for coverage"""
    
    def test_get_orders_empty(self):
        """Test GET /api/orders when user has no orders"""
        response = self.client.get('/api/orders', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['orders']), 0)
    
    def test_get_orders_with_orders(self):
        """Test GET /api/orders with existing orders"""
        # Create an order with shipping address
        order = Order(
            order_number='ORD-20260122-0001',
            user_id=self.user.id,
            subtotal=Decimal('59.98'),
            tax=Decimal('4.80'),
            shipping=Decimal('5.00'),
            total=Decimal('69.78'),
            status='confirmed',
            payment_status='paid',
            transaction_id='TXN-12345',
            shipping_address={'full_name': 'John Doe', 'street': '123 Main St', 'city': 'NY', 'state': 'NY', 'zip': '10001', 'country': 'US'}
        )
        db.session.add(order)
        db.session.commit()
        
        response = self.client.get('/api/orders', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['orders']), 1)
    
    def test_get_order_by_id(self):
        """Test GET /api/orders/<id>"""
        # Create an order with shipping address
        order = Order(
            order_number='ORD-20260122-0001',
            user_id=self.user.id,
            subtotal=Decimal('59.98'),
            tax=Decimal('4.80'),
            shipping=Decimal('5.00'),
            total=Decimal('69.78'),
            status='confirmed',
            payment_status='paid',
            transaction_id='TXN-12345',
            shipping_address={'full_name': 'John Doe', 'street': '123 Main St', 'city': 'NY', 'state': 'NY', 'zip': '10001', 'country': 'US'}
        )
        db.session.add(order)
        db.session.commit()
        
        response = self.client.get(f'/api/orders/{order.id}', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['order']['id'], order.id)
    
    def test_get_nonexistent_order(self):
        """Test GET /api/orders/99999"""
        response = self.client.get('/api/orders/99999', headers=self.headers)
        self.assertEqual(response.status_code, 404)
    
    def test_get_other_user_order(self):
        """Test GET /api/orders/<id> for another user's order"""
        # Create another user and order
        other_user = User(
            username='otheruser',
            email='other@example.com',
            role=User.ROLE_CUSTOMER
        )
        other_user.set_password('password123')
        db.session.add(other_user)
        
        order = Order(
            order_number='ORD-20260122-0002',
            user_id=other_user.id,
            subtotal=Decimal('59.98'),
            tax=Decimal('4.80'),
            shipping=Decimal('5.00'),
            total=Decimal('69.78'),
            status='confirmed',
            payment_status='paid',
            transaction_id='TXN-12346',
            shipping_address={'full_name': 'Other User', 'street': '456 St', 'city': 'LA', 'state': 'CA', 'zip': '90001', 'country': 'US'}
        )
        db.session.add(order)
        db.session.commit()
        
        response = self.client.get(f'/api/orders/{order.id}', headers=self.headers)
        self.assertEqual(response.status_code, 403)


class TestCartHelperFunctions(EcommerceRoutesCoverageTestCase):
    """Test helper functions in cart routes"""
    
    def test_get_or_create_cart_creates_new(self):
        """Test get_or_create_cart creates new cart"""
        from app.cart.routes import get_or_create_cart
        
        # Delete any existing cart
        Cart.query.filter_by(user_id=self.user.id).delete()
        db.session.commit()
        
        cart = get_or_create_cart(self.user.id)
        self.assertIsNotNone(cart)
        self.assertEqual(cart.user_id, self.user.id)
    
    def test_get_or_create_cart_returns_existing(self):
        """Test get_or_create_cart returns existing cart"""
        from app.cart.routes import get_or_create_cart
        
        # Create cart first
        existing_cart = Cart(user_id=self.user.id)
        db.session.add(existing_cart)
        db.session.commit()
        
        cart = get_or_create_cart(self.user.id)
        self.assertEqual(cart.id, existing_cart.id)


class TestCheckoutHelperFunctions(EcommerceRoutesCoverageTestCase):
    """Test helper functions in checkout routes"""
    
    def test_validate_card_number_valid(self):
        """Test validate_card_number with valid card"""
        from app.checkout.routes import validate_card_number
        self.assertTrue(validate_card_number('4111111111111111'))
    
    def test_validate_card_number_invalid(self):
        """Test validate_card_number with invalid card"""
        from app.checkout.routes import validate_card_number
        self.assertFalse(validate_card_number('4111111111111112'))
    
    def test_validate_card_expiry_valid(self):
        """Test validate_card_expiry with valid expiry"""
        from app.checkout.routes import validate_card_expiry
        future_year = datetime.now().year + 1
        self.assertTrue(validate_card_expiry(12, future_year))
    
    def test_validate_card_expiry_expired(self):
        """Test validate_card_expiry with expired card"""
        from app.checkout.routes import validate_card_expiry
        self.assertFalse(validate_card_expiry(1, 2020))
    
    def test_validate_card_expiry_invalid_month(self):
        """Test validate_card_expiry with invalid month"""
        from app.checkout.routes import validate_card_expiry
        self.assertFalse(validate_card_expiry(13, 2025))
        self.assertFalse(validate_card_expiry(0, 2025))
    
    def test_process_payment_mock_success(self):
        """Test process_payment_mock with valid payment"""
        from app.checkout.routes import process_payment_mock
        
        future_year = datetime.now().year + 1
        result = process_payment_mock({
            'card_number': '4111111111111111',
            'expiry_month': 12,
            'expiry_year': future_year,
            'cvv': '123'
        }, Decimal('100.00'))
        
        self.assertTrue(result['success'])
        self.assertIn('transaction_id', result)
    
    def test_process_payment_mock_invalid_card(self):
        """Test process_payment_mock with invalid card"""
        from app.checkout.routes import process_payment_mock
        
        future_year = datetime.now().year + 1
        result = process_payment_mock({
            'card_number': '4111111111111112',
            'expiry_month': 12,
            'expiry_year': future_year,
            'cvv': '123'
        }, Decimal('100.00'))
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)
    
    def test_process_payment_mock_expired_card(self):
        """Test process_payment_mock with expired card"""
        from app.checkout.routes import process_payment_mock
        
        result = process_payment_mock({
            'card_number': '4111111111111111',
            'expiry_month': 1,
            'expiry_year': 2020,
            'cvv': '123'
        }, Decimal('100.00'))
        
        self.assertFalse(result['success'])
        self.assertIn('expired', result['error'].lower())
    
    def test_process_payment_mock_invalid_cvv(self):
        """Test process_payment_mock with invalid CVV"""
        from app.checkout.routes import process_payment_mock
        
        future_year = datetime.now().year + 1
        result = process_payment_mock({
            'card_number': '4111111111111111',
            'expiry_month': 12,
            'expiry_year': future_year,
            'cvv': '12'  # Too short
        }, Decimal('100.00'))
        
        self.assertFalse(result['success'])
        self.assertIn('cvv', result['error'].lower())


class TestModelMethods(EcommerceRoutesCoverageTestCase):
    """Test model methods for coverage"""
    
    def test_cart_calculate_subtotal(self):
        """Test Cart.calculate_subtotal()"""
        cart = Cart(user_id=self.user.id)
        db.session.add(cart)
        db.session.flush()  # Get cart.id before creating items
        cart_item1 = CartItem(cart_id=cart.id, product_id=self.product1.id, quantity=2)
        cart_item2 = CartItem(cart_id=cart.id, product_id=self.product2.id, quantity=1)
        db.session.add_all([cart_item1, cart_item2])
        db.session.commit()
        
        subtotal = cart.calculate_subtotal()
        expected = Decimal('29.99') * 2 + Decimal('49.99') * 1
        self.assertEqual(subtotal, expected)
    
    def test_cart_calculate_total_with_discount(self):
        """Test Cart.calculate_total() with discount"""
        cart = Cart(user_id=self.user.id, discount_code_id=self.discount1.id)
        db.session.add(cart)
        db.session.flush()  # Get cart.id
        cart_item = CartItem(cart_id=cart.id, product_id=self.product1.id, quantity=2)
        db.session.add(cart_item)
        db.session.commit()
        
        total = cart.calculate_total()
        subtotal = cart.calculate_subtotal()
        discount = self.discount1.calculate_discount(subtotal)
        expected = max(subtotal - discount, 0)
        self.assertEqual(total, expected)
    
    def test_cart_to_dict(self):
        """Test Cart.to_dict()"""
        cart = Cart(user_id=self.user.id)
        db.session.add(cart)
        db.session.flush()  # Get cart.id
        cart_item = CartItem(cart_id=cart.id, product_id=self.product1.id, quantity=2)
        db.session.add(cart_item)
        db.session.commit()
        
        cart_dict = cart.to_dict()
        self.assertIn('id', cart_dict)
        self.assertIn('items', cart_dict)
        self.assertIn('subtotal', cart_dict)
        self.assertIn('total', cart_dict)
    
    def test_cart_item_subtotal(self):
        """Test CartItem.subtotal property"""
        cart = Cart(user_id=self.user.id)
        db.session.add(cart)
        db.session.flush()  # Get cart.id
        cart_item = CartItem(cart_id=cart.id, product_id=self.product1.id, quantity=3)
        db.session.add(cart_item)
        db.session.commit()
        
        expected_subtotal = Decimal('29.99') * 3
        self.assertEqual(cart_item.subtotal, expected_subtotal)
    
    def test_cart_item_to_dict(self):
        """Test CartItem.to_dict()"""
        cart = Cart(user_id=self.user.id)
        db.session.add(cart)
        db.session.flush()  # Get cart.id
        cart_item = CartItem(cart_id=cart.id, product_id=self.product1.id, quantity=2)
        db.session.add(cart_item)
        db.session.commit()
        
        item_dict = cart_item.to_dict()
        self.assertIn('id', item_dict)
        self.assertIn('product', item_dict)
        self.assertIn('quantity', item_dict)
        self.assertIn('subtotal', item_dict)
    
    def test_discount_code_is_valid(self):
        """Test DiscountCode.is_valid()"""
        # Valid code
        self.assertTrue(self.discount1.is_valid())
        
        # Expired code
        self.assertFalse(self.discount3.is_valid())
        
        # Inactive code
        inactive = DiscountCode(
            code='INACTIVE',
            discount_type='percentage',
            discount_percent=Decimal('10.00'),
            is_active=False
        )
        self.assertFalse(inactive.is_valid())
    
    def test_discount_code_calculate_discount_percentage(self):
        """Test DiscountCode.calculate_discount() for percentage"""
        amount = Decimal('100.00')
        discount = self.discount1.calculate_discount(amount)
        expected = amount * (Decimal('10.00') / 100)
        self.assertEqual(discount, expected)
    
    def test_discount_code_calculate_discount_fixed(self):
        """Test DiscountCode.calculate_discount() for fixed amount"""
        amount = Decimal('100.00')
        discount = self.discount2.calculate_discount(amount)
        self.assertEqual(discount, Decimal('5.00'))
    
    def test_discount_code_calculate_discount_below_minimum(self):
        """Test DiscountCode.calculate_discount() below minimum purchase"""
        code = DiscountCode(
            code='MIN50',
            discount_type='percentage',
            discount_percent=Decimal('10.00'),
            min_purchase=Decimal('50.00')
        )
        discount = code.calculate_discount(Decimal('30.00'))
        self.assertEqual(discount, Decimal('0.00'))
    
    def test_discount_code_calculate_discount_max_limit(self):
        """Test DiscountCode.calculate_discount() with max discount limit"""
        code = DiscountCode(
            code='MAX50',
            discount_type='percentage',
            discount_percent=Decimal('20.00'),
            max_discount=Decimal('50.00'),
            min_purchase=Decimal('0.00'),
            is_active=True
        )
        # 20% of 1000 = 200, but should cap at 50
        discount = code.calculate_discount(Decimal('1000.00'))
        self.assertEqual(discount, Decimal('50.00'))
    
    def test_order_generate_order_number(self):
        """Test Order.generate_order_number()"""
        order_number = Order.generate_order_number()
        self.assertIsInstance(order_number, str)
        self.assertTrue(order_number.startswith('ORD-'))
    
    def test_order_to_dict(self):
        """Test Order.to_dict()"""
        order = Order(
            order_number='ORD-20260122-0001',
            user_id=self.user.id,
            subtotal=Decimal('59.98'),
            tax=Decimal('4.80'),
            shipping=Decimal('5.00'),
            total=Decimal('69.78'),
            status='confirmed',
            payment_status='paid',
            transaction_id='TXN-12345',
            shipping_address={'full_name': 'John Doe'}
        )
        db.session.add(order)
        db.session.commit()
        
        order_dict = order.to_dict()
        self.assertIn('id', order_dict)
        self.assertIn('order_number', order_dict)
        self.assertIn('items', order_dict)
        self.assertIn('total', order_dict)
    
    def test_product_to_dict(self):
        """Test Product.to_dict()"""
        product_dict = self.product1.to_dict()
        self.assertIn('id', product_dict)
        self.assertIn('title', product_dict)
        self.assertIn('price', product_dict)
        self.assertIn('stock', product_dict)


class TestSchemaValidation(EcommerceRoutesCoverageTestCase):
    """Test schema validation for coverage"""
    
    def test_add_to_cart_invalid_schema(self):
        """Test POST /api/cart/items with invalid schema"""
        response = self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': 'invalid',  # Should be integer
            'quantity': 1
        })
        self.assertEqual(response.status_code, 400)
    
    def test_update_cart_item_invalid_schema(self):
        """Test PUT /api/cart/items/<id> with invalid schema"""
        add_response = self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product1.id,
            'quantity': 2
        })
        item_id = add_response.json['cart']['items'][0]['id']
        
        response = self.client.put(f'/api/cart/items/{item_id}', headers=self.headers, json={
            'quantity': 'invalid'  # Should be integer
        })
        self.assertEqual(response.status_code, 400)
    
    def test_checkout_invalid_payment_schema(self):
        """Test POST /api/checkout/process-payment with invalid payment schema"""
        self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product1.id,
            'quantity': 1
        })
        
        response = self.client.post('/api/checkout/process-payment', headers=self.headers, json={
            'payment': {
                'card_number': '4111111111111111',
                # Missing required fields
            },
            'shipping_address': {
                'full_name': 'John Doe',
                'street': '123 Main St',
                'city': 'New York',
                'state': 'NY',
                'zip': '10001',
                'country': 'US'
            }
        })
        self.assertEqual(response.status_code, 400)
    
    def test_checkout_invalid_shipping_schema(self):
        """Test POST /api/checkout/process-payment with invalid shipping schema"""
        self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product1.id,
            'quantity': 1
        })
        
        response = self.client.post('/api/checkout/process-payment', headers=self.headers, json={
            'payment': {
                'card_number': '4111111111111111',
                'cardholder_name': 'John Doe',
                'expiry_month': 12,
                'expiry_year': datetime.now().year + 1,
                'cvv': '123'
            },
            'shipping_address': {
                # Missing required fields
            }
        })
        self.assertEqual(response.status_code, 400)


class TestEdgeCases(EcommerceRoutesCoverageTestCase):
    """Test edge cases for coverage"""
    
    def test_cart_no_items_subtotal(self):
        """Test Cart.calculate_subtotal() with no items"""
        cart = Cart(user_id=self.user.id)
        db.session.add(cart)
        db.session.commit()
        
        subtotal = cart.calculate_subtotal()
        self.assertEqual(subtotal, Decimal('0.00'))
    
    def test_discount_code_calculate_exceeds_amount(self):
        """Test DiscountCode.calculate_discount() when discount exceeds amount"""
        code = DiscountCode(
            code='FIXED100',
            discount_type='fixed',
            discount_amount=Decimal('100.00'),
            min_purchase=Decimal('0.00'),
            is_active=True
        )
        # Discount is $100 but amount is only $50
        discount = code.calculate_discount(Decimal('50.00'))
        self.assertEqual(discount, Decimal('50.00'))  # Should cap at amount
    
    def test_process_payment_cart_not_found(self):
        """Test POST /api/checkout/process-payment when cart doesn't exist"""
        # Delete any existing cart
        Cart.query.filter_by(user_id=self.user.id).delete()
        db.session.commit()
        
        response = self.client.post('/api/checkout/process-payment', headers=self.headers, json={
            'payment': {
                'card_number': '4111111111111111',
                'cardholder_name': 'John Doe',
                'expiry_month': 12,
                'expiry_year': datetime.now().year + 1,
                'cvv': '123'
            },
            'shipping_address': {
                'full_name': 'John Doe',
                'street': '123 Main St',
                'city': 'New York',
                'state': 'NY',
                'zip': '10001',
                'country': 'US'
            }
        })
        self.assertEqual(response.status_code, 404)
    
    def test_process_payment_insufficient_stock(self):
        """Test POST /api/checkout/process-payment with insufficient stock"""
        # Add more items than available stock
        self.client.post('/api/cart/items', headers=self.headers, json={
            'product_id': self.product1.id,
            'quantity': 200  # More than available stock (100)
        })
        
        response = self.client.post('/api/checkout/process-payment', headers=self.headers, json={
            'payment': {
                'card_number': '4111111111111111',
                'cardholder_name': 'John Doe',
                'expiry_month': 12,
                'expiry_year': datetime.now().year + 1,
                'cvv': '123'
            },
            'shipping_address': {
                'full_name': 'John Doe',
                'street': '123 Main St',
                'city': 'New York',
                'state': 'NY',
                'zip': '10001',
                'country': 'US'
            }
        })
        # Should fail during checkout due to stock check
        self.assertIn(response.status_code, [400, 500])


if __name__ == '__main__':
    unittest.main()
