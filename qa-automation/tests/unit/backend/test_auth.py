"""Authentication and authorization tests"""
import pytest
import json
from app.models import User
from datetime import datetime

class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_register_user(self, client):
        """Test user registration"""
        response = client.post('/api/auth/register', json={
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'password123',
            'role': 'customer'
        })
        assert response.status_code == 201
        assert 'id' in response.json
        assert response.json['username'] == 'newuser'
        assert response.json['email'] == 'newuser@test.com'
        assert 'password' not in response.json
    
    def test_register_duplicate_username(self, client, test_user):
        """Test registration with duplicate username"""
        response = client.post('/api/auth/register', json={
            'username': test_user.username,
            'email': 'different@test.com',
            'password': 'password123'
        })
        assert response.status_code == 400
    
    def test_register_duplicate_email(self, client, test_user):
        """Test registration with duplicate email"""
        response = client.post('/api/auth/register', json={
            'username': 'differentuser',
            'email': test_user.email,
            'password': 'password123'
        })
        assert response.status_code == 400
    
    def test_register_invalid_password(self, client):
        """Test registration with invalid password"""
        response = client.post('/api/auth/register', json={
            'username': 'user',
            'email': 'user@test.com',
            'password': 'short'  # Too short
        })
        assert response.status_code == 400
    
    def test_login_success(self, client, test_user):
        """Test successful login"""
        response = client.post('/api/auth/login', json={
            'username': test_user.username,
            'password': 'testpassword123'
        })
        assert response.status_code == 200
        assert 'access_token' in response.json
        assert 'refresh_token' in response.json
    
    def test_login_invalid_username(self, client):
        """Test login with invalid username"""
        response = client.post('/api/auth/login', json={
            'username': 'nonexistent',
            'password': 'password123'
        })
        assert response.status_code == 401
    
    def test_login_invalid_password(self, client, test_user):
        """Test login with invalid password"""
        response = client.post('/api/auth/login', json={
            'username': test_user.username,
            'password': 'wrongpassword'
        })
        assert response.status_code == 401
    
    def test_login_inactive_user(self, client, db_session):
        """Test login with inactive user"""
        user = User(
            username='inactive',
            email='inactive@test.com',
            is_active=False
        )
        user.set_password('password123')
        db_session.add(user)
        db_session.commit()
        
        response = client.post('/api/auth/login', json={
            'username': 'inactive',
            'password': 'password123'
        })
        assert response.status_code == 401
    
    def test_get_current_user(self, client, auth_headers, test_user):
        """Test getting current user info"""
        response = client.get('/api/auth/me', headers=auth_headers)
        assert response.status_code == 200
        assert response.json['id'] == test_user.id
        assert response.json['username'] == test_user.username
    
    def test_get_current_user_unauthorized(self, client):
        """Test getting current user without token"""
        response = client.get('/api/auth/me')
        assert response.status_code == 401
    
    def test_refresh_token(self, client, test_user):
        """Test token refresh"""
        # Login to get refresh token
        login_response = client.post('/api/auth/login', json={
            'username': test_user.username,
            'password': 'testpassword123'
        })
        refresh_token = login_response.json['refresh_token']
        
        # Refresh token - use refresh token in Authorization header
        response = client.post('/api/auth/refresh', 
            headers={'Authorization': f'Bearer {refresh_token}'}
        )
        assert response.status_code == 200
        assert 'access_token' in response.json
    
    def test_logout(self, client, auth_headers):
        """Test logout"""
        response = client.post('/api/auth/logout', headers=auth_headers)
        assert response.status_code == 200

class TestAuthorization:
    """Test authorization and access control"""
    
    def test_access_protected_endpoint_without_token(self, client):
        """Test accessing protected endpoint without token"""
        response = client.get('/api/tasks')
        assert response.status_code == 401
    
    def test_access_protected_endpoint_with_invalid_token(self, client):
        """Test accessing protected endpoint with invalid token"""
        headers = {'Authorization': 'Bearer invalid_token'}
        response = client.get('/api/tasks', headers=headers)
        # Invalid token can return 401 or 422 depending on JWT library version
        assert response.status_code in [401, 422]
    
    def test_access_protected_endpoint_with_valid_token(self, client, auth_headers):
        """Test accessing protected endpoint with valid token"""
        response = client.get('/api/tasks', headers=auth_headers)
        assert response.status_code == 200
    
    def test_admin_only_endpoint_customer(self, client, auth_headers):
        """Test admin-only endpoint access as customer"""
        response = client.get('/api/admin/dashboard', headers=auth_headers)
        assert response.status_code == 403
    
    def test_admin_only_endpoint_admin(self, client, admin_headers):
        """Test admin-only endpoint access as admin"""
        response = client.get('/api/admin/dashboard', headers=admin_headers)
        assert response.status_code == 200
    
    def test_agent_can_access_assigned_tasks(self, client, db_session, test_agent):
        """Test agent can access assigned tasks"""
        from app.models import Task
        
        # Login as agent
        login_response = client.post('/api/auth/login', json={
            'username': test_agent.username,
            'password': 'agentpassword123'
        })
        token = login_response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create task assigned to agent
        task = Task(
            title='Agent Task',
            created_by_id=test_agent.id,
            assigned_to_id=test_agent.id
        )
        db_session.add(task)
        db_session.commit()
        
        # Access task
        response = client.get(f'/api/tasks/{task.id}', headers=headers)
        assert response.status_code == 200
    
    def test_customer_cannot_access_other_user_tasks(self, client, db_session, test_user):
        """Test customer cannot access other user's tasks"""
        from app.models import Task, User
        
        # Create another user
        other_user = User(
            username='other',
            email='other@test.com',
            role=User.ROLE_CUSTOMER
        )
        other_user.set_password('password123')
        db_session.add(other_user)
        db_session.commit()
        
        # Create task for other user
        task = Task(
            title='Other User Task',
            created_by_id=other_user.id
        )
        db_session.add(task)
        db_session.commit()
        
        # Login as test_user
        login_response = client.post('/api/auth/login', json={
            'username': test_user.username,
            'password': 'testpassword123'
        })
        token = login_response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Try to access other user's task
        response = client.get(f'/api/tasks/{task.id}', headers=headers)
        assert response.status_code == 403
