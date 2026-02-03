"""Ticket comment tests"""
import pytest
from app.models import TicketComment, Ticket

class TestTicketComments:
    """Test ticket comment operations"""
    
    def test_get_ticket_comments(self, client, auth_headers, db_session, test_user):
        """Test getting comments for a ticket"""
        ticket = Ticket(
            subject='Test Ticket Subject',
            description='This is a detailed ticket description that meets the minimum length requirement.',
            customer_email=test_user.email,
            category=Ticket.CATEGORY_GENERAL
        )
        db_session.add(ticket)
        db_session.commit()
        
        response = client.get(f'/api/tickets/{ticket.id}/comments',
            headers=auth_headers
        )
        assert response.status_code == 200
    
    def test_create_ticket_comment_public(self, client, db_session):
        """Test creating a public comment on a ticket"""
        ticket = Ticket(
            subject='Test Ticket Subject',
            description='This is a detailed ticket description that meets the minimum length requirement.',
            customer_email='test@test.com',
            category=Ticket.CATEGORY_GENERAL
        )
        db_session.add(ticket)
        db_session.commit()
        
        response = client.post(f'/api/tickets/{ticket.id}/comments',
            json={
                'content': 'Public comment on ticket',
                'customer_email': 'test@test.com'
            }
        )
        assert response.status_code == 201
        assert response.json['content'] == 'Public comment on ticket'
    
    def test_create_ticket_comment_internal(self, client, auth_headers, db_session, test_agent):
        """Test creating an internal comment"""
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
        
        response = client.post(f'/api/tickets/{ticket.id}/comments',
            headers=headers,
            json={
                'content': 'Internal comment for agents only',
                'is_internal': True
            }
        )
        assert response.status_code == 201
        assert response.json['is_internal'] == True
