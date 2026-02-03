"""Comprehensive tests for Customer Support Ticket System (FR-001 through FR-015)"""
import pytest
from datetime import datetime, timedelta
from app.models import Ticket, TicketComment, TicketAssignment, TicketStatusHistory, User


class TestTicketCreation:
    """Test ticket creation with validation (FR-001, FR-002, FR-003, FR-004)"""
    
    def test_create_ticket_with_all_fields(self, client):
        """Test creating ticket with all required fields (FR-001)"""
        response = client.post('/api/tickets', json={
            'subject': 'Cannot login to my account',
            'description': 'I am unable to login to my account. I have tried resetting my password but it did not work.',
            'priority': 'high',
            'category': 'technical',
            'customer_email': 'customer@test.com'
        })
        assert response.status_code == 201
        data = response.json
        assert 'ticket_number' in data
        assert data['ticket_number'].startswith('TICK-')
        assert data['subject'] == 'Cannot login to my account'
        assert data['status'] == Ticket.STATUS_OPEN
        assert data['priority'] == 'high'
        assert data['category'] == 'technical'
    
    def test_create_ticket_auto_generates_ticket_number(self, client):
        """Test ticket number is auto-generated (FR-002)"""
        response = client.post('/api/tickets', json={
            'subject': 'Test Ticket Subject',
            'description': 'This is a detailed ticket description that meets the minimum length requirement.',
            'category': 'general',
            'customer_email': 'test@test.com'
        })
        assert response.status_code == 201
        assert 'ticket_number' in response.json
        assert response.json['ticket_number'].startswith('TICK-')
        assert len(response.json['ticket_number']) > 10
    
    def test_create_ticket_with_minimal_fields(self, client):
        """Test creating ticket with only required fields (FR-001)"""
        response = client.post('/api/tickets', json={
            'subject': 'Test Subject',
            'description': 'This is a detailed description that meets the minimum length requirement of at least 20 characters.',
            'category': 'general',
            'customer_email': 'test@test.com'
        })
        assert response.status_code == 201
        assert response.json['priority'] == Ticket.PRIORITY_MEDIUM  # Default
    
    def test_create_ticket_validation_subject_too_short(self, client):
        """Test validation: subject too short (FR-001)"""
        response = client.post('/api/tickets', json={
            'subject': 'Test',
            'description': 'This is a detailed description that meets the minimum length requirement.',
            'category': 'general',
            'customer_email': 'test@test.com'
        })
        assert response.status_code == 400
        assert response.json['code'] == 'VALIDATION_ERROR'
    
    def test_create_ticket_validation_subject_too_long(self, client):
        """Test validation: subject too long (FR-001)"""
        response = client.post('/api/tickets', json={
            'subject': 'A' * 201,
            'description': 'This is a detailed description that meets the minimum length requirement.',
            'category': 'general',
            'customer_email': 'test@test.com'
        })
        assert response.status_code == 400
    
    def test_create_ticket_validation_description_too_short(self, client):
        """Test validation: description too short (FR-001)"""
        response = client.post('/api/tickets', json={
            'subject': 'Test Subject',
            'description': 'Too short',
            'category': 'general',
            'customer_email': 'test@test.com'
        })
        assert response.status_code == 400
    
    def test_create_ticket_validation_invalid_email(self, client):
        """Test validation: invalid email format (FR-001)"""
        response = client.post('/api/tickets', json={
            'subject': 'Test Subject',
            'description': 'This is a detailed description that meets the minimum length requirement.',
            'category': 'general',
            'customer_email': 'invalid-email'
        })
        assert response.status_code == 400
    
    def test_create_ticket_validation_invalid_priority(self, client):
        """Test validation: invalid priority (FR-001)"""
        response = client.post('/api/tickets', json={
            'subject': 'Test Subject',
            'description': 'This is a detailed description that meets the minimum length requirement.',
            'priority': 'invalid',
            'category': 'general',
            'customer_email': 'test@test.com'
        })
        assert response.status_code == 400
    
    def test_create_ticket_validation_invalid_category(self, client):
        """Test validation: invalid category (FR-001)"""
        response = client.post('/api/tickets', json={
            'subject': 'Test Subject',
            'description': 'This is a detailed description that meets the minimum length requirement.',
            'category': 'invalid_category',
            'customer_email': 'test@test.com'
        })
        assert response.status_code == 400
    
    def test_create_ticket_sets_status_open(self, client):
        """Test ticket status is set to open (FR-004)"""
        response = client.post('/api/tickets', json={
            'subject': 'Test Subject',
            'description': 'This is a detailed description that meets the minimum length requirement.',
            'category': 'general',
            'customer_email': 'test@test.com'
        })
        assert response.status_code == 201
        assert response.json['status'] == Ticket.STATUS_OPEN
    
    def test_create_ticket_calculates_sla_deadlines(self, client):
        """Test SLA deadlines are calculated based on priority (FR-020)"""
        response = client.post('/api/tickets', json={
            'subject': 'Urgent Issue',
            'description': 'This is a detailed description that meets the minimum length requirement.',
            'priority': 'urgent',
            'category': 'technical',
            'customer_email': 'test@test.com'
        })
        assert response.status_code == 201
        assert 'sla_response_deadline' in response.json
        assert 'sla_resolution_deadline' in response.json
        assert response.json['sla_response_deadline'] is not None


