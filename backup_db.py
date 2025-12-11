"""
Enhanced Database Backup Utility
Provides robust backup, restore, and management features with comprehensive error handling
"""
import os
import shutil
import sqlite3
import hashlib
import json
from datetime import datetime
from pathlib import Path

# Configuration
DB_PATH = 'instance/poetry_app.db'
BACKUP_DIR = 'instance/backups'
MAX_BACKUPS = 10  # Keep last 10 backups
METADATA_FILE = 'instance/backups/backup_metadata.json'


class BackupManager:
    """Manages database backups with validation and metadata tracking"""
    
    def __init__(self):
        self.db_path = Path(DB_PATH)
        self.backup_dir = Path(BACKUP_DIR)
        self.metadata_file = Path(METADATA_FILE)
        self._ensure_backup_dir()
    
    def _ensure_backup_dir(self):
        """Create backup directory if it doesn't exist"""
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def _calculate_checksum(self, file_path):
        """Calculate MD5 checksum of a file for integrity verification"""
        md5 = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    md5.update(chunk)
            return md5.hexdigest()
        except Exception as e:
            print(f"⚠️  Warning: Could not calculate checksum: {e}")
            return None
    
    def _validate_database(self, db_path):
        """Validate database integrity"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            conn.close()
            return result[0] == 'ok'
        except Exception as e:
            print(f"⚠️  Database validation failed: {e}")
            return False
    
    def _get_database_stats(self, db_path):
        """Get database statistics"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            stats = {}
            
            # Get table counts
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                stats[table_name] = count
            
            conn.close()
            return stats
        except Exception as e:
            print(f"⚠️  Could not get database stats: {e}")
            return {}
    
    def _save_metadata(self, backup_path, stats, checksum):
        """Save backup metadata"""
        try:
            metadata = {}
            if self.metadata_file.exists():
                with open(self.metadata_file, 'r') as f:
                    metadata = json.load(f)
            
            backup_name = backup_path.name
            metadata[backup_name] = {
                'created': datetime.now().isoformat(),
                'size': backup_path.stat().st_size,
                'checksum': checksum,
                'stats': stats,
                'validated': True
            }
            
            with open(self.metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not save metadata: {e}")
    
    def _load_metadata(self):
        """Load backup metadata"""
        try:
            if self.metadata_file.exists():
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️  Could not load metadata: {e}")
        return {}
    
    def backup_database(self, description=None):
        """
        Create a timestamped backup of the database
        
        Args:
            description: Optional description for this backup
        
        Returns:
            bool: True if backup successful, False otherwise
        """
        print("="*60)
        print("🔄 Starting Database Backup")
        print("="*60)
        
        # Check if database exists
        if not self.db_path.exists():
            print("❌ Error: No database found to backup")
            print(f"   Expected location: {self.db_path}")
            return False
        
        # Validate database before backup
        print("🔍 Validating database integrity...")
        if not self._validate_database(self.db_path):
            print("❌ Error: Database integrity check failed")
            print("   The database may be corrupted. Backup aborted.")
            return False
        print("✅ Database integrity verified")
        
        # Get database statistics
        print("📊 Collecting database statistics...")
        stats = self._get_database_stats(self.db_path)
        
        # Create timestamped backup filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self.backup_dir / f'poetry_app_{timestamp}.db'
        
        # Copy database to backup
        try:
            print(f"💾 Creating backup...")
            shutil.copy2(self.db_path, backup_path)
            
            # Calculate checksum
            print("🔐 Calculating checksum...")
            checksum = self._calculate_checksum(backup_path)
            
            # Validate backup
            print("🔍 Validating backup...")
            if not self._validate_database(backup_path):
                print("❌ Error: Backup validation failed")
                backup_path.unlink()  # Delete invalid backup
                return False
            
            # Save metadata
            self._save_metadata(backup_path, stats, checksum)
            
            # Get file size
            file_size = backup_path.stat().st_size / 1024  # KB
            
            print("\n" + "="*60)
            print("✅ BACKUP SUCCESSFUL!")
            print("="*60)
            print(f"📁 Location: {backup_path}")
            print(f"📊 Size: {file_size:.2f} KB")
            print(f"🔐 Checksum: {checksum[:16]}...")
            print(f"📅 Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            if stats:
                print("\n📈 Database Contents:")
                for table, count in stats.items():
                    if not table.startswith('sqlite_'):
                        print(f"   {table}: {count} records")
            
            # Cleanup old backups
            self._cleanup_old_backups()
            
            return True
            
        except Exception as e:
            print(f"\n❌ BACKUP FAILED!")
            print(f"   Error: {e}")
            if backup_path.exists():
                backup_path.unlink()  # Clean up failed backup
            return False
    
    def list_backups(self):
        """List all available backups with detailed information"""
        if not self.backup_dir.exists():
            print("📦 No backups found")
            return
        
        backups = sorted(
            [f for f in self.backup_dir.glob('poetry_app_*.db')],
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        if not backups:
            print("📦 No backups found")
            return
        
        metadata = self._load_metadata()
        
        print("\n" + "="*60)
        print(f"📦 AVAILABLE BACKUPS ({len(backups)})")
        print("="*60)
        
        for i, backup in enumerate(backups, 1):
            backup_name = backup.name
            size = backup.stat().st_size / 1024  # KB
            mtime = datetime.fromtimestamp(backup.stat().st_mtime)
            
            print(f"\n{i}. {backup_name}")
            print(f"   📅 Created: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   📊 Size: {size:.2f} KB")
            
            # Show metadata if available
            if backup_name in metadata:
                meta = metadata[backup_name]
                if 'checksum' in meta:
                    print(f"   🔐 Checksum: {meta['checksum'][:16]}...")
                if 'stats' in meta:
                    total_records = sum(
                        count for table, count in meta['stats'].items()
                        if not table.startswith('sqlite_')
                    )
                    print(f"   📈 Total Records: {total_records}")
                if 'validated' in meta and meta['validated']:
                    print(f"   ✅ Validated")
        
        print("\n" + "="*60)
    
    def restore_backup(self, backup_filename):
        """
        Restore database from a backup
        
        Args:
            backup_filename: Name of the backup file to restore
        
        Returns:
            bool: True if restore successful, False otherwise
        """
        backup_path = self.backup_dir / backup_filename
        
        print("="*60)
        print("🔄 Starting Database Restore")
        print("="*60)
        
        # Check if backup exists
        if not backup_path.exists():
            print(f"❌ Error: Backup not found")
            print(f"   Looking for: {backup_path}")
            print("\n💡 Tip: Run 'python backup_db.py list' to see available backups")
            return False
        
        # Validate backup before restoring
        print("🔍 Validating backup integrity...")
        if not self._validate_database(backup_path):
            print("❌ Error: Backup integrity check failed")
            print("   The backup file may be corrupted. Restore aborted.")
            return False
        print("✅ Backup integrity verified")
        
        # Verify checksum if available
        metadata = self._load_metadata()
        if backup_filename in metadata and 'checksum' in metadata[backup_filename]:
            print("🔐 Verifying checksum...")
            stored_checksum = metadata[backup_filename]['checksum']
            current_checksum = self._calculate_checksum(backup_path)
            if stored_checksum != current_checksum:
                print("⚠️  Warning: Checksum mismatch!")
                print("   The backup file may have been modified.")
                response = input("   Continue anyway? (yes/no): ")
                if response.lower() != 'yes':
                    print("   Restore aborted.")
                    return False
            else:
                print("✅ Checksum verified")
        
        try:
            # Backup current database before restoring
            if self.db_path.exists():
                print("💾 Backing up current database...")
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                temp_backup = self.backup_dir / f'before_restore_{timestamp}.db'
                shutil.copy2(self.db_path, temp_backup)
                print(f"   Saved to: {temp_backup}")
            
            # Restore from backup
            print(f"🔄 Restoring database...")
            shutil.copy2(backup_path, self.db_path)
            
            # Validate restored database
            print("🔍 Validating restored database...")
            if not self._validate_database(self.db_path):
                print("❌ Error: Restored database validation failed")
                return False
            
            # Get stats
            stats = self._get_database_stats(self.db_path)
            
            print("\n" + "="*60)
            print("✅ RESTORE SUCCESSFUL!")
            print("="*60)
            print(f"📁 Restored from: {backup_filename}")
            print(f"📅 Restore time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            if stats:
                print("\n📈 Database Contents:")
                for table, count in stats.items():
                    if not table.startswith('sqlite_'):
                        print(f"   {table}: {count} records")
            
            return True
            
        except Exception as e:
            print(f"\n❌ RESTORE FAILED!")
            print(f"   Error: {e}")
            return False
    
    def _cleanup_old_backups(self):
        """Remove old backups, keeping only the most recent MAX_BACKUPS"""
        backups = sorted(
            [f for f in self.backup_dir.glob('poetry_app_*.db')],
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        if len(backups) > MAX_BACKUPS:
            print(f"\n🗑️  Cleaning up old backups (keeping last {MAX_BACKUPS})...")
            for old_backup in backups[MAX_BACKUPS:]:
                try:
                    old_backup.unlink()
                    print(f"   Removed: {old_backup.name}")
                except Exception as e:
                    print(f"   ⚠️  Could not remove {old_backup.name}: {e}")
    
    def verify_backup(self, backup_filename):
        """Verify a backup's integrity and checksum"""
        backup_path = self.backup_dir / backup_filename
        
        if not backup_path.exists():
            print(f"❌ Backup not found: {backup_filename}")
            return False
        
        print(f"🔍 Verifying backup: {backup_filename}")
        
        # Validate database
        if not self._validate_database(backup_path):
            print("❌ Database integrity check failed")
            return False
        print("✅ Database integrity verified")
        
        # Verify checksum
        metadata = self._load_metadata()
        if backup_filename in metadata and 'checksum' in metadata[backup_filename]:
            stored_checksum = metadata[backup_filename]['checksum']
            current_checksum = self._calculate_checksum(backup_path)
            if stored_checksum == current_checksum:
                print("✅ Checksum verified")
                return True
            else:
                print("❌ Checksum mismatch")
                return False
        else:
            print("⚠️  No checksum available for verification")
            return True


def main():
    """Main entry point for command-line usage"""
    import sys
    
    manager = BackupManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'backup':
            manager.backup_database()
        elif command == 'list':
            manager.list_backups()
        elif command == 'restore' and len(sys.argv) > 2:
            manager.restore_backup(sys.argv[2])
        elif command == 'verify' and len(sys.argv) > 2:
            manager.verify_backup(sys.argv[2])
        else:
            print("Enhanced Database Backup Utility")
            print("="*60)
            print("\nUsage:")
            print("  python backup_db.py backup           - Create a backup")
            print("  python backup_db.py list             - List all backups")
            print("  python backup_db.py restore <file>   - Restore from backup")
            print("  python backup_db.py verify <file>    - Verify backup integrity")
            print("\nExamples:")
            print("  python backup_db.py backup")
            print("  python backup_db.py list")
            print("  python backup_db.py restore poetry_app_20241209_143022.db")
            print("  python backup_db.py verify poetry_app_20241209_143022.db")
    else:
        # Default action: create backup
        manager.backup_database()


if __name__ == '__main__':
    main()
