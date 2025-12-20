#!/usr/bin/env python3
"""
Render-specific migration for PostgreSQL
Adds security columns to production database
"""

import os
from app import create_app
from models import db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_render_database():
    """Add security columns to Render PostgreSQL database"""
    app = create_app()
    
    with app.app_context():
        try:
            logger.info("Starting Render database migration...")
            
            # PostgreSQL-specific column additions
            migrations = [
                # Users table
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMP",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS privacy_settings TEXT",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_banned BOOLEAN DEFAULT FALSE",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS ban_reason VARCHAR(500)",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS failed_login_attempts INTEGER DEFAULT 0",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS account_locked_until TIMESTAMP",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS two_factor_enabled BOOLEAN DEFAULT FALSE",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS data_sharing_consent BOOLEAN DEFAULT FALSE",
                
                # Poems table
                "ALTER TABLE poems ADD COLUMN IF NOT EXISTS is_protected BOOLEAN DEFAULT FALSE",
                "ALTER TABLE poems ADD COLUMN IF NOT EXISTS visibility VARCHAR(20) DEFAULT 'public'",
                "ALTER TABLE poems ADD COLUMN IF NOT EXISTS content_warning VARCHAR(200)",
                "ALTER TABLE poems ADD COLUMN IF NOT EXISTS is_flagged BOOLEAN DEFAULT FALSE",
                "ALTER TABLE poems ADD COLUMN IF NOT EXISTS flag_reason VARCHAR(500)",
                
                # Comments table
                "ALTER TABLE comments ADD COLUMN IF NOT EXISTS is_protected BOOLEAN DEFAULT FALSE",
                "ALTER TABLE comments ADD COLUMN IF NOT EXISTS is_flagged BOOLEAN DEFAULT FALSE",
                "ALTER TABLE comments ADD COLUMN IF NOT EXISTS flag_reason VARCHAR(500)"
            ]
            
            for sql in migrations:
                try:
                    with db.engine.connect() as connection:
                        connection.execute(db.text(sql))
                        connection.commit()
                    logger.info(f"✅ Executed: {sql}")
                except Exception as e:
                    if "already exists" in str(e).lower():
                        logger.info(f"⚠️  Column already exists: {sql}")
                    else:
                        logger.error(f"❌ Error: {sql} - {str(e)}")
                        # Don't raise - continue with other migrations
            
            logger.info("✅ Render migration completed!")
            
        except Exception as e:
            logger.error(f"❌ Migration failed: {str(e)}")
            raise

if __name__ == '__main__':
    migrate_render_database()