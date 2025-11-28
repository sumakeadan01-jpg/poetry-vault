"""
Fix database by adding has_seen_tutorial column
Run this if migration script doesn't work
"""

from app import create_app
from models import db
import sqlite3

def fix_database():
    """Add has_seen_tutorial column to users table"""
    app = create_app()
    
    with app.app_context():
        # Get database path
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
        else:
            db_path = 'instance/poetry_app.db'
        
        print(f"📍 Database: {db_path}")
        
        try:
            # Connect directly to SQLite
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if column exists
            cursor.execute("PRAGMA table_info(users)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'has_seen_tutorial' in columns:
                print("✅ Column 'has_seen_tutorial' already exists!")
            else:
                # Add the column
                cursor.execute("ALTER TABLE users ADD COLUMN has_seen_tutorial BOOLEAN DEFAULT 0")
                conn.commit()
                print("✅ Successfully added 'has_seen_tutorial' column!")
                
                # Set all existing users to False (0)
                cursor.execute("UPDATE users SET has_seen_tutorial = 0")
                conn.commit()
                print("✅ Set all existing users to has_seen_tutorial = False")
            
            conn.close()
            print("\n🎉 Database is ready!")
            print("You can now run the app: python run_test.py")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("\nTry Option 3 below...")

if __name__ == '__main__':
    fix_database()
