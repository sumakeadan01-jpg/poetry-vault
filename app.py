from flask import Flask, render_template, request, redirect, url_for, flash, abort, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, Poem, Comment
import requests

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
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        return redirect(url_for('login'))
    
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
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            # Check for admin secret code
            admin_code = 'P0.1'
            is_admin_login = username.startswith(admin_code)
            
            # Remove admin code from username for lookup
            if is_admin_login:
                actual_username = username[len(admin_code):]
            else:
                actual_username = username
            
            user = User.query.filter_by(username=actual_username).first()
            
            if user and user.check_password(password):
                # Grant admin access if they used the code
                if is_admin_login:
                    user.is_admin = True
                    db.session.commit()
                
                login_user(user)
                return redirect(url_for('home'))
            
            return render_template('login.html', error='Invalid username or password')
        
        return render_template('login.html')
    

    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))
    
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
        
        return render_template('home.html', poems=poems, greeting=greeting, saved_poem_ids=saved_poem_ids)
    
    @app.route('/new-poem', methods=['GET', 'POST'])
    @login_required
    def new_poem():
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            
            poem = Poem(title=title, content=content, user_id=current_user.id)
            db.session.add(poem)
            db.session.commit()
            
            return redirect(url_for('home'))
        
        return render_template('new_poem.html')
    
    @app.route('/users')
    @login_required
    def users():
        # Only show real users, not classic poets
        classic_poet_names = ['Shakespeare', 'Rumi', 'Emily Dickinson', 'Edgar Allan Poe', 
                             'Walt Whitman', 'Lord Byron', 'William Wordsworth', 
                             'John Keats', 'Percy Shelley', 'Robert Burns']
        all_users = User.query.filter(~User.username.in_(classic_poet_names)).order_by(User.created_at.desc()).all()
        return render_template('users.html', users=all_users)
    
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
    
    @app.route('/admin')
    @login_required
    def admin():
        if not current_user.is_admin:
            abort(403)
        
        total_users = User.query.count()
        total_poems = Poem.query.count()
        total_comments = Comment.query.count()
        all_users = User.query.order_by(User.created_at.desc()).all()
        recent_poems = Poem.query.order_by(Poem.created_at.desc()).limit(10).all()
        
        return render_template('admin.html', 
                             total_users=total_users,
                             total_poems=total_poems,
                             total_comments=total_comments,
                             users=all_users,
                             poems=recent_poems)
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
                             'John Keats', 'Percy Shelley', 'Robert Burns']
        
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
