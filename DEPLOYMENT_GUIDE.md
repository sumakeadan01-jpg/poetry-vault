# Poetry Vault - Deployment Guide

## Deploy to Render.com (FREE)

### Step 1: Prepare Your Code
1. Make sure all your code is committed to Git
2. Push to GitHub (create a repo if you haven't)

### Step 2: Sign Up for Render
1. Go to https://render.com
2. Sign up with your GitHub account (easiest)

### Step 3: Create a New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select your `JJ_PoetryApp0.1` repository

### Step 4: Configure the Service
Fill in these settings:

- **Name**: `poetry-vault` (or whatever you want)
- **Region**: Choose closest to you
- **Branch**: `main` (or `master`)
- **Root Directory**: Leave blank OR set to `JJ_PoetryApp0.1` if it's in a subfolder
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

### Step 5: Add Environment Variables
Click "Advanced" and add these environment variables:

```
SECRET_KEY = your-random-secret-key-here-make-it-long-and-random
DATABASE_URL = (Render will provide this if you add PostgreSQL)
OPENAI_API_KEY = your-openai-api-key (if using AI features)
```

To generate a SECRET_KEY, run in terminal:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### Step 6: Add PostgreSQL Database (Optional but Recommended)
1. In Render dashboard, click "New +" → "PostgreSQL"
2. Name it `poetry-vault-db`
3. Choose Free tier
4. Create database
5. Copy the "Internal Database URL"
6. Go back to your Web Service → Environment
7. Add/Update `DATABASE_URL` with the copied URL

### Step 7: Deploy!
1. Click "Create Web Service"
2. Wait 5-10 minutes for deployment
3. Your site will be live at: `https://poetry-vault.onrender.com` (or your chosen name)

### Step 8: Seed the Database
After first deployment, you need to run the seed script once:

**Option A: Using Render Shell**
1. Go to your service dashboard
2. Click "Shell" tab
3. Run: `python seed_poems.py`

**Option B: Add to Build Command (One-time)**
Temporarily change Build Command to:
```
pip install -r requirements.txt && python seed_poems.py
```
Then change it back after first deploy.

### Step 9: Share Your Link!
Your Poetry Vault is now live! Share the URL with friends:
`https://your-app-name.onrender.com`

---

## Alternative: Deploy to Railway.app

1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Python and deploys
6. Add environment variables in Settings
7. Get your public URL from Settings → Domains

---

## Alternative: Deploy to PythonAnywhere

1. Go to https://www.pythonanywhere.com
2. Sign up for free account
3. Upload your code via Files tab
4. Set up virtual environment
5. Configure WSGI file
6. Your site: `https://yourusername.pythonanywhere.com`

---

## Troubleshooting

**Database not found?**
- Make sure you ran `seed_poems.py` after deployment
- Check DATABASE_URL is set correctly

**500 Error?**
- Check logs in Render dashboard
- Make sure SECRET_KEY is set
- Verify all dependencies in requirements.txt

**Static files not loading?**
- Flask serves static files automatically
- Check your static folder path in templates

**Need help?**
- Check Render logs: Dashboard → Logs tab
- Common issues: missing environment variables, database not seeded
