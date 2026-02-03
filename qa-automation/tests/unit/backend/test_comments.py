"""Comment CRUD operation tests"""
import pytest
from app.models import Comment, Post, User
from app.models.post import Post as PostModel


class TestCommentCRUD:
    """Test comment CRUD operations"""
    
    def test_create_comment(self, client, auth_headers, db_session, test_user):
        """Test creating a new comment"""
        slug = PostModel.generate_slug('Test Post')
        post = Post(
            title='Test Post',
            content='Post content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        response = client.post('/api/comments',
            headers=auth_headers,
            json={
                'content': 'Great post!',
                'post_id': post.id
            }
        )
        assert response.status_code == 201
        assert response.json['content'] == 'Great post!'
        assert response.json['post_id'] == post.id
        assert response.json['user_id'] == test_user.id
    
    def test_get_comments(self, client, db_session, test_user):
        """Test getting all comments"""
        slug = PostModel.generate_slug('Test Post')
        post = Post(
            title='Test Post',
            content='Post content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        comment = Comment(
            content='Test comment',
            post_id=post.id,
            user_id=test_user.id,
            is_approved=True
        )
        db_session.add(comment)
        db_session.commit()
        
        response = client.get('/api/comments')
        assert response.status_code == 200
        assert 'comments' in response.json
        assert len(response.json['comments']) >= 1
    
    def test_get_comment(self, client, db_session, test_user):
        """Test getting a specific comment"""
        slug = PostModel.generate_slug('Test Post')
        post = Post(
            title='Test Post',
            content='Post content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        comment = Comment(
            content='Test comment',
            post_id=post.id,
            user_id=test_user.id,
            is_approved=True
        )
        db_session.add(comment)
        db_session.commit()
        
        response = client.get(f'/api/comments/{comment.id}')
        assert response.status_code == 200
        assert response.json['id'] == comment.id
        assert response.json['content'] == 'Test comment'
    
    def test_get_post_comments(self, client, db_session, test_user):
        """Test getting comments for a specific post"""
        slug = PostModel.generate_slug('Test Post')
        post = Post(
            title='Test Post',
            content='Post content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        comment1 = Comment(
            content='First comment',
            post_id=post.id,
            user_id=test_user.id,
            is_approved=True
        )
        comment2 = Comment(
            content='Second comment',
            post_id=post.id,
            user_id=test_user.id,
            is_approved=True
        )
        db_session.add(comment1)
        db_session.add(comment2)
        db_session.commit()
        
        response = client.get(f'/api/comments/post/{post.id}')
        assert response.status_code == 200
        assert len(response.json) >= 2
    
    def test_update_comment(self, client, auth_headers, db_session, test_user):
        """Test updating a comment"""
        slug = PostModel.generate_slug('Test Post')
        post = Post(
            title='Test Post',
            content='Post content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        comment = Comment(
            content='Original comment',
            post_id=post.id,
            user_id=test_user.id
        )
        db_session.add(comment)
        db_session.commit()
        
        response = client.put(f'/api/comments/{comment.id}',
            headers=auth_headers,
            json={'content': 'Updated comment'}
        )
        assert response.status_code == 200
        assert response.json['content'] == 'Updated comment'
    
    def test_delete_comment(self, client, auth_headers, db_session, test_user):
        """Test deleting a comment"""
        slug = PostModel.generate_slug('Test Post')
        post = Post(
            title='Test Post',
            content='Post content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        comment = Comment(
            content='Comment to delete',
            post_id=post.id,
            user_id=test_user.id
        )
        db_session.add(comment)
        db_session.commit()
        
        comment_id = comment.id
        response = client.delete(f'/api/comments/{comment_id}',
            headers=auth_headers
        )
        assert response.status_code == 204
        
        # Verify comment is deleted
        get_response = client.get(f'/api/comments/{comment_id}')
        assert get_response.status_code == 404


