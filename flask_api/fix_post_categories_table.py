#!/usr/bin/env python3
"""
Script to create the post_categories association table
This table is required for the many-to-many relationship between posts and categories
"""
from app import create_app, db
from sqlalchemy import inspect, text

app = create_app()

with app.app_context():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    print("🔍 Checking database state...")
    
    if 'post_categories' not in tables:
        print("➕ Creating post_categories table...")
        try:
            db.engine.execute(text('''
                CREATE TABLE IF NOT EXISTS post_categories (
                    post_id INTEGER NOT NULL,
                    category_id INTEGER NOT NULL,
                    PRIMARY KEY (post_id, category_id),
                    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
                    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
                )
            '''))
            print("✅ Created post_categories table")
        except Exception as e:
            print(f"❌ Error creating table: {str(e)}")
            # Try alternative method
            try:
                from app.models.category import post_categories
                post_categories.create(db.engine, checkfirst=True)
                print("✅ Created post_categories table using model definition")
            except Exception as e2:
                print(f"❌ Alternative method also failed: {str(e2)}")
    else:
        print("✓ post_categories table already exists")
    
    # Verify the table was created
    inspector = inspect(db.engine)
    if 'post_categories' in inspector.get_table_names():
        print("✅ Verification: post_categories table exists")
        cols = inspector.get_columns('post_categories')
        print(f"   Columns: {[c['name'] for c in cols]}")
    else:
        print("❌ Verification failed: post_categories table still missing")
