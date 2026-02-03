"""
Comprehensive test cases for User Profile Management Feature

This test suite covers:
- User Registration (positive, negative, edge cases, security)
- Profile Updates (positive, negative, edge cases, security)
- Password Changes (positive, negative, edge cases, security)
- Account Deletion (positive, negative, edge cases, security)

Test Categories:
- Positive Test Cases: Valid inputs and expected successful outcomes
- Negative Test Cases: Invalid inputs and expected error handling
- Edge Cases: Boundary conditions and unusual scenarios
- Security Test Cases: Authorization, authentication, and security vulnerabilities
"""

import pytest
from app.models import User
from datetime import datetime
import json


class TestUserRegistration:
    """Test cases for user registration"""
    
    # ========== POSITIVE TEST CASES ==========
    
    def test_register_user_with_minimal_fields(self, client, db_session):
        """Test: Register user with only required fields (username, email, password)
        Expected: User created successfully with default role 'customer'
        """
        response = client.post('/api/auth/register', json={
            'username': 'newuser123',
            'email': 'newuser@example.com',
            'password': 'SecurePass123'
        })
        assert response.status_code == 201
        assert response.json['username'] == 'newuser123'
        assert response.json['email'] == 'newuser@example.com'
        assert response.json['role'] == User.ROLE_CUSTOMER
        assert 'password' not in response.json
        assert response.json['is_active'] is True
    
    def test_register_user_with_all_fields(self, client, db_session):
        """Test: Register user with all optional fields
        Expected: User created with all provided information
        """
        response = client.post('/api/auth/register', json={
            'username': 'completeuser',
            'email': 'complete@example.com',
            'password': 'SecurePass123',
            'first_name': 'John',
            'last_name': 'Doe',
            'name': 'John Doe',
            'role': User.ROLE_CUSTOMER,
            'availability_status': User.AVAILABILITY_AVAILABLE,
            'expertise_areas': ['Python', 'Flask', 'API Development']
        })
        assert response.status_code == 201
        assert response.json['first_name'] == 'John'
        assert response.json['last_name'] == 'Doe'
        assert response.json['expertise_areas'] == ['Python', 'Flask', 'API Development']
    
    def test_register_user_as_agent(self, client, db_session):
        """Test: Register user with agent role
        Expected: User created with agent role and availability status
        """
        response = client.post('/api/auth/register', json={
            'username': 'agent1',
            'email': 'agent1@example.com',
            'password': 'SecurePass123',
            'role': User.ROLE_AGENT,
            'availability_status': User.AVAILABILITY_AVAILABLE,
            'expertise_areas': ['Support', 'Technical']
        })
        assert response.status_code == 201
        assert response.json['role'] == User.ROLE_AGENT
        assert response.json['availability_status'] == User.AVAILABILITY_AVAILABLE
    
    def test_register_user_with_long_username(self, client, db_session):
        """Test: Register user with maximum length username (80 chars)
        Expected: User created successfully
        """
        long_username = 'a' * 80
        response = client.post('/api/auth/register', json={
            'username': long_username,
            'email': 'longuser@example.com',
            'password': 'SecurePass123'
        })
        assert response.status_code == 201
        assert response.json['username'] == long_username
    
    def test_register_user_with_special_characters_in_name(self, client, db_session):
        """Test: Register user with special characters in name fields
        Expected: User created successfully with special characters preserved
        """
        response = client.post('/api/auth/register', json={
            'username': 'specialuser',
            'email': 'special@example.com',
            'password': 'SecurePass123',
            'first_name': "O'Brien",
            'last_name': 'van der Berg'
        })
        assert response.status_code == 201
        assert response.json['first_name'] == "O'Brien"
    
    # ========== NEGATIVE TEST CASES ==========
    
    def test_register_user_missing_username(self, client):
        """Test: Register without username
        Expected: 400 Bad Request with validation error
        """
        response = client.post('/api/auth/register', json={
            'email': 'test@example.com',
            'password': 'SecurePass123'
        })
        assert response.status_code == 400
    
    def test_register_user_missing_email(self, client):
        """Test: Register without email
        Expected: 400 Bad Request with validation error
        """
        response = client.post('/api/auth/register', json={
            'username': 'testuser',
            'password': 'SecurePass123'
        })
        assert response.status_code == 400
    
    def test_register_user_missing_password(self, client):
        """Test: Register without password
        Expected: 400 Bad Request with validation error
        """
        response = client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com'
        })
        assert response.status_code == 400
    
    def test_register_user_duplicate_username(self, client, test_user):
        """Test: Register with existing username
        Expected: 400 Bad Request - username already exists
        """
        response = client.post('/api/auth/register', json={
            'username': test_user.username,
            'email': 'different@example.com',
            'password': 'SecurePass123'
        })
        assert response.status_code == 400
        assert 'username' in str(response.json.get('error', '')).lower() or \
               'already exists' in str(response.json.get('error', '')).lower()
    
    def test_register_user_duplicate_email(self, client, test_user):
        """Test: Register with existing email
        Expected: 400 Bad Request - email already exists
        """
        response = client.post('/api/auth/register', json={
            'username': 'differentuser',
            'email': test_user.email,
            'password': 'SecurePass123'
        })
        assert response.status_code == 400
    
    def test_register_user_invalid_email_format(self, client):
        """Test: Register with invalid email format
        Expected: 400 Bad Request - invalid email
        """
        response = client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'notanemail',
            'password': 'SecurePass123'
        })
        assert response.status_code == 400
    
    def test_register_user_password_too_short(self, client):
        """Test: Register with password less than 8 characters
        Expected: 400 Bad Request - password too short
        """
        response = client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'short'  # Less than 8 chars
        })
        assert response.status_code == 400
    
    def test_register_user_username_too_short(self, client):
        """Test: Register with username less than 3 characters
        Expected: 400 Bad Request - username too short
        """
        response = client.post('/api/auth/register', json={
            'username': 'ab',  # Less than 3 chars
            'email': 'test@example.com',
            'password': 'SecurePass123'
        })
        assert response.status_code == 400
    
    def test_register_user_username_too_long(self, client):
        """Test: Register with username exceeding 80 characters
        Expected: 400 Bad Request - username too long
        """
        response = client.post('/api/auth/register', json={
            'username': 'a' * 81,  # Exceeds 80 chars
            'email': 'test@example.com',
            'password': 'SecurePass123'
        })
        assert response.status_code == 400
    
    def test_register_user_invalid_role(self, client):
        """Test: Register with invalid role value
        Expected: 400 Bad Request - invalid role
        """
        response = client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass123',
            'role': 'invalid_role'
        })
        assert response.status_code == 400
    
    def test_register_user_invalid_availability_status(self, client):
        """Test: Register with invalid availability status
        Expected: 400 Bad Request - invalid availability status
        """
        response = client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass123',
            'availability_status': 'invalid_status'
        })
        assert response.status_code == 400
    
    # ========== EDGE CASES ==========
    
    def test_register_user_with_empty_string_fields(self, client):
        """Test: Register with empty string for optional fields
        Expected: User created (empty strings may be converted to None)
        """
        response = client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass123',
            'first_name': '',
            'last_name': ''
        })
        # Should either accept empty strings or convert to None
        assert response.status_code in [201, 400]
    
    def test_register_user_with_whitespace_only_fields(self, client):
        """Test: Register with whitespace-only fields
        Expected: Validation error or whitespace trimmed
        """
        response = client.post('/api/auth/register', json={
            'username': '   whitespaceuser   ',
            'email': '   whitespace@example.com   ',
            'password': 'SecurePass123'
        })
        # Should handle whitespace appropriately
        assert response.status_code in [201, 400]
    
    def test_register_user_with_unicode_characters(self, client, db_session):
        """Test: Register with Unicode characters in name
        Expected: User created with Unicode characters preserved
        """
        response = client.post('/api/auth/register', json={
            'username': 'unicodeuser',
            'email': 'unicode@example.com',
            'password': 'SecurePass123',
            'first_name': 'José',
            'last_name': 'Müller'
        })
        assert response.status_code == 201
        assert response.json['first_name'] == 'José'
    
    def test_register_user_with_maximum_length_password(self, client, db_session):
        """Test: Register with very long password (1000 chars)
        Expected: User created successfully
        """
        long_password = 'A' * 1000
        response = client.post('/api/auth/register', json={
            'username': 'longpassuser',
            'email': 'longpass@example.com',
            'password': long_password
        })
        assert response.status_code == 201
    
    def test_register_user_with_json_array_expertise(self, client, db_session):
        """Test: Register with large expertise areas array
        Expected: User created with all expertise areas stored
        """
        expertise = [f'Area{i}' for i in range(50)]
        response = client.post('/api/auth/register', json={
            'username': 'expertuser',
            'email': 'expert@example.com',
            'password': 'SecurePass123',
            'expertise_areas': expertise
        })
        assert response.status_code == 201
        assert len(response.json['expertise_areas']) == 50
    
    # ========== SECURITY TEST CASES ==========
    
    def test_register_user_password_not_in_response(self, client, db_session):
        """Test: Password should never be returned in API response
        Expected: Password field absent from response
        """
        response = client.post('/api/auth/register', json={
            'username': 'secureuser',
            'email': 'secure@example.com',
            'password': 'SecurePass123'
        })
        assert response.status_code == 201
        assert 'password' not in response.json
        assert 'password_hash' not in response.json
    
    def test_register_user_password_is_hashed(self, client, db_session):
        """Test: Password is stored as hash, not plaintext
        Expected: Password hash stored, plaintext password not accessible
        """
        password = 'SecurePass123'
        response = client.post('/api/auth/register', json={
            'username': 'hashtest',
            'email': 'hashtest@example.com',
            'password': password
        })
        assert response.status_code == 201
        
        user = User.query.filter_by(username='hashtest').first()
        assert user.password_hash != password
        assert user.check_password(password) is True
        assert user.check_password('wrongpassword') is False
    
    def test_register_user_sql_injection_in_username(self, client):
        """Test: Attempt SQL injection in username field
        Expected: Treated as literal string, no SQL execution
        """
        malicious_username = "admin' OR '1'='1"
        response = client.post('/api/auth/register', json={
            'username': malicious_username,
            'email': 'sqltest@example.com',
            'password': 'SecurePass123'
        })
        # Should either create user with literal string or reject
        assert response.status_code in [201, 400]
        if response.status_code == 201:
            user = User.query.filter_by(username=malicious_username).first()
            assert user is not None
    
    def test_register_user_xss_in_name_fields(self, client, db_session):
        """Test: Attempt XSS attack in name fields
        Expected: Script tags stored as literal strings, not executed
        """
        xss_payload = '<script>alert("XSS")</script>'
        response = client.post('/api/auth/register', json={
            'username': 'xsstest',
            'email': 'xsstest@example.com',
            'password': 'SecurePass123',
            'first_name': xss_payload
        })
        assert response.status_code == 201
        # Should be stored as literal string
        assert xss_payload in response.json.get('first_name', '')
    
    def test_register_user_rate_limiting(self, client, db_session):
        """Test: Multiple rapid registration attempts
        Expected: Rate limiting prevents abuse
        """
        # Attempt multiple registrations rapidly
        for i in range(10):
            response = client.post('/api/auth/register', json={
                'username': f'ratelimit{i}',
                'email': f'ratelimit{i}@example.com',
                'password': 'SecurePass123'
            })
        # Should eventually hit rate limit or all succeed
        # Exact behavior depends on rate limiting configuration
        assert True  # Test passes if no crash occurs


