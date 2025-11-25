#!/bin/bash

# Start the Poetry App with automatic backups

echo "🚀 Starting Poetry Vault with Auto-Backup..."
echo "=============================================="

# Activate virtual environment
source .venv/bin/activate

# Install schedule if not installed
pip install schedule > /dev/null 2>&1

# Start auto-backup in background
echo "📦 Starting automatic backup system..."
python3 auto_backup.py &
BACKUP_PID=$!

# Wait a moment for backup to initialize
sleep 2

# Start Flask app
echo "🌐 Starting Flask application on port 5001..."
flask run --port 5001 &
FLASK_PID=$!

echo ""
echo "✅ Poetry Vault is running!"
echo "   🌐 App: http://localhost:5001"
echo "   💾 Auto-backup: Every 6 hours"
echo ""
echo "Press Ctrl+C to stop both services"
echo "=============================================="

# Wait for Ctrl+C
trap "echo ''; echo '🛑 Stopping services...'; kill $BACKUP_PID $FLASK_PID; echo '👋 Goodbye!'; exit" INT

# Keep script running
wait
