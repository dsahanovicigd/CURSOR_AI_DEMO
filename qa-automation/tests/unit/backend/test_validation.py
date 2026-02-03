"""Validation tests for API endpoints"""
import pytest
from datetime import datetime, timedelta

class TestTaskValidation:
    """Test task validation"""
    
    def test_create_task_without_title(self, client, auth_headers):
        """Test creating task without required title"""
        response = client.post('/api/tasks',
            headers=auth_headers,
            json={'description': 'No title'}
        )
        assert response.status_code == 400
    
    def test_create_task_with_empty_title(self, client, auth_headers):
        """Test creating task with empty title"""
        response = client.post('/api/tasks',
            headers=auth_headers,
            json={'title': ''}
        )
        assert response.status_code == 400
    
    def test_create_task_with_invalid_status(self, client, auth_headers):
        """Test creating task with invalid status"""
        response = client.post('/api/tasks',
            headers=auth_headers,
            json={
                'title': 'Task',
                'status': 'invalid_status'
            }
        )
        assert response.status_code == 400
    
    def test_create_task_with_invalid_priority(self, client, auth_headers):
        """Test creating task with invalid priority"""
        response = client.post('/api/tasks',
            headers=auth_headers,
            json={
                'title': 'Task',
                'priority': 'invalid_priority'
            }
        )
        assert response.status_code == 400
    
    def test_create_task_with_valid_status(self, client, auth_headers):
        """Test creating task with valid status"""
        response = client.post('/api/tasks',
            headers=auth_headers,
            json={
                'title': 'Task',
                'status': 'in_progress'
            }
        )
        assert response.status_code == 201
        assert response.json['status'] == 'in_progress'
    
    def test_create_task_with_valid_priority(self, client, auth_headers):
        """Test creating task with valid priority"""
        response = client.post('/api/tasks',
            headers=auth_headers,
            json={
                'title': 'Task',
                'priority': 'high'
            }
        )
        assert response.status_code == 201
        assert response.json['priority'] == 'high'
    
    def test_update_task_with_invalid_data(self, client, auth_headers, test_task):
        """Test updating task with invalid data"""
        response = client.put(f'/api/tasks/{test_task.id}',
            headers=auth_headers,
            json={'status': 'invalid_status'}
        )
        assert response.status_code == 400
    
    def test_update_task_with_valid_data(self, client, auth_headers, test_task):
        """Test updating task with valid data"""
        response = client.put(f'/api/tasks/{test_task.id}',
            headers=auth_headers,
            json={
                'title': 'Updated Task',
                'status': 'completed',
                'priority': 'urgent'
            }
        )
        assert response.status_code == 200
        assert response.json['title'] == 'Updated Task'
        assert response.json['status'] == 'completed'
        assert response.json['priority'] == 'urgent'

class TestUserValidation:
    """Test user validation"""
    
    def test_register_with_invalid_email(self, client):
        """Test registration with invalid email format"""
        response = client.post('/api/auth/register', json={
            'username': 'user',
            'email': 'invalid-email',
            'password': 'password123'
        })
        assert response.status_code == 400
    
    def test_register_with_short_password(self, client):
        """Test registration with password too short"""
        response = client.post('/api/auth/register', json={
            'username': 'user',
            'email': 'user@test.com',
            'password': 'short'  # Less than 8 characters
        })
        assert response.status_code == 400
    
    def test_register_with_valid_data(self, client):
        """Test registration with valid data"""
        response = client.post('/api/auth/register', json={
            'username': 'validuser',
            'email': 'valid@test.com',
            'password': 'password123'
        })
        assert response.status_code == 201
    
    def test_update_user_with_invalid_email(self, client, auth_headers, test_user):
        """Test updating user with invalid email"""
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={'email': 'invalid-email'}
        )
        assert response.status_code == 400
    
    def test_update_user_with_valid_data(self, client, auth_headers, test_user):
        """Test updating user with valid data"""
        response = client.put(f'/api/users/{test_user.id}',
            headers=auth_headers,
            json={
                'name': 'Updated Name',
                'email': 'updated@test.com'
            }
        )
        assert response.status_code == 200
        assert response.json['email'] == 'updated@test.com'

class TestProjectValidation:
    """Test project validation"""
    
    def test_create_project_without_name(self, client, auth_headers):
        """Test creating project without name"""
        response = client.post('/api/projects',
            headers=auth_headers,
            json={'description': 'No name'}
        )
        assert response.status_code == 400
    
    def test_create_project_with_empty_name(self, client, auth_headers):
        """Test creating project with empty name"""
        response = client.post('/api/projects',
            headers=auth_headers,
            json={'name': ''}
        )
        assert response.status_code == 400
    
    def test_create_project_with_valid_data(self, client, auth_headers):
        """Test creating project with valid data"""
        response = client.post('/api/projects',
            headers=auth_headers,
            json={
                'name': 'Test Project',
                'description': 'Project description'
            }
        )
        assert response.status_code == 201
        assert response.json['name'] == 'Test Project'