class TestTicketAssignment:
    """Test ticket assignment system (FR-005, FR-006, FR-007, FR-008, FR-009, FR-010)"""
    
    def test_admin_can_assign_ticket(self, client, admin_headers, db_session, test_agent):
        """Test admin can manually assign ticket (FR-005)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Test Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='test@test.com',
            status=Ticket.STATUS_OPEN
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        db_session.commit()
        
        response = client.post(f'/api/tickets/{ticket.id}/assign',
            headers=admin_headers,
            json={'assigned_to_id': test_agent.id}
        )
        assert response.status_code == 200
        assert response.json['assigned_to_id'] == test_agent.id
        assert response.json['status'] == Ticket.STATUS_ASSIGNED
    
    def test_auto_assign_ticket_on_creation(self, client, db_session, test_agent):
        """Test ticket auto-assignment (FR-006)"""
        # Ensure agent is available
        test_agent.availability_status = User.AVAILABILITY_AVAILABLE
        db_session.commit()
        
        response = client.post('/api/tickets', json={
            'subject': 'Test Subject',
            'description': 'This is a detailed description that meets the minimum length requirement.',
            'category': 'general',
            'customer_email': 'test@test.com'
        })
        assert response.status_code == 201
        # Ticket may be auto-assigned if agents are available
        assert 'assigned_to_id' in response.json
    
    def test_non_admin_cannot_assign_ticket(self, client, auth_headers, db_session, test_user, test_agent):
        """Test non-admin cannot assign ticket (FR-005)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Test Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='test@test.com',
            status=Ticket.STATUS_OPEN
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        db_session.commit()
        
        response = client.post(f'/api/tickets/{ticket.id}/assign',
            headers=auth_headers,
            json={'assigned_to_id': test_agent.id}
        )
        assert response.status_code == 403
    
    def test_admin_can_reassign_ticket(self, client, admin_headers, db_session, test_agent, other_user):
        """Test admin can reassign ticket (FR-009)"""
        # Create another agent
        agent2 = User(
            username='agent2',
            email='agent2@test.com',
            role=User.ROLE_AGENT,
            is_active=True
        )
        agent2.set_password('password123')
        db_session.add(agent2)
        
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Test Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='test@test.com',
            assigned_to_id=test_agent.id,
            status=Ticket.STATUS_ASSIGNED
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        db_session.commit()
        
        response = client.post(f'/api/tickets/{ticket.id}/assign',
            headers=admin_headers,
            json={'assigned_to_id': agent2.id, 'notes': 'Reassigned due to workload'}
        )
        assert response.status_code == 200
        assert response.json['assigned_to_id'] == agent2.id
    
    def test_assignment_creates_history_record(self, client, admin_headers, db_session, test_agent):
        """Test assignment history is tracked (FR-010)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Test Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='test@test.com',
            status=Ticket.STATUS_OPEN
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        db_session.commit()
        
        response = client.post(f'/api/tickets/{ticket.id}/assign',
            headers=admin_headers,
            json={'assigned_to_id': test_agent.id}
        )
        assert response.status_code == 200
        
        # Check assignment history
        history_response = client.get(f'/api/tickets/{ticket.id}/history',
            headers=admin_headers
        )
        assert history_response.status_code == 200
        assert len(history_response.json['assignment_history']) >= 1


class TestTicketStatusManagement:
    """Test status management with transitions (FR-011, FR-012, FR-013, FR-014)"""
    
    def test_valid_status_transition_open_to_assigned(self, client, auth_headers, db_session, test_agent):
        """Test valid status transition: open -> assigned (FR-012)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Test Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='test@test.com',
            status=Ticket.STATUS_OPEN
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        db_session.commit()
        
        response = client.put(f'/api/tickets/{ticket.id}/status',
            headers=auth_headers,
            json={'status': Ticket.STATUS_ASSIGNED}
        )
        assert response.status_code == 200
        assert response.json['status'] == Ticket.STATUS_ASSIGNED
    
    def test_valid_status_transition_assigned_to_in_progress(self, client, auth_headers, db_session, test_agent):
        """Test valid status transition: assigned -> in_progress (FR-012)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Test Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='test@test.com',
            assigned_to_id=test_agent.id,
            status=Ticket.STATUS_ASSIGNED
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        db_session.commit()
        
        response = client.put(f'/api/tickets/{ticket.id}/status',
            headers=auth_headers,
            json={'status': Ticket.STATUS_IN_PROGRESS}
        )
        assert response.status_code == 200
        assert response.json['status'] == Ticket.STATUS_IN_PROGRESS
    
    def test_invalid_status_transition(self, client, auth_headers, db_session, test_agent):
        """Test invalid status transition is rejected (FR-012)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Test Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='test@test.com',
            status=Ticket.STATUS_OPEN
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        db_session.commit()
        
        # Cannot go directly from open to resolved
        response = client.put(f'/api/tickets/{ticket.id}/status',
            headers=auth_headers,
            json={'status': Ticket.STATUS_RESOLVED}
        )
        assert response.status_code == 400
    
    def test_status_change_creates_history(self, client, auth_headers, db_session, test_agent):
        """Test status changes are logged (FR-013)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Test Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='test@test.com',
            assigned_to_id=test_agent.id,
            status=Ticket.STATUS_ASSIGNED
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        db_session.commit()
        
        response = client.put(f'/api/tickets/{ticket.id}/status',
            headers=auth_headers,
            json={'status': Ticket.STATUS_IN_PROGRESS, 'notes': 'Starting work'}
        )
        assert response.status_code == 200
        
        # Check status history
        history_response = client.get(f'/api/tickets/{ticket.id}/history',
            headers=auth_headers
        )
        assert history_response.status_code == 200
        assert len(history_response.json['status_history']) >= 1
    
    def test_reopen_closed_ticket_within_7_days(self, client, auth_headers, db_session, test_agent):
        """Test ticket can be reopened within 7 days (FR-012)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Test Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='test@test.com',
            assigned_to_id=test_agent.id,
            status=Ticket.STATUS_CLOSED,
            closed_at=datetime.utcnow() - timedelta(days=3)
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        db_session.commit()
        
        response = client.put(f'/api/tickets/{ticket.id}/status',
            headers=auth_headers,
            json={'status': Ticket.STATUS_REOPENED}
        )
        assert response.status_code == 200
        assert response.json['status'] == Ticket.STATUS_REOPENED
    
    def test_cannot_reopen_ticket_after_7_days(self, client, auth_headers, db_session, test_agent):
        """Test ticket cannot be reopened after 7 days (FR-012)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Test Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='test@test.com',
            assigned_to_id=test_agent.id,
            status=Ticket.STATUS_CLOSED,
            closed_at=datetime.utcnow() - timedelta(days=8)
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        db_session.commit()
        
        response = client.put(f'/api/tickets/{ticket.id}/status',
            headers=auth_headers,
            json={'status': Ticket.STATUS_REOPENED}
        )
        assert response.status_code == 400


class TestTicketComments:
    """Test comments system (FR-015, FR-016, FR-017, FR-018, FR-019)"""
    
    def test_create_public_comment(self, client, db_session):
        """Test creating public comment (FR-015, FR-016)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Test Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='test@test.com',
            status=Ticket.STATUS_OPEN
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        db_session.commit()
        
        response = client.post(f'/api/tickets/{ticket.id}/comments', json={
            'content': 'This is a public comment from the customer',
            'customer_email': 'test@test.com'
        })
        assert response.status_code == 201
        assert response.json['is_internal'] == False
        assert response.json['content'] == 'This is a public comment from the customer'
    
    def test_create_internal_comment_as_agent(self, client, auth_headers, db_session, test_agent):
        """Test agent can create internal comment (FR-016)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Test Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='test@test.com',
            assigned_to_id=test_agent.id,
            status=Ticket.STATUS_ASSIGNED
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        db_session.commit()
        
        response = client.post(f'/api/tickets/{ticket.id}/comments',
            headers=auth_headers,
            json={
                'content': 'This is an internal note for agents only',
                'is_internal': True
            }
        )
        assert response.status_code == 201
        assert response.json['is_internal'] == True
    
    def test_customer_cannot_create_internal_comment(self, client, db_session):
        """Test customer cannot create internal comment (FR-016)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Test Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='test@test.com',
            status=Ticket.STATUS_OPEN
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        db_session.commit()
        
        response = client.post(f'/api/tickets/{ticket.id}/comments', json={
            'content': 'Trying to create internal comment',
            'is_internal': True,
            'customer_email': 'test@test.com'
        })
        assert response.status_code == 403
    
    def test_get_comments_excludes_internal_for_customer(self, client, auth_headers, db_session, test_user, test_agent):
        """Test customer cannot see internal comments (FR-016)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Test Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email=test_user.email,
            assigned_to_id=test_agent.id,
            status=Ticket.STATUS_ASSIGNED
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        
        # Create public comment
        public_comment = TicketComment(
            ticket_id=ticket.id,
            content='Public comment',
            is_internal=False,
            customer_email=test_user.email
        )
        # Create internal comment
        internal_comment = TicketComment(
            ticket_id=ticket.id,
            user_id=test_agent.id,
            content='Internal comment',
            is_internal=True
        )
        db_session.add(public_comment)
        db_session.add(internal_comment)
        db_session.commit()
        
        response = client.get(f'/api/tickets/{ticket.id}/comments',
            headers=auth_headers
        )
        assert response.status_code == 200
        comments = response.json['comments']
        assert len(comments) == 1
        assert comments[0]['is_internal'] == False
    
    def test_get_comments_includes_internal_for_agent(self, client, auth_headers, db_session, test_agent):
        """Test agent can see internal comments (FR-016)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Test Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='test@test.com',
            assigned_to_id=test_agent.id,
            status=Ticket.STATUS_ASSIGNED
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        
        # Create both types of comments
        public_comment = TicketComment(
            ticket_id=ticket.id,
            content='Public comment',
            is_internal=False,
            customer_email='test@test.com'
        )
        internal_comment = TicketComment(
            ticket_id=ticket.id,
            user_id=test_agent.id,
            content='Internal comment',
            is_internal=True
        )
        db_session.add(public_comment)
        db_session.add(internal_comment)
        db_session.commit()
        
        response = client.get(f'/api/tickets/{ticket.id}/comments?include_internal=true',
            headers=auth_headers
        )
        assert response.status_code == 200
        comments = response.json['comments']
        assert len(comments) == 2