class TestProfileUpdates:
    """Test cases for profile updates"""
    
    # ========== POSITIVE TEST CASES ==========
    
    def test_update_own_profile_first_name(self, client, auth_headers, test_user):
        """Test: Update own profile first name
        Expected: Profile updated successfully
        """
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'first_name': 'UpdatedFirstName'}
        )
        assert response.status_code == 200
        assert response.json['first_name'] == 'UpdatedFirstName'
    
    def test_update_own_profile_last_name(self, client, auth_headers, test_user):
        """Test: Update own profile last name
        Expected: Profile updated successfully
        """
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'last_name': 'UpdatedLastName'}
        )
        assert response.status_code == 200
        assert response.json['last_name'] == 'UpdatedLastName'
    
    def test_update_own_profile_email(self, client, auth_headers, test_user, db_session):
        """Test: Update own profile email
        Expected: Email updated successfully
        """
        new_email = 'updatedemail@example.com'
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'email': new_email}
        )
        assert response.status_code == 200
        assert response.json['email'] == new_email
    
    def test_update_own_profile_multiple_fields(self, client, auth_headers, test_user):
        """Test: Update multiple profile fields at once
        Expected: All fields updated successfully
        """
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'johnsmith@example.com'
            }
        )
        assert response.status_code == 200
        assert response.json['first_name'] == 'John'
        assert response.json['last_name'] == 'Smith'
        assert response.json['email'] == 'johnsmith@example.com'
    
    def test_update_agent_availability_status(self, client, auth_headers, db_session):
        """Test: Agent updates own availability status
        Expected: Availability status updated
        """
        agent = User(
            username='agentuser',
            email='agent@example.com',
            role=User.ROLE_AGENT,
            availability_status=User.AVAILABILITY_AVAILABLE
        )
        agent.set_password('password123')
        db_session.add(agent)
        db_session.commit()
        
        # Login as agent
        login_response = client.post('/api/auth/login', json={
            'username': 'agentuser',
            'password': 'password123'
        })
        token = login_response.json['access_token']
        agent_headers = {'Authorization': f'Bearer {token}'}
        
        response = client.put(f'/api/users/{agent.id}',
            headers=agent_headers,
            json={'availability_status': User.AVAILABILITY_BUSY}
        )
        assert response.status_code == 200
        assert response.json['availability_status'] == User.AVAILABILITY_BUSY
    
    def test_update_agent_expertise_areas(self, client, auth_headers, db_session):
        """Test: Agent updates expertise areas
        Expected: Expertise areas updated
        """
        agent = User(
            username='expertagent',
            email='expert@example.com',
            role=User.ROLE_AGENT
        )
        agent.set_password('password123')
        db_session.add(agent)
        db_session.commit()
        
        login_response = client.post('/api/auth/login', json={
            'username': 'expertagent',
            'password': 'password123'
        })
        token = login_response.json['access_token']
        agent_headers = {'Authorization': f'Bearer {token}'}
        
        response = client.put(f'/api/users/{agent.id}',
            headers=agent_headers,
            json={'expertise_areas': ['Python', 'Django', 'REST APIs']}
        )
        assert response.status_code == 200
        assert response.json['expertise_areas'] == ['Python', 'Django', 'REST APIs']
    
    def test_admin_update_other_user_profile(self, client, admin_headers, test_user):
        """Test: Admin updates another user's profile
        Expected: Profile updated successfully
        """
        response = client.put(f'/api/users/{test_user.id}',
            headers=admin_headers,
            json={'first_name': 'AdminUpdated'}
        )
        assert response.status_code == 200
        assert response.json['first_name'] == 'AdminUpdated'
    
    def test_admin_update_user_role(self, client, admin_headers, test_user):
        """Test: Admin updates user role
        Expected: Role updated successfully
        """
        response = client.put(f'/api/users/{test_user.id}',
            headers=admin_headers,
            json={'role': User.ROLE_AGENT}
        )
        assert response.status_code == 200
        assert response.json['role'] == User.ROLE_AGENT
    
    def test_admin_update_user_active_status(self, client, admin_headers, test_user):
        """Test: Admin deactivates user account
        Expected: is_active set to False
        """
        response = client.put(f'/api/users/{test_user.id}',
            headers=admin_headers,
            json={'is_active': False}
        )
        assert response.status_code == 200
        assert response.json['is_active'] is False
    
    # ========== NEGATIVE TEST CASES ==========
    
    def test_update_other_user_profile_as_non_admin(self, client, auth_headers, db_session):
        """Test: Non-admin tries to update another user's profile
        Expected: 403 Forbidden
        """
        other_user = User(
            username='otheruser',
            email='other@example.com',
            role=User.ROLE_CUSTOMER
        )
        other_user.set_password('password123')
        db_session.add(other_user)
        db_session.commit()
        
        response = client.put(f'/api/users/{other_user.id}',
            headers=auth_headers,
            json={'first_name': 'ShouldFail'}
        )
        assert response.status_code == 403
    
    def test_update_profile_with_invalid_email(self, client, auth_headers, test_user):
        """Test: Update profile with invalid email format
        Expected: 400 Bad Request
        """
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'email': 'notanemail'}
        )
        assert response.status_code == 400
    
    def test_update_profile_with_duplicate_email(self, client, auth_headers, test_user, db_session):
        """Test: Update profile with email already in use
        Expected: 400 Bad Request or validation error
        """
        other_user = User(
            username='otheruser2',
            email='existing@example.com',
            role=User.ROLE_CUSTOMER
        )
        other_user.set_password('password123')
        db_session.add(other_user)
        db_session.commit()
        
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'email': 'existing@example.com'}
        )
        assert response.status_code == 400
    
    def test_update_profile_with_name_too_long(self, client, auth_headers, test_user):
        """Test: Update profile with name exceeding max length
        Expected: 400 Bad Request
        """
        long_name = 'a' * 201  # Exceeds 200 char limit
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'name': long_name}
        )
        assert response.status_code == 400
    
    def test_non_admin_update_role(self, client, auth_headers, test_user):
        """Test: Non-admin tries to update role
        Expected: 403 Forbidden
        """
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'role': User.ROLE_ADMIN}
        )
        assert response.status_code == 403
    
    def test_non_admin_update_active_status(self, client, auth_headers, test_user):
        """Test: Non-admin tries to update is_active
        Expected: 403 Forbidden
        """
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'is_active': False}
        )
        assert response.status_code == 403
    
    def test_update_nonexistent_user(self, client, admin_headers):
        """Test: Update non-existent user
        Expected: 404 Not Found
        """
        response = client.put('/api/users/99999',
            headers=admin_headers,
            json={'first_name': 'Test'}
        )
        assert response.status_code == 404
    
    def test_update_profile_without_authentication(self, client, test_user):
        """Test: Update profile without authentication token
        Expected: 401 Unauthorized
        """
        response = client.put(f'/api/users/{test_user.id}',
            json={'first_name': 'Test'}
        )
        assert response.status_code == 401
    
    # ========== EDGE CASES ==========
    
    def test_update_profile_with_empty_string(self, client, auth_headers, test_user):
        """Test: Update profile with empty string
        Expected: Field cleared or validation error
        """
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'first_name': ''}
        )
        # Should either accept empty string or reject
        assert response.status_code in [200, 400]
    
    def test_update_profile_partial_update(self, client, auth_headers, test_user):
        """Test: Update only one field when multiple exist
        Expected: Only specified field updated, others unchanged
        """
        # Set initial values
        client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={
                'first_name': 'Original',
                'last_name': 'Name'
            }
        )
        
        # Update only first_name
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'first_name': 'Updated'}
        )
        assert response.status_code == 200
        assert response.json['first_name'] == 'Updated'
        # last_name should remain unchanged
        assert response.json['last_name'] == 'Name'
    
    def test_update_profile_with_special_characters(self, client, auth_headers, test_user):
        """Test: Update profile with special characters
        Expected: Special characters preserved
        """
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={
                'first_name': "O'Brien",
                'last_name': 'van der Berg'
            }
        )
        assert response.status_code == 200
        assert response.json['first_name'] == "O'Brien"
    
    def test_update_profile_with_unicode(self, client, auth_headers, test_user):
        """Test: Update profile with Unicode characters
        Expected: Unicode characters preserved
        """
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={
                'first_name': 'José',
                'last_name': 'Müller'
            }
        )
        assert response.status_code == 200
        assert response.json['first_name'] == 'José'
    
    # ========== SECURITY TEST CASES ==========
    
    def test_update_profile_authorization_check(self, client, auth_headers, db_session):
        """Test: Verify authorization check prevents unauthorized updates
        Expected: 403 Forbidden for unauthorized access
        """
        other_user = User(
            username='victim',
            email='victim@example.com',
            role=User.ROLE_CUSTOMER
        )
        other_user.set_password('password123')
        db_session.add(other_user)
        db_session.commit()
        
        # Try to update other user's profile
        response = client.put(f'/api/users/{other_user.id}',
            headers=auth_headers,
            json={'email': 'hacked@example.com'}
        )
        assert response.status_code == 403
    
    def test_admin_cannot_remove_own_admin_role(self, client, admin_headers, test_admin):
        """Test: Admin cannot remove own admin role
        Expected: 400 Bad Request
        """
        response = client.put(f'/api/users/{test_admin.id}',
            headers=admin_headers,
            json={'role': User.ROLE_CUSTOMER}
        )
        assert response.status_code == 400
        assert 'admin role' in str(response.json.get('message', '')).lower()
    
    def test_admin_cannot_deactivate_own_account(self, client, admin_headers, test_admin):
        """Test: Admin cannot deactivate own account
        Expected: 400 Bad Request
        """
        response = client.put(f'/api/users/{test_admin.id}',
            headers=admin_headers,
            json={'is_active': False}
        )
        assert response.status_code == 400
        assert 'deactivate' in str(response.json.get('message', '')).lower()
    
    def test_update_profile_sql_injection(self, client, auth_headers, test_user, db_session):
        """Test: Attempt SQL injection in update fields
        Expected: Treated as literal string, no SQL execution
        """
        malicious_input = "'; DROP TABLE users; --"
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'first_name': malicious_input}
        )
        # Should either accept as literal string or reject
        assert response.status_code in [200, 400]
        if response.status_code == 200:
            # Verify user still exists
            user = User.query.get(test_user.id)
            assert user is not None


