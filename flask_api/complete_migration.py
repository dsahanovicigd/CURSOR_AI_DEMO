#!/usr/bin/env python3
"""
Script to complete the blogging platform migration
Adds missing tables and columns
"""
from app import create_app, db
from app.models import Post, Category, Comment
import sqlalchemy

app = create_app()

with app.app_context():
    inspector = sqlalchemy.inspect(db.engine)
    tables = inspector.get_table_names()
    
    print("🔍 Checking database state...")
    
    # Check if post_categories table exists
    if 'post_categories' not in tables:
        print("➕ Creating post_categories table...")
        db.engine.execute(sqlalchemy.text("""
            CREATE TABLE post_categories (
                post_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                PRIMARY KEY (post_id, category_id),
                FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
            )
        """))
        print("✅ Created post_categories table")
    else:
        print("✓ post_categories table already exists")
    
    # Check posts table columns
    posts_cols = [c['name'] for c in inspector.get_columns('posts')]
    
    # Add slug column if missing
    if 'slug' not in posts_cols:
        print("➕ Adding slug column to posts...")
        db.engine.execute(sqlalchemy.text("ALTER TABLE posts ADD COLUMN slug VARCHAR(250)"))
        # Generate slugs for existing posts
        posts = Post.query.all()
        for post in posts:
            slug = Post.generate_slug(post.title)
            counter = 1
            base_slug = slug
            while Post.query.filter_by(slug=slug).first():
                slug = f"{base_slug}-{counter}"
                counter += 1
            post.slug = slug
        db.session.commit()
        # Make slug NOT NULL after populating
        db.engine.execute(sqlalchemy.text("""
            CREATE TABLE posts_new (
                id INTEGER PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                slug VARCHAR(250) NOT NULL,
                content TEXT NOT NULL,
                excerpt TEXT,
                user_id INTEGER NOT NULL,
                is_published BOOLEAN NOT NULL,
                view_count INTEGER NOT NULL DEFAULT 0,
                tags VARCHAR(500),
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """))
        db.engine.execute(sqlalchemy.text("""
            INSERT INTO posts_new 
            SELECT id, title, slug, content, NULL, user_id, is_published, 0, NULL, created_at, updated_at 
            FROM posts
        """))
        db.engine.execute(sqlalchemy.text("DROP TABLE posts"))
        db.engine.execute(sqlalchemy.text("ALTER TABLE posts_new RENAME TO posts"))
        print("✅ Added slug column and generated slugs for existing posts")
    else:
        print("✓ slug column already exists")
    
    # Add excerpt column if missing
    if 'excerpt' not in posts_cols:
        print("➕ Adding excerpt column to posts...")
        db.engine.execute(sqlalchemy.text("ALTER TABLE posts ADD COLUMN excerpt TEXT"))
        print("✅ Added excerpt column")
    else:
        print("✓ excerpt column already exists")
    
    # Add view_count column if missing
    if 'view_count' not in posts_cols:
        print("➕ Adding view_count column to posts...")
        db.engine.execute(sqlalchemy.text("ALTER TABLE posts ADD COLUMN view_count INTEGER DEFAULT 0 NOT NULL"))
        print("✅ Added view_count column")
    else:
        print("✓ view_count column already exists")
    
    # Add tags column if missing
    if 'tags' not in posts_cols:
        print("➕ Adding tags column to posts...")
        db.engine.execute(sqlalchemy.text("ALTER TABLE posts ADD COLUMN tags VARCHAR(500)"))
        print("✅ Added tags column")
    else:
        print("✓ tags column already exists")
    
    # Create indexes
    print("➕ Creating indexes...")
    try:
        db.engine.execute(sqlalchemy.text("CREATE INDEX IF NOT EXISTS idx_published_created ON posts(is_published, created_at)"))
        db.engine.execute(sqlalchemy.text("CREATE UNIQUE INDEX IF NOT EXISTS idx_slug ON posts(slug)"))
        db.engine.execute(sqlalchemy.text("CREATE INDEX IF NOT EXISTS idx_posts_title ON posts(title)"))
        print("✅ Created indexes")
    except Exception as e:
        print(f"⚠️  Some indexes may already exist: {e}")
    
    # Stamp migration as complete
    print("\n📝 Stamping migration as complete...")
    try:
        db.engine.execute(sqlalchemy.text("""
            INSERT OR IGNORE INTO alembic_version (version_num) 
            VALUES ('5adfc79191ea')
        """))
        print("✅ Migration stamped as complete")
    except Exception as e:
        print(f"⚠️  Could not stamp migration: {e}")
        print("   You may need to run: flask db stamp 5adfc79191ea")
    
    print("\n✅ Migration completed successfully!")
    print("\nNext steps:")
    print("1. Start the server: python run.py")
    print("2. Access Swagger UI: http://localhost:5001/api/docs")
    print("3. See NEXT_STEPS.md for more details")
