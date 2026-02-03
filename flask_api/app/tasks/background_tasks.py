"""Background tasks using Celery"""
from app.celery_app import celery
from app import db
from app.models.task import Task
from app.models.notification import Notification
from app.models.user import User
from app.cache import invalidate_task_cache
from datetime import datetime, timedelta

@celery.task(name='tasks.send_task_notification')
def send_task_notification(task_id, user_id, notification_type, message):
    """Send notification about task update"""
    try:
        notification = Notification(
            user_id=user_id,
            type=notification_type,
            title=f'Task Update',
            message=message,
            related_task_id=task_id
        )
        db.session.add(notification)
        db.session.commit()
        return {'status': 'success', 'notification_id': notification.id}
    except Exception as e:
        db.session.rollback()
        return {'status': 'error', 'error': str(e)}

@celery.task(name='tasks.send_task_assignment_email')
def send_task_assignment_email(task_id, user_email):
    """Send email notification for task assignment (placeholder)"""
    # In production, integrate with email service (SendGrid, SES, etc.)
    print(f"Sending assignment email to {user_email} for task {task_id}")
    return {'status': 'success', 'task_id': task_id, 'email': user_email}

@celery.task(name='tasks.update_task_statistics')
def update_task_statistics():
    """Update task statistics (runs periodically)"""
    try:
        stats = {
            'total_tasks': Task.query.count(),
            'pending_tasks': Task.query.filter_by(status=Task.STATUS_PENDING).count(),
            'in_progress_tasks': Task.query.filter_by(status=Task.STATUS_IN_PROGRESS).count(),
            'completed_tasks': Task.query.filter_by(status=Task.STATUS_COMPLETED).count(),
            'overdue_tasks': Task.query.filter(
                Task.due_date < datetime.utcnow(),
                Task.status != Task.STATUS_COMPLETED
            ).count()
        }
        return {'status': 'success', 'statistics': stats}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

@celery.task(name='tasks.cleanup_old_notifications')
def cleanup_old_notifications(days=30):
    """Clean up old notifications"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        deleted = Notification.query.filter(
            Notification.created_at < cutoff_date
        ).delete()
        db.session.commit()
        return {'status': 'success', 'deleted_count': deleted}
    except Exception as e:
        db.session.rollback()
        return {'status': 'error', 'error': str(e)}

@celery.task(name='tasks.invalidate_task_cache')
def invalidate_task_cache_task(task_id):
    """Invalidate cache for a specific task"""
    invalidate_task_cache(task_id)
    return {'status': 'success', 'task_id': task_id}

@celery.task(name='tasks.process_due_date_reminders')
def process_due_date_reminders():
    """Send reminders for tasks due soon"""
    try:
        tomorrow = datetime.utcnow() + timedelta(days=1)
        tasks_due_soon = Task.query.filter(
            Task.due_date <= tomorrow,
            Task.due_date > datetime.utcnow(),
            Task.status != Task.STATUS_COMPLETED
        ).all()
        
        notifications_sent = 0
        for task in tasks_due_soon:
            if task.assigned_to_id:
                send_task_notification.delay(
                    task.id,
                    task.assigned_to_id,
                    Notification.TYPE_TASK_ASSIGNED,
                    f'Task "{task.title}" is due soon'
                )
                notifications_sent += 1
        
        return {'status': 'success', 'notifications_sent': notifications_sent}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}
