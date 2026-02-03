#!/usr/bin/env python3
"""
Script to add missing columns to posts table
"""
from app import create_app, db
from app.models.post import Post
import sqlalchemy

app = create_app()

with app.app_context():
    inspector = sqlalchemy.inspect(db.engine)
    posts_cols = [c['name'] for c in inspector.get_columns('posts')]
    
    print("🔍 Checking posts table columns...")
    print(f"Current columns: {posts_cols}")
    
    # Add missing columns one by one
    with db.engine.connect() as conn:
        # Add slug column
        if 'slug' not in posts_cols:
            print("➕ Adding slug column...")
            conn.execute(sqlalchemy.text("ALTER TABLE posts ADD COLUMN slug VARCHAR(250)"))
            conn.commit()
            print("✅ Added slug column")
            
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
            print(f"✅ Generated slugs for {len(posts)} posts")
        else:
            print("✓ slug column already exists")
        
        # Add excerpt column
        if 'excerpt' not in posts_cols:
            print("➕ Adding excerpt column...")
            conn.execute(sqlalchemy.text("ALTER TABLE posts ADD COLUMN excerpt TEXT"))
            conn.commit()
            print("✅ Added excerpt column")
        else:
            print("✓ excerpt column already exists")
        
        # Add view_count column
        if 'view_count' not in posts_cols:
            print("➕ Adding view_count column...")
            conn.execute(sqlalchemy.text("ALTER TABLE posts ADD COLUMN view_count INTEGER DEFAULT 0"))
            conn.commit()
            print("✅ Added view_count column")
        else:
            print("✓ view_count column already exists")
        
        # Add tags column
        if 'tags' not in posts_cols:
            print("➕ Adding tags column...")
            conn.execute(sqlalchemy.text("ALTER TABLE posts ADD COLUMN tags VARCHAR(500)"))
            conn.commit()
            print("✅ Added tags column")
        else:
            print("✓ tags column already exists")
        
        # Create indexes
        print("➕ Creating indexes...")
        try:
            conn.execute(sqlalchemy.text("CREATE INDEX IF NOT EXISTS idx_published_created ON posts(is_published, created_at)"))
            conn.execute(sqlalchemy.text("CREATE UNIQUE INDEX IF NOT EXISTS ix_posts_slug ON posts(slug)"))
            conn.execute(sqlalchemy.text("CREATE INDEX IF NOT EXISTS idx_posts_title ON posts(title)"))
            conn.commit()
            print("✅ Created indexes")
        except Exception as e:
            print(f"⚠️  Some indexes may already exist: {e}")
    
    print("\n✅ Posts table migration completed!")
    print("\nYou can now use the search endpoint: GET /api/search?q=keyword")
