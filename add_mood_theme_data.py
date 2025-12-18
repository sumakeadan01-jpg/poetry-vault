#!/usr/bin/env python3
"""
Add mood and theme data to existing poems
"""

import sqlite3
import os

# Mood and theme mappings based on categories
CATEGORY_TO_MOOD_THEME = {
    'love': {'mood': 'romantic', 'theme': 'passion'},
    'longing': {'mood': 'melancholic', 'theme': 'desire'},
    'tears': {'mood': 'sad', 'theme': 'sorrow'},
    'grief': {'mood': 'sorrowful', 'theme': 'loss'},
    'death': {'mood': 'somber', 'theme': 'mortality'},
    'hope': {'mood': 'optimistic', 'theme': 'faith'},
    'joy': {'mood': 'happy', 'theme': 'celebration'},
    'nature': {'mood': 'peaceful', 'theme': 'beauty'},
    'spirituality': {'mood': 'contemplative', 'theme': 'divine'},
    'solitude': {'mood': 'reflective', 'theme': 'isolation'},
    'time': {'mood': 'nostalgic', 'theme': 'passage'},
    'life': {'mood': 'philosophical', 'theme': 'existence'},
    'aging': {'mood': 'melancholic', 'theme': 'mortality'},
    'war': {'mood': 'intense', 'theme': 'conflict'},
    'patriotism': {'mood': 'proud', 'theme': 'loyalty'},
    'friendship': {'mood': 'warm', 'theme': 'companionship'},
    'betrayal': {'mood': 'bitter', 'theme': 'deception'},
    'memory': {'mood': 'nostalgic', 'theme': 'remembrance'},
    'dreams': {'mood': 'mystical', 'theme': 'imagination'},
    'beauty': {'mood': 'admiring', 'theme': 'aesthetics'},
    'wisdom': {'mood': 'thoughtful', 'theme': 'knowledge'},
    'youth': {'mood': 'energetic', 'theme': 'vitality'},
    'winter': {'mood': 'cold', 'theme': 'season'},
    'autumn': {'mood': 'melancholic', 'theme': 'change'},
    'night': {'mood': 'mysterious', 'theme': 'darkness'},
    'journey': {'mood': 'adventurous', 'theme': 'exploration'},
    'power': {'mood': 'confident', 'theme': 'strength'},
    'despair': {'mood': 'hopeless', 'theme': 'darkness'},
    'celebration': {'mood': 'joyful', 'theme': 'festivity'},
    'melancholy': {'mood': 'sad', 'theme': 'sorrow'},
    'reality': {'mood': 'serious', 'theme': 'truth'},
    'wonder': {'mood': 'amazed', 'theme': 'mystery'},
    'quest': {'mood': 'determined', 'theme': 'seeking'},
    'defiance': {'mood': 'rebellious', 'theme': 'resistance'},
    'devotion': {'mood': 'dedicated', 'theme': 'loyalty'},
    'yearning': {'mood': 'longing', 'theme': 'desire'},
    'suffering': {'mood': 'painful', 'theme': 'hardship'},
    'madness': {'mood': 'chaotic', 'theme': 'insanity'},
    'philosophy': {'mood': 'thoughtful', 'theme': 'wisdom'},
    'art': {'mood': 'creative', 'theme': 'expression'},
    'humor': {'mood': 'playful', 'theme': 'comedy'},
    'fear': {'mood': 'anxious', 'theme': 'terror'},
    'pride': {'mood': 'confident', 'theme': 'honor'},
    'compassion': {'mood': 'caring', 'theme': 'empathy'},
    'change': {'mood': 'uncertain', 'theme': 'transformation'},
    'eternal': {'mood': 'timeless', 'theme': 'infinity'},
    'light': {'mood': 'bright', 'theme': 'illumination'},
    'darkness': {'mood': 'dark', 'theme': 'shadow'},
    'freedom': {'mood': 'liberated', 'theme': 'independence'},
    'truth': {'mood': 'honest', 'theme': 'reality'},
    'illusion': {'mood': 'confused', 'theme': 'deception'},
    'peace': {'mood': 'calm', 'theme': 'serenity'},
    'conflict': {'mood': 'tense', 'theme': 'struggle'},
    'healing': {'mood': 'hopeful', 'theme': 'recovery'},
    'growth': {'mood': 'optimistic', 'theme': 'development'}
}

def add_mood_theme_data(db_path='instance/poetry_app.db'):
    """Add mood and theme data to poems based on their categories"""
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get all poems with categories but no mood/theme
        cursor.execute('''
            SELECT id, title, category 
            FROM poems 
            WHERE category IS NOT NULL 
            AND (mood IS NULL OR theme IS NULL)
        ''')
        poems = cursor.fetchall()
        
        updated_count = 0
        
        for poem_id, title, category in poems:
            if category and category.lower() in CATEGORY_TO_MOOD_THEME:
                mapping = CATEGORY_TO_MOOD_THEME[category.lower()]
                mood = mapping['mood']
                theme = mapping['theme']
                
                cursor.execute('''
                    UPDATE poems 
                    SET mood = ?, theme = ? 
                    WHERE id = ?
                ''', (mood, theme, poem_id))
                
                updated_count += 1
                print(f"✅ Updated '{title[:50]}...' - Mood: {mood}, Theme: {theme}")
        
        # Also add some default mood/theme for poems without categories
        cursor.execute('''
            SELECT id, title, content 
            FROM poems 
            WHERE category IS NULL 
            AND (mood IS NULL OR theme IS NULL)
            LIMIT 20
        ''')
        uncategorized = cursor.fetchall()
        
        for poem_id, title, content in uncategorized:
            # Simple content-based mood/theme assignment
            content_lower = content.lower()
            
            if any(word in content_lower for word in ['love', 'heart', 'beloved', 'kiss']):
                mood, theme = 'romantic', 'love'
            elif any(word in content_lower for word in ['death', 'grave', 'die', 'funeral']):
                mood, theme = 'somber', 'mortality'
            elif any(word in content_lower for word in ['nature', 'tree', 'flower', 'bird']):
                mood, theme = 'peaceful', 'nature'
            elif any(word in content_lower for word in ['sad', 'sorrow', 'weep', 'cry']):
                mood, theme = 'melancholic', 'sorrow'
            elif any(word in content_lower for word in ['joy', 'happy', 'laugh', 'smile']):
                mood, theme = 'joyful', 'happiness'
            else:
                mood, theme = 'contemplative', 'reflection'
            
            cursor.execute('''
                UPDATE poems 
                SET mood = ?, theme = ? 
                WHERE id = ?
            ''', (mood, theme, poem_id))
            
            updated_count += 1
            print(f"✅ Auto-assigned '{title[:50]}...' - Mood: {mood}, Theme: {theme}")
        
        conn.commit()
        print(f"\n🎉 Successfully updated {updated_count} poems with mood and theme data!")
        
        # Show summary of available moods and themes
        cursor.execute('SELECT DISTINCT mood FROM poems WHERE mood IS NOT NULL ORDER BY mood')
        moods = [row[0] for row in cursor.fetchall()]
        
        cursor.execute('SELECT DISTINCT theme FROM poems WHERE theme IS NOT NULL ORDER BY theme')
        themes = [row[0] for row in cursor.fetchall()]
        
        print(f"\nAvailable Moods ({len(moods)}): {', '.join(moods)}")
        print(f"Available Themes ({len(themes)}): {', '.join(themes)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating mood/theme data: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    add_mood_theme_data()