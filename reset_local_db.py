"""
Reset local database with new schema
This is the easiest fix for the tutorial feature
"""

import os
import shutil
from datetime import datetime

def reset_database():
    """Delete and recreate database"""
    db_path = 'instance/poetry_app.db'
    
    if os.path.exists(db_path):
        # Backup first
        backup_path = f'instance/poetry_app_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        shutil.copy(db_path, backup_path)
        print(f"✅ Backed up to: {backup_path}")
        
        # Delete old database
        os.remove(db_path)
        print(f"✅ Deleted old database")
    
    print("\n🎉 Done! Now run: python run_test.py")
    print("📝 The app will create a new database with the correct schema")
    print("🔐 You'll need to register a new test account")

if __name__ == '__main__':
    print("="*60)
    print("🔄 Resetting Local Database")
    print("="*60)
    print()
    reset_database()
