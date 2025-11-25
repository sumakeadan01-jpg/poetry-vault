# 📖 Poetry Vault

A beautiful web application for discovering, sharing, and saving classic poetry. Built with Flask and featuring 103+ classic poems from legendary poets.

## ✨ Features

- 📚 Browse 103 classic poems from 10 legendary poets
- 🔍 Search poems by title, content, or poet
- 📂 Filter by 35+ categories (Love, Nature, Spirituality, etc.)
- 💾 Save your favorite poems
- 💬 Comment on poems
- ❤️ Like poems
- 👤 User profiles and authentication
- 🔔 Notifications for interactions
- 👑 Admin panel for content management

## 🎭 Featured Poets

- William Shakespeare
- Rumi
- Emily Dickinson
- Edgar Allan Poe
- Walt Whitman
- Lord Byron
- William Wordsworth
- John Keats
- Percy Shelley
- Robert Burns

## 🚀 Quick Start (Local Development)

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

5. Seed the database with classic poems
```bash
python seed_poems.py
```

6. Visit http://localhost:5000

## 🌐 Deploy to Production

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions on deploying to:
- Render.com (Recommended - Free)
- Railway.app
- PythonAnywhere

## 📁 Project Structure

```
JJ_PoetryApp0.1/
├── app.py              # Main application file
├── models.py           # Database models
├── config.py           # Configuration
├── seed_poems.py       # Database seeding script
├── requirements.txt    # Python dependencies
├── Procfile           # Deployment configuration
├── templates/         # HTML templates
├── static/           # Static files (images, CSS)
└── instance/         # Database (created on first run)
```

## 🎨 Categories

Poems are organized into 35+ categories including:
- Love (24 poems)
- Nature (13 poems)
- Spirituality (8 poems)
- Death, Life, Melancholy, Beauty, and more!

See [POEM_CATEGORIES.md](POEM_CATEGORIES.md) for complete breakdown.

## 🔐 Environment Variables

For production deployment, set these environment variables:

```
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url (optional, defaults to SQLite)
OPENAI_API_KEY=your-api-key (if using AI features)
```

## 🛠️ Tech Stack

- **Backend**: Flask, SQLAlchemy
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Authentication**: Flask-Login
- **Deployment**: Gunicorn

## 📝 License

This project contains public domain poetry. The application code is available for educational purposes.

## 🤝 Contributing

Feel free to fork, improve, and submit pull requests!

## 📧 Contact

Created with ❤️ for poetry lovers everywhere.
