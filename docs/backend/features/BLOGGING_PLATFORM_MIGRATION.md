# Blogging Platform Migration Guide

## Overview
This guide covers the database changes needed to support the new blogging platform features:
- Enhanced Post model with slug, excerpt, tags, and view_count
- Category model with many-to-many relationship to posts
- Comment model with nested replies support

## Database Changes Required

### 1. Posts Table Updates
Add new columns to the `posts` table:
- `slug` VARCHAR(250) UNIQUE NOT NULL - URL-friendly identifier
- `excerpt` TEXT - Short summary for previews
- `view_count` INTEGER DEFAULT 0 - Track post views
- `tags` VARCHAR(500) - Comma-separated tags

**Note:** For existing posts, slugs will need to be generated from titles.

### 2. New Categories Table
Create `categories` table:
- `id` INTEGER PRIMARY KEY
- `name` VARCHAR(100) UNIQUE NOT NULL
- `slug` VARCHAR(100) UNIQUE NOT NULL
- `description` TEXT
- `created_at` DATETIME
- `updated_at` DATETIME

### 3. New Post-Categories Association Table
Create `post_categories` table:
- `post_id` INTEGER (FK to posts.id)
- `category_id` INTEGER (FK to categories.id)
- Primary key on (post_id, category_id)

### 4. New Comments Table
Create `comments` table:
- `id` INTEGER PRIMARY KEY
- `content` TEXT NOT NULL
- `post_id` INTEGER (FK to posts.id)
- `user_id` INTEGER (FK to users.id)
- `parent_id` INTEGER (FK to comments.id) - For nested replies
- `is_approved` BOOLEAN DEFAULT TRUE
- `created_at` DATETIME
- `updated_at` DATETIME

## Migration Options

### Option 1: Using Flask-Migrate (Recommended)

```bash
cd flask_api
source venv/bin/activate

# Create migration
flask db migrate -m "Add blogging platform features"

# Review the migration file in migrations/versions/

# Apply migration
flask db upgrade
```

### Option 2: Manual SQL Migration

If you prefer manual migration, run these SQL commands:

```sql
-- Add new columns to posts table
ALTER TABLE posts ADD COLUMN slug VARCHAR(250);
ALTER TABLE posts ADD COLUMN excerpt TEXT;
ALTER TABLE posts ADD COLUMN view_count INTEGER DEFAULT 0;
ALTER TABLE posts ADD COLUMN tags VARCHAR(500);

-- Generate slugs for existing posts (if any)
-- This would need to be done via Python script

-- Create categories table
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

-- Create post_categories association table
CREATE TABLE post_categories (
    post_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (post_id, category_id),
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- Create comments table
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    parent_id INTEGER,
    is_approved BOOLEAN DEFAULT 1 NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES comments(id) ON DELETE CASCADE
);

-- Create indexes
CREATE INDEX idx_post_slug ON posts(slug);
CREATE INDEX idx_post_published_created ON posts(is_published, created_at);
CREATE INDEX idx_comment_post_created ON comments(post_id, created_at);
CREATE INDEX idx_comment_user_created ON comments(user_id, created_at);
CREATE INDEX idx_category_slug ON categories(slug);
```

### Option 3: Fresh Database (For Development)

If starting fresh, simply run:

```bash
cd flask_api
source venv/bin/activate
python3 -c "from app import create_app, db; from app.models import *; app = create_app(); app.app_context().push(); db.create_all()"
```

## Post-Migration Steps

### 1. Generate Slugs for Existing Posts

If you have existing posts without slugs, run this script:

```python
from app import create_app, db
from app.models.post import Post

app = create_app()
with app.app_context():
    posts = Post.query.filter(Post.slug == None).all()
    for post in posts:
        slug = Post.generate_slug(post.title)
        # Ensure uniqueness
        counter = 1
        base_slug = slug
        while Post.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        post.slug = slug
    db.session.commit()
    print(f"Generated slugs for {len(posts)} posts")
```

### 2. Verify Migration

Test the new endpoints:
- `GET /api/posts` - Should return posts with new fields
- `GET /api/categories` - Should return empty list (or categories if created)
- `GET /api/comments` - Should return empty list (or comments if created)
- `GET /api/posts/search?q=test` - Should work with search

## Rollback (If Needed)

If you need to rollback:

```bash
# Using Flask-Migrate
flask db downgrade

# Or manually drop tables
# DROP TABLE comments;
# DROP TABLE post_categories;
# DROP TABLE categories;
# ALTER TABLE posts DROP COLUMN slug;
# ALTER TABLE posts DROP COLUMN excerpt;
# ALTER TABLE posts DROP COLUMN view_count;
# ALTER TABLE posts DROP COLUMN tags;
```

## Notes

- The migration is designed to be backward compatible where possible
- Existing posts will work but may need slugs generated
- Comments and categories are new features, so no data migration needed
- All foreign keys use CASCADE DELETE for data integrity
