"""
Enhanced Development Server with Auto-Backup
Runs Poetry Vault with automatic backups and enhanced logging
"""
import os
import sys
import threading
import time
from datetime import datetime
from pathlib import Path


def auto_backup_thread(interval_hours=6):
    """Background thread that creates backups at specified intervals"""
    from backup_db import BackupManager
    
    manager = BackupManager()
    
    print(f"💾 Auto-backup system started (every {interval_hours} hours)")
    
    # Wait for app to start
    time.sleep(5)
    
    # Create initial backup
    print("\n🔄 Creating initial backup...")
    manager.backup_database()
    
    # Then backup at intervals
    while True:
        time.sleep(interval_hours * 60 * 60)  # Convert hours to seconds
        print(f"\n🔄 Scheduled backup (every {interval_hours} hours)...")
        manager.backup_database()


def check_environment():
    """Check and setup development environment"""
    # Ensure required directories exist
    Path('instance').mkdir(exist_ok=True)
    Path('instance/backups').mkdir(exist_ok=True)
    Path('instance/uploads').mkdir(exist_ok=True)
    
    # Check if database exists
    db_path = Path('instance/poetry_app.db')
    if not db_path.exists():
        print("\n⚠️  No database found!")
        print("   The app will create a new database and auto-seed with classic poems.")
        print("   Or run 'python seed_poems.py' to seed manually.\n")


def print_startup_info(port=5001, backup_interval=6):
    """Print startup information"""
    print("\n" + "="*70)
    print("  🚀 POETRY VAULT - DEVELOPMENT SERVER")
    print("="*70)
    print(f"\n  📍 Server:")
    print(f"     Local:    http://localhost:{port}")
    print(f"     Network:  http://0.0.0.0:{port}")
    print(f"\n  💾 Auto-Backup:")
    print(f"     Enabled:  Yes")
    print(f"     Interval: Every {backup_interval} hours")
    print(f"     Location: instance/backups/")
    print(f"\n  🔧 Development Mode:")
    print(f"     Debug:    Enabled")
    print(f"     Reloader: Enabled")
    print(f"     Hot Reload: Yes")
    print(f"\n  🛑 Stop Server:")
    print(f"     Press Ctrl+C")
    print("\n" + "="*70 + "\n")


def main():
    """Main entry point"""
    # Parse command line arguments
    port = 5001
    backup_interval = 6
    enable_backup = True
    
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith('--port='):
                try:
                    port = int(arg.split('=')[1])
                except ValueError:
                    print(f"❌ Invalid port: {arg}")
                    sys.exit(1)
            elif arg.startswith('--backup-interval='):
                try:
                    backup_interval = int(arg.split('=')[1])
                except ValueError:
                    print(f"❌ Invalid backup interval: {arg}")
                    sys.exit(1)
            elif arg == '--no-backup':
                enable_backup = False
            elif arg == '--help':
                print("Enhanced Development Server")
                print("="*70)
                print("\nUsage:")
                print("  python run_app.py [options]")
                print("\nOptions:")
                print("  --port=<port>              Port to run on (default: 5001)")
                print("  --backup-interval=<hours>  Backup interval (default: 6)")
                print("  --no-backup                Disable auto-backup")
                print("  --help                     Show this help")
                print("\nExamples:")
                print("  python run_app.py")
                print("  python run_app.py --port=5002")
                print("  python run_app.py --backup-interval=3")
                print("  python run_app.py --no-backup")
                sys.exit(0)
    
    # Check environment
    check_environment()
    
    # Start backup thread if enabled
    if enable_backup:
        backup_thread = threading.Thread(
            target=auto_backup_thread,
            args=(backup_interval,),
            daemon=True
        )
        backup_thread.start()
    
    # Print startup info
    print_startup_info(port, backup_interval)
    
    # Import and run Flask app
    try:
        from app import app
        
        # Run with enhanced settings
        app.run(
            host='0.0.0.0',
            port=port,
            debug=True,
            use_reloader=True,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("  🛑 Server stopped")
        print("="*70)
        print("\n  💾 Backups saved in: instance/backups/")
        print("  📊 Database saved in: instance/poetry_app.db")
        print("\n  👋 Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
