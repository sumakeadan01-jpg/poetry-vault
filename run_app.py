"""
Run the Poetry Vault app with automatic backups
"""
import os
import threading
import time
from datetime import datetime
from backup_db import backup_database

def auto_backup_thread():
    """Background thread that creates backups every 6 hours"""
    print("💾 Auto-backup system started (every 6 hours)")
    
    # Create initial backup
    time.sleep(5)  # Wait for app to start
    backup_database()
    
    # Then backup every 6 hours
    while True:
        time.sleep(6 * 60 * 60)  # 6 hours in seconds
        backup_database()

if __name__ == '__main__':
    # Start backup thread
    backup_thread = threading.Thread(target=auto_backup_thread, daemon=True)
    backup_thread.start()
    
    # Import and run Flask app
    from app import app
    
    print("=" * 60)
    print("🚀 Poetry Vault Starting...")
    print("   🌐 App: http://localhost:5001")
    print("   💾 Auto-backup: Every 6 hours")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5001, debug=True)
