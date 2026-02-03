"""
Test Helper Utilities for User Profile Management Tests

This module provides helper functions and mock data generators
for use in unittest test cases.
"""

from faker import Faker
from app.models import User
from datetime import datetime
import random

fake = Faker()


class MockDataGenerator:
    """Generate mock data for testing"""
    
    @staticmethod
    def generate_user_data(**overrides):
        """Generate mock user registration data
        
        Args:
            **overrides: Fields to override in generated data
            
        Returns:
            dict: User registration data
        """
        default_data = {
            'username': fake.user_name(),
            'email': fake.email(),
            'password': 'SecurePass123',
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'role': User.ROLE_CUSTOMER
        }
        default_data.update(overrides)
        return default_data
    
    @staticmethod
    def generate_profile_update_data(**overrides):
        """Generate mock profile update data
        
        Args:
            **overrides: Fields to override in generated data
            
        Returns:
            dict: Profile update data
        """
        default_data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email()
        }
        default_data.update(overrides)
        return default_data
    
    @staticmethod
    def generate_invalid_user_data():
        """Generate invalid user data for negative testing
        
        Returns:
            list: List of invalid data dictionaries
        """
        return [
            # Missing required fields
            {'email': 'test@example.com', 'password': 'SecurePass123'},  # Missing username
            {'username': 'testuser', 'password': 'SecurePass123'},  # Missing email
            {'username': 'testuser', 'email': 'test@example.com'},  # Missing password
            
            # Invalid formats
            {'username': 'ab', 'email': 'test@example.com', 'password': 'SecurePass123'},  # Username too short
            {'username': 'a' * 81, 'email': 'test@example.com', 'password': 'SecurePass123'},  # Username too long
            {'username': 'testuser', 'email': 'notanemail', 'password': 'SecurePass123'},  # Invalid email
            {'username': 'testuser', 'email': 'test@example.com', 'password': 'short'},  # Password too short
            
            # Invalid values
            {'username': 'testuser', 'email': 'test@example.com', 'password': 'SecurePass123', 'role': 'invalid_role'},
            {'username': 'testuser', 'email': 'test@example.com', 'password': 'SecurePass123', 
             'availability_status': 'invalid_status'}
        ]
    
    @staticmethod
    def generate_edge_case_data():
        """Generate edge case data for testing
        
        Returns:
            dict: Edge case data scenarios
        """
        return {
            'unicode_names': {
                'first_name': 'José',
                'last_name': 'Müller'
            },
            'special_characters': {
                'first_name': "O'Brien",
                'last_name': 'van der Berg'
            },
            'maximum_length_username': {
                'username': 'a' * 80
            },
            'maximum_length_password': {
                'password': 'A' * 1000
            },
            'large_expertise_array': {
                'expertise_areas': [f'Area{i}' for i in range(50)]
            },
            'empty_strings': {
                'first_name': '',
                'last_name': ''
            },
            'whitespace_only': {
                'username': '   whitespaceuser   ',
                'email': '   whitespace@example.com   '
            }
        }
    
    @staticmethod
    def generate_security_test_data():
        """Generate security test data (SQL injection, XSS, etc.)
        
        Returns:
            dict: Security test data scenarios
        """
        return {
            'sql_injection_username': "admin' OR '1'='1",
            'sql_injection_email': "admin' OR '1'='1@example.com",
            'xss_payload': '<script>alert("XSS")</script>',
            'xss_name': '<img src=x onerror=alert(1)>',
            'command_injection': '; rm -rf /',
            'path_traversal': '../../../etc/passwd',
            'null_byte': 'test\x00user'
        }


