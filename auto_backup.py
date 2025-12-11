"""
Enhanced Automatic Database Backup System
Runs in the background with intelligent scheduling, notifications, and error recovery
"""
import os
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
import schedule
from backup_db import BackupManager

# Configuration
BACKUP_INTERVAL_HOURS = 6
MAX_BACKUPS = 10
LOG_FILE = 'instance/backups/auto_backup.log'
ENABLE_NOTIFICATIONS = True


class AutoBackupScheduler:
    """Manages automatic database backups with intelligent scheduling"""
    
    def __init__(self, interval_hours=BACKUP_INTERVAL_HOURS):
        self.interval_hours = interval_hours
        self.backup_manager = BackupManager()
        self.last_backup_time = None
        self.backup_count = 0
        self.failed_count = 0
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging to file and console"""
        log_dir = Path(LOG_FILE).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.FileHandler(LOG_FILE),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _log_system_info(self):
        """Log system information"""
        self.logger.info("="*60)
        self.logger.info("🔄 AUTOMATIC BACKUP SYSTEM")
        self.logger.info("="*60)
        self.logger.info(f"📅 Backup Interval: Every {self.interval_hours} hours")
        self.logger.info(f"📦 Max Backups: {MAX_BACKUPS}")
        self.logger.info(f"📁 Log File: {LOG_FILE}")
        self.logger.info(f"🔔 Notifications: {'Enabled' if ENABLE_NOTIFICATIONS else 'Disabled'}")
        self.logger.info("="*60)
    
    def _get_next_backup_time(self):
        """Calculate next backup time"""
        if self.last_backup_time:
            return self.last_backup_time + timedelta(hours=self.interval_hours)
        return datetime.now()
    
    def _send_notification(self, title, message, success=True):
        """Send system notification (if enabled)"""
        if not ENABLE_NOTIFICATIONS:
            return
        
        try:
            # Try to send desktop notification (macOS/Linux)
            import subprocess
            
            if os.system('which osascript > /dev/null 2>&1') == 0:
                # macOS
                script = f'display notification "{message}" with title "{title}"'
                subprocess.run(['osascript', '-e', script], check=False)
            elif os.system('which notify-send > /dev/null 2>&1') == 0:
                # Linux
                subprocess.run(['notify-send', title, message], check=False)
        except Exception:
            pass  # Silently fail if notifications not available
    
    def perform_backup(self):
        """Perform a backup with error handling and logging"""
        self.logger.info("\n" + "="*60)
        self.logger.info("🚀 Starting Scheduled Backup")
        self.logger.info("="*60)
        
        try:
            # Perform backup
            success = self.backup_manager.backup_database()
            
            if success:
                self.backup_count += 1
                self.last_backup_time = datetime.now()
                self.failed_count = 0  # Reset failed count on success
                
                next_backup = self._get_next_backup_time()
                self.logger.info(f"✅ Backup #{self.backup_count} completed successfully")
                self.logger.info(f"⏰ Next backup scheduled for: {next_backup.strftime('%Y-%m-%d %H:%M:%S')}")
                
                self._send_notification(
                    "Backup Successful",
                    f"Database backup #{self.backup_count} completed",
                    success=True
                )
            else:
                self.failed_count += 1
                self.logger.error(f"❌ Backup failed (Failure #{self.failed_count})")
                
                if self.failed_count >= 3:
                    self.logger.error("⚠️  WARNING: 3 consecutive backup failures!")
                    self._send_notification(
                        "Backup Failed",
                        "Multiple backup failures detected. Check logs.",
                        success=False
                    )
            
            return success
            
        except Exception as e:
            self.failed_count += 1
            self.logger.error(f"❌ Backup error: {e}", exc_info=True)
            
            if self.failed_count >= 3:
                self._send_notification(
                    "Backup Error",
                    f"Critical backup error: {str(e)[:50]}",
                    success=False
                )
            
            return False
    
    def run_initial_backup(self):
        """Run initial backup on startup"""
        self.logger.info("\n🚀 Creating initial backup...")
        self.perform_backup()
    
    def start(self):
        """Start the automatic backup scheduler"""
        self._log_system_info()
        
        # Schedule backups
        schedule.every(self.interval_hours).hours.do(self.perform_backup)
        
        # Run initial backup
        self.run_initial_backup()
        
        self.logger.info("\n⏰ Scheduler running... (Press Ctrl+C to stop)")
        self.logger.info("="*60 + "\n")
        
        # Keep the scheduler running
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self._shutdown()
    
    def _shutdown(self):
        """Graceful shutdown"""
        self.logger.info("\n" + "="*60)
        self.logger.info("🛑 Shutting down backup scheduler...")
        self.logger.info("="*60)
        self.logger.info(f"📊 Total backups created: {self.backup_count}")
        self.logger.info(f"❌ Total failures: {self.failed_count}")
        
        if self.last_backup_time:
            self.logger.info(f"📅 Last backup: {self.last_backup_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.logger.info("👋 Backup scheduler stopped")
        self.logger.info("="*60)


def main():
    """Main entry point"""
    import sys
    
    # Parse command line arguments
    interval_hours = BACKUP_INTERVAL_HOURS
    
    if len(sys.argv) > 1:
        try:
            interval_hours = int(sys.argv[1])
            if interval_hours < 1:
                print("❌ Error: Interval must be at least 1 hour")
                sys.exit(1)
        except ValueError:
            print("❌ Error: Invalid interval. Must be a number.")
            print("\nUsage:")
            print("  python auto_backup.py [interval_hours]")
            print("\nExamples:")
            print("  python auto_backup.py        # Use default (6 hours)")
            print("  python auto_backup.py 3      # Backup every 3 hours")
            print("  python auto_backup.py 12     # Backup every 12 hours")
            sys.exit(1)
    
    # Start scheduler
    scheduler = AutoBackupScheduler(interval_hours=interval_hours)
    scheduler.start()


if __name__ == '__main__':
    main()
