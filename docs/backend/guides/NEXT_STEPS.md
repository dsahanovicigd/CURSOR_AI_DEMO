# Next Steps - Blogging Platform Setup

## Current Status

✅ **Completed:**
- All models created (Post, Category, Comment)
- All routes implemented (Posts, Categories, Comments)
- Marshmallow schemas for validation
- Swagger UI documentation updated
- Migration file created

⚠️ **Migration Issue:**
- Database tables were partially created during a failed migration
- Need to resolve the migration state

## Step 1: Resolve Database Migration

You have two options:

### Option A: Mark Migration as Complete (If tables exist)

If the tables (`categories`, `comments`, `post_categories`) already exist in your database:

```bash
cd flask_api
source venv/bin/activate
export FLASK_APP=run.py

# Check if tables exist
python3 -c "from app import create_app, db; app = create_app(); app.app_context().push(); print([t for t in db.engine.table_names()])"

# If tables exist, stamp the migration as complete
flask db stamp 5adfc79191ea
```

### Option B: Clean Start (Recommended for Development)

If you're okay with losing existing data:

```bash
cd flask_api
source venv/bin/activate
export FLASK_APP=run.py

# Drop and recreate database
rm instance/flask_api_dev.db  # or your database file
flask db upgrade
```

### Option C: Manual Fix (If you have existing data)

1. Check what tables exist
2. Manually create missing tables or columns
3. Stamp the migration as complete

## Step 2: Verify Database Schema

After resolving the migration, verify all tables exist:

```bash
python3 -c "
from app import create_app, db
from app.models import *
app = create_app()
app.app_context().push()
tables = db.engine.table_names()
required = ['posts', 'categories', 'comments', 'post_categories', 'users']
missing = [t for t in required if t not in tables]
if missing:
    print(f'Missing tables: {missing}')
else:
    print('✅ All required tables exist')
"
```

## Step 3: Generate Slugs for Existing Posts

If you have existing posts without slugs:

```bash
python3 << EOF
from app import create_app, db
from app.models.post import Post

app = create_app()
with app.app_context():
    posts = Post.query.filter(Post.slug == None).all()
    if posts:
        for post in posts:
            slug = Post.generate_slug(post.title)
            counter = 1
            base_slug = slug
            while Post.query.filter_by(slug=slug).first():
                slug = f"{base_slug}-{counter}"
                counter += 1
            post.slug = slug
        db.session.commit()
        print(f"✅ Generated slugs for {len(posts)} posts")
    else:
        print("✅ No posts need slug generation")
EOF
```

## Step 4: Start the Server

```bash
cd flask_api
source venv/bin/activate
python run.py
```

The server will start on `http://localhost:5001`

## Step 5: Test the API

### Access Swagger UI
Open your browser and go to:
```
http://localhost:5001/api/docs
```

### Quick Test Commands

1. **Register a user:**
```bash
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

2. **Login:**
```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

3. **Create a category (as admin):**
```bash
curl -X POST http://localhost:5001/api/categories \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "Technology",
    "description": "Posts about technology"
  }'
```

4. **Create a post:**
```bash
curl -X POST http://localhost:5001/api/posts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "My First Blog Post",
    "content": "This is the content...",
    "excerpt": "A brief summary",
    "tags": ["python", "flask"],
    "category_ids": [1],
    "is_published": true
  }'
```

5. **Search posts:**
```bash
curl "http://localhost:5001/api/posts/search?q=python"
```

## Step 6: Create an Admin User (Optional)

To manage categories, you'll need an admin user:

```bash
python3 << EOF
from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    admin = User(
        username='admin',
        email='admin@example.com',
        role=User.ROLE_ADMIN,
        is_active=True
    )
    admin.set_password('admin123')
    
    if not User.query.filter_by(username='admin').first():
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created: username='admin', password='admin123'")
    else:
        print("ℹ️  Admin user already exists")
EOF
```

## Troubleshooting

### Issue: "table already exists"
- Tables were partially created
- Use Option A or B above to resolve

### Issue: "index already exists"
- Index names conflict
- Already fixed in the migration file (using `idx_comment_*` instead of `idx_*`)

### Issue: "slug is null"
- Existing posts need slugs generated
- Run Step 3 above

### Issue: "Cannot create category - Forbidden"
- Need admin role
- Create admin user (Step 6) or update existing user's role

## Documentation

- **API Documentation**: `BLOGGING_PLATFORM_README.md`
- **Migration Guide**: `BLOGGING_PLATFORM_MIGRATION.md`
- **Swagger UI**: `http://localhost:5001/api/docs`

## Quick Reference

### Key Endpoints

**Posts:**
- `GET /api/posts` - List posts
- `GET /api/posts/search?q=query` - Search posts
- `POST /api/posts` - Create post (auth required)
- `GET /api/posts/<id>` - Get post by ID
- `GET /api/posts/slug/<slug>` - Get post by slug

**Categories:**
- `GET /api/categories` - List categories
- `POST /api/categories` - Create category (admin only)
- `GET /api/categories/<id>` - Get category

**Comments:**
- `GET /api/comments` - List comments
- `POST /api/comments` - Create comment (auth required)
- `GET /api/comments/post/<post_id>` - Get post comments

## Next Development Steps

1. ✅ Core functionality complete
2. ⏭️ Add pagination improvements
3. ⏭️ Add rate limiting
4. ⏭️ Add caching for popular posts
5. ⏭️ Add image upload support
6. ⏭️ Add email notifications for comments
7. ⏭️ Add RSS feed support
8. ⏭️ Add post preview/featured images
