"""Category CRUD operation tests"""
import pytest
from app.models import Category, User


class TestCategoryCRUD:
    """Test category CRUD operations"""
    
    def test_get_categories(self, client, db_session):
        """Test getting all categories"""
        category = Category(
            name='Technology',
            slug='technology',
            description='Tech related posts'
        )
        db_session.add(category)
        db_session.commit()
        
        response = client.get('/api/categories')
        assert response.status_code == 200
        assert 'categories' in response.json
        assert len(response.json['categories']) >= 1
    
    def test_get_category(self, client, db_session):
        """Test getting a specific category"""
        category = Category(
            name='Technology',
            slug='technology',
            description='Tech related posts'
        )
        db_session.add(category)
        db_session.commit()
        
        response = client.get(f'/api/categories/{category.id}')
        assert response.status_code == 200
        assert response.json['id'] == category.id
        assert response.json['name'] == 'Technology'
    
    def test_get_category_by_slug(self, client, db_session):
        """Test getting category by slug"""
        category = Category(
            name='Technology',
            slug='technology',
            description='Tech related posts'
        )
        db_session.add(category)
        db_session.commit()
        
        response = client.get('/api/categories/slug/technology')
        assert response.status_code == 200
        assert response.json['slug'] == 'technology'
        assert response.json['name'] == 'Technology'
    
    def test_create_category_as_admin(self, client, admin_headers):
        """Test creating a category as admin"""
        response = client.post('/api/categories',
            headers=admin_headers,
            json={
                'name': 'Science',
                'description': 'Science related posts'
            }
        )
        assert response.status_code == 201
        assert response.json['name'] == 'Science'
        assert 'slug' in response.json
        assert response.json['slug'] == 'science'
    
    def test_create_category_auto_generates_slug(self, client, admin_headers):
        """Test that category creation auto-generates slug"""
        response = client.post('/api/categories',
            headers=admin_headers,
            json={
                'name': 'Web Development',
                'description': 'Web dev posts'
            }
        )
        assert response.status_code == 201
        assert response.json['slug'] == 'web-development'
    
    def test_create_category_duplicate_name(self, client, admin_headers, db_session):
        """Test creating category with duplicate name fails"""
        category = Category(
            name='Existing Category',
            slug='existing-category'
        )
        db_session.add(category)
        db_session.commit()
        
        response = client.post('/api/categories',
            headers=admin_headers,
            json={
                'name': 'Existing Category',
                'description': 'Duplicate'
            }
        )
        assert response.status_code == 400
    
    def test_create_category_unique_slug_generation(self, client, admin_headers, db_session):
        """Test that duplicate slugs get unique suffixes"""
        category1 = Category(
            name='Test Category',
            slug='test-category'
        )
        db_session.add(category1)
        db_session.commit()
        
        response = client.post('/api/categories',
            headers=admin_headers,
            json={
                'name': 'Test Category',
                'description': 'Should get unique slug'
            }
        )
        assert response.status_code == 201
        # Should have a suffix like test-category-1
        assert 'test-category' in response.json['slug']
    
    def test_update_category_as_admin(self, client, admin_headers, db_session):
        """Test updating a category as admin"""
        category = Category(
            name='Original Name',
            slug='original-name',
            description='Original description'
        )
        db_session.add(category)
        db_session.commit()
        
        response = client.put(f'/api/categories/{category.id}',
            headers=admin_headers,
            json={
                'name': 'Updated Name',
                'description': 'Updated description'
            }
        )
        assert response.status_code == 200
        assert response.json['name'] == 'Updated Name'
        assert response.json['description'] == 'Updated description'
    
    def test_update_category_slug_on_name_change(self, client, admin_headers, db_session):
        """Test that slug updates when name changes"""
        category = Category(
            name='Old Name',
            slug='old-name'
        )
        db_session.add(category)
        db_session.commit()
        
        response = client.put(f'/api/categories/{category.id}',
            headers=admin_headers,
            json={'name': 'New Name'}
        )
        assert response.status_code == 200
        assert response.json['slug'] == 'new-name'
    
    def test_delete_category_as_admin(self, client, admin_headers, db_session):
        """Test deleting a category as admin"""
        category = Category(
            name='To Delete',
            slug='to-delete'
        )
        db_session.add(category)
        db_session.commit()
        
        category_id = category.id
        response = client.delete(f'/api/categories/{category_id}',
            headers=admin_headers
        )
        assert response.status_code == 204
        
        # Verify category is deleted
        get_response = client.get(f'/api/categories/{category_id}')
        assert get_response.status_code == 404


