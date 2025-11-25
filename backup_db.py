"""
Database backup utility
Run this script to create a backup of your database
"""
import os
import shutil
from datetime import datetime

def backup_database():
    """Create a timestamped backup of the database"""
    db_path = 'instance/poetry_app.db'
    backup_dir = 'instance/backups'
    
    # Create backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Check if database exists
    if not os.path.exists(db_path):
        print("❌ No database found to backup")
        return False
    
    # Create timestamped backup filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f'{backup_dir}/poetry_app_{timestamp}.db'
    
    # Copy database to backup
    try:
        shutil.copy2(db_path, backup_path)
        file_size = os.path.getsize(backup_path) / 1024  # Size in KB
        print(f"✅ Database backed up successfully!")
        print(f"📁 Backup location: {backup_path}")
        print(f"📊 Backup size: {file_size:.2f} KB")
        return True
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False

def list_backups():
    """List all available backups"""
    backup_dir = 'instance/backups'
    
    if not os.path.exists(backup_dir):
        print("No backups found")
        return
    
    backups = [f for f in os.listdir(backup_dir) if f.endswith('.db')]
    
    if not backups:
        print("No backups found")
        return
    
    print(f"\n📦 Available backups ({len(backups)}):")
    print("-" * 60)
    
    for backup in sorted(backups, reverse=True):
        backup_path = os.path.join(backup_dir, backup)
        size = os.path.getsize(backup_path) / 1024
        mtime = datetime.fromtimestamp(os.path.getmtime(backup_path))
        print(f"  {backup}")
        print(f"    Created: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"    Size: {size:.2f} KB")
        print()

def restore_backup(backup_filename):
    """Restore database from a backup"""
    db_path = 'instance/poetry_app.db'
    backup_path = f'instance/backups/{backup_filename}'
    
    if not os.path.exists(backup_path):
        print(f"❌ Backup not found: {backup_filename}")
        return False
    
    try:
        # Backup current database before restoring
        if os.path.exists(db_path):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            temp_backup = f'instance/backups/before_restore_{timestamp}.db'
            shutil.copy2(db_path, temp_backup)
            print(f"📁 Current database backed up to: {temp_backup}")
        
        # Restore from backup
        shutil.copy2(backup_path, db_path)
        print(f"✅ Database restored from: {backup_filename}")
        return True
    except Exception as e:
        print(f"❌ Restore failed: {e}")
        return False

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'backup':
            backup_database()
        elif command == 'list':
            list_backups()
        elif command == 'restore' and len(sys.argv) > 2:
            restore_backup(sys.argv[2])
        else:
            print("Usage:")
            print("  python backup_db.py backup          - Create a backup")
            print("  python backup_db.py list            - List all backups")
            print("  python backup_db.py restore <file>  - Restore from backup")
    else:
        # Default action: create backup
        backup_database()
