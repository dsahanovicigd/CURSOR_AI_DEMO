"""Ticket CRUD operation tests"""
import pytest
from app.models import Ticket, User

class TestTicketCRUD:
    """Test ticket CRUD operations"""
    
    def test_create_ticket_public(self, client):
        """Test creating a ticket (public endpoint)"""
        response = client.post('/api/tickets',
            json={
                'subject': 'Test Ticket Subject',
                'description': 'This is a detailed ticket description that meets the minimum length requirement of at least 20 characters.',
                'customer_email': 'customer@test.com',
                'priority': 'medium',
                'category': 'general'
            }
        )
        assert response.status_code == 201
        assert response.json['subject'] == 'Test Ticket Subject'
        assert 'ticket_number' in response.json
    
    def test_get_ticket(self, client, auth_headers, db_session, test_user):
        """Test retrieving a specific ticket"""
        ticket = Ticket(
            subject='Test Ticket Subject',
            description='This is a detailed ticket description that meets the minimum length requirement.',
            customer_email=test_user.email,
            status=Ticket.STATUS_OPEN,
            category=Ticket.CATEGORY_GENERAL
        )
        db_session.add(ticket)
        db_session.commit()
        
        response = client.get(f'/api/tickets/{ticket.id}',
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json['id'] == ticket.id
    
    def test_get_tickets_list(self, client, auth_headers, db_session, test_user):
        """Test retrieving list of tickets"""
        ticket = Ticket(
            subject='Test Ticket Subject',
            description='This is a detailed ticket description that meets the minimum length requirement.',
            customer_email=test_user.email,
            status=Ticket.STATUS_OPEN,
            category=Ticket.CATEGORY_GENERAL
        )
        db_session.add(ticket)
        db_session.commit()
        
        response = client.get('/api/tickets', headers=auth_headers)
        assert response.status_code == 200
    
    def test_update_ticket_status(self, client, auth_headers, db_session, test_agent):
        """Test updating ticket status"""
        ticket = Ticket(
            subject='Test Ticket Subject',
            description='This is a detailed ticket description that meets the minimum length requirement.',
            customer_email='test@test.com',
            status=Ticket.STATUS_OPEN,
            assigned_to_id=test_agent.id,
            category=Ticket.CATEGORY_GENERAL
        )
        db_session.add(ticket)
        db_session.commit()
        
        # Login as agent
        login_response = client.post('/api/auth/login', json={
            'username': test_agent.username,
            'password': 'agentpassword123'
        })
        token = login_response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        response = client.put(f'/api/tickets/{ticket.id}/status',
            headers=headers,
            json={'status': Ticket.STATUS_IN_PROGRESS}
        )
        assert response.status_code == 200
        assert response.json['status'] == Ticket.STATUS_IN_PROGRESS
    
    def test_update_ticket_priority(self, client, auth_headers, db_session, test_agent):
        """Test updating ticket priority"""
        ticket = Ticket(
            subject='Test Ticket Subject',
            description='This is a detailed ticket description that meets the minimum length requirement.',
            customer_email='test@test.com',
            assigned_to_id=test_agent.id,
            category=Ticket.CATEGORY_GENERAL
        )
        db_session.add(ticket)
        db_session.commit()
        
        # Login as agent
        login_response = client.post('/api/auth/login', json={
            'username': test_agent.username,
            'password': 'agentpassword123'
        })
        token = login_response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        response = client.put(f'/api/tickets/{ticket.id}/priority',
            headers=headers,
            json={'priority': 'high', 'reason': 'Customer request for urgent assistance'}
        )
        assert response.status_code == 200
        assert response.json['priority'] == 'high'
    
    def test_assign_ticket(self, client, admin_headers, db_session, test_agent):
        """Test assigning ticket to agent"""
        ticket = Ticket(
            subject='Test Ticket Subject',
            description='This is a detailed ticket description that meets the minimum length requirement.',
            customer_email='test@test.com',
            category=Ticket.CATEGORY_GENERAL
        )
        db_session.add(ticket)
        db_session.commit()
        
        response = client.post(f'/api/tickets/{ticket.id}/assign',
            headers=admin_headers,
            json={'assigned_to_id': test_agent.id}
        )
        assert response.status_code == 200
        assert response.json['assigned_to_id'] == test_agent.id
    
    def test_get_ticket_history(self, client, auth_headers, db_session):
        """Test getting ticket history"""
        ticket = Ticket(
            subject='Test Ticket Subject',
            description='This is a detailed ticket description that meets the minimum length requirement.',
            customer_email='test@test.com',
            category=Ticket.CATEGORY_GENERAL
        )
        db_session.add(ticket)
        db_session.commit()
        
        response = client.get(f'/api/tickets/{ticket.id}/history',
            headers=auth_headers
        )
        assert response.status_code == 200
