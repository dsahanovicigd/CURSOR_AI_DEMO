"""Task CRUD operation tests"""
import pytest
import json
from datetime import datetime, timedelta
from app.models import Task, User, Project

class TestTaskCRUD:
    """Test task CRUD operations"""
    
    def test_create_task(self, client, auth_headers, test_project):
        """Test creating a new task"""
        response = client.post('/api/tasks', 
            headers=auth_headers,
            json={
                'title': 'New Task',
                'description': 'Task description',
                'project_id': test_project.id,
                'priority': 'high'
            }
        )
        assert response.status_code == 201
        data = response.json
        assert data['title'] == 'New Task'
        assert data['status'] == Task.STATUS_PENDING
        assert data['priority'] == 'high'
        assert 'id' in data
    
    def test_create_task_without_project(self, client, auth_headers):
        """Test creating task without project"""
        response = client.post('/api/tasks',
            headers=auth_headers,
            json={
                'title': 'Standalone Task',
                'description': 'No project'
            }
        )
        assert response.status_code == 201
        assert response.json['title'] == 'Standalone Task'
    
    def test_get_task(self, client, auth_headers, test_task):
        """Test retrieving a specific task"""
        response = client.get(f'/api/tasks/{test_task.id}',
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json['id'] == test_task.id
        assert response.json['title'] == test_task.title
    
    def test_get_tasks_list(self, client, auth_headers, multiple_tasks):
        """Test retrieving list of tasks"""
        response = client.get('/api/tasks',
            headers=auth_headers
        )
        assert response.status_code == 200
        assert 'tasks' in response.json
        assert len(response.json['tasks']) >= 5
    
    def test_get_tasks_with_filters(self, client, auth_headers, multiple_tasks):
        """Test filtering tasks by status"""
        response = client.get('/api/tasks?status=pending',
            headers=auth_headers
        )
        assert response.status_code == 200
        tasks = response.json['tasks']
        assert all(task['status'] == 'pending' for task in tasks)
    
    def test_update_task(self, client, auth_headers, test_task):
        """Test updating a task"""
        response = client.put(f'/api/tasks/{test_task.id}',
            headers=auth_headers,
            json={
                'title': 'Updated Task',
                'status': 'in_progress',
                'priority': 'urgent'
            }
        )
        assert response.status_code == 200
        assert response.json['title'] == 'Updated Task'
        assert response.json['status'] == 'in_progress'
        assert response.json['priority'] == 'urgent'
    
    def test_delete_task(self, client, auth_headers, test_task):
        """Test deleting a task"""
        task_id = test_task.id
        response = client.delete(f'/api/tasks/{task_id}',
            headers=auth_headers
        )
        assert response.status_code == 204
        
        # Verify task is deleted
        get_response = client.get(f'/api/tasks/{task_id}',
            headers=auth_headers
        )
        assert get_response.status_code == 404
    
    def test_complete_task(self, client, auth_headers, test_task):
        """Test completing a task"""
        response = client.post(f'/api/tasks/{test_task.id}/complete',
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json['status'] == Task.STATUS_COMPLETED
        assert response.json['completed_at'] is not None

class TestTaskAccessControl:
    """Test task access control"""
    
    def test_access_denied_for_other_user_task(self, client, db_session, test_user):
        """Test that users cannot access other users' tasks"""
        other_user = User(
            username='otheruser',
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
        
        # Try to access with test_user
        response = client.post('/api/auth/login', json={
            'username': test_user.username,
            'password': 'testpassword123'
        })
        token = response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        get_response = client.get(f'/api/tasks/{task.id}', headers=headers)
        assert get_response.status_code == 403
    
    def test_project_member_can_access_task(self, client, db_session, test_user, test_project):
        """Test that project members can access project tasks"""
        # Add another user to project
        other_user = User(
            username='member',
            email='member@test.com',
            role=User.ROLE_CUSTOMER
        )
        other_user.set_password('password123')
        db_session.add(other_user)
        db_session.commit()
        
        test_project.members.append(other_user)
        db_session.commit()
        
        # Create task in project
        task = Task(
            title='Project Task',
            project_id=test_project.id,
            created_by_id=test_user.id
        )
        db_session.add(task)
        db_session.commit()
        
        # Access with member user
        response = client.post('/api/auth/login', json={
            'username': other_user.username,
            'password': 'password123'
        })
        token = response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        get_response = client.get(f'/api/tasks/{task.id}', headers=headers)
        assert get_response.status_code == 200

class TestTaskPagination:
    """Test pagination functionality"""
    
    def test_pagination_defaults(self, client, auth_headers, multiple_tasks):
        """Test default pagination"""
        response = client.get('/api/tasks', headers=auth_headers)
        assert response.status_code == 200
        assert 'pagination' in response.json
        assert response.json['pagination']['page'] == 1
        assert response.json['pagination']['per_page'] == 20
    
    def test_pagination_custom_page(self, client, auth_headers, multiple_tasks):
        """Test custom page number"""
        response = client.get('/api/tasks?page=1&per_page=2', headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json['tasks']) <= 2
    
    def test_pagination_max_per_page(self, client, auth_headers, multiple_tasks):
        """Test max per page limit"""
        response = client.get('/api/tasks?per_page=200', headers=auth_headers)
        assert response.status_code == 200
        assert response.json['pagination']['per_page'] <= 100

class TestTaskFilters:
    """Test task filtering"""
    
    def test_filter_by_status(self, client, auth_headers, multiple_tasks):
        """Test filtering by status"""
        response = client.get('/api/tasks?status=in_progress', headers=auth_headers)
        assert response.status_code == 200
        tasks = response.json['tasks']
        assert all(task['status'] == 'in_progress' for task in tasks)
    
    def test_filter_by_priority(self, client, auth_headers, multiple_tasks):
        """Test filtering by priority"""
        # Update a task to high priority
        task = multiple_tasks[0]
        client.put(f'/api/tasks/{task.id}',
            headers=auth_headers,
            json={'priority': 'high'}
        )
        
        response = client.get('/api/tasks?priority=high', headers=auth_headers)
        assert response.status_code == 200
        tasks = response.json['tasks']
        assert all(task['priority'] == 'high' for task in tasks)
    
    def test_filter_by_project(self, client, auth_headers, test_project, multiple_tasks):
        """Test filtering by project"""
        response = client.get(f'/api/tasks?project_id={test_project.id}', headers=auth_headers)
        assert response.status_code == 200
        tasks = response.json['tasks']
        assert all(task['project_id'] == test_project.id for task in tasks)

class TestTaskAssignment:
    """Test task assignment functionality"""
    
    def test_assign_task_to_user(self, client, auth_headers, test_task, test_agent):
        """Test assigning task to a user"""
        response = client.put(f'/api/tasks/{test_task.id}',
            headers=auth_headers,
            json={'assigned_to_id': test_agent.id}
        )
        assert response.status_code == 200
        assert response.json['assigned_to_id'] == test_agent.id
    
    def test_unassign_task(self, client, auth_headers, test_task, test_agent):
        """Test unassigning a task"""
        # First assign
        client.put(f'/api/tasks/{test_task.id}',
            headers=auth_headers,
            json={'assigned_to_id': test_agent.id}
        )
        
        # Then unassign
        response = client.put(f'/api/tasks/{test_task.id}',
            headers=auth_headers,
            json={'assigned_to_id': None}
        )
        assert response.status_code == 200
        assert response.json['assigned_to_id'] is None
    
    def test_update_task_with_due_date(self, client, auth_headers, test_task):
        """Test updating task with due date"""
        from datetime import datetime, timedelta
        due_date = (datetime.utcnow() + timedelta(days=7)).isoformat()
        
        response = client.put(f'/api/tasks/{test_task.id}',
            headers=auth_headers,
            json={'due_date': due_date}
        )
        assert response.status_code == 200
        assert response.json['due_date'] is not None
    
    def test_filter_tasks_by_assigned_user(self, client, auth_headers, test_task, test_agent):
        """Test filtering tasks by assigned user"""
        # Assign task to agent
        client.put(f'/api/tasks/{test_task.id}',
            headers=auth_headers,
            json={'assigned_to_id': test_agent.id}
        )
        
        response = client.get(f'/api/tasks?assigned_to_id={test_agent.id}',
            headers=auth_headers
        )
        assert response.status_code == 200
        tasks = response.json['tasks']
        assert all(task['assigned_to_id'] == test_agent.id for task in tasks)
    
    def test_task_with_comments(self, client, auth_headers, test_task):
        """Test task with comments"""
        # Create comment
        client.post(f'/api/tasks/{test_task.id}/comments',
            headers=auth_headers,
            json={'content': 'Test comment'}
        )
        
        # Get task - should include comment count
        response = client.get(f'/api/tasks/{test_task.id}',
            headers=auth_headers
        )
        assert response.status_code == 200
