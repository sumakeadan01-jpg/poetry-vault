# Poetry Vault - Render Deployment Guide

## 🚀 Quick Deploy to Render

### Step 1: Prepare Your Repository
1. **Push all changes to GitHub** (make sure your latest code is committed)
2. **Verify these files exist** (✅ all present):
   - `Procfile` - Contains: `web: gunicorn app:app`
   - `requirements.txt` - All dependencies listed
   - `app.py` - Main application file

### Step 2: Create Render Web Service
1. Go to [render.com](https://render.com) and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select your Poetry Vault repository

### Step 3: Configure Deployment Settings
**Basic Settings:**
- **Name**: `poetry-vault` (or your preferred name)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

### Step 4: Set Environment Variables
Click **"Advanced"** and add these environment variables:

**Required:**
```
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
FLASK_ENV=production
```

**Database (Render will provide):**
```
DATABASE_URL=postgresql://... (Render PostgreSQL URL)
```

**Optional but Recommended:**
```
SQLALCHEMY_ECHO=false
SESSION_COOKIE_SECURE=true
BACKUP_ENABLED=false
ANALYTICS_ENABLED=true
```

### Step 5: Add PostgreSQL Database
1. In Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Name it `poetry-vault-db`
3. Copy the **External Database URL**
4. Add it as `DATABASE_URL` environment variable in your web service

### Step 6: Deploy!
1. Click **"Create Web Service"**
2. Render will automatically:
   - Install dependencies
   - Run database migrations
   - Start your app
   - Provide you with a live URL

## 🔧 Post-Deployment Setup

### Initialize Database
Your app will automatically:
- Create all database tables
- Seed with classic poems if database is empty
- Set up admin user (first registered user becomes admin)

### Access Your App
- **Live URL**: `https://your-app-name.onrender.com`
- **Admin Access**: Register first account, or use admin code `P0.1` prefix

### Test New Features
1. **Collections**: Create and manage poem collections
2. **Advanced Search**: Filter by mood, theme, category
3. **Thematic Channels**: Browse poems by theme
4. **Analytics**: Premium feature (shows upgrade prompt)
5. **Mood Discovery**: Discover poems by emotional mood

## 🎯 Your Pitch Deck Features - Now Live!

✅ **Core Tools:**
- Algorithmic Poetry Feed
- Searchable Library (500+ Classics)
- Anonymous Posting
- Mood-Based Discovery
- Private Collections

✅ **Unique Differentiators:**
- Conversational AI Poets (when Ollama available)
- Advanced Search & Filtering
- Thematic Channels

✅ **Subscription Framework:**
- Free/Plus/Pro tiers in database
- Analytics restricted to paid users
- Ready for payment integration

## 🔍 Troubleshooting

**If deployment fails:**
1. Check build logs in Render dashboard
2. Verify all files are committed to GitHub
3. Ensure requirements.txt has all dependencies

**If database issues:**
1. Verify DATABASE_URL is set correctly
2. Check PostgreSQL service is running
3. Database tables auto-create on first run

**If features don't work:**
1. Check environment variables are set
2. Verify SECRET_KEY is configured
3. Look at application logs in Render

## 🎉 Success!
Your Poetry Vault app with all pitch deck features is now live on Render!

**Next Steps:**
- Share your live URL
- Test all new features
- Add payment processing for subscriptions
- Expand classic poem library
- Implement Instagram integration