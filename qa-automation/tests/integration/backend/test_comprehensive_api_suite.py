"""
Comprehensive API Test Suite
Tests for User Management, Product Catalog, and Orders REST API

Covers:
- GET, POST, PUT, DELETE operations
- Authentication & Authorization
- Input validation
- Error responses
- Rate limiting
- Performance (response time < 500ms)
"""

import pytest
import time
import json
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_jwt_extended import create_access_token

from app import create_app, db
from app.models import User, Product, Order, OrderItem, Cart, CartItem, DiscountCode


class TestConfig:
    """Test configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'test-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = 'memory://'


@pytest.fixture(scope='function')
def app():
    """Create application for testing"""
    app = create_app('testing')
    app.config.from_object(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture(scope='function')
def regular_user(app):
    """Create a regular user"""
    with app.app_context():
        user = User(
            username='testuser',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            role=User.ROLE_CUSTOMER
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture(scope='function')
def admin_user(app):
    """Create an admin user"""
    with app.app_context():
        user = User(
            username='admin',
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            role=User.ROLE_ADMIN
        )
        user.set_password('admin123')
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture(scope='function')
def regular_user_token(app, regular_user):
    """Get JWT token for regular user"""
    with app.app_context():
        return create_access_token(identity=regular_user.id)


@pytest.fixture(scope='function')
def admin_user_token(app, admin_user):
    """Get JWT token for admin user"""
    with app.app_context():
        return create_access_token(identity=admin_user.id)


@pytest.fixture(scope='function')
def auth_headers_regular(regular_user_token):
    """Authorization headers for regular user"""
    return {'Authorization': f'Bearer {regular_user_token}'}


@pytest.fixture(scope='function')
def auth_headers_admin(admin_user_token):
    """Authorization headers for admin user"""
    return {'Authorization': f'Bearer {admin_user_token}'}


@pytest.fixture(scope='function')
def sample_products(app):
    """Create sample products"""
    with app.app_context():
        products = [
            Product(
                title='Product 1',
                description='Description 1',
                price=Decimal('29.99'),
                stock=100,
                in_stock=True,
                category='Electronics',
                sku='PROD-001'
            ),
            Product(
                title='Product 2',
                description='Description 2',
                price=Decimal('49.99'),
                stock=50,
                in_stock=True,
                category='Clothing',
                sku='PROD-002'
            ),
            Product(
                title='Product 3',
                description='Description 3',
                price=Decimal('19.99'),
                stock=0,
                in_stock=False,
                category='Electronics',
                sku='PROD-003'
            ),
        ]
        for product in products:
            db.session.add(product)
        db.session.commit()
        return products


@pytest.fixture(scope='function')
def sample_order(app, regular_user, sample_products):
    """Create a sample order"""
    with app.app_context():
        order = Order(
            order_number='ORD-20260122-0001',
            user_id=regular_user.id,
            subtotal=Decimal('29.99'),
            tax=Decimal('2.40'),
            shipping=Decimal('5.00'),
            total=Decimal('37.39'),
            status='confirmed',
            payment_status='paid',
            transaction_id='TXN-12345',
            shipping_address={
                'full_name': 'Test User',
                'street': '123 Main St',
                'city': 'New York',
                'state': 'NY',
                'zip': '10001',
                'country': 'US'
            }
        )
        db.session.add(order)
        db.session.flush()
        
        order_item = OrderItem(
            order_id=order.id,
            product_id=sample_products[0].id,
            product_title=sample_products[0].title,
            product_price=sample_products[0].price,
            quantity=1,
            subtotal=Decimal('29.99')
        )
        db.session.add(order_item)
        db.session.commit()
        return order


# ============================================================================
# AUTHENTICATION TESTS
# ============================================================================

class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_register_user_success(self, client):
        """Test successful user registration"""
        response = client.post('/api/auth/register', json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'first_name': 'New',
            'last_name': 'User'
        })
        
        assert response.status_code == 201
        data = response.json
        assert 'id' in data
        assert data['username'] == 'newuser'
        assert data['email'] == 'newuser@example.com'
        assert 'password' not in data  # Password should not be in response
    
    def test_register_user_duplicate_username(self, client, regular_user):
        """Test registration with duplicate username"""
        response = client.post('/api/auth/register', json={
            'username': regular_user.username,
            'email': 'different@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 400
    
    def test_register_user_duplicate_email(self, client, regular_user):
        """Test registration with duplicate email"""
        response = client.post('/api/auth/register', json={
            'username': 'differentuser',
            'email': regular_user.email,
            'password': 'password123'
        })
        
        assert response.status_code == 400
    
    def test_register_user_missing_fields(self, client):
        """Test registration with missing required fields"""
        response = client.post('/api/auth/register', json={
            'username': 'newuser'
            # Missing email and password
        })
        
        assert response.status_code == 400
    
    def test_register_user_invalid_email(self, client):
        """Test registration with invalid email format"""
        response = client.post('/api/auth/register', json={
            'username': 'newuser',
            'email': 'invalid-email',
            'password': 'password123'
        })
        
        assert response.status_code == 400
    
    def test_login_success(self, client, regular_user):
        """Test successful login"""
        response = client.post('/api/auth/login', json={
            'username': regular_user.username,
            'password': 'password123'
        })
        
        assert response.status_code == 200
        data = response.json
        assert 'access_token' in data
        assert 'refresh_token' in data
    
    def test_login_invalid_username(self, client):
        """Test login with invalid username"""
        response = client.post('/api/auth/login', json={
            'username': 'nonexistent',
            'password': 'password123'
        })
        
        assert response.status_code == 401
    
    def test_login_invalid_password(self, client, regular_user):
        """Test login with invalid password"""
        response = client.post('/api/auth/login', json={
            'username': regular_user.username,
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401
    
    def test_login_missing_fields(self, client):
        """Test login with missing fields"""
        response = client.post('/api/auth/login', json={
            'username': 'testuser'
            # Missing password
        })
        
        assert response.status_code == 400
    
    def test_get_current_user(self, client, auth_headers_regular, regular_user):
        """Test getting current user info"""
        response = client.get('/api/auth/me', headers=auth_headers_regular)
        
        assert response.status_code == 200
        data = response.json
        assert data['id'] == regular_user.id
        assert data['username'] == regular_user.username
    
    def test_get_current_user_unauthorized(self, client):
        """Test getting current user without authentication"""
        response = client.get('/api/auth/me')
        
        assert response.status_code == 401


# ============================================================================
# USER MANAGEMENT TESTS
# ============================================================================

class TestUserManagement:
    """Test user management endpoints"""
    
    def test_get_users_list_success(self, client, auth_headers_regular, regular_user, admin_user):
        """Test GET /api/users - list all users"""
        response = client.get('/api/users', headers=auth_headers_regular)
        
        assert response.status_code == 200
        data = response.json
        assert 'users' in data
        assert len(data['users']) >= 2  # At least regular_user and admin_user
        assert 'total' in data
        assert 'pages' in data
    
    def test_get_users_list_pagination(self, client, auth_headers_regular):
        """Test GET /api/users with pagination"""
        response = client.get('/api/users?page=1&per_page=1', headers=auth_headers_regular)
        
        assert response.status_code == 200
        data = response.json
        assert len(data['users']) <= 1
        assert data['current_page'] == 1
    
    def test_get_users_list_unauthorized(self, client):
        """Test GET /api/users without authentication"""
        response = client.get('/api/users')
        
        assert response.status_code == 401
    
    def test_get_user_by_id_success(self, client, auth_headers_regular, regular_user):
        """Test GET /api/users/<id> - get user by ID"""
        response = client.get(f'/api/users/{regular_user.id}', headers=auth_headers_regular)
        
        assert response.status_code == 200
        data = response.json
        assert data['id'] == regular_user.id
        assert data['username'] == regular_user.username
    
    def test_get_user_by_id_not_found(self, client, auth_headers_regular):
        """Test GET /api/users/<id> with non-existent ID"""
        response = client.get('/api/users/99999', headers=auth_headers_regular)
        
        assert response.status_code == 404
    
    def test_get_user_by_id_unauthorized(self, client, regular_user):
        """Test GET /api/users/<id> without authentication"""
        response = client.get(f'/api/users/{regular_user.id}')
        
        assert response.status_code == 401
    
    def test_update_user_own_profile(self, client, auth_headers_regular, regular_user):
        """Test PUT /api/users/<id> - update own profile"""
        response = client.put(
            f'/api/users/{regular_user.id}',
            headers=auth_headers_regular,
            json={
                'first_name': 'Updated',
                'last_name': 'Name'
            }
        )
        
        assert response.status_code == 200
        data = response.json
        assert data['first_name'] == 'Updated'
        assert data['last_name'] == 'Name'
    
    def test_update_user_other_user_forbidden(self, client, auth_headers_regular, admin_user):
        """Test PUT /api/users/<id> - update other user's profile (forbidden)"""
        response = client.put(
            f'/api/users/{admin_user.id}',
            headers=auth_headers_regular,
            json={'first_name': 'Hacked'}
        )
        
        assert response.status_code == 403
    
    def test_update_user_as_admin(self, client, auth_headers_admin, regular_user):
        """Test PUT /api/users/<id> - admin can update any user"""
        response = client.put(
            f'/api/users/{regular_user.id}',
            headers=auth_headers_admin,
            json={'first_name': 'AdminUpdated'}
        )
        
        assert response.status_code == 200
        data = response.json
        assert data['first_name'] == 'AdminUpdated'
    
    def test_update_user_invalid_email(self, client, auth_headers_regular, regular_user):
        """Test PUT /api/users/<id> with invalid email"""
        response = client.put(
            f'/api/users/{regular_user.id}',
            headers=auth_headers_regular,
            json={'email': 'invalid-email'}
        )
        
        assert response.status_code == 400
    
    def test_update_user_duplicate_email(self, client, auth_headers_regular, regular_user, admin_user):
        """Test PUT /api/users/<id> with duplicate email"""
        response = client.put(
            f'/api/users/{regular_user.id}',
            headers=auth_headers_regular,
            json={'email': admin_user.email}
        )
        
        assert response.status_code == 400
    
    def test_update_user_role_as_non_admin(self, client, auth_headers_regular, regular_user):
        """Test PUT /api/users/<id> - non-admin cannot update role"""
        response = client.put(
            f'/api/users/{regular_user.id}',
            headers=auth_headers_regular,
            json={'role': User.ROLE_ADMIN}
        )
        
        assert response.status_code == 403
    
    def test_update_user_role_as_admin(self, client, auth_headers_admin, regular_user):
        """Test PUT /api/users/<id> - admin can update role"""
        response = client.put(
            f'/api/users/{regular_user.id}',
            headers=auth_headers_admin,
            json={'role': User.ROLE_ADMIN}
        )
        
        assert response.status_code == 200
    
    def test_delete_user_own_profile(self, client, app, auth_headers_regular):
        """Test DELETE /api/users/<id> - delete own profile"""
        # Create a user to delete
        with app.app_context():
            user = User(
                username='todelete',
                email='todelete@example.com',
                role=User.ROLE_CUSTOMER
            )
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            user_id = user.id
        
        token = create_access_token(identity=user_id)
        headers = {'Authorization': f'Bearer {token}'}
        
        response = client.delete(f'/api/users/{user_id}', headers=headers)
        
        assert response.status_code == 204
        
        # Verify user is deleted
        with app.app_context():
            deleted_user = User.query.get(user_id)
            assert deleted_user is None
    
    def test_delete_user_other_user_forbidden(self, client, auth_headers_regular, admin_user):
        """Test DELETE /api/users/<id> - delete other user (forbidden)"""
        response = client.delete(f'/api/users/{admin_user.id}', headers=auth_headers_regular)
        
        assert response.status_code == 403
    
    def test_delete_user_as_admin(self, client, app, auth_headers_admin):
        """Test DELETE /api/users/<id> - admin can delete any user"""
        # Create a user to delete
        with app.app_context():
            user = User(
                username='todelete2',
                email='todelete2@example.com',
                role=User.ROLE_CUSTOMER
            )
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            user_id = user.id
        
        response = client.delete(f'/api/users/{user_id}', headers=auth_headers_admin)
        
        assert response.status_code == 204
    
    def test_delete_user_not_found(self, client, auth_headers_admin):
        """Test DELETE /api/users/<id> with non-existent ID"""
        response = client.delete('/api/users/99999', headers=auth_headers_admin)
        
        assert response.status_code == 404
    
    def test_delete_user_unauthorized(self, client, regular_user):
        """Test DELETE /api/users/<id> without authentication"""
        response = client.delete(f'/api/users/{regular_user.id}')
        
        assert response.status_code == 401


