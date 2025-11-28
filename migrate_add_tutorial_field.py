"""
Migration script to add has_seen_tutorial field to existing users
Run this once after deploying the tutorial feature
"""

from app import create_app
from models import db

def migrate_tutorial_field():
    """Add has_seen_tutorial field to User table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Try to add the column using raw SQL
            db.session.execute('ALTER TABLE users ADD COLUMN has_seen_tutorial BOOLEAN DEFAULT FALSE')
            db.session.commit()
            print("✅ Successfully added has_seen_tutorial column")
        except Exception as e:
            if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                print("✅ Column already exists, skipping...")
            else:
                print(f"❌ Error: {e}")
                print("\nAlternative: Drop and recreate tables (WARNING: loses data)")
                print("Or manually add column in database")

if __name__ == '__main__':
    migrate_tutorial_field()
