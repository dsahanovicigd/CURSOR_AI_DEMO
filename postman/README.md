# Postman Collection - Blogging Platform API

Complete Postman collection covering all API scenarios for the Blogging Platform.

## 📋 Collection Overview

This collection includes **6 main folders** covering all required scenarios:

1. **Authentication** - User registration and login
2. **Posts - CRUD Operations** - Create, read, update, delete posts
3. **Search Posts** - Search by keyword with filters
4. **Comments** - Create, read, delete comments (including nested replies)
5. **Categories** - Category management (admin only for create/update/delete)
6. **Pagination Examples** - Examples showing 20 items per page

## 🚀 Quick Start

### 1. Import Collection

1. Open Postman
2. Click **Import** button
3. Select `Blogging_API_Collection.json`
4. Collection will be imported with all requests

### 2. Collection Variables

The collection uses **collection variables** (set automatically via tests) - no environment setup required!

Variables are automatically saved when you run requests:
- `base_url` - API base URL (default: `http://localhost:5001`)
- `access_token` - JWT access token (set after login)
- `refresh_token` - JWT refresh token (set after login)
- `user_id` - Current user ID (set after register/login)
- `admin_access_token` - Admin JWT access token (set after admin login)
- `admin_refresh_token` - Admin JWT refresh token (set after admin login)
- `admin_user_id` - Admin user ID (set after admin login)
- `post_id` - Post ID (set after creating/getting a post)
- `comment_id` - Comment ID (set after creating a comment)
- `category_id` - Category ID (set after getting/creating a category)

**Note:** Variables are stored at the collection level, so they work without creating an environment. You can view/edit them by clicking on the collection name → Variables tab.

### 3. Run Requests in Order

**Recommended flow:**

1. **Register User** → Sets `user_id`
2. **Login** → Sets `access_token` and `refresh_token`
3. **Admin Login** → Sets `admin_access_token` (required for category management)
4. **Get All Categories** → Sets `category_id` (if categories exist)
5. **Create Post** → Sets `post_id`
6. **Get Post by ID** → Verifies post creation
7. **Create Comment** → Sets `comment_id`
8. **Search Posts** → Tests search functionality
9. **Pagination Examples** → Tests pagination

**Note:** For category management (Create/Update/Delete), you must run **Admin Login** first to get `admin_access_token`.

## 📚 API Endpoints Covered

### Authentication
- ✅ `POST /api/auth/register` - Register new user
- ✅ `POST /api/auth/login` - Login and get tokens
- ✅ `POST /api/auth/login` (Admin) - Login as admin (username: admin, password: admin123)
- ✅ `GET /api/auth/me` - Get current user (requires auth)

### Posts
- ✅ `GET /api/posts` - List posts (paginated, 20 per page)
- ✅ `GET /api/posts/<id>` - Get post by ID
- ✅ `POST /api/posts` - Create post (requires auth)
- ✅ `PUT /api/posts/<id>` - Update post (requires auth, author/admin)
- ✅ `DELETE /api/posts/<id>` - Delete post (requires auth, author/admin)

### Search
- ✅ `GET /api/posts/search?q=keyword` - Search posts by keyword
- ✅ `GET /api/posts?search=keyword&category_id=X&tag=Y` - Search with filters

### Comments
- ✅ `GET /api/posts/<id>/comments` - Get comments for a post
- ✅ `GET /api/comments` - List all comments (paginated)
- ✅ `POST /api/comments` - Create comment (requires auth)
- ✅ `POST /api/comments` (with parent_id) - Create reply comment
- ✅ `GET /api/comments/<id>` - Get comment by ID
- ✅ `DELETE /api/comments/<id>` - Delete comment (requires auth, author/admin)

### Categories
- ✅ `GET /api/categories` - List categories (paginated)
- ✅ `GET /api/categories/<id>` - Get category by ID
- ✅ `POST /api/categories` - Create category (requires auth, admin only)
- ✅ `PUT /api/categories/<id>` - Update category (requires auth, admin only)
- ✅ `DELETE /api/categories/<id>` - Delete category (requires auth, admin only)

## 🔑 Authentication Flow

1. **Register** a new user (or use existing credentials)
2. **Login** to get `access_token`
3. Use `access_token` in Authorization header for protected endpoints:
   ```
   Authorization: Bearer {{access_token}}
   ```

The collection automatically:
- Saves tokens after login (`access_token`, `refresh_token`) - **no environment needed!**
- Saves admin tokens after admin login (`admin_access_token`, `admin_refresh_token`)
- Sets tokens in subsequent requests automatically
- Saves IDs for use in other requests (`user_id`, `post_id`, `comment_id`, `category_id`)

