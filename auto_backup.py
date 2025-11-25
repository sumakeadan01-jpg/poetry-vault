"""
Automatic database backup system
This runs in the background and creates backups automatically
"""
import os
import shutil
import time
from datetime import datetime
import schedule

def backup_database():
    """Create a timestamped backup of the database"""
    db_path = 'instance/poetry_app.db'
    backup_dir = 'instance/backups'
    
    # Create backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ⚠️  No database found to backup")
        return False
    
    # Create timestamped backup filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f'{backup_dir}/poetry_app_{timestamp}.db'
    
    # Copy database to backup
    try:
        shutil.copy2(db_path, backup_path)
        file_size = os.path.getsize(backup_path) / 1024  # Size in KB
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Auto-backup created!")
        print(f"   📁 {backup_path}")
        print(f"   📊 Size: {file_size:.2f} KB")
        
        # Clean up old backups (keep last 10)
        cleanup_old_backups(backup_dir)
        return True
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Backup failed: {e}")
        return False

def cleanup_old_backups(backup_dir, keep_count=10):
    """Keep only the most recent backups"""
    try:
        backups = [f for f in os.listdir(backup_dir) if f.startswith('poetry_app_') and f.endswith('.db')]
        backups.sort(reverse=True)
        
        # Delete old backups beyond keep_count
        for old_backup in backups[keep_count:]:
            old_path = os.path.join(backup_dir, old_backup)
            os.remove(old_path)
            print(f"   🗑️  Removed old backup: {old_backup}")
    except Exception as e:
        print(f"   ⚠️  Cleanup warning: {e}")

def run_backup_scheduler():
    """Run the backup scheduler"""
    print("🔄 Automatic Backup System Started")
    print("=" * 60)
    print("📅 Backup Schedule:")
    print("   - Every 6 hours")
    print("   - Keeps last 10 backups")
    print("=" * 60)
    
    # Schedule backups every 6 hours
    schedule.every(6).hours.do(backup_database)
    
    # Create initial backup
    print("\n🚀 Creating initial backup...")
    backup_database()
    
    print("\n⏰ Scheduler running... (Press Ctrl+C to stop)")
    print("=" * 60)
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == '__main__':
    try:
        run_backup_scheduler()
    except KeyboardInterrupt:
        print("\n\n👋 Backup scheduler stopped")
