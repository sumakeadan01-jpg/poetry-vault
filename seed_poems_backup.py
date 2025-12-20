"""
Seed the database with famous poems from classic poets
This file contains the FAMOUS_POEMS dictionary used by app.py for auto-seeding
"""

# Famous poems database
FAMOUS_POEMS = {
    'Shakespeare': [
        {
            'title': 'Sonnet 29: When in Disgrace with Fortune',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
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
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
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
            'category': 'aging',
            'mood': 'melancholic',
            'theme': 'mortality',
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
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
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
        },
        {
            'title': 'Sonnet 55: Not Marble, Nor the Gilded Monuments',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''Not marble, nor the gilded monuments
Of princes, shall outlive this powerful rhyme;
But you shall shine more bright in these contents
Than unswept stone besmear'd with sluttish time.
When wasteful war shall statues overturn,
And broils root out the work of masonry,
Nor Mars his sword nor war's quick fire shall burn
The living record of your memory.
'Gainst death and all-oblivious enmity
Shall you pace forth; your praise shall still find room
Even in the eyes of all posterity
That wear this world out to the ending doom.
So, till the judgment that yourself arise,
You live in this, and dwell in lover's eyes.'''
        },
        {
            'title': 'Sonnet 60: Like as the Waves',
            'category': 'time',
            'mood': 'nostalgic',
            'theme': 'passage',
            'content': '''Like as the waves make towards the pebbled shore,
So do our minutes hasten to their end;
Each changing place with that which goes before,
In sequent toil all forwards do contend.
Nativity, once in the main of light,
Crawls to maturity, wherewith being crown'd,
Crooked eclipses 'gainst his glory fight,
And Time that gave doth now his gift confound.
Time doth transfix the flourish set on youth
And delves the parallels in beauty's brow,
Feeds on the rarities of nature's truth,
And nothing stands but for his scythe to mow:
And yet to times in hope my verse shall stand,
Praising thy worth, despite his cruel hand.'''
        },
        {
            'title': 'Sonnet 106: When in the Chronicle of Wasted Time',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''When in the chronicle of wasted time
I see descriptions of the fairest wights,
And beauty making beautiful old rhyme
In praise of ladies dead and lovely knights,
Then, in the blazon of sweet beauty's best,
Of hand, of foot, of lip, of eye, of brow,
I see their antique pen would have express'd
Even such a beauty as you master now.
So all their praises are but prophecies
Of this our time, all you prefiguring;
And, for they look'd but with divining eyes,
They had not skill enough your worth to sing:
For we, which now behold these present days,
Had eyes to wonder, but lack tongues to praise.'''
        },
        {
            'title': 'Sonnet 71: No Longer Mourn for Me',
            'category': 'death',
            'mood': 'somber',
            'theme': 'mortality',
            'content': '''No longer mourn for me when I am dead
Than you shall hear the surly sullen bell
Give warning to the world that I am fled
From this vile world, with vilest worms to dwell:
Nay, if you read this line, remember not
The hand that writ it; for I love you so
That I in your sweet thoughts would be forgot
If thinking on me then should make you woe.
O, if, I say, you look upon this verse
When I perhaps compounded am with clay,
Do not so much as my poor name rehearse.
But let your love even with my life decay,
Lest the wise world should look into your moan
And mock you with me after I am gone.'''
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
            'category': 'spirituality',
            'mood': 'contemplative',
            'theme': 'divine',
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
            'category': 'spirituality',
            'mood': 'contemplative',
            'theme': 'divine',
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
            'category': 'spirituality',
            'mood': 'contemplative',
            'theme': 'divine',
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
            'category': 'spirituality',
            'mood': 'contemplative',
            'theme': 'divine',
            'content': '''The breeze at dawn has secrets to tell you.
Don't go back to sleep.
You must ask for what you really want.
Don't go back to sleep.
People are going back and forth across the doorsill
where the two worlds touch.
The door is round and open.
Don't go back to sleep.'''
        },
        {
            'title': 'The Minute I Heard My First Love Story',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''The minute I heard my first love story,
I started looking for you, not knowing
how blind that was.
Lovers don't finally meet somewhere.
They're in each other all along.'''
        },
        {
            'title': 'Out Beyond Ideas',
            'category': 'spirituality',
            'mood': 'contemplative',
            'theme': 'divine',
            'content': '''Out beyond ideas of wrongdoing and rightdoing,
there is a field. I'll meet you there.
When the soul lies down in that grass,
the world is too full to talk about.
Ideas, language, even the phrase "each other"
doesn't make any sense.'''
        },
        {
            'title': 'Let Yourself Be Silently Drawn',
            'category': 'spirituality',
            'mood': 'contemplative',
            'theme': 'divine',
            'content': '''Let yourself be silently drawn
by the strange pull of what you really love.
It will not lead you astray.'''
        },
        {
            'title': 'The Wound is the Place',
            'category': 'spirituality',
            'mood': 'contemplative',
            'theme': 'divine',
            'content': '''The wound is the place where the Light enters you.
Don't grieve. Anything you lose comes round
in another form.'''
        },
        {
            'title': 'Forget Your Life',
            'category': 'spirituality',
            'mood': 'contemplative',
            'theme': 'divine',
            'content': '''Forget your life. Say God is Great. Get up.
You think you know what time it is. It's time to pray.
You've carved so many little figurines, too many.
Don't knock on any random door like a beggar.
Reach your long hand out to another door, beyond where
you go on the street, the street
where everyone says, "How are you?"
and no one says How aren't you?'''
        }
    ],
    'Emily Dickinson': [
        {
            'title': 'She rose to his requirement',
            'category': 'life',
            'mood': 'philosophical',
            'theme': 'existence',
            'content': '''She rose to his requirement, dropped
The playthings of her life,
To the honorable work
Of woman and of wife.
If aught she missed in her new day
Of amplitude, or awe,
Or first prospective, or the gold
in using wore away,
It lay unmentioned, as the sea
Develops pearl and weed,
But only to himself is known
The fathoms they abide.'''
        },
        {
            'title': 'Wild Nights - Wild Nights!',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
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
            'title': 'Hope is the Thing with Feathers',
            'category': 'hope',
            'mood': 'optimistic',
            'theme': 'faith',
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
            'category': 'death',
            'mood': 'somber',
            'theme': 'mortality',
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
My Tippet – only Tulle –
We paused before a House that seemed
A Swelling of the Ground –
The Roof was scarcely visible –
The Cornice – in the Ground –
Since then – 'tis Centuries – and yet
Feels shorter than the Day
I first surmised the Horses' Heads
Were toward Eternity –'''
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
        },
        {
            'title': 'Tell All the Truth but Tell It Slant',
            'category': 'truth',
            'mood': 'honest',
            'theme': 'reality',
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
            'category': 'solitude',
            'mood': 'reflective',
            'theme': 'isolation',
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
            'title': 'A Bird Came Down the Walk',
            'category': 'nature',
            'mood': 'peaceful',
            'theme': 'beauty',
            'content': '''A Bird came down the Walk —
He did not know I saw —
He bit an Angleworm in halves
And ate the fellow, raw,
And then he drank a Dew
From a convenient Grass —
And then hopped sidewise to the Wall
To let a Beetle pass —
He glanced with rapid eyes
That hurried all around —
They looked like frightened Beads, I thought —
He stirred his Velvet Head
Like one in danger, Cautious,
I offered him a Crumb
And he unrolled his feathers
And rowed him softer home —
Than Oars divide the Ocean,
Too silver for a seam —
Or Butterflies, off Banks of Noon
Leap, plashless as they swim.'''
        },
        {
            'title': 'There\'s a Certain Slant of Light',
            'content': '''There's a certain Slant of light,
Winter Afternoons —
That oppresses, like the Heft
Of Cathedral Tunes —
Heavenly Hurt, it gives us —
We can find no scar,
But internal difference —
Where the Meanings, are —
None may teach it — Any —
'Tis the seal Despair —
An imperial affliction
Sent us of the Air —
When it comes, the Landscape listens —
Shadows — hold their breath —
When it goes, 'tis like the Distance
On the look of Death —'''
        },
        {
            'title': 'I Heard a Fly Buzz When I Died',
            'category': 'death',
            'mood': 'somber',
            'theme': 'mortality',
            'content': '''I heard a Fly buzz — when I died —
The Stillness in the Room
Was like the Stillness in the Air —
Between the Heaves of Storm —
The Eyes around — had wrung them dry —
And Breaths were gathering firm
For that last Onset — when the King
Be witnessed — in the Room —
I willed my Keepsakes — Signed away
What portion of me be
Assignable — and then it was
There interposed a Fly —
With Blue — uncertain — stumbling Buzz —
Between the light — and me —
And then the Windows failed — and then
I could not see to see —'''
        },
        {
            'title': 'Success is Counted Sweetest',
            'category': 'life',
            'mood': 'philosophical',
            'theme': 'existence',
            'content': '''Success is counted sweetest
By those who ne'er succeed.
To comprehend a nectar
Requires sorest need.
Not one of all the purple Host
Who took the Flag today
Can tell the definition
So clear of victory
As he defeated — dying —
On whose forbidden ear
The distant strains of triumph
Burst agonized and clear!'''
        }
    ],
    'Edgar Allan Poe': [
        {
            'title': 'Alone',
            'category': 'solitude',
            'mood': 'reflective',
            'theme': 'isolation',
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
            'category': 'quest',
            'mood': 'determined',
            'theme': 'seeking',
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
            'category': 'grief',
            'mood': 'sorrowful',
            'theme': 'loss',
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
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
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
            'category': 'reality',
            'mood': 'serious',
            'theme': 'truth',
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
        },
        {
            'title': 'The Bells',
            'category': 'life',
            'mood': 'philosophical',
            'theme': 'existence',
            'content': '''Hear the sledges with the bells—
Silver bells!
What a world of merriment their melody foretells!
How they tinkle, tinkle, tinkle,
In the icy air of night!
While the stars that oversprinkle
All the heavens, seem to twinkle
With a crystalline delight;
Keeping time, time, time,
In a sort of Runic rhyme,
To the tintinnabulation that so musically wells
From the bells, bells, bells, bells,
Bells, bells, bells—
From the jingling and the tinkling of the bells.'''
        },
        {
            'title': 'To Helen',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''Helen, thy beauty is to me
Like those Nicéan barks of yore,
That gently, o'er a perfumed sea,
The weary, way-worn wanderer bore
To his own native shore.
On desperate seas long wont to roam,
Thy hyacinth hair, thy classic face,
Thy Naiad airs have brought me home
To the glory that was Greece,
And the grandeur that was Rome.'''
        },
        {
            'title': 'The Haunted Palace',
            'category': 'decay',
            'mood': 'melancholic',
            'theme': 'decline',
            'content': '''In the greenest of our valleys
By good angels tenanted,
Once a fair and stately palace—
Radiant palace—reared its head.
In the monarch Thought's dominion—
It stood there!
Never seraph spread a pinion
Over fabric half so fair!'''
        },
        {
            'title': 'A Dream',
            'category': 'melancholy',
            'mood': 'sad',
            'theme': 'sorrow',
            'content': '''In visions of the dark night
I have dreamed of joy departed—
But a waking dream of life and light
Hath left me broken-hearted.
Ah! what is not a dream by day
To him whose eyes are cast
On things around him with a ray
Turned back upon the past?'''
        },
        {
            'title': 'Spirits of the Dead',
            'category': 'death',
            'mood': 'somber',
            'theme': 'mortality',
            'content': '''Thy soul shall find itself alone
'Mid dark thoughts of the grey tomb-stone;
Not one, of all the crowd, to pry
Into thine hour of secrecy.
Be silent in that solitude,
Which is not loneliness—for then
The spirits of the dead, who stood
In life before thee, are again
In death around thee, and their will
Shall overshadow thee; be still.'''
        }
    ],
    'Walt Whitman': [
        {
            'title': 'Song of Myself (Excerpt)',
            'category': 'self',
            'mood': 'introspective',
            'theme': 'identity',
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
            'category': 'solitude',
            'mood': 'reflective',
            'theme': 'isolation',
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
            'category': 'grief',
            'mood': 'sorrowful',
            'theme': 'loss',
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
            'category': 'celebration',
            'mood': 'joyful',
            'theme': 'festivity',
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
        },
        {
            'title': 'When I Heard the Learn\'d Astronomer',
            'content': '''When I heard the learn'd astronomer,
When the proofs, the figures, were ranged in columns before me,
When I was shown the charts and diagrams, to add, divide, and measure them,
When I sitting heard the astronomer where he lectured with much applause in the lecture-room,
How soon unaccountable I became tired and sick,
Till rising and gliding out I wander'd off by myself,
In the mystical moist night-air, and from time to time,
Look'd up in perfect silence at the stars.'''
        },
        {
            'title': 'For You O Democracy',
            'category': 'patriotism',
            'mood': 'proud',
            'theme': 'loyalty',
            'content': '''Come, I will make the continent indissoluble,
I will make the most splendid race the sun ever shone upon,
I will make divine magnetic lands,
With the love of comrades,
With the life-long love of comrades.
I will plant companionship thick as trees along all the rivers of America,
and along the shores of the great lakes, and all over the prairies,
I will make inseparable cities with their arms about each other's necks,
By the love of comrades,
By the manly love of comrades.'''
        },
        {
            'title': 'Miracles',
            'category': 'wonder',
            'mood': 'amazed',
            'theme': 'mystery',
            'content': '''Why, who makes much of a miracle?
As to me I know of nothing else but miracles,
Whether I walk the streets of Manhattan,
Or dart my sight over the roofs of houses toward the sky,
Or wade with naked feet along the beach just in the edge of the water,
Or stand under trees in the woods,
Or talk by day with any one I love,
Or sleep in the bed at night with any one I love,
Or sit at table at dinner with the rest,
Or look at strangers opposite me riding in the car,
Or watch honey-bees busy around the hive of a summer forenoon.'''
        },
        {
            'title': 'The Wound-Dresser',
            'category': 'war',
            'mood': 'intense',
            'theme': 'conflict',
            'content': '''Bearing the bandages, water and sponge,
Straight and swift to my wounded I go,
Where they lie on the ground after the battle brought in,
Where their priceless blood reddens the grass, the ground,
Or to the rows of the hospital tent, or under the roof'd hospital,
To the long rows of cots up and down each side I return,
To each and all one after another I draw near, not one do I miss,
An attendant follows holding a tray, he carries a refuse pail,
Soon to be fill'd with clotted rags and blood, emptied, and fill'd again.'''
        },
        {
            'title': 'Crossing Brooklyn Ferry',
            'category': 'time',
            'mood': 'nostalgic',
            'theme': 'passage',
            'content': '''Flood-tide below me! I see you face to face!
Clouds of the west—sun there half an hour high—I see you also face to face.
Crowds of men and women attired in the usual costumes, how curious you are to me!
On the ferry-boats the hundreds and hundreds that cross, returning home, are more curious to me than you suppose,
And you that shall cross from shore to shore years hence are more to me, and more in my meditations, than you might suppose.'''
        }
    ],
    'Lord Byron': [
        {
            'title': 'Darkness',
            'category': 'apocalypse',
            'mood': 'ominous',
            'theme': 'destruction',
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
            'category': 'beauty',
            'mood': 'admiring',
            'theme': 'aesthetics',
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
            'category': 'heartbreak',
            'mood': 'devastated',
            'theme': 'loss',
            'content': '''When we two parted
In silence and tears,
Half broken-hearted
To sever for years,
Pale grew thy cheek and cold,
Colder thy kiss;
Truly that hour foretold
Sorrow to this.'''
        },
        {
            'title': 'The Destruction of Sennacherib',
            'category': 'war',
            'mood': 'intense',
            'theme': 'conflict',
            'content': '''The Assyrian came down like the wolf on the fold,
And his cohorts were gleaming in purple and gold;
And the sheen of their spears was like stars on the sea,
When the blue wave rolls nightly on deep Galilee.
Like the leaves of the forest when Summer is green,
That host with their banners at sunset were seen:
Like the leaves of the forest when Autumn hath blown,
That host on the morrow lay withered and strown.'''
        },
        {
            'title': 'Stanzas for Music',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''There be none of Beauty's daughters
With a magic like thee;
And like music on the waters
Is thy sweet voice to me:
When, as if its sound were causing
The charmed ocean's pausing,
The waves lie still and gleaming,
And the lull'd winds seem dreaming.'''
        },
        {
            'title': 'The Ocean',
            'category': 'nature',
            'mood': 'peaceful',
            'theme': 'beauty',
            'content': '''Roll on, thou deep and dark blue Ocean—roll!
Ten thousand fleets sweep over thee in vain;
Man marks the earth with ruin—his control
Stops with the shore;—upon the watery plain
The wrecks are all thy deed, nor doth remain
A shadow of man's ravage, save his own,
When for a moment, like a drop of rain,
He sinks into thy depths with bubbling groan,
Without a grave, unknell'd, uncoffin'd, and unknown.'''
        },
        {
            'title': 'To Thomas Moore',
            'category': 'friendship',
            'mood': 'warm',
            'theme': 'companionship',
            'content': '''My boat is on the shore,
And my bark is on the sea;
But, before I go, Tom Moore,
Here's a double health to thee!
Here's a sigh to those who love me,
And a smile to those who hate;
And, whatever sky's above me,
Here's a heart for every fate.'''
        },
        {
            'title': 'Remember Thee',
            'category': 'betrayal',
            'mood': 'bitter',
            'theme': 'deception',
            'content': '''Remember thee! remember thee!
Till Lethe quench life's burning stream
Remorse and shame shall cling to thee,
And haunt thee like a feverish dream!
Remember thee! Aye, doubt it not.
Thy husband too shall think of thee:
By neither shalt thou be forgot,
Thou false to him, thou fiend to me!'''
        }
    ],
    'William Wordsworth': [
        {
            'title': 'Lines Written in Early Spring',
            'category': 'nature',
            'mood': 'peaceful',
            'theme': 'beauty',
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
            'category': 'joy',
            'mood': 'happy',
            'theme': 'celebration',
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
            'category': 'nature',
            'mood': 'peaceful',
            'theme': 'beauty',
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
            'category': 'nature',
            'mood': 'peaceful',
            'theme': 'beauty',
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
        },
        {
            'title': 'Composed Upon Westminster Bridge',
            'category': 'beauty',
            'mood': 'admiring',
            'theme': 'aesthetics',
            'content': '''Earth has not anything to show more fair:
Dull would he be of soul who could pass by
A sight so touching in its majesty:
This City now doth, like a garment, wear
The beauty of the morning; silent, bare,
Ships, towers, domes, theatres, and temples lie
Open unto the fields, and to the sky;
All bright and glittering in the smokeless air.'''
        },
        {
            'title': 'She Dwelt Among the Untrodden Ways',
            'category': 'loss',
            'mood': 'sorrowful',
            'theme': 'grief',
            'content': '''She dwelt among the untrodden ways
Beside the springs of Dove,
A Maid whom there were none to praise
And very few to love:
A violet by a mossy stone
Half hidden from the eye!
—Fair as a star, when only one
Is shining in the sky.
She lived unknown, and few could know
When Lucy ceased to be;
But she is in her grave, and, oh,
The difference to me!'''
        },
        {
            'title': 'A Slumber Did My Spirit Seal',
            'category': 'death',
            'mood': 'somber',
            'theme': 'mortality',
            'content': '''A slumber did my spirit seal;
I had no human fears:
She seemed a thing that could not feel
The touch of earthly years.
No motion has she now, no force;
She neither hears nor sees;
Rolled round in earth's diurnal course,
With rocks, and stones, and trees.'''
        },
        {
            'title': 'The Solitary Reaper',
            'category': 'nature',
            'mood': 'peaceful',
            'theme': 'beauty',
            'content': '''Behold her, single in the field,
Yon solitary Highland Lass!
Reaping and singing by herself;
Stop here, or gently pass!
Alone she cuts and binds the grain,
And sings a melancholy strain;
O listen! for the Vale profound
Is overflowing with the sound.'''
        },
        {
            'title': 'Tintern Abbey (Excerpt)',
            'category': 'nature',
            'mood': 'peaceful',
            'theme': 'beauty',
            'content': '''Five years have past; five summers, with the length
Of five long winters! and again I hear
These waters, rolling from their mountain-springs
With a soft inland murmur.—Once again
Do I behold these steep and lofty cliffs,
That on a wild secluded scene impress
Thoughts of more deep seclusion; and connect
The landscape with the quiet of the sky.'''
        }
    ],
    'John Keats': [
        {
            'title': 'When I Have Fears That I May Cease to Be',
            'category': 'mortality',
            'mood': 'somber',
            'theme': 'death',
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
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
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
            'category': 'mortality',
            'mood': 'somber',
            'theme': 'death',
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
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
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
        },
        {
            'title': 'Ode on a Grecian Urn',
            'category': 'art',
            'mood': 'creative',
            'theme': 'expression',
            'content': '''Thou still unravish'd bride of quietness,
Thou foster-child of silence and slow time,
Sylvan historian, who canst thus express
A flowery tale more sweetly than our rhyme:
What leaf-fring'd legend haunts about thy shape
Of deities or mortals, or of both,
In Tempe or the dales of Arcady?
What men or gods are these? What maidens loth?
What mad pursuit? What struggle to escape?
What pipes and timbrels? What wild ecstasy?'''
        },
        {
            'title': 'Ode on Melancholy',
            'category': 'melancholy',
            'mood': 'sad',
            'theme': 'sorrow',
            'content': '''No, no, go not to Lethe, neither twist
Wolf's-bane, tight-rooted, for its poisonous wine;
Nor suffer thy pale forehead to be kiss'd
By nightshade, ruby grape of Proserpine;
Make not your rosary of yew-berries,
Nor let the beetle, nor the death-moth be
Your mournful Psyche, nor the downy owl
A partner in your sorrow's mysteries;
For shade to shade will come too drowsily,
And drown the wakeful anguish of the soul.'''
        },
        {
            'title': 'To Autumn',
            'category': 'autumn',
            'mood': 'melancholic',
            'theme': 'change',
            'content': '''Season of mists and mellow fruitfulness,
Close bosom-friend of the maturing sun;
Conspiring with him how to load and bless
With fruit the vines that round the thatch-eves run;
To bend with apples the moss'd cottage-trees,
And fill all fruit with ripeness to the core;
To swell the gourd, and plump the hazel shells
With a sweet kernel; to set budding more,
And still more, later flowers for the bees,
Until they think warm days will never cease,
For summer has o'er-brimm'd their clammy cells.'''
        },
        {
            'title': 'On First Looking into Chapman\'s Homer',
            'content': '''Much have I travell'd in the realms of gold,
And many goodly states and kingdoms seen;
Round many western islands have I been
Which bards in fealty to Apollo hold.
Oft of one wide expanse had I been told
That deep-brow'd Homer ruled as his demesne;
Yet did I never breathe its pure serene
Till I heard Chapman speak out loud and bold:
Then felt I like some watcher of the skies
When a new planet swims into his ken;
Or like stout Cortez when with eagle eyes
He star'd at the Pacific—and all his men
Look'd at each other with a wild surmise—
Silent, upon a peak in Darien.'''
        },
        {
            'title': 'The Eve of St. Agnes (Excerpt)',
            'category': 'winter',
            'mood': 'cold',
            'theme': 'season',
            'content': '''St. Agnes' Eve—Ah, bitter chill it was!
The owl, for all his feathers, was a-cold;
The hare limp'd trembling through the frozen grass,
And silent was the flock in woolly fold:
Numb were the Beadsman's fingers, while he told
His rosary, and while his frosted breath,
Like pious incense from a censer old,
Seem'd taking flight for heaven, without a death,
Past the sweet Virgin's picture, while his prayer he saith.'''
        }
    ],
    'Percy Shelley': [
        {
            'title': 'Ode to the West Wind',
            'category': 'nature',
            'mood': 'peaceful',
            'theme': 'beauty',
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
            'category': 'nature',
            'mood': 'peaceful',
            'theme': 'beauty',
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
            'category': 'power',
            'mood': 'confident',
            'theme': 'strength',
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
        },
        {
            'title': 'Music, When Soft Voices Die',
            'category': 'memory',
            'mood': 'nostalgic',
            'theme': 'remembrance',
            'content': '''Music, when soft voices die,
Vibrates in the memory—
Odours, when sweet violets sicken,
Live within the sense they quicken.
Rose leaves, when the rose is dead,
Are heaped for the belovèd's bed;
And so thy thoughts, when thou art gone,
Love itself shall slumber on.'''
        },
        {
            'title': 'The Cloud',
            'category': 'nature',
            'mood': 'peaceful',
            'theme': 'beauty',
            'content': '''I bring fresh showers for the thirsting flowers,
From the seas and the streams;
I bear light shade for the leaves when laid
In their noonday dreams.
From my wings are shaken the dews that waken
The sweet buds every one,
When rocked to rest on their mother's breast,
As she dances about the sun.'''
        },
        {
            'title': 'Mutability',
            'category': 'change',
            'mood': 'uncertain',
            'theme': 'transformation',
            'content': '''We are as clouds that veil the midnight moon;
How restlessly they speed, and gleam, and quiver,
Streaking the darkness radiantly!—yet soon
Night closes round, and they are lost for ever:
Or like forgotten lyres, whose dissonant strings
Give various response to each varying blast,
To whose frail frame no second motion brings
One mood or modulation like the last.'''
        },
        {
            'title': 'To Night',
            'category': 'night',
            'mood': 'mysterious',
            'theme': 'darkness',
            'content': '''Swiftly walk o'er the western wave,
Spirit of Night!
Out of the misty eastern cave,
Where, all the long and lone daylight,
Thou wovest dreams of joy and fear,
Which make thee terrible and dear,—
Swift be thy flight!'''
        },
        {
            'title': 'Hymn to Intellectual Beauty',
            'category': 'beauty',
            'mood': 'admiring',
            'theme': 'aesthetics',
            'content': '''The awful shadow of some unseen Power
Floats though unseen among us; visiting
This various world with as inconstant wing
As summer winds that creep from flower to flower;
Like moonbeams that behind some piny mountain shower,
It visits with inconstant glance
Each human heart and countenance;
Like hues and harmonies of evening,
Like clouds in starlight widely spread,
Like memory of music fled,
Like aught that for its grace may be
Dear, and yet dearer for its mystery.'''
        }
    ],
    'Robert Burns': [
        {
            'title': 'Auld Lang Syne',
            'category': 'friendship',
            'mood': 'warm',
            'theme': 'companionship',
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
            'category': 'heartbreak',
            'mood': 'devastated',
            'theme': 'loss',
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
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
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
            'category': 'nature',
            'mood': 'peaceful',
            'theme': 'beauty',
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
        },
        {
            'title': 'Tam o\' Shanter (Excerpt)',
            'content': '''When chapman billies leave the street,
And drouthy neibors neibors meet,
As market-days are wearing late,
An' folk begin to tak the gate;
While we sit bousing at the nappy,
An' getting fou and unco happy,
We think na on the lang Scots miles,
The mosses, waters, slaps, and stiles,
That lie between us and our hame,
Whare sits our sulky sullen dame,
Gathering her brows like gathering storm,
Nursing her wrath to keep it warm.'''
        },
        {
            'title': 'To a Louse',
            'category': 'humor',
            'mood': 'playful',
            'theme': 'comedy',
            'content': '''Ha! whare ye gaun, ye crowlin ferlie?
Your impudence protects you sairly;
I canna say but ye strunt rarely,
Owre gauze and lace;
Tho', faith! I fear ye dine but sparely
On sic a place.
Ye ugly, creepin, blastit wonner,
Detested, shunn'd by saunt an' sinner,
How daur ye set your fit upon her—
Sae fine a lady!
Gae somewhere else and seek your dinner
On some poor body.'''
        },
        {
            'title': 'Address to the Deil',
            'category': 'humor',
            'mood': 'playful',
            'theme': 'comedy',
            'content': '''O Thou! whatever title suit thee,
Auld Hornie, Satan, Nick, or Clootie!
Wha in yon cavern, grim an' sootie,
Clos'd under hatches,
Spairges about the brunstane cootie
To scaud poor wretches!
Hear me, Auld Hangie, for a wee,
An' let poor damned bodies be;
I'm sure sma' pleasure it can gie,
E'en to a deil,
To skelp an' scaud poor dogs like me,
An' hear us squeel!'''
        },
        {
            'title': 'The Banks o\' Doon',
            'content': '''Ye banks and braes o' bonnie Doon,
How can ye bloom sae fresh and fair?
How can ye chant, ye little birds,
And I sae weary fu' o' care!
Thou'll break my heart, thou warbling bird,
That wantons thro' the flowering thorn:
Thou minds me o' departed joys,
Departed never to return.'''
        },
        {
            'title': 'John Anderson, My Jo',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''John Anderson, my jo, John,
When we were first acquent,
Your locks were like the raven,
Your bonie brow was brent;
But now your brow is beld, John,
Your locks are like the snaw,
But blessings on your frosty pow,
John Anderson, my jo!'''
        },
        {
            'title': 'Scots Wha Hae',
            'category': 'patriotism',
            'mood': 'proud',
            'theme': 'loyalty',
            'content': '''Scots, wha hae wi' Wallace bled,
Scots, wham Bruce has aften led,
Welcome to your gory bed
Or to victorie!
Now's the day, and now's the hour:
See the front o' battle lour,
See approach proud Edward's power—
Chains and slaverie!'''
        }
    ],
    'Robert Frost': [
        {
            'title': 'The Road Not Taken',
            'content': '''Two roads diverged in a yellow wood,
And sorry I could not travel both
And be one traveler, long I stood
And looked down one as far as I could
To where it bent in the undergrowth;
Then took the other, as just as fair,
And having perhaps the better claim,
Because it was grassy and wanted wear;
Though as for that the passing there
Had worn them really about the same.'''
        },
        {
            'title': 'Stopping by Woods on a Snowy Evening',
            'content': '''Whose woods these are I think I know.
His house is in the village though;
He will not see me stopping here
To watch his woods fill up with snow.
My little horse must think it queer
To stop without a farmhouse near
Between the woods and frozen lake
The darkest evening of the year.
He gives his harness bells a shake
To ask if there is some mistake.
The only other sound's the sweep
Of easy wind and downy flake.
The woods are lovely, dark and deep,
But I have promises to keep,
And miles to go before I sleep,
And miles to go before I sleep.'''
        },
        {
            'title': 'Fire and Ice',
            'content': '''Some say the world will end in fire,
Some say in ice.
From what I've tasted of desire
I hold with those who favor fire.
But if it had to perish twice,
I think I know enough of hate
To say that for destruction ice
Is also great
And would suffice.'''
        },
        {
            'title': 'Mending Wall',
            'content': '''Something there is that doesn't love a wall,
That sends the frozen-ground-swell under it,
And spills the upper boulders in the sun;
And makes gaps even two can pass abreast.
The work of hunters is another thing:
I have come after them and made repair
Where they have left not one stone on a stone,
But they would have the rabbit out of hiding,
To please the yelping dogs.'''
        },
        {
            'title': 'Nothing Gold Can Stay',
            'content': '''Nature's first green is gold,
Her hardest hue to hold.
Her early leaf's a flower;
But only so an hour.
Then leaf subsides to leaf.
So Eden sank to grief,
So dawn goes down to day.
Nothing gold can stay.'''
        },
        {
            'title': 'Birches',
            'content': '''When I see birches bend to left and right
Across the lines of straighter darker trees,
I like to think some boy's been swinging them.
But swinging doesn't bend them down to stay
As ice-storms do. Often you must have seen them
Loaded with ice a sunny winter morning
After a rain. They click upon themselves
As the breeze rises, and turn many-colored
As the stir cracks and crazes their enamel.'''
        },
        {
            'title': 'Acquainted with the Night',
            'content': '''I have been one acquainted with the night.
I have walked out in rain—and back in rain.
I have outwalked the furthest city light.
I have looked down the saddest city lane.
I have passed by the watchman on his beat
And dropped my eyes, unwilling to explain.'''
        },
        {
            'title': 'The Gift Outright',
            'content': '''The land was ours before we were the land's.
She was our land more than a hundred years
Before we were her people. She was ours
In Massachusetts, in Virginia,
But we were England's, still colonials,
Possessing what we still were unpossessed by,
Possessed by what we now no more possessed.'''
        },
        {
            'title': 'Desert Places',
            'content': '''Snow falling and night falling fast, oh, fast
In a field I looked into going past,
And the ground almost covered smooth in snow,
But a few weeds and stubble showing last.
The woods around it have it—it is theirs.
All animals are smothered in their lairs.
I am too absent-spirited to count;
The loneliness includes me unawares.'''
        },
        {
            'title': 'After Apple-Picking',
            'content': '''My long two-pointed ladder's sticking through a tree
Toward heaven still,
And there's a barrel that I didn't fill
Beside it, and there may be two or three
Apples I didn't pick upon some bough.
But I am done with apple-picking now.
Essence of winter sleep is on the night,
The scent of apples: I am drowsing off.'''
        }
    ],
    'Maya Angelou': [
        {
            'title': 'Still I Rise',
            'content': '''You may write me down in history
With your bitter, twisted lies,
You may trod me in the very dirt
But still, like dust, I'll rise.
Does my sassiness upset you?
Why are you beset with gloom?
'Cause I walk like I've got oil wells
Pumping in my living room.
Just like moons and like suns,
With the certainty of tides,
Just like hopes springing high,
Still I'll rise.'''
        },
        {
            'title': 'Phenomenal Woman',
            'content': '''Pretty women wonder where my secret lies.
I'm not cute or built to suit a fashion model's size
But when I start to tell them,
They think I'm telling lies.
I say,
It's in the reach of my arms,
The span of my hips,
The stride of my step,
The curl of my lips.
I'm a woman
Phenomenally.
Phenomenal woman,
That's me.'''
        },
        {
            'title': 'Caged Bird',
            'content': '''A free bird leaps
on the back of the wind
and floats downstream
till the current ends
and dips his wing
in the orange sun rays
and dares to claim the sky.
But a bird that stalks
down his narrow cage
can seldom see through
his bars of rage
his wings are clipped and
his feet are tied
so he opens his throat to sing.'''
        },
        {
            'title': 'Alone',
            'category': 'solitude',
            'mood': 'reflective',
            'theme': 'isolation',
            'content': '''Lying, thinking
Last night
How to find my soul a home
Where water is not thirsty
And bread loaf is not stone
I came up with one thing
And I don't believe I'm wrong
That nobody,
But nobody
Can make it out here alone.'''
        },
        {
            'title': 'Human Family',
            'content': '''I note the obvious differences
in the human family.
Some of us are serious,
some thrive on comedy.
Some declare their lives are lived
as true profundity,
and others claim they really live
the real reality.
The variety of our skin tones
can confuse, bemuse, delight,
brown and pink and beige and purple,
tan and blue and white.'''
        },
        {
            'title': 'On the Pulse of Morning',
            'content': '''A Rock, A River, A Tree
Hosts to species long since departed,
Marked the mastodon,
The dinosaur, who left dried tokens
Of their sojourn here
On our planet floor,
Any broad alarm of their hastening doom
Is lost in the gloom of dust and ages.'''
        },
        {
            'title': 'Life Doesn\'t Frighten Me',
            'content': '''Shadows on the wall
Noises down the hall
Life doesn't frighten me at all
Bad dogs barking loud
Big ghosts in a cloud
Life doesn't frighten me at all
Mean old Mother Goose
Lions on the loose
They don't frighten me at all.'''
        },
        {
            'title': 'A Brave and Startling Truth',
            'content': '''We, this people, on a small and lonely planet
Traveling through casual space
Past aloof stars, across the way of indifferent suns
To a destination where all signs tell us
It is possible and imperative that we learn
A brave and startling truth.'''
        },
        {
            'title': 'Weekend Glory',
            'content': '''Some clichty folks
don't know the facts,
posin' and preenin'
and puttin' on acts,
stretchin' their necks
and strainin' their backs.
They move into condos
up over the ranks,
pawn their souls
to the local banks.'''
        },
        {
            'title': 'When I Think About Myself',
            'content': '''When I think about myself,
I almost laugh myself to death,
My life has been one great big joke,
A dance that's walked
A song that's spoke,
I laugh so hard I almost choke
When I think about myself.'''
        }
    ],
    'Langston Hughes': [
        {
            'title': 'Dreams',
            'content': '''Hold fast to dreams
For if dreams die
Life is a broken-winged bird
That cannot fly.
Hold fast to dreams
For when dreams go
Life is a barren field
Frozen with snow.'''
        },
        {
            'title': 'Harlem',
            'content': '''What happens to a dream deferred?
Does it dry up
like a raisin in the sun?
Or fester like a sore—
And then run?
Does it stink like rotten meat?
Or crust and sugar over—
like a syrupy sweet?
Maybe it just sags
like a heavy load.
Or does it explode?'''
        },
        {
            'title': 'I, Too',
            'content': '''I, too, sing America.
I am the darker brother.
They send me to eat in the kitchen
When company comes,
But I laugh,
And eat well,
And grow strong.
Tomorrow,
I'll be at the table
When company comes.
Nobody'll dare
Say to me,
"Eat in the kitchen,"
Then.'''
        },
        {
            'title': 'The Negro Speaks of Rivers',
            'content': '''I've known rivers:
I've known rivers ancient as the world and older than the flow of human blood in human veins.
My soul has grown deep like the rivers.
I bathed in the Euphrates when dawns were young.
I built my hut near the Congo and it lulled me to sleep.
I looked upon the Nile and raised the pyramids above it.
I heard the singing of the Mississippi when Abe Lincoln went down to New Orleans, and I've seen its muddy bosom turn all golden in the sunset.
I've known rivers:
Ancient, dusky rivers.
My soul has grown deep like the rivers.'''
        },
        {
            'title': 'Mother to Son',
            'content': '''Well, son, I'll tell you:
Life for me ain't been no crystal stair.
It's had tacks in it,
And splinters,
And boards torn up,
And places with no carpet on the floor—
Bare.
But all the time
I'se been a-climbin' on,
And reachin' landin's,
And turnin' corners,
And sometimes goin' in the dark
Where there ain't been no light.'''
        },
        {
            'title': 'Theme for English B',
            'content': '''The instructor said,
Go home and write
a page tonight.
And let that page come out of you—
Then, it will be true.
I wonder if it's that simple?
I am twenty-two, colored, born in Winston-Salem.
I went to school there, then Durham, then here
to this college on the hill above Harlem.'''
        },
        {
            'title': 'Let America Be America Again',
            'content': '''Let America be America again.
Let it be the dream it used to be.
Let it be the pioneer on the plain
Seeking a home where he himself is free.
(America never was America to me.)
Let America be the dream the dreamers dreamed—
Let it be that great strong land of love
Where never kings connive nor tyrants scheme
That any man be crushed by one above.'''
        },
        {
            'title': 'As I Grew Older',
            'content': '''It was a long time ago.
I have almost forgotten my dream.
But it was there then,
In front of me,
Bright like a sun—
My dream.
And then the wall rose,
Rose slowly,
Slowly,
Between me and my dream.
Rose until it touched the sky—
The wall.'''
        },
        {
            'title': 'Life is Fine',
            'content': '''I went down to the river,
I set down on the bank.
I tried to think but couldn't,
So I jumped in and sank.
I came up once and hollered!
I came up twice and cried!
If that water hadn't a-been so cold
I might've sunk and died.'''
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
            'title': 'أفاعل بي فعال الموكس الزاري',
            'category': 'satire',
            'mood': 'contemplative',
            'theme': 'reflection',
            'content': '''أفاعِلٌ بي فعالَ الموكِسِ الزاري
ونحنُ نُسألُ فيما كان من عارِ
قُل لي بحُرمَةِ من ضيَّعتَ حُرمَتَهُ
أكان قدرَكَ ذا أم كان مقداري
لا عشتُ إن رضيَت نفسي ولا رَكِبَت
رجلٌ سعَيتُ بها في مثلِ دينارِ
وَليُّكَ اللَهُ لِمْ صيَّرتَني مَثَلاً
كالمُستَجيرِ من الرمضاءِ بالنارِ''',
            'translation': '''Do you act upon me as the coward acts
While we are questioned about what was shameful
Tell me by the sanctity of one whose sanctity you wasted
Was this your worth or was it my measure
I shall not live if my soul is pleased, nor shall I ride
A man I sought with her for the like of a dinar
Your guardian is God, why did you make me an example
Like one seeking refuge from burning heat in fire'''
        },
        {
            'title': 'ذي الأرض عما أتاها الأمس غانية',
            'category': 'nature',
            'mood': 'peaceful',
            'theme': 'beauty',
            'content': '''ذي الأرضُ عمّا أتاها الأمسَ غانِيَةٌ
وغيرُها كان محتاجاً إلى المَطَرِ
شقَّ النباتَ عنِ البتسانِ ريِّقُهُمُ
حَيّياً جارَهُ الميدانَ بالشجرِ
كأنَّما مُطِرَت فيه صوالجةٌ
تُطَرِّحُ السدرَ فيه موضِعَ الأُكَرِ''',
            'translation': '''This earth, what came to it yesterday was beautiful
While others were in need of rain
The plants split from the gardens, their saliva
Greeting their neighbor the field with trees
As if maces rained upon it
Throwing the lotus trees in place of the hills'''
        },
        {
            'title': 'من الشوق والوجد المبرح أنني',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''منَ الشوقِ والوجدِ المُبَرِّحِ أنَّني
يُمَثَّلُ لي من بعدِ لُقياكَ لُقياكا
سأسلوا لَذيذَ العيشِ بعدك دائماً
وأنسى حياةَ النفسِ من قبلِ أنساكا''',
            'translation': '''From longing and tormenting passion that
Your meeting is imagined to me after meeting you
I shall forget the sweetness of life after you forever
And forget the life of the soul before I forget you'''
        },
        {
            'title': 'هينا فقدت من الرجال بليدا',
            'category': 'satire',
            'mood': 'contemplative',
            'theme': 'reflection',
            'content': '''هيناً فقدتُ من الرجال بليدا
من كان عندَ وجوده مَفقودا
غلَبَ التبَسُّمُ يومَ ماتَ تفجُّعي
وغدا به رأي الحمامِ سديدا
يا صاحبَ الجَدَثِ الذي شمَلَ البرييةَ جودُهُ لو كان لؤمُكَ جودا
قد كنتَ أنتَنَ منه يوم دخولهِ
ريحاً وأكثرَ في الحياة صديدا''',
            'translation': '''Easily I lost from men a dull one
Who was lost even when present
Smiling overcame my grief the day he died
And death's judgment became sound
O owner of the grave whose generosity encompassed creation
If only your meanness were generosity
You were more putrid than it on the day of entering it
In scent and more festering in life'''
        },
        {
            'title': 'أرى الشطرنج لو كانت رجالا',
            'category': 'war',
            'mood': 'intense',
            'theme': 'conflict',
            'content': '''أرى الشطرنج لو كانت رجالا
تهزُّ صفائحاً وقناً طِوالا
لغادرت الثواكل معولاتٍ
بساحتنا وأطولت القتالا
ولكني أرى خشباً ضعيفاً
إذا شهد الوغى لم يَدع آلا
ولم يُصدِرن حُمراً كُنَّ بيضاً
ولم يغشين من موت ظلالا
فلو كنا نحارب مثل هذا
لباقينا مع الدهر الجبالا''',
            'translation': '''I see chess, if its pieces were men
Shaking shields and long spears
It would leave the bereaved wailing
In our courtyard and prolong the battle
But I see weak wood
When it witnesses war, it leaves no trace
It does not return red what was white
Nor does it cover with shadows of death
If we fought like this
We would remain with time like mountains'''
        },
        {
            'title': 'أريك الرضا لو أخفت النفس خافيا',
            'category': 'satire',
            'mood': 'contemplative',
            'theme': 'reflection',
            'content': '''أُريكَ الرِضا لَو أَخفَتِ النَفسُ خافِيا
وَما أَنا عَن نَفسي وَلا عَنكَ راضِيا
أَمَيناً وَإِخلافاً وَغَدراً وَخِسَّةً
وَجُبناً أَشَخصاً لُحتَ لي أَم مَخازِيا
تَظُنُّ اِبتِساماتي رَجاءً وَغِبطَةً
وَما أَنا إِلّا ضاحِكٌ مِن رَجائِيا''',
            'translation': '''I show you contentment if the soul hid what is hidden
But I am neither pleased with myself nor with you
Trustworthiness and betrayal, treachery and baseness
And cowardice - are these persons you showed me or disgraces?
You think my smiles are hope and joy
But I am only laughing at my hopes'''
        },
        {
            'title': 'أحق دار بأن تسمى مباركة',
            'category': 'praise',
            'mood': 'contemplative',
            'theme': 'reflection',
            'content': '''أَحَقُّ دارٍ بِأَن تُسمى مُبارَكَةً
دارٌ مُبارَكَةُ المَلكِ الَّذي فيها
وَأَجدَرُ الدورِ أَن تُسقى بِساكِنِها
دارٌ غَدا الناسُ يَستَسقونَ أَهليها
هَذي مَنازِلُكَ الأُخرى نُهَنِّئُها
فَمَن يَمُرُّ عَلى الأولى يُسَلّيها''',
            'translation': '''Most deserving house to be called blessed
Is a house blessed by the king who is in it
And most worthy of houses to be watered by its inhabitant
Is a house whose people others seek rain from
These are your other dwellings we congratulate
Whoever passes by the first ones consoles them'''
        },
        {
            'title': 'أنا منك بين فضائل ومكارم',
            'category': 'praise',
            'mood': 'contemplative',
            'theme': 'reflection',
            'content': '''أَنا مِنكَ بَينَ فَضائِلٍ وَمَكارِمٍ
وَمِنِ اِرتِياحِكَ في غَمامٍ دائِمِ
وَمِنِ اِحتِقارِكَ كُلَّ ما تَحبو بِهِ
فيما أُلاحِظُهُ بِعَينَي حالِمِ
إِنَّ الخَليفَةَ لَم يُسَمِّكَ سَيفَها
حَتّى بَلاكَ فَكُنتَ عَينَ الصارِمِ''',
            'translation': '''I am from you among virtues and noble deeds
And from your comfort in perpetual clouds
And from your disdain for all you bestow
In what I observe with a dreamer's eyes
The Caliph did not name you his sword
Until he tested you and you became the eye of the blade'''
        },
        {
            'title': 'أما ترى ما أراه أيها الملك',
            'category': 'praise',
            'mood': 'contemplative',
            'theme': 'reflection',
            'content': '''أَما تَرى ما أَراهُ أَيُّها المَلِكُ
كَأَنَّنا في سَماءِ مالَها حُبُكُ
الفَرقَدُ اِبنُكَ وَالمِصباحُ صاحِبُهُ
وَأَنتَ بَدرُ الدُجى وَالمَجلِسُ الفَلَكُ''',
            'translation': '''Do you not see what I see, O King
As if we are in a sky that has no texture
The Pole Star is your son and the lamp his companion
And you are the full moon of darkness and the assembly is the sphere'''
        },
        {
            'title': 'لام أناس أبا العشائر في',
            'category': 'praise',
            'mood': 'contemplative',
            'theme': 'reflection',
            'content': '''لامَ أُناسٌ أَبا العَشائِرِ في
جودِ يَدَيهِ بِالعَينِ وَالوَرَقِ
وَإِنَّما قيلَ لِم خُلِقتَ كَذا
وَخالِقُ الخَلقِ خالِقُ الخُلُقِ
قالوا أَلَم تَكفِهِ سَماحَتُهُ
حَتّى بَنى بَيتَهُ عَلى الطُرُقِ''',
            'translation': '''People blamed Abu Al-Ashair for
The generosity of his hands with gold and silver
But it was only said: why were you created thus
And the Creator of creation is the Creator of character
They said: was his generosity not enough for him
That he built his house upon the roads'''
        },
        {
            'title': 'الصوم والفطر والأعياد والعصر',
            'category': 'praise',
            'mood': 'contemplative',
            'theme': 'reflection',
            'content': '''الصَومُ وَالفِطرُ وَالأَعيادُ وَالعَصرُ
مُنيرَةٌ بِكَ حَتّى الشَمسُ وَالقَمَرُ
تُري الأَهِلَّةَ وَجهاً عَمَّ نائِلُهُ
فَما يُخَصُّ بِهِ مِن دونِها البَشَرُ
ما الدَهرُ عِندَكَ إِلّا رَوضَةٌ أُنُفٌ
يا مَن شَمائِلُهُ في دَهرِهِ زَهَرُ''',
            'translation': '''Fasting and breaking fast, holidays and afternoon
Are illuminated by you, even the sun and moon
You show the crescents a face whose bounty is general
So humans are not specially favored over them
Time to you is nothing but a fragrant garden
O you whose qualities in his time are flowers'''
        },
        {
            'title': 'بكتب الأنام كتاب ورد',
            'category': 'praise',
            'mood': 'contemplative',
            'theme': 'reflection',
            'content': '''بِكُتبِ الأَنامِ كِتابٌ وَرَد
فَدَت يَدَ كاتِبِهِ كُلُّ يَدِ
يُعَبِّرُ عَمّا لَهُ عِندَنا
وَيَذكُرُ مِن شَوقِهِ ما نَجِد
فَأَخرَقَ رائِيَهُ ما رَأى
وَأَبرَقَ ناقِدَهُ ما اِنتَقَد''',
            'translation': '''Among the books of people came a book
May every hand ransom the hand of its writer
It expresses what he has with us
And mentions of his longing what we find
It amazed its reader with what he saw
And dazzled its critic with what he criticized'''
        },
        {
            'title': 'وطائرة تتبعها المنايا',
            'category': 'war',
            'mood': 'intense',
            'theme': 'conflict',
            'content': '''وَطائِرَةٍ تَتَبَّعُها المَنايا
عَلى آثارِها زَجِلُ الجَناحِ
كَأَنَّ الريشَ مِنهُ في سِهامٍ
عَلى جَسَدٍ تَجَسَّمَ مِن رِياحِ
كَأَنَّ رُؤوسَ أَقلامٍ غِلاظٍ
مُسِحنَ بِريشِ جُؤجُؤَةِ الصِحاحِ''',
            'translation': '''And a bird that deaths follow
In its tracks with swift wing
As if its feathers were in arrows
Upon a body embodied from winds
As if thick pen heads
Were wiped with the feathers of a sound breast'''
        },
        {
            'title': 'واحر قلباه ممن قلبه شبم',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''وَاحَـرّ قَلْبـاهُ مـمّنْ قَلْبُـهُ شَبِـمُ
وَمَنْ بجِسْمـي وَحالي عِنـدَهُ سَقَـمُ
ما لي أُكَتِّمُ حُبًّا قَدْ بَـرَى جَسَـدي
وَتَدّعي حُبّ سَيفِ الدّوْلـةِ الأُمَـمُ
إنْ كَـانَ يَجْمَعُنَـا حُـبٌّ لِغُرّتِـهِ
فَلَيْتَ أنّـا بِقَـدْرِ الحُـبّ نَقْتَسِـمُ''',
            'translation': '''How burning is my heart for one whose heart is cold
And my body and condition are sickness to him
Why do I conceal a love that has worn away my body
While nations claim to love Sayf al-Dawla
If love for his noble face unites us
Would that we could divide according to the measure of love'''
        },
        {
            'title': 'بم التعلل لا أهل ولا وطن',
            'category': 'wisdom',
            'mood': 'thoughtful',
            'theme': 'knowledge',
            'content': '''بِمَ التَعَلُّلُ لا أَهلٌ وَلا وَطَنُ
وَلا نَديمٌ وَلا كَأسٌ وَلا سَكَنُ
أُريدُ مِن زَمَني ذا أَن يُبَلِّغَني
ما لَيسَ يَبلُغُهُ مِن نَفسِهِ الزَمَنُ
لا تَلقَ دَهرَكَ إِلّا غَيرَ مُكتَرِثٍ
مادامَ يَصحَبُ فيهِ روحَكَ البَدَنُ''',
            'translation': '''With what consolation - no family and no homeland
No companion, no cup, and no dwelling
I want from my time to deliver me
What time cannot deliver from itself
Do not meet your fate except unconcerned
As long as the soul accompanies your body in it'''
        }
    ]
    'قيس بن الملوح': [
        {
            'title': 'لو كان لي قلبان',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''لو كانَ لي قلبان لعشت بواحدٍ
وأفردتُ قلباً في هواكَ يُعذَّبُ
لكنَّ لي قلباً تّمَلكَهُ الهَوى
لا العَيشُ يحلُو لَهُ ولا الموتُ يَقْرَبُ
كَعُصفُورةٍ في كفِّ طفلٍ يُهِينُها
تُعَانِي عَذابَ المَوتِ والطِفلُ يلعبُ
فلا الطفل ذو عقلٍ يرِقُّ لِحالِها
ولا الطّيرُ مَطلُوقُ الجنَاحَينِ فيذهبُ''',
            'translation': '''If I had two hearts, I would live with one
And dedicate a heart to suffer in your love
But I have one heart that passion has possessed
Neither sweet life pleases it, nor does death approach
Like a little bird in a child's hand who mistreats it
It suffers the torment of death while the child plays
The child has no mind to pity its condition
Nor is the bird free-winged to fly away'''
        },
        {
            'title': 'فواكبدا من حب من لا يحبني',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''فَواكَبِدا مِن حُبِّ مَن لا يَحُبُّني
وَمِن زَفَراتٍ ما لَهُنَّ فَناءُ
أَرَيتِكِ إِن لَم أُعطِكَ الحُبَّ عَن يَدِ
وَلَم يَكُ عِندي إِذ أَبَيتِ إِباءُ
أَتارِكَتي لِلمَوتُ إِنّي لَمَيِّتٌ
وَما لِلنُفوسِ الهالِكاتِ بَقاءُ''',
            'translation': '''Oh my liver aches from loving one who loves me not
And from sighs that have no end
Do you see if I don't give you love willingly
And I had no refusal when you refused
Will you leave me to death? I am dying
And perishing souls have no survival'''
        },
        {
            'title': 'إذ هي أمست منبت الربع دونها',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''إِذ هِيَ أَمسَت مَنبِتُ الرَبعِ دونَها
وَدونَكِ أَرطىً مُسهِلٌ وَأَلاءُ
فَلا وَصلَ إِلّا أَن يُقارِبَ بَينَنا
قَلائِصُ في أَذنابِهِنَّ صَفاءُ
يَجُبنَ بِنا عُرضَ الفَلاةِ وَما لَنا
عَليهِنَّ إِلّا وَحدَهُنَّ شِفاءُ''',
            'translation': '''When she became the dwelling place beyond her
And beyond you are tamarisk and desert shrubs
No union except that camels bring us together
She-camels with purity in their tails
They cross with us the width of the desert
And we have no cure upon them except them alone'''
        },
        {
            'title': 'وقالوا لو تشاء سلوت عنها',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''وقالوا لَو تَشاءُ سَلَوتَ عَنها
فَقُلتَ لَهُم فَإِنّي لا أَشاءُ
وَكَيفَ وَحُبُّها عَلِقٌ بِقَلبي
كَما عَلِقَت بِأَرشِيَةٍ دِلاءُ
لَها حُبٌّ تَنَشَّأَ في فُؤادي
فَلَيسَ لَهُ وَإِن زُجِرَ اِنتِهاءُ''',
            'translation': '''They said if you wish, you could forget her
I said to them: I do not wish to
How can I, when her love clings to my heart
Like buckets clinging to well-ropes
She has a love that grew in my heart
It has no end even if rebuked'''
        },
        {
            'title': 'أمن أجل خيمات على مدرج الصبا',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''أَمِن أَجلِ خَيماتٍ عَلى مَدرَجِ الصَبا
بِجَرعاءَ تَعفوها الصَبا وَالجَنائِبُ
أَلا قاتَلَ اللَهُ الرَكائِبَ إِنَّما
تُفَرِّقُ بَينَ العاشِقينَ الرَكائِبُ
بَكَرنَ بُكوراً وَاِجتَمَعنَ لِمَوعِدٍ
وَسارَ بِقَلبي بَينَهُنَّ النَجائِبُ''',
            'translation': '''Is it for tents on the path of youth
In a valley that morning winds and south winds erase
May God curse the mounts, for indeed
The mounts separate between lovers
They departed early and gathered for an appointment
And the noble camels traveled with my heart among them'''
        },
        {
            'title': 'يقولون لي يوما وقد جئت حيهم',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''يَقولونَ لي يَوماً وَقَد جِئتُ حَيَّهُم
وَفي باطِني نارٌ يُشَبُّ لَهيبُها
أَما تَختَشي مِن أُسدِنا فَأَجَبتُهُم
هَوى كُلَّ نَفسٍ أَينَ حَلَّ حَبيبُها''',
            'translation': '''They say to me one day when I came to their tribe
While in my heart burns a fire whose flame is kindled
Do you not fear our lions? I answered them:
Every soul's passion is where its beloved dwells'''
        },
        {
            'title': 'أصور صورة في التراب منها',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''أُصَوِّرُ صورَةً في التُربِ مِنها
وَأَبكي إِنَّ قَلبي في عَذابِ
وَأَشكو هَجرَها مِنها إِلَيها
شِكايَةَ مُدنِفٍ عَظِمِ المُصابِ
وَأَشكو ما لَقيتُ وَكُلَّ وَجدٍ
غَراماً بِالشِكايَةِ لِلتُرابِ''',
            'translation': '''I draw her image in the dust
And weep for my heart is in torment
I complain of her abandonment from her to her
The complaint of one gravely afflicted
I complain what I met and every passion
Lovingly complaining to the dust'''
        },
        {
            'title': 'عفا الله عن ليلى وإن سفكت دمي',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''عَفا اللَهُ عَن لَيلى وَإِن سَفَكَت دَمي
فَإِنّي وَإِن لَم تَحزِني غَيرُ عاتِبِ
عَلَيها وَلا مُبدٍ لِلَيلى شِكايَةً
وَقَد يَشتَكي المُشكى إِلى كُلَّ صاحِبِ
يَقولونَ تُب عَن ذِكرِ لَيلى وَحُبِّها
وَما خَلِدي عَن حُبِّ لَيلى بِتائِبِ''',
            'translation': '''May God forgive Layla even if she shed my blood
For I, even if you don't grieve me, am not reproachful
Towards her, nor showing Layla any complaint
Though the complainant may complain to every companion
They say repent from mentioning Layla and her love
But my heart from Layla's love is not repentant'''
        },
        {
            'title': 'أحبك يا ليلى وأفرط في حبي',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''أُحُبُّكِ يا لَيلى وَأُفرِطُ في حُبّي
وَتُبدينَ لي هَجراً عَلى البُعدِ وَالقُربِ
وَأَهواكِ يا لَيلى هَوىً لَو تَنَسَّمَت
نُفوسُ الوَرى أَدناهُ صِحنَ مِنَ الكَربِ
شَكَوتُ إِلَيها الشَوقُ سِرّاً وَجَهرَةً
وَبُحتُ بِما أَلقاهُ مِن شِدَّةِ الحُبِّ''',
            'translation': '''I love you O Layla and exceed in my love
While you show me abandonment in distance and nearness
I desire you O Layla with a desire that if
The souls of people breathed its least, they would cry from distress
I complained to her of longing secretly and openly
And revealed what I suffer from the intensity of love'''
        },
        {
            'title': 'وأحببتها حبا يقر بعينها',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''وَأَحبَبتُها حُبّاً يَقَرُّ بِعَينِها
وَحُبّي إِذا أَحبَبتُ لا يُشبِهُ الحُبّا
وَلَو تَفَلَت في البَحرِ وَالبَحرُ مالِحٌ
لَأَصبَحَ ماءُ البَحرِ مِن ريقِها عَذبا''',
            'translation': '''I loved her with a love that delights her eye
And my love when I love is unlike any love
If she spat in the sea while the sea is salty
The sea water would become sweet from her saliva'''
        },
        {
            'title': 'ألا قاتل الله الهوى ما أشده',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''أَلا قاتَلَ اللَهُ الهَوى ما أَشَدَّهُ
وَأَسرَعَهُ لِلمَرءِ وَهوَ جَليدُ
دَعاني الهَوى مِن نَحوِها فَأَجَبتُهُ
فَأَصبَحَ بي يَستَنُّ حَيثُ يُريدُ''',
            'translation': '''May God curse passion, how intense it is
And how swift it is to man while he is steadfast
Passion called me from her direction so I answered it
And it became leading me wherever it wishes'''
        },
        {
            'title': 'ولما تلاقينا على سفح رامة',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''ولما تلاقينا على سفح رامة
وجدتُ بنان العامرية أحمرا
فقلت خضبت الكف بعد فراقنا؟
فقالت معاذ الله ذلك ما جرى
ولكنني لما رأيتك راحلاً
بكيت دماً حتى بللت به الثرى
مسحت بأطراف البنان مدامعي
فصار خضاباً بالأكف كما ترى''',
            'translation': '''When we met on the slope of Ramah
I found the fingers of Al-Amiriya red
I said: Did you henna your hands after our separation?
She said: God forbid, that did not happen
But when I saw you departing
I wept blood until I moistened the earth with it
I wiped my tears with my fingertips
So it became henna on the palms as you see'''
        },
        {
            'title': 'فوالله ما أبكي على يوم ميتتي',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''فَوَاللَهِ ما أَبكي عَلى يَومِ ميتَتي
وَلَكِنَّني مِن وَشكِ بَينِكِ أَجزَعُ
فَصَبراً لِأَمرِ اللَهِ إِن حانَ يَومُنا
فَلَيسَ لِأَمرٍ حَمَّهُ اللَهُ مَدفَعُ''',
            'translation': '''By God, I do not weep for the day of my death
But I am terrified of the nearness of separation from you
So patience for God's command if our day comes
For there is no preventing what God has decreed'''
        },
        {
            'title': 'أيا مهديا نفي الحبيب صبيحة',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''أَيا مُهدِياً نَفيَ الحَبيبِ صَبيحَةً
بِمَن وَإِلى مَن جِئتُما تَشِيانِ
بِمَن لَو أَراهُ عانِياً لَفَدَيتُهُ
وَمَن لَو رَآني عانِياً لَفَدانِ
فَمَن مُبلِغٌ عَنّي الحَبيبَ رِسالَةً
بِأَنَّ فُؤادي دائِمُ الخَفَقانِ''',
            'translation': '''O you who brought news of the beloved's exile at dawn
With whom and to whom did you two come walking
With one whom if I saw him captive I would ransom him
And who if he saw me captive would ransom me
Who will convey from me to the beloved a message
That my heart is in constant palpitation'''
        },
        {
            'title': 'لقد طفت سبعا قلت لما قضيتها',
            'category': 'love',
            'mood': 'romantic',
            'theme': 'passion',
            'content': '''لَقَد طُفتُ سَبعاً قُلتُ لَمّا قَضَيتُها
أَلا لَيتَ هَذا لا عَلَيَّ وَلا لِيا
يُسائِلُني صَحبي فَما أَعقَلُ الَّذي
يَقولونَ مِن ذِكرٍ لِلَيلى اِعتَرانِيا
إِذا جِئتَ بابَ الشِعبِ شِعبَ اِبنِ عامِرٍ
فَأَقرِ غَزالَ الشِعبِ مِنّي سَلامِيا''',
            'translation': '''I circumambulated seven times, when I finished I said
Would that this were neither for me nor against me
My companions ask me but I cannot comprehend what
They say about mentioning Layla that came over me
When you come to the gate of the valley, Ibn Amer's valley
Give the gazelle of the valley my greetings'''
        }
    ]
}
