#!/usr/bin/env python3
"""
Migration script to add new features to Poetry Vault
- Add mood, theme columns to poems table
- Add subscription_tier, subscription_expires to users table
- Create collections, collection_poems, user_analytics tables
"""

from app import create_app
from models import db
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_database():
    app = create_app()
    
    with app.app_context():
        try:
            logger.info("Starting database migration...")
            
            # Add new columns to poems table
            try:
                logger.info("Adding mood and theme columns to poems table...")
                db.session.execute(text('ALTER TABLE poems ADD COLUMN mood VARCHAR(50)'))
                db.session.execute(text('ALTER TABLE poems ADD COLUMN theme VARCHAR(50)'))
                db.session.commit()
                logger.info("✓ Added mood and theme columns to poems")
            except Exception as e:
                if 'already exists' in str(e).lower() or 'duplicate column' in str(e).lower():
                    logger.info("✓ Mood and theme columns already exist")
                else:
                    logger.error(f"Error adding poem columns: {e}")
                db.session.rollback()
            
            # Add subscription columns to users table
            try:
                logger.info("Adding subscription columns to users table...")
                db.session.execute(text('ALTER TABLE users ADD COLUMN subscription_tier VARCHAR(20) DEFAULT \'free\''))
                db.session.execute(text('ALTER TABLE users ADD COLUMN subscription_expires TIMESTAMP'))
                db.session.commit()
                logger.info("✓ Added subscription columns to users")
            except Exception as e:
                if 'already exists' in str(e).lower() or 'duplicate column' in str(e).lower():
                    logger.info("✓ Subscription columns already exist")
                else:
                    logger.error(f"Error adding user columns: {e}")
                db.session.rollback()
            
            # Create new tables
            logger.info("Creating new tables...")
            db.create_all()
            logger.info("✓ Created all new tables")
            
            # Update existing users to have free tier
            try:
                logger.info("Setting default subscription tier for existing users...")
                db.session.execute(text('UPDATE users SET subscription_tier = \'free\' WHERE subscription_tier IS NULL'))
                db.session.commit()
                logger.info("✓ Updated user subscription tiers")
            except Exception as e:
                logger.error(f"Error updating user tiers: {e}")
                db.session.rollback()
            
            logger.info("✅ Database migration completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Migration failed: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    migrate_database()