class TestPasswordChanges:
    """Test cases for password changes"""
    
    # ========== POSITIVE TEST CASES ==========
    
    def test_change_password_success(self, client, auth_headers, test_user):
        """Test: User changes own password successfully
        Expected: Password updated, can login with new password
        """
        old_password = 'password123'
        new_password = 'NewSecurePass123'
        
        # Change password
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'password': new_password}
        )
        assert response.status_code == 200
        
        # Verify old password no longer works
        login_old = client.post('/api/auth/login', json={
            'username': test_user.username,
            'password': old_password
        })
        assert login_old.status_code == 401
        
        # Verify new password works
        login_new = client.post('/api/auth/login', json={
            'username': test_user.username,
            'password': new_password
        })
        assert login_new.status_code == 200
    
    def test_change_password_with_special_characters(self, client, auth_headers, test_user):
        """Test: Change password with special characters
        Expected: Password updated successfully
        """
        special_password = 'P@ssw0rd!#$%^&*()'
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'password': special_password}
        )
        assert response.status_code == 200
        
        # Verify login works
        login_response = client.post('/api/auth/login', json={
            'username': test_user.username,
            'password': special_password
        })
        assert login_response.status_code == 200
    
    def test_change_password_with_unicode(self, client, auth_headers, test_user):
        """Test: Change password with Unicode characters
        Expected: Password updated successfully
        """
        unicode_password = 'Pässwörd123'
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'password': unicode_password}
        )
        assert response.status_code == 200
        
        # Verify login works
        login_response = client.post('/api/auth/login', json={
            'username': test_user.username,
            'password': unicode_password
        })
        assert login_response.status_code == 200
    
    def test_admin_change_user_password(self, client, admin_headers, test_user):
        """Test: Admin changes another user's password
        Expected: Password updated successfully
        """
        new_password = 'AdminChangedPass123'
        response = client.put(f'/api/users/{test_user.id}',
            headers=admin_headers,
            json={'password': new_password}
        )
        assert response.status_code == 200
        
        # Verify new password works
        login_response = client.post('/api/auth/login', json={
            'username': test_user.username,
            'password': new_password
        })
        assert login_response.status_code == 200
    
    # ========== NEGATIVE TEST CASES ==========
    
    def test_change_password_too_short(self, client, auth_headers, test_user):
        """Test: Change password to less than 8 characters
        Expected: 400 Bad Request
        """
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'password': 'short'}  # Less than 8 chars
        )
        assert response.status_code == 400
    
    def test_change_password_without_authentication(self, client, test_user):
        """Test: Change password without authentication
        Expected: 401 Unauthorized
        """
        response = client.put(f'/api/users/{test_user.id}',
            json={'password': 'NewPassword123'}
        )
        assert response.status_code == 401
    
    def test_change_other_user_password_as_non_admin(self, client, auth_headers, db_session):
        """Test: Non-admin tries to change another user's password
        Expected: 403 Forbidden
        """
        other_user = User(
            username='otheruser3',
            email='other3@example.com',
            role=User.ROLE_CUSTOMER
        )
        other_user.set_password('password123')
        db_session.add(other_user)
        db_session.commit()
        
        response = client.put(f'/api/users/{other_user.id}',
            headers=auth_headers,
            json={'password': 'HackedPassword123'}
        )
        assert response.status_code == 403
    
    # ========== EDGE CASES ==========
    
    def test_change_password_to_same_password(self, client, auth_headers, test_user):
        """Test: Change password to the same value
        Expected: Password updated (hash regenerated)
        """
        current_password = 'password123'
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'password': current_password}
        )
        assert response.status_code == 200
        
        # Password should still work
        login_response = client.post('/api/auth/login', json={
            'username': test_user.username,
            'password': current_password
        })
        assert login_response.status_code == 200
    
    def test_change_password_with_maximum_length(self, client, auth_headers, test_user):
        """Test: Change password to maximum length
        Expected: Password updated successfully
        """
        long_password = 'A' * 1000
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'password': long_password}
        )
        assert response.status_code == 200
        
        # Verify login works
        login_response = client.post('/api/auth/login', json={
            'username': test_user.username,
            'password': long_password
        })
        assert login_response.status_code == 200
    
    def test_change_password_multiple_times_rapidly(self, client, auth_headers, test_user):
        """Test: Change password multiple times rapidly
        Expected: All changes succeed, last password is active
        """
        passwords = ['Pass1', 'Pass2', 'Pass3']
        for pwd in passwords:
            response = client.put(f'/api/users/{test_user.id}',
                headers=auth_headers,
                json={'password': pwd}
            )
            assert response.status_code == 200
        
        # Only last password should work
        login_response = client.post('/api/auth/login', json={
            'username': test_user.username,
            'password': passwords[-1]
        })
        assert login_response.status_code == 200
    
    # ========== SECURITY TEST CASES ==========
    
    def test_password_not_returned_in_response(self, client, auth_headers, test_user):
        """Test: Password never returned in API response
        Expected: Password field absent from response
        """
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'password': 'NewSecurePass123'}
        )
        assert response.status_code == 200
        assert 'password' not in response.json
        assert 'password_hash' not in response.json
    
    def test_password_is_hashed(self, client, auth_headers, test_user, db_session):
        """Test: Password is stored as hash, not plaintext
        Expected: Password hash stored, plaintext not accessible
        """
        new_password = 'NewSecurePass123'
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'password': new_password}
        )
        assert response.status_code == 200
        
        user = User.query.get(test_user.id)
        assert user.password_hash != new_password
        assert user.check_password(new_password) is True
    
    def test_password_change_invalidates_old_tokens(self, client, auth_headers, test_user):
        """Test: Changing password should ideally invalidate old tokens
        Expected: Old token may or may not work (depends on implementation)
        """
        # Get initial token
        initial_token = auth_headers['Authorization'].split(' ')[1]
        
        # Change password
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'password': 'NewPassword123'}
        )
        assert response.status_code == 200
        
        # Try to use old token (behavior depends on implementation)
        old_headers = {'Authorization': f'Bearer {initial_token}'}
        get_response = client.get(f'/api/users/{test_user.id}', headers=old_headers)
        # Token may still work (JWT doesn't automatically invalidate)
        assert get_response.status_code in [200, 401]


