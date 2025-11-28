"""
Additional 50 poems per poet (except Emily Dickinson and Majnun Layla)
To be added to seed_poems.py
"""

ADDITIONAL_POEMS = {
    'Shakespeare': [
        # 50 new poems
        {
            'title': 'Sonnet 1: From Fairest Creatures',
            'category': 'beauty',
            'content': '''From fairest creatures we desire increase,
That thereby beauty's rose might never die,
But as the riper should by time decease,
His tender heir might bear his memory:
But thou contracted to thine own bright eyes,
Feed'st thy light's flame with self-substantial fuel,
Making a famine where abundance lies,
Thy self thy foe, to thy sweet self too cruel:
Thou that art now the world's fresh ornament,
And only herald to the gaudy spring,
Within thine own bud buriest thy content,
And tender churl mak'st waste in niggarding:
Pity the world, or else this glutton be,
To eat the world's due, by the grave and thee.'''
        },
        {
            'title': 'Sonnet 2: When Forty Winters',
            'category': 'aging',
            'content': '''When forty winters shall besiege thy brow,
And dig deep trenches in thy beauty's field,
Thy youth's proud livery so gazed on now,
Will be a totter'd weed of small worth held:
Then being asked, where all thy beauty lies,
Where all the treasure of thy lusty days;
To say, within thine own deep sunken eyes,
Were an all-eating shame, and thriftless praise.
How much more praise deserv'd thy beauty's use,
If thou couldst answer 'This fair child of mine
Shall sum my count, and make my old excuse,'
Proving his beauty by succession thine!
This were to be new made when thou art old,
And see thy blood warm when thou feel'st it cold.'''
        },
        {
            'title': 'Sonnet 12: When I Do Count the Clock',
            'category': 'time',
            'content': '''When I do count the clock that tells the time,
And see the brave day sunk in hideous night;
When I behold the violet past prime,
And sable curls all silver'd o'er with white;
When lofty trees I see barren of leaves
Which erst from heat did canopy the herd,
And summer's green all girded up in sheaves
Borne on the bier with white and bristly beard,
Then of thy beauty do I question make,
That thou among the wastes of time must go,
Since sweets and beauties do themselves forsake
And die as fast as they see others grow;
And nothing 'gainst Time's scythe can make defence
Save breed, to brave him when he takes thee hence.'''
        },
        {
            'title': 'Sonnet 15: When I Consider',
            'category': 'time',
            'content': '''When I consider every thing that grows
Holds in perfection but a little moment,
That this huge stage presenteth nought but shows
Whereon the stars in secret influence comment;
When I perceive that men as plants increase,
Cheered and checked even by the self-same sky,
Vaunt in their youthful sap, at height decrease,
And wear their brave state out of memory;
Then the conceit of this inconstant stay
Sets you most rich in youth before my sight,
Where wasteful Time debateth with Decay,
To change your day of youth to sullied night;
And all in war with Time for love of you,
As he takes from you, I engraft you new.'''
        },
        {
            'title': 'Sonnet 19: Devouring Time',
            'category': 'time',
            'content': '''Devouring Time, blunt thou the lion's paws,
And make the earth devour her own sweet brood;
Pluck the keen teeth from the fierce tiger's jaws,
And burn the long-liv'd phoenix, in her blood;
Make glad and sorry seasons as thou fleet'st,
And do whate'er thou wilt, swift-footed Time,
To the wide world and all her fading sweets;
But I forbid thee one most heinous crime:
O! carve not with thy hours my love's fair brow,
Nor draw no lines there with thine antique pen;
Him in thy course untainted do allow
For beauty's pattern to succeeding men.
Yet, do thy worst old Time: despite thy wrong,
My love shall in my verse ever live young.'''
        },
        {
            'title': 'Sonnet 20: A Woman\'s Face',
            'category': 'beauty',
            'content': '''A woman's face with nature's own hand painted,
Hast thou, the master mistress of my passion;
A woman's gentle heart, but not acquainted
With shifting change, as is false women's fashion:
An eye more bright than theirs, less false in rolling,
Gilding the object whereupon it gazeth;
A man in hue all hues in his controlling,
Which steals men's eyes and women's souls amazeth.
And for a woman wert thou first created;
Till Nature, as she wrought thee, fell a-doting,
And by addition me of thee defeated,
By adding one thing to my purpose nothing.
But since she prick'd thee out for women's pleasure,
Mine be thy love and thy love's use their treasure.'''
        },
        {
            'title': 'Sonnet 23: As an Unperfect Actor',
            'category': 'love',
            'content': '''As an unperfect actor on the stage,
Who with his fear is put beside his part,
Or some fierce thing replete with too much rage,
Whose strength's abundance weakens his own heart;
So I, for fear of trust, forget to say
The perfect ceremony of love's rite,
And in mine own love's strength seem to decay,
O'ercharg'd with burthen of mine own love's might.
O! let my looks be then the eloquence
And dumb presagers of my speaking breast,
Who plead for love, and look for recompense,
More than that tongue that more hath more express'd.
O! learn to read what silent love hath writ:
To hear with eyes belongs to love's fine wit.'''
        },
        {
            'title': 'Sonnet 27: Weary with Toil',
            'category': 'longing',
            'content': '''Weary with toil, I haste me to my bed,
The dear repose for limbs with travel tired;
But then begins a journey in my head
To work my mind, when body's work's expired:
For then my thoughts—from far where I abide—
Intend a zealous pilgrimage to thee,
And keep my drooping eyelids open wide,
Looking on darkness which the blind do see:
Save that my soul's imaginary sight
Presents thy shadow to my sightless view,
Which, like a jewel hung in ghastly night,
Makes black night beauteous, and her old face new.
Lo! thus, by day my limbs, by night my mind,
For thee, and for myself, no quiet find.'''
        },
        {
            'title': 'Sonnet 29: When in Disgrace',
            'category': 'love',
            'content': '''When in disgrace with fortune and men's eyes
I all alone beweep my outcast state,
And trouble deaf heaven with my bootless cries,
And look upon myself, and curse my fate,
Wishing me like to one more rich in hope,
Featured like him, like him with friends possessed,
Desiring this man's art, and that man's scope,
With what I most enjoy contented least;
Yet in these thoughts my self almost despising,
Haply I think on thee, and then my state,
Like to the lark at break of day arising
From sullen earth, sings hymns at heaven's gate;
For thy sweet love remembered such wealth brings
That then I scorn to change my state with kings.'''
        },
        {
            'title': 'Sonnet 30: When to the Sessions',
            'category': 'memory',
            'content': '''When to the sessions of sweet silent thought
I summon up remembrance of things past,
I sigh the lack of many a thing I sought,
And with old woes new wail my dear time's waste:
Then can I drown an eye, unused to flow,
For precious friends hid in death's dateless night,
And weep afresh love's long since cancell'd woe,
And moan the expense of many a vanish'd sight:
Then can I grieve at grievances foregone,
And heavily from woe to woe tell o'er
The sad account of fore-bemoaned moan,
Which I new pay as if not paid before.
But if the while I think on thee, dear friend,
All losses are restor'd and sorrows end.'''
        },
