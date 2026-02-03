# Blogging Platform API

A comprehensive Flask REST API for a blogging platform with user authentication, blog post management, comments, categories, and search functionality.

## Features

### ✅ User Authentication
- JWT-based authentication
- User registration and login
- Token refresh mechanism
- Protected endpoints with role-based access

### ✅ Blog Posts
- **CRUD Operations**: Create, read, update, delete posts
- **Slug Support**: URL-friendly identifiers for posts
- **Tags**: Categorize posts with tags
- **Excerpt**: Short summaries for post previews
- **View Count**: Track post popularity
- **Publishing**: Draft/published status
- **Author Information**: Track post authors

### ✅ Categories
- **CRUD Operations**: Manage post categories
- **Slug Support**: URL-friendly category identifiers
- **Many-to-Many**: Posts can belong to multiple categories
- **Admin Only**: Category management restricted to admins

### ✅ Comments System
- **CRUD Operations**: Create, read, update, delete comments
- **Nested Replies**: Support for comment threads
- **Moderation**: Approve/reject comments (admin)
- **Post Association**: Comments linked to posts
- **User Association**: Track comment authors

### ✅ Search Functionality
- **Full-Text Search**: Search in title, content, and excerpt
- **Filtering**: By category, tag, author, published status
- **Pagination**: Efficient result pagination
- **Advanced Search**: Dedicated search endpoint

### ✅ API Documentation
- **Swagger UI**: Interactive API documentation
- **JWT Integration**: Easy token management in Swagger
- **Request/Response Examples**: Clear API examples

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT tokens
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - Logout (client-side token clearing)

### Posts
- `GET /api/posts` - List all posts (with filtering and pagination)
- `GET /api/posts/search?q=query` - Search posts
- `GET /api/posts/<id>` - Get post by ID
- `GET /api/posts/slug/<slug>` - Get post by slug
- `POST /api/posts` - Create new post (requires auth)
- `PUT /api/posts/<id>` - Update post (requires auth, author or admin)
- `DELETE /api/posts/<id>` - Delete post (requires auth, author or admin)

**Query Parameters for GET /api/posts:**
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 20, max: 100)
- `user_id` - Filter by author
- `category_id` - Filter by category
- `search` - Search in title/content
- `tag` - Filter by tag
- `published_only` - Show only published posts (default: true)

### Categories
- `GET /api/categories` - List all categories
- `GET /api/categories/<id>` - Get category by ID
- `GET /api/categories/slug/<slug>` - Get category by slug
- `POST /api/categories` - Create category (requires auth, admin only)
- `PUT /api/categories/<id>` - Update category (requires auth, admin only)
- `DELETE /api/categories/<id>` - Delete category (requires auth, admin only)

### Comments
- `GET /api/comments` - List all comments (with filtering)
- `GET /api/comments/<id>` - Get comment by ID
- `GET /api/comments/post/<post_id>` - Get comments for a post
- `POST /api/comments` - Create comment (requires auth)
- `PUT /api/comments/<id>` - Update comment (requires auth, author or admin)
- `DELETE /api/comments/<id>` - Delete comment (requires auth, author or admin)

**Query Parameters for GET /api/comments:**
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 20, max: 100)
- `post_id` - Filter by post
- `user_id` - Filter by author
- `approved_only` - Show only approved comments (default: true)

## Usage Examples

### 1. Register and Login

```bash
# Register
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'

# Login
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepassword123"
  }'
```

### 2. Create a Post

```bash
curl -X POST http://localhost:5001/api/posts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "My First Blog Post",
    "content": "This is the content of my blog post...",
    "excerpt": "A brief summary",
    "tags": ["python", "flask", "api"],
    "category_ids": [1, 2],
    "is_published": true
  }'
```

### 3. Search Posts

```bash
# Simple search
curl "http://localhost:5001/api/posts/search?q=python&page=1&per_page=10"

# Advanced search with filters
curl "http://localhost:5001/api/posts?search=flask&category_id=1&tag=api"
```

### 4. Create a Comment

```bash
curl -X POST http://localhost:5001/api/comments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "content": "Great post! Thanks for sharing.",
    "post_id": 1
  }'
```

### 5. Create a Nested Comment (Reply)

```bash
curl -X POST http://localhost:5001/api/comments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "content": "I agree with your point.",
    "post_id": 1,
    "parent_id": 5
  }'
```

## Data Models

### Post Model
```python
{
    "id": 1,
    "title": "Post Title",
    "slug": "post-title",
    "content": "Post content...",
    "excerpt": "Brief summary",
    "user_id": 1,
    "author": "johndoe",
    "author_name": "John Doe",
    "is_published": true,
    "view_count": 42,
    "tags": ["python", "flask"],
    "category_ids": [1, 2],
    "category_names": ["Technology", "Programming"],
    "comment_count": 5,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
}
```

### Category Model
```python
{
    "id": 1,
    "name": "Technology",
    "slug": "technology",
    "description": "Posts about technology",
    "post_count": 10,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
}
```

### Comment Model
```python
{
    "id": 1,
    "content": "Comment text...",
    "post_id": 1,
    "user_id": 2,
    "author": "janedoe",
    "author_name": "Jane Doe",
    "parent_id": null,
    "is_approved": true,
    "reply_count": 2,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
}
```

## Validation Rules

### Post Validation
- Title: 1-200 characters, required
- Content: Minimum 1 character, required
- Excerpt: Maximum 500 characters, optional
- Tags: Maximum 20 tags, each tag max 50 characters
- Category IDs: Maximum 10 categories

### Category Validation
- Name: 1-100 characters, required, unique
- Description: Maximum 1000 characters, optional

### Comment Validation
- Content: 1-5000 characters, required
- Post ID: Required, must exist
- Parent ID: Optional, must exist if provided

## Error Handling

All endpoints return consistent error responses:

```json
{
    "error": "Error message",
    "messages": {
        "field_name": ["Validation error details"]
    }
}
```

Common HTTP Status Codes:
- `200` - Success
- `201` - Created
- `204` - No Content (successful delete)
- `400` - Bad Request (validation error)
- `401` - Unauthorized (missing/invalid token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `500` - Internal Server Error

## Security Features

1. **JWT Authentication**: Secure token-based authentication
2. **Password Hashing**: Passwords are hashed using Werkzeug
3. **Role-Based Access**: Admin-only endpoints for category management
4. **Author Verification**: Users can only modify their own content
5. **Input Validation**: Comprehensive validation using Marshmallow
6. **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
7. **CORS Configuration**: Configurable CORS for API access

## Database Schema

See `BLOGGING_PLATFORM_MIGRATION.md` for detailed database schema and migration instructions.

## Testing

Run tests with:
```bash
cd flask_api
source venv/bin/activate
pytest
```

## Swagger UI

Access interactive API documentation at:
```
http://localhost:5001/api/docs
```

The Swagger UI includes:
- All endpoint documentation
- Try-it-out functionality
- JWT token management
- Request/response examples

## Next Steps

1. Run database migrations (see `BLOGGING_PLATFORM_MIGRATION.md`)
2. Start the Flask server: `python run.py`
3. Access Swagger UI: `http://localhost:5001/api/docs`
4. Register a user and start creating posts!

## Technologies Used

- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **Marshmallow** - Serialization and validation
- **Flask-JWT-Extended** - JWT authentication
- **Flasgger** - Swagger UI integration
- **Flask-Migrate** - Database migrations
