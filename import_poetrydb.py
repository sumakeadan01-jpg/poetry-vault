"""
Import poems from PoetryDB API
Automatically adds 50+ poems per poet in seconds!

Usage:
    python import_poetrydb.py
"""

import requests
from app import create_app
from models import db, User, Poem

# Map our poet names to PoetryDB names
POET_NAME_MAPPING = {
    'Shakespeare': 'William Shakespeare',
    'William Wordsworth': 'William Wordsworth',
    'John Keats': 'John Keats',
    'Percy Shelley': 'Percy Bysshe Shelley',
    'Lord Byron': 'George Gordon Byron',
    'Robert Burns': 'Robert Burns',
    'Robert Frost': 'Robert Frost',
    'Edgar Allan Poe': 'Edgar Allan Poe',
    'Walt Whitman': 'Walt Whitman',
    'Emily Dickinson': 'Emily Dickinson'
}

def import_from_poetrydb(our_poet_name, api_poet_name, max_poems=50):
    """
    Import poems from PoetryDB API
    
    Args:
        our_poet_name: Name in our database
        api_poet_name: Name in PoetryDB
        max_poems: Maximum number of poems to import
    """
    app = create_app()
    
    with app.app_context():
        # Find poet in database
        poet = User.query.filter_by(username=our_poet_name).first()
        if not poet:
            print(f"❌ Poet '{our_poet_name}' not found in database!")
            return 0
        
        # Fetch from API
        print(f"🔍 Fetching poems for {our_poet_name}...")
        url = f"https://poetrydb.org/author/{api_poet_name}"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                print(f"❌ API error: {response.status_code}")
                return 0
            
            poems_data = response.json()
            
            # Check for error response
            if isinstance(poems_data, dict) and 'status' in poems_data:
                print(f"❌ No poems found for {our_poet_name}")
                return 0
            
            added = 0
            skipped = 0
            
            for poem_data in poems_data[:max_poems]:
                # Check if already exists
                existing = Poem.query.filter_by(
                    title=poem_data['title'],
                    user_id=poet.id
                ).first()
                
                if existing:
                    skipped += 1
                    continue
                
                # Create poem
                poem = Poem(
                    title=poem_data['title'],
                    content='\n'.join(poem_data['lines']),
                    user_id=poet.id,
                    is_classic=True,
                    category='general'
                )
                db.session.add(poem)
                added += 1
                print(f"  ✅ {poem_data['title'][:60]}...")
            
            db.session.commit()
            print(f"\n🎉 Success for {our_poet_name}!")
            print(f"   Added: {added} poems")
            print(f"   Skipped: {skipped} (already exist)")
            return added
            
        except requests.exceptions.Timeout:
            print(f"❌ Timeout connecting to API")
            return 0
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return 0

def import_all_poets():
    """Import poems for all available poets"""
    print("="*60)
    print("🚀 POETRYDB BULK IMPORT")
    print("="*60)
    print()
    
    total_added = 0
    
    for our_name, api_name in POET_NAME_MAPPING.items():
        added = import_from_poetrydb(our_name, api_name, max_poems=50)
        total_added += added
        print("\n" + "-"*60 + "\n")
    
    print("="*60)
    print(f"🎉 COMPLETE! Total poems added: {total_added}")
    print("="*60)

if __name__ == '__main__':
    import_all_poets()
