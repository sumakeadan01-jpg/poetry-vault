"""
Enhanced Admin Password Reset Tool
Secure password reset utility for admin accounts
"""
from app import create_app
from models import db, User
import getpass
import sys


class AdminPasswordReset:
    """Manages secure admin password resets"""
    
    def __init__(self):
        self.app = create_app()
    
    def _print_section(self, title):
        """Print formatted section header"""
        print("\n" + "="*70)
        print(f"  {title}")
        print("="*70)
    
    def list_admin_users(self):
        """List all admin users"""
        with self.app.app_context():
            admins = User.query.filter_by(is_admin=True).all()
            
            if not admins:
                print("\n  ❌ No admin users found")
                return []
            
            print(f"\n  👑 Admin Users ({len(admins)}):")
            for i, admin in enumerate(admins, 1):
                print(f"     {i}. {admin.username:.<30} {admin.email}")
            
            return admins
    
    def reset_password(self, username=None):
        """
        Reset password for an admin user
        
        Args:
            username: Optional username to reset
        """
        with self.app.app_context():
            self._print_section("🔐 ADMIN PASSWORD RESET")
            
            # If no username provided, list admins and ask
            if not username:
                admins = self.list_admin_users()
                
                if not admins:
                    print("\n  💡 Tip: Make a user admin first using check_users.py")
                    return False
                
                username = input("\n  Enter admin username: ").strip()
            
            if not username:
                print("\n  ❌ Username required")
                return False
            
            # Find user
            user = User.query.filter_by(username=username).first()
            
            if not user:
                print(f"\n  ❌ User '{username}' not found")
                return False
            
            if not user.is_admin:
                print(f"\n  ⚠️  Warning: '{username}' is not an admin")
                confirm = input("  Continue anyway? (yes/no): ").strip().lower()
                if confirm != 'yes':
                    print("  Cancelled.")
                    return False
            
            # Display user info
            print(f"\n  👤 User Information:")
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
            print(f"     Password: (hidden for security)")
            print(f"\n  💡 Tip: Login with username '{user.username}' and your new password")
            
            return True
    
    def reset_by_email(self, email=None):
        """Reset password by email address"""
        with self.app.app_context():
            self._print_section("🔐 PASSWORD RESET BY EMAIL")
            
            if not email:
                email = input("\n  Enter email address: ").strip()
            
            if not email:
                print("\n  ❌ Email required")
                return False
            
            # Find user by email
            user = User.query.filter_by(email=email).first()
            
            if not user:
                print(f"\n  ❌ No user found with email: {email}")
                return False
            
            # Use the regular reset function
            return self.reset_password(user.username)
    
    def interactive_reset(self):
        """Interactive password reset"""
        self._print_section("🔐 ADMIN PASSWORD RESET TOOL")
        
        print("\n  Options:")
        print("     1. Reset by username")
        print("     2. Reset by email")
        print("     3. List all admins")
        print("     0. Cancel")
        
        choice = input("\n  Select option: ").strip()
        
        if choice == '1':
            self.reset_password()
        elif choice == '2':
            self.reset_by_email()
        elif choice == '3':
            self.list_admin_users()
        else:
            print("\n  Cancelled.")


def main():
    """Main entry point"""
    resetter = AdminPasswordReset()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'list':
            with resetter.app.app_context():
                resetter.list_admin_users()
        elif command == 'reset' and len(sys.argv) > 2:
            resetter.reset_password(sys.argv[2])
        elif command == 'email' and len(sys.argv) > 2:
            resetter.reset_by_email(sys.argv[2])
        else:
            print("Enhanced Admin Password Reset Tool")
            print("="*70)
            print("\nUsage:")
            print("  python reset_admin_password.py [command] [args]")
            print("\nCommands:")
            print("  list                  - List all admin users")
            print("  reset <username>      - Reset password by username")
            print("  email <email>         - Reset password by email")
            print("  (no args)             - Interactive mode")
            print("\nExamples:")
            print("  python reset_admin_password.py")
            print("  python reset_admin_password.py list")
            print("  python reset_admin_password.py reset Autumn")
            print("  python reset_admin_password.py email admin@example.com")
    else:
        # Interactive mode
        resetter.interactive_reset()


if __name__ == '__main__':
    main()
