"""
Enhanced User Management Tool
Comprehensive user inspection, management, and password reset utility
"""
from app import create_app
from models import db, User, Poem, Comment, Like, Follow
from datetime import datetime
import getpass


class UserManager:
    """Manages user inspection and operations"""
    
    def __init__(self):
        self.app = create_app()
    
    def _print_section(self, title):
        """Print formatted section header"""
        print("\n" + "="*70)
        print(f"  {title}")
        print("="*70)
    
    def list_all_users(self, detailed=True):
        """List all users with detailed information"""
        with self.app.app_context():
            users = User.query.order_by(User.created_at.desc()).all()
            
            self._print_section(f"👥 ALL USERS ({len(users)} total)")
            
            # Categorize users
            admins = []
            classic_poets = []
            real_users = []
            
            for user in users:
                if user.is_admin:
                    admins.append(user)
                elif '@poetryvault.com' in user.email or '@poetry.vault' in user.email:
                    classic_poets.append(user)
                else:
                    real_users.append(user)
            
            print(f"\n  📊 Summary:")
            print(f"     Admins: {len(admins)}")
            print(f"     Classic Poets: {len(classic_poets)}")
            print(f"     Real Users: {len(real_users)}")
            
            # Display admins
            if admins:
                print(f"\n  🔑 ADMIN USERS:")
                for user in admins:
                    self._display_user(user, detailed)
            
            # Display real users
            if real_users:
                print(f"\n  👤 REAL USERS:")
                for user in real_users:
                    self._display_user(user, detailed)
            
            # Display classic poets (summary only)
            if classic_poets and detailed:
                print(f"\n  🎭 CLASSIC POETS:")
                for user in classic_poets:
                    poems_count = Poem.query.filter_by(user_id=user.id).count()
                    print(f"     • {user.username:.<30} {poems_count:>3} poems")
    
    def _display_user(self, user, detailed=True):
        """Display user information"""
        poems_count = Poem.query.filter_by(user_id=user.id, is_classic=False).count()
        comments_count = Comment.query.filter_by(user_id=user.id).count()
        likes_count = Like.query.filter_by(user_id=user.id).count()
        followers_count = Follow.query.filter_by(followed_id=user.id).count()
        following_count = Follow.query.filter_by(follower_id=user.id).count()
        
        created = user.created_at.strftime('%Y-%m-%d %H:%M') if user.created_at else 'Unknown'
        
        print(f"\n     • {user.username}")
        print(f"       Email: {user.email}")
        print(f"       Created: {created}")
        print(f"       Admin: {'Yes' if user.is_admin else 'No'}")
        print(f"       Tutorial Seen: {'Yes' if user.has_seen_tutorial else 'No'}")
        
        if detailed:
            print(f"       Poems: {poems_count} | Comments: {comments_count} | Likes: {likes_count}")
            print(f"       Followers: {followers_count} | Following: {following_count}")
    
    def search_user(self, search_term):
        """Search for users by username or email"""
        with self.app.app_context():
            users = User.query.filter(
                db.or_(
                    User.username.ilike(f'%{search_term}%'),
                    User.email.ilike(f'%{search_term}%')
                )
            ).all()
            
            if not users:
                print(f"\n❌ No users found matching '{search_term}'")
                return
            
            self._print_section(f"🔍 SEARCH RESULTS ({len(users)} found)")
            
            for user in users:
                self._display_user(user, detailed=True)
    
    def get_user_details(self, username):
        """Get detailed information about a specific user"""
        with self.app.app_context():
            user = User.query.filter_by(username=username).first()
            
            if not user:
                print(f"\n❌ User '{username}' not found")
                return None
            
            self._print_section(f"👤 USER DETAILS: {username}")
            
            # Basic info
            print(f"\n  📋 Basic Information:")
            print(f"     Username: {user.username}")
            print(f"     Email: {user.email}")
            print(f"     Age: {user.age if user.age else 'Not specified'}")
            print(f"     Favorite Poet: {user.favorite_poet if user.favorite_poet else 'Not specified'}")
            print(f"     Admin: {'Yes' if user.is_admin else 'No'}")
            print(f"     Tutorial Seen: {'Yes' if user.has_seen_tutorial else 'No'}")
            print(f"     Created: {user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else 'Unknown'}")
            
            # Content stats
            poems = Poem.query.filter_by(user_id=user.id, is_classic=False).all()
            comments = Comment.query.filter_by(user_id=user.id).all()
            likes = Like.query.filter_by(user_id=user.id).all()
            
            print(f"\n  📊 Content Statistics:")
            print(f"     Poems Written: {len(poems)}")
            print(f"     Comments Made: {len(comments)}")
            print(f"     Likes Given: {len(likes)}")
            
            # Social stats
            followers = Follow.query.filter_by(followed_id=user.id).all()
            following = Follow.query.filter_by(follower_id=user.id).all()
            
            print(f"\n  👥 Social Statistics:")
            print(f"     Followers: {len(followers)}")
            print(f"     Following: {len(following)}")
            
            # Recent poems
            if poems:
                print(f"\n  📚 Recent Poems:")
                for poem in poems[:5]:
                    likes_count = Like.query.filter_by(poem_id=poem.id).count()
                    comments_count = Comment.query.filter_by(poem_id=poem.id).count()
                    print(f"     • {poem.title[:40]:.<42} {likes_count:>2} ❤️  {comments_count:>2} 💬")
            
            return user
    
    def reset_password(self, username=None):
        """Reset password for a user"""
        with self.app.app_context():
            if not username:
                username = input("\n👤 Enter username: ").strip()
            
            if not username:
                print("❌ Username required")
                return False
            
            user = User.query.filter_by(username=username).first()
            
            if not user:
                print(f"❌ User '{username}' not found")
                return False
            
            print(f"\n🔐 Resetting password for: {username}")
            print(f"   Email: {user.email}")
            print(f"   Admin: {'Yes' if user.is_admin else 'No'}")
            
            # Get new password securely
            new_password = getpass.getpass("\n🔑 Enter new password: ")
            confirm_password = getpass.getpass("🔑 Confirm password: ")
            
            if new_password != confirm_password:
                print("❌ Passwords don't match")
                return False
            
            if len(new_password) < 6:
                print("❌ Password must be at least 6 characters")
                return False
            
            # Update password
            user.set_password(new_password)
            db.session.commit()
            
            print(f"\n✅ Password updated successfully!")
            print(f"   Username: {username}")
            print(f"   New password has been set")
            
            return True
    
    def toggle_admin(self, username):
        """Toggle admin status for a user"""
        with self.app.app_context():
            user = User.query.filter_by(username=username).first()
            
            if not user:
                print(f"❌ User '{username}' not found")
                return False
            
            user.is_admin = not user.is_admin
            db.session.commit()
            
            status = "granted" if user.is_admin else "revoked"
            print(f"✅ Admin access {status} for {username}")
            
            return True
    
    def delete_user(self, username):
        """Delete a user (with confirmation)"""
        with self.app.app_context():
            user = User.query.filter_by(username=username).first()
            
            if not user:
                print(f"❌ User '{username}' not found")
                return False
            
            # Show user details
            poems_count = Poem.query.filter_by(user_id=user.id).count()
            comments_count = Comment.query.filter_by(user_id=user.id).count()
            
            print(f"\n⚠️  WARNING: About to delete user '{username}'")
            print(f"   This will also delete:")
            print(f"   - {poems_count} poems")
            print(f"   - {comments_count} comments")
            print(f"   - All likes, follows, and notifications")
            
            confirm = input(f"\n   Type '{username}' to confirm deletion: ").strip()
            
            if confirm != username:
                print("❌ Deletion cancelled")
                return False
            
            # Delete user (cascades will handle related data)
            db.session.delete(user)
            db.session.commit()
            
            print(f"✅ User '{username}' deleted successfully")
            
            return True
    
    def interactive_menu(self):
        """Interactive menu for user management"""
        while True:
            self._print_section("🔧 USER MANAGEMENT TOOL")
            
            print("\n  Options:")
            print("     1. List all users")
            print("     2. Search users")
            print("     3. View user details")
            print("     4. Reset password")
            print("     5. Toggle admin status")
            print("     6. Delete user")
            print("     0. Exit")
            
            choice = input("\n  Select option: ").strip()
            
            if choice == '1':
                self.list_all_users(detailed=True)
            elif choice == '2':
                search_term = input("\n  Enter search term: ").strip()
                if search_term:
                    self.search_user(search_term)
            elif choice == '3':
                username = input("\n  Enter username: ").strip()
                if username:
                    self.get_user_details(username)
            elif choice == '4':
                self.reset_password()
            elif choice == '5':
                username = input("\n  Enter username: ").strip()
                if username:
                    self.toggle_admin(username)
            elif choice == '6':
                username = input("\n  Enter username: ").strip()
                if username:
                    self.delete_user(username)
            elif choice == '0':
                print("\n👋 Goodbye!")
                break
            else:
                print("\n❌ Invalid option")
            
            input("\nPress Enter to continue...")


