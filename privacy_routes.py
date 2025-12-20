"""
Privacy and security routes for Poetry Vault
Provides user privacy controls and data management
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, User, Poem, Comment
from security_middleware import security_manager, require_permission, protect_user_data
from data_protection import data_protection, get_user_data_summary
import json

privacy_bp = Blueprint('privacy', __name__)

@privacy_bp.route('/privacy-dashboard')
@login_required
@protect_user_data()
def privacy_dashboard():
    """User privacy and data management dashboard"""
    try:
        # Get user's data summary
        data_summary = get_user_data_summary(current_user.id)
        
        # Get current privacy settings
        privacy_settings = current_user.get_privacy_settings()
        
        return render_template('privacy_dashboard.html', 
                             data_summary=data_summary,
                             privacy_settings=privacy_settings)
    except Exception as e:
        flash('Error loading privacy dashboard', 'error')
        return redirect(url_for('home'))

@privacy_bp.route('/update-privacy-settings', methods=['POST'])
@login_required
@protect_user_data()
def update_privacy_settings():
    """Update user privacy settings"""
    try:
        settings = {
            'profile_visibility': request.form.get('profile_visibility', 'public'),
            'poem_visibility': request.form.get('poem_visibility', 'public'),
            'activity_visibility': request.form.get('activity_visibility', 'friends'),
            'allow_comments': request.form.get('allow_comments') == 'on',
            'allow_follows': request.form.get('allow_follows') == 'on',
            'email_notifications': request.form.get('email_notifications') == 'on',
            'data_sharing_consent': request.form.get('data_sharing_consent') == 'on'
        }
        
        success = current_user.update_privacy_settings(settings)
        
        if success:
            # Update data sharing consent in user model
            current_user.data_sharing_consent = settings['data_sharing_consent']
            db.session.commit()
            
            security_manager.log_security_event('privacy_settings_updated', current_user.id)
            flash('Privacy settings updated successfully', 'success')
        else:
            flash('Error updating privacy settings', 'error')
            
    except Exception as e:
        flash('Error updating privacy settings', 'error')
        db.session.rollback()
    
    return redirect(url_for('privacy.privacy_dashboard'))

@privacy_bp.route('/download-data')
@login_required
@require_permission('download_data')
def download_data():
    """Allow user to download their data"""
    try:
        backup_file = data_protection.backup_user_data(current_user.id)
        
        if backup_file:
            security_manager.log_security_event('data_download', current_user.id)
            flash('Your data backup has been created. Check your downloads.', 'success')
        else:
            flash('Error creating data backup', 'error')
            
    except Exception as e:
        flash('Error downloading data', 'error')
    
    return redirect(url_for('privacy.privacy_dashboard'))

@privacy_bp.route('/delete-account', methods=['GET', 'POST'])
@login_required
@protect_user_data()
def delete_account():
    """Allow user to delete their account"""
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_delete = request.form.get('confirm_delete') == 'on'
        keep_backup = request.form.get('keep_backup') == 'on'
        
        if not password:
            flash('Password is required to delete account', 'error')
            return render_template('delete_account.html')
        
        if not current_user.check_password(password):
            flash('Incorrect password', 'error')
            return render_template('delete_account.html')
        
        if not confirm_delete:
            flash('You must confirm account deletion', 'error')
            return render_template('delete_account.html')
        
        try:
            # Delete user data
            success, message = data_protection.delete_user_data(current_user.id, keep_backup)
            
            if success:
                security_manager.log_security_event('account_deleted', current_user.id)
                flash('Your account has been deleted successfully', 'success')
                return redirect(url_for('index'))
            else:
                flash(f'Error deleting account: {message}', 'error')
                
        except Exception as e:
            flash('Error deleting account', 'error')
            db.session.rollback()
    
    return render_template('delete_account.html')

@privacy_bp.route('/protect-content/<content_type>/<int:content_id>')
@login_required
@protect_user_data()
def protect_content(content_type, content_id):
    """Toggle protection status of user content"""
    try:
        if content_type == 'poem':
            poem = Poem.query.get_or_404(content_id)
            if poem.user_id != current_user.id:
                flash('You can only protect your own content', 'error')
                return redirect(url_for('home'))
            
            poem.is_protected = not poem.is_protected
            db.session.commit()
            
            status = 'protected' if poem.is_protected else 'unprotected'
            flash(f'Poem "{poem.title}" is now {status}', 'success')
            security_manager.log_security_event('content_protection_toggled', current_user.id, 
                                              {'content_type': 'poem', 'content_id': content_id, 'protected': poem.is_protected})
            
        elif content_type == 'comment':
            comment = Comment.query.get_or_404(content_id)
            if comment.user_id != current_user.id:
                flash('You can only protect your own content', 'error')
                return redirect(url_for('home'))
            
            comment.is_protected = not comment.is_protected
            db.session.commit()
            
            status = 'protected' if comment.is_protected else 'unprotected'
            flash(f'Comment is now {status}', 'success')
            security_manager.log_security_event('content_protection_toggled', current_user.id,
                                              {'content_type': 'comment', 'content_id': content_id, 'protected': comment.is_protected})
        
    except Exception as e:
        flash('Error updating content protection', 'error')
        db.session.rollback()
    
    return redirect(request.referrer or url_for('home'))

@privacy_bp.route('/report-content', methods=['POST'])
@login_required
@protect_user_data()
def report_content():
    """Report inappropriate content"""
    try:
        content_type = request.form.get('content_type')
        content_id = request.form.get('content_id')
        reason = request.form.get('reason', '').strip()
        
        if not content_type or not content_id or not reason:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Sanitize reason
        reason = security_manager.sanitize_input(reason)
        
        if content_type == 'poem':
            poem = Poem.query.get(content_id)
            if poem:
                poem.is_flagged = True
                poem.flag_reason = f"Reported by {current_user.username}: {reason}"
                db.session.commit()
                
        elif content_type == 'comment':
            comment = Comment.query.get(content_id)
            if comment:
                comment.is_flagged = True
                comment.flag_reason = f"Reported by {current_user.username}: {reason}"
                db.session.commit()
        
        security_manager.log_security_event('content_reported', current_user.id,
                                          {'content_type': content_type, 'content_id': content_id, 'reason': reason})
        
        return jsonify({'success': True, 'message': 'Content reported successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error reporting content'}), 500

@privacy_bp.route('/security-log')
@login_required
@protect_user_data()
def security_log():
    """Show user's security activity log"""
    try:
        # In a real implementation, you'd fetch this from a security log table
        # For now, we'll show basic account info
        account_info = {
            'last_login': current_user.last_login,
            'account_created': current_user.created_at,
            'failed_attempts': current_user.failed_login_attempts,
            'is_locked': current_user.account_locked_until is not None,
            'email_verified': current_user.email_verified,
            'two_factor_enabled': current_user.two_factor_enabled
        }
        
        return render_template('security_log.html', account_info=account_info)
        
    except Exception as e:
        flash('Error loading security log', 'error')
        return redirect(url_for('privacy.privacy_dashboard'))