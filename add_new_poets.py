"""
Enhanced Poet Addition Tool
Safely add new classic poets to the database without affecting existing data
"""
from app import create_app
from models import db, User, Poem
from werkzeug.security import generate_password_hash
import sys
import json
from pathlib import Path


# Default poets to add (can be customized)
DEFAULT_POETS = {
    'Pablo Neruda': [
        {
            'title': 'Tonight I Can Write',
            'content': '''Tonight I can write the saddest lines.

Write, for example, 'The night is starry
and the stars are blue and shiver in the distance.'

The night wind revolves in the sky and sings.

Tonight I can write the saddest lines.
I loved her, and sometimes she loved me too.

Through nights like this one I held her in my arms.
I kissed her again and again under the endless sky.

She loved me, sometimes I loved her too.
How could one not have loved her great still eyes.

Tonight I can write the saddest lines.
To think that I do not have her. To feel that I have lost her.

To hear the immense night, still more immense without her.
And the verse falls to the soul like dew to the pasture.

What does it matter that my love could not keep her.
The night is starry and she is not with me.

This is all. In the distance someone is singing. In the distance.
My soul is not satisfied that it has lost her.

My sight tries to find her as though to bring her closer.
My heart looks for her, and she is not with me.

The same night whitening the same trees.
We, of that time, are no longer the same.

I no longer love her, that's certain, but how I loved her.
My voice tried to find the wind to touch her hearing.

Another's. She will be another's. As she was before my kisses.
Her voice, her bright body. Her infinite eyes.

I no longer love her, that's certain, but maybe I love her.
Love is so short, forgetting is so long.

Because through nights like this one I held her in my arms
my soul is not satisfied that it has lost her.

Though this be the last pain that she makes me suffer
and these the last verses that I write for her.''',
            'category': 'love'
        },
        {
            'title': 'If You Forget Me',
            'content': '''I want you to know
one thing.

You know how this is:
if I look
at the crystal moon, at the red branch
of the slow autumn at my window,
if I touch
near the fire
the impalpable ash
or the wrinkled body of the log,
everything carries me to you,
as if everything that exists,
aromas, light, metals,
were little boats
that sail
toward those isles of yours that wait for me.

Well, now,
if little by little you stop loving me
I shall stop loving you little by little.

If suddenly
you forget me
do not look for me,
for I shall already have forgotten you.

If you think it long and mad,
the wind of banners
that passes through my life,
and you decide
to leave me at the shore
of the heart where I have roots,
remember
that on that day,
at that hour,
I shall lift my arms
and my roots will set off
to seek another land.

But
if each day,
each hour,
you feel that you are destined for me
with implacable sweetness,
if each day a flower
climbs up to your lips to seek me,
ah my love, ah my own,
in me all that fire is repeated,
in me nothing is extinguished or forgotten,
my love feeds on your love, beloved,
and as long as you live it will be in your arms
without leaving mine.''',
            'category': 'love'
        }
    ],
    
    'Hafiz': [
        {
            'title': 'The Gift',
            'content': '''All this time
The sun never says to the earth,

"You owe me."

Look what happens with
A love like that.

It lights the whole sky.''',
            'category': 'spirituality'
        },
        {
            'title': 'I Wish I Could Show You',
            'content': '''I wish I could show you,
When you are lonely or in darkness,
The Astonishing Light
Of your own Being!''',
            'category': 'spirituality'
        }
    ],
    
    'Sylvia Plath': [
        {
            'title': 'Mirror',
            'content': '''I am silver and exact. I have no preconceptions.
Whatever I see I swallow immediately
Just as it is, unmisted by love or dislike.
I am not cruel, only truthful‚
The eye of a little god, four-cornered.
Most of the time I meditate on the opposite wall.
It is pink, with speckles. I have looked at it so long
I think it is part of my heart. But it flickers.
Faces and darkness separate us over and over.

Now I am a lake. A woman bends over me,
Searching my reaches for what she really is.
Then she turns to those liars, the candles or the moon.
I see her back, and reflect it faithfully.
She rewards me with tears and an agitation of hands.
I am important to her. She comes and goes.
Each morning it is her face that replaces the darkness.
In me she has drowned a young girl, and in me an old woman
Rises toward her day after day, like a terrible fish.''',
            'category': 'reflection'
        },
        {
            'title': 'Mad Girl\'s Love Song',
            'content': '''I shut my eyes and all the world drops dead;
I lift my lids and all is born again.
(I think I made you up inside my head.)

The stars go waltzing out in blue and red,
And arbitrary blackness gallops in:
I shut my eyes and all the world drops dead.

I dreamed that you bewitched me into bed
And sung me moon-struck, kissed me quite insane.
(I think I made you up inside my head.)

God topples from the sky, hell's fires fade:
Exit seraphim and Satan's men:
I shut my eyes and all the world drops dead.

I fancied you'd return the way you said,
But I grow old and I forget your name.
(I think I made you up inside my head.)

I should have loved a thunderbird instead;
At least when spring comes they roar back again.
I shut my eyes and all the world drops dead.
(I think I made you up inside my head.)''',
            'category': 'love'
        }
    ]
}


