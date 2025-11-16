"""
Seed the database with famous poems from classic poets
Run this script once to populate your Poetry Vault with classic works
"""

from app import create_app
from models import db, User, Poem
from werkzeug.security import generate_password_hash

app = create_app()

# Famous poems database
FAMOUS_POEMS = {
    'Shakespeare': [
        {
            'title': 'Sonnet 29: When in Disgrace with Fortune',
            'content': '''When, in disgrace with fortune and men's eyes,
I all alone beweep my outcast state,
And trouble deaf heaven with my bootless cries,
And look upon myself and curse my fate,
Wishing me like to one more rich in hope,
Featured like him, like him with friends possessed,
Desiring this man's art and that man's scope,
With what I most enjoy contented least;
Yet in these thoughts myself almost despising,
Haply I think on thee, and then my state,
(Like to the lark at break of day arising
From sullen earth) sings hymns at heaven's gate;
For thy sweet love remembered such wealth brings
That then I scorn to change my state with kings.'''
        },
        {
            'title': 'Sonnet 130: My Mistress\' Eyes',
            'content': '''My mistress' eyes are nothing like the sun;
Coral is far more red than her lips' red;
If snow be white, why then her breasts are dun;
If hairs be wires, black wires grow on her head.
I have seen roses damasked, red and white,
But no such roses see I in her cheeks;
And in some perfumes is there more delight
Than in the breath that from my mistress reeks.
I love to hear her speak, yet well I know
That music hath a far more pleasing sound;
I grant I never saw a goddess go;
My mistress, when she walks, treads on the ground.
And yet, by heaven, I think my love as rare
As any she belied with false compare.'''
        },
        {
            'title': 'Sonnet 73: That Time of Year',
            'content': '''That time of year thou mayst in me behold
When yellow leaves, or none, or few, do hang
Upon those boughs which shake against the cold,
Bare ruined choirs, where late the sweet birds sang.
In me thou see'st the twilight of such day
As after sunset fadeth in the west,
Which by and by black night doth take away,
Death's second self, that seals up all in rest.
In me thou see'st the glowing of such fire
That on the ashes of his youth doth lie,
As the death-bed whereon it must expire,
Consumed with that which it was nourished by.
This thou perceiv'st, which makes thy love more strong,
To love that well which thou must leave ere long.'''
        },
        {
            'title': 'Sonnet 18: Shall I Compare Thee to a Summer\'s Day?',
            'content': '''Shall I compare thee to a summer's day?
Thou art more lovely and more temperate:
Rough winds do shake the darling buds of May,
And summer's lease hath all too short a date;
Sometime too hot the eye of heaven shines,
And often is his gold complexion dimm'd;
And every fair from fair sometime declines,
By chance or nature's changing course untrimm'd;
But thy eternal summer shall not fade,
Nor lose possession of that fair thou ow'st;
Nor shall death brag thou wander'st in his shade,
When in eternal lines to time thou grow'st:
So long as men can breathe or eyes can see,
So long lives this, and this gives life to thee.'''
        },
        {
            'title': 'Sonnet 116: Let Me Not to the Marriage of True Minds',
            'content': '''Let me not to the marriage of true minds
Admit impediments. Love is not love
Which alters when it alteration finds,
Or bends with the remover to remove.
O no! it is an ever-fixed mark
That looks on tempests and is never shaken;
It is the star to every wand'ring bark,
Whose worth's unknown, although his height be taken.
Love's not Time's fool, though rosy lips and cheeks
Within his bending sickle's compass come;
Love alters not with his brief hours and weeks,
But bears it out even to the edge of doom.
If this be error and upon me prov'd,
I never writ, nor no man ever lov'd.'''
        },
        {
            'title': 'All the World\'s a Stage',
            'content': '''All the world's a stage,
And all the men and women merely players;
They have their exits and their entrances,
And one man in his time plays many parts,
His acts being seven ages. At first, the infant,
Mewling and puking in the nurse's arms.
Then the whining schoolboy, with his satchel
And shining morning face, creeping like snail
Unwillingly to school. And then the lover,
Sighing like furnace, with a woeful ballad
Made to his mistress' eyebrow. Then a soldier,
Full of strange oaths and bearded like the pard,
Jealous in honor, sudden and quick in quarrel,
Seeking the bubble reputation
Even in the cannon's mouth.'''
        }
    ],
    'Rumi': [
        {
            'title': 'The Reed Flute\'s Song',
            'content': '''Listen to the story told by the reed,
of being separated.
"Since I was cut from the reedbed,
I have made this crying sound.
Anyone apart from someone he loves
understands what I say.
Anyone pulled from a source
longs to go back.
At any gathering I am there,
mingling in the laughing and grieving,
a friend to each, but few
will hear the secrets hidden
within the notes. No ears for that.
Body flowing out of spirit,
spirit up from body: no concealing
that mixing. But it's not given us
to see the soul. The reed flute
is fire, not wind. Be that empty."'''
        },
        {
            'title': 'Only Breath',
            'content': '''Not Christian or Jew or Muslim, not Hindu,
Buddhist, sufi, or zen. Not any religion
or cultural system. I am not from the East
or the West, not out of the ocean or up
from the ground, not natural or ethereal, not
composed of elements at all. I do not exist,
am not an entity in this world or the next,
did not descend from Adam or Eve or any
origin story. My place is placeless, a trace
of the traceless. Neither body or soul.
I belong to the beloved, have seen the two
worlds as one and that one call to and know,
first, last, outer, inner, only that
breath breathing human being.'''
        },
        {
            'title': 'The Guest House',
            'content': '''This being human is a guest house.
Every morning a new arrival.
A joy, a depression, a meanness,
some momentary awareness comes
as an unexpected visitor.
Welcome and entertain them all!
Even if they're a crowd of sorrows,
who violently sweep your house
empty of its furniture,
still, treat each guest honorably.
He may be clearing you out
for some new delight.
The dark thought, the shame, the malice,
meet them at the door laughing,
and invite them in.
Be grateful for whoever comes,
because each has been sent
as a guide from beyond.'''
        },
        {
            'title': 'Love Dogs',
            'content': '''One night a man was crying,
Allah! Allah!
His lips grew sweet with the praising,
until a cynic said,
"So! I have heard you calling out, but have you ever
gotten any response?"
The man had no answer to that.
He quit praying and fell into a confused sleep.
He dreamed he saw Khidr, the guide of souls,
in a thick, green foliage.
"Why did you stop praising?"
"Because I've never heard anything back."
"This longing you express is the return message."'''
        },
        {
            'title': 'The Breeze at Dawn',
            'content': '''The breeze at dawn has secrets to tell you.
Don't go back to sleep.
You must ask for what you really want.
Don't go back to sleep.
People are going back and forth across the doorsill
where the two worlds touch.
The door is round and open.
Don't go back to sleep.'''
        }
    ],
    'Emily Dickinson': [
        {
            'title': 'Wild Nights - Wild Nights!',
            'content': '''Wild nights - Wild nights!
Were I with thee
Wild nights should be
Our luxury!
Futile - the winds -
To a Heart in port -
Done with the Compass -
Done with the Chart!
Rowing in Eden -
Ah - the Sea!
Might I but moor - tonight -
In thee!'''
        },
        {
            'title': 'Tell All the Truth but Tell It Slant',
            'content': '''Tell all the truth but tell it slant —
Success in Circuit lies
Too bright for our infirm Delight
The Truth's superb surprise
As Lightning to the Children eased
With explanation kind
The Truth must dazzle gradually
Or every man be blind —'''
        },
        {
            'title': 'The Soul Selects Her Own Society',
            'content': '''The Soul selects her own Society —
Then — shuts the Door —
To her divine Majority —
Present no more —
Unmoved — she notes the Chariots — pausing —
At her low Gate —
Unmoved — an Emperor be kneeling
Upon her Mat —
I've known her — from an ample nation —
Choose One —
Then — close the Valves of her attention —
Like Stone —'''
        },
        {
            'title': 'Hope is the Thing with Feathers',
            'content': '''Hope is the thing with feathers
That perches in the soul,
And sings the tune without the words,
And never stops at all,
And sweetest in the gale is heard;
And sore must be the storm
That could abash the little bird
That kept so many warm.
I've heard it in the chillest land,
And on the strangest sea;
Yet, never, in extremity,
It asked a crumb of me.'''
        },
        {
            'title': 'Because I Could Not Stop for Death',
            'content': '''Because I could not stop for Death –
He kindly stopped for me –
The Carriage held but just Ourselves –
And Immortality.
We slowly drove – He knew no haste
And I had put away
My labor and my leisure too,
For His Civility –
We passed the School, where Children strove
At Recess – in the Ring –
We passed the Fields of Gazing Grain –
We passed the Setting Sun –
Or rather – He passed Us –
The Dews drew quivering and Chill –
For only Gossamer, my Gown –
My Tippet – only Tulle –'''
        },
        {
            'title': 'I\'m Nobody! Who Are You?',
            'content': '''I'm Nobody! Who are you?
Are you – Nobody – too?
Then there's a pair of us!
Don't tell! they'd advertise – you know!
How dreary – to be – Somebody!
How public – like a Frog –
To tell one's name – the livelong June –
To an admiring Bog!'''
        }
    ],
    'Edgar Allan Poe': [
        {
            'title': 'Alone',
            'content': '''From childhood's hour I have not been
As others were—I have not seen
As others saw—I could not bring
My passions from a common spring—
From the same source I have not taken
My sorrow—I could not awaken
My heart to joy at the same tone—
And all I lov'd—I lov'd alone—
Then—in my childhood—in the dawn
Of a most stormy life—was drawn
From ev'ry depth of good and ill
The mystery which binds me still—
From the torrent, or the fountain—
From the red cliff of the mountain—
From the sun that 'round me roll'd
In its autumn tint of gold—
From the lightning in the sky
As it pass'd me flying by—
From the thunder, and the storm—
And the cloud that took the form
(When the rest of Heaven was blue)
Of a demon in my view—'''
        },
        {
            'title': 'Eldorado',
            'content': '''Gaily bedight,
A gallant knight,
In sunshine and in shadow,
Had journeyed long,
Singing a song,
In search of Eldorado.
But he grew old—
This knight so bold—
And o'er his heart a shadow—
Fell as he found
No spot of ground
That looked like Eldorado.
And, as his strength
Failed him at length,
He met a pilgrim shadow—
'Shadow,' said he,
'Where can it be—
This land of Eldorado?'
'Over the Mountains
Of the Moon,
Down the Valley of the Shadow,
Ride, boldly ride,'
The shade replied,—
'If you seek for Eldorado!'''
        },
        {
            'title': 'The Raven',
            'content': '''Once upon a midnight dreary, while I pondered, weak and weary,
Over many a quaint and curious volume of forgotten lore—
While I nodded, nearly napping, suddenly there came a tapping,
As of some one gently rapping, rapping at my chamber door.
"'Tis some visitor," I muttered, "tapping at my chamber door—
Only this and nothing more."
Ah, distinctly I remember it was in the bleak December;
And each separate dying ember wrought its ghost upon the floor.
Eagerly I wished the morrow;—vainly I had sought to borrow
From my books surcease of sorrow—sorrow for the lost Lenore—
For the rare and radiant maiden whom the angels name Lenore—
Nameless here for evermore.'''
        },
        {
            'title': 'Annabel Lee',
            'content': '''It was many and many a year ago,
In a kingdom by the sea,
That a maiden there lived whom you may know
By the name of Annabel Lee;
And this maiden she lived with no other thought
Than to love and be loved by me.
I was a child and she was a child,
In this kingdom by the sea,
But we loved with a love that was more than love—
I and my Annabel Lee—
With a love that the wingèd seraphs of Heaven
Coveted her and me.'''
        },
        {
            'title': 'A Dream Within a Dream',
            'content': '''Take this kiss upon the brow!
And, in parting from you now,
Thus much let me avow —
You are not wrong, who deem
That my days have been a dream;
Yet if hope has flown away
In a night, or in a day,
In a vision, or in none,
Is it therefore the less gone?
All that we see or seem
Is but a dream within a dream.'''
        }
    ],
    'Walt Whitman': [
        {
            'title': 'Song of Myself (Excerpt)',
            'content': '''I celebrate myself, and sing myself,
And what I assume you shall assume,
For every atom belonging to me as good belongs to you.
I loafe and invite my soul,
I lean and loafe at my ease observing a spear of summer grass.
My tongue, every atom of my blood, form'd from this soil, this air,
Born here of parents born here from parents the same, and their parents the same,
I, now thirty-seven years old in perfect health begin,
Hoping to cease not till death.'''
        },
        {
            'title': 'A Noiseless Patient Spider',
            'content': '''A noiseless patient spider,
I mark'd where on a little promontory it stood isolated,
Mark'd how to explore the vacant vast surrounding,
It launch'd forth filament, filament, filament, out of itself,
Ever unreeling them, ever tirelessly speeding them.
And you O my soul where you stand,
Surrounded, detached, in measureless oceans of space,
Ceaselessly musing, venturing, throwing, seeking the spheres to connect them,
Till the bridge you will need be form'd, till the ductile anchor hold,
Till the gossamer thread you fling catch somewhere, O my soul.'''
        },
        {
            'title': 'O Captain! My Captain!',
            'content': '''O Captain! my Captain! our fearful trip is done,
The ship has weather'd every rack, the prize we sought is won,
The port is near, the bells I hear, the people all exulting,
While follow eyes the steady keel, the vessel grim and daring;
But O heart! heart! heart!
O the bleeding drops of red,
Where on the deck my Captain lies,
Fallen cold and dead.'''
        },
        {
            'title': 'I Hear America Singing',
            'content': '''I hear America singing, the varied carols I hear,
Those of mechanics, each one singing his as it should be blithe and strong,
The carpenter singing his as he measures his plank or beam,
The mason singing his as he makes ready for work, or leaves off work,
The boatman singing what belongs to him in his boat, the deckhand singing on the steamboat deck,
The shoemaker singing as he sits on his bench, the hatter singing as he stands,
The wood-cutter's song, the ploughboy's on his way in the morning, or at noon intermission or at sundown,
The delicious singing of the mother, or of the young wife at work, or of the girl sewing or washing,
Each singing what belongs to him or her and to none else,
The day what belongs to the day—at night the party of young fellows, robust, friendly,
Singing with open mouths their strong melodious songs.'''
        }
    ],
    'Lord Byron': [
        {
            'title': 'Darkness',
            'content': '''I had a dream, which was not all a dream.
The bright sun was extinguish'd, and the stars
Did wander darkling in the eternal space,
Rayless, and pathless, and the icy earth
Swung blind and blackening in the moonless air;
Morn came and went—and came, and brought no day,
And men forgot their passions in the dread
Of this their desolation; and all hearts
Were chill'd into a selfish prayer for light:'''
        },
        {
            'title': 'So We\'ll Go No More a Roving',
            'content': '''So, we'll go no more a roving
So late into the night,
Though the heart be still as loving,
And the moon be still as bright.
For the sword outwears its sheath,
And the soul wears out the breast,
And the heart must pause to breathe,
And love itself have rest.
Though the night was made for loving,
And the day returns too soon,
Yet we'll go no more a roving
By the light of the moon.'''
        },
        {
            'title': 'She Walks in Beauty',
            'content': '''She walks in beauty, like the night
Of cloudless climes and starry skies;
And all that's best of dark and bright
Meet in her aspect and her eyes;
Thus mellowed to that tender light
Which heaven to gaudy day denies.
One shade the more, one ray the less,
Had half impaired the nameless grace
Which waves in every raven tress,
Or softly lightens o'er her face;
Where thoughts serenely sweet express,
How pure, how dear their dwelling-place.'''
        },
        {
            'title': 'When We Two Parted',
            'content': '''When we two parted
In silence and tears,
Half broken-hearted
To sever for years,
Pale grew thy cheek and cold,
Colder thy kiss;
Truly that hour foretold
Sorrow to this.'''
        }
    ],
    'William Wordsworth': [
        {
            'title': 'Lines Written in Early Spring',
            'content': '''I heard a thousand blended notes,
While in a grove I sate reclined,
In that sweet mood when pleasant thoughts
Bring sad thoughts to the mind.
To her fair works did Nature link
The human soul that through me ran;
And much it grieved my heart to think
What man has made of man.
Through primrose tufts, in that green bower,
The periwinkle trailed its wreaths;
And 'tis my faith that every flower
Enjoys the air it breathes.'''
        },
        {
            'title': 'My Heart Leaps Up',
            'content': '''My heart leaps up when I behold
A rainbow in the sky:
So was it when my life began;
So is it now I am a man;
So be it when I shall grow old,
Or let me die!
The Child is father of the Man;
And I could wish my days to be
Bound each to each by natural piety.'''
        },
        {
            'title': 'I Wandered Lonely as a Cloud',
            'content': '''I wandered lonely as a cloud
That floats on high o'er vales and hills,
When all at once I saw a crowd,
A host, of golden daffodils;
Beside the lake, beneath the trees,
Fluttering and dancing in the breeze.
Continuous as the stars that shine
And twinkle on the milky way,
They stretched in never-ending line
Along the margin of a bay:
Ten thousand saw I at a glance,
Tossing their heads in sprightly dance.'''
        },
        {
            'title': 'The World Is Too Much with Us',
            'content': '''The world is too much with us; late and soon,
Getting and spending, we lay waste our powers;—
Little we see in Nature that is ours;
We have given our hearts away, a sordid boon!
This Sea that bares her bosom to the moon;
The winds that will be howling at all hours,
And are up-gathered now like sleeping flowers;
For this, for everything, we are out of tune;
It moves us not. Great God! I'd rather be
A Pagan suckled in a creed outworn;
So might I, standing on this pleasant lea,
Have glimpses that would make me less forlorn;
Have sight of Proteus rising from the sea;
Or hear old Triton blow his wreathèd horn.'''
        }
    ],
    'John Keats': [
        {
            'title': 'When I Have Fears That I May Cease to Be',
            'content': '''When I have fears that I may cease to be
Before my pen has gleaned my teeming brain,
Before high-pilèd books, in charactery,
Hold like rich garners the full ripened grain;
When I behold, upon the night's starred face,
Huge cloudy symbols of a high romance,
And think that I may never live to trace
Their shadows with the magic hand of chance;
And when I feel, fair creature of an hour,
That I shall never look upon thee more,
Never have relish in the faery power
Of unreflecting love—then on the shore
Of the wide world I stand alone, and think
Till love and fame to nothingness do sink.'''
        },
        {
            'title': 'La Belle Dame sans Merci',
            'content': '''O what can ail thee, knight-at-arms,
Alone and palely loitering?
The sedge has withered from the lake,
And no birds sing.
O what can ail thee, knight-at-arms,
So haggard and so woe-begone?
The squirrel's granary is full,
And the harvest's done.
I see a lily on thy brow,
With anguish moist and fever-dew,
And on thy cheeks a fading rose
Fast withereth too.'''
        },
        {
            'title': 'Ode to a Nightingale',
            'content': '''My heart aches, and a drowsy numbness pains
My sense, as though of hemlock I had drunk,
Or emptied some dull opiate to the drains
One minute past, and Lethe-wards had sunk:
'Tis not through envy of thy happy lot,
But being too happy in thine happiness,—
That thou, light-winged Dryad of the trees
In some melodious plot
Of beechen green, and shadows numberless,
Singest of summer in full-throated ease.'''
        },
        {
            'title': 'Bright Star',
            'content': '''Bright star, would I were stedfast as thou art—
Not in lone splendour hung aloft the night
And watching, with eternal lids apart,
Like nature's patient, sleepless Eremite,
The moving waters at their priestlike task
Of pure ablution round earth's human shores,
Or gazing on the new soft-fallen mask
Of snow upon the mountains and the moors—
No—yet still stedfast, still unchangeable,
Pillow'd upon my fair love's ripening breast,
To feel for ever its soft fall and swell,
Awake for ever in a sweet unrest,
Still, still to hear her tender-taken breath,
And so live ever—or else swoon to death.'''
        }
    ],
    'Percy Shelley': [
        {
            'title': 'Ode to the West Wind',
            'content': '''O wild West Wind, thou breath of Autumn's being,
Thou, from whose unseen presence the leaves dead
Are driven, like ghosts from an enchanter fleeing,
Yellow, and black, and pale, and hectic red,
Pestilence-stricken multitudes: O thou,
Who chariotest to their dark wintry bed
The winged seeds, where they lie cold and low,
Each like a corpse within its grave, until
Thine azure sister of the Spring shall blow
Her clarion o'er the dreaming earth, and fill
(Driving sweet buds like flocks to feed in air)
With living hues and odours plain and hill:
Wild Spirit, which art moving everywhere;
Destroyer and preserver; hear, oh hear!'''
        },
        {
            'title': 'To a Skylark',
            'content': '''Hail to thee, blithe Spirit!
Bird thou never wert,
That from Heaven, or near it,
Pourest thy full heart
In profuse strains of unpremeditated art.
Higher still and higher
From the earth thou springest
Like a cloud of fire;
The blue deep thou wingest,
And singing still dost soar, and soaring ever singest.'''
        },
        {
            'title': 'Ozymandias',
            'content': '''I met a traveller from an antique land,
Who said—"Two vast and trunkless legs of stone
Stand in the desert. . . . Near them, on the sand,
Half sunk a shattered visage lies, whose frown,
And wrinkled lip, and sneer of cold command,
Tell that its sculptor well those passions read
Which yet survive, stamped on these lifeless things,
The hand that mocked them, and the heart that fed;
And on the pedestal, these words appear:
My name is Ozymandias, King of Kings;
Look on my Works, ye Mighty, and despair!
Nothing beside remains. Round the decay
Of that colossal Wreck, boundless and bare
The lone and level sands stretch far away."'''
        },
        {
            'title': 'Love\'s Philosophy',
            'content': '''The fountains mingle with the river
And the rivers with the ocean,
The winds of heaven mix for ever
With a sweet emotion;
Nothing in the world is single;
All things by a law divine
In one spirit meet and mingle.
Why not I with thine?—
See the mountains kiss high heaven
And the waves clasp one another;
No sister-flower would be forgiven
If it disdained its brother;
And the sunlight clasps the earth
And the moonbeams kiss the sea:
What is all this sweet work worth
If thou kiss not me?'''
        }
    ],
    'Robert Burns': [
        {
            'title': 'Auld Lang Syne',
            'content': '''Should auld acquaintance be forgot,
And never brought to mind?
Should auld acquaintance be forgot,
And auld lang syne!
For auld lang syne, my dear,
For auld lang syne.
We'll tak a cup o' kindness yet,
For auld lang syne.
And surely ye'll be your pint-stowp!
And surely I'll be mine!
And we'll tak a cup o' kindness yet,
For auld lang syne.'''
        },
        {
            'title': 'Ae Fond Kiss',
            'content': '''Ae fond kiss, and then we sever;
Ae fareweel, alas, for ever!
Deep in heart-wrung tears I'll pledge thee,
Warring sighs and groans I'll wage thee.
Who shall say that Fortune grieves him,
While the star of hope she leaves him?
Me, nae cheerful twinkle lights me;
Dark despair around benights me.'''
        },
        {
            'title': 'A Red, Red Rose',
            'content': '''O my Luve is like a red, red rose
That's newly sprung in June;
O my Luve is like the melody
That's sweetly played in tune.
So fair art thou, my bonnie lass,
So deep in luve am I;
And I will luve thee still, my dear,
Till a' the seas gang dry.
Till a' the seas gang dry, my dear,
And the rocks melt wi' the sun;
I will love thee still, my dear,
While the sands o' life shall run.'''
        },
        {
            'title': 'To a Mouse',
            'content': '''Wee, sleekit, cowrin, tim'rous beastie,
O, what a panic's in thy breastie!
Thou need na start awa sae hasty,
Wi' bickering brattle!
I wad be laith to rin an' chase thee,
Wi' murd'ring pattle!
I'm truly sorry man's dominion,
Has broken nature's social union,
An' justifies that ill opinion,
Which makes thee startle
At me, thy poor, earth-born companion,
An' fellow-mortal!'''
        }
    ]
}

