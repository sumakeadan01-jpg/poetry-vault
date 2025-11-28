"""
Check users in database and reset password if needed
"""

from app import create_app
from models import db, User

def check_users():
    app = create_app()
    
    with app.app_context():
        users = User.query.all()
        
        print("="*60)
        print(f"📊 Found {len(users)} users in database:")
        print("="*60)
        
        for user in users:
            print(f"\n👤 Username: {user.username}")
            print(f"   Email: {user.email}")
            print(f"   Admin: {user.is_admin}")
            print(f"   Tutorial seen: {user.has_seen_tutorial}")
        
        print("\n" + "="*60)
        print("🔧 Reset password for a user?")
        print("="*60)
        
        username = input("\nEnter username (or press Enter to skip): ").strip()
        
        if username:
            user = User.query.filter_by(username=username).first()
            if user:
                new_password = input("Enter new password: ").strip()
                if new_password:
                    user.set_password(new_password)
                    db.session.commit()
                    print(f"\n✅ Password updated for {username}")
                    print(f"   Username: {username}")
                    print(f"   Password: {new_password}")
            else:
                print(f"❌ User '{username}' not found")

if __name__ == '__main__':
    check_users()
