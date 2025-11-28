# 📚 Poetry Vault - Simple Coding Guide

A beginner-friendly guide to understand how we built this poetry app!

---

## 🎯 What is This App?

Poetry Vault is like Instagram, but for poems! Users can:
- Write and share poems
- Like and comment on poems
- Follow other poets
- Save favorite poems
- Chat with AI poets

---

## 📁 The Files Explained

### Main Files (The Important Ones)

**app.py** - The Brain 🧠
- This is where all the magic happens
- Contains all the "routes" (like /home, /login, /poem/123)
- Think of routes as different pages on a website
- When you visit a URL, Flask runs the code for that route

**models.py** - The Database Blueprint 📋
- Defines what data we store (users, poems, comments, etc.)
- Like creating a form: "Every user needs a username, email, password..."
- SQLAlchemy turns these into actual database tables

**config.py** - The Settings ⚙️
- Stores important settings like secret keys
- Tells the app where the database is
- Different settings for development vs production

**templates/** - The HTML Pages 📄
- 20 different HTML files for different pages
- Uses Jinja2 to make HTML dynamic (show user's name, etc.)
- Like Mad Libs: "Hello, {{ username }}!" becomes "Hello, John!"

---

## 🗄️ Understanding the Database (Simple Version)

Think of the database like Excel spreadsheets. Each "model" is a different sheet:

### 1. Users Sheet
Stores everyone who signs up:
- Username (like "JohnPoet")
- Email
- Password (encrypted for security!)
- Age
- Favorite poet
- Is admin? (yes/no)

### 2. Poems Sheet
Stores all poems:
- Title
- Content (the actual poem text)
- Who wrote it (links to Users)
- When it was created
- Is it a classic poem? (yes/no)
- Is it anonymous? (yes/no)

### 3. Comments Sheet
Stores comments on poems:
- The comment text
- Who wrote it
- Which poem it's on
- When it was posted

### 4. Likes Sheet
Tracks who liked what:
- User ID
- Poem ID
- When they liked it

### 5. Follows Sheet
Tracks who follows who:
- Follower ID (person following)
- Followed ID (person being followed)

### 6. SavedPoems Sheet
Tracks bookmarked poems:
- User ID
- Poem ID
- When they saved it

### 7. Notifications Sheet
Alerts for users:
- Message ("John liked your poem!")
- Type (like, comment, follow)
- Read or unread?

---

## 🔧 How Flask Works (The Basics)

### Routes = Pages

```python
@app.route('/home')
def home():
    return render_template('home.html')
```

This means: "When someone visits /home, show them home.html"

### Getting Data from Forms

```python
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Check if correct...
```

When you submit a form, Flask grabs the data with `request.form`

### Sending Data to HTML

```python
@app.route('/profile')
def profile():
    user = User.query.get(current_user.id)
    return render_template('profile.html', user=user)
```

Now in profile.html, you can use `{{ user.username }}`

---

## 🎨 How the Frontend Works

### HTML Templates (Jinja2)

**Regular HTML:**
```html
<h1>Hello, World!</h1>
```

**Dynamic HTML (Jinja2):**
```html
<h1>Hello, {{ username }}!</h1>
```

The `{{ }}` gets replaced with actual data!

### Loops in Templates

```html
{% for poem in poems %}
    <div class="poem-card">
        <h2>{{ poem.title }}</h2>
        <p>{{ poem.content }}</p>
    </div>
{% endfor %}
```

This creates a card for each poem automatically!

### If Statements in Templates

```html
{% if current_user.is_admin %}
    <button>Delete User</button>
{% endif %}
```

Only admins see the delete button!

---

## 🔐 How Login Works (Authentication)

### Step 1: User Registers
1. User fills out form (username, email, password)
2. Flask receives the data
3. Password gets "hashed" (encrypted) - never store plain passwords!
4. New user saved to database

### Step 2: User Logs In
1. User enters username and password
2. Flask finds user in database
3. Checks if password matches (compares hashes)
4. If correct, creates a "session" (remembers you're logged in)
5. Redirects to home page

### Step 3: Staying Logged In
- Flask-Login creates a cookie in your browser
- Every time you visit a page, Flask checks the cookie
- If valid, you stay logged in
- When you logout, cookie is deleted

### Protected Pages
```python
@app.route('/new-poem')
@login_required  # ← This line!
def new_poem():
    # Only logged-in users can access this
```

---

## 💾 How Database Queries Work

### Getting One Thing
```python
user = User.query.get(5)  # Get user with ID 5
```

### Getting Multiple Things
```python
poems = Poem.query.all()  # Get ALL poems
```

### Filtering
```python
# Get poems by specific user
poems = Poem.query.filter_by(user_id=5).all()
```

### Searching
```python
# Find poems with "love" in title
poems = Poem.query.filter(Poem.title.ilike('%love%')).all()
```

### Creating New Data
```python
new_poem = Poem(title="My Poem", content="Roses are red...")
db.session.add(new_poem)
db.session.commit()  # Save to database!
```

### Updating Data
```python
poem = Poem.query.get(5)
poem.title = "New Title"
db.session.commit()  # Save changes!
```

### Deleting Data
```python
poem = Poem.query.get(5)
db.session.delete(poem)
db.session.commit()  # Gone forever!
```

---

## ⚡ How AJAX Works (No Page Reload)

### The Old Way (Page Reloads)
1. Click "Like" button
2. Browser sends request to server
3. Server processes it
4. **Entire page reloads** ← Annoying!

### The New Way (AJAX - No Reload)
1. Click "Like" button
2. JavaScript sends request in background
3. Server responds with JSON data
4. JavaScript updates just the like count
5. **No page reload!** ← Smooth!

### Example: Like Button

**JavaScript (Frontend):**
```javascript
async function toggleLike(poemId) {
    const response = await fetch(`/poem/${poemId}/like`, {
        method: 'POST'
    });
    const data = await response.json();
    
    // Update the count on the page
    document.getElementById('like-count').textContent = data.count;
}
```

**Python (Backend):**
```python
@app.route('/poem/<int:poem_id>/like', methods=['POST'])
def toggle_like_poem(poem_id):
    # ... like/unlike logic ...
    like_count = Like.query.filter_by(poem_id=poem_id).count()
    return jsonify({'count': like_count})  # Send back JSON
```

---

## 🎭 Key Features Explained Simply

### 1. Home Feed
**What it does:** Shows poems from people you follow

**How it works:**
1. Get list of users you follow
2. Get their poems from database
3. Sort by newest first
4. Display in cards

### 2. Like System
**What it does:** Heart/unheart poems

**How it works:**
1. Check if you already liked it
2. If yes → remove like
3. If no → add like
4. Count total likes
5. Send back new count (AJAX)

### 3. Follow System
**What it does:** Follow/unfollow users

**How it works:**
1. Check if you already follow them
2. If yes → unfollow (delete from Follows table)
3. If no → follow (add to Follows table)
4. Update follower count
5. Create notification for them

### 4. Search
**What it does:** Find poems by keyword

**How it works:**
1. User types search query
2. Search database for poems with that word in title or content
3. Also search for usernames
4. Show all results

### 5. Notifications
**What it does:** Alert you when someone interacts with your content

**How it works:**
1. Someone likes your poem → create notification
2. Someone comments → create notification
3. Someone follows you → create notification
4. You visit /notifications → mark all as read

### 6. Save/Bookmark
**What it does:** Save poems to read later

**How it works:**
1. Click bookmark icon
2. Add entry to SavedPoems table (user_id + poem_id)
3. View saved poems at /saved-poems
4. Click again to unsave (delete from table)

### 7. Admin Panel
**What it does:** Manage users and content

**How it works:**
1. Check if user is admin
2. If not → show error 403 (forbidden)
3. If yes → show dashboard with stats
4. Can reset passwords, view all users, etc.

### 8. AI Chatbot
**What it does:** Chat with famous poets using AI

**How it works:**
1. User types message
2. JavaScript sends to /chat endpoint
3. Flask sends to Ollama API (local AI)
4. AI responds as the poet
5. JavaScript displays response

---

## 🔒 Security Features

### 1. Password Hashing
**Bad:** Storing "password123" in database
**Good:** Storing "8f7h3j9k2l..." (encrypted hash)

If database gets hacked, they can't read passwords!

### 2. Login Required
Some pages need login:
```python
@login_required  # ← Must be logged in
```

### 3. Permission Checks
Can only edit your own poems:
```python
if poem.user_id != current_user.id:
    abort(403)  # Forbidden!
```

### 4. Admin-Only Pages
```python
if not current_user.is_admin:
    abort(403)  # Only admins allowed
```

---

## 🎨 How the Design Works

### CSS Styling
We use CSS to make it look pretty:
- Dark blue background (#1c2532)
- Golden accents (#d4af37)
- Card-based layout (like Instagram)
- Hover effects (buttons change color)

### Responsive Design
Works on phones and computers:
```css
@media (max-width: 768px) {
    /* Different styles for small screens */
}
```

---

## 🚀 How Deployment Works

### Local (Your Computer)
1. Run `python app.py`
2. Flask starts a server
3. Visit http://localhost:5000
4. Only you can access it

### Production (Internet)
1. Push code to GitHub
2. Render.com pulls your code
3. Installs dependencies
4. Runs with Gunicorn (production server)
5. Everyone can access it!

**Environment Variables:**
- `SECRET_KEY`: Random string for security
- `DATABASE_URL`: Where the database is

---

## 📊 What We Built (Summary)

### Pages (20 total)
1. Login / Register
2. Home Feed
3. User Profile
4. Poem Detail
5. New Poem
6. Edit Poem
7. Search Results
8. Saved Poems
9. Notifications
10. Followers / Following
11. Discover Users
12. Settings
13. Admin Dashboard
14. Chat with Poet
15. Terms / Privacy

### Features
✅ User authentication (login/register)
✅ Create, edit, delete poems
✅ Like and comment on poems
✅ Follow/unfollow users
✅ Save favorite poems
✅ Real-time notifications
✅ Search functionality
✅ User profiles
✅ Admin panel
✅ AI chatbot
✅ 103 classic poems pre-loaded

### Database Tables (9 total)
1. Users
2. Poems
3. Comments
4. Likes
5. SavedPoems
6. Follows
7. Notifications
8. Highlights
9. HighlightPoems

---

## 🎓 Coding Concepts You Learned

### Backend (Python/Flask)
- Routes and views
- Database models (ORM)
- Queries and filters
- Form handling
- Authentication
- Sessions and cookies
- JSON APIs
- Error handling

### Frontend (HTML/CSS/JS)
- HTML templates
- CSS styling
- JavaScript events
- AJAX requests
- DOM manipulation
- Responsive design

### Database (SQLAlchemy)
- Creating tables
- Relationships (one-to-many, many-to-many)
- Queries (get, filter, search)
- CRUD operations (Create, Read, Update, Delete)

### Security
- Password hashing
- Login sessions
- Permission checks
- Admin roles

### Deployment
- Environment variables
- Production servers
- Cloud hosting

---

## 💡 Common Patterns Used

### Pattern 1: Create Something
```python
@app.route('/new-poem', methods=['POST'])
def new_poem():
    # 1. Get data from form
    title = request.form['title']
    content = request.form['content']
    
    # 2. Create new object
    poem = Poem(title=title, content=content, user_id=current_user.id)
    
    # 3. Save to database
    db.session.add(poem)
    db.session.commit()
    
    # 4. Redirect somewhere
    return redirect(url_for('home'))
