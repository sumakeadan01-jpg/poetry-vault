"""
Run the app on port 5001 for testing
Usage: python run_test.py
"""

from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("="*60)
    print("🚀 Starting Poetry Vault on port 5001 for testing...")
    print("="*60)
    print("📍 Visit: http://localhost:5001")
    print("🛑 Press Ctrl+C to stop")
    print("="*60)
    app.run(debug=True, port=5001)
