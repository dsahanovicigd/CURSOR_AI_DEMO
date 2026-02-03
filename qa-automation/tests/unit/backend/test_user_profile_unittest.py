"""
Comprehensive User Profile Management Test Cases - Unittest Format

This test suite uses Python's unittest framework with:
- Proper setUp and tearDown methods
- Mock data generation
- Organized test categories
- Comprehensive assertions

Test Categories:
- User Registration (positive, negative, edge cases, security)
- Profile Updates (positive, negative, edge cases, security)
- Password Changes (positive, negative, edge cases, security)
- Account Deletion (positive, negative, edge cases, security)
"""

import unittest
from app import create_app, db
from app.models import User
from app.cache import cache
from faker import Faker
import json


class BaseTestCase(unittest.TestCase):
    """Base test case with common setup and teardown"""
    
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
        
        # Create test users
        self.test_user = self._create_test_user()
        self.test_admin = self._create_test_admin()
        self.test_agent = self._create_test_agent()
        
        # Get authentication tokens
        self.user_headers = self._get_auth_headers(self.test_user, 'testpassword123')
        self.admin_headers = self._get_auth_headers(self.test_admin, 'adminpassword123')
        self.agent_headers = self._get_auth_headers(self.test_agent, 'agentpassword123')
    
    def tearDown(self):
        """Clean up after each test method"""
        db.session.remove()
        db.drop_all()
        cache.clear()
        self.app_context.pop()
    
    def _create_test_user(self):
        """Create a test customer user"""
        user = User(
            username=self.fake.user_name(),
            email=self.fake.email(),
            role=User.ROLE_CUSTOMER,
            is_active=True
        )
        user.set_password('testpassword123')
        db.session.add(user)
        db.session.commit()
        return user
    
    def _create_test_admin(self):
        """Create a test admin user"""
        admin = User(
            username='testadmin',
            email='admin@test.com',
            role=User.ROLE_ADMIN,
            is_admin=True,
            is_active=True
        )
        admin.set_password('adminpassword123')
        db.session.add(admin)
        db.session.commit()
        return admin
    
    def _create_test_agent(self):
        """Create a test agent user"""
        agent = User(
            username='testagent',
            email='agent@test.com',
            role=User.ROLE_AGENT,
            is_active=True,
            availability_status=User.AVAILABILITY_AVAILABLE
        )
        agent.set_password('agentpassword123')
        db.session.add(agent)
        db.session.commit()
        return agent
    
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
    
    def _create_user(self, username=None, email=None, password='SecurePass123', **kwargs):
        """Helper method to create a user"""
        user = User(
            username=username or self.fake.user_name(),
            email=email or self.fake.email(),
            role=kwargs.get('role', User.ROLE_CUSTOMER),
            is_active=kwargs.get('is_active', True),
            **{k: v for k, v in kwargs.items() if k not in ['role', 'is_active']}
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user


# ============================================================================
# USER REGISTRATION TESTS
# ============================================================================

class TestUserRegistrationPositive(BaseTestCase):
    """Positive test cases for user registration"""
    
    def test_register_user_with_minimal_fields(self):
        """Test: Register user with only required fields
        Expected: User created successfully with default role 'customer'
        """
        data = {
            'username': 'newuser123',
            'email': 'newuser@example.com',
            'password': 'SecurePass123'
        }
        response = self.client.post('/api/auth/register', json=data)
        
        self.assertEqual(response.status_code, 201, "Registration should succeed")
        response_data = response.json
        self.assertEqual(response_data['username'], 'newuser123')
        self.assertEqual(response_data['email'], 'newuser@example.com')
        self.assertEqual(response_data['role'], User.ROLE_CUSTOMER)
        self.assertNotIn('password', response_data, "Password should not be in response")
        self.assertTrue(response_data['is_active'])
    
    def test_register_user_with_all_fields(self):
        """Test: Register user with all optional fields
        Expected: User created with all provided information
        """
        data = {
            'username': 'completeuser',
            'email': 'complete@example.com',
            'password': 'SecurePass123',
            'first_name': 'John',
            'last_name': 'Doe',
            'name': 'John Doe',
            'role': User.ROLE_CUSTOMER,
            'availability_status': User.AVAILABILITY_AVAILABLE,
            'expertise_areas': ['Python', 'Flask', 'API Development']
        }
        response = self.client.post('/api/auth/register', json=data)
        
        self.assertEqual(response.status_code, 201)
        response_data = response.json
        self.assertEqual(response_data['first_name'], 'John')
        self.assertEqual(response_data['last_name'], 'Doe')
        self.assertEqual(response_data['expertise_areas'], ['Python', 'Flask', 'API Development'])
    
    def test_register_user_as_agent(self):
        """Test: Register user with agent role
        Expected: User created with agent role and availability status
        """
        data = {
            'username': 'agent1',
            'email': 'agent1@example.com',
            'password': 'SecurePass123',
            'role': User.ROLE_AGENT,
            'availability_status': User.AVAILABILITY_AVAILABLE,
            'expertise_areas': ['Support', 'Technical']
        }
        response = self.client.post('/api/auth/register', json=data)
        
        self.assertEqual(response.status_code, 201)
        response_data = response.json
        self.assertEqual(response_data['role'], User.ROLE_AGENT)
        self.assertEqual(response_data['availability_status'], User.AVAILABILITY_AVAILABLE)
    
    def test_register_user_with_maximum_length_username(self):
        """Test: Register user with maximum length username (80 chars)
        Expected: User created successfully
        """
        long_username = 'a' * 80
        data = {
            'username': long_username,
            'email': 'longuser@example.com',
            'password': 'SecurePass123'
        }
        response = self.client.post('/api/auth/register', json=data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['username'], long_username)
    
    def test_register_user_with_special_characters_in_name(self):
        """Test: Register user with special characters in name fields
        Expected: User created successfully with special characters preserved
        """
        data = {
            'username': 'specialuser',
            'email': 'special@example.com',
            'password': 'SecurePass123',
            'first_name': "O'Brien",
            'last_name': 'van der Berg'
        }
        response = self.client.post('/api/auth/register', json=data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['first_name'], "O'Brien")


class TestUserRegistrationNegative(BaseTestCase):
    """Negative test cases for user registration"""
    
    def test_register_user_missing_username(self):
        """Test: Register without username
        Expected: 400 Bad Request with validation error
        """
        data = {
            'email': 'test@example.com',
            'password': 'SecurePass123'
        }
        response = self.client.post('/api/auth/register', json=data)
        self.assertEqual(response.status_code, 400)
    
    def test_register_user_missing_email(self):
        """Test: Register without email
        Expected: 400 Bad Request with validation error
        """
        data = {
            'username': 'testuser',
            'password': 'SecurePass123'
        }
        response = self.client.post('/api/auth/register', json=data)
        self.assertEqual(response.status_code, 400)
    
    def test_register_user_missing_password(self):
        """Test: Register without password
        Expected: 400 Bad Request with validation error
        """
        data = {
            'username': 'testuser',
            'email': 'test@example.com'
        }
        response = self.client.post('/api/auth/register', json=data)
        self.assertEqual(response.status_code, 400)
    
    def test_register_user_duplicate_username(self):
        """Test: Register with existing username
        Expected: 400 Bad Request - username already exists
        """
        # Create existing user
        existing_user = self._create_user(username='existinguser')
        
        data = {
            'username': 'existinguser',
            'email': 'different@example.com',
            'password': 'SecurePass123'
        }
        response = self.client.post('/api/auth/register', json=data)
        self.assertEqual(response.status_code, 400)
        error_msg = str(response.json.get('error', '')).lower()
        self.assertTrue('username' in error_msg or 'already exists' in error_msg)
    
    def test_register_user_duplicate_email(self):
        """Test: Register with existing email
        Expected: 400 Bad Request - email already exists
        """
        existing_user = self._create_user(email='existing@example.com')
        
        data = {
            'username': 'differentuser',
            'email': 'existing@example.com',
            'password': 'SecurePass123'
        }
        response = self.client.post('/api/auth/register', json=data)
        self.assertEqual(response.status_code, 400)
    
    def test_register_user_invalid_email_format(self):
        """Test: Register with invalid email format
        Expected: 400 Bad Request - invalid email
        """
        data = {
            'username': 'testuser',
            'email': 'notanemail',
            'password': 'SecurePass123'
        }
        response = self.client.post('/api/auth/register', json=data)
        self.assertEqual(response.status_code, 400)
    
    def test_register_user_password_too_short(self):
        """Test: Register with password less than 8 characters
        Expected: 400 Bad Request - password too short
        """
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'short'  # Less than 8 chars
        }
        response = self.client.post('/api/auth/register', json=data)
        self.assertEqual(response.status_code, 400)
    
    def test_register_user_username_too_short(self):
        """Test: Register with username less than 3 characters
        Expected: 400 Bad Request - username too short
        """
        data = {
            'username': 'ab',  # Less than 3 chars
            'email': 'test@example.com',
            'password': 'SecurePass123'
        }
        response = self.client.post('/api/auth/register', json=data)
        self.assertEqual(response.status_code, 400)
    
    def test_register_user_username_too_long(self):
        """Test: Register with username exceeding 80 characters
        Expected: 400 Bad Request - username too long
        """
        data = {
            'username': 'a' * 81,  # Exceeds 80 chars
            'email': 'test@example.com',
            'password': 'SecurePass123'
        }
        response = self.client.post('/api/auth/register', json=data)
        self.assertEqual(response.status_code, 400)
    
    def test_register_user_invalid_role(self):
        """Test: Register with invalid role value
        Expected: 400 Bad Request - invalid role
        """
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass123',
            'role': 'invalid_role'
        }
        response = self.client.post('/api/auth/register', json=data)
        self.assertEqual(response.status_code, 400)


