#!/usr/bin/env python3
"""
Test script to verify all imports work correctly for Render deployment
"""

def test_imports():
    print("Testing Poetry Vault imports...")
    
    try:
        from seed_poems import FAMOUS_POEMS
        print(f"✅ seed_poems.py: {len(FAMOUS_POEMS)} poets loaded")
    except Exception as e:
        print(f"❌ seed_poems.py failed: {e}")
        return False
    
    try:
        from seed_poems_part2 import ADDITIONAL_FAMOUS_POEMS
        print(f"✅ seed_poems_part2.py: {len(ADDITIONAL_FAMOUS_POEMS)} poets loaded")
    except Exception as e:
        print(f"❌ seed_poems_part2.py failed: {e}")
        return False
    
    try:
        from app import create_app
        app = create_app()
        print("✅ Flask app creation successful")
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return False
    
    try:
        from models import User, Poem, Comment
        print("✅ Database models imported successfully")
    except Exception as e:
        print(f"❌ Database models failed: {e}")
        return False
    
    print("\n🎉 All imports successful! Ready for Render deployment.")
    return True

if __name__ == "__main__":
    test_imports()