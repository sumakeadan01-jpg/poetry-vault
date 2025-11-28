#!/bin/bash

# Test Tutorial Feature Script
# This script sets up and tests the tutorial feature

echo "======================================"
echo "🧪 Testing Tutorial Feature"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run: python3 -m venv .venv"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Check if database needs fixing
if [ -f "instance/poetry_app.db" ]; then
    echo "📊 Checking database..."
    python3 -c "
import sqlite3
conn = sqlite3.connect('instance/poetry_app.db')
cursor = conn.cursor()
cursor.execute('PRAGMA table_info(users)')
columns = [col[1] for col in cursor.fetchall()]
if 'has_seen_tutorial' not in columns:
    print('⚠️  Database needs migration!')
    print('Run: python3 fix_database.py')
    exit(1)
else:
    print('✅ Database is up to date')
conn.close()
" || {
        echo ""
        echo "🔧 Fixing database..."
        python3 fix_database.py
    }
else
    echo "📊 No database found - will be created on first run"
fi

echo ""
echo "======================================"
echo "🚀 Starting app on port 5001..."
echo "======================================"
echo ""
echo "📍 Visit: http://localhost:5001"
echo "🛑 Press Ctrl+C to stop"
echo ""
echo "✅ Test checklist:"
echo "   1. Register a new account"
echo "   2. Tutorial should appear automatically"
echo "   3. Click through all 3 steps"
echo "   4. Try the Skip button"
echo "   5. Refresh - tutorial should NOT appear again"
echo ""
echo "======================================"
echo ""

# Run the app
python3 run_test.py
