# Poetry Vault

A modern web application for poetry enthusiasts to discover, share, and connect through poetry. Built with Flask and PostgreSQL, featuring classic literature and user-generated content.

## Features

- **Poetry Collection**: Browse classic works from Shakespeare, Rumi, Emily Dickinson, and other renowned poets
- **User Content**: Create, edit, and share original poetry with categorization and tagging
- **Social Features**: Follow users, like and comment on poems, create collections
- **Search & Discovery**: Advanced filtering by poet, mood, theme, and category
- **Security**: Rate limiting, content validation, and privacy controls
- **Admin Dashboard**: User management, analytics, and content moderation

## Quick Start

### Local Development

```bash
# Clone and setup
git clone <repository-url>
cd poetry-vault
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies and run
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000`

### Railway Deployment

1. Connect your GitHub repository to Railway
2. Add PostgreSQL database service
3. Set environment variables:
   ```
   SECRET_KEY=your-secret-key
   FLASK_ENV=production
   ```
4. Deploy automatically

## Project Structure

```
├── app.py                    # Main Flask application
├── models.py                 # Database models
├── config.py                 # Configuration
├── security_middleware.py    # Security features
├── analytics.py              # User analytics
├── seed_poems.py            # Classic poetry data
├── templates/               # HTML templates
├── static/                  # CSS, JS, images
└── requirements.txt         # Dependencies
```

## Administration

Create an admin account by registering with the prefix `P## (e.g., `P##admin`). Access the admin panel at to manage users, content, and view analytics. 
p## has a secret number for only one admin.

## Technology Stack

- **Backend**: Flask, SQLAlchemy
- **Database**: PostgreSQL (production), SQLite (development)
- **Security**: Flask-Login, custom middleware
- **Deployment**: Railway, Gunicorn
- **Frontend**: HTML, CSS, JavaScript

## License

MIT License