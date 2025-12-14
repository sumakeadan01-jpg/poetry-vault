#!/usr/bin/env python3
"""
Replace Arabic poems with clean, authentic classical texts
"""

def clean_arabic_poems():
    with open('seed_poems.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the start and end of المتنبي section
    mutanabbi_start = None
    mutanabbi_end = None
    majnun_start = None
    majnun_end = None
    
    for i, line in enumerate(lines):
        if "'المتنبي': [" in line:
            mutanabbi_start = i
        elif "'قيس بن الملوح': [" in line:
            majnun_start = i
            if mutanabbi_start is not None:
                mutanabbi_end = i
        elif line.strip() == '}' and majnun_start is not None and majnun_end is None:
            majnun_end = i + 1
            break
    
    if mutanabbi_start is not None and mutanabbi_end is not None:
        # Replace المتنبي section
        new_mutanabbi = [
            "    'المتنبي': [\n",
            "        {\n",
            "            'title': 'على قدر أهل العزم',\n",
            "            'category': 'wisdom',\n",
            "            'content': '''على قدر أهل العزم تأتي العزائم\n",
            "وتأتي على قدر الكرام المكارم\n",
            "وتعظم في عين الصغير صغارها\n",
            "وتصغر في عين العظيم العظائم'''\n",
            "        },\n",
            "        {\n",
            "            'title': 'أعز مكان في الدنى',\n",
            "            'category': 'wisdom',\n",
            "            'content': '''أعز مكان في الدنى سرج سابح\n",
            "وخير جليس في الزمان كتاب\n",
            "ولم أر في عيوب الناس شيئا\n",
            "كنقص القادرين على التمام'''\n",
            "        },\n",
            "        {\n",
            "            'title': 'الخيل والليل والبيداء',\n",
            "            'category': 'pride',\n",
            "            'content': '''الخيل والليل والبيداء تعرفني\n",
            "والسيف والرمح والقرطاس والقلم\n",
            "صحبت في الفلوات الوحش منفردا\n",
            "حتى تعجب مني القور والأكم'''\n",
            "        },\n",
            "        {\n",
            "            'title': 'واحر قلباه',\n",
            "            'category': 'longing',\n",
            "            'content': '''واحر قلباه ممن قلبه شبم\n",
            "ومن بجسمي وحالي عنده سقم\n",
            "ما لي أكتم حبا قد برى جسدي\n",
            "وتدعي حب سيف الدولة الأمم'''\n",
            "        },\n",
            "        {\n",
            "            'title': 'أنا الذي نظر الأعمى',\n",
            "            'category': 'pride',\n",
            "            'content': '''أنا الذي نظر الأعمى إلى أدبي\n",
            "وأسمعت كلماتي من به صمم\n",
            "أنام ملء جفوني عن شواردها\n",
            "ويسهر الخلق جراها ويختصم'''\n",
            "        }\n",
            "    ],\n"
        ]
        
        lines[mutanabbi_start:mutanabbi_end] = new_mutanabbi
    
    # Update indices after replacement
    for i, line in enumerate(lines):
        if "'قيس بن الملوح': [" in line:
            majnun_start = i
            break
    
    if majnun_start is not None:
        # Find end of majnun section
        for i in range(majnun_start + 1, len(lines)):
            if lines[i].strip() == '}' and i < len(lines) - 1:
                majnun_end = i + 1
                break
        
        if majnun_end is not None:
            # Replace قيس بن الملوح section
            new_majnun = [
                "    'قيس بن الملوح': [\n",
                "        {\n",
                "            'title': 'أمر على الديار',\n",
                "            'category': 'love',\n",
                "            'content': '''أمر على الديار ديار ليلى\n",
                "أقبل ذا الجدار وذا الجدارا\n",
                "وما حب الديار شغفن قلبي\n",
                "ولكن حب من سكن الديارا'''\n",
                "        },\n",
                "        {\n",
                "            'title': 'وأهيم وجدا بليلى',\n",
                "            'category': 'love',\n",
                "            'content': '''وأهيم و��دا بليلى وأحبها\n",
                "وأعلم أني عن ليلى مصروف\n",
                "وأعلم أن الذي بي من صبابة\n",
                "إليها سيبقى ما بقيت وأبقى'''\n",
                "        },\n",
                "        {\n",
                "            'title': 'يا ليل الصب',\n",
                "            'category': 'longing',\n",
                "            'content': '''يا ليل الصب متى غده\n",
                "أقيام الساعة موعده\n",
                "رقد السمار وأرقه\n",
                "أسف للبين يردده'''\n",
                "        },\n",
                "        {\n",
                "            'title': 'تعلقت ليلى وهي ذات ذوائب',\n",
                "            'category': 'love',\n",
                "            'content': '''تعلقت ليلى وهي ذات ذوائب\n",
                "ولم يبد للأتراب من ثديها حجم\n",
                "صغيرين نرعى البهم يا ليت أننا\n",
                "إلى اليوم لم نكبر ولم تكبر البهم'''\n",
                "        },\n",
                "        {\n",
                "            'title': 'أحب النوم في غير أوانه',\n",
                "            'category': 'longing',\n",
                "            'content': '''أحب النوم في غير أوانه\n",
                "لعل لقاء في المنام يكون\n",
                "وأكره أن أرى الصبح منيرا\n",
                "لأن الصبح يذهب بالظنون'''\n",
                "        }\n",
                "    ]\n"
            ]
            
            lines[majnun_start:majnun_end] = new_majnun
    
    # Write back the cleaned file
    with open('seed_poems.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✅ Arabic poems cleaned - removed translations, kept only authentic classical texts")

if __name__ == '__main__':
    clean_arabic_poems()