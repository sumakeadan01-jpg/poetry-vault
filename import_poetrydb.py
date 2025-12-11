"""
Import poems from PoetryDB API
Automatically adds 50+ poems per poet in seconds!

Usage:
    python import_poetrydb.py

Features:
    - Automatic retry logic with exponential backoff
    - Progress tracking and detailed logging
    - Duplicate detection
    - Error handling and validation
    - Batch processing with commit optimization
"""

import requests
import time
import sys
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

# Configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
TIMEOUT = 15  # seconds
BATCH_COMMIT_SIZE = 10  # Commit every N poems

def fetch_with_retry(url, max_retries=MAX_RETRIES, timeout=TIMEOUT):
    """
    Fetch URL with automatic retry logic
    
    Args:
        url: URL to fetch
        max_retries: Maximum number of retry attempts
        timeout: Request timeout in seconds
    
    Returns:
        Response object or None on failure
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                return response
            elif response.status_code == 429:  # Rate limited
                wait_time = RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                print(f"  ⏳ Rate limited. Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                print(f"  ⚠️  HTTP {response.status_code} on attempt {attempt + 1}/{max_retries}")
                if attempt < max_retries - 1:
                    time.sleep(RETRY_DELAY)
        except requests.exceptions.Timeout:
            print(f"  ⏱️  Timeout on attempt {attempt + 1}/{max_retries}")
            if attempt < max_retries - 1:
                time.sleep(RETRY_DELAY)
        except requests.exceptions.ConnectionError:
            print(f"  🔌 Connection error on attempt {attempt + 1}/{max_retries}")
            if attempt < max_retries - 1:
                time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"  ❌ Unexpected error: {str(e)}")
            return None
    
    return None

def validate_poem_data(poem_data):
    """
    Validate poem data from API
    
    Args:
        poem_data: Dictionary with poem data
    
    Returns:
        (is_valid, error_message)
    """
    if not isinstance(poem_data, dict):
        return False, "Invalid data format"
    
    if 'title' not in poem_data or not poem_data['title']:
        return False, "Missing title"
    
    if 'lines' not in poem_data or not poem_data['lines']:
        return False, "Missing content"
    
    if not isinstance(poem_data['lines'], list):
        return False, "Invalid content format"
    
    return True, "Valid"

def import_from_poetrydb(our_poet_name, api_poet_name, max_poems=50):
    """
    Import poems from PoetryDB API with retry logic and validation
    
    Args:
        our_poet_name: Name in our database
        api_poet_name: Name in PoetryDB
        max_poems: Maximum number of poems to import
    
    Returns:
        Number of poems successfully added
    """
    app = create_app()
    
    with app.app_context():
        # Find poet in database
        poet = User.query.filter_by(username=our_poet_name).first()
        if not poet:
            print(f"❌ Poet '{our_poet_name}' not found in database!")
            return 0
        
        # Fetch from API with retry logic
        print(f"🔍 Fetching poems for {our_poet_name}...")
        url = f"https://poetrydb.org/author/{api_poet_name}"
        
        response = fetch_with_retry(url)
        if not response:
            print(f"❌ Failed to fetch data after {MAX_RETRIES} attempts")
            return 0
        
        try:
            poems_data = response.json()
        except ValueError as e:
            print(f"❌ Invalid JSON response: {str(e)}")
            return 0
        
        # Check for error response
        if isinstance(poems_data, dict) and 'status' in poems_data:
            print(f"❌ No poems found for {our_poet_name}")
            return 0
        
        if not isinstance(poems_data, list):
            print(f"❌ Unexpected response format")
            return 0
        
        added = 0
        skipped = 0
        errors = 0
        
        print(f"📚 Processing {min(len(poems_data), max_poems)} poems...")
        
        for i, poem_data in enumerate(poems_data[:max_poems], 1):
            # Validate poem data
            is_valid, error_msg = validate_poem_data(poem_data)
            if not is_valid:
                print(f"  ⚠️  Skipping invalid poem #{i}: {error_msg}")
                errors += 1
                continue
            
            try:
                # Check if already exists
                existing = Poem.query.filter_by(
                    title=poem_data['title'],
                    user_id=poet.id
                ).first()
                
                if existing:
                    skipped += 1
                    continue
                
                # Create poem
                content = '\n'.join(poem_data['lines'])
                
                # Validate using model validators
                title_valid, title_msg = Poem.validate_title(poem_data['title'])
                content_valid, content_msg = Poem.validate_content(content)
                
                if not title_valid:
                    print(f"  ⚠️  Invalid title: {title_msg}")
                    errors += 1
                    continue
                
                if not content_valid:
                    print(f"  ⚠️  Invalid content: {content_msg}")
                    errors += 1
                    continue
                
                poem = Poem(
                    title=poem_data['title'][:200],  # Truncate if needed
                    content=content[:50000],  # Truncate if needed
                    user_id=poet.id,
                    is_classic=True,
                    category='general'
                )
                db.session.add(poem)
                added += 1
                
                # Progress indicator
                if i % 10 == 0:
                    print(f"  📝 Progress: {i}/{min(len(poems_data), max_poems)} processed...")
                
                # Batch commit for performance
                if added % BATCH_COMMIT_SIZE == 0:
                    try:
                        db.session.commit()
                    except Exception as e:
                        print(f"  ❌ Commit error: {str(e)}")
                        db.session.rollback()
                        errors += 1
                
            except Exception as e:
                print(f"  ❌ Error processing poem #{i}: {str(e)}")
                errors += 1
                continue
        
        # Final commit
        try:
            db.session.commit()
        except Exception as e:
            print(f"❌ Final commit error: {str(e)}")
            db.session.rollback()
        
        print(f"\n🎉 Complete for {our_poet_name}!")
        print(f"   ✅ Added: {added} poems")
        print(f"   ⏭️  Skipped: {skipped} (already exist)")
        if errors > 0:
            print(f"   ⚠️  Errors: {errors}")
        
        return added

def import_all_poets():
    """Import poems for all available poets with progress tracking"""
    print("="*60)
    print("🚀 POETRYDB BULK IMPORT")
    print("="*60)
    print(f"📊 Poets to process: {len(POET_NAME_MAPPING)}")
    print()
    
    total_added = 0
    total_skipped = 0
    failed_poets = []
    start_time = time.time()
    
    for idx, (our_name, api_name) in enumerate(POET_NAME_MAPPING.items(), 1):
        print(f"[{idx}/{len(POET_NAME_MAPPING)}] Processing {our_name}...")
        
        try:
            added = import_from_poetrydb(our_name, api_name, max_poems=50)
            total_added += added
            
            if added == 0:
                failed_poets.append(our_name)
        except Exception as e:
            print(f"❌ Fatal error for {our_name}: {str(e)}")
            failed_poets.append(our_name)
        
        print("\n" + "-"*60 + "\n")
        
        # Small delay between poets to be nice to the API
        if idx < len(POET_NAME_MAPPING):
            time.sleep(1)
    
    elapsed_time = time.time() - start_time
    
    print("="*60)
    print("🎉 IMPORT COMPLETE!")
    print("="*60)
    print(f"✅ Total poems added: {total_added}")
    print(f"⏱️  Time elapsed: {elapsed_time:.1f} seconds")
    
    if failed_poets:
        print(f"\n⚠️  Failed poets ({len(failed_poets)}):")
        for poet in failed_poets:
            print(f"   - {poet}")
    
    print("="*60)

if __name__ == '__main__':
    try:
        import_all_poets()
    except KeyboardInterrupt:
        print("\n\n⚠️  Import interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")
        sys.exit(1)
