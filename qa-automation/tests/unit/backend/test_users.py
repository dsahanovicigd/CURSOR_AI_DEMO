"""User management tests"""
import pytest
from app.models import User

class TestUserManagement:
    """Test user management operations"""
    
    def test_get_users_list(self, client, auth_headers):
        """Test retrieving list of users"""
        response = client.get('/api/users',
            headers=auth_headers
        )
        assert response.status_code == 200
        assert 'users' in response.json
    
    def test_get_user(self, client, auth_headers, test_user):
        """Test retrieving a specific user"""
        response = client.get(f'/api/users/{test_user.id}',
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json['id'] == test_user.id
    
    def test_update_own_profile(self, client, auth_headers, test_user):
        """Test updating own profile"""
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={
                'first_name': 'Updated',
                'last_name': 'Name'
            }
        )
        assert response.status_code == 200
        assert response.json['first_name'] == 'Updated'
    
    def test_update_other_user_as_admin(self, client, admin_headers, test_user):
        """Test admin updating another user"""
        response = client.put(f'/api/users/{test_user.id}',
            headers=admin_headers,
            json={'first_name': 'Admin Updated'}
        )
        assert response.status_code == 200
    
    def test_update_other_user_as_non_admin(self, client, auth_headers, db_session):
        """Test non-admin cannot update other user"""
        other_user = User(
            username='other',
            email='other@test.com',
            role=User.ROLE_CUSTOMER
        )
        other_user.set_password('password123')
        db_session.add(other_user)
        db_session.commit()
        
        response = client.put(f'/api/users/{other_user.id}',
            headers=auth_headers,
            json={'first_name': 'Should Fail'}
        )
        assert response.status_code == 403
    
    def test_admin_update_role(self, client, admin_headers, test_user):
        """Test admin updating user role"""
        response = client.put(f'/api/users/{test_user.id}',
            headers=admin_headers,
            json={'role': User.ROLE_AGENT}
        )
        assert response.status_code == 200
        assert response.json['role'] == User.ROLE_AGENT
    
    def test_non_admin_cannot_update_role(self, client, auth_headers, test_user):
        """Test non-admin cannot update role"""
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'role': User.ROLE_ADMIN}
        )
        assert response.status_code == 403
    
    def test_delete_user(self, client, admin_headers, db_session):
        """Test deleting a user"""
        user = User(
            username='todelete',
            email='delete@test.com',
            role=User.ROLE_CUSTOMER
        )
        user.set_password('password123')
        db_session.add(user)
        db_session.commit()
        
        user_id = user.id
        response = client.delete(f'/api/users/{user_id}',
            headers=admin_headers
        )
        assert response.status_code == 204
        
        # Verify user is deleted
        get_response = client.get(f'/api/users/{user_id}',
            headers=admin_headers
        )
        assert get_response.status_code == 404
    
    def test_user_pagination(self, client, auth_headers):
        """Test user list pagination"""
        response = client.get('/api/users?page=1&per_page=10',
            headers=auth_headers
        )
        assert response.status_code == 200
        assert 'users' in response.json
    
    def test_update_user_password(self, client, auth_headers, test_user):
        """Test updating user password"""
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'password': 'newpassword123'}
        )
        assert response.status_code == 200
    
    def test_update_user_availability(self, client, auth_headers, test_user):
        """Test updating user availability status"""
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'availability_status': User.AVAILABILITY_BUSY}
        )
        assert response.status_code == 200
    
    def test_update_user_expertise_areas(self, client, auth_headers, test_user):
        """Test updating user expertise areas"""
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'expertise_areas': ['python', 'flask']}
        )
        assert response.status_code == 200
        assert response.json['expertise_areas'] == ['python', 'flask']
    
    def test_admin_cannot_remove_own_admin_role(self, client, admin_headers, test_admin):
        """Test admin cannot remove own admin role"""
        response = client.put(f'/api/users/{test_admin.id}',
            headers=admin_headers,
            json={'role': User.ROLE_CUSTOMER}
        )
        assert response.status_code == 400
    
    def test_admin_cannot_deactivate_own_account(self, client, admin_headers, test_admin):
        """Test admin cannot deactivate own account"""
        response = client.put(f'/api/users/{test_admin.id}',
            headers=admin_headers,
            json={'is_active': False}
        )
        assert response.status_code == 400