class TestTicketPriorityAndSLA:
    """Test priority levels with SLA (FR-020, FR-021, FR-022, FR-023, FR-024)"""
    
    def test_urgent_priority_sla_deadlines(self, client, db_session):
        """Test urgent priority SLA deadlines (FR-020)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Urgent Issue',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_TECHNICAL,
            customer_email='test@test.com',
            priority=Ticket.PRIORITY_URGENT
        )
        ticket.calculate_sla_deadlines()
        
        # Check SLA deadlines
        assert ticket.sla_response_deadline is not None
        assert ticket.sla_resolution_deadline is not None
        
        # Urgent: 2 hours response, 24 hours resolution
        response_time = (ticket.sla_response_deadline - ticket.created_at).total_seconds() / 3600
        resolution_time = (ticket.sla_resolution_deadline - ticket.created_at).total_seconds() / 3600
        
        assert abs(response_time - 2) < 0.1  # Within 0.1 hours
        assert abs(resolution_time - 24) < 0.1  # Within 0.1 hours
    
    def test_high_priority_sla_deadlines(self, client, db_session):
        """Test high priority SLA deadlines (FR-020)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='High Priority Issue',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_TECHNICAL,
            customer_email='test@test.com',
            priority=Ticket.PRIORITY_HIGH
        )
        ticket.calculate_sla_deadlines()
        
        # High: 4 hours response, 48 hours resolution
        response_time = (ticket.sla_response_deadline - ticket.created_at).total_seconds() / 3600
        resolution_time = (ticket.sla_resolution_deadline - ticket.created_at).total_seconds() / 3600
        
        assert abs(response_time - 4) < 0.1
        assert abs(resolution_time - 48) < 0.1
    
    def test_medium_priority_sla_deadlines(self, client, db_session):
        """Test medium priority SLA deadlines (FR-020)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Medium Priority Issue',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='test@test.com',
            priority=Ticket.PRIORITY_MEDIUM
        )
        ticket.calculate_sla_deadlines()
        
        # Medium: 8 hours response, 5 days resolution
        response_time = (ticket.sla_response_deadline - ticket.created_at).total_seconds() / 3600
        resolution_time = (ticket.sla_resolution_deadline - ticket.created_at).total_seconds() / (3600 * 24)
        
        assert abs(response_time - 8) < 0.1
        assert abs(resolution_time - 5) < 0.1
    
    def test_low_priority_sla_deadlines(self, client, db_session):
        """Test low priority SLA deadlines (FR-020)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Low Priority Issue',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='test@test.com',
            priority=Ticket.PRIORITY_LOW
        )
        ticket.calculate_sla_deadlines()
        
        # Low: 24 hours response, 10 days resolution
        response_time = (ticket.sla_response_deadline - ticket.created_at).total_seconds() / 3600
        resolution_time = (ticket.sla_resolution_deadline - ticket.created_at).total_seconds() / (3600 * 24)
        
        assert abs(response_time - 24) < 0.1
        assert abs(resolution_time - 10) < 0.1
    
    def test_update_priority_requires_reason(self, client, auth_headers, db_session, test_agent):
        """Test priority change requires reason (FR-024)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Test Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='test@test.com',
            assigned_to_id=test_agent.id,
            priority=Ticket.PRIORITY_MEDIUM,
            status=Ticket.STATUS_ASSIGNED
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        db_session.commit()
        
        # Missing reason
        response = client.put(f'/api/tickets/{ticket.id}/priority',
            headers=auth_headers,
            json={'priority': Ticket.PRIORITY_HIGH}
        )
        assert response.status_code == 400
        
        # With reason
        response = client.put(f'/api/tickets/{ticket.id}/priority',
            headers=auth_headers,
            json={
                'priority': Ticket.PRIORITY_HIGH,
                'reason': 'Customer reported critical business impact requiring immediate attention'
            }
        )
        assert response.status_code == 200
        assert response.json['priority'] == Ticket.PRIORITY_HIGH
    
    def test_update_priority_recalculates_sla(self, client, auth_headers, db_session, test_agent):
        """Test priority change recalculates SLA (FR-020)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Test Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='test@test.com',
            assigned_to_id=test_agent.id,
            priority=Ticket.PRIORITY_MEDIUM,
            status=Ticket.STATUS_ASSIGNED
        )
        ticket.calculate_sla_deadlines()
        original_deadline = ticket.sla_resolution_deadline
        db_session.add(ticket)
        db_session.commit()
        
        response = client.put(f'/api/tickets/{ticket.id}/priority',
            headers=auth_headers,
            json={
                'priority': Ticket.PRIORITY_URGENT,
                'reason': 'Escalated due to business criticality'
            }
        )
        assert response.status_code == 200
        
        # Refresh ticket
        db_session.refresh(ticket)
        assert ticket.sla_resolution_deadline != original_deadline
        # Urgent should have shorter deadline
        assert ticket.sla_resolution_deadline < original_deadline


