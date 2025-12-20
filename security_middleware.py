"""
Security middleware for Poetry Vault
Protects user data, prevents spam, and adds security layers
"""

from functools import wraps
from flask import request, jsonify, session, current_app
from flask_login import current_user
from datetime import datetime, timedelta
import hashlib
import re
from models import db, User, Poem, Comment

class SecurityManager:
    """Comprehensive security management for Poetry Vault"""
    
    def __init__(self):
        self.rate_limits = {}
        self.failed_attempts = {}
        self.suspicious_ips = set()
    
    def rate_limit_check(self, user_id, action, limit=5, window_minutes=15):
        """Rate limiting for user actions"""
        now = datetime.now()
        key = f"{user_id}_{action}"
        
        if key not in self.rate_limits:
            self.rate_limits[key] = []
        
        # Clean old attempts
        self.rate_limits[key] = [
            timestamp for timestamp in self.rate_limits[key]
            if now - timestamp < timedelta(minutes=window_minutes)
        ]
        
        # Check if limit exceeded
        if len(self.rate_limits[key]) >= limit:
            return False
        
        # Add current attempt
        self.rate_limits[key].append(now)
        return True
    
    def validate_content(self, content, content_type="general"):
        """Validate and sanitize user content"""
        if not content or not isinstance(content, str):
            return False, "Content cannot be empty"
        
        content = content.strip()
        
        # Length checks
        if content_type == "poem":
            if len(content) < 10:
                return False, "Poem must be at least 10 characters"
            if len(content) > 50000:
                return False, "Poem is too long (max 50,000 characters)"
        elif content_type == "comment":
            if len(content) < 1:
                return False, "Comment cannot be empty"
            if len(content) > 1000:
                return False, "Comment is too long (max 1,000 characters)"
        elif content_type == "title":
            if len(content) < 1:
                return False, "Title cannot be empty"
            if len(content) > 200:
                return False, "Title is too long (max 200 characters)"
        
        # Check for spam patterns
        spam_patterns = [
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            r'\b(?:buy|sell|cheap|free|click|visit|www\.)\b',
            r'(.)\1{10,}',  # Repeated characters
        ]
        
        for pattern in spam_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return False, "Content appears to be spam"
        
        return True, content
    
    def check_user_permissions(self, user, action, target=None):
        """Check if user has permission for specific actions"""
        if not user or not user.is_authenticated:
            return False, "Authentication required"
        
        # Check if user is banned or suspended
        if hasattr(user, 'is_banned') and user.is_banned:
            return False, "Account is suspended"
        
        # Action-specific checks
        if action == "create_poem":
            if not self.rate_limit_check(user.id, "create_poem", limit=10, window_minutes=60):
                return False, "Too many poems created recently. Please wait."
        
        elif action == "create_comment":
            if not self.rate_limit_check(user.id, "create_comment", limit=20, window_minutes=15):
                return False, "Too many comments posted recently. Please wait."
        
        elif action == "like_poem":
            if not self.rate_limit_check(user.id, "like_poem", limit=50, window_minutes=15):
                return False, "Too many likes recently. Please wait."
        
        elif action == "follow_user":
            if not self.rate_limit_check(user.id, "follow_user", limit=10, window_minutes=60):
                return False, "Too many follow actions recently. Please wait."
        
        elif action == "edit_poem" and target:
            if target.user_id != user.id and not user.is_admin:
                return False, "You can only edit your own poems"
        
        elif action == "delete_poem" and target:
            if target.user_id != user.id and not user.is_admin:
                return False, "You can only delete your own poems"
        
        return True, "Permission granted"
    
    def sanitize_input(self, data):
        """Sanitize user input to prevent XSS and injection"""
        if isinstance(data, str):
            # Remove potentially dangerous characters
            data = re.sub(r'[<>"\']', '', data)
            # Limit length
            data = data[:1000]
            return data.strip()
        return data
    
    def log_security_event(self, event_type, user_id=None, details=None):
        """Log security events for monitoring"""
        timestamp = datetime.now().isoformat()
        ip_address = request.remote_addr if request else "unknown"
        
        log_entry = {
            'timestamp': timestamp,
            'event_type': event_type,
            'user_id': user_id,
            'ip_address': ip_address,
            'details': details
        }
        
        # In production, you'd want to log this to a file or monitoring service
        current_app.logger.warning(f"SECURITY EVENT: {log_entry}")

# Global security manager instance
security_manager = SecurityManager()

def require_permission(action):
    """Decorator to check permissions before executing actions"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'error': 'Authentication required'}), 401
            
            # Get target object if needed
            target = None
            if 'poem_id' in kwargs:
                from models import Poem
                target = Poem.query.get(kwargs['poem_id'])
            
            # Check permissions
            has_permission, message = security_manager.check_user_permissions(
                current_user, action, target
            )
            
            if not has_permission:
                security_manager.log_security_event(
                    'permission_denied',
                    current_user.id,
                    {'action': action, 'reason': message}
                )
                return jsonify({'error': message}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_content_input(content_type):
    """Decorator to validate content before processing"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get content from request
            content = None
            if request.method == 'POST':
                if content_type == 'poem':
                    content = request.form.get('content')
                elif content_type == 'comment':
                    content = request.form.get('content')
                elif content_type == 'title':
                    content = request.form.get('title')
            
            if content:
                is_valid, result = security_manager.validate_content(content, content_type)
                if not is_valid:
                    security_manager.log_security_event(
                        'invalid_content',
                        current_user.id if current_user.is_authenticated else None,
                        {'content_type': content_type, 'reason': result}
                    )
                    return jsonify({'error': result}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def protect_user_data():
    """Decorator to add general data protection"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Log access attempt
            if current_user.is_authenticated:
                security_manager.log_security_event(
                    'data_access',
                    current_user.id,
                    {'endpoint': request.endpoint, 'method': request.method}
                )
            
            # Add security headers
            response = f(*args, **kwargs)
            if hasattr(response, 'headers'):
                response.headers['X-Content-Type-Options'] = 'nosniff'
                response.headers['X-Frame-Options'] = 'DENY'
                response.headers['X-XSS-Protection'] = '1; mode=block'
            
            return response
        return decorated_function
    return decorator