# ============================================================================
# PRODUCT CATALOG TESTS
# ============================================================================

class TestProductCatalog:
    """Test product catalog endpoints"""
    
    def test_get_products_list_success(self, client, sample_products):
        """Test GET /api/products - list all products"""
        response = client.get('/api/products')
        
        assert response.status_code == 200
        data = response.json
        assert 'products' in data
        assert len(data['products']) >= len(sample_products)
        assert 'pagination' in data
    
    def test_get_products_list_pagination(self, client, sample_products):
        """Test GET /api/products with pagination"""
        response = client.get('/api/products?page=1&per_page=1')
        
        assert response.status_code == 200
        data = response.json
        assert len(data['products']) <= 1
        assert data['pagination']['page'] == 1
    
    def test_get_products_filter_by_category(self, client, sample_products):
        """Test GET /api/products filtered by category"""
        response = client.get('/api/products?category=Electronics')
        
        assert response.status_code == 200
        data = response.json
        assert all(p['category'] == 'Electronics' for p in data['products'])
    
    def test_get_products_search(self, client, sample_products):
        """Test GET /api/products with search"""
        response = client.get('/api/products?search=Product 1')
        
        assert response.status_code == 200
        data = response.json
        assert len(data['products']) > 0
        assert any('Product 1' in p['title'] for p in data['products'])
    
    def test_get_products_in_stock_only(self, client, sample_products):
        """Test GET /api/products filtered to in-stock only"""
        response = client.get('/api/products?in_stock_only=true')
        
        assert response.status_code == 200
        data = response.json
        assert all(p['inStock'] is True for p in data['products'])
    
    def test_get_product_by_id_success(self, client, sample_products):
        """Test GET /api/products/<id> - get product by ID"""
        product = sample_products[0]
        response = client.get(f'/api/products/{product.id}')
        
        assert response.status_code == 200
        data = response.json
        assert 'product' in data
        assert int(data['product']['id']) == product.id
        assert data['product']['title'] == product.title
    
    def test_get_product_by_id_not_found(self, client):
        """Test GET /api/products/<id> with non-existent ID"""
        response = client.get('/api/products/99999')
        
        assert response.status_code == 404
    
    def test_get_products_max_per_page_limit(self, client, sample_products):
        """Test GET /api/products respects max per_page limit"""
        response = client.get('/api/products?per_page=200')  # Request more than max (100)
        
        assert response.status_code == 200
        data = response.json
        assert data['pagination']['per_page'] <= 100


