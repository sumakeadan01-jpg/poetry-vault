"""
Delete specific test user accounts
Run this script to delete test accounts: Ked, test2, Selen
"""

from app import create_app
from models import db, User, Poem, Comment, Follow, Notification

app = create_app()

with app.app_context():
    # List of test usernames to delete
    test_usernames = ['Ked', 'test2', 'Selen']
    
    print("🗑️  Deleting test accounts...")
    print("-" * 50)
    
    for username in test_usernames:
        user = User.query.filter_by(username=username).first()
        
        if user:
            print(f"\n📝 Found user: {username} (ID: {user.id})")
            print(f"   Email: {user.email}")
            print(f"   Joined: {user.created_at}")
            
            # Count what will be deleted
            poems_count = Poem.query.filter_by(user_id=user.id).count()
            comments_count = Comment.query.filter_by(user_id=user.id).count()
            followers_count = Follow.query.filter_by(followed_id=user.id).count()
            following_count = Follow.query.filter_by(follower_id=user.id).count()
            
            print(f"   Will delete:")
            print(f"   - {poems_count} poems")
            print(f"   - {comments_count} comments")
            print(f"   - {followers_count} followers")
            print(f"   - {following_count} following")
            
            # Delete all user's poems (comments will cascade)
            Poem.query.filter_by(user_id=user.id).delete()
            
            # Delete all notifications
            Notification.query.filter_by(user_id=user.id).delete()
            Notification.query.filter_by(from_user_id=user.id).delete()
            
            # Delete all follow relationships
            Follow.query.filter_by(follower_id=user.id).delete()
            Follow.query.filter_by(followed_id=user.id).delete()
            
            # Delete all comments
            Comment.query.filter_by(user_id=user.id).delete()
            
            # Delete the user
            db.session.delete(user)
            
            print(f"   ✅ Deleted {username}")
        else:
            print(f"\n❌ User '{username}' not found")
    
    # Commit all changes
    db.session.commit()
    
    print("\n" + "=" * 50)
    print("✅ All test accounts deleted successfully!")
    print("=" * 50)
    
    # Show remaining users
    remaining_users = User.query.all()
    print(f"\n📊 Remaining users: {len(remaining_users)}")
    for user in remaining_users:
        print(f"   - {user.username} ({user.email})")
