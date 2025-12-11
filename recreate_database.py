"""
Enhanced Database Recreation Tool
Safely recreates database with automatic backup and optional data preservation
"""
from app import create_app
from models import db, User, Poem
from backup_db import BackupManager
import sys
from pathlib import Path


class DatabaseRecreator:
    """Manages safe database recreation with backup and restore options"""
    
    def __init__(self):
        self.app = create_app()
        self.backup_manager = BackupManager()
        self.db_path = Path('instance/poetry_app.db')
    
    def _print_section(self, title):
        """Print formatted section header"""
        print("\n" + "="*70)
        print(f"  {title}")
        print("="*70)
    
    def check_database_exists(self):
        """Check if database exists and get stats"""
        if not self.db_path.exists():
            return False, {}
        
        try:
            with self.app.app_context():
                stats = {
                    'users': User.query.count(),
                    'poems': Poem.query.count()
                }
                return True, stats
        except Exception:
            return True, {}
    
    def recreate_fresh(self):
        """Recreate database from scratch (no data preservation)"""
        self._print_section("🔄 RECREATING DATABASE (FRESH START)")
        
        exists, stats = self.check_database_exists()
        
        if exists:
            print(f"\n  Current database found:")
            if stats:
                print(f"     Users: {stats.get('users', 0)}")
                print(f"     Poems: {stats.get('poems', 0)}")
            
            # Create backup first
            print(f"\n  📦 Creating safety backup...")
            self.backup_manager.backup_database()
        
        with self.app.app_context():
            # Drop all tables
            print(f"\n  🗑️  Dropping all tables...")
            db.drop_all()
            
            # Create all tables with new schema
            print(f"  🔨 Creating tables with new schema...")
            db.create_all()
            
            print(f"\n  ✅ Database recreated successfully!")
            print(f"\n  📝 Next steps:")
            print(f"     1. Run: python seed_poems.py (to add classic poems)")
            print(f"     2. Register a new account")
            print(f"     3. Or restore from backup if needed")
    
    def recreate_with_seed(self):
        """Recreate database and auto-seed with classic poems"""
        self._print_section("🔄 RECREATING DATABASE (WITH CLASSIC POEMS)")
        
        exists, stats = self.check_database_exists()
        
        if exists:
            print(f"\n  Current database found:")
            if stats:
                print(f"     Users: {stats.get('users', 0)}")
                print(f"     Poems: {stats.get('poems', 0)}")
            
            # Create backup first
            print(f"\n  📦 Creating safety backup...")
            self.backup_manager.backup_database()
        
        with self.app.app_context():
            # Drop all tables
            print(f"\n  🗑️  Dropping all tables...")
            db.drop_all()
            
            # Create all tables
            print(f"  🔨 Creating tables...")
            db.create_all()
            
            # Auto-seed with classic poems
            print(f"\n  📚 Seeding classic poems...")
            try:
                from seed_poems import FAMOUS_POEMS
                from werkzeug.security import generate_password_hash
                
                poem_count = 0
                for poet_name, poems in FAMOUS_POEMS.items():
                    # Create poet user
                    poet_user = User.query.filter_by(username=poet_name).first()
                    
                    if not poet_user:
                        poet_user = User(
                            username=poet_name,
                            email=f'{poet_name.lower().replace(" ", "")}@poetryvault.com',
                            password_hash=generate_password_hash('classic_poet_2024'),
                            age=None,
                            favorite_poet=poet_name,
                            is_admin=False
                        )
                        db.session.add(poet_user)
                        db.session.flush()
                    
                    # Add poems
                    for poem_data in poems:
                        poem = Poem(
                            title=poem_data['title'],
                            content=poem_data['content'],
                            category=poem_data.get('category', 'general'),
                            user_id=poet_user.id,
                            is_classic=True
                        )
                        db.session.add(poem)
                        poem_count += 1
                
                db.session.commit()
                print(f"  ✅ Added {poem_count} classic poems")
                
            except Exception as e:
                print(f"  ⚠️  Could not seed poems: {e}")
                print(f"     You can run 'python seed_poems.py' manually")
            
            print(f"\n  ✅ Database recreated and seeded successfully!")
            print(f"\n  📝 Next steps:")
            print(f"     1. Register your account")
            print(f"     2. Start using the app!")
    
    def interactive_recreate(self):
        """Interactive recreation with user choices"""
        self._print_section("🔄 DATABASE RECREATION TOOL")
        
        exists, stats = self.check_database_exists()
        
        if exists:
            print(f"\n  ⚠️  WARNING: Current database will be replaced!")
            if stats:
                print(f"\n  Current database contains:")
                print(f"     Users: {stats.get('users', 0)}")
                print(f"     Poems: {stats.get('poems', 0)}")
                print(f"\n  A backup will be created automatically.")
        else:
            print(f"\n  No existing database found.")
            print(f"  A new database will be created.")
        
        print(f"\n  Options:")
        print(f"     1. Fresh start (empty database)")
        print(f"     2. With classic poems (recommended)")
        print(f"     0. Cancel")
        
        choice = input(f"\n  Select option: ").strip()
        
        if choice == '1':
            confirm = input(f"\n  Type 'YES' to confirm: ").strip()
            if confirm == 'YES':
                self.recreate_fresh()
            else:
                print(f"\n  Cancelled.")
        elif choice == '2':
            confirm = input(f"\n  Type 'YES' to confirm: ").strip()
            if confirm == 'YES':
                self.recreate_with_seed()
            else:
                print(f"\n  Cancelled.")
        else:
            print(f"\n  Cancelled.")


def main():
    """Main entry point"""
    recreator = DatabaseRecreator()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'fresh':
            print("\n⚠️  This will recreate the database (fresh start)")
            confirm = input("Type 'YES' to confirm: ").strip()
            if confirm == 'YES':
                recreator.recreate_fresh()
            else:
                print("Cancelled.")
        elif command == 'seed':
            print("\n⚠️  This will recreate the database (with classic poems)")
            confirm = input("Type 'YES' to confirm: ").strip()
            if confirm == 'YES':
                recreator.recreate_with_seed()
            else:
                print("Cancelled.")
        else:
            print("Enhanced Database Recreation Tool")
            print("="*70)
            print("\nUsage:")
            print("  python recreate_database.py [command]")
            print("\nCommands:")
            print("  fresh       - Recreate empty database")
            print("  seed        - Recreate with classic poems (recommended)")
            print("  (no args)   - Interactive mode")
            print("\nExamples:")
            print("  python recreate_database.py")
            print("  python recreate_database.py seed")
    else:
        # Interactive mode
        recreator.interactive_recreate()


if __name__ == '__main__':
    main()
