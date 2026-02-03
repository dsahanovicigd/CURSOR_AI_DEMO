"""Model method tests"""
import pytest
from app.models import (
    User, Task, Project, Team, Notification,
    Ticket, TicketComment, TicketAttachment,
    TaskComment, Post
)
from datetime import datetime, timedelta

class TestUserModel:
    """Test User model methods"""
    
    def test_user_password_hashing(self, db_session):
        """Test password hashing"""
        user = User(
            username='testuser',
            email='test@test.com',
            role=User.ROLE_CUSTOMER
        )
        user.set_password('password123')
        db_session.add(user)
        db_session.commit()
        
        assert user.check_password('password123')
        assert not user.check_password('wrongpassword')
    
    def test_user_role_methods(self, db_session):
        """Test user role check methods"""
        customer = User(
            username='customer',
            email='customer@test.com',
            role=User.ROLE_CUSTOMER
        )
        agent = User(
            username='agent',
            email='agent@test.com',
            role=User.ROLE_AGENT
        )
        admin = User(
            username='admin',
            email='admin@test.com',
            role=User.ROLE_ADMIN,
            is_admin=True
        )
        
        assert customer.is_customer()
        assert not customer.is_agent()
        assert not customer.is_admin_user()
        
        assert agent.is_agent()
        assert not agent.is_customer()
        assert not agent.is_admin_user()
        
        assert admin.is_admin_user()
        assert not admin.is_customer()
        assert not admin.is_agent()
    
    def test_user_full_name(self, db_session):
        """Test user full name method"""
        user = User(
            username='testuser',
            email='test@test.com',
            first_name='John',
            last_name='Doe'
        )
        assert user.full_name == 'John Doe'
        
        user2 = User(
            username='testuser2',
            email='test2@test.com',
            name='Jane Smith'
        )
        assert user2.full_name == 'Jane Smith'

class TestTaskModel:
    """Test Task model methods"""
    
    def test_task_mark_completed(self, db_session, test_user):
        """Test marking task as completed"""
        task = Task(
            title='Test Task',
            created_by_id=test_user.id,
            status=Task.STATUS_PENDING
        )
        db_session.add(task)
        db_session.commit()
        
        task.mark_completed()
        db_session.commit()
        
        assert task.status == Task.STATUS_COMPLETED
        assert task.completed_at is not None

class TestProjectModel:
    """Test Project model methods"""
    
    def test_project_add_member(self, db_session, test_user):
        """Test adding member to project"""
        project = Project(
            name='Test Project',
            owner_id=test_user.id
        )
        db_session.add(project)
        
        member = User(
            username='member',
            email='member@test.com',
            role=User.ROLE_CUSTOMER
        )
        member.set_password('password123')
        db_session.add(member)
        db_session.commit()
        
        project.add_member(member, 'admin')
        db_session.commit()
        
        assert member in project.members.all()
        assert project.get_member_role(member) == 'admin'
    
    def test_project_remove_member(self, db_session, test_user):
        """Test removing member from project"""
        project = Project(
            name='Test Project',
            owner_id=test_user.id
        )
        db_session.add(project)
        
        member = User(
            username='member',
            email='member@test.com',
            role=User.ROLE_CUSTOMER
        )
        member.set_password('password123')
        db_session.add(member)
        db_session.commit()
        
        project.add_member(member)
        db_session.commit()
        
        assert member in project.members.all()
        
        project.remove_member(member)
        db_session.commit()
        
        assert member not in project.members.all()
    
    def test_project_to_dict(self, db_session, test_user):
        """Test project to_dict method"""
        project = Project(
            name='Test Project',
            description='Description',
            owner_id=test_user.id
        )
        db_session.add(project)
        db_session.commit()
        
        project_dict = project.to_dict()
        assert project_dict['name'] == 'Test Project'
        assert project_dict['id'] == project.id

class TestTeamModel:
    """Test Team model methods"""
    
    def test_team_add_member(self, db_session, test_user):
        """Test adding member to team"""
        team = Team(
            name='Test Team',
            owner_id=test_user.id
        )
        db_session.add(team)
        
        member = User(
            username='member',
            email='member@test.com',
            role=User.ROLE_CUSTOMER
        )
        member.set_password('password123')
        db_session.add(member)
        db_session.commit()
        
        team.add_member(member, 'admin')
        db_session.commit()
        
        assert member in team.members.all()
        assert team.get_member_role(member) == 'admin'
    
    def test_team_remove_member(self, db_session, test_user):
        """Test removing member from team"""
        team = Team(
            name='Test Team',
            owner_id=test_user.id
        )
        db_session.add(team)
        
        member = User(
            username='member',
            email='member@test.com',
            role=User.ROLE_CUSTOMER
        )
        member.set_password('password123')
        db_session.add(member)
        db_session.commit()
        
        team.add_member(member)
        db_session.commit()
        
        assert member in team.members.all()
        
        team.remove_member(member)
        db_session.commit()
        
        assert member not in team.members.all()
    
    def test_team_to_dict(self, db_session, test_user):
        """Test team to_dict method"""
        team = Team(
            name='Test Team',
            description='Description',
            owner_id=test_user.id
        )
        db_session.add(team)
        db_session.commit()
        
        team_dict = team.to_dict()
        assert team_dict['name'] == 'Test Team'
        assert team_dict['id'] == team.id

