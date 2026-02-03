"""Background task tests"""
import pytest
from app.tasks.background_tasks import (
    send_task_notification,
    send_task_assignment_email,
    update_task_statistics,
    cleanup_old_notifications,
    process_due_date_reminders
)
from app.models import Task, User, Notification
from datetime import datetime, timedelta

class TestBackgroundTasks:
    """Test background task execution"""
    
    def test_send_task_notification(self, app, db_session, test_user):
        """Test sending task notification"""
        with app.app_context():
            task = Task(
                title='Test Task',
                created_by_id=test_user.id
            )
            db_session.add(task)
            db_session.commit()
            
            result = send_task_notification.run(
                task.id,
                test_user.id,
                Notification.TYPE_TASK_ASSIGNED,
                'Test notification'
            )
            
            assert result['status'] == 'success'
            assert 'notification_id' in result
    
    def test_send_task_assignment_email(self, app):
        """Test sending assignment email"""
        with app.app_context():
            result = send_task_assignment_email.run(1, 'test@example.com')
            assert result['status'] == 'success'
            assert result['email'] == 'test@example.com'
    
    def test_update_task_statistics(self, app, db_session, test_user):
        """Test updating task statistics"""
        with app.app_context():
            # Create various tasks
            task1 = Task(
                title='Pending Task',
                status=Task.STATUS_PENDING,
                created_by_id=test_user.id
            )
            task2 = Task(
                title='In Progress Task',
                status=Task.STATUS_IN_PROGRESS,
                created_by_id=test_user.id
            )
            task3 = Task(
                title='Completed Task',
                status=Task.STATUS_COMPLETED,
                created_by_id=test_user.id
            )
            db_session.add_all([task1, task2, task3])
            db_session.commit()
            
            result = update_task_statistics.run()
            assert result['status'] == 'success'
            assert 'statistics' in result
            stats = result['statistics']
            assert stats['total_tasks'] >= 3
    
    def test_cleanup_old_notifications(self, app, db_session, test_user):
        """Test cleaning up old notifications"""
        with app.app_context():
            # Create old notification
            old_notification = Notification(
                user_id=test_user.id,
                type=Notification.TYPE_TASK_ASSIGNED,
                title='Old',
                message='Old notification',
                created_at=datetime.utcnow() - timedelta(days=31)
            )
            db_session.add(old_notification)
            
            # Create recent notification
            recent_notification = Notification(
                user_id=test_user.id,
                type=Notification.TYPE_TASK_ASSIGNED,
                title='Recent',
                message='Recent notification',
                created_at=datetime.utcnow() - timedelta(days=5)
            )
            db_session.add(recent_notification)
            db_session.commit()
            
            result = cleanup_old_notifications.run(days=30)
            assert result['status'] == 'success'
            assert result['deleted_count'] >= 1
    
    def test_process_due_date_reminders(self, app, db_session, test_user):
        """Test processing due date reminders"""
        with app.app_context():
            from datetime import datetime, timedelta
            # Create task due tomorrow
            task = Task(
                title='Due Soon Task',
                created_by_id=test_user.id,
                assigned_to_id=test_user.id,
                due_date=datetime.utcnow() + timedelta(days=1),
                status=Task.STATUS_IN_PROGRESS
            )
            db_session.add(task)
            db_session.commit()
            
            result = process_due_date_reminders.run()
            assert result['status'] == 'success'
            assert 'notifications_sent' in result