class TestCommentNestedReplies:
    """Test nested comment replies"""
    
    def test_create_nested_comment(self, client, auth_headers, db_session, test_user):
        """Test creating a nested comment reply"""
        slug = PostModel.generate_slug('Test Post')
        post = Post(
            title='Test Post',
            content='Post content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        parent_comment = Comment(
            content='Parent comment',
            post_id=post.id,
            user_id=test_user.id,
            is_approved=True
        )
        db_session.add(parent_comment)
        db_session.commit()
        
        response = client.post('/api/comments',
            headers=auth_headers,
            json={
                'content': 'Reply to parent',
                'post_id': post.id,
                'parent_id': parent_comment.id
            }
        )
        assert response.status_code == 201
        assert response.json['parent_id'] == parent_comment.id
    
    def test_get_comments_with_replies(self, client, db_session, test_user):
        """Test getting comments with nested replies"""
        slug = PostModel.generate_slug('Test Post')
        post = Post(
            title='Test Post',
            content='Post content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        parent = Comment(
            content='Parent',
            post_id=post.id,
            user_id=test_user.id,
            is_approved=True
        )
        db_session.add(parent)
        db_session.commit()
        
        reply = Comment(
            content='Reply',
            post_id=post.id,
            user_id=test_user.id,
            parent_id=parent.id,
            is_approved=True
        )
        db_session.add(reply)
        db_session.commit()
        
        response = client.get(f'/api/comments/post/{post.id}?include_replies=true')
        assert response.status_code == 200
        assert len(response.json) >= 2


