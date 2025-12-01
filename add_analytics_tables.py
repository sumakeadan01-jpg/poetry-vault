"""
Add analytics tables to database
Run this locally and on Render after deploying
"""

import sqlite3
import os

def add_analytics_tables_sqlite():
    """Add analytics tables to SQLite database"""
    
    db_path = 'instance/poetry_app.db'
    
    if not os.path.exists(db_path):
        print("❌ Database not found at:", db_path)
        return
    
    print(f"📍 Database: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create user_activities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                activity_type VARCHAR(50) NOT NULL,
                description VARCHAR(255),
                ip_address VARCHAR(50),
                user_agent VARCHAR(255),
                referrer VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Create visitors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS visitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname VARCHAR(100),
                source VARCHAR(100),
                ip_address VARCHAR(50),
                user_agent VARCHAR(255),
                referrer VARCHAR(255),
                first_visit TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_visit TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                visit_count INTEGER DEFAULT 1
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Analytics tables created successfully!")
        print("   - user_activities")
        print("   - visitors")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    print("="*60)
    print("🔧 Adding Analytics Tables")
    print("="*60)
    print()
    add_analytics_tables_sqlite()
