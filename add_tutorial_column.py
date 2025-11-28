"""
Add has_seen_tutorial column to existing database
Keeps all users and data intact
"""

import sqlite3
import os

def add_column():
    """Add has_seen_tutorial column to users table"""
    
    db_path = 'instance/poetry_app.db'
    
    if not os.path.exists(db_path):
        print("❌ Database not found at:", db_path)
        return
    
    print(f"📍 Database: {db_path}")
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'has_seen_tutorial' in columns:
            print("✅ Column 'has_seen_tutorial' already exists!")
        else:
            print("🔄 Adding 'has_seen_tutorial' column...")
            
            # Add the column
            cursor.execute("ALTER TABLE users ADD COLUMN has_seen_tutorial BOOLEAN DEFAULT 0")
            
            # Set all existing users to 0 (False)
            cursor.execute("UPDATE users SET has_seen_tutorial = 0")
            
            conn.commit()
            
            # Verify
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            print(f"✅ Successfully added column!")
            print(f"✅ Updated {user_count} existing users")
            print(f"✅ All users will see tutorial once")
        
        conn.close()
        
        print("\n🎉 Done! Now run: python run_test.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nIf you see 'duplicate column' error, the column already exists.")

if __name__ == '__main__':
    print("="*60)
    print("🔧 Adding Tutorial Column to Database")
    print("="*60)
    print()
    add_column()