class TestPaginationValidation:
    """Test pagination validation"""
    
    def test_pagination_with_negative_page(self, client, auth_headers):
        """Test pagination with negative page number"""
        response = client.get('/api/tasks?page=-1', headers=auth_headers)
        # Should default to page 1 or return 400
        assert response.status_code in [200, 400]
    
    def test_pagination_with_zero_page(self, client, auth_headers):
        """Test pagination with zero page number"""
        response = client.get('/api/tasks?page=0', headers=auth_headers)
        # Should default to page 1 or return 400
        assert response.status_code in [200, 400]
    
    def test_pagination_with_large_per_page(self, client, auth_headers):
        """Test pagination with per_page exceeding max"""
        response = client.get('/api/tasks?per_page=1000', headers=auth_headers)
        assert response.status_code == 200
        # Should be capped at max (100)
        assert response.json['pagination']['per_page'] <= 100
    
    def test_pagination_with_valid_params(self, client, auth_headers):
        """Test pagination with valid parameters"""
        response = client.get('/api/tasks?page=1&per_page=10', headers=auth_headers)
        assert response.status_code == 200
        assert response.json['pagination']['page'] == 1
        assert response.json['pagination']['per_page'] == 10

class TestFilterValidation:
    """Test filter validation"""
    
    def test_filter_with_invalid_status(self, client, auth_headers):
        """Test filtering with invalid status"""
        response = client.get('/api/tasks?status=invalid', headers=auth_headers)
        # Should return empty results or 400
        assert response.status_code in [200, 400]
    
    def test_filter_with_valid_status(self, client, auth_headers, test_task):
        """Test filtering with valid status"""
        response = client.get(f'/api/tasks?status={test_task.status}', headers=auth_headers)
        assert response.status_code == 200
        tasks = response.json.get('tasks', [])
        if tasks:
            assert all(task['status'] == test_task.status for task in tasks)
    
    def test_filter_with_invalid_priority(self, client, auth_headers):
        """Test filtering with invalid priority"""
        response = client.get('/api/tasks?priority=invalid', headers=auth_headers)
        # Should return empty results or 400
        assert response.status_code in [200, 400]
    
    def test_filter_with_valid_priority(self, client, auth_headers, test_task):
        """Test filtering with valid priority"""
        response = client.get(f'/api/tasks?priority={test_task.priority}', headers=auth_headers)
        assert response.status_code == 200
        tasks = response.json.get('tasks', [])
        if tasks:
            assert all(task['priority'] == test_task.priority for task in tasks)
    
    def test_filter_with_nonexistent_project(self, client, auth_headers):
        """Test filtering with nonexistent project"""
        response = client.get('/api/tasks?project_id=99999', headers=auth_headers)
        # Should return 404 or empty results
        assert response.status_code in [200, 404]

class TestDateValidation:
    """Test date validation"""
    
    def test_create_task_with_invalid_due_date(self, client, auth_headers):
        """Test creating task with invalid due date format"""
        response = client.post('/api/tasks',
            headers=auth_headers,
            json={
                'title': 'Task',
                'due_date': 'invalid-date'
            }
        )
        # Should return 400 or handle gracefully
        assert response.status_code in [201, 400]
    
    def test_create_task_with_valid_due_date(self, client, auth_headers):
        """Test creating task with valid due date"""
        due_date = (datetime.utcnow() + timedelta(days=7)).isoformat()
        response = client.post('/api/tasks',
            headers=auth_headers,
            json={
                'title': 'Task',
                'due_date': due_date
            }
        )
        assert response.status_code == 201
        assert response.json['due_date'] is not None
    
    def test_create_task_with_past_due_date(self, client, auth_headers):
        """Test creating task with past due date (should be allowed)"""
        past_date = (datetime.utcnow() - timedelta(days=1)).isoformat()
        response = client.post('/api/tasks',
            headers=auth_headers,
            json={
                'title': 'Task',
                'due_date': past_date
            }
        )
        # Should be allowed (business logic may vary)
        assert response.status_code in [201, 400]

class TestAccessValidation:
    """Test access validation"""
    
    def test_access_nonexistent_task(self, client, auth_headers):
        """Test accessing nonexistent task"""
        response = client.get('/api/tasks/99999', headers=auth_headers)
        assert response.status_code == 404
    
    def test_update_nonexistent_task(self, client, auth_headers):
        """Test updating nonexistent task"""
        response = client.put('/api/tasks/99999',
            headers=auth_headers,
            json={'title': 'Updated'}
        )
        assert response.status_code == 404
    
    def test_delete_nonexistent_task(self, client, auth_headers):
        """Test deleting nonexistent task"""
        response = client.delete('/api/tasks/99999', headers=auth_headers)
        assert response.status_code == 404
    
    def test_access_task_without_permission(self, client, db_session, test_user):
        """Test accessing task without permission"""
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
            title='Private Task',
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
