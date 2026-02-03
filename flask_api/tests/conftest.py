"""Pytest configuration and fixtures"""
import pytest
from app import create_app, db
from app.models import User, Task, Project
from app.cache import cache
from faker import Faker

fake = Faker()

@pytest.fixture(scope='function')
def app():
    """Create application for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        cache.clear()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()

@pytest.fixture(scope='function')
def db_session(app):
    """Create database session"""
    with app.app_context():
        yield db.session

@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    user = User(
        username=fake.user_name(),
        email=fake.email(),
        password_hash='hashed_password',
        role=User.ROLE_CUSTOMER,
        is_active=True
    )
    user.set_password('testpassword123')
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def test_admin(db_session):
    """Create a test admin user"""
    admin = User(
        username='testadmin',
        email='admin@test.com',
        password_hash='hashed_password',
        role=User.ROLE_ADMIN,
        is_admin=True,
        is_active=True
    )
    admin.set_password('adminpassword123')
    db_session.add(admin)
    db_session.commit()
    return admin

@pytest.fixture
def admin_user(db_session):
    """Alias for test_admin fixture"""
    admin = User(
        username='adminuser',
        email='adminuser@test.com',
        password_hash='hashed_password',
        role=User.ROLE_ADMIN,
        is_admin=True,
        is_active=True
    )
    admin.set_password('adminpassword123')
    db_session.add(admin)
    db_session.commit()
    return admin

@pytest.fixture
def other_user(db_session):
    """Create another test user for authorization tests"""
    user = User(
        username=fake.user_name(),
        email=fake.email(),
        password_hash='hashed_password',
        role=User.ROLE_CUSTOMER,
        is_active=True
    )
    user.set_password('testpassword123')
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def test_agent(db_session):
    """Create a test agent user"""
    agent = User(
        username='testagent',
        email='agent@test.com',
        password_hash='hashed_password',
        role=User.ROLE_AGENT,
        is_active=True,
        availability_status=User.AVAILABILITY_AVAILABLE
    )
    agent.set_password('agentpassword123')
    db_session.add(agent)
    db_session.commit()
    return agent

@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers for test user"""
    response = client.post('/api/auth/login', json={
        'username': test_user.username,
        'password': 'testpassword123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def admin_headers(client, test_admin):
    """Get authentication headers for admin user"""
    response = client.post('/api/auth/login', json={
        'username': test_admin.username,
        'password': 'adminpassword123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def test_project(db_session, test_user):
    """Create a test project"""
    project = Project(
        name=fake.company(),
        description=fake.text(),
        owner_id=test_user.id
    )
    db_session.add(project)
    db_session.commit()
    return project

@pytest.fixture
def test_task(db_session, test_user, test_project):
    """Create a test task"""
    task = Task(
        title=fake.sentence(),
        description=fake.text(),
        status=Task.STATUS_PENDING,
        priority=Task.PRIORITY_MEDIUM,
        project_id=test_project.id,
        created_by_id=test_user.id
    )
    db_session.add(task)
    db_session.commit()
    return task

@pytest.fixture
def multiple_tasks(db_session, test_user, test_project):
    """Create multiple test tasks"""
    tasks = []
    for i in range(5):
        task = Task(
            title=f'Test Task {i+1}',
            description=f'Description {i+1}',
            status=Task.STATUS_PENDING if i % 2 == 0 else Task.STATUS_IN_PROGRESS,
            priority=Task.PRIORITY_MEDIUM,
            project_id=test_project.id,
            created_by_id=test_user.id
        )
        db_session.add(task)
        tasks.append(task)
    db_session.commit()
    return tasks