class TestTicketModel:
    """Test Ticket model methods"""
    
    def test_ticket_generate_ticket_number(self, db_session):
        """Test ticket number generation"""
        ticket_number = Ticket.generate_ticket_number()
        assert ticket_number.startswith('TICK-')
        assert len(ticket_number) > 10
    
    def test_ticket_calculate_sla_deadlines(self, db_session):
        """Test SLA deadline calculation"""
        ticket = Ticket(
            subject='Test Ticket',
            description='Description',
            customer_email='test@test.com',
            category=Ticket.CATEGORY_GENERAL,
            priority=Ticket.PRIORITY_HIGH
        )
        ticket.calculate_sla_deadlines()
        
        assert ticket.sla_response_deadline is not None
        assert ticket.sla_resolution_deadline is not None
    
    def test_ticket_can_transition_to(self, db_session):
        """Test ticket status transition validation"""
        ticket = Ticket(
            subject='Test Ticket',
            description='Description',
            customer_email='test@test.com',
            category=Ticket.CATEGORY_GENERAL,
            status=Ticket.STATUS_OPEN
        )
        
        assert ticket.can_transition_to(Ticket.STATUS_ASSIGNED)
        assert ticket.can_transition_to(Ticket.STATUS_CLOSED)
        assert not ticket.can_transition_to(Ticket.STATUS_RESOLVED)
    
    def test_ticket_can_reopen(self, db_session):
        """Test ticket reopen validation"""
        ticket = Ticket(
            subject='Test Ticket',
            description='Description',
            customer_email='test@test.com',
            category=Ticket.CATEGORY_GENERAL,
            status=Ticket.STATUS_CLOSED,
            closed_at=datetime.utcnow() - timedelta(days=5)
        )
        
        assert ticket.can_reopen()
        
        ticket.closed_at = datetime.utcnow() - timedelta(days=10)
        assert not ticket.can_reopen()
    
    def test_ticket_is_sla_breached(self, db_session):
        """Test SLA breach check"""
        ticket = Ticket(
            subject='Test Ticket',
            description='Description',
            customer_email='test@test.com',
            category=Ticket.CATEGORY_GENERAL,
            sla_resolution_deadline=datetime.utcnow() - timedelta(days=1)
        )
        
        assert ticket.is_sla_breached()
        
        ticket.status = Ticket.STATUS_RESOLVED
        assert not ticket.is_sla_breached()

class TestNotificationModel:
    """Test Notification model methods"""
    
    def test_notification_mark_as_read(self, db_session, test_user):
        """Test marking notification as read"""
        notification = Notification(
            user_id=test_user.id,
            type=Notification.TYPE_TASK_ASSIGNED,
            title='Test',
            message='Test notification',
            is_read=False
        )
        db_session.add(notification)
        db_session.commit()
        
        assert not notification.is_read
        assert notification.read_at is None
        
        notification.mark_as_read()
        db_session.commit()
        
        assert notification.is_read
        assert notification.read_at is not None
    
    def test_notification_to_dict(self, db_session, test_user):
        """Test notification to_dict method"""
        notification = Notification(
            user_id=test_user.id,
            type=Notification.TYPE_TASK_ASSIGNED,
            title='Test',
            message='Test notification'
        )
        db_session.add(notification)
        db_session.commit()
        
        notification_dict = notification.to_dict()
        assert notification_dict['title'] == 'Test'
        assert notification_dict['id'] == notification.id

class TestTicketAttachmentModel:
    """Test TicketAttachment model methods"""
    
    def test_ticket_attachment_to_dict(self, db_session, test_user):
        """Test attachment to_dict method"""
        ticket = Ticket(
            subject='Test Ticket',
            description='Description',
            customer_email='test@test.com',
            category=Ticket.CATEGORY_GENERAL
        )
        db_session.add(ticket)
        
        attachment = TicketAttachment(
            ticket_id=ticket.id,
            filename='test.txt',
            file_path='/tmp/test.txt',
            file_size=100,
            uploaded_by_id=test_user.id
        )
        db_session.add(attachment)
        db_session.commit()
        
        attachment_dict = attachment.to_dict()
        assert attachment_dict['filename'] == 'test.txt'
        assert attachment_dict['file_size'] == 100
