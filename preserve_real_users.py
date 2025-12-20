#!/usr/bin/env python3
"""
User Preservation System for Poetry Vault
Exports and imports real user accounts to survive deployments
"""

import sqlite3
import json
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

# Define which users are "real" vs auto-generated poet accounts
POET_ACCOUNTS = {
    'shakespeare@poetryvault.com',
    'rumi@poetryvault.com', 
    'emilydickinson@poetryvault.com',
    'edgarallanpoe@poetryvault.com',
    'waltwhitman@poetryvault.com',
    'lordbyron@poetryvault.com',
    'williamwordsworth@poetryvault.com',
    'johnkeats@poetryvault.com',
    'percyshelley@poetryvault.com',
    'robertburns@poetryvault.com',
    'robertfrost@poetryvault.com',
    'mayaangelou@poetryvault.com',
    'langstonhughes@poetryvault.com',
    'المتنبي@poetryvault.com',
    'قيسبنالملوح@poetryvault.com'
}

def export_real_users(db_path='instance/poetry_app.db', export_file='real_users_backup.json'):
    """Export real user accounts (excluding poet accounts)"""
    
    if not os.path.exists(db_path):
        print(f"Database not found: {db_path}")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get all users
        cursor.execute('''
            SELECT id, username, email, password_hash, is_admin, 
                   subscription_tier, subscription_expires, created_at
            FROM users
        ''')
        all_users = cursor.fetchall()
        
        # Filter out poet accounts
        real_users = []
        for user in all_users:
            user_id, username, email, password_hash, is_admin, sub_tier, sub_expires, created_at = user
            
            if email not in POET_ACCOUNTS:
                real_users.append({
                    'username': username,
                    'email': email,
                    'password_hash': password_hash,
                    'is_admin': bool(is_admin),
                    'subscription_tier': sub_tier or 'free',
                    'subscription_expires': sub_expires,
                    'created_at': created_at,
                    'original_id': user_id
                })
        
        # Export to JSON
        export_data = {
            'export_date': datetime.now().isoformat(),
            'real_users': real_users,
            'total_users_exported': len(real_users)
        }
        
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"Exported {len(real_users)} real users to {export_file}")
        
        if real_users:
            print("\nExported users:")
            for user in real_users:
                admin_flag = " (ADMIN)" if user['is_admin'] else ""
                print(f"  • {user['username']} - {user['email']}{admin_flag}")
        
        return True
        
    except Exception as e:
        print(f"Export failed: {e}")
        return False
    finally:
        conn.close()

def import_real_users(db_path='instance/poetry_app.db', import_file='real_users_backup.json'):
    """Import real user accounts after deployment"""
    
    if not os.path.exists(import_file):
        print(f"Backup file not found: {import_file}")
        return False
    
    if not os.path.exists(db_path):
        print(f"Database not found: {db_path}")
        return False
    
    # Load backup data
    with open(import_file, 'r', encoding='utf-8') as f:
        backup_data = json.load(f)
    
    real_users = backup_data.get('real_users', [])
    
    if not real_users:
        print("ℹ️  No real users to import")
        return True
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        imported_count = 0
        skipped_count = 0
        
        for user in real_users:
            # Check if user already exists
            cursor.execute('SELECT id FROM users WHERE email = ?', (user['email'],))
            existing = cursor.fetchone()
            
            if existing:
                print(f"User {user['email']} already exists, skipping")
                skipped_count += 1
                continue
            
            # Insert user
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, is_admin, 
                                 subscription_tier, subscription_expires, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                user['username'],
                user['email'], 
                user['password_hash'],
                user['is_admin'],
                user['subscription_tier'],
                user['subscription_expires'],
                user['created_at']
            ))
            
            imported_count += 1
            admin_flag = " (ADMIN)" if user['is_admin'] else ""
            print(f"Imported: {user['username']} - {user['email']}{admin_flag}")
        
        conn.commit()
        print(f"\n🎉 Successfully imported {imported_count} users, skipped {skipped_count}")
        return True
        
    except Exception as e:
        print(f"Import failed: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def create_deployment_user(username, email, password, is_admin=True, db_path='instance/poetry_app.db'):
    """Create a specific user account for deployment"""
    
    if not os.path.exists(db_path):
        print(f"Database not found: {db_path}")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if user exists
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            print(f"User {email} already exists")
            return False
        
        # Create user
        password_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, is_admin, 
                             subscription_tier, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            username, email, password_hash, is_admin, 'free', 
            datetime.now().isoformat()
        ))
        
        conn.commit()
        admin_flag = " (ADMIN)" if is_admin else ""
        print(f"Created user: {username} - {email}{admin_flag}")
        return True
        
    except Exception as e:
        print(f"Failed to create user: {e}")
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python preserve_real_users.py export")
        print("  python preserve_real_users.py import")
        print("  python preserve_real_users.py create <username> <email> <password>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'export':
        export_real_users()
    elif command == 'import':
        import_real_users()
    elif command == 'create' and len(sys.argv) >= 5:
        username, email, password = sys.argv[2], sys.argv[3], sys.argv[4]
        create_deployment_user(username, email, password)
    else:
        print("Invalid command")