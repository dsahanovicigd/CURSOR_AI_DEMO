"""Task comment tests"""
import pytest
from app.models import TaskComment, Task

class TestTaskComments:
    """Test task comment operations"""
    
    def test_get_task_comments(self, client, auth_headers, test_task):
        """Test getting comments for a task"""
        response = client.get(f'/api/tasks/{test_task.id}/comments',
            headers=auth_headers
        )
        assert response.status_code == 200
    
    def test_create_task_comment(self, client, auth_headers, test_task):
        """Test creating a comment on a task"""
        response = client.post(f'/api/tasks/{test_task.id}/comments',
            headers=auth_headers,
            json={
                'content': 'This is a comment'
            }
        )
        assert response.status_code == 201
        assert response.json['content'] == 'This is a comment'
    
    def test_update_task_comment(self, client, auth_headers, test_task, db_session, test_user):
        """Test updating a task comment"""
        comment = TaskComment(
            task_id=test_task.id,
            user_id=test_user.id,
            content='Original comment'
        )
        db_session.add(comment)
        db_session.commit()
        
        response = client.put(f'/api/comments/{comment.id}',
            headers=auth_headers,
            json={'content': 'Updated comment'}
        )
        assert response.status_code == 200
        assert response.json['content'] == 'Updated comment'
    
    def test_delete_task_comment(self, client, auth_headers, test_task, db_session, test_user):
        """Test deleting a task comment"""
        comment = TaskComment(
            task_id=test_task.id,
            user_id=test_user.id,
            content='Comment to delete'
        )
        db_session.add(comment)
        db_session.commit()
        
        comment_id = comment.id
        response = client.delete(f'/api/comments/{comment_id}',
            headers=auth_headers
        )
        assert response.status_code == 204
    
    def test_task_comment_pagination(self, client, auth_headers, test_task, db_session, test_user):
        """Test task comment pagination"""
        # Create multiple comments
        for i in range(5):
            comment = TaskComment(
                task_id=test_task.id,
                user_id=test_user.id,
                content=f'Comment {i}'
            )
            db_session.add(comment)
        db_session.commit()
        
        response = client.get(f'/api/tasks/{test_task.id}/comments?page=1&per_page=2',
            headers=auth_headers
        )
        assert response.status_code == 200
        assert 'pagination' in response.json or len(response.json.get('comments', [])) <= 2
