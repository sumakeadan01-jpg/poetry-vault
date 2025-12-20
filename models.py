from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    favorite_poet = db.Column(db.String(100), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    has_seen_tutorial = db.Column(db.Boolean, default=False)
    subscription_tier = db.Column(db.String(20), default='free')  # free, plus, pro
    subscription_expires = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Privacy and Security fields
    privacy_settings = db.Column(db.Text, nullable=True)  # Encrypted JSON
    is_banned = db.Column(db.Boolean, default=False)
    ban_reason = db.Column(db.String(500), nullable=True)
    failed_login_attempts = db.Column(db.Integer, default=0)
    account_locked_until = db.Column(db.DateTime, nullable=True)
    email_verified = db.Column(db.Boolean, default=False)
    two_factor_enabled = db.Column(db.Boolean, default=False)
    data_sharing_consent = db.Column(db.Boolean, default=False)
    
    poems = db.relationship('Poem', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    saved_poems = db.relationship('SavedPoem', backref='user', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='user', lazy=True, cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy=True, cascade='all, delete-orphan')
    highlights = db.relationship('Highlight', backref='user', lazy=True, cascade='all, delete-orphan')
    
    # Follow relationships
    following = db.relationship('Follow', foreign_keys='Follow.follower_id', backref='follower', lazy='dynamic', cascade='all, delete-orphan')
    followers = db.relationship('Follow', foreign_keys='Follow.followed_id', backref='followed', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Set hashed password with validation"""
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        if not password:
            return False
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def validate_username(username):
        """Validate username format"""
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters"
        if len(username) > 80:
            return False, "Username must be less than 80 characters"
        if not re.match(r'^[a-zA-Z0-9_\u0600-\u06FF\s]+$', username):
            return False, "Username can only contain letters, numbers, underscores, and spaces"
        return True, "Valid"
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        if not email:
            return False, "Email is required"
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Invalid email format"
        return True, "Valid"
    
    # Security Methods
    def record_login(self):
        """Record successful login"""
        try:
            self.last_login = datetime.utcnow()
            self.failed_login_attempts = 0
            self.account_locked_until = None
            db.session.commit()
        except Exception:
            # Handle case where columns don't exist yet
            db.session.rollback()
    
    def record_failed_login(self):
        """Record failed login attempt"""
        try:
            self.failed_login_attempts += 1
            if self.failed_login_attempts >= 5:
                # Lock account for 30 minutes
                from datetime import timedelta
                self.account_locked_until = datetime.utcnow() + timedelta(minutes=30)
            db.session.commit()
        except Exception:
            # Handle case where columns don't exist yet
            db.session.rollback()
    
    def is_account_locked(self):
        """Check if account is locked"""
        try:
            if hasattr(self, 'is_banned') and self.is_banned:
                return True, getattr(self, 'ban_reason', 'Account is banned')
            
            if hasattr(self, 'account_locked_until') and self.account_locked_until:
                if datetime.utcnow() < self.account_locked_until:
                    return True, "Account is temporarily locked due to failed login attempts"
                else:
                    # Unlock account
                    self.account_locked_until = None
                    self.failed_login_attempts = 0
                    db.session.commit()
        except Exception:
            # Handle case where columns don't exist yet
            pass
        
        return False, None
    
    def get_privacy_settings(self):
        """Get user privacy settings"""
        try:
            if not hasattr(self, 'privacy_settings') or not self.privacy_settings:
                return {
                    'profile_visibility': 'public',
                    'poem_visibility': 'public',
                    'activity_visibility': 'friends',
                    'allow_comments': True,
                    'allow_follows': True,
                    'email_notifications': True
                }
            
            from data_protection import data_protection
            decrypted = data_protection.decrypt_sensitive_data(self.privacy_settings)
            import json
            return json.loads(decrypted) if decrypted else {}
        except:
            return {
                'profile_visibility': 'public',
                'poem_visibility': 'public',
                'activity_visibility': 'friends',
                'allow_comments': True,
                'allow_follows': True,
                'email_notifications': True
            }
    
    def update_privacy_settings(self, settings):
        """Update user privacy settings"""
        try:
            if not hasattr(self, 'privacy_settings'):
                return False
                
            from data_protection import data_protection
            import json
            self.privacy_settings = data_protection.encrypt_sensitive_data(settings)
            db.session.commit()
            return True
        except:
            return False
    
    def get_follower_count(self):
        """Get number of followers"""
        return self.followers.count()
    
    def get_following_count(self):
        """Get number of users being followed"""
        return self.following.count()
    
    def get_poem_count(self):
        """Get number of poems authored"""
        return Poem.query.filter_by(user_id=self.id, is_classic=False).count()
    
    def is_following(self, user):
        """Check if this user follows another user"""
        return self.following.filter_by(followed_id=user.id).first() is not None
    
    def __repr__(self):
        return f'<User {self.username}>'

class Poem(db.Model):
    __tablename__ = 'poems'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=True)  # love, nature, death, spirituality, etc.
    mood = db.Column(db.String(50), nullable=True)  # happy, sad, contemplative, passionate, etc.
    theme = db.Column(db.String(50), nullable=True)  # romance, loss, hope, rebellion, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_classic = db.Column(db.Boolean, default=False)  # Hide from home feed, show in search only
    is_anonymous = db.Column(db.Boolean, default=False)  # Post anonymously
    
    # Protection and Privacy fields
    is_protected = db.Column(db.Boolean, default=False)  # User-protected content
    visibility = db.Column(db.String(20), default='public')  # public, friends, private
    content_warning = db.Column(db.String(200), nullable=True)  # Content warning text
    is_flagged = db.Column(db.Boolean, default=False)  # Flagged for review
    flag_reason = db.Column(db.String(500), nullable=True)  # Reason for flagging
    
    comments = db.relationship('Comment', backref='poem', lazy=True, cascade='all, delete-orphan')
    saved_by = db.relationship('SavedPoem', backref='poem', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='poem', lazy=True, cascade='all, delete-orphan')
    
    @staticmethod
    def validate_title(title):
        """Validate poem title"""
        if not title or not title.strip():
            return False, "Title is required"
        if len(title) > 200:
            return False, "Title must be less than 200 characters"
        return True, "Valid"
    
    @staticmethod
    def validate_content(content):
        """Validate poem content"""
        if not content or not content.strip():
            return False, "Content is required"
        if len(content) < 10:
            return False, "Poem must be at least 10 characters"
        if len(content) > 50000:
            return False, "Poem must be less than 50,000 characters"
        return True, "Valid"
    
    def get_like_count(self):
        """Get number of likes"""
        return Like.query.filter_by(poem_id=self.id).count()
    
    def get_comment_count(self):
        """Get number of comments"""
        return Comment.query.filter_by(poem_id=self.id).count()
    
    def is_liked_by(self, user):
        """Check if user has liked this poem"""
        return Like.query.filter_by(user_id=user.id, poem_id=self.id).first() is not None
    
    def is_saved_by(self, user):
        """Check if user has saved this poem"""
        return SavedPoem.query.filter_by(user_id=user.id, poem_id=self.id).first() is not None
    
    def get_author_display_name(self):
        """Get display name (Anonymous or actual username)"""
        if self.is_anonymous:
            return "Anonymous"
        return self.author.username if self.author else "Unknown"
    
    def __repr__(self):
        return f'<Poem {self.title}>'

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    poem_id = db.Column(db.Integer, db.ForeignKey('poems.id'), nullable=False)
    
    # Protection fields
    is_protected = db.Column(db.Boolean, default=False)  # User-protected content
    is_flagged = db.Column(db.Boolean, default=False)  # Flagged for review
    flag_reason = db.Column(db.String(500), nullable=True)  # Reason for flagging
    
    @staticmethod
    def validate_content(content):
        """Validate comment content"""
        if not content or not content.strip():
            return False, "Comment cannot be empty"
        if len(content) > 5000:
            return False, "Comment must be less than 5,000 characters"
        return True, "Valid"
    
    def __repr__(self):
        return f'<Comment by {self.author.username} on Poem {self.poem_id}>'

class SavedPoem(db.Model):
    __tablename__ = 'saved_poems'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    poem_id = db.Column(db.Integer, db.ForeignKey('poems.id'), nullable=False)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'poem_id', name='unique_user_poem'),)

class Like(db.Model):
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    poem_id = db.Column(db.Integer, db.ForeignKey('poems.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'poem_id', name='unique_user_poem_like'),)

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'comment', 'like', 'follow'
    message = db.Column(db.String(255), nullable=False)
    poem_id = db.Column(db.Integer, db.ForeignKey('poems.id'), nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def create_notification(user_id, notif_type, message, poem_id=None):
        """Factory method to create notifications safely"""
        try:
            if not user_id or not notif_type or not message:
                return None
            
            notif = Notification(
                user_id=user_id,
                type=notif_type,
                message=message[:255],  # Truncate if too long
                poem_id=poem_id
            )
            return notif
        except Exception as e:
            print(f"Error creating notification: {e}")
            return None
    
    def __repr__(self):
        return f'<Notification {self.type} for User {self.user_id}>'

class Follow(db.Model):
    __tablename__ = 'follows'
    
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # User who follows
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # User being followed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('follower_id', 'followed_id', name='unique_follow'),)

class Highlight(db.Model):
    __tablename__ = 'highlights'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    poems = db.relationship('HighlightPoem', backref='highlight', lazy=True, cascade='all, delete-orphan')

class HighlightPoem(db.Model):
    __tablename__ = 'highlight_poems'
    
    id = db.Column(db.Integer, primary_key=True)
    highlight_id = db.Column(db.Integer, db.ForeignKey('highlights.id'), nullable=False)
    poem_id = db.Column(db.Integer, db.ForeignKey('poems.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('highlight_id', 'poem_id', name='unique_highlight_poem'),)

class UserActivity(db.Model):
    __tablename__ = 'user_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Null for anonymous visitors
    activity_type = db.Column(db.String(50), nullable=False)  # 'login', 'poem_created', 'like', 'comment', 'visit'
    description = db.Column(db.String(255), nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    referrer = db.Column(db.String(255), nullable=True)  # Where they came from (Instagram, direct, etc.)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to User
    user = db.relationship('User', backref='activities', foreign_keys=[user_id])

class Visitor(db.Model):
    __tablename__ = 'visitors'
    
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), nullable=True)  # Optional nickname from URL parameter
    source = db.Column(db.String(100), nullable=True)  # 'instagram', 'direct', 'google', etc.
    ip_address = db.Column(db.String(50), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    referrer = db.Column(db.String(255), nullable=True)
    first_visit = db.Column(db.DateTime, default=datetime.utcnow)
    last_visit = db.Column(db.DateTime, default=datetime.utcnow)
    visit_count = db.Column(db.Integer, default=1)

class Collection(db.Model):
    __tablename__ = 'collections'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_private = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    poems = db.relationship('CollectionPoem', backref='collection', lazy=True, cascade='all, delete-orphan')
    user = db.relationship('User', backref='collections')

class CollectionPoem(db.Model):
    __tablename__ = 'collection_poems'
    
    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id'), nullable=False)
    poem_id = db.Column(db.Integer, db.ForeignKey('poems.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    poem = db.relationship('Poem')
    __table_args__ = (db.UniqueConstraint('collection_id', 'poem_id', name='unique_collection_poem'),)

class UserAnalytics(db.Model):
    __tablename__ = 'user_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_views = db.Column(db.Integer, default=0)
    total_likes = db.Column(db.Integer, default=0)
    total_comments = db.Column(db.Integer, default=0)
    total_saves = db.Column(db.Integer, default=0)
    most_popular_poem_id = db.Column(db.Integer, db.ForeignKey('poems.id'), nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='analytics')
    most_popular_poem = db.relationship('Poem')