**All variables are stored at the collection level** - they persist across sessions and don't require an environment to be created.

## 📄 Request Examples

### Register User
```json
POST /api/auth/register
{
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "SecurePass123!",
    "first_name": "Test",
    "last_name": "User"
}
```

### Login
```json
POST /api/auth/login
{
    "username": "testuser",
    "password": "SecurePass123!"
}
```

### Admin Login
```json
POST /api/auth/login
{
    "username": "admin",
    "password": "admin123"
}
```
**Response:** Sets `admin_access_token` automatically (required for category management)

### Admin Login
```json
POST /api/auth/login
{
    "username": "admin",
    "password": "admin123"
}
```
**Response:** Sets `admin_access_token` automatically (required for category management)

### Create Post
```json
POST /api/posts
Authorization: Bearer {{access_token}}
{
    "title": "My First Blog Post",
    "content": "Full content here...",
    "excerpt": "Brief summary",
    "is_published": true,
    "tags": ["python", "flask", "api"],
    "category_ids": [1]
}
```

### Search Posts
```
GET /api/posts/search?q=python&page=1&per_page=20
```

### Create Comment
```json
POST /api/comments
Authorization: Bearer {{access_token}}
{
    "content": "Great post!",
    "post_id": 1
}
```

### Create Reply Comment
```json
POST /api/comments
Authorization: Bearer {{access_token}}
{
    "content": "I agree!",
    "post_id": 1,
    "parent_id": 1
}
```

## 📊 Pagination

All list endpoints support pagination:
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 20, max: 100)

**Example:**
```
GET /api/posts?page=1&per_page=20
GET /api/posts?page=2&per_page=20
GET /api/comments?page=1&per_page=20&post_id=1
GET /api/categories?page=1&per_page=20
```

## 🔍 Search Features

### Search Posts by Keyword
```
GET /api/posts/search?q=python
```

### Search with Filters
```
GET /api/posts?search=flask&category_id=1&tag=api&page=1&per_page=20
```

**Search Parameters:**
- `q` or `search` - Search keyword (searches in title, content, excerpt)
- `category_id` - Filter by category
- `tag` - Filter by tag
- `user_id` - Filter by author
- `published_only` - Show only published posts (default: true)

## 🧪 Testing Scenarios

### Scenario 1: User Registration and Login
1. Register User
2. Login
3. Get Current User

### Scenario 2: Post CRUD Operations
1. Get All Posts (Page 1)
2. Create Post
3. Get Post by ID
4. Update Post
5. Delete Post

### Scenario 3: Comment System
1. Get Comments for Post
2. Create Comment
3. Create Reply Comment
4. Get Comment by ID
5. Delete Comment

### Scenario 4: Category Management
1. Get All Categories
2. Get Category by ID
3. Create Category (Admin)
4. Update Category (Admin)
5. Delete Category (Admin)

### Scenario 5: Search and Pagination
1. Search Posts by Keyword
2. Search Posts with Filters
3. Get Posts - Page 1 (20 per page)
4. Get Posts - Page 2 (20 per page)

## 📝 Notes

- **Admin Access**: Category create/update/delete requires admin role
  - Use **Admin Login** request (username: `admin`, password: `admin123`) to get `admin_access_token`
  - Admin token is automatically saved and used in category management requests
- **Author Access**: Post/comment update/delete requires author or admin role
- **Token Expiry**: Access tokens expire after 1 hour, use refresh token to get new access token
- **Pagination**: Default is 20 items per page, maximum is 100 per page
- **Search**: Searches in post title, content, and excerpt fields

## 🔧 Troubleshooting

### 401 Unauthorized
- Make sure you've logged in and `access_token` is set
- Check that token hasn't expired
- Verify Authorization header format: `Bearer {{access_token}}`

### 403 Forbidden
- Category operations require admin role
- Post/comment operations require author or admin role

### 404 Not Found
- Verify IDs are correct (check environment variables)
- Make sure resources exist before accessing

### 400 Bad Request
- Check request body format
- Verify required fields are provided
- Check data validation rules

## 📖 API Documentation

For complete API documentation, visit:
- **Swagger UI**: http://localhost:5001/api/docs
- **Interactive Docs**: Full endpoint documentation with try-it-out functionality

---

**Collection Version**: 1.0  
**Last Updated**: 2026-02-03  
**API Base URL**: http://localhost:5001