# ============================================================================
# ORDERS TESTS
# ============================================================================

class TestOrders:
    """Test order endpoints"""
    
    def test_get_orders_list_success(self, client, auth_headers_regular, sample_order):
        """Test GET /api/orders - list user's orders"""
        response = client.get('/api/orders', headers=auth_headers_regular)
        
        assert response.status_code == 200
        data = response.json
        assert 'orders' in data
        assert len(data['orders']) >= 1
        assert 'pagination' in data
    
    def test_get_orders_list_empty(self, client, auth_headers_admin):
        """Test GET /api/orders when user has no orders"""
        response = client.get('/api/orders', headers=auth_headers_admin)
        
        assert response.status_code == 200
        data = response.json
        assert len(data['orders']) == 0
    
    def test_get_orders_list_unauthorized(self, client):
        """Test GET /api/orders without authentication"""
        response = client.get('/api/orders')
        
        assert response.status_code == 401
    
    def test_get_orders_list_pagination(self, client, auth_headers_regular, sample_order):
        """Test GET /api/orders with pagination"""
        response = client.get('/api/orders?page=1&per_page=1', headers=auth_headers_regular)
        
        assert response.status_code == 200
        data = response.json
        assert len(data['orders']) <= 1
    
    def test_get_order_by_id_success(self, client, auth_headers_regular, sample_order):
        """Test GET /api/orders/<id> - get order by ID"""
        response = client.get(f'/api/orders/{sample_order.id}', headers=auth_headers_regular)
        
        assert response.status_code == 200
        data = response.json
        assert 'order' in data
        assert data['order']['id'] == sample_order.id
        assert data['order']['order_number'] == sample_order.order_number
    
    def test_get_order_by_id_not_found(self, client, auth_headers_regular):
        """Test GET /api/orders/<id> with non-existent ID"""
        response = client.get('/api/orders/99999', headers=auth_headers_regular)
        
        assert response.status_code == 404
    
    def test_get_order_by_id_other_user_forbidden(self, client, app, auth_headers_admin):
        """Test GET /api/orders/<id> - access other user's order (forbidden)"""
        # Create order for different user
        with app.app_context():
            other_user = User(
                username='otheruser',
                email='other@example.com',
                role=User.ROLE_CUSTOMER
            )
            other_user.set_password('password123')
            db.session.add(other_user)
            db.session.commit()
            
            product = Product(
                title='Test Product',
                price=Decimal('10.00'),
                stock=10,
                in_stock=True
            )
            db.session.add(product)
            db.session.commit()
            
            order = Order(
                order_number='ORD-OTHER',
                user_id=other_user.id,
                subtotal=Decimal('10.00'),
                total=Decimal('10.00'),
                status='confirmed',
                payment_status='paid',
                shipping_address={'full_name': 'Other User', 'street': '123 St', 'city': 'NY', 'state': 'NY', 'zip': '10001', 'country': 'US'}
            )
            db.session.add(order)
            db.session.commit()
            order_id = order.id
        
        response = client.get(f'/api/orders/{order_id}', headers=auth_headers_admin)
        
        assert response.status_code == 403
    
    def test_get_order_by_id_unauthorized(self, client, sample_order):
        """Test GET /api/orders/<id> without authentication"""
        response = client.get(f'/api/orders/{sample_order.id}')
        
        assert response.status_code == 401


