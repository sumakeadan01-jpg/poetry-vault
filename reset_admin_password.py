"""
Reset password for P0.1Autumn admin account
"""

from app import create_app
from models import db, User

app = create_app()

with app.app_context():
    # Find the P0.1Autumn user
    user = User.query.filter_by(username='P0.1Autumn').first()
    
    if user:
        print(f"✅ Found user: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Admin: {user.is_admin}")
        
        # Set new password
        new_password = input("\n🔑 Enter new password for P0.1Autumn: ")
        confirm_password = input("🔑 Confirm password: ")
        
        if new_password != confirm_password:
            print("❌ Passwords don't match!")
        else:
            user.set_password(new_password)
            db.session.commit()
            print(f"\n✅ Password updated successfully for {user.username}!")
            print(f"   You can now login with:")
            print(f"   Username: {user.username}")
            print(f"   Password: {new_password}")
    else:
        print("❌ User 'P0.1Autumn' not found!")
        print("\n📋 Available users:")
        all_users = User.query.all()
        for u in all_users:
            print(f"   - {u.username} ({u.email}) {'[ADMIN]' if u.is_admin else ''}")
