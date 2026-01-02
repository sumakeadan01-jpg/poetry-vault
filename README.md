# Poetry Vault

A beautiful web application for discovering, sharing, and saving classic poetry. Built with Flask and featuring 228+ classic poems from 15 legendary poets.

## Features

- Browse 228+ classic poems from 15 legendary poets
- Search poems by title, content, or poet
- Filter by 35+ categories (Love, Nature, Spirituality, etc.)
- Save your favorite poems
- Comment on poems
- Like poems
- Follow other poets
- User profiles and authentication
- Notifications for interactions
- Admin panel with analytics
- Instagram visitor tracking
- AI chatbot with classic poets

## Featured Poets

### English Poets
- William Shakespeare
- Emily Dickinson (44 poems)
- Edgar Allan Poe
- Walt Whitman
- Lord Byron
- William Wordsworth
- John Keats
- Percy Shelley
- Robert Burns
- Robert Frost
- Maya Angelou
- Langston Hughes
- Rumi

### Arabic Poets
- المتنبي (Al-Mutanabbi)
- قيس بن الملوح (Majnun Layla) - 49 poems

---

## Quick Start (Local Development)

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository
```bash
git clone <your-repo-url>
cd JJ_PoetryApp0.1
```

2. Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
python app.py
```

5. Visit http://localhost:5000

The database will auto-seed with classic poems on first run!

### Development with Auto-Backup
```bash
python run_app.py
```
This runs the app on port 5001 with automatic backups every 6 hours.

---

## Deploy to Production

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions on deploying to:
- Render.com (Recommended - Free)
- Railway.app
- PythonAnywhere

---

## Project Structure

```
JJ_PoetryApp0.1/
├── app.py              # Main application file (1094 lines)
├── models.py           # Database models (9 models)
├── config.py           # Configuration
├── analytics.py        # Visitor tracking
├── seed_poems.py       # Initial 165 poems
├── seed_poems_part2.py # Additional 63 poems
├── requirements.txt    # Python dependencies
├── Procfile           # Deployment configuration
├── templates/         # HTML templates (20 files)
├── static/           # Static files (CSS, JS, images)
└── instance/         # Database (created on first run)
```

---

## Database Backup & Recovery

### Automatic Backups (Recommended)

Run the app with automatic backups:
```bash
source .venv/bin/activate
python run_app.py
```

This will:
- ✅ Start your Flask app on port 5001
- ✅ Automatically backup every 6 hours
- ✅ Keep the last 10 backups
- ✅ Run in the background while app is running

### Manual Backup Commands

**Create a Backup:**
```bash
python backup_db.py backup
```

**List All Backups:**
```bash
python backup_db.py list
```

**Restore from Backup:**
```bash
python backup_db.py restore poetry_app_20241125_143022.db
```

### When to Backup

**Always backup before:**
- Deploying to Render
- Making database schema changes
- Deleting the database
- Testing new features that modify data

### Backup Workflow

**Before Deploying:**
```bash
# 1. Create backup
python backup_db.py backup

# 2. Commit and push changes
git add .
git commit -m "Update: Added new features"
git push origin main
```

**If Something Goes Wrong:**
```bash
# 1. List available backups
python backup_db.py list

