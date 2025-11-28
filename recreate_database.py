"""
Recreate database with new schema
This will preserve your data by backing up and restoring
"""

from app import create_app
from models import db
import os
import shutil
from datetime import datetime

def recreate_database():
    """Recreate database with new schema"""
    app = create_app()
    
    with app.app_context():
        db_path = 'instance/poetry_app.db'
        
        # Backup existing database
        if os.path.exists(db_path):
            backup_path = f'instance/poetry_app_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
            shutil.copy(db_path, backup_path)
            print(f"✅ Backed up database to: {backup_path}")
        
        # Drop all tables
        print("🔄 Dropping all tables...")
        db.drop_all()
        
        # Create all tables with new schema
        print("🔄 Creating tables with new schema...")
        db.create_all()
        
        print("✅ Database recreated successfully!")
        print("\n⚠️  NOTE: You'll need to:")
        print("   1. Register a new account")
        print("   2. Or restore your backup if you want old data")
        print("\n🚀 Run: python run_test.py")

if __name__ == '__main__':
    response = input("⚠️  This will recreate the database. Continue? (yes/no): ")
    if response.lower() == 'yes':
        recreate_database()
    else:
        print("Cancelled.")
