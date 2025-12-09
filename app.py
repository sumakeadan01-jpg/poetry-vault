from flask import Flask, render_template, request, redirect, url_for, flash, abort, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, Poem, Comment
import requests
from analytics import track_visitor, log_activity

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @app.route('/')
    def index():
        # Track visitor
        track_visitor()
        
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        return redirect(url_for('login'))
    
    @app.route('/emergency-reset/<secret_code>', methods=['GET', 'POST'])
    def emergency_reset(secret_code):
        """Emergency password reset - use secret URL"""
        if secret_code != 'reset2024poetry':
            abort(404)
        
        if request.method == 'POST':
            username = request.form.get('username')
            new_password = request.form.get('new_password')
            
            user = User.query.filter_by(username=username).first()
            if user:
                user.set_password(new_password)
                db.session.commit()
                return '''
                    <html>
                    <head><title>Password Reset Successful</title></head>
                    <body style="font-family: Georgia; background: #1c2532; color: #d4af37; padding: 50px; text-align: center;">
                        <h1>✅ Password Reset Successful!</h1>
                        <p style="font-size: 18px; margin: 20px 0;">Password updated for: ''' + username + '''</p>
                        <p><a href="/login" style="color: #d4af37; font-size: 16px; text-decoration: none; border: 2px solid #d4af37; padding: 10px 20px; display: inline-block; border-radius: 6px;">Go to Login →</a></p>
                    </body>
                    </html>
                '''
            else:
                return '<html><body style="font-family: Georgia; background: #1c2532; color: #ff6b6b; padding: 50px; text-align: center;"><h1>❌ User not found: ' + username + '</h1></body></html>'
        
        # Show reset form (inline HTML - no template needed)
        return '''
            <html>
            <head><title>Emergency Password Reset - Poetry Vault</title></head>
            <body style="font-family: Georgia; background: #1c2532; min-height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0;">
                <div style="max-width: 450px; width: 100%; padding: 20px;">
                    <div style="background: rgba(28, 37, 50, 0.85); border: 2px solid #d4af37; border-radius: 12px; padding: 50px 40px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);">
                        <h1 style="color: #d4af37; text-align: center; margin-bottom: 10px; font-size: 28px;">🔑 Emergency Reset</h1>
                        <p style="color: #8e7a5a; text-align: center; margin-bottom: 30px; font-size: 14px;">Reset your admin password</p>
                        
                        <form method="POST">
                            <div style="margin-bottom: 20px;">
                                <label style="display: block; color: #d4af37; font-size: 13px; margin-bottom: 8px; letter-spacing: 1px; text-transform: uppercase;">Username</label>
                                <input type="text" name="username" value="P0.1Autumn" required 
                                       style="width: 100%; padding: 15px; background: rgba(0, 0, 0, 0.4); border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 6px; color: #e8e8e8; font-family: Georgia; font-size: 15px; box-sizing: border-box;">
                            </div>
                            
                            <div style="margin-bottom: 20px;">
                                <label style="display: block; color: #d4af37; font-size: 13px; margin-bottom: 8px; letter-spacing: 1px; text-transform: uppercase;">New Password</label>
                                <input type="password" name="new_password" required placeholder="Enter new password"
                                       style="width: 100%; padding: 15px; background: rgba(0, 0, 0, 0.4); border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 6px; color: #e8e8e8; font-family: Georgia; font-size: 15px; box-sizing: border-box;">
                            </div>
                            
                            <button type="submit" style="width: 100%; padding: 15px; background: #d4af37; color: #1c2532; border: none; border-radius: 6px; font-size: 16px; font-weight: 600; cursor: pointer; font-family: Georgia; margin-top: 10px;">
                                Reset Password
                            </button>
                        </form>
                        
                        <div style="text-align: center; margin-top: 20px;">
                            <a href="/login" style="color: #d4af37; text-decoration: none; font-size: 14px;">← Back to Login</a>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        '''
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            age = request.form['age']
            favorite_poet = request.form['favorite_poet']
            
            if User.query.filter_by(username=username).first():
                return render_template('register.html', error='Username already exists')
            
            if User.query.filter_by(email=email).first():
                return render_template('register.html', error='Email already exists')
            
            # Make first user admin
            is_first_user = User.query.count() == 0
            
            user = User(username=username, email=email, age=age, favorite_poet=favorite_poet, is_admin=is_first_user)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            login_user(user)
            return redirect(url_for('home'))
        
        return render_template('register.html')
    
    @app.route('/test-route')
    def test_route():
        return '<h1>Route works!</h1>'
    
    @app.route('/reset-admin-now')
    def reset_admin_now():
        """Quick admin password reset - tries multiple usernames"""
        # Try different possible usernames
        possible_usernames = ['P0.1Autumn', 'Autumn', 'P0.1autumn', 'autumn']
        
        for username in possible_usernames:
            user = User.query.filter_by(username=username).first()
            if user:
                # Set a temporary password
                user.set_password('temp2024')
                db.session.commit()
                return f'<html><body style="font-family: Arial; background: #1c2532; color: #d4af37; padding: 50px; text-align: center;"><h1>✅ Password Reset!</h1><p>Username: {user.username}</p><p>New Password: temp2024</p><p><a href="/login" style="color: #d4af37;">Go to Login</a></p><p style="color: #ff6b6b; margin-top: 30px;">⚠️ Change this password immediately after logging in!</p></body></html>'
        
        # If no user found, show all users
        all_users = User.query.all()
        user_list = '<br>'.join([f'{u.username} ({u.email}) {"[ADMIN]" if u.is_admin else ""}' for u in all_users])
        return f'<html><body style="background: #1c2532; color: #ff6b6b; padding: 50px;"><h1>Admin user not found</h1><p>Available users:</p><p style="color: #d4af37;">{user_list}</p></body></html>'
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            # Block classic poets from logging in
            classic_poet_names = ['Shakespeare', 'Rumi', 'Emily Dickinson', 'Edgar Allan Poe', 
                                 'Walt Whitman', 'Lord Byron', 'William Wordsworth', 
                                 'John Keats', 'Percy Shelley', 'Robert Burns',
                                 'Robert Frost', 'Maya Angelou', 'Langston Hughes',
                                 'المتنبي', 'قيس بن الملوح']
            
            # Check for admin secret code
            admin_code = 'P0.1'
            is_admin_login = username.startswith(admin_code)
            
            # Remove admin code from username for lookup
            if is_admin_login:
                actual_username = username[len(admin_code):]
            else:
                actual_username = username
            
            # Prevent classic poets from logging in
            if actual_username in classic_poet_names:
                return render_template('login.html', error='Classic poet accounts are for reference only')
            
            user = User.query.filter_by(username=actual_username).first()
            
            if user and user.check_password(password):
                # Grant admin access if they used the code
                if is_admin_login:
                    user.is_admin = True
                    db.session.commit()
                
                login_user(user)
                log_activity('login', f'User {user.username} logged in')
                return redirect(url_for('home'))
            
            return render_template('login.html', error='Invalid username or password')
        
        return render_template('login.html')
    

    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))
    
    @app.route('/admin/reset-database/<secret_code>')
    def reset_database(secret_code):
        """Admin route to reset the database - USE WITH CAUTION!"""
        # Secret code to prevent accidental resets
        if secret_code != 'RESET_POETRY_VAULT_2024':
            abort(404)
        
        try:
            import os
            # Drop all tables
            db.drop_all()
            # Recreate all tables
            db.create_all()
            
            # Auto-seed with classic poems
            from seed_poems import FAMOUS_POEMS
            
            for poet_name, poems_list in FAMOUS_POEMS.items():
                # Create poet user
                poet = User(
                    username=poet_name,
                    email=f"{poet_name.lower().replace(' ', '')}@poetry.vault",
                    age=100,
                    favorite_poet=poet_name,
                    is_admin=False
                )
                poet.set_password('classic_poet_password')
                db.session.add(poet)
                db.session.flush()
                
                # Add their poems
                for poem_data in poems_list:
                    poem = Poem(
                        title=poem_data['title'],
                        content=poem_data['content'],
                        user_id=poet.id,
                        is_classic=True
                    )
                    db.session.add(poem)
            
            db.session.commit()
            
            return '''
            <html>
            <head><title>Database Reset</title></head>
            <body style="font-family: Arial; padding: 50px; text-align: center;">
                <h1 style="color: green;">✅ Database Reset Successful!</h1>
                <p>The database has been reset with all classic poets and poems.</p>
                <p><a href="/register" style="color: #d4af37; text-decoration: none; font-size: 18px;">→ Register Your Account</a></p>
            </body>
            </html>
            '''
        except Exception as e:
            return f'''
            <html>
            <head><title>Reset Failed</title></head>
            <body style="font-family: Arial; padding: 50px; text-align: center;">
                <h1 style="color: red;">❌ Reset Failed</h1>
                <p>Error: {str(e)}</p>
                <p><a href="/" style="color: #d4af37;">← Back to Home</a></p>
            </body>
            </html>
            '''
    
    @app.route('/admin/add-tutorial-column/<secret_code>')
    def add_tutorial_column_route(secret_code):
        """Add has_seen_tutorial column to database - Safe migration"""
        if secret_code != 'ADD_TUTORIAL_2024':
            abort(404)
        
        try:
            # Check if column already exists
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('users')]
            
            if 'has_seen_tutorial' in columns:
                return '''
                <html>
                <head><title>Migration Status</title></head>
                <body style="font-family: Arial; padding: 50px; text-align: center;">
                    <h1 style="color: green;">✅ Column Already Exists!</h1>
                    <p>The has_seen_tutorial column is already in the database.</p>
                    <p>No changes needed.</p>
                    <p><a href="/" style="color: #d4af37; text-decoration: none; font-size: 18px;">→ Go to Home</a></p>
                </body>
                </html>
                '''
            
            # Add the column using raw SQL
            from sqlalchemy import text
            
            try:
                if 'postgresql' in str(db.engine.url):
                    # PostgreSQL
                    db.session.execute(text('ALTER TABLE users ADD COLUMN has_seen_tutorial BOOLEAN DEFAULT FALSE'))
                    db.session.commit()
                    db.session.execute(text('UPDATE users SET has_seen_tutorial = FALSE WHERE has_seen_tutorial IS NULL'))
                    db.session.commit()
                else:
                    # SQLite
                    db.session.execute(text('ALTER TABLE users ADD COLUMN has_seen_tutorial BOOLEAN DEFAULT 0'))
                    db.session.commit()
                    db.session.execute(text('UPDATE users SET has_seen_tutorial = 0 WHERE has_seen_tutorial IS NULL'))
                    db.session.commit()
            except Exception as e:
                db.session.rollback()
                if 'already exists' in str(e).lower() or 'duplicate column' in str(e).lower():
                    # Column already exists, that's fine
                    pass
                else:
                    raise e
            
            # Count users
            user_count = User.query.count()
            
            return f'''
            <html>
            <head><title>Migration Successful</title></head>
            <body style="font-family: Arial; padding: 50px; text-align: center;">
                <h1 style="color: green;">✅ Migration Successful!</h1>
                <p>Added has_seen_tutorial column to database.</p>
                <p>Updated {user_count} users - they will all see the tutorial once.</p>
                <p><a href="/" style="color: #d4af37; text-decoration: none; font-size: 18px;">→ Go to Home</a></p>
            </body>
            </html>
            '''
        except Exception as e:
            return f'''
            <html>
            <head><title>Migration Failed</title></head>
            <body style="font-family: Arial; padding: 50px; text-align: center;">
                <h1 style="color: red;">❌ Migration Failed</h1>
                <p>Error: {str(e)}</p>
                <p>The column might already exist, or there's a database issue.</p>
                <p><a href="/" style="color: #d4af37;">← Back to Home</a></p>
            </body>
            </html>
            '''
    
    @app.route('/admin/import-new-poems/<secret_code>')
    def import_new_poems_route(secret_code):
        """Import new poems from seed_poems_part2.py"""
        if secret_code != 'IMPORT_POEMS_2024':
            abort(404)
        
        try:
            from seed_poems_part2 import ADDITIONAL_FAMOUS_POEMS
            
            added_total = 0
            skipped_total = 0
            results = []
            
            for poet_name, poems_list in ADDITIONAL_FAMOUS_POEMS.items():
                poet = User.query.filter_by(username=poet_name).first()
                
                if not poet:
                    results.append(f"❌ {poet_name}: Poet not found")
                    continue
                
                added = 0
                skipped = 0
                
                for poem_data in poems_list:
                    existing = Poem.query.filter_by(
                        title=poem_data['title'],
                        user_id=poet.id
                    ).first()
                    
                    if existing:
                        skipped += 1
                    else:
                        poem = Poem(
                            title=poem_data['title'],
                            content=poem_data['content'],
                            category=poem_data.get('category', 'general'),
                            user_id=poet.id,
                            is_classic=True
                        )
                        db.session.add(poem)
                        added += 1
                
                db.session.commit()
                added_total += added
                skipped_total += skipped
                results.append(f"✅ {poet_name}: Added {added}, Skipped {skipped}")
            
            results_html = '<br>'.join(results)
            
            return f'''
            <html>
            <head><title>Import Successful</title></head>
            <body style="font-family: Arial; padding: 50px; text-align: center;">
                <h1 style="color: green;">✅ Import Successful!</h1>
                <p>Added {added_total} new poems, Skipped {skipped_total} (already exist)</p>
                <div style="text-align: left; max-width: 600px; margin: 20px auto; padding: 20px; background: #f5f5f5; border-radius: 8px;">
                    {results_html}
                </div>
                <p><a href="/" style="color: #d4af37; text-decoration: none; font-size: 18px;">→ Go to Home</a></p>
            </body>
            </html>
            '''
        except Exception as e:
            return f'''
            <html>
            <head><title>Import Failed</title></head>
            <body style="font-family: Arial; padding: 50px; text-align: center;">
                <h1 style="color: red;">❌ Import Failed</h1>
                <p>Error: {str(e)}</p>
                <p><a href="/" style="color: #d4af37;">← Back to Home</a></p>
            </body>
            </html>
            '''
    
    @app.route('/admin/add-analytics-tables/<secret_code>')
    def add_analytics_tables_route(secret_code):
        """Add analytics tables to database"""
        if secret_code != 'ADD_ANALYTICS_2024':
            abort(404)
        
        try:
            from sqlalchemy import text
            
            # Create user_activities table
            db.session.execute(text('''
                CREATE TABLE IF NOT EXISTS user_activities (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    activity_type VARCHAR(50) NOT NULL,
                    description VARCHAR(255),
                    ip_address VARCHAR(50),
                    user_agent VARCHAR(255),
                    referrer VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            
            # Create visitors table
            db.session.execute(text('''
                CREATE TABLE IF NOT EXISTS visitors (
                    id SERIAL PRIMARY KEY,
                    nickname VARCHAR(100),
                    source VARCHAR(100),
                    ip_address VARCHAR(50),
                    user_agent VARCHAR(255),
                    referrer VARCHAR(255),
                    first_visit TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_visit TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    visit_count INTEGER DEFAULT 1
                )
            '''))
            
            db.session.commit()
            
            return '''
            <html>
            <head><title>Analytics Tables Added</title></head>
            <body style="font-family: Arial; padding: 50px; text-align: center;">
                <h1 style="color: green;">✅ Analytics Tables Created!</h1>
                <p>Successfully added user_activities and visitors tables.</p>
                <p>Your admin panel now tracks visitor and user activity!</p>
                <p><a href="/admin" style="color: #d4af37; text-decoration: none; font-size: 18px;">→ Go to Admin Panel</a></p>
            </body>
            </html>
            '''
        except Exception as e:
            return f'''
            <html>
            <head><title>Migration Failed</title></head>
            <body style="font-family: Arial; padding: 50px; text-align: center;">
                <h1 style="color: red;">❌ Migration Failed</h1>
                <p>Error: {str(e)}</p>
                <p>Tables might already exist.</p>
                <p><a href="/" style="color: #d4af37;">← Back to Home</a></p>
            </body>
            </html>
            '''
    
    @app.route('/home')
    @login_required
    def home():
        from datetime import datetime
        from models import SavedPoem, Follow
        
        # Get current hour
        current_hour = datetime.now().hour
        
        # Determine greeting based on time
        if 5 <= current_hour < 12:
            greeting = "Good morning"
        elif 12 <= current_hour < 17:
            greeting = "Good afternoon"
        elif 17 <= current_hour < 21:
            greeting = "Good evening"
        else:
            greeting = "Good night"
        
        # Get IDs of users current user follows
        following_ids = [f.followed_id for f in Follow.query.filter_by(follower_id=current_user.id).all()]
        
        # Show poems from followed users, or all poems if not following anyone yet
        if following_ids:
            poems = Poem.query.filter(Poem.user_id.in_(following_ids), Poem.is_classic == False).order_by(Poem.created_at.desc()).all()
        else:
            # If not following anyone, show all user poems (not classic) to help discover
            poems = Poem.query.filter_by(is_classic=False).order_by(Poem.created_at.desc()).all()
        
        # Get saved poem IDs for current user
        saved_poem_ids = [s.poem_id for s in SavedPoem.query.filter_by(user_id=current_user.id).all()]
        
        # Check if user should see tutorial
        show_tutorial = not current_user.has_seen_tutorial
        
        return render_template('home.html', poems=poems, greeting=greeting, saved_poem_ids=saved_poem_ids, show_tutorial=show_tutorial)
    
    @app.route('/new-poem', methods=['GET', 'POST'])
    @login_required
    def new_poem():
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            is_anonymous = request.form.get('anonymous') == 'on'
            
            poem = Poem(title=title, content=content, user_id=current_user.id, is_anonymous=is_anonymous)
            db.session.add(poem)
            db.session.commit()
            
            return redirect(url_for('home'))
        
        return render_template('new_poem.html')
    
    @app.route('/users')
    @login_required
    def users():
        from models import Follow
        # Only show real users, not classic poets
        classic_poet_names = ['Shakespeare', 'Rumi', 'Emily Dickinson', 'Edgar Allan Poe', 
                             'Walt Whitman', 'Lord Byron', 'William Wordsworth', 
                             'John Keats', 'Percy Shelley', 'Robert Burns',
                             'Robert Frost', 'Maya Angelou', 'Langston Hughes',
                             'المتنبي', 'قيس بن الملوح']
        all_users = User.query.filter(~User.username.in_(classic_poet_names)).order_by(User.created_at.desc()).all()
        
        # Get IDs of users current user follows
        current_user_following_ids = [f.followed_id for f in Follow.query.filter_by(follower_id=current_user.id).all()]
        
        return render_template('users.html', users=all_users, current_user_following_ids=current_user_following_ids)
    
    @app.route('/settings')
    @login_required
    def settings():
        return render_template('settings.html')
    
    @app.route('/terms')
    def terms():
        return render_template('terms.html')
    
    @app.route('/privacy')
    def privacy():
        return render_template('privacy.html')
    
    @app.route('/settings/profile', methods=['POST'])
    @login_required
    def update_profile():
        username = request.form.get('username')
        email = request.form.get('email')
        favorite_poet = request.form.get('favorite_poet')
        
        if username and username != current_user.username:
            if User.query.filter_by(username=username).first():
                return render_template('settings.html', message='Username already taken', message_type='error')
            current_user.username = username
        
        if email and email != current_user.email:
            if User.query.filter_by(email=email).first():
                return render_template('settings.html', message='Email already in use', message_type='error')
            current_user.email = email
        
        if favorite_poet:
            current_user.favorite_poet = favorite_poet
        
        db.session.commit()
        return render_template('settings.html', message='Profile updated successfully!', message_type='success')
    
    @app.route('/settings/password', methods=['POST'])
    @login_required
    def change_password():
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if not current_user.check_password(old_password):
            return render_template('settings.html', message='Current password is incorrect', message_type='error')
        
        if new_password != confirm_password:
            return render_template('settings.html', message='New passwords do not match', message_type='error')
        
        current_user.set_password(new_password)
        db.session.commit()
        return render_template('settings.html', message='Password changed successfully!', message_type='success')
    
    @app.route('/settings/delete-account', methods=['POST'])
    @login_required
    def delete_account():
        """Permanently delete user account and all associated data"""
        try:
            from models import Notification, Follow
            
            user_id = current_user.id
            
            # Delete all user's poems (this will cascade delete comments via relationship)
            user_poems = Poem.query.filter_by(user_id=user_id).all()
            for poem in user_poems:
                db.session.delete(poem)
            
            # Delete all notifications for this user
            Notification.query.filter_by(user_id=user_id).delete()
            
            # Delete all follow relationships (following and followers)
            Follow.query.filter_by(follower_id=user_id).delete()
            Follow.query.filter_by(followed_id=user_id).delete()
            
            # Delete all comments by this user
            Comment.query.filter_by(user_id=user_id).delete()
            
            # Finally, delete the user account
            db.session.delete(current_user)
            db.session.commit()
            
            # Log out the user
            logout_user()
            
            return jsonify({'status': 'success', 'message': 'Account deleted successfully'})
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting account: {e}")
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    @app.route('/admin')
    @login_required
    def admin():
        if not current_user.is_admin:
            abort(403)
        
        from models import UserActivity, Visitor
        from datetime import datetime, timedelta
        
        total_users = User.query.count()
        total_poems = Poem.query.count()
        total_comments = Comment.query.count()
        all_users = User.query.order_by(User.created_at.desc()).all()
        recent_poems = Poem.query.order_by(Poem.created_at.desc()).limit(10).all()
        
        # Analytics data
        total_visitors = Visitor.query.count()
        recent_visitors = Visitor.query.order_by(Visitor.last_visit.desc()).limit(20).all()
        recent_activities = UserActivity.query.order_by(UserActivity.created_at.desc()).limit(50).all()
        
        # Today's stats
        today = datetime.utcnow().date()
        today_start = datetime.combine(today, datetime.min.time())
        today_activities = UserActivity.query.filter(UserActivity.created_at >= today_start).count()
        today_visitors = Visitor.query.filter(Visitor.last_visit >= today_start).count()
        
        # Source breakdown
        instagram_visitors = Visitor.query.filter_by(source='instagram').count()
        direct_visitors = Visitor.query.filter_by(source='direct').count()
        
        return render_template('admin.html', 
                             total_users=total_users,
                             total_poems=total_poems,
                             total_comments=total_comments,
                             users=all_users,
                             poems=recent_poems,
                             total_visitors=total_visitors,
                             recent_visitors=recent_visitors,
                             recent_activities=recent_activities,
                             today_activities=today_activities,
                             today_visitors=today_visitors,
                             instagram_visitors=instagram_visitors,
                             direct_visitors=direct_visitors)
    
    @app.route('/admin/delete-user/<int:user_id>', methods=['POST'])
    @login_required
    def admin_delete_user(user_id):
        """Admin route to delete a user account"""
        if not current_user.is_admin:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
        
        try:
            from models import Notification, Follow
            
            user = User.query.get(user_id)
            if not user:
                return jsonify({'status': 'error', 'message': 'User not found'}), 404
            
            # Prevent deleting admin accounts
            if user.is_admin:
                return jsonify({'status': 'error', 'message': 'Cannot delete admin accounts'}), 403
            
            username = user.username
            
            # Delete all user's poems (comments will cascade)
            user_poems = Poem.query.filter_by(user_id=user_id).all()
            for poem in user_poems:
                db.session.delete(poem)
            
            # Delete all notifications for this user
            Notification.query.filter_by(user_id=user_id).delete()
            
            # Delete all follow relationships
            Follow.query.filter_by(follower_id=user_id).delete()
            Follow.query.filter_by(followed_id=user_id).delete()
            
            # Delete all comments
            Comment.query.filter_by(user_id=user_id).delete()
            
            # Delete the user
            db.session.delete(user)
            db.session.commit()
            
            return jsonify({'status': 'success', 'message': f'User {username} deleted successfully'})
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting user: {e}")
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    @app.route('/admin/reset-password/<int:user_id>', methods=['GET', 'POST'])
    @login_required
    def reset_password(user_id):
        if not current_user.is_admin:
            abort(403)
        
        user = User.query.get(user_id)
        
        if request.method == 'POST':
            new_password = request.form['new_password']
            user.set_password(new_password)
            db.session.commit()
            return redirect(url_for('admin'))
        
        return render_template('reset_password.html', user=user)
    
    @app.route('/poem/<int:poem_id>', methods=['GET', 'POST'])
    @login_required
    def poem_detail(poem_id):
        from models import Notification, SavedPoem
        poem = Poem.query.get_or_404(poem_id)
        
        if request.method == 'POST':
            comment_text = request.form['comment']
            comment = Comment(content=comment_text, user_id=current_user.id, poem_id=poem_id)
            db.session.add(comment)
            
            # Create notification for poem author
            if poem.user_id != current_user.id:
                notif = Notification(
                    user_id=poem.user_id,
                    type='comment',
                    message=f'{current_user.username} commented on your poem "{poem.title}"',
                    poem_id=poem_id
                )
                db.session.add(notif)
            
            db.session.commit()
            return redirect(url_for('poem_detail', poem_id=poem_id))
        
        # Check if poem is saved by current user
        is_saved = SavedPoem.query.filter_by(user_id=current_user.id, poem_id=poem_id).first() is not None
        
        return render_template('poem_detail.html', poem=poem, is_saved=is_saved)
    
    @app.route('/poem/<int:poem_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_poem(poem_id):
        poem = Poem.query.get_or_404(poem_id)
        
        # Check permissions
        if poem.user_id != current_user.id and not current_user.is_admin:
            abort(403)
        
        if request.method == 'POST':
            poem.title = request.form['title']
            poem.content = request.form['content']
            db.session.commit()
            return redirect(url_for('poem_detail', poem_id=poem_id))
        
        return render_template('edit_poem.html', poem=poem)
    
    @app.route('/poem/<int:poem_id>/delete', methods=['POST'])
    @login_required
    def delete_poem(poem_id):
        poem = Poem.query.get_or_404(poem_id)
        
        # Check permissions
        if poem.user_id != current_user.id and not current_user.is_admin:
            abort(403)
        
        db.session.delete(poem)
        db.session.commit()
        return redirect(url_for('home'))
    
    @app.route('/poem/<int:poem_id>/save', methods=['POST'])
    @login_required
    def toggle_save_poem(poem_id):
        from models import SavedPoem
        poem = Poem.query.get_or_404(poem_id)
        saved = SavedPoem.query.filter_by(user_id=current_user.id, poem_id=poem_id).first()
        
        if saved:
            db.session.delete(saved)
            action = 'unsaved'
        else:
            new_save = SavedPoem(user_id=current_user.id, poem_id=poem_id)
            db.session.add(new_save)
            action = 'saved'
        
        db.session.commit()
        return jsonify({'status': 'success', 'action': action})
    
    @app.route('/saved-poems')
    @login_required
    def saved_poems():
        from models import SavedPoem
        saved = SavedPoem.query.filter_by(user_id=current_user.id).order_by(SavedPoem.saved_at.desc()).all()
        poems = [s.poem for s in saved]
        return render_template('saved_poems.html', poems=poems)
    @app.route('/poem/<int:poem_id>/like', methods=['POST'])
    @login_required
    def toggle_like_poem(poem_id):
        from models import Like, Notification
        poem = Poem.query.get_or_404(poem_id)
        like = Like.query.filter_by(user_id=current_user.id, poem_id=poem_id).first()
        
        if like:
            db.session.delete(like)
            action = 'unliked'
        else:
            new_like = Like(user_id=current_user.id, poem_id=poem_id)
            db.session.add(new_like)
            action = 'liked'
            
            # Create notification for poem author
            if poem.user_id != current_user.id:
                notif = Notification(
                    user_id=poem.user_id,
                    type='like',
                    message=f'{current_user.username} liked your poem "{poem.title}"',
                    poem_id=poem_id
                )
                db.session.add(notif)
        
        db.session.commit()
        like_count = Like.query.filter_by(poem_id=poem_id).count()
        return jsonify({'status': 'success', 'action': action, 'count': like_count})

    @app.route('/api/search-poets', methods=['GET'])
    @login_required
    def search_poets():
        query = request.args.get('q', '').strip()
        poets = []
        if query:
            results = db.session.query(User.username).join(Poem).filter(
                User.username.ilike(f'%{query}%'),
                Poem.is_classic == True
            ).distinct().all()
            poets = [r[0] for r in results]
        return jsonify({'poets': poets})

    @app.route('/profile')
    @login_required
    def my_profile():
        return redirect(url_for('user_profile', user_id=current_user.id))
    
    @app.route('/user/<int:user_id>')
    @login_required
    def user_profile(user_id):
        from models import Follow, Highlight
        user = User.query.get_or_404(user_id)
        poems = Poem.query.filter_by(user_id=user_id, is_classic=False).order_by(Poem.created_at.desc()).all()
        
        # Check if current user follows this user
        is_following = Follow.query.filter_by(follower_id=current_user.id, followed_id=user_id).first() is not None
        
        # Get follower/following counts
        followers_count = Follow.query.filter_by(followed_id=user_id).count()
        following_count = Follow.query.filter_by(follower_id=user_id).count()
        
        # Get highlights
        highlights = Highlight.query.filter_by(user_id=user_id).all()
        
        return render_template('user_profile.html', user=user, poems=poems, is_following=is_following, 
                             followers_count=followers_count, following_count=following_count, highlights=highlights)
    
    @app.route('/user/<int:user_id>/follow', methods=['POST'])
    @login_required
    def toggle_follow(user_id):
        from models import Follow, Notification
        
        if user_id == current_user.id:
            return jsonify({'status': 'error', 'message': 'Cannot follow yourself'}), 400
        
        user = User.query.get_or_404(user_id)
        follow = Follow.query.filter_by(follower_id=current_user.id, followed_id=user_id).first()
        
        if follow:
            db.session.delete(follow)
            action = 'unfollowed'
        else:
            new_follow = Follow(follower_id=current_user.id, followed_id=user_id)
            db.session.add(new_follow)
            action = 'followed'
            
            # Create notification
            notif = Notification(
                user_id=user_id,
                type='follow',
                message=f'{current_user.username} started following you'
            )
            db.session.add(notif)
        
        db.session.commit()
        followers_count = Follow.query.filter_by(followed_id=user_id).count()
        return jsonify({'status': 'success', 'action': action, 'followers_count': followers_count})
    
    @app.route('/user/<int:user_id>/followers')
    @login_required
    def user_followers(user_id):
        from models import Follow
        user = User.query.get_or_404(user_id)
        
        # Get all followers
        follower_relationships = Follow.query.filter_by(followed_id=user_id).all()
        followers = [User.query.get(f.follower_id) for f in follower_relationships]
        
        # Check which ones current user follows
        current_user_following_ids = [f.followed_id for f in Follow.query.filter_by(follower_id=current_user.id).all()]
        
        return render_template('followers.html', user=user, followers=followers, 
                             current_user_following_ids=current_user_following_ids)
    
    @app.route('/user/<int:user_id>/following')
    @login_required
    def user_following(user_id):
        from models import Follow
        user = User.query.get_or_404(user_id)
        
        # Get all users this user follows
        following_relationships = Follow.query.filter_by(follower_id=user_id).all()
        following = [User.query.get(f.followed_id) for f in following_relationships]
        
        # Check which ones current user follows
        current_user_following_ids = [f.followed_id for f in Follow.query.filter_by(follower_id=current_user.id).all()]
        
        return render_template('following.html', user=user, following=following, 
                             current_user_following_ids=current_user_following_ids)
    
    @app.route('/search', methods=['GET'])
    @login_required
    def search():
        query = request.args.get('q', '').strip()
        poems = []
        if query:
            # Search in title, content, AND author username
            poems = Poem.query.join(User).filter(
                db.or_(
                    Poem.title.ilike(f'%{query}%'),
                    Poem.content.ilike(f'%{query}%'),
                    User.username.ilike(f'%{query}%')
                )
            ).order_by(Poem.created_at.desc()).all()
        return render_template('search.html', poems=poems, query=query)
    
    @app.route('/discover')
    @login_required
    def discover():
        from models import Follow
        import random
        
        # Get users current user already follows
        following_ids = [f.followed_id for f in Follow.query.filter_by(follower_id=current_user.id).all()]
        following_ids.append(current_user.id)  # Exclude self
        
        # Get classic poet names to exclude
        classic_poet_names = ['Shakespeare', 'Rumi', 'Emily Dickinson', 'Edgar Allan Poe', 
                             'Walt Whitman', 'Lord Byron', 'William Wordsworth', 
                             'John Keats', 'Percy Shelley', 'Robert Burns',
                             'Robert Frost', 'Maya Angelou', 'Langston Hughes',
                             'المتنبي', 'قيس بن الملوح']
        
        # Get suggested users (not following, not self, not classic poets)
        suggested_users = User.query.filter(
            ~User.id.in_(following_ids),
            ~User.username.in_(classic_poet_names)
        ).all()
        
        # Shuffle for variety
        random.shuffle(suggested_users)
        
        # Get recent poems for each suggested user
        for user in suggested_users[:10]:  # Limit to 10 suggestions
            user.recent_poems = Poem.query.filter_by(user_id=user.id, is_classic=False).order_by(Poem.created_at.desc()).limit(3).all()
        
        return render_template('discover.html', suggested_users=suggested_users[:10])
    
    @app.route('/notifications')
    @login_required
    def notifications():
        from models import Notification
        notifs = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
        # Mark as read
        for notif in notifs:
            notif.is_read = True
        db.session.commit()
        return render_template('notifications.html', notifications=notifs)
    
    @app.route('/notifications/unread-count')
    @login_required
    def unread_notifications_count():
        from models import Notification
        count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
        return jsonify({'count': count})
    
    @app.route('/api/track-instagram-visitor', methods=['POST'])
    def track_instagram_visitor():
        """Hidden API endpoint to track Instagram visitors automatically"""
        try:
            from models import Visitor
            from datetime import datetime
            
            data = request.get_json()
            ip_address = request.remote_addr
            user_agent = data.get('userAgent', '')[:255]
            referrer = data.get('referrer', '')[:255]
            nickname = data.get('nickname', '')  # Get nickname from URL parameter
            source = 'instagram'
            
            # Check if visitor exists
            visitor = Visitor.query.filter_by(ip_address=ip_address).first()
            
            if visitor:
                # Update existing visitor
                visitor.last_visit = datetime.utcnow()
                visitor.visit_count += 1
                if visitor.source == 'direct':  # Update if was previously direct
                    visitor.source = source
                if nickname and not visitor.nickname:  # Add nickname if provided
                    visitor.nickname = nickname
            else:
                # Create new visitor
                visitor = Visitor(
                    nickname=nickname if nickname else None,
                    source=source,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    referrer=referrer if referrer else None
                )
                db.session.add(visitor)
            
            db.session.commit()
            return jsonify({'status': 'success'})
        except Exception as e:
            print(f"Error tracking Instagram visitor: {e}")
            db.session.rollback()
            return jsonify({'status': 'error'}), 500
    
    @app.route('/api/check-new-notifications')
    @login_required
    def check_new_notifications():
        """API endpoint for desktop notifications - returns unread notifications"""
        from models import Notification
        
        # Get unread notifications
        notifications = Notification.query.filter_by(
            user_id=current_user.id,
            is_read=False
        ).order_by(Notification.created_at.desc()).limit(5).all()
        
        # Convert to JSON
        notif_list = [{
            'id': n.id,
            'type': n.type,
            'message': n.message,
            'created_at': n.created_at.isoformat()
        } for n in notifications]
        
        return jsonify({'notifications': notif_list})
    
    @app.route('/mark-tutorial-seen', methods=['POST'])
    @login_required
    def mark_tutorial_seen():
        """Mark that user has seen the onboarding tutorial"""
        current_user.has_seen_tutorial = True
        db.session.commit()
        return jsonify({'status': 'success'})
    
    @app.route('/chat-with-poet')
    @login_required
    def chat_page():
        return render_template('chat.html')
    
    @app.route('/chat', methods=['POST'])
    @login_required
    def chat():
        data = request.get_json()
        user_message = data.get('message', '')
        poet = current_user.favorite_poet
        
        # Poet personalities - Keep responses SHORT and ANSWER THE QUESTION DIRECTLY
        poet_prompts = {
            'Shakespeare': f"You are William Shakespeare (1564-1616). Answer questions DIRECTLY and FACTUALLY first, then add personality. Keep it SHORT (2-3 sentences). User asks: '{user_message}'",
            'Rumi': f"You are Rumi (1207-1273), Persian Sufi mystic. Answer questions DIRECTLY and FACTUALLY first, then add wisdom. Keep it SHORT (2-3 sentences). User asks: '{user_message}'",
            'Emily Dickinson': f"You are Emily Dickinson (1830-1886) in an educational historical conversation. Answer questions DIRECTLY and FACTUALLY about your life. You were reclusive, never married, had a close relationship with Susan Gilbert (your sister-in-law). You wrote passionate letters to her. Died 1886 in Amherst. Keep it SHORT (2-3 sentences). User asks: '{user_message}'",
            'Edgar Allan Poe': f"You are Edgar Allan Poe (1809-1849). Answer questions DIRECTLY and FACTUALLY first. You married Virginia Clemm (your cousin), she died young. You died mysteriously in 1849. Keep it SHORT (2-3 sentences). User asks: '{user_message}'",
            'Walt Whitman': f"You are Walt Whitman (1819-1892). Answer questions DIRECTLY and FACTUALLY first. You celebrated democracy, worked as nurse in Civil War, died 1892. Keep it SHORT (2-3 sentences). User asks: '{user_message}'",
            'Lord Byron': f"You are Lord Byron (1788-1824). Answer questions DIRECTLY and FACTUALLY first. You had many scandalous affairs, died fighting for Greek independence in 1824. Keep it SHORT (2-3 sentences). User asks: '{user_message}'",
            'William Wordsworth': f"You are William Wordsworth (1770-1850). Answer questions DIRECTLY and FACTUALLY first. You loved nature, married Mary Hutchinson, died 1850. Keep it SHORT (2-3 sentences). User asks: '{user_message}'",
            'John Keats': f"You are John Keats (1795-1821). Answer questions DIRECTLY and FACTUALLY first. You loved Fanny Brawne, died of tuberculosis at 25 in Rome, 1821. Keep it SHORT (2-3 sentences). User asks: '{user_message}'",
            'Percy Shelley': f"You are Percy Bysshe Shelley (1792-1822). Answer questions DIRECTLY and FACTUALLY first. You married Mary Shelley (Frankenstein author), drowned in sailing accident 1822. Keep it SHORT (2-3 sentences). User asks: '{user_message}'",
            'Robert Burns': f"You are Robert Burns (1759-1796). Answer questions DIRECTLY and FACTUALLY first. You were a Scottish farmer-poet, had many loves and children, died 1796. Keep it SHORT (2-3 sentences). User asks: '{user_message}'"
        }
        
        prompt = poet_prompts.get(poet, f"You are a wise poet. Respond thoughtfully to: {user_message}")
        
        try:
            # Call Ollama API
            response = requests.post('http://localhost:11434/api/generate',
                json={
                    'model': 'llama3.2:1b',
                    'prompt': prompt,
                    'stream': False
                })
            
            if response.status_code == 200:
                ai_response = response.json()['response']
                return jsonify({'response': ai_response})
            else:
                return jsonify({'response': 'Alas, I seem to have lost my voice momentarily. Please try again.'})
        except Exception as e:
            return jsonify({'response': 'My connection to the muse has been interrupted. Ensure Ollama is running.'})
    
    with app.app_context():
        db.create_all()
        
        # Auto-seed database if empty
        if Poem.query.count() == 0:
            from seed_poems import FAMOUS_POEMS
            from werkzeug.security import generate_password_hash
            
            for poet_name, poems in FAMOUS_POEMS.items():
                poet_user = User.query.filter_by(username=poet_name).first()
                
                if not poet_user:
                    poet_user = User(
                        username=poet_name,
                        email=f'{poet_name.lower().replace(" ", "")}@poetryvault.com',
                        password_hash=generate_password_hash('classic_poet_2024'),
                        age=None,
                        favorite_poet=poet_name,
                        is_admin=False
                    )
                    db.session.add(poet_user)
                    db.session.flush()
                
                for poem_data in poems:
                    poem = Poem(
                        title=poem_data['title'],
                        content=poem_data['content'],
                        category=poem_data.get('category', 'general'),
                        user_id=poet_user.id,
                        is_classic=True
                    )
                    db.session.add(poem)
            
            db.session.commit()
            print("✅ Database auto-seeded with classic poems!")
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
