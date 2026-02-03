# Quick Start Guide - Blogging Platform API

## ✅ Migration Complete!

Now that the migration is done, here are your next steps:

## Step 1: Start the Server

```bash
cd flask_api
source venv/bin/activate
python run.py
```

The server will start on `http://localhost:5001`

## Step 2: Access Swagger UI

Open your browser and navigate to:
```
http://localhost:5001/api/docs
```

This gives you interactive API documentation where you can test all endpoints!

## Step 3: Test the API

### 3.1 Register a User

In Swagger UI, go to **Authentication** → **POST /api/auth/register**

Example request:
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "testpass123"
}
```

### 3.2 Login

Go to **Authentication** → **POST /api/auth/login**

Example request:
```json
{
  "username": "testuser",
  "password": "testpass123"
}
```

**Important:** Copy the `access_token` from the response!

### 3.3 Authorize in Swagger

1. Click the **🔒 Authorize** button (top right)
2. Enter: `Bearer YOUR_ACCESS_TOKEN` (include the word "Bearer" and a space)
3. Click **Authorize** then **Close**

Now all protected endpoints will use your token automatically!

### 3.4 Create a Category (Admin Only)

First, make your user an admin:

```bash
python3 << EOF
from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    user = User.query.filter_by(username='testuser').first()
    if user:
        user.role = User.ROLE_ADMIN
        db.session.commit()
        print("✅ User is now admin")
    else:
        print("User not found")
EOF
```

Then in Swagger: **Categories** → **POST /api/categories**

```json
{
  "name": "Technology",
  "description": "Posts about technology"
}
```

### 3.5 Create a Blog Post

Go to **Posts** → **POST /api/posts**

```json
{
  "title": "My First Blog Post",
  "content": "This is the full content of my blog post. It can be quite long and contain multiple paragraphs.",
  "excerpt": "A brief summary of the post",
  "tags": ["python", "flask", "api"],
  "category_ids": [1],
  "is_published": true
}
```

### 3.6 Search Posts

Go to **Posts** → **GET /api/posts/search**

Query parameters:
- `q`: Search term (e.g., "python")
- `page`: Page number (default: 1)
- `per_page`: Results per page (default: 20)

### 3.7 Create a Comment

Go to **Comments** → **POST /api/comments**

```json
{
  "content": "Great post! Thanks for sharing.",
  "post_id": 1
}
```

### 3.8 Get Post Comments

Go to **Comments** → **GET /api/comments/post/{post_id}**

## Step 4: Test with cURL (Alternative)

If you prefer command line:

```bash
# Set your token
TOKEN="your_access_token_here"

# Create a post
curl -X POST http://localhost:5001/api/posts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Test Post",
    "content": "Test content",
    "tags": ["test"],
    "is_published": true
  }'

# Search posts
curl "http://localhost:5001/api/posts/search?q=test"

# Get all posts
curl "http://localhost:5001/api/posts"
```

## Step 5: Verify Everything Works

Run these checks:

```bash
# Health check
curl http://localhost:5001/api/health

# List posts (should work without auth)
curl http://localhost:5001/api/posts

# List categories (should work without auth)
curl http://localhost:5001/api/categories
```

## Common Issues & Solutions

### Issue: "Forbidden: Admin access required"
**Solution:** Make your user an admin (see Step 3.4)

### Issue: "Post not found"
**Solution:** Make sure the post exists and is published (or you're the author)

### Issue: "Category with this name already exists"
**Solution:** Use a different category name or update the existing one

### Issue: "Token has expired"
**Solution:** Login again to get a new token

## API Endpoints Summary

### Public Endpoints (No Auth Required)
- `GET /api/posts` - List posts
- `GET /api/posts/search` - Search posts
- `GET /api/posts/{id}` - Get post by ID
- `GET /api/posts/slug/{slug}` - Get post by slug
- `GET /api/categories` - List categories
- `GET /api/categories/{id}` - Get category
- `GET /api/comments` - List comments
- `GET /api/comments/post/{post_id}` - Get post comments

### Protected Endpoints (Auth Required)
- `POST /api/posts` - Create post
- `PUT /api/posts/{id}` - Update post (author or admin)
- `DELETE /api/posts/{id}` - Delete post (author or admin)
- `POST /api/comments` - Create comment
- `PUT /api/comments/{id}` - Update comment (author or admin)
- `DELETE /api/comments/{id}` - Delete comment (author or admin)

### Admin Only Endpoints
- `POST /api/categories` - Create category
- `PUT /api/categories/{id}` - Update category
- `DELETE /api/categories/{id}` - Delete category

## Next Steps

1. ✅ **Start the server** - `python run.py`
2. ✅ **Test endpoints** - Use Swagger UI at `/api/docs`
3. ✅ **Create content** - Posts, categories, comments
4. ⏭️ **Integrate with frontend** - Connect your React/Vue/Angular app
5. ⏭️ **Add features** - Image uploads, rich text editor, etc.

## Documentation

- **Full API Docs**: `BLOGGING_PLATFORM_README.md`
- **Migration Guide**: `BLOGGING_PLATFORM_MIGRATION.md`
- **Next Steps**: `NEXT_STEPS.md`

## Need Help?

Check the Swagger UI at `http://localhost:5001/api/docs` for:
- Complete endpoint documentation
- Request/response examples
- Try-it-out functionality
- Schema definitions

Happy coding! 🚀
