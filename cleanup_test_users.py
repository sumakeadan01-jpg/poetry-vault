#!/usr/bin/env python3
"""
Clean up test user accounts while preserving classic poets
Removes accounts like 'autumn', 'bbean', etc. but keeps Shakespeare, Rumi, etc.
"""

from app import create_app
from models import db, User, Poem, Comment, Follow, SavedPoem, Like, Notification
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def cleanup_test_users():
    app = create_app()
    
    with app.app_context():
        try:
            # Define classic poets to preserve
            classic_poets = [
                'Shakespeare', 'Rumi', 'Emily Dickinson', 'Edgar Allan Poe',
                'Walt Whitman', 'Lord Byron', 'William Wordsworth',
                'John Keats', 'Percy Shelley', 'Robert Burns',
                'Robert Frost', 'Maya Angelou', 'Langston Hughes',
                'المتنبي', 'قيس بن الملوح'
            ]
            
            # Get all users
            all_users = User.query.all()
            
            logger.info(f"Found {len(all_users)} total users")
            
            # Show current users
            logger.info("Current users in database:")
            for user in all_users:
                user_type = "CLASSIC POET" if user.username in classic_poets else "TEST USER"
                logger.info(f"  - {user.username} ({user_type})")
            
            # Find test users to delete (not classic poets)
            test_users = [user for user in all_users if user.username not in classic_poets]
            
            if not test_users:
                logger.info("✅ No test users found to delete")
                return
            
            logger.info(f"\n🗑️  Will delete {len(test_users)} test users:")
            for user in test_users:
                logger.info(f"  - {user.username} (ID: {user.id})")
            
            # Confirm deletion
            confirm = input(f"\nDelete {len(test_users)} test users? (y/N): ").strip().lower()
            if confirm != 'y':
                logger.info("❌ Deletion cancelled")
                return
            
            # Delete test users and their data
            deleted_count = 0
            for user in test_users:
                try:
                    user_id = user.id
                    username = user.username
                    
                    # Delete user's poems (comments will cascade)
                    user_poems = Poem.query.filter_by(user_id=user_id, is_classic=False).all()
                    for poem in user_poems:
                        db.session.delete(poem)
                    
                    # Delete user's comments
                    Comment.query.filter_by(user_id=user_id).delete()
                    
                    # Delete user's likes
                    Like.query.filter_by(user_id=user_id).delete()
                    
                    # Delete user's saved poems
                    SavedPoem.query.filter_by(user_id=user_id).delete()
                    
                    # Delete user's notifications
                    Notification.query.filter_by(user_id=user_id).delete()
                    
                    # Delete follow relationships
                    Follow.query.filter_by(follower_id=user_id).delete()
                    Follow.query.filter_by(followed_id=user_id).delete()
                    
                    # Delete the user account
                    db.session.delete(user)
                    
                    deleted_count += 1
                    logger.info(f"✅ Deleted user: {username}")
                    
                except Exception as e:
                    logger.error(f"❌ Error deleting user {username}: {str(e)}")
                    db.session.rollback()
                    continue
            
            # Commit all deletions
            db.session.commit()
            
            logger.info(f"\n🎉 Successfully deleted {deleted_count} test users")
            logger.info("✅ Classic poets preserved:")
            
            # Show remaining users
            remaining_users = User.query.all()
            for user in remaining_users:
                logger.info(f"  - {user.username}")
            
        except Exception as e:
            logger.error(f"❌ Error during cleanup: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    cleanup_test_users()