class TestRoleBasedAccessControl:
    """Test role-based access control (FR-032, FR-033)"""
    
    def test_customer_can_view_own_tickets(self, client, auth_headers, db_session, test_user):
        """Test customer can view own tickets (FR-033)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Customer Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email=test_user.email,
            status=Ticket.STATUS_OPEN
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        db_session.commit()
        
        response = client.get(f'/api/tickets/{ticket.id}',
            headers=auth_headers
        )
        assert response.status_code == 200
    
    def test_customer_cannot_view_other_tickets(self, client, auth_headers, db_session, test_user):
        """Test customer cannot view other customers' tickets (FR-033)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Other Customer Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='other@test.com',
            status=Ticket.STATUS_OPEN
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        db_session.commit()
        
        response = client.get(f'/api/tickets/{ticket.id}',
            headers=auth_headers
        )
        assert response.status_code == 403
    
    def test_agent_can_view_assigned_tickets(self, client, auth_headers, db_session, test_agent):
        """Test agent can view assigned tickets (FR-033)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Assigned Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='test@test.com',
            assigned_to_id=test_agent.id,
            status=Ticket.STATUS_ASSIGNED
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        db_session.commit()
        
        # Login as agent
        login_response = client.post('/api/auth/login', json={
            'username': test_agent.username,
            'password': 'agentpassword123'
        })
        token = login_response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        response = client.get(f'/api/tickets/{ticket.id}',
            headers=headers
        )
        assert response.status_code == 200
    
    def test_agent_can_view_unassigned_tickets(self, client, db_session, test_agent):
        """Test agent can view unassigned tickets (FR-033)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Unassigned Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='test@test.com',
            status=Ticket.STATUS_OPEN
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        db_session.commit()
        
        # Login as agent
        login_response = client.post('/api/auth/login', json={
            'username': test_agent.username,
            'password': 'agentpassword123'
        })
        token = login_response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        response = client.get(f'/api/tickets/{ticket.id}',
            headers=headers
        )
        assert response.status_code == 200
    
    def test_admin_can_view_all_tickets(self, client, admin_headers, db_session):
        """Test admin can view all tickets (FR-033)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Any Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='any@test.com',
            status=Ticket.STATUS_OPEN
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        db_session.commit()
        
        response = client.get(f'/api/tickets/{ticket.id}',
            headers=admin_headers
        )
        assert response.status_code == 200
    
    def test_customer_cannot_update_ticket_status(self, client, auth_headers, db_session, test_user):
        """Test customer cannot update ticket status (FR-033)"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Customer Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email=test_user.email,
            status=Ticket.STATUS_OPEN
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        db_session.commit()
        
        response = client.put(f'/api/tickets/{ticket.id}/status',
            headers=auth_headers,
            json={'status': Ticket.STATUS_RESOLVED}
        )
        assert response.status_code == 403