# 2. Restore from the backup you want
python backup_db.py restore poetry_app_20241125_143022.db
```

### Backup Storage

- **Local backups**: Stored in `instance/backups/`
- **Git backups**: Committed to GitHub (optional)
- **Render backups**: Download database from Render dashboard

### Download Database from Render

1. Go to your Render dashboard
2. Click on your web service
3. Go to "Shell" tab
4. Run: `cat instance/poetry_app.db > /tmp/backup.db`
5. Download the file

### Backup Naming Convention

Backups are automatically named with timestamps:
- Format: `poetry_app_YYYYMMDD_HHMMSS.db`
- Example: `poetry_app_20241125_143022.db`
  - Date: November 25, 2024
  - Time: 14:30:22 (2:30:22 PM)

### Best Practices

1. **Backup before every deployment**
2. **Keep at least 3-5 recent backups**
3. **Test restores occasionally**
4. **Document what changed in each backup**

---

## Instagram Visitor Tracking

### The Problem
Instagram doesn't share visitor usernames when they click links (for privacy). So we use URL parameters to track who visits.

### The Solution - Disguised Tracking Links

Use subtle parameters that look natural!

### Tracking Link Options

**Option 1: `?ref=` (Referral Code - Most Natural)**
```
https://your-app.onrender.com/?ref=sarah
https://your-app.onrender.com/?ref=mike
```
✅ Looks like a referral program
✅ Very common on websites
✅ Not suspicious at all

**Option 2: `?u=` (Short & Subtle)**
```
https://your-app.onrender.com/?u=alex
https://your-app.onrender.com/?u=emma
```
✅ Super short
✅ Could mean "user" or anything
✅ Minimal and clean

**Option 3: `?id=` (Page/Content ID)**
```
https://your-app.onrender.com/?id=john
https://your-app.onrender.com/?id=lisa
```
✅ Looks like a page identifier
✅ Very common parameter
✅ Natural looking

**All Supported Parameters:**
- `?from=name`
- `?ref=name`
- `?u=name`
- `?wist=name`
- `?id=name`

### How It Works

1. **You create custom links** for different people/posts
2. **Share them on Instagram** (bio, stories, DMs)
3. **When someone clicks**, the parameter is captured
4. **Admin panel shows** who visited with their nickname

### Real Examples

**For Your Instagram Bio:**
```
https://your-app.onrender.com/?ref=bio
```

**For Instagram Stories:**
```
https://your-app.onrender.com/?ref=story1
https://your-app.onrender.com/?ref=story2
```

**For Specific Friends (DM them):**
```
https://your-app.onrender.com/?u=sarah
https://your-app.onrender.com/?u=mike
```

**For Posts:**
```
https://your-app.onrender.com/?ref=post1
https://your-app.onrender.com/?ref=post2
```

### Pro Tips

**1. Use Short Codes:**
```
?u=SJ    (for Sarah Johnson)
?u=MK    (for Mike Kim)
?u=AL    (for Alex Lee)
```

**2. Track Post Performance:**
```
?ref=post1   (first poem post)
?ref=post2   (second poem post)
?ref=reel1   (first reel)
```

**3. Track Story Performance:**
```
?id=s1   (story 1)
?id=s2   (story 2)
?id=s3   (story 3)
```

**4. Track Different Platforms:**
```
?ref=ig      (Instagram)
?ref=fb      (Facebook)
?ref=tw      (Twitter)
```

### What You'll See in Admin Panel

**Recent Visitors Table:**
```
Nickname/Source    Source       First Visit    Last Visit    Visits
sarah              Instagram    Dec 09, 14:30  Dec 09, 15:20   5
mike               Instagram    Dec 09, 13:15  Dec 09, 13:15   1
story1             Instagram    Dec 09, 12:00  Dec 09, 16:45   12
bio                Instagram    Dec 08, 10:30  Dec 09, 17:00   43
```

Now you know:
- ✅ Who visited (sarah, mike)
- ✅ Which story performed best (story1 = 12 visits)
- ✅ How many came from bio (43 visits)
- ✅ When they visited
- ✅ How many times they came back

### Privacy Note

- The parameter is **only visible in the URL**
- Visitors can see it if they look closely
- But most people don't notice URL parameters
- It's completely safe and legal
- Many websites use this method

---

## Poem Categories

Poems are organized into **35+ categories**:

### Major Categories

**Love (24 poems)**
- Shakespeare: Sonnets 18, 29, 55, 106, 116, 130
- Rumi: The Minute I Heard My First Love Story
- Emily Dickinson: Wild Nights - Wild Nights!
- Edgar Allan Poe: Annabel Lee, To Helen
- Lord Byron: So We'll Go No More a Roving, Stanzas for Music
- John Keats: La Belle Dame sans Merci, Bright Star
- Percy Shelley: Love's Philosophy
- Robert Burns: A Red, Red Rose, John Anderson, My Jo

**Nature (13 poems)**
- Emily Dickinson: A Bird Came Down the Walk
- Walt Whitman: When I Heard the Learn'd Astronomer
- Lord Byron: The Ocean
- William Wordsworth: I Wandered Lonely as a Cloud, The World Is Too Much with Us, The Solitary Reaper, Tintern Abbey, Lines Written in Early Spring
- Robert Burns: To a Mouse
- Percy Shelley: Ode to the West Wind, To a Skylark, The Cloud

**Spirituality (8 poems)**
- Rumi: The Reed Flute's Song, Only Breath, The Guest House, Love Dogs, The Breeze at Dawn, Out Beyond Ideas, Let Yourself Be Silently Drawn, The Wound is the Place, Forget Your Life

**Death (5 poems)**
- Shakespeare: Sonnet 71
- Emily Dickinson: Because I Could Not Stop for Death, I Heard a Fly Buzz When I Died
- Edgar Allan Poe: Spirits of the Dead
- William Wordsworth: A Slumber Did My Spirit Seal

**Life (4 poems)**
- Shakespeare: All the World's a Stage
- Emily Dickinson: She rose to his requirement, Success is Counted Sweetest
- Edgar Allan Poe: The Bells

### Other Categories

- Melancholy (3 poems)
- Heartbreak (3 poems)
- Beauty (3 poems)
- Solitude (3 poems)
- War (2 poems)
- Grief (2 poems)
- Mortality (2 poems)
- Friendship (2 poems)
- Humor (2 poems)
- Patriotism (2 poems)

### Single Category Poems

- Aging, Time, Hope, Identity, Truth, Quest, Reality, Decay, Self, Celebration, Wonder, Apocalypse, Betrayal, Joy, Loss, Art, Autumn, Discovery, Winter, Memory, Change, Night, Power, Folklore

**Total: 228+ Poems across 35+ Categories**

---

## Environment Variables

For production deployment, set these environment variables:

```
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url (optional, defaults to SQLite)
```

---

## 🛠️ Tech Stack

- **Backend**: Flask, SQLAlchemy
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Authentication**: Flask-Login
- **Deployment**: Gunicorn
- **Analytics**: Custom visitor tracking
- **AI**: Ollama (local AI for chatbot)

---

## Utility Scripts

### Content Management
- `add_new_poets.py` - Add new poets without losing data
- `import_poetrydb.py` - Auto-import poems from PoetryDB API

### Database Management
- `check_database.py` - Check database contents
- `check_users.py` - List all users
- `recreate_database.py` - Recreate database from scratch

### Backup & Recovery
- `backup_db.py` - Create database backups
- `auto_backup.py` - Automatic backup system
- `restore_backup.py` - Restore from backup

### Emergency Tools
- `reset_admin_password.py` - Reset admin password
- `reset_password_now.py` - Emergency password reset

### Development
- `run_app.py` - Run app with auto-backup (port 5001)
- `run_test.py` - Run app for testing (port 5001)
- `start_with_backup.sh` - Start app with backup

---

## Additional Documentation

- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Detailed deployment instructions
- [FEATURES.md](FEATURES.md) - Complete feature list
- [HOW_TO_ADD_POETS.md](HOW_TO_ADD_POETS.md) - Guide for adding more poets
- [LEARNING_GUIDE.md](LEARNING_GUIDE.md) - Beginner's guide to the codebase
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Complete project overview

---

## License

This project contains public domain poetry. The application code is available for educational purposes.

---

## Contributing

Feel free to fork, improve, and submit pull requests!

---

## Contact

Created with ❤️ for poetry lovers everywhere.

---

## Project Stats

- **Total Poems**: 228+
- **Poets**: 15 (13 classic + real users)
- **Templates**: 20 HTML pages
- **Database Models**: 9
- **Routes**: 30+
- **Lines of Code**: 2,000+
- **Categories**: 35+

---

*Last Updated: December 9, 2024*
