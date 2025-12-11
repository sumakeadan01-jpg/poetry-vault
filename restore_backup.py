"""
Enhanced Database Restore Utility
Interactive tool for safely restoring database from backups
"""
import sys
from pathlib import Path
from backup_db import BackupManager


def interactive_restore():
    """Interactive restore process with user selection"""
    manager = BackupManager()
    
    print("\n" + "="*60)
    print("🔄 INTERACTIVE DATABASE RESTORE")
    print("="*60)
    
    # List available backups
    backup_dir = Path('instance/backups')
    if not backup_dir.exists():
        print("\n❌ No backups directory found")
        return False
    
    backups = sorted(
        [f for f in backup_dir.glob('poetry_app_*.db')],
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )
    
    if not backups:
        print("\n❌ No backups found")
        print("💡 Tip: Create a backup first with 'python backup_db.py backup'")
        return False
    
    # Display backups
    print(f"\n📦 Found {len(backups)} backup(s):\n")
    for i, backup in enumerate(backups, 1):
        from datetime import datetime
        size = backup.stat().st_size / 1024  # KB
        mtime = datetime.fromtimestamp(backup.stat().st_mtime)
        print(f"{i}. {backup.name}")
        print(f"   📅 Created: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   📊 Size: {size:.2f} KB")
        print()
    
    # Get user selection
    while True:
        try:
            choice = input("Select backup number to restore (or 'q' to quit): ").strip()
            
            if choice.lower() == 'q':
                print("Restore cancelled")
                return False
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(backups):
                selected_backup = backups[choice_num - 1]
                break
            else:
                print(f"❌ Please enter a number between 1 and {len(backups)}")
        except ValueError:
            print("❌ Please enter a valid number or 'q' to quit")
    
    # Confirm restore
    print(f"\n⚠️  WARNING: This will replace your current database!")
    print(f"   Selected backup: {selected_backup.name}")
    confirm = input("\nType 'YES' to confirm restore: ").strip()
    
    if confirm != 'YES':
        print("Restore cancelled")
        return False
    
    # Perform restore
    return manager.restore_backup(selected_backup.name)


def quick_restore(backup_filename):
    """Quick restore from specified backup"""
    manager = BackupManager()
    return manager.restore_backup(backup_filename)


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # Quick restore mode with specified backup
        backup_filename = sys.argv[1]
        success = quick_restore(backup_filename)
    else:
        # Interactive mode
        success = interactive_restore()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
