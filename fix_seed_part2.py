#!/usr/bin/env python3
"""
Fix seed_poems_part2.py to include mood and theme data
"""

import re

# Category to mood/theme mapping
CATEGORY_MAPPING = {
    'love': {'mood': 'romantic', 'theme': 'passion'},
    'longing': {'mood': 'melancholic', 'theme': 'desire'},
    'tears': {'mood': 'sad', 'theme': 'sorrow'},
    'grief': {'mood': 'sorrowful', 'theme': 'loss'},
    'mental state': {'mood': 'psychological', 'theme': 'mind'},
}

def fix_seed_part2():
    """Add mood and theme to all poems in seed_poems_part2.py"""
    
    with open('seed_poems_part2.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match poem dictionaries
    poem_pattern = r"(\s+{\s*\n\s*'title':[^}]+?'category':\s*'([^']+)'[^}]+?})"
    
    def add_mood_theme(match):
        poem_dict = match.group(1)
        category = match.group(2)
        
        # Skip if already has mood/theme
        if "'mood':" in poem_dict or "'theme':" in poem_dict:
            return poem_dict
        
        # Get mood/theme for category
        mapping = CATEGORY_MAPPING.get(category, {'mood': 'contemplative', 'theme': 'reflection'})
        mood = mapping['mood']
        theme = mapping['theme']
        
        # Insert mood and theme after category
        updated = poem_dict.replace(
            f"'category': '{category}'",
            f"'category': '{category}',\n            'mood': '{mood}',\n            'theme': '{theme}'"
        )
        
        return updated
    
    # Apply the transformation
    updated_content = re.sub(poem_pattern, add_mood_theme, content, flags=re.DOTALL)
    
    # Write back to file
    with open('seed_poems_part2.py', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✅ Updated seed_poems_part2.py with mood and theme data")
    
    # Count how many poems were updated
    mood_count = updated_content.count("'mood':")
    theme_count = updated_content.count("'theme':")
    
    print(f"📊 Added mood to {mood_count} poems")
    print(f"📊 Added theme to {theme_count} poems")

if __name__ == '__main__':
    fix_seed_part2()