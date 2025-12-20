#!/usr/bin/env python3
"""
Database migration to add security and privacy features
Adds new columns for user protection, privacy settings, and content security
"""

from app import create_app
from models import db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_security_features():
    """Add security and privacy columns to existing database"""
    app = create_app()
    
    with app.app_context():
        try:
            logger.info("Starting security features migration...")
            
            # Add new columns to users table
            user_columns = [
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMP",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS privacy_settings TEXT",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_banned BOOLEAN DEFAULT FALSE",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS ban_reason VARCHAR(500)",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS failed_login_attempts INTEGER DEFAULT 0",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS account_locked_until TIMESTAMP",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS two_factor_enabled BOOLEAN DEFAULT FALSE",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS data_sharing_consent BOOLEAN DEFAULT FALSE"
            ]
            
            # Add new columns to poems table
            poem_columns = [
                "ALTER TABLE poems ADD COLUMN IF NOT EXISTS is_protected BOOLEAN DEFAULT FALSE",
                "ALTER TABLE poems ADD COLUMN IF NOT EXISTS visibility VARCHAR(20) DEFAULT 'public'",
                "ALTER TABLE poems ADD COLUMN IF NOT EXISTS content_warning VARCHAR(200)",
                "ALTER TABLE poems ADD COLUMN IF NOT EXISTS is_flagged BOOLEAN DEFAULT FALSE",
                "ALTER TABLE poems ADD COLUMN IF NOT EXISTS flag_reason VARCHAR(500)"
            ]
            
            # Add new columns to comments table
            comment_columns = [
                "ALTER TABLE comments ADD COLUMN IF NOT EXISTS is_protected BOOLEAN DEFAULT FALSE",
                "ALTER TABLE comments ADD COLUMN IF NOT EXISTS is_flagged BOOLEAN DEFAULT FALSE",
                "ALTER TABLE comments ADD COLUMN IF NOT EXISTS flag_reason VARCHAR(500)"
            ]
            
            # Execute all migrations
            all_columns = user_columns + poem_columns + comment_columns
            
            for sql in all_columns:
                try:
                    with db.engine.connect() as connection:
                        connection.execute(db.text(sql))
                        connection.commit()
                    logger.info(f"✅ Executed: {sql}")
                except Exception as e:
                    if "already exists" in str(e).lower() or "duplicate column" in str(e).lower():
                        logger.info(f"⚠️  Column already exists: {sql}")
                    else:
                        logger.error(f"❌ Error executing {sql}: {str(e)}")
                        raise
            
            # Commit changes
            db.session.commit()
            
            logger.info("✅ Security features migration completed successfully!")
            
            # Verify the migration
            verify_migration()
            
        except Exception as e:
            logger.error(f"❌ Migration failed: {str(e)}")
            db.session.rollback()
            raise

def verify_migration():
    """Verify that all new columns were added successfully"""
    try:
        from models import User, Poem, Comment
        
        # Test creating objects with new fields
        logger.info("🔍 Verifying migration...")
        
        # Check if we can query the new columns
        user_count = User.query.filter_by(is_banned=False).count()
        poem_count = Poem.query.filter_by(is_protected=False).count()
        comment_count = Comment.query.filter_by(is_flagged=False).count()
        
        logger.info(f"✅ Verification successful!")
        logger.info(f"   - Users (not banned): {user_count}")
        logger.info(f"   - Poems (not protected): {poem_count}")
        logger.info(f"   - Comments (not flagged): {comment_count}")
        
    except Exception as e:
        logger.error(f"❌ Verification failed: {str(e)}")
        raise

def rollback_migration():
    """Rollback the security features migration (remove added columns)"""
    app = create_app()
    
    with app.app_context():
        try:
            logger.info("Rolling back security features migration...")
            
            # Remove columns from users table
            user_rollback = [
                "ALTER TABLE users DROP COLUMN IF EXISTS last_login",
                "ALTER TABLE users DROP COLUMN IF EXISTS privacy_settings",
                "ALTER TABLE users DROP COLUMN IF EXISTS is_banned",
                "ALTER TABLE users DROP COLUMN IF EXISTS ban_reason",
                "ALTER TABLE users DROP COLUMN IF EXISTS failed_login_attempts",
                "ALTER TABLE users DROP COLUMN IF EXISTS account_locked_until",
                "ALTER TABLE users DROP COLUMN IF EXISTS email_verified",
                "ALTER TABLE users DROP COLUMN IF EXISTS two_factor_enabled",
                "ALTER TABLE users DROP COLUMN IF EXISTS data_sharing_consent"
            ]
            
            # Remove columns from poems table
            poem_rollback = [
                "ALTER TABLE poems DROP COLUMN IF EXISTS is_protected",
                "ALTER TABLE poems DROP COLUMN IF EXISTS visibility",
                "ALTER TABLE poems DROP COLUMN IF EXISTS content_warning",
                "ALTER TABLE poems DROP COLUMN IF EXISTS is_flagged",
                "ALTER TABLE poems DROP COLUMN IF EXISTS flag_reason"
            ]
            
            # Remove columns from comments table
            comment_rollback = [
                "ALTER TABLE comments DROP COLUMN IF EXISTS is_protected",
                "ALTER TABLE comments DROP COLUMN IF EXISTS is_flagged",
                "ALTER TABLE comments DROP COLUMN IF EXISTS flag_reason"
            ]
            
            # Execute all rollbacks
            all_rollbacks = user_rollback + poem_rollback + comment_rollback
            
            for sql in all_rollbacks:
                try:
                    with db.engine.connect() as connection:
                        connection.execute(db.text(sql))
                        connection.commit()
                    logger.info(f"✅ Rolled back: {sql}")
                except Exception as e:
                    logger.warning(f"⚠️  Rollback warning for {sql}: {str(e)}")
            
            db.session.commit()
            logger.info("✅ Rollback completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Rollback failed: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'rollback':
        rollback_migration()
    else:
        migrate_security_features()