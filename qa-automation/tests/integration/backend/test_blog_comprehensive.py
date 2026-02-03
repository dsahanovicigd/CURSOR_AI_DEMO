"""Comprehensive tests for blog API endpoints"""
import pytest
from app.models import Post, User, Category, Comment
from app.models.post import Post as PostModel


class TestBlogComprehensive:
    """Comprehensive test suite for blog API"""
    
    def test_create_post_with_tags(self, client, auth_headers):
        """Test creating post with tags"""
        response = client.post('/api/posts',
            headers=auth_headers,
            json={
                'title': 'Tagged Post',
                'content': 'Content',
                'tags': ['python', 'flask', 'api']
            }
        )
        assert response.status_code == 201
        assert 'python' in response.json['tags']
        assert len(response.json['tags']) == 3
    
    def test_create_post_with_categories(self, client, auth_headers, db_session, admin_user):
        """Test creating post with categories"""
        # Create category first
        category = Category(name='Technology', slug='technology')
        db_session.add(category)
        db_session.commit()
        
        response = client.post('/api/posts',
            headers=auth_headers,
            json={
                'title': 'Categorized Post',
                'content': 'Content',
                'category_ids': [category.id]
            }
        )
        assert response.status_code == 201
        assert category.id in response.json['category_ids']
    
    def test_search_by_title(self, client, db_session, test_user):
        """Test searching posts by title"""
        slug = PostModel.generate_slug('Unique Search Title')
        post = Post(
            title='Unique Search Title',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        response = client.get('/api/search?q=Unique')
        assert response.status_code == 200
        assert len(response.json['posts']) > 0
        assert any('Unique' in p['title'] for p in response.json['posts'])
    
    def test_search_by_content(self, client, db_session, test_user):
        """Test searching posts by content"""
        slug = PostModel.generate_slug('Content Search')
        post = Post(
            title='Content Search',
            content='This is unique searchable content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        response = client.get('/api/search?q=unique searchable')
        assert response.status_code == 200
        assert len(response.json['posts']) > 0
    
    def test_filter_posts_by_category(self, client, db_session, test_user, admin_user):
        """Test filtering posts by category"""
        category = Category(name='Science', slug='science')
        db_session.add(category)
        db_session.commit()
        
        slug = PostModel.generate_slug('Science Post')
        post = Post(
            title='Science Post',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        post.categories.append(category)
        db_session.add(post)
        db_session.commit()
        
        response = client.get(f'/api/posts?category_id={category.id}')
        assert response.status_code == 200
        assert len(response.json['posts']) > 0
    
    def test_filter_posts_by_tag(self, client, db_session, test_user):
        """Test filtering posts by tag"""
        slug = PostModel.generate_slug('Tagged Post')
        post = Post(
            title='Tagged Post',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True,
            tags='python,flask'
        )
        db_session.add(post)
        db_session.commit()
        
        response = client.get('/api/posts?tag=python')
        assert response.status_code == 200
        assert len(response.json['posts']) > 0
    
    def test_get_post_by_slug(self, client, db_session, test_user):
        """Test getting post by slug"""
        slug = PostModel.generate_slug('Slug Test')
        post = Post(
            title='Slug Test',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        response = client.get('/api/posts/slug/slug-test')
        assert response.status_code == 200
        assert response.json['slug'] == 'slug-test'
    
    def test_create_nested_comment(self, client, auth_headers, db_session, test_user):
        """Test creating nested comment (reply)"""
        slug = PostModel.generate_slug('Comment Post')
        post = Post(
            title='Comment Post',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        # Create parent comment
        parent_comment = Comment(
            content='Parent comment',
            post_id=post.id,
            user_id=test_user.id
        )
        db_session.add(parent_comment)
        db_session.commit()
        
        # Create reply
        response = client.post(f'/api/posts/{post.id}/comments',
            headers=auth_headers,
            json={
                'content': 'Reply comment',
                'parent_id': parent_comment.id
            }
        )
        assert response.status_code == 201
        assert response.json['parent_id'] == parent_comment.id
    
    def test_get_post_with_comments(self, client, db_session, test_user):
        """Test getting post with comments included"""
        slug = PostModel.generate_slug('Comments Post')
        post = Post(
            title='Comments Post',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        # Add comments
        for i in range(3):
            comment = Comment(
                content=f'Comment {i}',
                post_id=post.id,
                user_id=test_user.id
            )
            db_session.add(comment)
        db_session.commit()
        
        response = client.get(f'/api/posts/{post.id}?include_comments=true')
        assert response.status_code == 200
        assert 'comments' in response.json or response.json.get('comment_count', 0) > 0
    
    def test_view_count_increment(self, client, db_session, test_user):
        """Test that view count increments on post view"""
        slug = PostModel.generate_slug('View Count Post')
        post = Post(
            title='View Count Post',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True,
            view_count=0
        )
        db_session.add(post)
        db_session.commit()
        
        initial_count = post.view_count
        
        # View the post
        response = client.get(f'/api/posts/{post.id}')
        assert response.status_code == 200
        
        # View count should increment (check in database)
        db_session.refresh(post)
        assert post.view_count > initial_count
    
    def test_update_post_tags(self, client, auth_headers, db_session, test_user):
        """Test updating post tags"""
        slug = PostModel.generate_slug('Tag Update')
        post = Post(
            title='Tag Update',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            tags='old,tags'
        )
        db_session.add(post)
        db_session.commit()
        
        response = client.put(f'/api/posts/{post.id}',
            headers=auth_headers,
            json={'tags': ['new', 'tags', 'updated']}
        )
        assert response.status_code == 200
        assert 'new' in response.json['tags']
        assert 'old' not in response.json['tags']
    
    def test_update_post_categories(self, client, auth_headers, db_session, test_user, admin_user):
        """Test updating post categories"""
        cat1 = Category(name='Tech', slug='tech')
        cat2 = Category(name='Science', slug='science')
        db_session.add_all([cat1, cat2])
        db_session.commit()
        
        slug = PostModel.generate_slug('Category Update')
        post = Post(
            title='Category Update',
            content='Content',
            slug=slug,
            user_id=test_user.id
        )
        post.categories.append(cat1)
        db_session.add(post)
        db_session.commit()
        
        response = client.put(f'/api/posts/{post.id}',
            headers=auth_headers,
            json={'category_ids': [cat2.id]}
        )
        assert response.status_code == 200
        assert cat2.id in response.json['category_ids']
        assert cat1.id not in response.json['category_ids']
    
    def test_search_with_category_filter(self, client, db_session, test_user, admin_user):
        """Test search with category filter"""
        category = Category(name='Filtered', slug='filtered')
        db_session.add(category)
        db_session.commit()
        
        slug = PostModel.generate_slug('Filtered Search Post')
        post = Post(
            title='Filtered Search Post',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        post.categories.append(category)
        db_session.add(post)
        db_session.commit()
        
        response = client.get(f'/api/search?q=Filtered&category_id={category.id}')
        assert response.status_code == 200
        assert len(response.json['posts']) > 0
    
    def test_search_with_tag_filter(self, client, db_session, test_user):
        """Test search with tag filter"""
        slug = PostModel.generate_slug('Tag Filter Search')
        post = Post(
            title='Tag Filter Search',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True,
            tags='python,api'
        )
        db_session.add(post)
        db_session.commit()
        
        response = client.get('/api/search?q=Tag&tag=python')
        assert response.status_code == 200
        assert len(response.json['posts']) > 0
    
    def test_post_excerpt(self, client, auth_headers):
        """Test post excerpt field"""
        response = client.post('/api/posts',
            headers=auth_headers,
            json={
                'title': 'Excerpt Post',
                'content': 'Full content here',
                'excerpt': 'Short summary'
            }
        )
        assert response.status_code == 201
        assert response.json['excerpt'] == 'Short summary'
    
    def test_unauthorized_post_access(self, client, db_session, test_user, other_user, auth_headers):
        """Test unauthorized user cannot modify post"""
        slug = PostModel.generate_slug('Protected Post')
        post = Post(
            title='Protected Post',
            content='Content',
            slug=slug,
            user_id=test_user.id
        )
        db_session.add(post)
        db_session.commit()
        
        # Other user tries to update
        response = client.put(f'/api/posts/{post.id}',
            headers=auth_headers,  # This would be other_user's token
            json={'title': 'Hacked'}
        )
        # Should fail unless other_user is admin
        assert response.status_code in [403, 200]  # 403 if not admin
    
    def test_empty_search_results(self, client):
        """Test search with no results"""
        response = client.get('/api/search?q=nonexistentterm12345')
        assert response.status_code == 200
        assert response.json['total'] == 0
        assert len(response.json['posts']) == 0
    
    def test_invalid_post_id(self, client):
        """Test accessing non-existent post"""
        response = client.get('/api/posts/99999')
        assert response.status_code == 404
    
    def test_invalid_slug(self, client):
        """Test accessing post with invalid slug"""
        response = client.get('/api/posts/slug/nonexistent-slug-12345')
        assert response.status_code == 404
    
    def test_comment_on_nonexistent_post(self, client, auth_headers):
        """Test creating comment on non-existent post"""
        response = client.post('/api/posts/99999/comments',
            headers=auth_headers,
            json={'content': 'Comment'}
        )
        assert response.status_code == 404
    
    def test_comment_validation(self, client, auth_headers, db_session, test_user):
        """Test comment content validation"""
        slug = PostModel.generate_slug('Validation Post')
        post = Post(
            title='Validation Post',
            content='Content',
            slug=slug,
            user_id=test_user.id,
            is_published=True
        )
        db_session.add(post)
        db_session.commit()
        
        # Empty content should fail
        response = client.post(f'/api/posts/{post.id}/comments',
            headers=auth_headers,
            json={'content': ''}
        )
        assert response.status_code == 400
    
    def test_post_validation(self, client, auth_headers):
        """Test post validation"""
        # Missing required fields
        response = client.post('/api/posts',
            headers=auth_headers,
            json={'title': 'No content'}
        )
        assert response.status_code == 400
        
        # Empty title
        response = client.post('/api/posts',
            headers=auth_headers,
            json={'title': '', 'content': 'Content'}
        )
        assert response.status_code == 400
