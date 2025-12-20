"""
Seed the database with famous poems from classic poets
This file contains the FAMOUS_POEMS dictionary used by app.py for auto-seeding
"""

# Famous poems database
FAMOUS_POEMS = {
    'Shakespeare': [
        {
            'title': 'Test Sonnet',
            'content': 'Test content'
        }
    ],
    'Langston Hughes': [
        {
            'title': 'Dreams',
            'content': '''Hold fast to dreams
For if dreams die
Life is a broken-winged bird
That cannot fly.'''
        },
        {
            'title': 'Montage of a Dream Deferred',
            'content': '''Good morning, daddy!
Ain't you heard
The boogie-woogie rumble
Of a dream deferred?
Listen closely:
You'll hear their feet
Beating out and beating out a—
You think
It's a happy beat?'''
        }
    ],
    'Al-Mutanabbi': [
        {
            'title': 'Test Arabic Poem',
            'content': 'Test Arabic content'
        }
    ]
}