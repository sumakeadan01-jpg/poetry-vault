# Database Backup Guide

## Quick Backup Commands

### Create a Backup
```bash
cd JJ_PoetryApp0.1
python backup_db.py backup
```

### List All Backups
```bash
python backup_db.py list
```

### Restore from Backup
```bash
python backup_db.py restore poetry_app_20241125_143022.db
```

## When to Backup

**Always backup before:**
- Deploying to Render
- Making database schema changes
- Deleting the database
- Testing new features that modify data

## Automatic Backup Workflow

### Before Deploying to Render:
```bash
# 1. Create backup
python backup_db.py backup

# 2. Commit and push changes
git add .
git commit -m "Update: Added new features"
git push origin main
```

### If Something Goes Wrong:
```bash
# 1. List available backups
python backup_db.py list

# 2. Restore from the backup you want
python backup_db.py restore poetry_app_20241125_143022.db
```

## Backup Storage

- **Local backups**: Stored in `instance/backups/`
- **Git backups**: Committed to GitHub (optional)
- **Render backups**: Download database from Render dashboard

## Download Database from Render

1. Go to your Render dashboard
2. Click on your web service
3. Go to "Shell" tab
4. Run: `cat instance/poetry_app.db > /tmp/backup.db`
5. Download the file

## Best Practices

1. **Backup before every deployment**
2. **Keep at least 3-5 recent backups**
3. **Test restores occasionally**
4. **Document what changed in each backup**

## Backup Naming Convention

Backups are automatically named with timestamps:
- Format: `poetry_app_YYYYMMDD_HHMMSS.db`
- Example: `poetry_app_20241125_143022.db`
  - Date: November 25, 2024
  - Time: 14:30:22 (2:30:22 PM)