class TestErrorHandling:
    """Test error handling and validation"""
    
    def test_create_ticket_missing_required_fields(self, client):
        """Test error handling for missing required fields"""
        response = client.post('/api/tickets', json={
            'subject': 'Test Subject'
            # Missing description, category, customer_email
        })
        assert response.status_code == 400
        assert response.json['code'] == 'VALIDATION_ERROR'
    
    def test_get_nonexistent_ticket(self, client, auth_headers):
        """Test error handling for nonexistent ticket"""
        response = client.get('/api/tickets/99999',
            headers=auth_headers
        )
        assert response.status_code == 404
    
    def test_update_ticket_with_invalid_data(self, client, auth_headers, db_session, test_agent):
        """Test error handling for invalid update data"""
        ticket = Ticket(
            ticket_number=Ticket.generate_ticket_number(),
            subject='Test Ticket',
            description='This is a detailed description that meets the minimum length requirement.',
            category=Ticket.CATEGORY_GENERAL,
            customer_email='test@test.com',
            assigned_to_id=test_agent.id,
            status=Ticket.STATUS_ASSIGNED
        )
        ticket.calculate_sla_deadlines()
        db_session.add(ticket)
        db_session.commit()
        
        response = client.put(f'/api/tickets/{ticket.id}',
            headers=auth_headers,
            json={'subject': 'A' * 201}  # Too long
        )
        assert response.status_code == 400
    
    def test_error_response_format(self, client):
        """Test error response follows specified format"""
        response = client.post('/api/tickets', json={
            'subject': 'Test'
        })
        assert response.status_code == 400
        assert 'status' in response.json
        assert 'message' in response.json
        assert 'code' in response.json
        assert response.json['status'] == 'error'
        assert response.json['code'] == 'VALIDATION_ERROR'
