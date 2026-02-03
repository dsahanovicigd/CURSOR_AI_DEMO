"""Team CRUD operation tests"""
import pytest
from app.models import Team, User

class TestTeamCRUD:
    """Test team CRUD operations"""
    
    def test_create_team(self, client, auth_headers):
        """Test creating a new team"""
        response = client.post('/api/teams',
            headers=auth_headers,
            json={
                'name': 'New Team',
                'description': 'Team description'
            }
        )
        assert response.status_code == 201
        assert response.json['name'] == 'New Team'
        assert 'id' in response.json
    
    def test_get_team(self, client, auth_headers, db_session, test_user):
        """Test retrieving a specific team"""
        team = Team(
            name='Test Team',
            description='Description',
            owner_id=test_user.id
        )
        db_session.add(team)
        db_session.commit()
        
        response = client.get(f'/api/teams/{team.id}',
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json['id'] == team.id
    
    def test_get_teams_list(self, client, auth_headers, db_session, test_user):
        """Test retrieving list of teams"""
        team = Team(
            name='Test Team',
            owner_id=test_user.id
        )
        db_session.add(team)
        db_session.commit()
        
        response = client.get('/api/teams',
            headers=auth_headers
        )
        assert response.status_code == 200
    
    def test_update_team(self, client, auth_headers, db_session, test_user):
        """Test updating a team"""
        team = Team(
            name='Test Team',
            owner_id=test_user.id
        )
        db_session.add(team)
        db_session.commit()
        
        response = client.put(f'/api/teams/{team.id}',
            headers=auth_headers,
            json={'name': 'Updated Team'}
        )
        assert response.status_code == 200
        assert response.json['name'] == 'Updated Team'
    
    def test_delete_team(self, client, auth_headers, db_session, test_user):
        """Test deleting a team"""
        team = Team(
            name='Test Team',
            owner_id=test_user.id
        )
        db_session.add(team)
        db_session.commit()
        
        team_id = team.id
        response = client.delete(f'/api/teams/{team_id}',
            headers=auth_headers
        )
        assert response.status_code in [200, 204]
    
    def test_add_team_member(self, client, auth_headers, db_session, test_user):
        """Test adding a member to team"""
        team = Team(
            name='Test Team',
            owner_id=test_user.id
        )
        db_session.add(team)
        
        new_user = User(
            username='newmember',
            email='newmember@test.com',
            role=User.ROLE_CUSTOMER
        )
        new_user.set_password('password123')
        db_session.add(new_user)
        db_session.commit()
        
        response = client.post(f'/api/teams/{team.id}/members',
            headers=auth_headers,
            json={'user_id': new_user.id}
        )
        assert response.status_code in [200, 201]
    
    def test_remove_team_member(self, client, auth_headers, db_session, test_user):
        """Test removing a member from team"""
        team = Team(
            name='Test Team',
            owner_id=test_user.id
        )
        db_session.add(team)
        
        new_user = User(
            username='removemember',
            email='removemember@test.com',
            role=User.ROLE_CUSTOMER
        )
        new_user.set_password('password123')
        db_session.add(new_user)
        db_session.commit()
        
        team.members.append(new_user)
        db_session.commit()
        
        response = client.delete(f'/api/teams/{team.id}/members/{new_user.id}',
            headers=auth_headers
        )
        assert response.status_code in [200, 204]
    
    def test_get_team_members(self, client, auth_headers, db_session, test_user):
        """Test getting team members"""
        team = Team(
            name='Test Team',
            owner_id=test_user.id
        )
        db_session.add(team)
        db_session.commit()
        
        response = client.get(f'/api/teams/{team.id}/members',
            headers=auth_headers
        )
        assert response.status_code == 200
    
    def test_team_pagination(self, client, auth_headers, db_session, test_user):
        """Test team pagination"""
        team = Team(
            name='Test Team',
            owner_id=test_user.id
        )
        db_session.add(team)
        db_session.commit()
        
        response = client.get('/api/teams?page=1&per_page=10',
            headers=auth_headers
        )
        assert response.status_code == 200
        assert 'pagination' in response.json
    
    def test_team_member_role(self, client, auth_headers, db_session, test_user):
        """Test adding member with specific role"""
        team = Team(
            name='Test Team',
            owner_id=test_user.id
        )
        db_session.add(team)
        
        new_user = User(
            username='adminmember',
            email='adminmember@test.com',
            role=User.ROLE_CUSTOMER
        )
        new_user.set_password('password123')
        db_session.add(new_user)
        db_session.commit()
        
        response = client.post(f'/api/teams/{team.id}/members',
            headers=auth_headers,
            json={'user_id': new_user.id, 'role': 'admin'}
        )
        assert response.status_code in [200, 201]
    
    def test_update_team_description(self, client, auth_headers, db_session, test_user):
        """Test updating team description"""
        team = Team(
            name='Test Team',
            owner_id=test_user.id
        )
        db_session.add(team)
        db_session.commit()
        
        response = client.put(f'/api/teams/{team.id}',
            headers=auth_headers,
            json={'description': 'Updated description'}
        )
        assert response.status_code == 200
        assert response.json['description'] == 'Updated description'
