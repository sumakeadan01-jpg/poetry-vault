#!/usr/bin/env python3
"""
Fix Arabic poems by removing modern translations and keeping only authentic classical Arabic text
"""

import re

def fix_arabic_poems():
    # Read the current seed_poems.py
    with open('seed_poems.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace المتنبي poems with authentic classical texts only
    mutanabbi_poems = """    'المتنبي': [
        {
            'title': 'على قدر أهل العزم',
            'category': 'wisdom',
            'content': '''على قدر أهل العزم تأتي العزائم
وتأتي على قدر الكرام المكارم
وتعظم في عين الصغير صغارها
وتصغر في عين العظيم العظائم'''
        },
        {
            'title': 'أعز مكان في الدنى',
            'category': 'wisdom',
            'content': '''أعز مكان في الدنى سرج سابح
وخير جليس في الزمان كتاب
ولم أر في عيوب الناس شيئا
كنقص القادرين على التمام'''
        },
        {
            'title': 'الخيل والليل والبيداء',
            'category': 'pride',
            'content': '''الخيل والليل والبيداء تعرفني
والسيف والرمح والقرطاس والقلم
صحبت في الفلوات الوحش منفردا
حتى تعجب مني القور والأكم'''
        },
        {
            'title': 'واحر قلباه',
            'category': 'longing',
            'content': '''واحر قلباه ممن قلبه شبم
ومن بجسمي وحالي عنده سقم
ما لي أكتم حبا قد برى جسدي
وتدعي حب سيف الدولة الأمم'''
        },
        {
            'title': 'أنا الذي نظر الأعمى',
            'category': 'pride',
            'content': '''أنا الذي نظر الأعمى إلى أدبي
وأسمعت كلماتي من به صمم
أنام ملء جفوني عن شواردها
ويسهر الخلق جراها ويختصم'''
        }
    ],'''

    # Replace قيس بن الملوح poems with authentic classical texts only
    majnun_poems = '''    'قيس بن الملوح': [
        {
            'title': 'أمر على الديار',
            'category': 'love',
            'content': '''أمر على الديار ديار ليلى
أقبل ذا الجدار وذا الجدارا
وما حب الديار شغفن قلبي
ولكن حب من سكن الديارا'''
        },
        {
            'title': 'وأهيم وجدا بليلى',
            'category': 'love',
            'content': '''وأهيم وجدا بليلى وأحبها
وأعلم أني عن ليلى مصروف
وأعلم أن الذي بي من صبابة
إليها سيبقى ما بقيت وأبقى'''
        },
        {
            'title': 'يا ليل الصب',
            'category': 'longing',
            'content': '''يا ليل الصب متى غده
أقيام الساعة موعده
رقد السمار وأرقه
أسف للبين يردده'''
        },
        {
            'title': 'تعلقت ليلى وهي ذات ذوائب',
            'category': 'love',
            'content': '''تعلقت ليلى وهي ذات ذوائب
ولم يبد للأتراب من ثديها حجم
صغيرين نرعى البهم يا ليت أننا
إلى اليوم لم نكبر ولم تكبر البهم'''
        },
        {
            'title': 'أحب النوم في غير أوانه',
            'category': 'longing',
            'content': '''أحب النوم في غير أوانه
لعل لقاء في المنام يكون
وأكره أن أرى الصبح منيرا
لأن الصبح يذهب بالظنون'''
        }
    ]'''

    # Find and replace the Arabic poets sections
    # Pattern to match المتنبي section
    mutanabbi_pattern = r"    'المتنبي': \[.*?\n    \],"
    content = re.sub(mutanabbi_pattern, mutanabbi_poems, content, flags=re.DOTALL)
    
    # Pattern to match قيس بن الملوح section  
    majnun_pattern = r"    'قيس بن الملوح': \[.*?\n    \]"
    content = re.sub(majnun_pattern, majnun_poems, content, flags=re.DOTALL)
    
    # Write the fixed content back
    with open('seed_poems.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed Arabic poems - removed translations, kept only authentic classical texts")

if __name__ == '__main__':
    fix_arabic_poems()