class TestCommentFiltering:
    """Test comment filtering and pagination"""
    
    def test_filter_comments_by_post(self, client, db_session, test_user):
        """Test filtering comments by post ID"""
        slug = PostModel.generate_slug('Test Post')
        post1 = Post(
            title='Post 1',
            content='Content 1',
            slug=PostModel.generate_slug('Post 1'),
            user_id=test_user.id,
            is_published=True
        )
        post2 = Post(
            title='Post 2',
            content='Content 2',
            slug=PostModel.generate_slug('Post 2'),
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post1)
        db_session.add(post2)
        db_session.commit()
        
        comment1 = Comment(
            content='Comment 1',
            post_id=post1.id,
            user_id=test_user.id,
            is_approved=True
        )
        comment2 = Comment(
            content='Comment 2',
            post_id=post2.id,
            user_id=test_user.id,
            is_approved=True
        )
        db_session.add(comment1)
        db_session.add(comment2)
        db_session.commit()
        
        response = client.get(f'/api/comments?post_id={post1.id}')
        assert response.status_code == 200
        comments = response.json['comments']
        assert all(c['post_id'] == post1.id for c in comments)
    
    def test_filter_comments_by_user(self, client, db_session, test_user):
        """Test filtering comments by user ID"""
        slug = PostModel.generate_slug('Test Post')
        post = Post(
            title='Test Post',
            content='Post content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        
        other_user = User(
            username='otheruser',
            email='other@test.com',
            role=User.ROLE_CUSTOMER
        )
        other_user.set_password('password123')
        db_session.add(other_user)
        db_session.commit()
        
        comment1 = Comment(
            content='Comment by test_user',
            post_id=post.id,
            user_id=test_user.id,
            is_approved=True
        )
        comment2 = Comment(
            content='Comment by other_user',
            post_id=post.id,
            user_id=other_user.id,
            is_approved=True
        )
        db_session.add(comment1)
        db_session.add(comment2)
        db_session.commit()
        
        response = client.get(f'/api/comments?user_id={test_user.id}')
        assert response.status_code == 200
        comments = response.json['comments']
        assert all(c['user_id'] == test_user.id for c in comments)
    
    def test_filter_approved_comments_only(self, client, db_session, test_user):
        """Test filtering to show only approved comments"""
        slug = PostModel.generate_slug('Test Post')
        post = Post(
            title='Test Post',
            content='Post content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        approved = Comment(
            content='Approved comment',
            post_id=post.id,
            user_id=test_user.id,
            is_approved=True
        )
        unapproved = Comment(
            content='Unapproved comment',
            post_id=post.id,
            user_id=test_user.id,
            is_approved=False
        )
        db_session.add(approved)
        db_session.add(unapproved)
        db_session.commit()
        
        response = client.get('/api/comments?approved_only=true')
        assert response.status_code == 200
        comments = response.json['comments']
        assert all(c['is_approved'] == True for c in comments)
    
    def test_comment_pagination(self, client, db_session, test_user):
        """Test comment pagination"""
        slug = PostModel.generate_slug('Test Post')
        post = Post(
            title='Test Post',
            content='Post content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        # Create multiple comments
        for i in range(5):
            comment = Comment(
                content=f'Comment {i}',
                post_id=post.id,
                user_id=test_user.id,
                is_approved=True
            )
            db_session.add(comment)
        db_session.commit()
        
        response = client.get('/api/comments?page=1&per_page=2')
        assert response.status_code == 200
        assert 'total' in response.json
        assert 'pages' in response.json
        assert len(response.json['comments']) <= 2


class TestCommentPermissions:
    """Test comment permissions and access control"""
    
    def test_cannot_update_other_user_comment(self, client, db_session, test_user, auth_headers):
        """Test that users cannot update other users' comments"""
        slug = PostModel.generate_slug('Test Post')
        post = Post(
            title='Test Post',
            content='Post content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        
        other_user = User(
            username='otheruser',
            email='other@test.com',
            role=User.ROLE_CUSTOMER
        )
        other_user.set_password('password123')
        db_session.add(other_user)
        db_session.commit()
        
        comment = Comment(
            content='Other user comment',
            post_id=post.id,
            user_id=other_user.id
        )
        db_session.add(comment)
        db_session.commit()
        
        response = client.put(f'/api/comments/{comment.id}',
            headers=auth_headers,
            json={'content': 'Hacked comment'}
        )
        assert response.status_code == 403
    
    def test_admin_can_approve_comment(self, client, admin_headers, db_session, test_user):
        """Test admin can approve/unapprove comments"""
        slug = PostModel.generate_slug('Test Post')
        post = Post(
            title='Test Post',
            content='Post content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        comment = Comment(
            content='Unapproved comment',
            post_id=post.id,
            user_id=test_user.id,
            is_approved=False
        )
        db_session.add(comment)
        db_session.commit()
        
        response = client.put(f'/api/comments/{comment.id}',
            headers=admin_headers,
            json={'is_approved': True}
        )
        assert response.status_code == 200
        assert response.json['is_approved'] == True
    
    def test_non_admin_cannot_approve_comment(self, client, auth_headers, db_session, test_user):
        """Test non-admin cannot modify approval status"""
        slug = PostModel.generate_slug('Test Post')
        post = Post(
            title='Test Post',
            content='Post content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        comment = Comment(
            content='Comment',
            post_id=post.id,
            user_id=test_user.id,
            is_approved=False
        )
        db_session.add(comment)
        db_session.commit()
        
        response = client.put(f'/api/comments/{comment.id}',
            headers=auth_headers,
            json={'is_approved': True}
        )
        assert response.status_code == 403
    
    def test_unapproved_comment_not_visible_to_public(self, client, db_session, test_user):
        """Test unapproved comments are not visible to public"""
        slug = PostModel.generate_slug('Test Post')
        post = Post(
            title='Test Post',
            content='Post content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        comment = Comment(
            content='Unapproved comment',
            post_id=post.id,
            user_id=test_user.id,
            is_approved=False
        )
        db_session.add(comment)
        db_session.commit()
        
        # Public access should return 404
        response = client.get(f'/api/comments/{comment.id}')
        assert response.status_code == 404
        
        # Author can access
        login_response = client.post('/api/auth/login', json={
            'username': test_user.username,
            'password': 'testpassword123'
        })
        token = login_response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        response = client.get(f'/api/comments/{comment.id}', headers=headers)
        assert response.status_code == 200
    
    def test_create_comment_with_invalid_parent(self, client, auth_headers, db_session, test_user):
        """Test creating comment with invalid parent ID"""
        slug = PostModel.generate_slug('Test Post')
        post = Post(
            title='Test Post',
            content='Post content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        response = client.post('/api/comments',
            headers=auth_headers,
            json={
                'content': 'Reply',
                'post_id': post.id,
                'parent_id': 99999  # Non-existent parent
            }
        )
        assert response.status_code == 404
    
    def test_create_comment_with_parent_from_different_post(self, client, auth_headers, db_session, test_user):
        """Test creating comment with parent from different post"""
        slug1 = PostModel.generate_slug('Post 1')
        post1 = Post(
            title='Post 1',
            content='Content 1',
            slug=slug1,
            user_id=test_user.id,
            is_published=True
        )
        slug2 = PostModel.generate_slug('Post 2')
        post2 = Post(
            title='Post 2',
            content='Content 2',
            slug=slug2,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post1)
        db_session.add(post2)
        db_session.commit()
        
        parent_comment = Comment(
            content='Parent comment',
            post_id=post1.id,
            user_id=test_user.id,
            is_approved=True
        )
        db_session.add(parent_comment)
        db_session.commit()
        
        # Try to create reply in post2 with parent from post1
        response = client.post('/api/comments',
            headers=auth_headers,
            json={
                'content': 'Reply',
                'post_id': post2.id,
                'parent_id': parent_comment.id
            }
        )
        assert response.status_code == 400
