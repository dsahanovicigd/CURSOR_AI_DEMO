"""Project CRUD operation tests"""
import pytest
from app.models import Project, User, Task

class TestProjectCRUD:
    """Test project CRUD operations"""
    
    def test_create_project(self, client, auth_headers):
        """Test creating a new project"""
        response = client.post('/api/projects',
            headers=auth_headers,
            json={
                'name': 'New Project',
                'description': 'Project description'
            }
        )
        assert response.status_code == 201
        assert response.json['name'] == 'New Project'
        assert 'id' in response.json
    
    def test_get_project(self, client, auth_headers, test_project):
        """Test retrieving a specific project"""
        response = client.get(f'/api/projects/{test_project.id}',
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json['id'] == test_project.id
        assert response.json['name'] == test_project.name
    
    def test_get_projects_list(self, client, auth_headers, test_project):
        """Test retrieving list of projects"""
        response = client.get('/api/projects',
            headers=auth_headers
        )
        assert response.status_code == 200
        assert 'projects' in response.json or isinstance(response.json, list)
    
    def test_update_project(self, client, auth_headers, test_project):
        """Test updating a project"""
        response = client.put(f'/api/projects/{test_project.id}',
            headers=auth_headers,
            json={
                'name': 'Updated Project',
                'description': 'Updated description'
            }
        )
        assert response.status_code == 200
        assert response.json['name'] == 'Updated Project'
    
    def test_delete_project(self, client, auth_headers, test_project):
        """Test deleting a project"""
        project_id = test_project.id
        response = client.delete(f'/api/projects/{project_id}',
            headers=auth_headers
        )
        assert response.status_code in [200, 204]
        
        # Verify project is deleted
        get_response = client.get(f'/api/projects/{project_id}',
            headers=auth_headers
        )
        assert get_response.status_code == 404
    
    def test_get_project_members(self, client, auth_headers, test_project):
        """Test getting project members"""
        response = client.get(f'/api/projects/{test_project.id}/members',
            headers=auth_headers
        )
        assert response.status_code == 200
    
    def test_add_project_member(self, client, auth_headers, test_project, db_session):
        """Test adding a member to project"""
        # Create another user
        new_user = User(
            username='newmember',
            email='newmember@test.com',
            role=User.ROLE_CUSTOMER
        )
        new_user.set_password('password123')
        db_session.add(new_user)
        db_session.commit()
        
        response = client.post(f'/api/projects/{test_project.id}/members',
            headers=auth_headers,
            json={'user_id': new_user.id}
        )
        assert response.status_code in [200, 201]
    
    def test_remove_project_member(self, client, auth_headers, test_project, db_session):
        """Test removing a member from project"""
        # Create and add member
        new_user = User(
            username='removemember',
            email='removemember@test.com',
            role=User.ROLE_CUSTOMER
        )
        new_user.set_password('password123')
        db_session.add(new_user)
        db_session.commit()
        
        test_project.members.append(new_user)
        db_session.commit()
        
        response = client.delete(f'/api/projects/{test_project.id}/members/{new_user.id}',
            headers=auth_headers
        )
        assert response.status_code in [200, 204]
    
    def test_access_denied_for_other_user_project(self, client, db_session, test_user):
        """Test that users cannot access other users' projects"""
        other_user = User(
            username='otheruser',
            email='other@test.com',
            role=User.ROLE_CUSTOMER
        )
        other_user.set_password('password123')
        db_session.add(other_user)
        db_session.commit()
        
        # Create project for other user
        project = Project(
            name='Other User Project',
            owner_id=other_user.id
        )
        db_session.add(project)
        db_session.commit()
        
        # Try to access with test_user
        response = client.post('/api/auth/login', json={
            'username': test_user.username,
            'password': 'testpassword123'
        })
        token = response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        get_response = client.get(f'/api/projects/{project.id}', headers=headers)
        assert get_response.status_code == 403
    
    def test_project_with_tasks(self, client, auth_headers, test_project, db_session, test_user):
        """Test project with associated tasks"""
        # Create task in project
        task = Task(
            title='Project Task',
            project_id=test_project.id,
            created_by_id=test_user.id
        )
        db_session.add(task)
        db_session.commit()
        
        response = client.get(f'/api/projects/{test_project.id}',
            headers=auth_headers
        )
        assert response.status_code == 200
    
    def test_project_filter_by_status(self, client, auth_headers, test_project):
        """Test filtering projects by status"""
        response = client.get('/api/projects?status=active',
            headers=auth_headers
        )
        assert response.status_code == 200
    
    def test_project_pagination(self, client, auth_headers, test_project):
        """Test project pagination"""
        response = client.get('/api/projects?page=1&per_page=10',
            headers=auth_headers
        )
        assert response.status_code == 200
        assert 'pagination' in response.json
    
    def test_create_project_with_team(self, client, auth_headers, db_session, test_user):
        """Test creating project with team"""
        from app.models import Team
        
        team = Team(
            name='Test Team',
            owner_id=test_user.id
        )
        db_session.add(team)
        db_session.commit()
        
        response = client.post('/api/projects',
            headers=auth_headers,
            json={
                'name': 'Team Project',
                'team_id': team.id
            }
        )
        assert response.status_code == 201
        assert response.json['team_id'] == team.id
    
    def test_update_project_status(self, client, auth_headers, test_project):
        """Test updating project status"""
        response = client.put(f'/api/projects/{test_project.id}',
            headers=auth_headers,
            json={'status': 'archived'}
        )
        assert response.status_code == 200
        assert response.json['status'] == 'archived'
    
    def test_project_member_role(self, client, auth_headers, test_project, db_session):
        """Test adding member with specific role"""
        new_user = User(
            username='adminmember',
            email='adminmember@test.com',
            role=User.ROLE_CUSTOMER
        )
        new_user.set_password('password123')
        db_session.add(new_user)
        db_session.commit()
        
        response = client.post(f'/api/projects/{test_project.id}/members',
            headers=auth_headers,
            json={'user_id': new_user.id, 'role': 'admin'}
        )
        assert response.status_code in [200, 201]
