"""
Add new classic poets to the database WITHOUT deleting existing data
Run this script to add more poets while keeping all current users and poems
"""

from app import create_app
from models import db, User, Poem
from werkzeug.security import generate_password_hash

# Add your new poets here
NEW_POETS = {
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

def add_poets():
    """Add new poets without deleting existing data"""
    app = create_app()
    
    with app.app_context():
        added_poets = 0
        added_poems = 0
        
        for poet_name, poems_list in NEW_POETS.items():
            # Check if poet already exists
            existing_poet = User.query.filter_by(username=poet_name).first()
            
            if existing_poet:
                print(f"⚠️  {poet_name} already exists, skipping...")
                continue
            
            # Create new poet user
            poet = User(
                username=poet_name,
                email=f"{poet_name.lower().replace(' ', '').replace("'", '')}@poetryvault.com",
                password_hash=generate_password_hash('classic_poet_2024'),
                age=None,
                favorite_poet=poet_name,
                is_admin=False
            )
            db.session.add(poet)
            db.session.flush()  # Get the poet ID
            
            added_poets += 1
            print(f"✅ Added poet: {poet_name}")
            
            # Add their poems
            for poem_data in poems_list:
                poem = Poem(
                    title=poem_data['title'],
                    content=poem_data['content'],
                    category=poem_data.get('category', 'general'),
                    user_id=poet.id,
                    is_classic=True
                )
                db.session.add(poem)
                added_poems += 1
                print(f"   📝 Added poem: {poem_data['title']}")
        
        # Save all changes
        db.session.commit()
        
        print(f"\n🎉 Success!")
        print(f"   Added {added_poets} new poets")
        print(f"   Added {added_poems} new poems")
        print(f"   All existing data preserved!")

if __name__ == '__main__':
    add_poets()