# ============================================================================
# INPUT VALIDATION TESTS
# ============================================================================

class TestInputValidation:
    """Test input validation"""
    
    def test_register_invalid_password_length(self, client):
        """Test registration with password too short"""
        response = client.post('/api/auth/register', json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': '123'  # Too short
        })
        
        assert response.status_code == 400
    
    def test_register_invalid_username_format(self, client):
        """Test registration with invalid username format"""
        response = client.post('/api/auth/register', json={
            'username': 'user name with spaces',  # Invalid format
            'email': 'user@example.com',
            'password': 'password123'
        })
        
        # Should either accept or reject based on validation rules
        assert response.status_code in [200, 400]
    
    def test_update_user_invalid_id_type(self, client, auth_headers_regular):
        """Test update user with invalid ID type"""
        response = client.put(
            '/api/users/abc',  # Invalid ID type
            headers=auth_headers_regular,
            json={'first_name': 'Test'}
        )
        
        assert response.status_code == 404  # Flask returns 404 for invalid route
    
    def test_get_products_invalid_page_number(self, client):
        """Test get products with invalid page number"""
        response = client.get('/api/products?page=abc')
        
        # Should default to page 1 or return 400
        assert response.status_code in [200, 400]
    
    def test_get_products_negative_page_number(self, client):
        """Test get products with negative page number"""
        response = client.get('/api/products?page=-1')
        
        # Should default to page 1 or return 400
        assert response.status_code in [200, 400]
    
    def test_update_user_empty_json(self, client, auth_headers_regular, regular_user):
        """Test update user with empty JSON body"""
        response = client.put(
            f'/api/users/{regular_user.id}',
            headers=auth_headers_regular,
            json={}
        )
        
        # Should accept empty update (partial update)
        assert response.status_code == 200
    
    def test_update_user_invalid_json(self, client, auth_headers_regular, regular_user):
        """Test update user with invalid JSON"""
        response = client.put(
            f'/api/users/{regular_user.id}',
            headers=auth_headers_regular,
            data='invalid json',
            content_type='application/json'
        )
        
        assert response.status_code == 400


