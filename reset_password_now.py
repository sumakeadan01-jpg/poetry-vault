"""
Quick password reset script
Run this to reset your admin password
"""

from app import create_app
from models import db, User

app = create_app()

with app.app_context():
    print("🔍 Looking for user with email: sumakeadan01@gmail.com")
    
    user = User.query.filter_by(email='sumakeadan01@gmail.com').first()
    
    if user:
        print(f"\n✅ Found user!")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Admin: {user.is_admin}")
        
        # Ask user to enter new password
        print("\n" + "="*50)
        new_password = input("🔑 Enter NEW password: ")
        confirm_password = input("🔑 Confirm password: ")
        
        if new_password != confirm_password:
            print("\n❌ Passwords don't match! Try again.")
        elif len(new_password) < 6:
            print("\n❌ Password too short! Must be at least 6 characters.")
        else:
            user.set_password(new_password)
            db.session.commit()
            
            print(f"\n🎉 Password reset successful!")
            print(f"\n📝 Login credentials:")
            print(f"   Username: {user.username}")
            print(f"   Password: {new_password}")
            print(f"\n✅ You can now login with these credentials!")
    else:
        print("\n❌ User not found with that email")
        print("\n📋 All users in database:")
        all_users = User.query.all()
        for u in all_users:
            print(f"   - {u.username} ({u.email}) {'[ADMIN]' if u.is_admin else ''}")