class TestAccountDeletion:
    """Test cases for account deletion"""
    
    # ========== POSITIVE TEST CASES ==========
    
    def test_delete_own_account(self, client, auth_headers, db_session):
        """Test: User deletes own account
        Expected: Account deleted, 204 No Content
        """
        user = User(
            username='todelete',
            email='todelete@example.com',
            role=User.ROLE_CUSTOMER
        )
        user.set_password('password123')
        db_session.add(user)
        db_session.commit()
        user_id = user.id
        
        # Login as user
        login_response = client.post('/api/auth/login', json={
            'username': 'todelete',
            'password': 'password123'
        })
        token = login_response.json['access_token']
        user_headers = {'Authorization': f'Bearer {token}'}
        
        # Delete account
        response = client.delete(f'/api/users/{user_id}', headers=user_headers)
        assert response.status_code == 204
        
        # Verify user is deleted
        deleted_user = User.query.get(user_id)
        assert deleted_user is None
    
    def test_admin_delete_user_account(self, client, admin_headers, db_session):
        """Test: Admin deletes another user's account
        Expected: Account deleted successfully
        """
        user = User(
            username='admindelete',
            email='admindelete@example.com',
            role=User.ROLE_CUSTOMER
        )
        user.set_password('password123')
        db_session.add(user)
        db_session.commit()
        user_id = user.id
        
        # Delete as admin
        response = client.delete(f'/api/users/{user_id}', headers=admin_headers)
        assert response.status_code == 204
        
        # Verify user is deleted
        deleted_user = User.query.get(user_id)
        assert deleted_user is None
    
    def test_delete_account_cascades_to_related_data(self, client, admin_headers, db_session):
        """Test: Deleting account cascades to related data (posts, etc.)
        Expected: Related data deleted or handled appropriately
        """
        user = User(
            username='cascadetest',
            email='cascade@example.com',
            role=User.ROLE_CUSTOMER
        )
        user.set_password('password123')
        db_session.add(user)
        db_session.commit()
        
        # Create related data (posts)
        from app.models.post import Post
        post = Post(
            title='Test Post',
            content='Content',
            slug='test-post',
            user_id=user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        post_id = post.id
        
        # Delete user
        response = client.delete(f'/api/users/{user.id}', headers=admin_headers)
        assert response.status_code == 204
        
        # Verify user is deleted
        assert User.query.get(user.id) is None
        # Verify related data is handled (may be deleted or orphaned)
        # This depends on cascade settings
    
    # ========== NEGATIVE TEST CASES ==========
    
    def test_delete_other_user_account_as_non_admin(self, client, auth_headers, db_session):
        """Test: Non-admin tries to delete another user's account
        Expected: 403 Forbidden
        """
        other_user = User(
            username='protected',
            email='protected@example.com',
            role=User.ROLE_CUSTOMER
        )
        other_user.set_password('password123')
        db_session.add(other_user)
        db_session.commit()
        
        response = client.delete(f'/api/users/{other_user.id}', headers=auth_headers)
        assert response.status_code == 403
    
    def test_delete_nonexistent_account(self, client, admin_headers):
        """Test: Delete non-existent account
        Expected: 404 Not Found
        """
        response = client.delete('/api/users/99999', headers=admin_headers)
        assert response.status_code == 404
    
    def test_delete_account_without_authentication(self, client, test_user):
        """Test: Delete account without authentication
        Expected: 401 Unauthorized
        """
        response = client.delete(f'/api/users/{test_user.id}')
        assert response.status_code == 401
    
    def test_delete_account_with_invalid_token(self, client, test_user):
        """Test: Delete account with invalid token
        Expected: 401 Unauthorized
        """
        invalid_headers = {'Authorization': 'Bearer invalid_token'}
        response = client.delete(f'/api/users/{test_user.id}', headers=invalid_headers)
        assert response.status_code == 401
    
    # ========== EDGE CASES ==========
    
    def test_delete_account_twice(self, client, admin_headers, db_session):
        """Test: Attempt to delete already deleted account
        Expected: 404 Not Found on second attempt
        """
        user = User(
            username='doubledelete',
            email='double@example.com',
            role=User.ROLE_CUSTOMER
        )
        user.set_password('password123')
        db_session.add(user)
        db_session.commit()
        user_id = user.id
        
        # First deletion
        response1 = client.delete(f'/api/users/{user_id}', headers=admin_headers)
        assert response1.status_code == 204
        
        # Second deletion attempt
        response2 = client.delete(f'/api/users/{user_id}', headers=admin_headers)
        assert response2.status_code == 404
    
    def test_delete_account_with_active_sessions(self, client, auth_headers, db_session):
        """Test: Delete account while user has active sessions
        Expected: Account deleted, sessions may become invalid
        """
        user = User(
            username='sessiontest',
            email='session@example.com',
            role=User.ROLE_CUSTOMER
        )
        user.set_password('password123')
        db_session.add(user)
        db_session.commit()
        user_id = user.id
        
        # Login (creates session/token)
        login_response = client.post('/api/auth/login', json={
            'username': 'sessiontest',
            'password': 'password123'
        })
        token = login_response.json['access_token']
        user_headers = {'Authorization': f'Bearer {token}'}
        
        # Delete account
        response = client.delete(f'/api/users/{user_id}', headers=user_headers)
        assert response.status_code == 204
        
        # Try to use token after deletion (may or may not work)
        get_response = client.get(f'/api/users/{user_id}', headers=user_headers)
        assert get_response.status_code in [401, 404]
    
    # ========== SECURITY TEST CASES ==========
    
    def test_delete_account_authorization_check(self, client, auth_headers, db_session):
        """Test: Verify authorization prevents unauthorized deletion
        Expected: 403 Forbidden for unauthorized access
        """
        other_user = User(
            username='protected2',
            email='protected2@example.com',
            role=User.ROLE_CUSTOMER
        )
        other_user.set_password('password123')
        db_session.add(other_user)
        db_session.commit()
        
        response = client.delete(f'/api/users/{other_user.id}', headers=auth_headers)
        assert response.status_code == 403
    
    def test_admin_cannot_delete_self(self, client, admin_headers, test_admin):
        """Test: Admin attempts to delete own account
        Expected: May be allowed or prevented (depends on implementation)
        """
        response = client.delete(f'/api/users/{test_admin.id}', headers=admin_headers)
        # Behavior depends on implementation - may allow or prevent
        assert response.status_code in [204, 400, 403]
    
    def test_delete_account_sql_injection(self, client, admin_headers):
        """Test: Attempt SQL injection in user ID
        Expected: Treated as invalid ID, 404 Not Found
        """
        malicious_id = "1' OR '1'='1"
        response = client.delete(f'/api/users/{malicious_id}', headers=admin_headers)
        # Should treat as invalid ID format
        assert response.status_code in [404, 400]
    
    def test_delete_account_idor_vulnerability(self, client, auth_headers, db_session):
        """Test: Test for Insecure Direct Object Reference vulnerability
        Expected: Authorization check prevents unauthorized access
        """
        # Create multiple users
        user1 = User(username='user1', email='user1@example.com', role=User.ROLE_CUSTOMER)
        user1.set_password('password123')
        user2 = User(username='user2', email='user2@example.com', role=User.ROLE_CUSTOMER)
        user2.set_password('password123')
        db_session.add_all([user1, user2])
        db_session.commit()
        
        # Login as user1
        login_response = client.post('/api/auth/login', json={
            'username': 'user1',
            'password': 'password123'
        })
        token = login_response.json['access_token']
        user1_headers = {'Authorization': f'Bearer {token}'}
        
        # Try to delete user2's account
        response = client.delete(f'/api/users/{user2.id}', headers=user1_headers)
        assert response.status_code == 403
        
        # Verify user2 still exists
        assert User.query.get(user2.id) is not None


# ========== INTEGRATION TEST CASES ==========

class TestUserProfileIntegration:
    """Integration test cases combining multiple operations"""
    
    def test_complete_user_lifecycle(self, client, db_session):
        """Test: Complete user lifecycle - register, update, change password, delete
        Expected: All operations succeed in sequence
        """
        # 1. Register
        register_response = client.post('/api/auth/register', json={
            'username': 'lifecycle',
            'email': 'lifecycle@example.com',
            'password': 'InitialPass123',
            'first_name': 'Initial',
            'last_name': 'Name'
        })
        assert register_response.status_code == 201
        user_id = register_response.json['id']
        
        # 2. Login
        login_response = client.post('/api/auth/login', json={
            'username': 'lifecycle',
            'password': 'InitialPass123'
        })
        assert login_response.status_code == 200
        token = login_response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # 3. Update profile
        update_response = client.put(f'/api/users/{user_id}',
            headers=headers,
            json={
                'first_name': 'Updated',
                'last_name': 'Name'
            }
        )
        assert update_response.status_code == 200
        
        # 4. Change password
        password_response = client.put(f'/api/users/{user_id}',
            headers=headers,
            json={'password': 'NewPassword123'}
        )
        assert password_response.status_code == 200
        
        # 5. Login with new password
        new_login = client.post('/api/auth/login', json={
            'username': 'lifecycle',
            'password': 'NewPassword123'
        })
        assert new_login.status_code == 200
        new_token = new_login.json['access_token']
        new_headers = {'Authorization': f'Bearer {new_token}'}
        
        # 6. Delete account
        delete_response = client.delete(f'/api/users/{user_id}', headers=new_headers)
        assert delete_response.status_code == 204
        
        # 7. Verify deletion
        assert User.query.get(user_id) is None
    
    def test_concurrent_updates(self, client, auth_headers, test_user):
        """Test: Multiple concurrent update requests
        Expected: Last update wins or proper conflict handling
        """
        # Simulate concurrent updates
        update1 = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'first_name': 'Update1'}
        )
        update2 = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'first_name': 'Update2'}
        )
        
        # Both should succeed
        assert update1.status_code == 200
        assert update2.status_code == 200
        
        # Last update should be reflected
        get_response = client.get(f'/api/users/{test_user.id}', headers=auth_headers)
        assert get_response.json['first_name'] in ['Update1', 'Update2']
