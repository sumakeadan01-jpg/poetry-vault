"""
Analytics tracking for Poetry Vault
Tracks user activity and visitor information
"""

from flask import request
from models import db, UserActivity, Visitor
from flask_login import current_user
from datetime import datetime


def get_source_from_referrer(referrer, user_agent=''):
    """Determine source from referrer URL and user agent"""
    if not referrer:
        # Check user agent for Instagram app
        if user_agent and 'instagram' in user_agent.lower():
            return 'instagram'
        return 'direct'

    referrer_lower = referrer.lower()

    if 'instagram.com' in referrer_lower or 'ig.me' in referrer_lower:
        return 'instagram'
    elif 'facebook.com' in referrer_lower or 'fb.com' in referrer_lower:
        return 'facebook'
    elif 'twitter.com' in referrer_lower or 't.co' in referrer_lower:
        return 'twitter'
    elif 'google.com' in referrer_lower:
        return 'google'
    elif 'bing.com' in referrer_lower:
        return 'bing'
    else:
        return 'other'


def track_visitor():
    """Track visitor information"""
    try:
        # Get visitor info
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')[:255]
        referrer = request.referrer or ''

        # Get nickname from URL parameter (supports multiple formats for discretion)
        nickname = request.args.get('from') or request.args.get('ref') or request.args.get('u') or request.args.get('wist') or request.args.get('id')

        # Determine source (use nickname if provided, otherwise detect from referrer/user agent)
        if nickname:
            # If nickname contains social media name, use that as source
            nickname_lower = nickname.lower()
            if 'instagram' in nickname_lower or 'ig' in nickname_lower:
                source = 'instagram'
            elif 'facebook' in nickname_lower or 'fb' in nickname_lower:
                source = 'facebook'
            elif 'twitter' in nickname_lower:
                source = 'twitter'
            else:
                source = get_source_from_referrer(referrer, user_agent)
        else:
            source = get_source_from_referrer(referrer, user_agent)

        # Check if visitor exists (by IP)
        visitor = Visitor.query.filter_by(ip_address=ip_address).first()

        if visitor:
            # Update existing visitor
            visitor.last_visit = datetime.utcnow()
            visitor.visit_count += 1
            if nickname and not visitor.nickname:
                visitor.nickname = nickname
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
    except Exception as e:
        print(f"Error tracking visitor: {e}")
        db.session.rollback()


def log_activity(activity_type, description=None):
    """Log user activity"""
    try:
        user_id = current_user.id if current_user.is_authenticated else None
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')[:255]
        referrer = request.referrer or ''

        activity = UserActivity(
            user_id=user_id,
            activity_type=activity_type,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
            referrer=referrer[:255] if referrer else None
        )

        db.session.add(activity)
        db.session.commit()
    except Exception as e:
        print(f"Error logging activity: {e}")
        db.session.rollback()