class TestUserRegistrationEdgeCases(BaseTestCase):
    """Edge cases for user registration"""
    
    def test_register_user_with_unicode_characters(self):
        """Test: Register with Unicode characters in name
        Expected: User created with Unicode characters preserved
        """
        data = {
            'username': 'unicodeuser',
            'email': 'unicode@example.com',
            'password': 'SecurePass123',
            'first_name': 'José',
            'last_name': 'Müller'
        }
        response = self.client.post('/api/auth/register', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['first_name'], 'José')
    
    def test_register_user_with_maximum_length_password(self):
        """Test: Register with very long password (1000 chars)
        Expected: User created successfully
        """
        long_password = 'A' * 1000
        data = {
            'username': 'longpassuser',
            'email': 'longpass@example.com',
            'password': long_password
        }
        response = self.client.post('/api/auth/register', json=data)
        self.assertEqual(response.status_code, 201)
    
    def test_register_user_with_large_expertise_array(self):
        """Test: Register with large expertise areas array
        Expected: User created with all expertise areas stored
        """
        expertise = [f'Area{i}' for i in range(50)]
        data = {
            'username': 'expertuser',
            'email': 'expert@example.com',
            'password': 'SecurePass123',
            'expertise_areas': expertise
        }
        response = self.client.post('/api/auth/register', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.json['expertise_areas']), 50)


