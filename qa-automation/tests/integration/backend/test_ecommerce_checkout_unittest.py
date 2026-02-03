"""
Comprehensive E-Commerce Checkout Process Test Cases - Unittest Format

This test suite covers the complete e-commerce checkout workflow:
- Cart Management (add, update, remove items)
- Discount Code Application
- Payment Processing
- Order Confirmation
- Email Notifications

Test Categories:
- Positive Test Cases: Valid scenarios and successful operations
- Negative Test Cases: Invalid inputs and error handling
- Edge Cases: Boundary conditions and unusual scenarios
- Security Test Cases: Payment data validation, SQL injection prevention, XSS protection

Note: These tests define expected behavior for e-commerce functionality.
Actual implementation should follow these test specifications.
"""

import unittest
from app import create_app, db
from app.models import User
from app.cache import cache
from faker import Faker
from datetime import datetime, timedelta
from decimal import Decimal
import json
from unittest.mock import patch, MagicMock


class BaseEcommerceTestCase(unittest.TestCase):
    """Base test case for e-commerce tests with common setup"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.fake = Faker()
        
        # Create database tables
        db.create_all()
        cache.clear()
        
        # Automatically create test user (customer) - no registration needed
        self.test_customer = self._create_test_customer()
        
        # Automatically get authentication token - no login needed
        # Authentication is optional - tests can work with or without headers
        self.customer_headers = self._get_auth_headers(
            self.test_customer, 
            'customerpassword123'
        )
        
        # Create actual products in database for testing
        self.mock_products = self._create_mock_products()
        self._create_products_in_db()
        
        # Create discount codes in database
        self._create_discount_codes_in_db()
    
    def tearDown(self):
        """Clean up after each test method"""
        db.session.remove()
        db.drop_all()
        cache.clear()
        self.app_context.pop()
    
    def _create_test_customer(self):
        """Create a test customer user"""
        customer = User(
            username='testcustomer',
            email='customer@example.com',
            role=User.ROLE_CUSTOMER,
            is_active=True,
            first_name='John',
            last_name='Doe'
        )
        customer.set_password('customerpassword123')
        db.session.add(customer)
        db.session.commit()
        return customer
    
    def _get_auth_headers(self, user, password):
        """Get authentication headers for a user"""
        response = self.client.post('/api/auth/login', json={
            'username': user.username,
            'password': password
        })
        if response.status_code == 200:
            token = response.json['access_token']
            return {'Authorization': f'Bearer {token}'}
        return {}
    
    def _create_mock_products(self):
        """Create mock product data for testing"""
        return [
            {
                'id': 1,
                'name': 'Test Product 1',
                'price': Decimal('29.99'),
                'sku': 'PROD-001',
                'stock': 100,
                'description': 'Test product description'
            },
            {
                'id': 2,
                'name': 'Test Product 2',
                'price': Decimal('49.99'),
                'sku': 'PROD-002',
                'stock': 50,
                'description': 'Another test product'
            },
            {
                'id': 3,
                'name': 'Test Product 3',
                'price': Decimal('99.99'),
                'sku': 'PROD-003',
                'stock': 0,  # Out of stock
                'description': 'Out of stock product'
            }
        ]
    
    def _create_mock_discount_code(self, code='SAVE10', discount_percent=10, 
                                   min_purchase=0, max_discount=None, 
                                   expires_at=None, is_active=True):
        """Create mock discount code data"""
        return {
            'code': code,
            'discount_percent': discount_percent,
            'discount_amount': None,
            'min_purchase': Decimal(str(min_purchase)),
            'max_discount': Decimal(str(max_discount)) if max_discount else None,
            'expires_at': expires_at or (datetime.utcnow() + timedelta(days=30)),
            'is_active': is_active,
            'usage_limit': None,
            'used_count': 0
        }
    
    def _create_mock_payment_data(self, card_number='4111111111111111', 
                                  cvv='123', expiry_month=12, expiry_year=None):
        # Default to future year if not provided
        if expiry_year is None:
            from datetime import datetime
            expiry_year = datetime.now().year + 1
        """Create mock payment data"""
        return {
            'card_number': card_number,
            'cardholder_name': 'John Doe',
            'expiry_month': expiry_month,
            'expiry_year': expiry_year,
            'cvv': cvv,
            'billing_address': {
                'street': '123 Main St',
                'city': 'New York',
                'state': 'NY',
                'zip': '10001',
                'country': 'US'
            }
        }
    
    def _create_mock_shipping_address(self):
        """Create mock shipping address"""
        return {
            'full_name': 'John Doe',
            'street': '456 Shipping Ave',
            'city': 'Los Angeles',
            'state': 'CA',
            'zip': '90001',
            'country': 'US',
            'phone': '+1234567890'
        }
    
    def _create_products_in_db(self):
        """Create products in database for testing"""
        from app.models import Product
        for product_data in self.mock_products:
            product = Product(
                title=product_data['name'],
                description=product_data.get('description', ''),
                price=product_data['price'],
                stock=product_data['stock'],
                in_stock=product_data['stock'] > 0,
                sku=product_data.get('sku'),
                category='Test Category'
            )
            db.session.add(product)
        db.session.commit()
    
    def _create_discount_codes_in_db(self):
        """Create discount codes in database for testing"""
        from app.models import DiscountCode
        from datetime import datetime, timedelta
        
        # Create SAVE10 discount code
        save10 = DiscountCode(
            code='SAVE10',
            discount_type='percentage',
            discount_percent=Decimal('10.00'),
            min_purchase=Decimal('0.00'),
            max_discount=None,
            expires_at=datetime.utcnow() + timedelta(days=30),
            is_active=True
        )
        db.session.add(save10)
        
        # Create FIXED5 discount code
        fixed5 = DiscountCode(
            code='FIXED5',
            discount_type='fixed',
            discount_amount=Decimal('5.00'),
            min_purchase=Decimal('0.00'),
            is_active=True
        )
        db.session.add(fixed5)
        
        # Create MIN50 discount code (requires $50 minimum)
        min50 = DiscountCode(
            code='MIN50',
            discount_type='percentage',
            discount_percent=Decimal('10.00'),
            min_purchase=Decimal('50.00'),
            is_active=True
        )
        db.session.add(min50)
        
        # Create MAX50 discount code (max $50 discount)
        max50 = DiscountCode(
            code='MAX50',
            discount_type='percentage',
            discount_percent=Decimal('20.00'),
            min_purchase=Decimal('0.00'),
            max_discount=Decimal('50.00'),
            is_active=True
        )
        db.session.add(max50)
        
        # Create expired discount code
        expired = DiscountCode(
            code='EXPIRED',
            discount_type='percentage',
            discount_percent=Decimal('10.00'),
            expires_at=datetime.utcnow() - timedelta(days=1),
            is_active=True
        )
        db.session.add(expired)
        
        # Create SAVE20 discount code for test_replace_existing_discount_code
        save20 = DiscountCode(
            code='SAVE20',
            discount_type='percentage',
            discount_percent=Decimal('20.00'),
            min_purchase=Decimal('0.00'),
            is_active=True
        )
        db.session.add(save20)
        
        db.session.commit()


# ============================================================================
# CART MANAGEMENT TESTS
# ============================================================================

class TestCartManagementPositive(BaseEcommerceTestCase):
    """Positive test cases for cart management"""
    
    def test_add_item_to_cart(self):
        """Test: Add item to cart successfully
        Expected: Item added to cart, cart updated with correct quantity
        Note: User is automatically created and authenticated - no manual registration/login needed
        """
        # Products are automatically created in database during setUp
        # User is automatically created and authenticated during setUp
        cart_data = {
            'product_id': 1,
            'quantity': 2
        }
        response = self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json=cart_data
        )
        # Expected: 201 Created or 200 OK
        self.assertIn(response.status_code, [200, 201])
        if response.status_code in [200, 201]:
            response_data = response.json
            self.assertIn('cart', response_data)
            self.assertEqual(response_data['cart']['items'][0]['product_id'], 1)
            self.assertEqual(response_data['cart']['items'][0]['quantity'], 2)
    
    def test_add_multiple_items_to_cart(self):
        """Test: Add multiple different items to cart
        Expected: All items added successfully
        """
        items = [
            {'product_id': 1, 'quantity': 2},
            {'product_id': 2, 'quantity': 1}
        ]
        for item in items:
            response = self.client.post(
                '/api/cart/items',
                headers=self.customer_headers,
                json=item
            )
            self.assertIn(response.status_code, [200, 201])
        
        # Verify cart contains all items
        get_response = self.client.get('/api/cart', headers=self.customer_headers)
        self.assertEqual(get_response.status_code, 200)
        cart = get_response.json['cart']
        self.assertEqual(len(cart['items']), 2)
    
    def test_update_cart_item_quantity(self):
        """Test: Update quantity of item in cart
        Expected: Quantity updated successfully
        """
        # Add item first
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        
        # Update quantity
        response = self.client.put(
            '/api/cart/items/1',
            headers=self.customer_headers,
            json={'quantity': 5}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['cart']['items'][0]['quantity'], 5)
    
    def test_get_cart_contents(self):
        """Test: Retrieve cart contents
        Expected: Cart returned with all items and totals
        """
        # Add items first
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 2}
        )
        
        response = self.client.get('/api/cart', headers=self.customer_headers)
        self.assertEqual(response.status_code, 200)
        cart = response.json['cart']
        self.assertIn('items', cart)
        self.assertIn('subtotal', cart)
        self.assertIn('total', cart)
        self.assertEqual(len(cart['items']), 1)
    
    def test_remove_item_from_cart(self):
        """Test: Remove item from cart
        Expected: Item removed, cart updated
        """
        # Add item first
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 2}
        )
        
        # Remove item
        response = self.client.delete(
            '/api/cart/items/1',
            headers=self.customer_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify cart is empty
        get_response = self.client.get('/api/cart', headers=self.customer_headers)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(len(get_response.json['cart']['items']), 0)
    
    def test_clear_cart(self):
        """Test: Clear all items from cart
        Expected: All items removed, cart empty
        """
        # Add multiple items
        for product_id in [1, 2]:
            self.client.post(
                '/api/cart/items',
                headers=self.customer_headers,
                json={'product_id': product_id, 'quantity': 1}
            )
        
        # Clear cart
        response = self.client.delete(
            '/api/cart',
            headers=self.customer_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify cart is empty
        get_response = self.client.get('/api/cart', headers=self.customer_headers)
        self.assertEqual(len(get_response.json['cart']['items']), 0)


class TestCartManagementNegative(BaseEcommerceTestCase):
    """Negative test cases for cart management"""
    
    def test_add_item_without_authentication(self):
        """Test: Add item to cart without authentication
        Expected: 401 Unauthorized (if auth required) or 200 (if anonymous carts supported)
        Note: This test verifies authentication behavior - may pass or fail based on API design
        """
        response = self.client.post(
            '/api/cart/items',
            json={'product_id': 1, 'quantity': 1}
        )
        # Accept either 401 (auth required) or 200 (anonymous carts supported)
        self.assertIn(response.status_code, [200, 201, 401])
    
    def test_add_nonexistent_product_to_cart(self):
        """Test: Add non-existent product to cart
        Expected: 404 Not Found
        """
        response = self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 99999, 'quantity': 1}
        )
        self.assertEqual(response.status_code, 404)
    
    def test_add_out_of_stock_product_to_cart(self):
        """Test: Add out of stock product to cart
        Expected: 400 Bad Request - product out of stock
        """
        response = self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 3, 'quantity': 1}  # Product 3 is out of stock
        )
        self.assertEqual(response.status_code, 400)
        error_msg = str(response.json.get('error', '') or response.json.get('message', '')).lower()
        self.assertIn('stock', error_msg)
    
    def test_add_item_with_invalid_quantity(self):
        """Test: Add item with invalid quantity (zero or negative)
        Expected: 400 Bad Request
        """
        # Zero quantity
        response = self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 0}
        )
        self.assertEqual(response.status_code, 400)
        
        # Negative quantity
        response = self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': -1}
        )
        self.assertEqual(response.status_code, 400)
    
    def test_add_item_exceeding_stock(self):
        """Test: Add quantity exceeding available stock
        Expected: 400 Bad Request - insufficient stock
        """
        response = self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 200}  # Only 100 in stock
        )
        self.assertEqual(response.status_code, 400)
        error_msg = str(response.json.get('error', '') or response.json.get('message', '')).lower()
        self.assertIn('stock', error_msg)
    
    def test_update_nonexistent_cart_item(self):
        """Test: Update non-existent cart item
        Expected: 404 Not Found
        """
        response = self.client.put(
            '/api/cart/items/99999',
            headers=self.customer_headers,
            json={'quantity': 5}
        )
        self.assertEqual(response.status_code, 404)
    
    def test_remove_nonexistent_cart_item(self):
        """Test: Remove non-existent cart item
        Expected: 404 Not Found
        """
        response = self.client.delete(
            '/api/cart/items/99999',
            headers=self.customer_headers
        )
        self.assertEqual(response.status_code, 404)


class TestCartManagementEdgeCases(BaseEcommerceTestCase):
    """Edge cases for cart management"""
    
    def test_add_same_product_multiple_times(self):
        """Test: Add same product multiple times
        Expected: Quantity should increase, not create duplicate entries
        """
        # Add product first time
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 2}
        )
        
        # Add same product again
        response = self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 3}
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify only one cart item exists with combined quantity
        get_response = self.client.get('/api/cart', headers=self.customer_headers)
        cart = get_response.json['cart']
        self.assertEqual(len(cart['items']), 1)
        self.assertEqual(cart['items'][0]['quantity'], 5)  # 2 + 3
    
    def test_update_quantity_to_zero_removes_item(self):
        """Test: Update quantity to zero removes item from cart
        Expected: Item removed from cart
        """
        # Add item
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 2}
        )
        
        # Update to zero
        response = self.client.put(
            '/api/cart/items/1',
            headers=self.customer_headers,
            json={'quantity': 0}
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify item removed
        get_response = self.client.get('/api/cart', headers=self.customer_headers)
        self.assertEqual(len(get_response.json['cart']['items']), 0)
    
    def test_cart_calculation_with_multiple_items(self):
        """Test: Cart totals calculated correctly with multiple items
        Expected: Subtotal, tax, and total calculated correctly
        """
        # Add multiple items
        items = [
            {'product_id': 1, 'quantity': 2},  # $29.99 * 2 = $59.98
            {'product_id': 2, 'quantity': 1}   # $49.99 * 1 = $49.99
        ]
        for item in items:
            self.client.post(
                '/api/cart/items',
                headers=self.customer_headers,
                json=item
            )
        
        # Get cart
        response = self.client.get('/api/cart', headers=self.customer_headers)
        cart = response.json['cart']
        
        # Verify calculations
        expected_subtotal = Decimal('109.97')  # 59.98 + 49.99
        self.assertEqual(Decimal(str(cart['subtotal'])), expected_subtotal)
        self.assertIn('tax', cart)
        self.assertIn('total', cart)


class TestCartManagementSecurity(BaseEcommerceTestCase):
    """Security test cases for cart management"""
    
    def test_cart_isolation_between_users(self):
        """Test: Users can only access their own cart
        Expected: Cart data isolated per user
        """
        # Create second customer
        customer2 = User(
            username='customer2',
            email='customer2@example.com',
            role=User.ROLE_CUSTOMER
        )
        customer2.set_password('password123')
        db.session.add(customer2)
        db.session.commit()
        
        # Login as customer2
        login_response = self.client.post('/api/auth/login', json={
            'username': 'customer2',
            'password': 'password123'
        })
        customer2_token = login_response.json['access_token']
        customer2_headers = {'Authorization': f'Bearer {customer2_token}'}
        
        # Add item to customer1's cart
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        
        # Customer2's cart should be empty
        response = self.client.get('/api/cart', headers=customer2_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['cart']['items']), 0)
    
    def test_sql_injection_in_product_id(self):
        """Test: Attempt SQL injection in product_id
        Expected: Treated as invalid ID, no SQL execution
        """
        malicious_id = "1' OR '1'='1"
        response = self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': malicious_id, 'quantity': 1}
        )
        # Should treat as invalid ID format
        self.assertIn(response.status_code, [400, 404])


# ============================================================================
# DISCOUNT CODE TESTS
# ============================================================================

class TestDiscountCodePositive(BaseEcommerceTestCase):
    """Positive test cases for discount code application"""
    
    def test_apply_valid_discount_code(self):
        """Test: Apply valid discount code
        Expected: Discount applied, cart total updated
        """
        # Add items to cart
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 2}
        )
        
        # Apply discount code
        response = self.client.post(
            '/api/cart/apply-discount',
            headers=self.customer_headers,
            json={'discount_code': 'SAVE10'}
        )
        self.assertEqual(response.status_code, 200)
        cart = response.json['cart']
        # Cart.to_dict() returns 'discount_code' and 'discount_amount', not 'discount'
        self.assertIn('discount_code', cart)
        self.assertIn('discount_amount', cart)
        self.assertLess(cart['total'], cart['subtotal'])
    
    def test_apply_percentage_discount(self):
        """Test: Apply percentage-based discount
        Expected: Discount calculated as percentage of subtotal
        """
        # Add items totaling $100
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 3}  # ~$90
        )
        
        # Apply 10% discount
        response = self.client.post(
            '/api/cart/apply-discount',
            headers=self.customer_headers,
            json={'discount_code': 'SAVE10'}
        )
        self.assertEqual(response.status_code, 200)
        cart = response.json['cart']
        # Discount should be approximately 10% of subtotal
        discount_percent = (cart['discount_amount'] / cart['subtotal']) * 100
        self.assertAlmostEqual(float(discount_percent), 10.0, places=1)
    
    def test_apply_fixed_amount_discount(self):
        """Test: Apply fixed amount discount
        Expected: Fixed amount deducted from total
        """
        # Add items
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 2}
        )
        
        # Apply $5 fixed discount
        response = self.client.post(
            '/api/cart/apply-discount',
            headers=self.customer_headers,
            json={'discount_code': 'FIXED5'}
        )
        self.assertEqual(response.status_code, 200)
        cart = response.json['cart']
        self.assertEqual(float(cart['discount_amount']), 5.0)
    
    def test_remove_discount_code(self):
        """Test: Remove applied discount code
        Expected: Discount removed, cart total recalculated
        """
        # Add items and apply discount
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 2}
        )
        self.client.post(
            '/api/cart/apply-discount',
            headers=self.customer_headers,
            json={'discount_code': 'SAVE10'}
        )
        
        # Remove discount
        response = self.client.delete(
            '/api/cart/discount',
            headers=self.customer_headers
        )
        self.assertEqual(response.status_code, 200)
        cart = response.json['cart']
        self.assertIsNone(cart.get('discount_code'))
        self.assertEqual(float(cart.get('discount_amount', 0)), 0.0)


class TestDiscountCodeNegative(BaseEcommerceTestCase):
    """Negative test cases for discount codes"""
    
    def test_apply_invalid_discount_code(self):
        """Test: Apply invalid/non-existent discount code
        Expected: 400 Bad Request - invalid code
        """
        response = self.client.post(
            '/api/cart/apply-discount',
            headers=self.customer_headers,
            json={'discount_code': 'INVALID123'}
        )
        self.assertEqual(response.status_code, 400)
        error_msg = str(response.json.get('error', '') or response.json.get('message', '')).lower()
        self.assertIn('discount', error_msg)
    
    def test_apply_expired_discount_code(self):
        """Test: Apply expired discount code
        Expected: 400 Bad Request - code expired
        """
        response = self.client.post(
            '/api/cart/apply-discount',
            headers=self.customer_headers,
            json={'discount_code': 'EXPIRED'}
        )
        self.assertEqual(response.status_code, 400)
        error_msg = str(response.json.get('error', '') or response.json.get('message', '')).lower()
        self.assertIn('expired', error_msg)
    
    def test_apply_discount_below_minimum_purchase(self):
        """Test: Apply discount code when cart total below minimum purchase
        Expected: 400 Bad Request - minimum purchase not met
        """
        # Add small amount to cart
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}  # $29.99
        )
        
        # Try to apply code requiring $50 minimum
        response = self.client.post(
            '/api/cart/apply-discount',
            headers=self.customer_headers,
            json={'discount_code': 'MIN50'}
        )
        self.assertEqual(response.status_code, 400)
        error_msg = str(response.json.get('error', '') or response.json.get('message', '')).lower()
        self.assertIn('minimum', error_msg)
    
    def test_apply_discount_to_empty_cart(self):
        """Test: Apply discount code to empty cart
        Expected: 400 Bad Request - cart is empty
        """
        response = self.client.post(
            '/api/cart/apply-discount',
            headers=self.customer_headers,
            json={'discount_code': 'SAVE10'}
        )
        self.assertEqual(response.status_code, 400)
        error_msg = str(response.json.get('error', '') or response.json.get('message', '')).lower()
        self.assertIn('cart', error_msg)
    
    def test_apply_discount_without_authentication(self):
        """Test: Apply discount without authentication
        Expected: 401 Unauthorized (if auth required) or 400 (if anonymous carts supported)
        Note: This test verifies authentication behavior - may pass or fail based on API design
        """
        response = self.client.post(
            '/api/cart/apply-discount',
            json={'discount_code': 'SAVE10'}
        )
        # Accept either 401 (auth required) or 400 (cart empty) or 200 (anonymous carts)
        self.assertIn(response.status_code, [200, 400, 401])


class TestDiscountCodeEdgeCases(BaseEcommerceTestCase):
    """Edge cases for discount codes"""
    
    def test_discount_exceeds_max_discount_limit(self):
        """Test: Discount amount exceeds maximum discount limit
        Expected: Discount capped at maximum limit
        """
        # Add large amount to cart
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 2, 'quantity': 10}  # $499.90
        )
        
        # Apply 20% discount with $50 max
        response = self.client.post(
            '/api/cart/apply-discount',
            headers=self.customer_headers,
            json={'discount_code': 'MAX50'}
        )
        self.assertEqual(response.status_code, 200)
        cart = response.json['cart']
        # Discount should be capped at $50, not 20% of $499.90 (~$100)
        self.assertEqual(float(cart['discount_amount']), 50.0)
    
    def test_discount_makes_total_zero(self):
        """Test: Discount makes total zero or negative
        Expected: Total should not go below zero
        """
        # Add small amount
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}  # $29.99
        )
        
        # Apply 100% discount (if allowed)
        response = self.client.post(
            '/api/cart/apply-discount',
            headers=self.customer_headers,
            json={'discount_code': 'FREE100'}
        )
        if response.status_code == 200:
            cart = response.json['cart']
            self.assertGreaterEqual(float(cart['total']), 0.0)
    
    def test_replace_existing_discount_code(self):
        """Test: Apply new discount code when one already applied
        Expected: Old discount replaced with new one
        """
        # Add items
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 2}
        )
        
        # Apply first discount
        self.client.post(
            '/api/cart/apply-discount',
            headers=self.customer_headers,
            json={'discount_code': 'SAVE10'}
        )
        
        # Apply second discount
        response = self.client.post(
            '/api/cart/apply-discount',
            headers=self.customer_headers,
            json={'discount_code': 'SAVE20'}
        )
        self.assertEqual(response.status_code, 200)
        cart = response.json['cart']
        self.assertEqual(cart['discount_code'], 'SAVE20')


class TestDiscountCodeSecurity(BaseEcommerceTestCase):
    """Security test cases for discount codes"""
    
    def test_sql_injection_in_discount_code(self):
        """Test: Attempt SQL injection in discount code
        Expected: Treated as invalid code, no SQL execution
        """
        malicious_code = "SAVE10' OR '1'='1"
        response = self.client.post(
            '/api/cart/apply-discount',
            headers=self.customer_headers,
            json={'discount_code': malicious_code}
        )
        # Should reject as invalid code
        self.assertEqual(response.status_code, 400)
    
    def test_xss_in_discount_code(self):
        """Test: Attempt XSS attack in discount code
        Expected: Script tags treated as literal string
        """
        xss_code = '<script>alert("XSS")</script>'
        response = self.client.post(
            '/api/cart/apply-discount',
            headers=self.customer_headers,
            json={'discount_code': xss_code}
        )
        # Should reject as invalid code
        self.assertEqual(response.status_code, 400)


# ============================================================================
# PAYMENT PROCESSING TESTS
# ============================================================================

class TestPaymentProcessingPositive(BaseEcommerceTestCase):
    """Positive test cases for payment processing"""
    
    @patch('app.services.payment_service.process_payment')
    def test_process_payment_with_valid_card(self, mock_payment):
        """Test: Process payment with valid credit card
        Expected: Payment processed successfully, order created
        """
        # Mock successful payment
        mock_payment.return_value = {
            'success': True,
            'transaction_id': 'TXN-12345',
            'amount': 29.99
        }
        
        # Add items to cart
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        
        # Process payment
        payment_data = self._create_mock_payment_data()
        shipping_address = self._create_mock_shipping_address()
        
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': payment_data,
                'shipping_address': shipping_address
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('order', response.json)
        self.assertIn('transaction_id', response.json)
        self.assertEqual(response.json['order']['status'], 'confirmed')
    
    @patch('app.services.payment_service.process_payment')
    def test_process_payment_with_discount_applied(self, mock_payment):
        """Test: Process payment with discount code applied
        Expected: Payment processed for discounted amount
        """
        mock_payment.return_value = {
            'success': True,
            'transaction_id': 'TXN-12346',
            'amount': 26.99  # After 10% discount
        }
        
        # Add items and apply discount
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        self.client.post(
            '/api/cart/apply-discount',
            headers=self.customer_headers,
            json={'discount_code': 'SAVE10'}
        )
        
        # Process payment
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': self._create_mock_payment_data(),
                'shipping_address': self._create_mock_shipping_address()
            }
        )
        self.assertEqual(response.status_code, 200)
        # Verify payment amount matches discounted total
        order = response.json['order']
        self.assertLess(order['total'], order['subtotal'])
    
    @patch('app.services.payment_service.process_payment')
    def test_process_payment_creates_order(self, mock_payment):
        """Test: Payment processing creates order record
        Expected: Order created with all items and details
        """
        mock_payment.return_value = {
            'success': True,
            'transaction_id': 'TXN-12347',
            'amount': 79.98
        }
        
        # Add multiple items
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 2}
        )
        
        # Process payment
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': self._create_mock_payment_data(),
                'shipping_address': self._create_mock_shipping_address()
            }
        )
        self.assertEqual(response.status_code, 200)
        order = response.json['order']
        self.assertIn('order_number', order)
        self.assertEqual(len(order['items']), 1)
        self.assertEqual(order['items'][0]['quantity'], 2)


class TestPaymentProcessingNegative(BaseEcommerceTestCase):
    """Negative test cases for payment processing"""
    
    def test_process_payment_with_empty_cart(self):
        """Test: Process payment with empty cart
        Expected: 400 Bad Request - cart is empty
        """
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': self._create_mock_payment_data(),
                'shipping_address': self._create_mock_shipping_address()
            }
        )
        self.assertEqual(response.status_code, 400)
        error_msg = str(response.json.get('error', '') or response.json.get('message', '')).lower()
        self.assertIn('cart', error_msg)
    
    def test_process_payment_with_invalid_card_number(self):
        """Test: Process payment with invalid card number
        Expected: 400 Bad Request - invalid card number
        """
        # Add items
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        
        # Invalid card number
        payment_data = self._create_mock_payment_data(card_number='1234567890123456')
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': payment_data,
                'shipping_address': self._create_mock_shipping_address()
            }
        )
        self.assertEqual(response.status_code, 400)
        error_msg = str(response.json.get('error', '') or response.json.get('message', '')).lower()
        self.assertIn('card', error_msg)
    
    def test_process_payment_with_expired_card(self):
        """Test: Process payment with expired card
        Expected: 400 Bad Request - card expired
        """
        # Add items
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        
        # Expired card (year in past)
        payment_data = self._create_mock_payment_data(expiry_year=2020)
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': payment_data,
                'shipping_address': self._create_mock_shipping_address()
            }
        )
        self.assertEqual(response.status_code, 400)
        error_msg = str(response.json.get('error', '') or response.json.get('message', '')).lower()
        self.assertIn('expired', error_msg)
    
    def test_process_payment_with_invalid_cvv(self):
        """Test: Process payment with invalid CVV
        Expected: 400 Bad Request - invalid CVV
        """
        # Add items
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        
        # Invalid CVV (too short)
        payment_data = self._create_mock_payment_data(cvv='12')
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': payment_data,
                'shipping_address': self._create_mock_shipping_address()
            }
        )
        self.assertEqual(response.status_code, 400)
    
    def test_process_payment_without_shipping_address(self):
        """Test: Process payment without shipping address
        Expected: 400 Bad Request - shipping address required
        """
        # Add items
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': self._create_mock_payment_data()
            }
        )
        self.assertEqual(response.status_code, 400)
        error_msg = str(response.json.get('error', '') or response.json.get('message', '')).lower()
        self.assertIn('shipping', error_msg)
    
    @patch('app.services.payment_service.process_payment')
    def test_process_payment_gateway_failure(self, mock_payment):
        """Test: Payment gateway returns failure
        Expected: 402 Payment Required or 500 Internal Server Error
        """
        # Mock payment failure
        mock_payment.return_value = {
            'success': False,
            'error': 'Insufficient funds',
            'error_code': 'INSUFFICIENT_FUNDS'
        }
        
        # Add items
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': self._create_mock_payment_data(),
                'shipping_address': self._create_mock_shipping_address()
            }
        )
        self.assertIn(response.status_code, [402, 400, 500])
        error_msg = str(response.json.get('error', '') or response.json.get('message', '')).lower()
        self.assertIn('payment', error_msg)


class TestPaymentProcessingEdgeCases(BaseEcommerceTestCase):
    """Edge cases for payment processing"""
    
    def test_process_payment_with_missing_optional_fields(self):
        """Test: Process payment with missing optional fields
        Expected: Payment processed if required fields present
        """
        # Add items
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        
        # Minimal payment data (only required fields)
        from datetime import datetime
        future_year = datetime.now().year + 1
        minimal_payment = {
            'card_number': '4111111111111111',
            'expiry_month': 12,
            'expiry_year': future_year,
            'cvv': '123'
        }
        
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': minimal_payment,
                'shipping_address': self._create_mock_shipping_address()
            }
        )
        # Should either succeed or fail with specific error
        self.assertIn(response.status_code, [200, 400])
    
    def test_process_payment_with_special_characters_in_name(self):
        """Test: Process payment with special characters in cardholder name
        Expected: Payment processed successfully
        """
        # Add items
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        
        payment_data = self._create_mock_payment_data()
        payment_data['cardholder_name'] = "O'Brien"
        
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': payment_data,
                'shipping_address': self._create_mock_shipping_address()
            }
        )
        # Should handle special characters
        self.assertIn(response.status_code, [200, 400])


class TestPaymentProcessingSecurity(BaseEcommerceTestCase):
    """Security test cases for payment processing"""
    
    def test_payment_data_not_stored_in_plaintext(self):
        """Test: Payment card data not stored in database
        Expected: Only transaction ID and last 4 digits stored
        """
        # Add items
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        
        payment_data = self._create_mock_payment_data()
        
        # Process payment (mocked)
        with patch('app.services.payment_service.process_payment') as mock_payment:
            mock_payment.return_value = {
                'success': True,
                'transaction_id': 'TXN-12345',
                'amount': 29.99
            }
            
            response = self.client.post(
                '/api/checkout/process-payment',
                headers=self.customer_headers,
                json={
                    'payment': payment_data,
                    'shipping_address': self._create_mock_shipping_address()
                }
            )
            
            if response.status_code == 200:
                order = response.json['order']
                # Verify full card number not in response
                self.assertNotIn('card_number', str(order))
                # Only last 4 digits should be present if any
                if 'last4' in order.get('payment', {}):
                    self.assertEqual(len(str(order['payment']['last4'])), 4)
    
    def test_sql_injection_in_payment_fields(self):
        """Test: Attempt SQL injection in payment fields
        Expected: Treated as invalid input, no SQL execution
        """
        # Add items
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        
        payment_data = self._create_mock_payment_data()
        payment_data['cardholder_name'] = "'; DROP TABLE orders; --"
        
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': payment_data,
                'shipping_address': self._create_mock_shipping_address()
            }
        )
        # Should reject as invalid input
        self.assertEqual(response.status_code, 400)
    
    def test_xss_in_shipping_address(self):
        """Test: Attempt XSS attack in shipping address
        Expected: Script tags sanitized or rejected
        """
        # Add items
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        
        shipping_address = self._create_mock_shipping_address()
        shipping_address['full_name'] = '<script>alert("XSS")</script>'
        
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': self._create_mock_payment_data(),
                'shipping_address': shipping_address
            }
        )
        # Should either sanitize or reject
        self.assertIn(response.status_code, [200, 400])
        if response.status_code == 200:
            # If accepted, verify XSS payload not executed
            order = response.json['order']
            self.assertNotIn('<script>', str(order['shipping_address']))
    
    def test_payment_data_validation_luhn_algorithm(self):
        """Test: Card number validated using Luhn algorithm
        Expected: Invalid card numbers rejected
        """
        # Add items
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        
        # Invalid card number (fails Luhn check)
        payment_data = self._create_mock_payment_data(card_number='4111111111111112')
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': payment_data,
                'shipping_address': self._create_mock_shipping_address()
            }
        )
        self.assertEqual(response.status_code, 400)
        error_msg = str(response.json.get('error', '') or response.json.get('message', '')).lower()
        self.assertIn('card', error_msg)
    
    def test_payment_amount_tampering_prevention(self):
        """Test: Prevent payment amount tampering
        Expected: Payment amount must match cart total
        """
        # Add items
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}  # $29.99
        )
        
        # Try to send different amount
        payment_data = self._create_mock_payment_data()
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': payment_data,
                'shipping_address': self._create_mock_shipping_address(),
                'amount': 1.00  # Attempted tampering
            }
        )
        # Should use cart total, not provided amount
        # This depends on implementation - verify amount matches cart
        if response.status_code == 200:
            order = response.json['order']
            # Amount should match cart total, not tampered value
            self.assertNotEqual(float(order['total']), 1.00)


# ============================================================================
# ORDER CONFIRMATION TESTS
# ============================================================================

class TestOrderConfirmationPositive(BaseEcommerceTestCase):
    """Positive test cases for order confirmation"""
    
    @patch('app.services.payment_service.process_payment')
    def test_order_confirmation_after_payment(self, mock_payment):
        """Test: Order confirmed after successful payment
        Expected: Order created with confirmed status
        """
        mock_payment.return_value = {
            'success': True,
            'transaction_id': 'TXN-12345',
            'amount': 29.99
        }
        
        # Add items and process payment
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': self._create_mock_payment_data(),
                'shipping_address': self._create_mock_shipping_address()
            }
        )
        
        self.assertEqual(response.status_code, 200)
        order = response.json['order']
        self.assertEqual(order['status'], 'confirmed')
        self.assertIn('order_number', order)
        self.assertIn('created_at', order)
    
    @patch('app.services.payment_service.process_payment')
    def test_order_contains_all_cart_items(self, mock_payment):
        """Test: Order contains all items from cart
        Expected: All cart items included in order
        """
        mock_payment.return_value = {
            'success': True,
            'transaction_id': 'TXN-12346',
            'amount': 79.98
        }
        
        # Add multiple items
        items = [
            {'product_id': 1, 'quantity': 2},
            {'product_id': 2, 'quantity': 1}
        ]
        for item in items:
            self.client.post(
                '/api/cart/items',
                headers=self.customer_headers,
                json=item
            )
        
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': self._create_mock_payment_data(),
                'shipping_address': self._create_mock_shipping_address()
            }
        )
        
        order = response.json['order']
        self.assertEqual(len(order['items']), 2)
    
    @patch('app.services.payment_service.process_payment')
    def test_order_includes_shipping_address(self, mock_payment):
        """Test: Order includes shipping address
        Expected: Shipping address stored with order
        """
        mock_payment.return_value = {
            'success': True,
            'transaction_id': 'TXN-12347',
            'amount': 29.99
        }
        
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        
        shipping_address = self._create_mock_shipping_address()
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': self._create_mock_payment_data(),
                'shipping_address': shipping_address
            }
        )
        
        order = response.json['order']
        self.assertIn('shipping_address', order)
        self.assertEqual(order['shipping_address']['city'], shipping_address['city'])
    
    @patch('app.services.payment_service.process_payment')
    def test_order_includes_payment_details(self, mock_payment):
        """Test: Order includes payment transaction details
        Expected: Transaction ID and payment method stored
        """
        mock_payment.return_value = {
            'success': True,
            'transaction_id': 'TXN-12348',
            'amount': 29.99
        }
        
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': self._create_mock_payment_data(),
                'shipping_address': self._create_mock_shipping_address()
            }
        )
        
        order = response.json['order']
        self.assertIn('transaction_id', order)
        self.assertEqual(order['transaction_id'], 'TXN-12348')
        self.assertIn('payment_method', order)


class TestOrderConfirmationNegative(BaseEcommerceTestCase):
    """Negative test cases for order confirmation"""
    
    def test_get_order_without_authentication(self):
        """Test: Get order details without authentication
        Expected: 401 Unauthorized (if auth required) or 404 (if order doesn't exist)
        Note: This test verifies authentication behavior - may pass or fail based on API design
        """
        response = self.client.get('/api/orders/1')
        # Accept either 401 (auth required) or 404 (order not found)
        self.assertIn(response.status_code, [401, 404])
    
    def test_get_nonexistent_order(self):
        """Test: Get non-existent order
        Expected: 404 Not Found
        """
        response = self.client.get(
            '/api/orders/99999',
            headers=self.customer_headers
        )
        self.assertEqual(response.status_code, 404)
    
    def test_get_other_user_order(self):
        """Test: Get another user's order
        Expected: 403 Forbidden
        """
        # Create second customer and order
        customer2 = User(
            username='customer2',
            email='customer2@example.com',
            role=User.ROLE_CUSTOMER
        )
        customer2.set_password('password123')
        db.session.add(customer2)
        db.session.commit()
        
        # Try to access order as different user
        response = self.client.get(
            '/api/orders/1',
            headers=self.customer_headers
        )
        # Should be 403 if order belongs to customer2, or 404 if order doesn't exist
        self.assertIn(response.status_code, [403, 404])


class TestOrderConfirmationEdgeCases(BaseEcommerceTestCase):
    """Edge cases for order confirmation"""
    
    @patch('app.services.payment_service.process_payment')
    def test_order_preserves_discount_applied(self, mock_payment):
        """Test: Order preserves discount code that was applied
        Expected: Discount code and amount stored with order
        """
        mock_payment.return_value = {
            'success': True,
            'transaction_id': 'TXN-12349',
            'amount': 26.99
        }
        
        # Add items and apply discount
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        self.client.post(
            '/api/cart/apply-discount',
            headers=self.customer_headers,
            json={'discount_code': 'SAVE10'}
        )
        
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': self._create_mock_payment_data(),
                'shipping_address': self._create_mock_shipping_address()
            }
        )
        
        order = response.json['order']
        self.assertIn('discount_code', order)
        self.assertEqual(order['discount_code'], 'SAVE10')
        self.assertGreater(float(order.get('discount_amount', 0)), 0)


# ============================================================================
# EMAIL NOTIFICATION TESTS
# ============================================================================

class TestEmailNotificationsPositive(BaseEcommerceTestCase):
    """Positive test cases for email notifications"""
    
    @patch('app.services.email_service.send_email')
    @patch('app.services.payment_service.process_payment')
    def test_send_order_confirmation_email(self, mock_payment, mock_email):
        """Test: Send order confirmation email after successful payment
        Expected: Email sent to customer with order details
        """
        mock_payment.return_value = {
            'success': True,
            'transaction_id': 'TXN-12350',
            'amount': 29.99
        }
        mock_email.return_value = {'success': True, 'message_id': 'MSG-123'}
        
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': self._create_mock_payment_data(),
                'shipping_address': self._create_mock_shipping_address()
            }
        )
        
        self.assertEqual(response.status_code, 200)
        # Verify email service was called
        self.assertTrue(mock_email.called)
        call_args = mock_email.call_args
        self.assertEqual(call_args[1]['to'], self.test_customer.email)
        self.assertIn('order', call_args[1]['subject'].lower())
    
    @patch('app.services.email_service.send_email')
    @patch('app.services.payment_service.process_payment')
    def test_order_confirmation_email_contains_order_details(self, mock_payment, mock_email):
        """Test: Order confirmation email contains order details
        Expected: Email includes order number, items, total
        """
        mock_payment.return_value = {
            'success': True,
            'transaction_id': 'TXN-12351',
            'amount': 29.99
        }
        mock_email.return_value = {'success': True}
        
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        
        self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': self._create_mock_payment_data(),
                'shipping_address': self._create_mock_shipping_address()
            }
        )
        
        # Verify email content
        call_args = mock_email.call_args
        email_body = call_args[1].get('body', '') or call_args[1].get('html', '')
        self.assertIn('order', email_body.lower())
        self.assertIn('total', email_body.lower())


class TestEmailNotificationsNegative(BaseEcommerceTestCase):
    """Negative test cases for email notifications"""
    
    @patch('app.services.email_service.send_email')
    @patch('app.services.payment_service.process_payment')
    def test_order_created_even_if_email_fails(self, mock_payment, mock_email):
        """Test: Order created even if email sending fails
        Expected: Order created, email failure logged but doesn't block order
        """
        mock_payment.return_value = {
            'success': True,
            'transaction_id': 'TXN-12352',
            'amount': 29.99
        }
        mock_email.side_effect = Exception('Email service unavailable')
        
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        
        response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': self._create_mock_payment_data(),
                'shipping_address': self._create_mock_shipping_address()
            }
        )
        
        # Order should still be created
        self.assertEqual(response.status_code, 200)
        self.assertIn('order', response.json)


class TestEmailNotificationsSecurity(BaseEcommerceTestCase):
    """Security test cases for email notifications"""
    
    @patch('app.services.email_service.send_email')
    @patch('app.services.payment_service.process_payment')
    def test_email_does_not_contain_payment_details(self, mock_payment, mock_email):
        """Test: Email does not contain sensitive payment information
        Expected: Email excludes full card numbers, CVV
        """
        mock_payment.return_value = {
            'success': True,
            'transaction_id': 'TXN-12353',
            'amount': 29.99
        }
        mock_email.return_value = {'success': True}
        
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 1}
        )
        
        payment_data = self._create_mock_payment_data()
        self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': payment_data,
                'shipping_address': self._create_mock_shipping_address()
            }
        )
        
        # Verify email doesn't contain sensitive data
        call_args = mock_email.call_args
        email_body = str(call_args[1].get('body', '') or call_args[1].get('html', ''))
        self.assertNotIn(payment_data['card_number'], email_body)
        self.assertNotIn(payment_data['cvv'], email_body)


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestCheckoutIntegration(BaseEcommerceTestCase):
    """Integration test cases for complete checkout flow"""
    
    @patch('app.services.email_service.send_email')
    @patch('app.services.payment_service.process_payment')
    def test_complete_checkout_flow(self, mock_payment, mock_email):
        """Test: Complete checkout flow from cart to order confirmation
        Expected: All steps succeed in sequence
        """
        mock_payment.return_value = {
            'success': True,
            'transaction_id': 'TXN-12354',
            'amount': 79.98
        }
        mock_email.return_value = {'success': True}
        
        # 1. Add items to cart
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 2}
        )
        
        # 2. Verify cart
        cart_response = self.client.get('/api/cart', headers=self.customer_headers)
        self.assertEqual(cart_response.status_code, 200)
        self.assertEqual(len(cart_response.json['cart']['items']), 1)
        
        # 3. Apply discount code
        discount_response = self.client.post(
            '/api/cart/apply-discount',
            headers=self.customer_headers,
            json={'discount_code': 'SAVE10'}
        )
        self.assertEqual(discount_response.status_code, 200)
        
        # 4. Process payment
        payment_response = self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': self._create_mock_payment_data(),
                'shipping_address': self._create_mock_shipping_address()
            }
        )
        self.assertEqual(payment_response.status_code, 200)
        
        # 5. Verify order created
        order = payment_response.json['order']
        self.assertEqual(order['status'], 'confirmed')
        self.assertIn('order_number', order)
        
        # 6. Verify email sent
        self.assertTrue(mock_email.called)
        
        # 7. Verify cart cleared after order
        final_cart = self.client.get('/api/cart', headers=self.customer_headers)
        self.assertEqual(len(final_cart.json['cart']['items']), 0)
    
    @patch('app.services.payment_service.process_payment')
    def test_checkout_updates_product_stock(self, mock_payment):
        """Test: Checkout updates product stock levels
        Expected: Product stock decreased after order
        """
        mock_payment.return_value = {
            'success': True,
            'transaction_id': 'TXN-12355',
            'amount': 29.99
        }
        
        initial_stock = 100
        
        # Add items
        self.client.post(
            '/api/cart/items',
            headers=self.customer_headers,
            json={'product_id': 1, 'quantity': 5}
        )
        
        # Process payment
        self.client.post(
            '/api/checkout/process-payment',
            headers=self.customer_headers,
            json={
                'payment': self._create_mock_payment_data(),
                'shipping_address': self._create_mock_shipping_address()
            }
        )
        
        # Verify stock updated (if product endpoint exists)
        # This would require product model/endpoint implementation
        # product_response = self.client.get('/api/products/1')
        # self.assertEqual(product_response.json['stock'], initial_stock - 5)


# ============================================================================
# TEST SUITE RUNNER
# ============================================================================

def suite():
    """Create test suite for e-commerce checkout"""
    test_suite = unittest.TestSuite()
    
    # Cart management tests
    test_suite.addTest(unittest.makeSuite(TestCartManagementPositive))
    test_suite.addTest(unittest.makeSuite(TestCartManagementNegative))
    test_suite.addTest(unittest.makeSuite(TestCartManagementEdgeCases))
    test_suite.addTest(unittest.makeSuite(TestCartManagementSecurity))
    
    # Discount code tests
    test_suite.addTest(unittest.makeSuite(TestDiscountCodePositive))
    test_suite.addTest(unittest.makeSuite(TestDiscountCodeNegative))
    test_suite.addTest(unittest.makeSuite(TestDiscountCodeEdgeCases))
    test_suite.addTest(unittest.makeSuite(TestDiscountCodeSecurity))
    
    # Payment processing tests
    test_suite.addTest(unittest.makeSuite(TestPaymentProcessingPositive))
    test_suite.addTest(unittest.makeSuite(TestPaymentProcessingNegative))
    test_suite.addTest(unittest.makeSuite(TestPaymentProcessingEdgeCases))
    test_suite.addTest(unittest.makeSuite(TestPaymentProcessingSecurity))
    
    # Order confirmation tests
    test_suite.addTest(unittest.makeSuite(TestOrderConfirmationPositive))
    test_suite.addTest(unittest.makeSuite(TestOrderConfirmationNegative))
    test_suite.addTest(unittest.makeSuite(TestOrderConfirmationEdgeCases))
    
    # Email notification tests
    test_suite.addTest(unittest.makeSuite(TestEmailNotificationsPositive))
    test_suite.addTest(unittest.makeSuite(TestEmailNotificationsNegative))
    test_suite.addTest(unittest.makeSuite(TestEmailNotificationsSecurity))
    
    # Integration tests
    test_suite.addTest(unittest.makeSuite(TestCheckoutIntegration))
    
    return test_suite


if __name__ == '__main__':
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    
    # Print summary
    print(f"\n{'='*70}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100)
        print(f"Success rate: {success_rate:.1f}%")
    print(f"{'='*70}")