def seed_database():
    with app.app_context():
        print("Starting to seed database with famous poems...")
        
        # Create or get poet accounts
        poets_created = 0
        poems_created = 0
        
        for poet_name, poems in FAMOUS_POEMS.items():
            # Check if poet user already exists
            poet_user = User.query.filter_by(username=poet_name).first()
            
            if not poet_user:
                # Create poet user account
                poet_user = User(
                    username=poet_name,
                    email=f'{poet_name.lower().replace(" ", "")}@poetryvault.com',
                    password_hash=generate_password_hash('classic_poet_2024'),
                    age=None,
                    favorite_poet=poet_name,
                    is_admin=False
                )
                db.session.add(poet_user)
                db.session.flush()  # Get the user ID
                poets_created += 1
                print(f"Created poet account: {poet_name}")
            
            # Add poems for this poet
            for poem_data in poems:
                # Check if poem already exists
                existing_poem = Poem.query.filter_by(
                    title=poem_data['title'],
                    user_id=poet_user.id
                ).first()
                
                if not existing_poem:
                    poem = Poem(
                        title=poem_data['title'],
                        content=poem_data['content'],
                        user_id=poet_user.id,
                        is_classic=True  # Mark as classic so it's hidden from home feed
                    )
                    db.session.add(poem)
                    poems_created += 1
                    print(f"  Added: {poem_data['title']}")
        
        db.session.commit()
        print(f"\n✅ Database seeded successfully!")
        print(f"   Poets created: {poets_created}")
        print(f"   Poems added: {poems_created}")
        print(f"\nYou can now search for these classic poems in Poetry Vault!")

if __name__ == '__main__':
    seed_database()