class TestUserRegistrationSecurity(BaseTestCase):
    """Security test cases for user registration"""
    
    def test_register_user_password_not_in_response(self):
        """Test: Password should never be returned in API response
        Expected: Password field absent from response
        """
        data = {
            'username': 'secureuser',
            'email': 'secure@example.com',
            'password': 'SecurePass123'
        }
        response = self.client.post('/api/auth/register', json=data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json
        self.assertNotIn('password', response_data)
        self.assertNotIn('password_hash', response_data)
    
    def test_register_user_password_is_hashed(self):
        """Test: Password is stored as hash, not plaintext
        Expected: Password hash stored, plaintext password not accessible
        """
        password = 'SecurePass123'
        data = {
            'username': 'hashtest',
            'email': 'hashtest@example.com',
            'password': password
        }
        response = self.client.post('/api/auth/register', json=data)
        self.assertEqual(response.status_code, 201)
        
        user = User.query.filter_by(username='hashtest').first()
        self.assertIsNotNone(user)
        self.assertNotEqual(user.password_hash, password)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.check_password('wrongpassword'))
    
    def test_register_user_sql_injection_in_username(self):
        """Test: Attempt SQL injection in username field
        Expected: Treated as literal string, no SQL execution
        """
        malicious_username = "admin' OR '1'='1"
        data = {
            'username': malicious_username,
            'email': 'sqltest@example.com',
            'password': 'SecurePass123'
        }
        response = self.client.post('/api/auth/register', json=data)
        # Should either create user with literal string or reject
        self.assertIn(response.status_code, [201, 400])
        if response.status_code == 201:
            user = User.query.filter_by(username=malicious_username).first()
            self.assertIsNotNone(user)


# ============================================================================
# PROFILE UPDATE TESTS
# ============================================================================