class PoetAdder:
    """Manages adding new poets to the database safely"""
    
    def __init__(self):
        self.app = create_app()
    
    def _print_section(self, title):
        """Print formatted section header"""
        print("\n" + "="*70)
        print(f"  {title}")
        print("="*70)
    
    def _validate_poet_data(self, poet_name, poems_list):
        """
        Validate poet data before adding
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not poet_name or not isinstance(poet_name, str):
            return False, "Invalid poet name"
        
        if not poems_list or not isinstance(poems_list, list):
            return False, f"Invalid poems list for {poet_name}"
        
        for i, poem in enumerate(poems_list):
            if not isinstance(poem, dict):
                return False, f"Poem {i+1} for {poet_name} is not a dictionary"
            
            if 'title' not in poem:
                return False, f"Poem {i+1} for {poet_name} missing title"
            
            if 'content' not in poem:
                return False, f"Poem {i+1} for {poet_name} missing content"
            
            if not poem['title'] or not poem['content']:
                return False, f"Poem {i+1} for {poet_name} has empty title or content"
        
        return True, None
    
    def _sanitize_email(self, poet_name):
        """Create a safe email address from poet name"""
        try:
            # Remove special characters and spaces
            safe_name = poet_name.lower()
            safe_name = safe_name.replace(' ', '').replace("'", '').replace('"', '')
            safe_name = ''.join(c for c in safe_name if c.isalnum())
            return f"{safe_name}@poetryvault.com"
        except Exception:
            # Fallback to a generic email
            return f"poet{hash(poet_name)}@poetryvault.com"
    
    def add_poets(self, poets_dict=None, dry_run=False):
        """
        Add new poets to the database
        
        Args:
            poets_dict: Dictionary of poets to add (defaults to DEFAULT_POETS)
            dry_run: If True, validate but don't commit changes
        
        Returns:
            dict: Statistics about the operation
        """
        if poets_dict is None:
            poets_dict = DEFAULT_POETS
        
        self._print_section("📚 ADDING NEW POETS")
        
        if dry_run:
            print("\n  🔍 DRY RUN MODE - No changes will be made\n")
        
        stats = {
            'poets_added': 0,
            'poets_skipped': 0,
            'poems_added': 0,
            'errors': []
        }
        
        try:
            with self.app.app_context():
                for poet_name, poems_list in poets_dict.items():
                    print(f"\n  📖 Processing: {poet_name}")
                    
                    # Validate data
                    is_valid, error_msg = self._validate_poet_data(poet_name, poems_list)
                    if not is_valid:
                        print(f"     ❌ Validation failed: {error_msg}")
                        stats['errors'].append(f"{poet_name}: {error_msg}")
                        stats['poets_skipped'] += 1
                        continue
                    
                    # Check if poet already exists
                    existing_poet = User.query.filter_by(username=poet_name).first()
                    
                    if existing_poet:
                        print(f"     ⚠️  Already exists, skipping...")
                        stats['poets_skipped'] += 1
                        continue
                    
                    if dry_run:
                        print(f"     ✓ Would add poet: {poet_name}")
                        print(f"     ✓ Would add {len(poems_list)} poems")
                        stats['poets_added'] += 1
                        stats['poems_added'] += len(poems_list)
                        continue
                    
                    # Create new poet user
                    try:
                        email = self._sanitize_email(poet_name)
                        poet = User(
                            username=poet_name,
                            email=email,
                            password_hash=generate_password_hash('classic_poet_2024'),
                            age=None,
                            favorite_poet=poet_name,
                            is_admin=False
                        )
                        db.session.add(poet)
                        db.session.flush()  # Get the poet ID
                        
                        stats['poets_added'] += 1
                        print(f"     ✅ Added poet: {poet_name}")
                        
                        # Add their poems
                        for poem_data in poems_list:
                            try:
                                poem = Poem(
                                    title=poem_data['title'],
                                    content=poem_data['content'],
                                    category=poem_data.get('category', 'general'),
                                    user_id=poet.id,
                                    is_classic=True
                                )
                                db.session.add(poem)
                                stats['poems_added'] += 1
                                print(f"        📝 Added: {poem_data['title'][:50]}...")
                            except Exception as e:
                                error_msg = f"Failed to add poem '{poem_data.get('title', 'Unknown')}': {e}"
                                print(f"        ❌ {error_msg}")
                                stats['errors'].append(f"{poet_name}: {error_msg}")
                        
                    except Exception as e:
                        error_msg = f"Failed to add poet: {e}"
                        print(f"     ❌ {error_msg}")
                        stats['errors'].append(f"{poet_name}: {error_msg}")
                        stats['poets_skipped'] += 1
                        db.session.rollback()
                        continue
                
                # Commit all changes
                if not dry_run:
                    db.session.commit()
                    print("\n  💾 Changes committed to database")
                
                # Print summary
                self._print_section("📊 SUMMARY")
                print(f"\n  Poets Added: {stats['poets_added']}")
                print(f"  Poets Skipped: {stats['poets_skipped']}")
                print(f"  Poems Added: {stats['poems_added']}")
                
                if stats['errors']:
                    print(f"\n  ⚠️  Errors ({len(stats['errors'])}):")
                    for error in stats['errors']:
                        print(f"     - {error}")
                
                if not dry_run and stats['poets_added'] > 0:
                    print(f"\n  ✅ All existing data preserved!")
                
                return stats
                
        except Exception as e:
            print(f"\n  ❌ Critical error: {e}")
            if not dry_run:
                db.session.rollback()
            stats['errors'].append(f"Critical: {e}")
            return stats
    
    def load_from_json(self, json_file):
        """Load poets from JSON file"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                poets_dict = json.load(f)
            return poets_dict
        except Exception as e:
            print(f"❌ Error loading JSON file: {e}")
            return None


