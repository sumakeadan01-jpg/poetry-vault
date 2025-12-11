"""
Enhanced Quick Password Reset Tool
Fast and secure password reset for any user
"""
from app import create_app
from models import db, User
import getpass
import sys


class QuickPasswordReset:
    """Quick password reset utility"""
    
    def __init__(self):
        self.app = create_app()
    
    def _print_section(self, title):
        """Print formatted section header"""
        print("\n" + "="*70)
        print(f"  {title}")
        print("="*70)
    
    def list_all_users(self):
        """List all users in database"""
        with self.app.app_context():
            users = User.query.order_by(User.username).all()
            
            if not users:
                print("\n  ❌ No users found in database")
                return []
            
            print(f"\n  👥 All Users ({len(users)}):")
            for i, user in enumerate(users, 1):
                admin_badge = " [ADMIN]" if user.is_admin else ""
                print(f"     {i}. {user.username:.<30} {user.email}{admin_badge}")
            
            return users
    
    def reset_password(self, identifier=None, by_email=False):
        """
        Reset password for a user
        
        Args:
            identifier: Username or email
            by_email: If True, search by email instead of username
        """
        with self.app.app_context():
            self._print_section("🔐 QUICK PASSWORD RESET")
            
            # If no identifier provided, list users and ask
            if not identifier:
                self.list_all_users()
                
                search_type = "email" if by_email else "username"
                identifier = input(f"\n  Enter {search_type}: ").strip()
            
            if not identifier:
                print(f"\n  ❌ {'Email' if by_email else 'Username'} required")
                return False
            
            # Find user
            if by_email:
                user = User.query.filter_by(email=identifier).first()
                search_desc = f"email '{identifier}'"
            else:
                user = User.query.filter_by(username=identifier).first()
                search_desc = f"username '{identifier}'"
            
            if not user:
                print(f"\n  ❌ No user found with {search_desc}")
                print(f"\n  💡 Tip: Run 'python reset_password_now.py list' to see all users")
                return False
            
            # Display user info
            print(f"\n  ✅ User Found!")
            print(f"     Username: {user.username}")
            print(f"     Email: {user.email}")
            print(f"     Admin: {'Yes' if user.is_admin else 'No'}")
            
            # Get new password securely
            print(f"\n  🔑 Enter New Password:")
            new_password = getpass.getpass("     Password: ")
            confirm_password = getpass.getpass("     Confirm: ")
            
            # Validate passwords
            if not new_password:
                print("\n  ❌ Password cannot be empty")
                return False
            
            if new_password != confirm_password:
                print("\n  ❌ Passwords don't match")
                return False
            
            if len(new_password) < 6:
                print("\n  ❌ Password must be at least 6 characters")
                return False
            
            # Update password
            user.set_password(new_password)
            db.session.commit()
            
            print(f"\n  " + "="*70)
            print(f"  ✅ PASSWORD RESET SUCCESSFUL!")
            print(f"  " + "="*70)
            print(f"\n  📝 Login Credentials:")
            print(f"     Username: {user.username}")
            print(f"     Email: {user.email}")
            print(f"     Password: (hidden for security)")
            print(f"\n  💡 You can now login with username '{user.username}' and your new password")
            
            # If admin, show admin login tip
            if user.is_admin:
                print(f"\n  👑 Admin Tip: Login with 'P0.1{user.username}' for admin access")
            
            return True
    
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
                print(f"\n  ❌ No users found matching '{search_term}'")
                return []
            
            print(f"\n  🔍 Search Results ({len(users)} found):")
            for i, user in enumerate(users, 1):
                admin_badge = " [ADMIN]" if user.is_admin else ""
                print(f"     {i}. {user.username:.<30} {user.email}{admin_badge}")
            
            return users
    
    def interactive_reset(self):
        """Interactive password reset"""
        self._print_section("🔐 QUICK PASSWORD RESET TOOL")
        
        print("\n  Options:")
        print("     1. Reset by username")
        print("     2. Reset by email")
        print("     3. Search users")
        print("     4. List all users")
        print("     0. Cancel")
        
        choice = input("\n  Select option: ").strip()
        
        if choice == '1':
            self.reset_password(by_email=False)
        elif choice == '2':
            self.reset_password(by_email=True)
        elif choice == '3':
            search_term = input("\n  Enter search term: ").strip()
            if search_term:
                self.search_user(search_term)
        elif choice == '4':
            self.list_all_users()
        else:
            print("\n  Cancelled.")


def main():
    """Main entry point"""
    resetter = QuickPasswordReset()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'list':
            with resetter.app.app_context():
                resetter.list_all_users()
        elif command == 'search' and len(sys.argv) > 2:
            with resetter.app.app_context():
                resetter.search_user(sys.argv[2])
        elif command == 'reset' and len(sys.argv) > 2:
            resetter.reset_password(sys.argv[2], by_email=False)
        elif command == 'email' and len(sys.argv) > 2:
            resetter.reset_password(sys.argv[2], by_email=True)
        else:
            print("Enhanced Quick Password Reset Tool")
            print("="*70)
            print("\nUsage:")
            print("  python reset_password_now.py [command] [args]")
            print("\nCommands:")
            print("  list                  - List all users")
            print("  search <term>         - Search users")
            print("  reset <username>      - Reset password by username")
            print("  email <email>         - Reset password by email")
            print("  (no args)             - Interactive mode")
            print("\nExamples:")
            print("  python reset_password_now.py")
            print("  python reset_password_now.py list")
            print("  python reset_password_now.py search john")
            print("  python reset_password_now.py reset Autumn")
            print("  python reset_password_now.py email user@example.com")
    else:
        # Interactive mode
        resetter.interactive_reset()


if __name__ == '__main__':
    main()
