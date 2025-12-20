#!/usr/bin/env python3
"""
Create admin account for production deployment
This script ensures an admin account exists on Render
"""

from app import create_app
from models import db, User
from werkzeug.security import generate_password_hash
import os

def create_admin_account():
    """Create admin account if it doesn't exist"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if admin already exists
            admin = User.query.filter_by(username='admin').first()
            
            if not admin:
                # Create admin account
                admin = User(
                    username='admin',
                    email='admin@poetryvault.com',
                    password_hash=generate_password_hash('admin123'),
                    is_admin=True,
                    age=25
                )
                db.session.add(admin)
                db.session.commit()
                print('✅ Admin account created successfully!')
                print('Username: admin')
                print('Password: admin123')
            else:
                print('✅ Admin account already exists')
                
        except Exception as e:
            print(f'❌ Error creating admin account: {e}')
            return False
            
    return True

if __name__ == '__main__':
    create_admin_account()