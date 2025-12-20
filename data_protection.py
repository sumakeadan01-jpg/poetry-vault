"""
User Data Protection System for Poetry Vault
Encrypts sensitive data and provides privacy controls
"""

import hashlib
import json
from datetime import datetime
from cryptography.fernet import Fernet
from flask import current_app
from models import db, User, Poem, Comment
import os

class DataProtectionManager:
    """Manages encryption and protection of user data"""
    
    def __init__(self):
        self.encryption_key = self._get_or_create_key()
        self.cipher = Fernet(self.encryption_key)
    
    def _get_or_create_key(self):
        """Get or create encryption key"""
        key_file = 'instance/encryption.key'
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # Create new key
            key = Fernet.generate_key()
            os.makedirs('instance', exist_ok=True)
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def encrypt_sensitive_data(self, data):
        """Encrypt sensitive user data"""
        if not data:
            return None
        
        if isinstance(data, str):
            data = data.encode()
        elif isinstance(data, dict):
            data = json.dumps(data).encode()
        
        return self.cipher.encrypt(data).decode()
    
    def decrypt_sensitive_data(self, encrypted_data):
        """Decrypt sensitive user data"""
        if not encrypted_data:
            return None
        
        try:
            decrypted = self.cipher.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except Exception:
            return None
    
    def hash_user_identifier(self, identifier):
        """Create anonymous hash of user identifier"""
        salt = current_app.config.get('SECRET_KEY', 'default_salt')
        return hashlib.sha256(f"{identifier}{salt}".encode()).hexdigest()[:16]
    
    def anonymize_user_data(self, user_data):
        """Anonymize user data for analytics"""
        if isinstance(user_data, dict):
            anonymized = user_data.copy()
            # Remove or hash sensitive fields
            sensitive_fields = ['email', 'username', 'password_hash']
            for field in sensitive_fields:
                if field in anonymized:
                    if field == 'email':
                        anonymized[field] = self.hash_user_identifier(anonymized[field])
                    elif field == 'username':
                        anonymized[field] = f"user_{self.hash_user_identifier(anonymized[field])}"
                    else:
                        del anonymized[field]
            return anonymized
        return user_data
    
    def create_privacy_settings(self, user_id):
        """Create default privacy settings for user"""
        privacy_settings = {
            'profile_visibility': 'public',  # public, friends, private
            'poem_visibility': 'public',
            'activity_visibility': 'friends',
            'allow_comments': True,
            'allow_follows': True,
            'email_notifications': True,
            'data_sharing': False
        }
        
        # Store encrypted privacy settings
        encrypted_settings = self.encrypt_sensitive_data(privacy_settings)
        
        # You would store this in a PrivacySettings table
        # For now, we'll add it to the user model
        return encrypted_settings
    
    def backup_user_data(self, user_id):
        """Create encrypted backup of user's data"""
        try:
            user = User.query.get(user_id)
            if not user:
                return None
            
            # Collect all user data
            user_poems = Poem.query.filter_by(user_id=user_id).all()
            user_comments = Comment.query.filter_by(user_id=user_id).all()
            
            backup_data = {
                'user_info': {
                    'username': user.username,
                    'email': user.email,
                    'age': user.age,
                    'favorite_poet': user.favorite_poet,
                    'created_at': user.created_at.isoformat() if user.created_at else None
                },
                'poems': [
                    {
                        'title': poem.title,
                        'content': poem.content,
                        'category': poem.category,
                        'mood': poem.mood,
                        'theme': poem.theme,
                        'created_at': poem.created_at.isoformat() if poem.created_at else None
                    }
                    for poem in user_poems
                ],
                'comments': [
                    {
                        'content': comment.content,
                        'poem_id': comment.poem_id,
                        'created_at': comment.created_at.isoformat() if comment.created_at else None
                    }
                    for comment in user_comments
                ],
                'backup_created': datetime.now().isoformat()
            }
            
            # Encrypt the backup
            encrypted_backup = self.encrypt_sensitive_data(backup_data)
            
            # Save to file
            backup_filename = f"instance/user_backups/user_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.backup"
            os.makedirs('instance/user_backups', exist_ok=True)
            
            with open(backup_filename, 'w') as f:
                f.write(encrypted_backup)
            
            return backup_filename
            
        except Exception as e:
            current_app.logger.error(f"Error creating user backup: {str(e)}")
            return None
    
    def delete_user_data(self, user_id, keep_backup=True):
        """Safely delete user data with optional backup"""
        try:
            if keep_backup:
                backup_file = self.backup_user_data(user_id)
                if not backup_file:
                    return False, "Failed to create backup"
            
            # Delete user's poems
            Poem.query.filter_by(user_id=user_id).delete()
            
            # Delete user's comments
            Comment.query.filter_by(user_id=user_id).delete()
            
            # Delete the user
            User.query.filter_by(id=user_id).delete()
            
            db.session.commit()
            
            return True, "User data deleted successfully"
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error deleting user data: {str(e)}")
            return False, f"Error deleting user data: {str(e)}"

# Global data protection manager
data_protection = DataProtectionManager()

def protect_user_content(user_id, content_type, content_id):
    """Add protection flag to user content"""
    try:
        if content_type == 'poem':
            poem = Poem.query.get(content_id)
            if poem and poem.user_id == user_id:
                # Add protection metadata (you'd extend the model for this)
                poem.is_protected = True
                db.session.commit()
                return True
        elif content_type == 'comment':
            comment = Comment.query.get(content_id)
            if comment and comment.user_id == user_id:
                comment.is_protected = True
                db.session.commit()
                return True
        return False
    except Exception:
        db.session.rollback()
        return False

def get_user_data_summary(user_id):
    """Get summary of user's data for privacy dashboard"""
    try:
        user = User.query.get(user_id)
        if not user:
            return None
        
        poems_count = Poem.query.filter_by(user_id=user_id).count()
        comments_count = Comment.query.filter_by(user_id=user_id).count()
        
        # Get recent activity (last 30 days)
        from datetime import timedelta
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        recent_poems = Poem.query.filter(
            Poem.user_id == user_id,
            Poem.created_at >= thirty_days_ago
        ).count()
        
        recent_comments = Comment.query.filter(
            Comment.user_id == user_id,
            Comment.created_at >= thirty_days_ago
        ).count()
        
        return {
            'total_poems': poems_count,
            'total_comments': comments_count,
            'recent_poems': recent_poems,
            'recent_comments': recent_comments,
            'account_created': user.created_at.isoformat() if user.created_at else None,
            'last_login': user.last_login.isoformat() if hasattr(user, 'last_login') and user.last_login else None
        }
        
    except Exception as e:
        current_app.logger.error(f"Error getting user data summary: {str(e)}")
        return None