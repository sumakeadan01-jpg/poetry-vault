from flask import Flask, render_template, request, redirect, url_for, flash, abort, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, Poem, Comment
import requests
from analytics import track_visitor, log_activity
from datetime import datetime
import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except Exception as e:
            logger.error(f"Error loading user {user_id}: {str(e)}")
            return None
    
    # Global error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        logger.warning(f"404 error: {request.url}")
        return render_template('404.html'), 404 if app.config.get('DEBUG') else ('Page not found', 404)
    
    @app.errorhandler(403)
    def forbidden_error(error):
        logger.warning(f"403 error: {request.url}")
        return render_template('403.html'), 403 if app.config.get('DEBUG') else ('Access forbidden', 403)
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"500 error: {str(error)}\n{traceback.format_exc()}")
        db.session.rollback()
        return render_template('500.html'), 500 if app.config.get('DEBUG') else ('Internal server error', 500)
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error(f"Unhandled exception: {str(error)}\n{traceback.format_exc()}")
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'An unexpected error occurred'}), 500
    
    @app.route('/')
    def index():
        try:
            # Track visitor
            track_visitor()
            
            if current_user.is_authenticated:
                return redirect(url_for('home'))
            return redirect(url_for('login'))
        except Exception as e:
            logger.error(f"Error in index route: {str(e)}")
            return redirect(url_for('login'))
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        try:
            if request.method == 'POST':
                username = request.form.get('username', '').strip()
                email = request.form.get('email', '').strip()
                password = request.form.get('password', '')
                age = request.form.get('age', '').strip()
                favorite_poet = request.form.get('favorite_poet', '').strip()
                
                # Validate inputs
                username_valid, username_msg = User.validate_username(username)
                if not username_valid:
                    return render_template('register.html', error=username_msg)
                
                email_valid, email_msg = User.validate_email(email)
                if not email_valid:
                    return render_template('register.html', error=email_msg)
                
                if not password or len(password) < 6:
                    return render_template('register.html', error='Password must be at least 6 characters')
                
                # Check for existing users
                if User.query.filter_by(username=username).first():
                    return render_template('register.html', error='Username already exists')
                
                if User.query.filter_by(email=email).first():
                    return render_template('register.html', error='Email already exists')
                
                # Validate age
                try:
                    age_int = int(age) if age else None
                    if age_int and (age_int < 13 or age_int > 120):
                        return render_template('register.html', error='Please enter a valid age')
                except ValueError:
                    return render_template('register.html', error='Please enter a valid age')
                
                # Make first user admin
                is_first_user = User.query.count() == 0
                
                user = User(
                    username=username,
                    email=email,
                    age=age_int,
                    favorite_poet=favorite_poet if favorite_poet else None,
                    is_admin=is_first_user
                )
                user.set_password(password)
                
                db.session.add(user)
                db.session.commit()
                
                login_user(user)
                logger.info(f"New user registered: {username}")
                return redirect(url_for('home'))
            
            return render_template('register.html')
        except Exception as e:
            logger.error(f"Error in register route: {str(e)}")
            db.session.rollback()
            return render_template('register.html', error='Registration failed. Please try again.')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        try:
            if request.method == 'POST':
                username = request.form.get('username', '').strip()
                password = request.form.get('password', '')
                
                if not username or not password:
                    return render_template('login.html', error='Username and password are required')
                
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
                    logger.info(f"User logged in: {user.username}")
                    return redirect(url_for('home'))
                
                return render_template('login.html', error='Invalid username or password')
            
            return render_template('login.html')
        except Exception as e:
            logger.error(f"Error in login route: {str(e)}")
            return render_template('login.html', error='Login failed. Please try again.')
    

    
    @app.route('/logout')
    @login_required
    def logout():
        try:
            username = current_user.username
            logout_user()
            logger.info(f"User logged out: {username}")
            return redirect(url_for('login'))
        except Exception as e:
            logger.error(f"Error in logout route: {str(e)}")
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
        try:
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
                poems = Poem.query.filter(
                    Poem.user_id.in_(following_ids),
                    Poem.is_classic == False
                ).order_by(Poem.created_at.desc()).limit(50).all()  # Limit for performance
            else:
                # If not following anyone, show all user poems (not classic) to help discover
                poems = Poem.query.filter_by(is_classic=False).order_by(Poem.created_at.desc()).limit(50).all()
            
            # Get saved poem IDs for current user
            saved_poem_ids = [s.poem_id for s in SavedPoem.query.filter_by(user_id=current_user.id).all()]
            
            # Check if user should see tutorial
            show_tutorial = not current_user.has_seen_tutorial
            
            return render_template('home.html', poems=poems, greeting=greeting, saved_poem_ids=saved_poem_ids, show_tutorial=show_tutorial)
        except Exception as e:
            logger.error(f"Error in home route: {str(e)}")
            return render_template('home.html', poems=[], greeting="Hello", saved_poem_ids=[], show_tutorial=False, error='Failed to load home page')
    
    @app.route('/new-poem', methods=['GET', 'POST'])
    @login_required
    def new_poem():
        try:
            if request.method == 'POST':
                title = request.form.get('title', '').strip()
                content = request.form.get('content', '').strip()
                category = request.form.get('category', '').strip()
                mood = request.form.get('mood', '').strip()
                theme = request.form.get('theme', '').strip()
                is_anonymous = request.form.get('anonymous') == 'on'
                
                # Validate inputs
                title_valid, title_msg = Poem.validate_title(title)
                if not title_valid:
                    return render_template('new_poem.html', error=title_msg)
                
                content_valid, content_msg = Poem.validate_content(content)
                if not content_valid:
                    return render_template('new_poem.html', error=content_msg)
                
                poem = Poem(
                    title=title,
                    content=content,
                    category=category if category else None,
                    mood=mood if mood else None,
                    theme=theme if theme else None,
                    user_id=current_user.id,
                    is_anonymous=is_anonymous
                )
                db.session.add(poem)
                db.session.commit()
                
                logger.info(f"New poem created by {current_user.username}: {title}")
                return redirect(url_for('home'))
            
            # Get existing options for dropdowns
            categories = db.session.query(Poem.category).filter(Poem.category.isnot(None)).distinct().all()
            moods = db.session.query(Poem.mood).filter(Poem.mood.isnot(None)).distinct().all()
            themes = db.session.query(Poem.theme).filter(Poem.theme.isnot(None)).distinct().all()
            
            existing_categories = [c[0] for c in categories if c[0]]
            existing_moods = [m[0] for m in moods if m[0]]
            existing_themes = [t[0] for t in themes if t[0]]
            
            return render_template('new_poem.html', 
                                 existing_categories=existing_categories,
                                 existing_moods=existing_moods,
                                 existing_themes=existing_themes)
        except Exception as e:
            logger.error(f"Error in new_poem route: {str(e)}")
            db.session.rollback()
            return render_template('new_poem.html', error='Failed to create poem. Please try again.')
    
    @app.route('/users')
    @login_required
    def users():
        try:
            from models import Follow
            # Only show real users, not classic poets
            classic_poet_names = ['Shakespeare', 'Rumi', 'Emily Dickinson', 'Edgar Allan Poe', 
                                 'Walt Whitman', 'Lord Byron', 'William Wordsworth', 
                                 'John Keats', 'Percy Shelley', 'Robert Burns',
                                 'Robert Frost', 'Maya Angelou', 'Langston Hughes',
                                 'المتنبي', 'قيس بن الملوح']
            all_users = User.query.filter(
                ~User.username.in_(classic_poet_names)
            ).order_by(User.created_at.desc()).limit(100).all()  # Limit for performance
            
            # Get IDs of users current user follows
            current_user_following_ids = [f.followed_id for f in Follow.query.filter_by(follower_id=current_user.id).all()]
            
            return render_template('users.html', users=all_users, current_user_following_ids=current_user_following_ids)
        except Exception as e:
            logger.error(f"Error in users route: {str(e)}")
            return render_template('users.html', users=[], current_user_following_ids=[], error='Failed to load users')
    
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
        try:
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            favorite_poet = request.form.get('favorite_poet', '').strip()
            
            if username and username != current_user.username:
                # Validate username
                username_valid, username_msg = User.validate_username(username)
                if not username_valid:
                    return render_template('settings.html', message=username_msg, message_type='error')
                
                if User.query.filter_by(username=username).first():
                    return render_template('settings.html', message='Username already taken', message_type='error')
                current_user.username = username
            
            if email and email != current_user.email:
                # Validate email
                email_valid, email_msg = User.validate_email(email)
                if not email_valid:
                    return render_template('settings.html', message=email_msg, message_type='error')
                
                if User.query.filter_by(email=email).first():
                    return render_template('settings.html', message='Email already in use', message_type='error')
                current_user.email = email
            
            if favorite_poet:
                current_user.favorite_poet = favorite_poet
            
            db.session.commit()
            logger.info(f"Profile updated for user: {current_user.username}")
            return render_template('settings.html', message='Profile updated successfully!', message_type='success')
        except Exception as e:
            logger.error(f"Error in update_profile route: {str(e)}")
            db.session.rollback()
            return render_template('settings.html', message='Failed to update profile', message_type='error')
    
    @app.route('/settings/password', methods=['POST'])
    @login_required
    def change_password():
        try:
            old_password = request.form.get('old_password', '')
            new_password = request.form.get('new_password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            if not old_password or not new_password or not confirm_password:
                return render_template('settings.html', message='All password fields are required', message_type='error')
            
            if not current_user.check_password(old_password):
                return render_template('settings.html', message='Current password is incorrect', message_type='error')
            
            if new_password != confirm_password:
                return render_template('settings.html', message='New passwords do not match', message_type='error')
            
            if len(new_password) < 6:
                return render_template('settings.html', message='New password must be at least 6 characters', message_type='error')
            
            current_user.set_password(new_password)
            db.session.commit()
            logger.info(f"Password changed for user: {current_user.username}")
            return render_template('settings.html', message='Password changed successfully!', message_type='success')
        except ValueError as e:
            return render_template('settings.html', message=str(e), message_type='error')
        except Exception as e:
            logger.error(f"Error in change_password route: {str(e)}")
            db.session.rollback()
            return render_template('settings.html', message='Failed to change password', message_type='error')
    
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
        try:
            if not current_user.is_admin:
                abort(403)
            
            from models import UserActivity, Visitor
            from datetime import datetime, timedelta
            
            total_users = User.query.count()
            total_poems = Poem.query.count()
            total_comments = Comment.query.count()
            all_users = User.query.order_by(User.created_at.desc()).limit(100).all()  # Limit for performance
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
        except Exception as e:
            logger.error(f"Error in admin route: {str(e)}")
            abort(500)
    
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
        try:
            from models import Notification, SavedPoem
            poem = Poem.query.get_or_404(poem_id)
            
            if request.method == 'POST':
                comment_text = request.form.get('comment', '').strip()
                
                # Validate comment
                comment_valid, comment_msg = Comment.validate_content(comment_text)
                if not comment_valid:
                    is_saved = SavedPoem.query.filter_by(user_id=current_user.id, poem_id=poem_id).first() is not None
                    return render_template('poem_detail.html', poem=poem, is_saved=is_saved, error=comment_msg)
                
                comment = Comment(content=comment_text, user_id=current_user.id, poem_id=poem_id)
                db.session.add(comment)
                
                # Create notification for poem author
                if poem.user_id != current_user.id:
                    notif = Notification.create_notification(
                        user_id=poem.user_id,
                        notif_type='comment',
                        message=f'{current_user.username} commented on your poem "{poem.title}"',
                        poem_id=poem_id
                    )
                    if notif:
                        db.session.add(notif)
                
                db.session.commit()
                logger.info(f"Comment added by {current_user.username} on poem {poem_id}")
                return redirect(url_for('poem_detail', poem_id=poem_id))
            
            # Check if poem is saved by current user
            is_saved = SavedPoem.query.filter_by(user_id=current_user.id, poem_id=poem_id).first() is not None
            
            return render_template('poem_detail.html', poem=poem, is_saved=is_saved)
        except Exception as e:
            logger.error(f"Error in poem_detail route: {str(e)}")
            if request.method == 'POST':
                db.session.rollback()
            abort(500)
    
    @app.route('/poem/<int:poem_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_poem(poem_id):
        try:
            poem = Poem.query.get_or_404(poem_id)
            
            # Check permissions
            if poem.user_id != current_user.id and not current_user.is_admin:
                abort(403)
            
            if request.method == 'POST':
                title = request.form.get('title', '').strip()
                content = request.form.get('content', '').strip()
                
                # Validate inputs
                title_valid, title_msg = Poem.validate_title(title)
                if not title_valid:
                    return render_template('edit_poem.html', poem=poem, error=title_msg)
                
                content_valid, content_msg = Poem.validate_content(content)
                if not content_valid:
                    return render_template('edit_poem.html', poem=poem, error=content_msg)
                
                poem.title = title
                poem.content = content
                db.session.commit()
                
                logger.info(f"Poem {poem_id} edited by {current_user.username}")
                return redirect(url_for('poem_detail', poem_id=poem_id))
            
            return render_template('edit_poem.html', poem=poem)
        except Exception as e:
            logger.error(f"Error in edit_poem route: {str(e)}")
            if request.method == 'POST':
                db.session.rollback()
            abort(500)
    
    @app.route('/poem/<int:poem_id>/delete', methods=['POST'])
    @login_required
    def delete_poem(poem_id):
        try:
            poem = Poem.query.get_or_404(poem_id)
            
            # Check permissions
            if poem.user_id != current_user.id and not current_user.is_admin:
                abort(403)
            
            poem_title = poem.title
            db.session.delete(poem)
            db.session.commit()
            
            logger.info(f"Poem {poem_id} ({poem_title}) deleted by {current_user.username}")
            return redirect(url_for('home'))
        except Exception as e:
            logger.error(f"Error in delete_poem route: {str(e)}")
            db.session.rollback()
            abort(500)
    
    @app.route('/poem/<int:poem_id>/save', methods=['POST'])
    @login_required
    def toggle_save_poem(poem_id):
        try:
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
        except Exception as e:
            logger.error(f"Error in toggle_save_poem route: {str(e)}")
            db.session.rollback()
            return jsonify({'status': 'error', 'message': 'Failed to toggle save'}), 500
    
    @app.route('/saved-poems')
    @login_required
    def saved_poems():
        from models import SavedPoem
        saved = SavedPoem.query.filter_by(user_id=current_user.id).order_by(SavedPoem.saved_at.desc()).all()
        poems = [s.poem for s in saved]
        return render_template('saved_poems.html', poems=poems)
    
    @app.route('/collections')
    @login_required
    def collections():
        try:
            from models import Collection
            user_collections = Collection.query.filter_by(user_id=current_user.id).order_by(Collection.created_at.desc()).all()
            return render_template('collections.html', collections=user_collections)
        except Exception as e:
            logger.error(f"Error in collections route: {str(e)}")
            return render_template('collections.html', collections=[], error='Failed to load collections')
    
    @app.route('/collections/new', methods=['GET', 'POST'])
    @login_required
    def new_collection():
        try:
            if request.method == 'POST':
                name = request.form.get('name', '').strip()
                description = request.form.get('description', '').strip()
                is_private = request.form.get('private') == 'on'
                
                if not name:
                    return render_template('new_collection.html', error='Collection name is required')
                
                if len(name) > 100:
                    return render_template('new_collection.html', error='Collection name must be less than 100 characters')
                
                from models import Collection
                collection = Collection(
                    name=name,
                    description=description if description else None,
                    user_id=current_user.id,
                    is_private=is_private
                )
                db.session.add(collection)
                db.session.commit()
                
                logger.info(f"New collection created by {current_user.username}: {name}")
                return redirect(url_for('collections'))
            
            return render_template('new_collection.html')
        except Exception as e:
            logger.error(f"Error in new_collection route: {str(e)}")
            db.session.rollback()
            return render_template('new_collection.html', error='Failed to create collection')
    
    @app.route('/collections/<int:collection_id>')
    @login_required
    def view_collection(collection_id):
        try:
            from models import Collection, CollectionPoem
            collection = Collection.query.get_or_404(collection_id)
            
            # Check permissions
            if collection.is_private and collection.user_id != current_user.id:
                abort(403)
            
            # Get poems in collection
            collection_poems = CollectionPoem.query.filter_by(collection_id=collection_id).order_by(CollectionPoem.added_at.desc()).all()
            poems = [cp.poem for cp in collection_poems]
            
            return render_template('view_collection.html', collection=collection, poems=poems)
        except Exception as e:
            logger.error(f"Error in view_collection route: {str(e)}")
            abort(500)
    
    @app.route('/collections/<int:collection_id>/add-poem/<int:poem_id>', methods=['POST'])
    @login_required
    def add_poem_to_collection(collection_id, poem_id):
        try:
            from models import Collection, CollectionPoem
            collection = Collection.query.get_or_404(collection_id)
            
            # Check permissions
            if collection.user_id != current_user.id:
                return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
            
            # Check if poem already in collection
            existing = CollectionPoem.query.filter_by(collection_id=collection_id, poem_id=poem_id).first()
            if existing:
                return jsonify({'status': 'error', 'message': 'Poem already in collection'})
            
            # Add poem to collection
            collection_poem = CollectionPoem(collection_id=collection_id, poem_id=poem_id)
            db.session.add(collection_poem)
            db.session.commit()
            
            return jsonify({'status': 'success', 'message': 'Poem added to collection'})
        except Exception as e:
            logger.error(f"Error adding poem to collection: {str(e)}")
            db.session.rollback()
            return jsonify({'status': 'error', 'message': 'Failed to add poem'}), 500
    @app.route('/poem/<int:poem_id>/like', methods=['POST'])
    @login_required
    def toggle_like_poem(poem_id):
        try:
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
                    notif = Notification.create_notification(
                        user_id=poem.user_id,
                        notif_type='like',
                        message=f'{current_user.username} liked your poem "{poem.title}"',
                        poem_id=poem_id
                    )
                    if notif:
                        db.session.add(notif)
            
            db.session.commit()
            like_count = Like.query.filter_by(poem_id=poem_id).count()
            return jsonify({'status': 'success', 'action': action, 'count': like_count})
        except Exception as e:
            logger.error(f"Error in toggle_like_poem route: {str(e)}")
            db.session.rollback()
            return jsonify({'status': 'error', 'message': 'Failed to toggle like'}), 500

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
    
    @app.route('/analytics')
    @login_required
    def user_analytics():
        """User analytics dashboard - Premium feature"""
        try:
            # Check subscription tier
            if current_user.subscription_tier == 'free':
                return render_template('analytics.html', 
                                     error='Analytics are available for Poetry Plus and Pro subscribers only',
                                     is_premium_feature=True)
            
            from models import Like, Comment, SavedPoem
            from datetime import datetime, timedelta
            
            # Get user's poems
            user_poems = Poem.query.filter_by(user_id=current_user.id, is_classic=False).all()
            poem_ids = [p.id for p in user_poems]
            
            if not poem_ids:
                return render_template('analytics.html', 
                                     total_poems=0,
                                     total_likes=0,
                                     total_comments=0,
                                     total_saves=0,
                                     poems=[])
            
            # Calculate totals
            total_poems = len(user_poems)
            total_likes = Like.query.filter(Like.poem_id.in_(poem_ids)).count()
            total_comments = Comment.query.filter(Comment.poem_id.in_(poem_ids)).count()
            total_saves = SavedPoem.query.filter(SavedPoem.poem_id.in_(poem_ids)).count()
            
            # Get poem performance
            poem_stats = []
            for poem in user_poems:
                likes = Like.query.filter_by(poem_id=poem.id).count()
                comments = Comment.query.filter_by(poem_id=poem.id).count()
                saves = SavedPoem.query.filter_by(poem_id=poem.id).count()
                
                poem_stats.append({
                    'poem': poem,
                    'likes': likes,
                    'comments': comments,
                    'saves': saves,
                    'total_engagement': likes + comments + saves
                })
            
            # Sort by engagement
            poem_stats.sort(key=lambda x: x['total_engagement'], reverse=True)
            
            # Recent activity (last 30 days)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_likes = Like.query.filter(
                Like.poem_id.in_(poem_ids),
                Like.created_at >= thirty_days_ago
            ).count()
            
            recent_comments = Comment.query.filter(
                Comment.poem_id.in_(poem_ids),
                Comment.created_at >= thirty_days_ago
            ).count()
            
            return render_template('analytics.html',
                                 total_poems=total_poems,
                                 total_likes=total_likes,
                                 total_comments=total_comments,
                                 total_saves=total_saves,
                                 recent_likes=recent_likes,
                                 recent_comments=recent_comments,
                                 poem_stats=poem_stats[:10])  # Top 10 poems
        except Exception as e:
            logger.error(f"Error in user_analytics route: {str(e)}")
            return render_template('analytics.html', error='Failed to load analytics')
    
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
        try:
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
                notif = Notification.create_notification(
                    user_id=user_id,
                    notif_type='follow',
                    message=f'{current_user.username} started following you'
                )
                if notif:
                    db.session.add(notif)
            
            db.session.commit()
            followers_count = Follow.query.filter_by(followed_id=user_id).count()
            logger.info(f"User {current_user.username} {action} user {user.username}")
            return jsonify({'status': 'success', 'action': action, 'followers_count': followers_count})
        except Exception as e:
            logger.error(f"Error in toggle_follow route: {str(e)}")
            db.session.rollback()
            return jsonify({'status': 'error', 'message': 'Failed to toggle follow'}), 500
    
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
        try:
            query = request.args.get('q', '').strip()
            mood_filter = request.args.get('mood', '').strip()
            theme_filter = request.args.get('theme', '').strip()
            category_filter = request.args.get('category', '').strip()
            poet_filter = request.args.get('poet', '').strip()
            sort_by = request.args.get('sort', 'recent')  # recent, popular, oldest
            
            poems = []
            
            if query or mood_filter or theme_filter or category_filter or poet_filter:
                # Build query
                search_query = Poem.query.join(User)
                
                # Text search
                if query:
                    if len(query) > 200:
                        query = query[:200]
                    search_query = search_query.filter(
                        db.or_(
                            Poem.title.ilike(f'%{query}%'),
                            Poem.content.ilike(f'%{query}%'),
                            User.username.ilike(f'%{query}%')
                        )
                    )
                
                # Mood filter
                if mood_filter:
                    search_query = search_query.filter(Poem.mood.ilike(f'%{mood_filter}%'))
                
                # Theme filter
                if theme_filter:
                    search_query = search_query.filter(Poem.theme.ilike(f'%{theme_filter}%'))
                
                # Category filter
                if category_filter:
                    search_query = search_query.filter(Poem.category.ilike(f'%{category_filter}%'))
                
                # Poet filter
                if poet_filter:
                    search_query = search_query.filter(User.username.ilike(f'%{poet_filter}%'))
                
                # Sorting
                if sort_by == 'popular':
                    # Sort by like count (requires subquery)
                    from models import Like
                    like_counts = db.session.query(
                        Like.poem_id,
                        db.func.count(Like.id).label('like_count')
                    ).group_by(Like.poem_id).subquery()
                    
                    search_query = search_query.outerjoin(like_counts, Poem.id == like_counts.c.poem_id)
                    search_query = search_query.order_by(db.desc(like_counts.c.like_count))
                elif sort_by == 'oldest':
                    search_query = search_query.order_by(Poem.created_at.asc())
                else:  # recent
                    search_query = search_query.order_by(Poem.created_at.desc())
                
                poems = search_query.limit(100).all()
            
            # Get available filter options
            moods = db.session.query(Poem.mood).filter(Poem.mood.isnot(None)).distinct().all()
            themes = db.session.query(Poem.theme).filter(Poem.theme.isnot(None)).distinct().all()
            categories = db.session.query(Poem.category).filter(Poem.category.isnot(None)).distinct().all()
            
            moods = [m[0] for m in moods if m[0]]
            themes = [t[0] for t in themes if t[0]]
            categories = [c[0] for c in categories if c[0]]
            
            return render_template('search.html', 
                                 poems=poems, 
                                 query=query,
                                 mood_filter=mood_filter,
                                 theme_filter=theme_filter,
                                 category_filter=category_filter,
                                 poet_filter=poet_filter,
                                 sort_by=sort_by,
                                 moods=moods,
                                 themes=themes,
                                 categories=categories)
        except Exception as e:
            logger.error(f"Error in search route: {str(e)}")
            return render_template('search.html', poems=[], query='', error='Search failed')
    
    @app.route('/discover')
    @login_required
    def discover():
        from models import Follow
        import random
        
        mood = request.args.get('mood', '')
        
        if mood:
            # Mood-based discovery
            poems = Poem.query.filter(
                Poem.mood.ilike(f'%{mood}%')
            ).order_by(Poem.created_at.desc()).limit(50).all()
            
            # Shuffle for variety
            random.shuffle(poems)
            
            return render_template('discover.html', poems=poems[:20], selected_mood=mood, is_mood_discovery=True)
        
        # Regular user discovery
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
        
        # Get available moods for mood discovery
        moods = db.session.query(Poem.mood).filter(Poem.mood.isnot(None)).distinct().all()
        available_moods = [m[0] for m in moods if m[0]]
        
        return render_template('discover.html', suggested_users=suggested_users[:10], available_moods=available_moods)
    
    @app.route('/themes')
    @login_required
    def themes():
        """Thematic channels - browse poems by theme"""
        try:
            theme = request.args.get('theme', '')
            
            # Get all available themes
            themes = db.session.query(Poem.theme).filter(Poem.theme.isnot(None)).distinct().all()
            available_themes = [t[0] for t in themes if t[0]]
            
            poems = []
            if theme:
                poems = Poem.query.filter(
                    Poem.theme.ilike(f'%{theme}%')
                ).order_by(Poem.created_at.desc()).limit(50).all()
            
            return render_template('themes.html', poems=poems, available_themes=available_themes, selected_theme=theme)
        except Exception as e:
            logger.error(f"Error in themes route: {str(e)}")
            return render_template('themes.html', poems=[], available_themes=[], selected_theme='', error='Failed to load themes')
    
    @app.route('/notifications')
    @login_required
    def notifications():
        try:
            from models import Notification
            notifs = Notification.query.filter_by(
                user_id=current_user.id
            ).order_by(Notification.created_at.desc()).limit(100).all()  # Limit for performance
            
            # Mark as read
            for notif in notifs:
                notif.is_read = True
            db.session.commit()
            
            return render_template('notifications.html', notifications=notifs)
        except Exception as e:
            logger.error(f"Error in notifications route: {str(e)}")
            db.session.rollback()
            return render_template('notifications.html', notifications=[], error='Failed to load notifications')
    
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
            if not data:
                return jsonify({'status': 'error', 'message': 'Invalid request'}), 400
            
            ip_address = request.remote_addr
            user_agent = data.get('userAgent', '')[:255]
            referrer = data.get('referrer', '')[:255]
            nickname = data.get('nickname', '')[:100] if data.get('nickname') else None
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
                    nickname=nickname,
                    source=source,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    referrer=referrer if referrer else None
                )
                db.session.add(visitor)
            
            db.session.commit()
            return jsonify({'status': 'success'})
        except Exception as e:
            logger.error(f"Error tracking Instagram visitor: {str(e)}")
            db.session.rollback()
            return jsonify({'status': 'error', 'message': 'Tracking failed'}), 500
    
    @app.route('/api/check-new-notifications')
    @login_required
    def check_new_notifications():
        """API endpoint for desktop notifications - returns unread notifications"""
        try:
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
        except Exception as e:
            logger.error(f"Error in check_new_notifications route: {str(e)}")
            return jsonify({'notifications': []}), 500
    
    @app.route('/mark-tutorial-seen', methods=['POST'])
    @login_required
    def mark_tutorial_seen():
        """Mark that user has seen the onboarding tutorial"""
        try:
            current_user.has_seen_tutorial = True
            db.session.commit()
            logger.info(f"Tutorial marked as seen for user: {current_user.username}")
            return jsonify({'status': 'success'})
        except Exception as e:
            logger.error(f"Error in mark_tutorial_seen route: {str(e)}")
            db.session.rollback()
            return jsonify({'status': 'error', 'message': 'Failed to update tutorial status'}), 500
    
    @app.route('/chat-with-poet')
    @login_required
    def chat_page():
        return render_template('chat.html')
    
    @app.route('/chat', methods=['POST'])
    @login_required
    def chat():
        try:
            data = request.get_json()
            if not data:
                return jsonify({'response': 'Invalid request'}), 400
            
            user_message = data.get('message', '').strip()
            
            if not user_message:
                return jsonify({'response': 'Please enter a message'})
            
            # Limit message length
            if len(user_message) > 500:
                return jsonify({'response': 'Message too long. Please keep it under 500 characters.'})
            
            poet = current_user.favorite_poet
            
            if not poet:
                return jsonify({'response': 'Please set your favorite poet in settings first.'})
            
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
                    },
                    timeout=30)
                
                if response.status_code == 200:
                    ai_response = response.json()['response']
                    return jsonify({'response': ai_response})
                else:
                    logger.warning(f"Ollama API returned status {response.status_code}")
                    return jsonify({'response': 'Alas, I seem to have lost my voice momentarily. Please try again.'})
            except requests.exceptions.Timeout:
                logger.error("Ollama API timeout")
                return jsonify({'response': 'The poet is taking too long to respond. Please try again.'})
            except requests.exceptions.ConnectionError:
                logger.error("Cannot connect to Ollama")
                return jsonify({'response': 'My connection to the muse has been interrupted. Ensure Ollama is running.'})
            except Exception as e:
                logger.error(f"Error calling Ollama API: {str(e)}")
                return jsonify({'response': 'An error occurred while connecting to the poet.'})
        except Exception as e:
            logger.error(f"Error in chat route: {str(e)}")
            return jsonify({'response': 'An unexpected error occurred'}), 500
    
    with app.app_context():
        try:
            db.create_all()
            
            # Auto-seed database if empty
            if Poem.query.count() == 0:
                logger.info("Database is empty. Auto-seeding with classic poems...")
                from seed_poems import FAMOUS_POEMS
                from werkzeug.security import generate_password_hash
                
                for poet_name, poems in FAMOUS_POEMS.items():
                    try:
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
                            try:
                                poem = Poem(
                                    title=poem_data['title'][:200],
                                    content=poem_data['content'][:50000],
                                    category=poem_data.get('category', 'general'),
                                    user_id=poet_user.id,
                                    is_classic=True
                                )
                                db.session.add(poem)
                            except Exception as e:
                                logger.error(f"Error adding poem {poem_data.get('title', 'Unknown')}: {str(e)}")
                                continue
                    except Exception as e:
                        logger.error(f"Error processing poet {poet_name}: {str(e)}")
                        continue
                
                db.session.commit()
                logger.info("✅ Database auto-seeded with classic poems!")
        except Exception as e:
            logger.error(f"Error during database initialization: {str(e)}")
            db.session.rollback()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
