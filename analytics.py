"""
Enhanced Analytics Tracking System
Comprehensive visitor tracking, user activity logging, and analytics reporting
"""
from flask import request
from models import db, UserActivity, Visitor
from flask_login import current_user
from datetime import datetime, timedelta
from functools import wraps
import logging

# Setup logger
logger = logging.getLogger(__name__)


class AnalyticsTracker:
    """Centralized analytics tracking with enhanced features"""
    
    # Source detection patterns
    SOCIAL_PATTERNS = {
        'instagram': ['instagram.com', 'ig.me', 'instagram'],
        'facebook': ['facebook.com', 'fb.com', 'fb.me', 'facebook'],
        'twitter': ['twitter.com', 't.co', 'x.com', 'twitter'],
        'linkedin': ['linkedin.com', 'lnkd.in', 'linkedin'],
        'pinterest': ['pinterest.com', 'pin.it', 'pinterest'],
        'reddit': ['reddit.com', 'redd.it', 'reddit'],
        'tiktok': ['tiktok.com', 'tiktok'],
        'youtube': ['youtube.com', 'youtu.be', 'youtube']
    }
    
    SEARCH_PATTERNS = {
        'google': ['google.com', 'google'],
        'bing': ['bing.com', 'bing'],
        'yahoo': ['yahoo.com', 'yahoo'],
        'duckduckgo': ['duckduckgo.com', 'ddg']
    }
    
    @staticmethod
    def get_source_from_referrer(referrer='', user_agent=''):
        """
        Intelligently determine traffic source from referrer and user agent
        
        Args:
            referrer: HTTP referrer URL
            user_agent: User agent string
        
        Returns:
            str: Detected source (instagram, facebook, google, direct, etc.)
        """
        if not referrer:
            # Check user agent for app signatures
            if user_agent:
                user_agent_lower = user_agent.lower()
                for source, patterns in AnalyticsTracker.SOCIAL_PATTERNS.items():
                    if any(pattern in user_agent_lower for pattern in patterns):
                        return source
            return 'direct'
        
        referrer_lower = referrer.lower()
        
        # Check social media sources
        for source, patterns in AnalyticsTracker.SOCIAL_PATTERNS.items():
            if any(pattern in referrer_lower for pattern in patterns):
                return source
        
        # Check search engines
        for source, patterns in AnalyticsTracker.SEARCH_PATTERNS.items():
            if any(pattern in referrer_lower for pattern in patterns):
                return source
        
        # Check if it's from same domain (internal navigation)
        if 'poetryvault' in referrer_lower or 'poetry-vault' in referrer_lower:
            return 'internal'
        
        return 'other'
    
    @staticmethod
    def extract_nickname_from_params():
        """
        Extract nickname from various URL parameter formats
        Supports: ?from=, ?ref=, ?u=, ?wist=, ?id=, ?source=
        """
        param_names = ['from', 'ref', 'u', 'wist', 'id', 'source', 'utm_source']
        
        for param in param_names:
            value = request.args.get(param)
            if value:
                # Clean and validate nickname
                nickname = value.strip()[:100]  # Limit length
                if nickname:
                    return nickname
        
        return None
    
    @staticmethod
    def track_visitor():
        """
        Track visitor information with enhanced detection
        
        Returns:
            bool: True if tracking successful, False otherwise
        """
        try:
            # Get visitor info
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent', '')[:255]
            referrer = request.referrer or ''
            
            # Extract nickname from URL parameters
            nickname = AnalyticsTracker.extract_nickname_from_params()
            
            # Determine source
            if nickname:
                # Check if nickname hints at source
                nickname_lower = nickname.lower()
                source = None
                
                for src, patterns in AnalyticsTracker.SOCIAL_PATTERNS.items():
                    if any(pattern in nickname_lower for pattern in patterns):
                        source = src
                        break
                
                if not source:
                    source = AnalyticsTracker.get_source_from_referrer(referrer, user_agent)
            else:
                source = AnalyticsTracker.get_source_from_referrer(referrer, user_agent)
            
            # Check if visitor exists (by IP)
            visitor = Visitor.query.filter_by(ip_address=ip_address).first()
            
            if visitor:
                # Update existing visitor
                visitor.last_visit = datetime.utcnow()
                visitor.visit_count += 1
                
                # Update nickname if provided and not already set
                if nickname and not visitor.nickname:
                    visitor.nickname = nickname
                
                # Update source if it's more specific than current
                if source != 'direct' and source != 'other':
                    visitor.source = source
            else:
                # Create new visitor
                visitor = Visitor(
                    nickname=nickname,
                    source=source,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    referrer=referrer[:255] if referrer else None
                )
                db.session.add(visitor)
            
            db.session.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error tracking visitor: {e}", exc_info=True)
            db.session.rollback()
            return False
    
    @staticmethod
    def log_activity(activity_type, description=None, user_id=None):
        """
        Log user activity with enhanced context
        
        Args:
            activity_type: Type of activity (login, poem_created, like, etc.)
            description: Optional description
            user_id: Optional user ID (defaults to current user)
        
        Returns:
            bool: True if logging successful, False otherwise
        """
        try:
            # Get user ID
            if user_id is None:
                user_id = current_user.id if current_user.is_authenticated else None
            
            # Get request context
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent', '')[:255]
            referrer = request.referrer or ''
            
            # Create activity record
            activity = UserActivity(
                user_id=user_id,
                activity_type=activity_type,
                description=description[:255] if description else None,
                ip_address=ip_address,
                user_agent=user_agent,
                referrer=referrer[:255] if referrer else None
            )
            
            db.session.add(activity)
            db.session.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error logging activity: {e}", exc_info=True)
            db.session.rollback()
            return False
    
    @staticmethod
    def get_visitor_stats(days=30):
        """
        Get visitor statistics for the last N days
        
        Args:
            days: Number of days to analyze
        
        Returns:
            dict: Statistics dictionary
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Total visitors
            total_visitors = Visitor.query.count()
            
            # Recent visitors
            recent_visitors = Visitor.query.filter(
                Visitor.last_visit >= cutoff_date
            ).count()
            
            # Source breakdown
            sources = db.session.query(
                Visitor.source,
                db.func.count(Visitor.id)
            ).group_by(Visitor.source).all()
            
            source_breakdown = {source: count for source, count in sources}
            
            # Total visits
            total_visits = db.session.query(
                db.func.sum(Visitor.visit_count)
            ).scalar() or 0
            
            return {
                'total_visitors': total_visitors,
                'recent_visitors': recent_visitors,
                'total_visits': total_visits,
                'source_breakdown': source_breakdown,
                'period_days': days
            }
            
        except Exception as e:
            logger.error(f"Error getting visitor stats: {e}", exc_info=True)
            return {}
    
    @staticmethod
    def get_activity_stats(days=30):
        """
        Get user activity statistics for the last N days
        
        Args:
            days: Number of days to analyze
        
        Returns:
            dict: Statistics dictionary
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Total activities
            total_activities = UserActivity.query.filter(
                UserActivity.created_at >= cutoff_date
            ).count()
            
            # Activity type breakdown
            activities = db.session.query(
                UserActivity.activity_type,
                db.func.count(UserActivity.id)
            ).filter(
                UserActivity.created_at >= cutoff_date
            ).group_by(UserActivity.activity_type).all()
            
            activity_breakdown = {activity: count for activity, count in activities}
            
            # Unique active users
            active_users = db.session.query(
                UserActivity.user_id
            ).filter(
                UserActivity.created_at >= cutoff_date,
                UserActivity.user_id.isnot(None)
            ).distinct().count()
            
            return {
                'total_activities': total_activities,
                'active_users': active_users,
                'activity_breakdown': activity_breakdown,
                'period_days': days
            }
            
        except Exception as e:
            logger.error(f"Error getting activity stats: {e}", exc_info=True)
            return {}


def track_visitor():
    """Convenience function for visitor tracking"""
    return AnalyticsTracker.track_visitor()


def log_activity(activity_type, description=None, user_id=None):
    """Convenience function for activity logging"""
    return AnalyticsTracker.log_activity(activity_type, description, user_id)


def track_page_view(page_name):
    """
    Decorator to track page views
    
    Usage:
        @app.route('/home')
        @track_page_view('home')
        def home():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            log_activity('page_view', f'Viewed {page_name}')
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def track_action(action_name):
    """
    Decorator to track user actions
    
    Usage:
        @app.route('/poem/<id>/like', methods=['POST'])
        @track_action('like_poem')
        def like_poem(id):
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            result = f(*args, **kwargs)
            log_activity(action_name, f'Performed {action_name}')
            return result
        return decorated_function
    return decorator


# Export main functions
__all__ = [
    'AnalyticsTracker',
    'track_visitor',
    'log_activity',
    'track_page_view',
    'track_action'
]