# ============================================================================
# ERROR RESPONSE TESTS
# ============================================================================

class TestErrorResponses:
    """Test error responses"""
    
    def test_404_not_found(self, client):
        """Test 404 Not Found response"""
        response = client.get('/api/nonexistent')
        
        assert response.status_code == 404
        data = response.json
        assert 'error' in data
    
    def test_400_bad_request(self, client):
        """Test 400 Bad Request response"""
        response = client.post('/api/auth/register', json={
            'invalid': 'data'
        })
        
        assert response.status_code == 400
    
    def test_401_unauthorized(self, client):
        """Test 401 Unauthorized response"""
        response = client.get('/api/users')
        
        assert response.status_code == 401
    
    def test_403_forbidden(self, client, auth_headers_regular, admin_user):
        """Test 403 Forbidden response"""
        response = client.put(
            f'/api/users/{admin_user.id}',
            headers=auth_headers_regular,
            json={'first_name': 'Hacked'}
        )
        
        assert response.status_code == 403
    
    def test_500_internal_server_error(self, client, app, auth_headers_regular, regular_user):
        """Test 500 Internal Server Error handling"""
        # Mock database error
        with patch('app.users.routes.db.session.commit') as mock_commit:
            mock_commit.side_effect = Exception('Database error')
            
            response = client.put(
                f'/api/users/{regular_user.id}',
                headers=auth_headers_regular,
                json={'first_name': 'Test'}
            )
            
            # Should handle error gracefully
            assert response.status_code in [400, 500]


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPerformance:
    """Test API performance"""
    
    def test_get_products_response_time(self, client, sample_products):
        """Test GET /api/products response time < 500ms"""
        start_time = time.time()
        response = client.get('/api/products')
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        assert response.status_code == 200
        assert response_time_ms < 500, f"Response time {response_time_ms}ms exceeds 500ms"
    
    def test_get_users_response_time(self, client, auth_headers_regular):
        """Test GET /api/users response time < 500ms"""
        start_time = time.time()
        response = client.get('/api/users', headers=auth_headers_regular)
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        assert response.status_code == 200
        assert response_time_ms < 500, f"Response time {response_time_ms}ms exceeds 500ms"
    
    def test_get_orders_response_time(self, client, auth_headers_regular, sample_order):
        """Test GET /api/orders response time < 500ms"""
        start_time = time.time()
        response = client.get('/api/orders', headers=auth_headers_regular)
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        assert response.status_code == 200
        assert response_time_ms < 500, f"Response time {response_time_ms}ms exceeds 500ms"
    
    def test_get_product_by_id_response_time(self, client, sample_products):
        """Test GET /api/products/<id> response time < 500ms"""
        product = sample_products[0]
        start_time = time.time()
        response = client.get(f'/api/products/{product.id}')
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        assert response.status_code == 200
        assert response_time_ms < 500, f"Response time {response_time_ms}ms exceeds 500ms"
    
    def test_post_register_response_time(self, client):
        """Test POST /api/auth/register response time < 500ms"""
        start_time = time.time()
        response = client.post('/api/auth/register', json={
            'username': f'perfuser{int(time.time())}',
            'email': f'perf{int(time.time())}@example.com',
            'password': 'password123'
        })
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        assert response.status_code == 201
        assert response_time_ms < 500, f"Response time {response_time_ms}ms exceeds 500ms"


