"""
Import poems from seed_poems_part2.py
Adds 30+ poems for Emily Dickinson and قيس بن الملوح (Majnun Layla)

Usage:
    python import_part2.py
"""

from app import create_app
from models import db, User, Poem
from seed_poems_part2 import ADDITIONAL_FAMOUS_POEMS

def import_part2_poems():
    """Import all poems from seed_poems_part2.py"""
    app = create_app()
    
    print("="*60)
    print("🚀 IMPORTING ADDITIONAL POEMS")
    print("="*60)
    print()
    print("📝 Adding:")
    print("   - Emily Dickinson: 33 new poems")
    print("   - قيس بن الملوح (Majnun Layla): 30 new poems")
    print()
    
    with app.app_context():
        total_added = 0
        
        for poet_name, poems_list in ADDITIONAL_FAMOUS_POEMS.items():
            print(f"📚 Processing {poet_name}...")
            
            # Find poet in database
            poet = User.query.filter_by(username=poet_name).first()
            
            if not poet:
                print(f"  ❌ Poet not found in database!")
                print(f"  💡 Make sure the poet exists in your database first")
                continue
            
            added = 0
            skipped = 0
            
            for poem_data in poems_list:
                # Check if poem already exists
                existing = Poem.query.filter_by(
                    title=poem_data['title'],
                    user_id=poet.id
                ).first()
                
                if existing:
                    skipped += 1
                    continue
                
                # Create new poem
                poem = Poem(
                    title=poem_data['title'],
                    content=poem_data['content'],
                    category=poem_data.get('category', 'general'),
                    user_id=poet.id,
                    is_classic=True
                )
                db.session.add(poem)
                added += 1
                
                # Show progress every 5 poems
                if added % 5 == 0:
                    print(f"  ✅ Added {added} poems so far...")
            
            # Save to database
            db.session.commit()
            
            print(f"\n  🎉 {poet_name}: Added {added} new poems, Skipped {skipped} (already exist)")
            print()
            
            total_added += added
        
        print("="*60)
        print(f"🎉 COMPLETE! Total poems added: {total_added}")
        print()
        print("📊 New Totals:")
        print("   Emily Dickinson: 11 → 44 poems")
        print("   قيس بن الملوح: 19 → 49 poems")
        print("="*60)

if __name__ == '__main__':
    import_part2_poems()
