"""
Enhanced Test Server
Quick development server for testing with enhanced features
"""
import sys
from pathlib import Path


def check_environment():
    """Check and setup test environment"""
    # Ensure required directories exist
    Path('instance').mkdir(exist_ok=True)
    Path('instance/backups').mkdir(exist_ok=True)
    
    # Check if database exists
    db_path = Path('instance/poetry_app.db')
    if not db_path.exists():
        print("\n⚠️  No database found!")
        print("   Creating new database with auto-seeding...")
        return False
    return True


def print_startup_info(port=5001):
    """Print startup information"""
    print("\n" + "="*70)
    print("  🧪 POETRY VAULT - TEST SERVER")
    print("="*70)
    print(f"\n  📍 Server:")
    print(f"     URL: http://localhost:{port}")
    print(f"\n  🔧 Test Mode:")
    print(f"     Debug:    Enabled")
    print(f"     Reloader: Enabled")
    print(f"     Database: instance/poetry_app.db")
    print(f"\n  💡 Tips:")
    print(f"     - Changes auto-reload")
    print(f"     - Check logs in terminal")
    print(f"     - Database persists between runs")
    print(f"\n  🛑 Stop Server:")
    print(f"     Press Ctrl+C")
    print("\n" + "="*70 + "\n")


def print_database_info():
    """Print database information"""
    try:
        from app import create_app
        from models import User, Poem
        
        app = create_app()
        with app.app_context():
            user_count = User.query.count()
            poem_count = Poem.query.count()
            
            print(f"  📊 Database Status:")
            print(f"     Users: {user_count}")
            print(f"     Poems: {poem_count}")
            
            if user_count == 0:
                print(f"\n  💡 Tip: Register an account to get started!")
            
            print()
    except Exception as e:
        print(f"  ⚠️  Could not read database: {e}\n")


def main():
    """Main entry point"""
    # Parse command line arguments
    port = 5001
    show_db_info = True
    
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith('--port='):
                try:
                    port = int(arg.split('=')[1])
                except ValueError:
                    print(f"❌ Invalid port: {arg}")
                    sys.exit(1)
            elif arg == '--no-db-info':
                show_db_info = False
            elif arg == '--help':
                print("Enhanced Test Server")
                print("="*70)
                print("\nUsage:")
                print("  python run_test.py [options]")
                print("\nOptions:")
                print("  --port=<port>    Port to run on (default: 5001)")
                print("  --no-db-info     Don't show database info")
                print("  --help           Show this help")
                print("\nExamples:")
                print("  python run_test.py")
                print("  python run_test.py --port=5002")
                print("  python run_test.py --no-db-info")
                sys.exit(0)
    
    # Check environment
    db_exists = check_environment()
    
    # Print startup info
    print_startup_info(port)
    
    # Show database info if enabled
    if show_db_info and db_exists:
        print_database_info()
    
    # Import and run Flask app
    try:
        from app import create_app
        
        app = create_app()
        
        # Run with test settings
        app.run(
            host='127.0.0.1',  # Localhost only for testing
            port=port,
            debug=True,
            use_reloader=True,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("  🛑 Test server stopped")
        print("="*70)
        print("\n  📊 Database: instance/poetry_app.db")
        print("  💾 Backups: instance/backups/")
        print("\n  👋 Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