class TestCategoryPermissions:
    """Test category permissions and access control"""
    
    def test_create_category_requires_admin(self, client, auth_headers):
        """Test that non-admin cannot create category"""
        response = client.post('/api/categories',
            headers=auth_headers,
            json={
                'name': 'Unauthorized Category',
                'description': 'Should fail'
            }
        )
        assert response.status_code == 403
    
    def test_update_category_requires_admin(self, client, auth_headers, db_session):
        """Test that non-admin cannot update category"""
        category = Category(
            name='Protected Category',
            slug='protected-category'
        )
        db_session.add(category)
        db_session.commit()
        
        response = client.put(f'/api/categories/{category.id}',
            headers=auth_headers,
            json={'name': 'Hacked Name'}
        )
        assert response.status_code == 403
    
    def test_delete_category_requires_admin(self, client, auth_headers, db_session):
        """Test that non-admin cannot delete category"""
        category = Category(
            name='Protected Category',
            slug='protected-category'
        )
        db_session.add(category)
        db_session.commit()
        
        response = client.delete(f'/api/categories/{category.id}',
            headers=auth_headers
        )
        assert response.status_code == 403
    
    def test_public_can_view_categories(self, client, db_session):
        """Test that public can view categories without auth"""
        category = Category(
            name='Public Category',
            slug='public-category'
        )
        db_session.add(category)
        db_session.commit()
        
        response = client.get('/api/categories')
        assert response.status_code == 200
        assert len(response.json['categories']) >= 1


class TestCategoryFiltering:
    """Test category filtering and pagination"""
    
    def test_search_categories_by_name(self, client, db_session):
        """Test searching categories by name"""
        category1 = Category(
            name='Python Programming',
            slug='python-programming'
        )
        category2 = Category(
            name='JavaScript Development',
            slug='javascript-development'
        )
        category3 = Category(
            name='Database Design',
            slug='database-design'
        )
        db_session.add(category1)
        db_session.add(category2)
        db_session.add(category3)
        db_session.commit()
        
        response = client.get('/api/categories?search=Python')
        assert response.status_code == 200
        categories = response.json['categories']
        assert any('Python' in c['name'] for c in categories)
    
    def test_category_pagination(self, client, db_session):
        """Test category pagination"""
        # Create multiple categories
        for i in range(5):
            category = Category(
                name=f'Category {i}',
                slug=f'category-{i}'
            )
            db_session.add(category)
        db_session.commit()
        
        response = client.get('/api/categories?page=1&per_page=2')
        assert response.status_code == 200
        assert 'total' in response.json
        assert 'pages' in response.json
        assert len(response.json['categories']) <= 2
    
    def test_category_max_per_page_limit(self, client, db_session):
        """Test that per_page is capped at 100"""
        response = client.get('/api/categories?per_page=200')
        assert response.status_code == 200
        # Should be capped at 100
        assert len(response.json['categories']) <= 100


class TestCategoryEdgeCases:
    """Test category edge cases and error handling"""
    
    def test_get_nonexistent_category(self, client):
        """Test getting non-existent category returns 404"""
        response = client.get('/api/categories/99999')
        assert response.status_code == 404
    
    def test_get_nonexistent_category_by_slug(self, client):
        """Test getting non-existent category by slug returns 404"""
        response = client.get('/api/categories/slug/nonexistent-slug')
        assert response.status_code == 404
    
    def test_update_category_with_duplicate_name(self, client, admin_headers, db_session):
        """Test updating category to duplicate name fails"""
        category1 = Category(
            name='Category One',
            slug='category-one'
        )
        category2 = Category(
            name='Category Two',
            slug='category-two'
        )
        db_session.add(category1)
        db_session.add(category2)
        db_session.commit()
        
        # Try to rename category2 to category1's name
        response = client.put(f'/api/categories/{category2.id}',
            headers=admin_headers,
            json={'name': 'Category One'}
        )
        assert response.status_code == 400
    
    def test_category_slug_special_characters(self, client, admin_headers):
        """Test that special characters are removed from slug"""
        response = client.post('/api/categories',
            headers=admin_headers,
            json={
                'name': 'Category & More! @#$',
                'description': 'Test special chars'
            }
        )
        assert response.status_code == 201
        slug = response.json['slug']
        # Should not contain special characters
        assert '&' not in slug
        assert '!' not in slug
        assert '@' not in slug
        assert '#' not in slug
        assert '$' not in slug
    
    def test_category_slug_length_limit(self, client, admin_headers):
        """Test that slug is truncated to 100 characters"""
        long_name = 'A' * 150  # Very long name
        response = client.post('/api/categories',
            headers=admin_headers,
            json={
                'name': long_name,
                'description': 'Long name test'
            }
        )
        assert response.status_code == 201
        assert len(response.json['slug']) <= 100