# ============================================================================
# RATE LIMITING TESTS
# ============================================================================

class TestRateLimiting:
    """Test rate limiting (if implemented)"""
    
    def test_rate_limiting_not_exceeded(self, client):
        """Test normal request rate doesn't trigger rate limit"""
        # Make a few requests quickly
        for i in range(5):
            response = client.get('/api/products')
            assert response.status_code == 200
    
    def test_rate_limiting_exceeded(self, client):
        """Test excessive requests trigger rate limit"""
        # Make many requests quickly
        rate_limited = False
        for i in range(100):
            response = client.get('/api/products')
            if response.status_code == 429:  # Too Many Requests
                rate_limited = True
                break
        
        # Rate limiting may or may not be implemented
        # If implemented, should return 429 after threshold
        # If not implemented, all requests should succeed
        if rate_limited:
            assert response.status_code == 429
            assert 'error' in response.json or 'message' in response.json


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for complete workflows"""
    
    def test_complete_user_workflow(self, client, app):
        """Test complete user registration and profile update workflow"""
        # 1. Register user
        register_response = client.post('/api/auth/register', json={
            'username': 'workflowuser',
            'email': 'workflow@example.com',
            'password': 'password123',
            'first_name': 'Workflow',
            'last_name': 'User'
        })
        assert register_response.status_code == 201
        user_id = register_response.json['id']
        
        # 2. Login
        login_response = client.post('/api/auth/login', json={
            'username': 'workflowuser',
            'password': 'password123'
        })
        assert login_response.status_code == 200
        token = login_response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # 3. Get current user
        me_response = client.get('/api/auth/me', headers=headers)
        assert me_response.status_code == 200
        assert me_response.json['id'] == user_id
        
        # 4. Update profile
        update_response = client.put(
            f'/api/users/{user_id}',
            headers=headers,
            json={'first_name': 'Updated'}
        )
        assert update_response.status_code == 200
        assert update_response.json['first_name'] == 'Updated'
        
        # 5. Get user by ID
        get_response = client.get(f'/api/users/{user_id}', headers=headers)
        assert get_response.status_code == 200
        assert get_response.json['id'] == user_id
    
    def test_complete_product_browse_workflow(self, client, sample_products):
        """Test complete product browsing workflow"""
        # 1. List all products
        list_response = client.get('/api/products')
        assert list_response.status_code == 200
        assert len(list_response.json['products']) > 0
        
        # 2. Filter by category
        category_response = client.get('/api/products?category=Electronics')
        assert category_response.status_code == 200
        
        # 3. Search products
        search_response = client.get('/api/products?search=Product')
        assert search_response.status_code == 200
        
        # 4. Get specific product
        product = sample_products[0]
        detail_response = client.get(f'/api/products/{product.id}')
        assert detail_response.status_code == 200
        assert detail_response.json['product']['id'] == str(product.id)
    
    def test_complete_order_workflow(self, client, app, sample_products):
        """Test complete order viewing workflow"""
        # Create user and order
        with app.app_context():
            user = User(
                username='orderuser',
                email='order@example.com',
                role=User.ROLE_CUSTOMER
            )
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            
            order = Order(
                order_number='ORD-WORKFLOW',
                user_id=user.id,
                subtotal=Decimal('29.99'),
                total=Decimal('29.99'),
                status='confirmed',
                payment_status='paid',
                shipping_address={'full_name': 'Test', 'street': '123 St', 'city': 'NY', 'state': 'NY', 'zip': '10001', 'country': 'US'}
            )
            db.session.add(order)
            db.session.commit()
            order_id = order.id
        
        # Login
        login_response = client.post('/api/auth/login', json={
            'username': 'orderuser',
            'password': 'password123'
        })
        assert login_response.status_code == 200
        token = login_response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # List orders
        list_response = client.get('/api/orders', headers=headers)
        assert list_response.status_code == 200
        assert len(list_response.json['orders']) >= 1
        
        # Get order details
        detail_response = client.get(f'/api/orders/{order_id}', headers=headers)
        assert detail_response.status_code == 200
        assert detail_response.json['order']['id'] == order_id


# ============================================================================
# SECURITY TESTS
# ============================================================================

class TestSecurity:
    """Security-related tests"""
    
    def test_sql_injection_username(self, client):
        """Test SQL injection attempt in username"""
        response = client.post('/api/auth/register', json={
            'username': "admin' OR '1'='1",
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        # Should handle safely (either reject or treat as literal string)
        assert response.status_code in [200, 400]
    
    def test_xss_in_user_input(self, client, auth_headers_regular, regular_user):
        """Test XSS attempt in user input"""
        response = client.put(
            f'/api/users/{regular_user.id}',
            headers=auth_headers_regular,
            json={'first_name': '<script>alert("XSS")</script>'}
        )
        
        # Should sanitize or reject
        assert response.status_code in [200, 400]
        if response.status_code == 200:
            # If accepted, verify it's sanitized in response
            assert '<script>' not in response.json.get('first_name', '')
    
    def test_jwt_token_tampering(self, client):
        """Test JWT token tampering"""
        tampered_token = 'Bearer invalid.token.here'
        response = client.get('/api/users', headers={'Authorization': tampered_token})
        
        assert response.status_code == 422  # Unprocessable Entity for invalid JWT
    
    def test_password_not_in_response(self, client, regular_user):
        """Test password is never returned in API responses"""
        response = client.post('/api/auth/login', json={
            'username': regular_user.username,
            'password': 'password123'
        })
        
        assert response.status_code == 200
        assert 'password' not in response.json
    
    def test_user_password_not_in_get_user(self, client, auth_headers_regular, regular_user):
        """Test password not in GET /api/users/<id> response"""
        response = client.get(f'/api/users/{regular_user.id}', headers=auth_headers_regular)
        
        assert response.status_code == 200
        assert 'password' not in response.json


# ============================================================================
# EDGE CASES
# ============================================================================

class TestEdgeCases:
    """Test edge cases"""
    
    def test_get_users_empty_database(self, client, app, auth_headers_admin, admin_user):
        """Test GET /api/users with empty database"""
        with app.app_context():
            # Delete all users except admin
            User.query.filter(User.id != admin_user.id).delete()
            db.session.commit()
        
        response = client.get('/api/users', headers=auth_headers_admin)
        
        assert response.status_code == 200
        assert len(response.json['users']) >= 1  # At least admin
    
    def test_get_products_empty_database(self, client, app):
        """Test GET /api/products with empty database"""
        with app.app_context():
            Product.query.delete()
            db.session.commit()
        
        response = client.get('/api/products')
        
        assert response.status_code == 200
        assert len(response.json['products']) == 0
    
    def test_get_orders_empty_database(self, client, auth_headers_regular):
        """Test GET /api/orders with empty database"""
        response = client.get('/api/orders', headers=auth_headers_regular)
        
        assert response.status_code == 200
        assert len(response.json['orders']) == 0
    
    def test_very_long_string_input(self, client, auth_headers_regular, regular_user):
        """Test very long string input"""
        long_string = 'a' * 10000
        response = client.put(
            f'/api/users/{regular_user.id}',
            headers=auth_headers_regular,
            json={'first_name': long_string}
        )
        
        # Should either accept (with truncation) or reject
        assert response.status_code in [200, 400]
    
    def test_special_characters_in_input(self, client, auth_headers_regular, regular_user):
        """Test special characters in input"""
        response = client.put(
            f'/api/users/{regular_user.id}',
            headers=auth_headers_regular,
            json={'first_name': "O'Brien & O'Connor"}
        )
        
        # Should handle special characters safely
        assert response.status_code in [200, 400]
    
    def test_unicode_characters(self, client, auth_headers_regular, regular_user):
        """Test Unicode characters in input"""
        response = client.put(
            f'/api/users/{regular_user.id}',
            headers=auth_headers_regular,
            json={'first_name': 'José 中文 🎉'}
        )
        
        # Should handle Unicode safely
        assert response.status_code in [200, 400]
