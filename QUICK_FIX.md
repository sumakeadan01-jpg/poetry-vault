# 🔧 Quick Fix for Database Error

## The Error:
```
no such column: users.has_seen_tutorial
```

## ✅ Solution (Choose One):

### Option 1: Run Fix Script in PyCharm

1. **Open PyCharm**
2. **Open Terminal in PyCharm** (bottom of screen)
3. **Run:**
   ```bash
   python fix_database.py
   ```
4. **Then run:**
   ```bash
   python run_test.py
   ```

---

### Option 2: Manual SQL Fix

1. **Open your database file:**
   - File: `instance/poetry_app.db`
   - Use DB Browser for SQLite or any SQLite tool

2. **Run this SQL:**
   ```sql
   ALTER TABLE users ADD COLUMN has_seen_tutorial BOOLEAN DEFAULT 0;
   UPDATE users SET has_seen_tutorial = 0;
   ```

3. **Save and close**

4. **Run the app**

---

### Option 3: Fresh Start (Easiest!)

If you don't mind losing local test data:

1. **Delete local database:**
   ```bash
   rm instance/poetry_app.db
   ```

2. **Run the app** (it will create a new database with the correct schema):
   ```bash
   python run_test.py
   ```

3. **Register a new test account**

---

## 🎯 Recommended: Option 3 (Fresh Start)

Since this is just your local test database (not the live Render one), the easiest fix is:

**In PyCharm Terminal:**
```bash
rm instance/poetry_app.db
python run_test.py
```

Then register a new account and test the tutorial!

**Your live Render database is completely safe and unaffected!**

---

## After Fixing:

Visit: http://localhost:5001

You should see the tutorial tooltips! 🎉