def main():
    """Main entry point"""
    import sys
    
    manager = UserManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'list':
            manager.list_all_users(detailed=True)
        elif command == 'search' and len(sys.argv) > 2:
            manager.search_user(sys.argv[2])
        elif command == 'details' and len(sys.argv) > 2:
            manager.get_user_details(sys.argv[2])
        elif command == 'reset' and len(sys.argv) > 2:
            manager.reset_password(sys.argv[2])
        elif command == 'admin' and len(sys.argv) > 2:
            manager.toggle_admin(sys.argv[2])
        elif command == 'delete' and len(sys.argv) > 2:
            manager.delete_user(sys.argv[2])
        else:
            print("Enhanced User Management Tool")
            print("="*70)
            print("\nUsage:")
            print("  python check_users.py [command] [args]")
            print("\nCommands:")
            print("  list                  - List all users")
            print("  search <term>         - Search users")
            print("  details <username>    - View user details")
            print("  reset <username>      - Reset password")
            print("  admin <username>      - Toggle admin status")
            print("  delete <username>     - Delete user")
            print("\nExamples:")
            print("  python check_users.py list")
            print("  python check_users.py search john")
            print("  python check_users.py details Autumn")
            print("  python check_users.py reset Autumn")
    else:
        # Default: interactive menu
        manager.interactive_menu()


if __name__ == '__main__':
    main()