class TestProfileUpdatesPositive(BaseTestCase):
    """Positive test cases for profile updates"""
    
    def test_update_own_profile_first_name(self):
        """Test: Update own profile first name
        Expected: Profile updated successfully
        """
        response = self.client.put(
            f'/api/users/{self.test_user.id}',
            headers=self.user_headers,
            json={'first_name': 'UpdatedFirstName'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['first_name'], 'UpdatedFirstName')
    
    def test_update_own_profile_last_name(self):
        """Test: Update own profile last name
        Expected: Profile updated successfully
        """
        response = self.client.put(
            f'/api/users/{self.test_user.id}',
            headers=self.user_headers,
            json={'last_name': 'UpdatedLastName'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['last_name'], 'UpdatedLastName')
    
    def test_update_own_profile_email(self):
        """Test: Update own profile email
        Expected: Email updated successfully
        """
        new_email = 'updatedemail@example.com'
        response = self.client.put(
            f'/api/users/{self.test_user.id}',
            headers=self.user_headers,
            json={'email': new_email}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], new_email)
    
    def test_update_own_profile_multiple_fields(self):
        """Test: Update multiple profile fields at once
        Expected: All fields updated successfully
        """
        response = self.client.put(
            f'/api/users/{self.test_user.id}',
            headers=self.user_headers,
            json={
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'johnsmith@example.com'
            }
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertEqual(response_data['first_name'], 'John')
        self.assertEqual(response_data['last_name'], 'Smith')
        self.assertEqual(response_data['email'], 'johnsmith@example.com')
    
    def test_update_agent_availability_status(self):
        """Test: Agent updates own availability status
        Expected: Availability status updated
        """
        response = self.client.put(
            f'/api/users/{self.test_agent.id}',
            headers=self.agent_headers,
            json={'availability_status': User.AVAILABILITY_BUSY}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['availability_status'], User.AVAILABILITY_BUSY)
    
    def test_admin_update_other_user_profile(self):
        """Test: Admin updates another user's profile
        Expected: Profile updated successfully
        """
        response = self.client.put(
            f'/api/users/{self.test_user.id}',
            headers=self.admin_headers,
            json={'first_name': 'AdminUpdated'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['first_name'], 'AdminUpdated')
    
    def test_admin_update_user_role(self):
        """Test: Admin updates user role
        Expected: Role updated successfully
        """
        response = self.client.put(
            f'/api/users/{self.test_user.id}',
            headers=self.admin_headers,
            json={'role': User.ROLE_AGENT}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['role'], User.ROLE_AGENT)


class TestProfileUpdatesNegative(BaseTestCase):
    """Negative test cases for profile updates"""
    
    def test_update_other_user_profile_as_non_admin(self):
        """Test: Non-admin tries to update another user's profile
        Expected: 403 Forbidden
        """
        other_user = self._create_user()
        response = self.client.put(
            f'/api/users/{other_user.id}',
            headers=self.user_headers,
            json={'first_name': 'ShouldFail'}
        )
        self.assertEqual(response.status_code, 403)
    
    def test_update_profile_with_invalid_email(self):
        """Test: Update profile with invalid email format
        Expected: 400 Bad Request
        """
        response = self.client.put(
            f'/api/users/{self.test_user.id}',
            headers=self.user_headers,
            json={'email': 'notanemail'}
        )
        self.assertEqual(response.status_code, 400)
    
    def test_update_profile_with_duplicate_email(self):
        """Test: Update profile with email already in use
        Expected: 400 Bad Request or validation error
        """
        # Ensure test_user has a unique email first
        unique_email = self.fake.email()
        self.test_user.email = unique_email
        db.session.commit()
        
        # Create another user with a different email
        existing_email = self.fake.email()
        other_user = self._create_user(email=existing_email)
        
        # Try to update test_user's email to existing_email
        response = self.client.put(
            f'/api/users/{self.test_user.id}',
            headers=self.user_headers,
            json={'email': existing_email}
        )
        self.assertEqual(response.status_code, 400)
        error_msg = str(response.json.get('message', '')).lower()
        self.assertIn('email', error_msg)
    
    def test_non_admin_update_role(self):
        """Test: Non-admin tries to update role
        Expected: 403 Forbidden
        """
        response = self.client.put(
            f'/api/users/{self.test_user.id}',
            headers=self.user_headers,
            json={'role': User.ROLE_ADMIN}
        )
        self.assertEqual(response.status_code, 403)
    
    def test_update_profile_without_authentication(self):
        """Test: Update profile without authentication token
        Expected: 401 Unauthorized
        """
        response = self.client.put(
            f'/api/users/{self.test_user.id}',
            json={'first_name': 'Test'}
        )
        self.assertEqual(response.status_code, 401)


class TestProfileUpdatesEdgeCases(BaseTestCase):
    """Edge cases for profile updates"""
    
    def test_update_profile_partial_update(self):
        """Test: Update only one field when multiple exist
        Expected: Only specified field updated, others unchanged
        """
        # Set initial values
        self.client.put(
            f'/api/users/{self.test_user.id}',
            headers=self.user_headers,
            json={
                'first_name': 'Original',
                'last_name': 'Name'
            }
        )
        
        # Update only first_name
        response = self.client.put(
            f'/api/users/{self.test_user.id}',
            headers=self.user_headers,
            json={'first_name': 'Updated'}
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertEqual(response_data['first_name'], 'Updated')
        # last_name should remain unchanged
        self.assertEqual(response_data['last_name'], 'Name')
    
    def test_update_profile_with_special_characters(self):
        """Test: Update profile with special characters
        Expected: Special characters preserved
        """
        response = self.client.put(
            f'/api/users/{self.test_user.id}',
            headers=self.user_headers,
            json={
                'first_name': "O'Brien",
                'last_name': 'van der Berg'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['first_name'], "O'Brien")


class TestProfileUpdatesSecurity(BaseTestCase):
    """Security test cases for profile updates"""
    
    def test_update_profile_authorization_check(self):
        """Test: Verify authorization check prevents unauthorized updates
        Expected: 403 Forbidden for unauthorized access
        """
        other_user = self._create_user()
        response = self.client.put(
            f'/api/users/{other_user.id}',
            headers=self.user_headers,
            json={'email': 'hacked@example.com'}
        )
        self.assertEqual(response.status_code, 403)
    
    def test_admin_cannot_remove_own_admin_role(self):
        """Test: Admin cannot remove own admin role
        Expected: 400 Bad Request
        """
        response = self.client.put(
            f'/api/users/{self.test_admin.id}',
            headers=self.admin_headers,
            json={'role': User.ROLE_CUSTOMER}
        )
        self.assertEqual(response.status_code, 400)
        error_msg = str(response.json.get('message', '')).lower()
        self.assertIn('admin role', error_msg)
    
    def test_admin_cannot_deactivate_own_account(self):
        """Test: Admin cannot deactivate own account
        Expected: 400 Bad Request
        """
        response = self.client.put(
            f'/api/users/{self.test_admin.id}',
            headers=self.admin_headers,
            json={'is_active': False}
        )
        self.assertEqual(response.status_code, 400)
        error_msg = str(response.json.get('message', '')).lower()
        self.assertIn('deactivate', error_msg)


# ============================================================================
# PASSWORD CHANGE TESTS
# ============================================================================

class TestPasswordChangesPositive(BaseTestCase):
    """Positive test cases for password changes"""
    
    def test_change_password_success(self):
        """Test: User changes own password successfully
        Expected: Password updated, can login with new password
        """
        old_password = 'testpassword123'
        new_password = 'NewSecurePass123'
        
        # Change password
        response = self.client.put(
            f'/api/users/{self.test_user.id}',
            headers=self.user_headers,
            json={'password': new_password}
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify old password no longer works
        login_old = self.client.post('/api/auth/login', json={
            'username': self.test_user.username,
            'password': old_password
        })
        self.assertEqual(login_old.status_code, 401)
        
        # Verify new password works
        login_new = self.client.post('/api/auth/login', json={
            'username': self.test_user.username,
            'password': new_password
        })
        self.assertEqual(login_new.status_code, 200)
    
    def test_change_password_with_special_characters(self):
        """Test: Change password with special characters
        Expected: Password updated successfully
        """
        special_password = 'P@ssw0rd!#$%^&*()'
        response = self.client.put(
            f'/api/users/{self.test_user.id}',
            headers=self.user_headers,
            json={'password': special_password}
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify login works
        login_response = self.client.post('/api/auth/login', json={
            'username': self.test_user.username,
            'password': special_password
        })
        self.assertEqual(login_response.status_code, 200)
    
    def test_admin_change_user_password(self):
        """Test: Admin changes another user's password
        Expected: Password updated successfully
        """
        new_password = 'AdminChangedPass123'
        response = self.client.put(
            f'/api/users/{self.test_user.id}',
            headers=self.admin_headers,
            json={'password': new_password}
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify new password works
        login_response = self.client.post('/api/auth/login', json={
            'username': self.test_user.username,
            'password': new_password
        })
        self.assertEqual(login_response.status_code, 200)


class TestPasswordChangesNegative(BaseTestCase):
    """Negative test cases for password changes"""
    
    def test_change_password_too_short(self):
        """Test: Change password to less than 8 characters
        Expected: 400 Bad Request
        """
        response = self.client.put(
            f'/api/users/{self.test_user.id}',
            headers=self.user_headers,
            json={'password': 'short'}  # Less than 8 chars
        )
        self.assertEqual(response.status_code, 400)
    
    def test_change_password_without_authentication(self):
        """Test: Change password without authentication
        Expected: 401 Unauthorized
        """
        response = self.client.put(
            f'/api/users/{self.test_user.id}',
            json={'password': 'NewPassword123'}
        )
        self.assertEqual(response.status_code, 401)
    
    def test_change_other_user_password_as_non_admin(self):
        """Test: Non-admin tries to change another user's password
        Expected: 403 Forbidden
        """
        other_user = self._create_user()
        response = self.client.put(
            f'/api/users/{other_user.id}',
            headers=self.user_headers,
            json={'password': 'HackedPassword123'}
        )
        self.assertEqual(response.status_code, 403)


class TestPasswordChangesSecurity(BaseTestCase):
    """Security test cases for password changes"""
    
    def test_password_not_returned_in_response(self):
        """Test: Password never returned in API response
        Expected: Password field absent from response
        """
        response = self.client.put(
            f'/api/users/{self.test_user.id}',
            headers=self.user_headers,
            json={'password': 'NewSecurePass123'}
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertNotIn('password', response_data)
        self.assertNotIn('password_hash', response_data)
    
    def test_password_is_hashed(self):
        """Test: Password is stored as hash, not plaintext
        Expected: Password hash stored, plaintext not accessible
        """
        new_password = 'NewSecurePass123'
        response = self.client.put(
            f'/api/users/{self.test_user.id}',
            headers=self.user_headers,
            json={'password': new_password}
        )
        self.assertEqual(response.status_code, 200)
        
        user = User.query.get(self.test_user.id)
        self.assertNotEqual(user.password_hash, new_password)
        self.assertTrue(user.check_password(new_password))


# ============================================================================
# ACCOUNT DELETION TESTS
# ============================================================================

class TestAccountDeletionPositive(BaseTestCase):
    """Positive test cases for account deletion"""
    
    def test_delete_own_account(self):
        """Test: User deletes own account
        Expected: Account deleted, 204 No Content
        """
        user = self._create_user(username='todelete', email='todelete@example.com')
        user_id = user.id
        
        # Login as user
        login_response = self.client.post('/api/auth/login', json={
            'username': 'todelete',
            'password': 'SecurePass123'
        })
        token = login_response.json['access_token']
        user_headers = {'Authorization': f'Bearer {token}'}
        
        # Delete account
        response = self.client.delete(f'/api/users/{user_id}', headers=user_headers)
        self.assertEqual(response.status_code, 204)
        
        # Verify user is deleted
        deleted_user = User.query.get(user_id)
        self.assertIsNone(deleted_user)
    
    def test_admin_delete_user_account(self):
        """Test: Admin deletes another user's account
        Expected: Account deleted successfully
        """
        user = self._create_user()
        user_id = user.id
        
        # Delete as admin
        response = self.client.delete(f'/api/users/{user_id}', headers=self.admin_headers)
        self.assertEqual(response.status_code, 204)
        
        # Verify user is deleted
        deleted_user = User.query.get(user_id)
        self.assertIsNone(deleted_user)


class TestAccountDeletionNegative(BaseTestCase):
    """Negative test cases for account deletion"""
    
    def test_delete_other_user_account_as_non_admin(self):
        """Test: Non-admin tries to delete another user's account
        Expected: 403 Forbidden
        """
        other_user = self._create_user()
        response = self.client.delete(f'/api/users/{other_user.id}', headers=self.user_headers)
        self.assertEqual(response.status_code, 403)
    
    def test_delete_nonexistent_account(self):
        """Test: Delete non-existent account
        Expected: 404 Not Found
        """
        response = self.client.delete('/api/users/99999', headers=self.admin_headers)
        self.assertEqual(response.status_code, 404)
    
    def test_delete_account_without_authentication(self):
        """Test: Delete account without authentication
        Expected: 401 Unauthorized
        """
        response = self.client.delete(f'/api/users/{self.test_user.id}')
        self.assertEqual(response.status_code, 401)


class TestAccountDeletionSecurity(BaseTestCase):
    """Security test cases for account deletion"""
    
    def test_delete_account_authorization_check(self):
        """Test: Verify authorization prevents unauthorized deletion
        Expected: 403 Forbidden for unauthorized access
        """
        other_user = self._create_user()
        response = self.client.delete(f'/api/users/{other_user.id}', headers=self.user_headers)
        self.assertEqual(response.status_code, 403)
        
        # Verify user still exists
        self.assertIsNotNone(User.query.get(other_user.id))


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestUserProfileIntegration(BaseTestCase):
    """Integration test cases combining multiple operations"""
    
    def test_complete_user_lifecycle(self):
        """Test: Complete user lifecycle - register, update, change password, delete
        Expected: All operations succeed in sequence
        """
        # 1. Register
        register_data = {
            'username': 'lifecycle',
            'email': 'lifecycle@example.com',
            'password': 'InitialPass123',
            'first_name': 'Initial',
            'last_name': 'Name'
        }
        register_response = self.client.post('/api/auth/register', json=register_data)
        self.assertEqual(register_response.status_code, 201)
        user_id = register_response.json['id']
        
        # 2. Login
        login_response = self.client.post('/api/auth/login', json={
            'username': 'lifecycle',
            'password': 'InitialPass123'
        })
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # 3. Update profile
        update_response = self.client.put(
            f'/api/users/{user_id}',
            headers=headers,
            json={
                'first_name': 'Updated',
                'last_name': 'Name'
            }
        )
        self.assertEqual(update_response.status_code, 200)
        
        # 4. Change password
        password_response = self.client.put(
            f'/api/users/{user_id}',
            headers=headers,
            json={'password': 'NewPassword123'}
        )
        self.assertEqual(password_response.status_code, 200)
        
        # 5. Login with new password
        new_login = self.client.post('/api/auth/login', json={
            'username': 'lifecycle',
            'password': 'NewPassword123'
        })
        self.assertEqual(new_login.status_code, 200)
        new_token = new_login.json['access_token']
        new_headers = {'Authorization': f'Bearer {new_token}'}
        
        # 6. Delete account
        delete_response = self.client.delete(f'/api/users/{user_id}', headers=new_headers)
        self.assertEqual(delete_response.status_code, 204)
        
        # 7. Verify deletion
        self.assertIsNone(User.query.get(user_id))


# ============================================================================
# TEST SUITE RUNNER
# ============================================================================

def suite():
    """Create test suite"""
    test_suite = unittest.TestSuite()
    
    # Registration tests
    test_suite.addTest(unittest.makeSuite(TestUserRegistrationPositive))
    test_suite.addTest(unittest.makeSuite(TestUserRegistrationNegative))
    test_suite.addTest(unittest.makeSuite(TestUserRegistrationEdgeCases))
    test_suite.addTest(unittest.makeSuite(TestUserRegistrationSecurity))
    
    # Profile update tests
    test_suite.addTest(unittest.makeSuite(TestProfileUpdatesPositive))
    test_suite.addTest(unittest.makeSuite(TestProfileUpdatesNegative))
    test_suite.addTest(unittest.makeSuite(TestProfileUpdatesEdgeCases))
    test_suite.addTest(unittest.makeSuite(TestProfileUpdatesSecurity))
    
    # Password change tests
    test_suite.addTest(unittest.makeSuite(TestPasswordChangesPositive))
    test_suite.addTest(unittest.makeSuite(TestPasswordChangesNegative))
    test_suite.addTest(unittest.makeSuite(TestPasswordChangesSecurity))
    
    # Account deletion tests
    test_suite.addTest(unittest.makeSuite(TestAccountDeletionPositive))
    test_suite.addTest(unittest.makeSuite(TestAccountDeletionNegative))
    test_suite.addTest(unittest.makeSuite(TestAccountDeletionSecurity))
    
    # Integration tests
    test_suite.addTest(unittest.makeSuite(TestUserProfileIntegration))
    
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
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*70}")
