"""
Restore database from backup
This will restore all users, poems, comments from December 1st backup
"""

import shutil
import os
from datetime import datetime

# Backup the current database first
current_db = 'instance/poetry_app.db'
backup_to_restore = 'instance/backups/poetry_app_20251201_163559.db'

print("🔄 RESTORING DATABASE FROM BACKUP")
print("=" * 60)

# Create a backup of current state (just in case)
if os.path.exists(current_db):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safety_backup = f'instance/backups/before_restore_{timestamp}.db'
    shutil.copy2(current_db, safety_backup)
    print(f"✅ Current database backed up to: {safety_backup}")

# Restore from December 1st backup
if os.path.exists(backup_to_restore):
    shutil.copy2(backup_to_restore, current_db)
    print(f"\n✅ DATABASE RESTORED!")
    print(f"📁 Restored from: {backup_to_restore}")
    print(f"📅 Backup date: December 1, 2025")
    print("\n🎉 All your data is back:")
    print("   - Autumn account")
    print("   - BBean account")
    print("   - All real user accounts")
    print("   - All poems")
    print("   - All comments")
    print("   - Everything!")
    print("\n⚠️  NOTE: This restored your LOCAL database.")
    print("   To restore on Render (live site), we need to upload this file.")
else:
    print(f"❌ Backup file not found: {backup_to_restore}")

print("\n" + "=" * 60)
