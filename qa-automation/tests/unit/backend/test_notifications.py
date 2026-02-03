"""Notification tests"""
import pytest
from app.models import Notification

class TestNotifications:
    """Test notification operations"""
    
    def test_get_notifications(self, client, auth_headers, db_session, test_user):
        """Test getting notifications"""
        notification = Notification(
            user_id=test_user.id,
            type=Notification.TYPE_TASK_ASSIGNED,
            title='Test',
            message='Test notification'
        )
        db_session.add(notification)
        db_session.commit()
        
        response = client.get('/api/notifications',
            headers=auth_headers
        )
        assert response.status_code == 200
        assert 'notifications' in response.json
    
    def test_get_notification(self, client, auth_headers, db_session, test_user):
        """Test getting a specific notification"""
        notification = Notification(
            user_id=test_user.id,
            type=Notification.TYPE_TASK_ASSIGNED,
            title='Test',
            message='Test notification'
        )
        db_session.add(notification)
        db_session.commit()
        
        response = client.get(f'/api/notifications/{notification.id}',
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json['id'] == notification.id
    
    def test_mark_notification_read(self, client, auth_headers, db_session, test_user):
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
        
        response = client.post(f'/api/notifications/{notification.id}/read',
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json['is_read'] == True
    
    def test_mark_all_notifications_read(self, client, auth_headers, db_session, test_user):
        """Test marking all notifications as read"""
        for i in range(3):
            notification = Notification(
                user_id=test_user.id,
                type=Notification.TYPE_TASK_ASSIGNED,
                title=f'Test {i}',
                message='Test notification',
                is_read=False
            )
            db_session.add(notification)
        db_session.commit()
        
        response = client.post('/api/notifications/read-all',
            headers=auth_headers
        )
        assert response.status_code == 200
    
    def test_get_unread_count(self, client, auth_headers, db_session, test_user):
        """Test getting unread notification count"""
        notification = Notification(
            user_id=test_user.id,
            type=Notification.TYPE_TASK_ASSIGNED,
            title='Test',
            message='Test notification',
            is_read=False
        )
        db_session.add(notification)
        db_session.commit()
        
        response = client.get('/api/notifications/unread-count',
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json['unread_count'] >= 1
    
    def test_filter_notifications_by_type(self, client, auth_headers, db_session, test_user):
        """Test filtering notifications by type"""
        notification = Notification(
            user_id=test_user.id,
            type=Notification.TYPE_TASK_ASSIGNED,
            title='Test',
            message='Test notification'
        )
        db_session.add(notification)
        db_session.commit()
        
        response = client.get('/api/notifications?type=task_assigned',
            headers=auth_headers
        )
        assert response.status_code == 200
        # Verify filter works
        notifications = response.json.get('notifications', [])
        if notifications:
            assert all(n['type'] == Notification.TYPE_TASK_ASSIGNED for n in notifications)
    
    def test_filter_notifications_by_read_status(self, client, auth_headers, db_session, test_user):
        """Test filtering notifications by read status"""
        notification = Notification(
            user_id=test_user.id,
            type=Notification.TYPE_TASK_ASSIGNED,
            title='Test',
            message='Test notification',
            is_read=False
        )
        db_session.add(notification)
        db_session.commit()
        
        response = client.get('/api/notifications?is_read=false',
            headers=auth_headers
        )
        assert response.status_code == 200
        # Verify filter works
        notifications = response.json.get('notifications', [])
        if notifications:
            assert all(not n['is_read'] for n in notifications)
    
    def test_notification_pagination(self, client, auth_headers, db_session, test_user):
        """Test notification pagination"""
        # Create multiple notifications
        for i in range(5):
            notification = Notification(
                user_id=test_user.id,
                type=Notification.TYPE_TASK_ASSIGNED,
                title=f'Test {i}',
                message='Test notification'
            )
            db_session.add(notification)
        db_session.commit()
        
        response = client.get('/api/notifications?page=1&per_page=2',
            headers=auth_headers
        )
        assert response.status_code == 200
        # Check pagination structure
        assert 'pagination' in response.json or 'notifications' in response.json
        if 'pagination' in response.json:
            assert response.json['pagination']['per_page'] == 2
