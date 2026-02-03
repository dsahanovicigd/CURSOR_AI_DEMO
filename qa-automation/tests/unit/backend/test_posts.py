"""Post tests"""
import pytest
from app.models import Post, User
from app.models.post import Post as PostModel

class TestPosts:
    """Test post operations"""
    
    def test_get_posts(self, client, db_session, test_user):
        """Test getting all posts"""
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
        
        response = client.get('/api/posts')
        assert response.status_code == 200
        assert 'posts' in response.json
    
    def test_get_post(self, client, db_session, test_user):
        """Test getting a specific post"""
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
        
        response = client.get(f'/api/posts/{post.id}')
        assert response.status_code == 200
        assert response.json['id'] == post.id
    
    def test_create_post(self, client, auth_headers):
        """Test creating a post"""
        response = client.post('/api/posts',
            headers=auth_headers,
            json={
                'title': 'New Post',
                'content': 'Post content'
            }
        )
        assert response.status_code == 201
        assert response.json['title'] == 'New Post'
    
    def test_update_post(self, client, auth_headers, db_session, test_user):
        """Test updating a post"""
        slug = PostModel.generate_slug('Test Post')
        post = Post(
            title='Test Post',
            content='Original content',
            slug=slug,
            user_id=test_user.id
        )
        db_session.add(post)
        db_session.commit()
        
        response = client.put(f'/api/posts/{post.id}',
            headers=auth_headers,
            json={'title': 'Updated Post'}
        )
        assert response.status_code == 200
        assert response.json['title'] == 'Updated Post'
    
    def test_delete_post(self, client, auth_headers, db_session, test_user):
        """Test deleting a post"""
        slug = PostModel.generate_slug('Test Post')
        post = Post(
            title='Test Post',
            content='Post content',
            slug=slug,
            user_id=test_user.id
        )
        db_session.add(post)
        db_session.commit()
        
        post_id = post.id
        response = client.delete(f'/api/posts/{post_id}',
            headers=auth_headers
        )
        assert response.status_code == 204
    
    def test_filter_posts_by_user(self, client, db_session, test_user):
        """Test filtering posts by user"""
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
        
        response = client.get(f'/api/posts?user_id={test_user.id}')
        assert response.status_code == 200
    
    def test_post_pagination(self, client, db_session, test_user):
        """Test post pagination"""
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
        
        response = client.get('/api/posts?page=1&per_page=10')
        assert response.status_code == 200
        assert 'posts' in response.json
    
    def test_unpublished_post_not_visible(self, client, db_session, test_user, auth_headers):
        """Test unpublished post is not visible to public"""
        slug = PostModel.generate_slug('Unpublished Post')
        post = Post(
            title='Unpublished Post',
            content='Post content',
            slug=slug,
            user_id=test_user.id,
            is_published=False
        )
        db_session.add(post)
        db_session.commit()
        
        # Public access should return 404
        response = client.get(f'/api/posts/{post.id}')
        assert response.status_code == 404
        
        # Owner can access
        response = client.get(f'/api/posts/{post.id}',
            headers=auth_headers
        )
        assert response.status_code == 200
    
    def test_publish_post(self, client, auth_headers, db_session, test_user):
        """Test publishing a post"""
        slug = PostModel.generate_slug('Draft Post')
        post = Post(
            title='Draft Post',
            content='Post content',
            slug=slug,
            user_id=test_user.id,
            is_published=False
        )
        db_session.add(post)
        db_session.commit()
        
        response = client.put(f'/api/posts/{post.id}',
            headers=auth_headers,
            json={'is_published': True}
        )
        assert response.status_code == 200
        assert response.json['is_published'] == True
    
    def test_create_draft_post(self, client, auth_headers):
        """Test creating a draft post"""
        response = client.post('/api/posts',
            headers=auth_headers,
            json={
                'title': 'Draft Post',
                'content': 'Post content',
                'is_published': False
            }
        )
        assert response.status_code == 201
        assert response.json['is_published'] == False
    
    def test_update_post_content(self, client, auth_headers, db_session, test_user):
        """Test updating post content"""
        slug = PostModel.generate_slug('Test Post')
        post = Post(
            title='Test Post',
            content='Original content',
            slug=slug,
            user_id=test_user.id
        )
        db_session.add(post)
        db_session.commit()
        
        response = client.put(f'/api/posts/{post.id}',
            headers=auth_headers,
            json={'content': 'Updated content'}
        )
        assert response.status_code == 200
        assert response.json['content'] == 'Updated content'
    
    def test_delete_other_user_post_as_admin(self, client, admin_headers, db_session, test_user):
        """Test admin can delete other user's post"""
        slug = PostModel.generate_slug('Test Post')
        post = Post(
            title='Test Post',
            content='Post content',
            slug=slug,
            user_id=test_user.id
        )
        db_session.add(post)
        db_session.commit()
        
        post_id = post.id
        response = client.delete(f'/api/posts/{post_id}',
            headers=admin_headers
        )
        assert response.status_code == 204