def main():
    """Main entry point"""
    adder = PoetAdder()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'dry-run':
            adder.add_poets(dry_run=True)
        elif command == 'add':
            adder.add_poets(dry_run=False)
        elif command == 'from-json' and len(sys.argv) > 2:
            poets_dict = adder.load_from_json(sys.argv[2])
            if poets_dict:
                adder.add_poets(poets_dict, dry_run=False)
        else:
            print("Enhanced Poet Addition Tool")
            print("="*70)
            print("\nUsage:")
            print("  python add_new_poets.py [command] [args]")
            print("\nCommands:")
            print("  dry-run              - Validate without making changes")
            print("  add                  - Add poets to database")
            print("  from-json <file>     - Load poets from JSON file")
            print("\nExamples:")
            print("  python add_new_poets.py dry-run")
            print("  python add_new_poets.py add")
            print("  python add_new_poets.py from-json poets.json")
            print("\nJSON Format:")
            print('  {')
            print('    "Poet Name": [')
            print('      {')
            print('        "title": "Poem Title",')
            print('        "content": "Poem content...",')
            print('        "category": "love"')
            print('      }')
            print('    ]')
            print('  }')
    else:
        # Default: add poets
        adder.add_poets(dry_run=False)


if __name__ == '__main__':
    main()
