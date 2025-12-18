#!/usr/bin/env python3
"""
Fix seed_poems.py to include mood and theme data for deployment
"""

import re

# Category to mood/theme mapping
CATEGORY_MAPPING = {
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
    'growth': {'mood': 'optimistic', 'theme': 'development'},
    'general': {'mood': 'contemplative', 'theme': 'reflection'},
    'decay': {'mood': 'melancholic', 'theme': 'decline'},
    'self': {'mood': 'introspective', 'theme': 'identity'},
    'apocalypse': {'mood': 'ominous', 'theme': 'destruction'},
    'heartbreak': {'mood': 'devastated', 'theme': 'loss'},
    'loss': {'mood': 'sorrowful', 'theme': 'grief'},
    'mortality': {'mood': 'somber', 'theme': 'death'},
    'sleeplessness': {'mood': 'restless', 'theme': 'insomnia'},
    'glory': {'mood': 'triumphant', 'theme': 'achievement'},
    'reproach': {'mood': 'critical', 'theme': 'judgment'},
    'questioning': {'mood': 'curious', 'theme': 'inquiry'},
    'farewell': {'mood': 'bittersweet', 'theme': 'departure'},
    'illness': {'mood': 'weak', 'theme': 'suffering'},
    'wandering': {'mood': 'restless', 'theme': 'journey'},
    'emotion': {'mood': 'intense', 'theme': 'feeling'},
    'message': {'mood': 'communicative', 'theme': 'expression'},
    'mental state': {'mood': 'psychological', 'theme': 'mind'},
    'mind': {'mood': 'intellectual', 'theme': 'thought'},
    'communication': {'mood': 'expressive', 'theme': 'connection'},
    'poetry': {'mood': 'artistic', 'theme': 'creativity'},
    'society': {'mood': 'observant', 'theme': 'culture'},
    'modern life': {'mood': 'contemporary', 'theme': 'progress'},
    'desire': {'mood': 'yearning', 'theme': 'want'},
    'empathy': {'mood': 'compassionate', 'theme': 'understanding'},
    'return': {'mood': 'nostalgic', 'theme': 'homecoming'},
    'language': {'mood': 'expressive', 'theme': 'words'},
    'imagination': {'mood': 'creative', 'theme': 'fantasy'},
    'vision': {'mood': 'prophetic', 'theme': 'foresight'},
    'unfulfilled': {'mood': 'disappointed', 'theme': 'incompletion'},
    'persistence': {'mood': 'determined', 'theme': 'endurance'},
    'declaration': {'mood': 'bold', 'theme': 'statement'},
    'blame': {'mood': 'accusatory', 'theme': 'fault'},
    'heart': {'mood': 'emotional', 'theme': 'core'},
    'remembrance': {'mood': 'nostalgic', 'theme': 'memory'},
    'distance': {'mood': 'longing', 'theme': 'separation'},
    'if only': {'mood': 'wistful', 'theme': 'regret'},
    'everywhere': {'mood': 'omnipresent', 'theme': 'universality'},
    'reason': {'mood': 'logical', 'theme': 'rationality'},
    'conclusion': {'mood': 'final', 'theme': 'ending'},
    'patience': {'mood': 'calm', 'theme': 'waiting'},
    'meeting': {'mood': 'anticipatory', 'theme': 'encounter'}
}

def fix_seed_data():
    """Add mood and theme to all poems in seed_poems.py"""
    
    with open('seed_poems.py', 'r', encoding='utf-8') as f:
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
    with open('seed_poems.py', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✅ Updated seed_poems.py with mood and theme data")
    
    # Count how many poems were updated
    mood_count = updated_content.count("'mood':")
    theme_count = updated_content.count("'theme':")
    
    print(f"📊 Added mood to {mood_count} poems")
    print(f"📊 Added theme to {theme_count} poems")

if __name__ == '__main__':
    fix_seed_data()