```

### Pattern 2: Show a List
```python
@app.route('/home')
def home():
    # 1. Get data from database
    poems = Poem.query.all()
    
    # 2. Send to template
    return render_template('home.html', poems=poems)
```

### Pattern 3: Toggle Something (Like/Follow/Save)
```python
@app.route('/poem/<id>/like', methods=['POST'])
def toggle_like(id):
    # 1. Check if already exists
    like = Like.query.filter_by(user_id=current_user.id, poem_id=id).first()
    
    # 2. If exists, remove it
    if like:
        db.session.delete(like)
        action = 'unliked'
    # 3. If not, create it
    else:
        like = Like(user_id=current_user.id, poem_id=id)
        db.session.add(like)
        action = 'liked'
    
    # 4. Save and respond
    db.session.commit()
    return jsonify({'action': action})
```

### Pattern 4: Check Permissions
```python
@app.route('/poem/<id>/edit')
@login_required
def edit_poem(id):
    poem = Poem.query.get_or_404(id)
    
    # Check if user owns this poem
    if poem.user_id != current_user.id and not current_user.is_admin:
        abort(403)  # Forbidden
    
    return render_template('edit_poem.html', poem=poem)
```

---

## 🤔 Common Questions Answered

**Q: What is Flask?**
A: A Python framework for building websites. It handles routes, templates, and requests.

**Q: What is SQLAlchemy?**
A: A tool that lets you work with databases using Python code instead of SQL.

**Q: What is Jinja2?**
A: A template engine that lets you put Python code in HTML files.

**Q: What is AJAX?**
A: A way to send requests to the server without reloading the page.

**Q: What is a route?**
A: A URL path (like /home or /login) that triggers specific code.

**Q: What is a model?**
A: A Python class that represents a database table.

**Q: What is a session?**
A: A way to remember who's logged in across different pages.

**Q: What is JSON?**
A: A format for sending data between frontend and backend (like `{"count": 5}`).

**Q: What is a foreign key?**
A: A link between tables (like poem.user_id links to user.id).

**Q: What is hashing?**
A: Encrypting passwords so they can't be read if database is hacked.

---

## 🎉 You Built a Real App!

This isn't a toy project - it's a real, working social platform with:
- User accounts
- Social features (follow, like, comment)
- Search and discovery
- Admin tools
- AI integration
- Production deployment

You learned the same concepts used by companies like Instagram, Twitter, and Medium!

---

## 📚 Next Steps

Want to keep learning? Try:
1. Add a new feature (direct messages?)
2. Improve the design
3. Add more AI features
4. Build a mobile app version
5. Add email notifications
6. Create a recommendation system

The best way to learn is by building! 🚀

---

*Keep coding, keep creating!*
