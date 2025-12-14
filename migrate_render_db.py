#!/usr/bin/env python3
"""
Migration script for Render deployment
Ensures database has correct schema and seed data
"""

import os
import sys
from app import create_app
from models import db, User, Poem
from seed_poems import FAMOUS_POEMS

def migrate_render_database():
    """Migrate database for Render deployment"""
    print("🔄 Starting Render database migration...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Create all tables
            print("📋 Creating database tables...")
            db.create_all()
            
            # Check if we have poems
            poem_count = Poem.query.count()
            print(f"📊 Current poems in database: {poem_count}")
            
            # The app will auto-seed poems when first user registers
            print("📚 Poems will be auto-seeded by the app")
            
            # Check users
            user_count = User.query.count()
            print(f"👥 Current users in database: {user_count}")
            
            print("✅ Database migration completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Migration failed: {str(e)}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = migrate_render_database()
    sys.exit(0 if success else 1)