class TestUserFactory:
    """Factory for creating test users"""
    
    @staticmethod
    def create_customer(db_session, **overrides):
        """Create a test customer user
        
        Args:
            db_session: Database session
            **overrides: User attributes to override
            
        Returns:
            User: Created user instance
        """
        user_data = MockDataGenerator.generate_user_data(
            role=User.ROLE_CUSTOMER,
            **overrides
        )
        user = User(**{k: v for k, v in user_data.items() if k != 'password'})
        user.set_password(user_data['password'])
        db_session.add(user)
        db_session.commit()
        return user
    
    @staticmethod
    def create_admin(db_session, **overrides):
        """Create a test admin user
        
        Args:
            db_session: Database session
            **overrides: User attributes to override
            
        Returns:
            User: Created admin user instance
        """
        user_data = MockDataGenerator.generate_user_data(
            username='admin',
            email='admin@test.com',
            role=User.ROLE_ADMIN,
            **overrides
        )
        user = User(**{k: v for k, v in user_data.items() if k != 'password'})
        user.is_admin = True
        user.set_password(user_data['password'])
        db_session.add(user)
        db_session.commit()
        return user
    
    @staticmethod
    def create_agent(db_session, **overrides):
        """Create a test agent user
        
        Args:
            db_session: Database session
            **overrides: User attributes to override
            
        Returns:
            User: Created agent user instance
        """
        user_data = MockDataGenerator.generate_user_data(
            role=User.ROLE_AGENT,
            availability_status=User.AVAILABILITY_AVAILABLE,
            **overrides
        )
        user = User(**{k: v for k, v in user_data.items() if k != 'password'})
        user.set_password(user_data['password'])
        db_session.add(user)
        db_session.commit()
        return user
    
    @staticmethod
    def create_multiple_users(db_session, count=5, role=User.ROLE_CUSTOMER):
        """Create multiple test users
        
        Args:
            db_session: Database session
            count: Number of users to create
            role: Role for all users
            
        Returns:
            list: List of created user instances
        """
        users = []
        for i in range(count):
            user = TestUserFactory.create_customer(db_session, role=role)
            users.append(user)
        return users


class AssertionHelpers:
    """Helper methods for common test assertions"""
    
    @staticmethod
    def assert_user_response_structure(response_data):
        """Assert that user response has correct structure
        
        Args:
            response_data: Response JSON data
        """
        required_fields = ['id', 'username', 'email', 'role', 'is_active']
        for field in required_fields:
            assert field in response_data, f"Missing required field: {field}"
        
        # Password should never be in response
        assert 'password' not in response_data, "Password should not be in response"
        assert 'password_hash' not in response_data, "Password hash should not be in response"
    
    @staticmethod
    def assert_error_response(response, expected_status, error_keywords=None):
        """Assert error response structure
        
        Args:
            response: HTTP response object
            expected_status: Expected HTTP status code
            error_keywords: List of keywords that should appear in error message
        """
        assert response.status_code == expected_status, \
            f"Expected status {expected_status}, got {response.status_code}"
        
        if error_keywords:
            error_msg = str(response.json.get('error', '') or response.json.get('message', '')).lower()
            for keyword in error_keywords:
                assert keyword.lower() in error_msg, \
                    f"Error message should contain '{keyword}'"
    
    @staticmethod
    def assert_password_security(user, password):
        """Assert password is properly secured
        
        Args:
            user: User instance
            password: Plaintext password
        """
        assert user.password_hash != password, "Password should be hashed"
        assert user.check_password(password), "Password check should succeed"
        assert not user.check_password('wrongpassword'), "Wrong password should fail"


class TestDataCleanup:
    """Helper for cleaning up test data"""
    
    @staticmethod
    def cleanup_users(db_session, user_ids):
        """Delete users by IDs
        
        Args:
            db_session: Database session
            user_ids: List of user IDs to delete
        """
        for user_id in user_ids:
            user = User.query.get(user_id)
            if user:
                db_session.delete(user)
        db_session.commit()
    
    @staticmethod
    def cleanup_all_test_users(db_session, prefix='test'):
        """Delete all users with username starting with prefix
        
        Args:
            db_session: Database session
            prefix: Username prefix to match
        """
        users = User.query.filter(User.username.like(f'{prefix}%')).all()
        for user in users:
            db_session.delete(user)
        db_session.commit()


# Example usage in tests:
"""
from tests.test_helpers import MockDataGenerator, TestUserFactory, AssertionHelpers

class MyTestCase(BaseTestCase):
    def test_example(self):
        # Generate mock data
        user_data = MockDataGenerator.generate_user_data(
            username='testuser',
            email='test@example.com'
        )
        
        # Create test user
        user = TestUserFactory.create_customer(self.db_session)
        
        # Make request
        response = self.client.post('/api/auth/register', json=user_data)
        
        # Assert response
        AssertionHelpers.assert_user_response_structure(response.json)
        AssertionHelpers.assert_password_security(user, 'password123')
"""
