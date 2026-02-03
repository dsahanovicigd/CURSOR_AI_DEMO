"""Final comprehensive blog API tests - focused on core functionality"""
import pytest
from app.models import Post, User, Category, Comment
from app.models.post import Post as PostModel


class TestBlogFinal:
    """Final test suite ensuring 15+ tests pass"""
    
    def test_1_get_all_posts(self, client, db_session, test_user):
        """Test getting all posts"""
        slug = PostModel.generate_slug('Test Post 1')
        post = Post(title='Test Post 1', content='Content', slug=slug, user_id=test_user.id, is_published=True)
        db_session.add(post)
        db_session.commit()
        
        response = client.get('/api/posts')
        assert response.status_code == 200
        assert 'posts' in response.json
        assert len(response.json['posts']) > 0
    
    def test_2_get_post_by_id(self, client, db_session, test_user):
        """Test getting post by ID"""
        slug = PostModel.generate_slug('Test Post 2')
        post = Post(title='Test Post 2', content='Content', slug=slug, user_id=test_user.id, is_published=True)
        db_session.add(post)
        db_session.commit()
        
        response = client.get(f'/api/posts/{post.id}')
        assert response.status_code == 200
        assert response.json['id'] == post.id
        assert response.json['title'] == 'Test Post 2'
    
    def test_3_create_post(self, client, auth_headers):
        """Test creating a post"""
        response = client.post('/api/posts',
            headers=auth_headers,
            json={'title': 'Created Post', 'content': 'Content here'}
        )
        assert response.status_code == 201
        assert response.json['title'] == 'Created Post'
        assert 'slug' in response.json
    
    def test_4_update_post(self, client, auth_headers, db_session, test_user):
        """Test updating a post"""
        slug = PostModel.generate_slug('Original Title')
        post = Post(title='Original Title', content='Content', slug=slug, user_id=test_user.id)
        db_session.add(post)
        db_session.commit()
        
        response = client.put(f'/api/posts/{post.id}',
            headers=auth_headers,
            json={'title': 'Updated Title'}
        )
        assert response.status_code == 200
        assert response.json['title'] == 'Updated Title'
    
    def test_5_delete_post(self, client, auth_headers, db_session, test_user):
        """Test deleting a post"""
        slug = PostModel.generate_slug('To Delete')
        post = Post(title='To Delete', content='Content', slug=slug, user_id=test_user.id)
        db_session.add(post)
        db_session.commit()
        
        response = client.delete(f'/api/posts/{post.id}', headers=auth_headers)
        assert response.status_code == 204
        
        # Verify deleted
        response = client.get(f'/api/posts/{post.id}')
        assert response.status_code == 404
    
    def test_6_search_posts(self, client, db_session, test_user):
        """Test searching posts"""
        slug = PostModel.generate_slug('Searchable Content')
        post = Post(title='Searchable Content', content='Unique search term', slug=slug, user_id=test_user.id, is_published=True)
        db_session.add(post)
        db_session.commit()
        
        response = client.get('/api/search?q=Unique')
        assert response.status_code == 200
        assert 'posts' in response.json
        assert len(response.json['posts']) > 0
    
    def test_7_get_post_by_slug(self, client, db_session, test_user):
        """Test getting post by slug"""
        slug = PostModel.generate_slug('Slug Test Post')
        post = Post(title='Slug Test Post', content='Content', slug=slug, user_id=test_user.id, is_published=True)
        db_session.add(post)
        db_session.commit()
        
        response = client.get(f'/api/posts/slug/{slug}')
        assert response.status_code == 200
        assert response.json['slug'] == slug
    
    def test_8_create_comment(self, client, auth_headers, db_session, test_user):
        """Test creating a comment"""
        slug = PostModel.generate_slug('Comment Post')
        post = Post(title='Comment Post', content='Content', slug=slug, user_id=test_user.id, is_published=True)
        db_session.add(post)
        db_session.commit()
        
        response = client.post(f'/api/posts/{post.id}/comments',
            headers=auth_headers,
            json={'content': 'Great post!'}
        )
        assert response.status_code == 201
        assert response.json['content'] == 'Great post!'
        assert response.json['post_id'] == post.id
    
    def test_9_get_post_comments(self, client, db_session, test_user):
        """Test getting comments for a post"""
        slug = PostModel.generate_slug('Comments Post')
        post = Post(title='Comments Post', content='Content', slug=slug, user_id=test_user.id, is_published=True)
        db_session.add(post)
        db_session.commit()
        
        comment = Comment(content='Test comment', post_id=post.id, user_id=test_user.id)
        db_session.add(comment)
        db_session.commit()
        
        response = client.get(f'/api/posts/{post.id}/comments')
        assert response.status_code == 200
        assert len(response.json) > 0
    
    def test_10_filter_by_user(self, client, db_session, test_user):
        """Test filtering posts by user"""
        slug = PostModel.generate_slug('User Filter Post')
        post = Post(title='User Filter Post', content='Content', slug=slug, user_id=test_user.id, is_published=True)
        db_session.add(post)
        db_session.commit()
        
        response = client.get(f'/api/posts?user_id={test_user.id}')
        assert response.status_code == 200
        assert len(response.json['posts']) > 0
    
    def test_11_pagination(self, client, db_session, test_user):
        """Test post pagination"""
        # Create multiple posts
        for i in range(5):
            slug = PostModel.generate_slug(f'Page Post {i}')
            post = Post(title=f'Page Post {i}', content='Content', slug=slug, user_id=test_user.id, is_published=True)
            db_session.add(post)
        db_session.commit()
        
        response = client.get('/api/posts?page=1&per_page=2')
        assert response.status_code == 200
        assert response.json['current_page'] == 1
        assert len(response.json['posts']) <= 2
    
    def test_12_post_with_tags(self, client, auth_headers):
        """Test creating post with tags"""
        response = client.post('/api/posts',
            headers=auth_headers,
            json={
                'title': 'Tagged Post',
                'content': 'Content',
                'tags': ['python', 'flask']
            }
        )
        assert response.status_code == 201
        assert 'python' in response.json['tags']
    
    def test_13_post_with_excerpt(self, client, auth_headers):
        """Test creating post with excerpt"""
        response = client.post('/api/posts',
            headers=auth_headers,
            json={
                'title': 'Excerpt Post',
                'content': 'Full content',
                'excerpt': 'Short summary'
            }
        )
        assert response.status_code == 201
        assert response.json['excerpt'] == 'Short summary'
    
    def test_14_unpublished_post(self, client, db_session, test_user, auth_headers):
        """Test unpublished post visibility"""
        slug = PostModel.generate_slug('Draft Post')
        post = Post(title='Draft Post', content='Content', slug=slug, user_id=test_user.id, is_published=False)
        db_session.add(post)
        db_session.commit()
        
        # Public should not see it
        response = client.get(f'/api/posts/{post.id}')
        assert response.status_code == 404
        
        # Author should see it
        response = client.get(f'/api/posts/{post.id}', headers=auth_headers)
        assert response.status_code == 200
    
    def test_15_view_count(self, client, db_session, test_user):
        """Test view count increments"""
        slug = PostModel.generate_slug('View Count Test')
        post = Post(title='View Count Test', content='Content', slug=slug, user_id=test_user.id, is_published=True, view_count=0)
        db_session.add(post)
        db_session.commit()
        
        initial_count = post.view_count
        client.get(f'/api/posts/{post.id}')
        
        db_session.refresh(post)
        assert post.view_count > initial_count
    
    def test_16_invalid_post_id(self, client):
        """Test invalid post ID returns 404"""
        response = client.get('/api/posts/99999')
        assert response.status_code == 404
    
    def test_17_empty_search(self, client):
        """Test empty search results"""
        response = client.get('/api/search?q=nonexistent12345')
        assert response.status_code == 200
        assert response.json['total'] == 0
    
    def test_18_post_validation_empty_title(self, client, auth_headers):
        """Test post validation - empty title"""
        response = client.post('/api/posts',
            headers=auth_headers,
            json={'title': '', 'content': 'Content'}
        )
        assert response.status_code == 400
    
    def test_19_post_validation_missing_content(self, client, auth_headers):
        """Test post validation - missing content"""
        response = client.post('/api/posts',
            headers=auth_headers,
            json={'title': 'Title only'}
        )
        assert response.status_code == 400
    
    def test_20_unauthorized_access(self, client, db_session, test_user):
        """Test unauthorized access to protected endpoint"""
        response = client.post('/api/posts',
            json={'title': 'Test', 'content': 'Content'}
        )
        assert response.status_code == 401
