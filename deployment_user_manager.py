#!/usr/bin/env python3
"""
Deployment User Management System
Automatically preserves real user accounts across deployments
"""

import os
import json
from datetime import datetime

def create_deployment_route():
    """Add a route to app.py for managing users during deployment"""
    
    route_code = '''
    @app.route('/admin/preserve-users', methods=['GET', 'POST'])
    @login_required
    def preserve_users():
        """Admin route to preserve real users across deployments"""
        if not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        if request.method == 'POST':
            action = request.json.get('action')
            
            if action == 'export':
                # Export real users (non-poet accounts)
                poet_emails = {
                    'shakespeare@poetryvault.com', 'rumi@poetryvault.com',
                    'emilydickinson@poetryvault.com', 'edgarallanpoe@poetryvault.com',
                    'waltwhitman@poetryvault.com', 'lordbyron@poetryvault.com',
                    'williamwordsworth@poetryvault.com', 'johnkeats@poetryvault.com',
                    'percyshelley@poetryvault.com', 'robertburns@poetryvault.com',
                    'robertfrost@poetryvault.com', 'mayaangelou@poetryvault.com',
                    'langstonhughes@poetryvault.com', 'المتنبي@poetryvault.com',
                    'قيسبنالملوح@poetryvault.com'
                }
                
                real_users = User.query.filter(~User.email.in_(poet_emails)).all()
                
                user_data = []
                for user in real_users:
                    user_data.append({
                        'username': user.username,
                        'email': user.email,
                        'password_hash': user.password_hash,
                        'is_admin': user.is_admin,
                        'subscription_tier': user.subscription_tier or 'free',
                        'subscription_expires': user.subscription_expires.isoformat() if user.subscription_expires else None,
                        'created_at': user.created_at.isoformat() if user.created_at else datetime.now().isoformat()
                    })
                
                return jsonify({
                    'success': True,
                    'users': user_data,
                    'count': len(user_data),
                    'export_date': datetime.now().isoformat()
                })
            
            elif action == 'import':
                # Import users from provided data
                users_data = request.json.get('users', [])
                imported = 0
                
                for user_data in users_data:
                    existing = User.query.filter_by(email=user_data['email']).first()
                    if not existing:
                        user = User(
                            username=user_data['username'],
                            email=user_data['email'],
                            password_hash=user_data['password_hash'],
                            is_admin=user_data['is_admin'],
                            subscription_tier=user_data.get('subscription_tier', 'free'),
                            subscription_expires=datetime.fromisoformat(user_data['subscription_expires']) if user_data.get('subscription_expires') else None
                        )
                        db.session.add(user)
                        imported += 1
                
                db.session.commit()
                return jsonify({'success': True, 'imported': imported})
        
        # GET request - show preservation interface
        return render_template('admin/preserve_users.html')
'''
    
    return route_code

def create_preservation_template():
    """Create admin template for user preservation"""
    
    template_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Preservation - Poetry Vault Admin</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .section { background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 8px; }
        button { background: #007cba; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #005a87; }
        .success { color: green; }
        .error { color: red; }
        textarea { width: 100%; height: 200px; font-family: monospace; }
    </style>
</head>
<body>
    <h1>🔒 User Preservation System</h1>
    
    <div class="section">
        <h2>📤 Export Real Users</h2>
        <p>Export all real user accounts (excluding poet accounts) for backup before deployment.</p>
        <button onclick="exportUsers()">Export Users</button>
        <div id="exportResult"></div>
    </div>
    
    <div class="section">
        <h2>📥 Import Users</h2>
        <p>Import previously exported user data after deployment.</p>
        <textarea id="importData" placeholder="Paste exported user JSON data here..."></textarea>
        <br><br>
        <button onclick="importUsers()">Import Users</button>
        <div id="importResult"></div>
    </div>
    
    <div class="section">
        <h2>📋 Instructions</h2>
        <ol>
            <li><strong>Before deployment:</strong> Click "Export Users" and save the JSON data</li>
            <li><strong>Deploy your app</strong> to Render (fresh database will be created)</li>
            <li><strong>After deployment:</strong> Paste the JSON data and click "Import Users"</li>
            <li><strong>Done!</strong> Your real users are preserved across deployments</li>
        </ol>
    </div>

    <script>
        async function exportUsers() {
            try {
                const response = await fetch('/admin/preserve-users', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: 'export' })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('exportResult').innerHTML = 
                        `<div class="success">✅ Exported ${data.count} users</div>
                         <textarea readonly>${JSON.stringify(data, null, 2)}</textarea>`;
                } else {
                    document.getElementById('exportResult').innerHTML = 
                        `<div class="error">❌ Export failed</div>`;
                }
            } catch (error) {
                document.getElementById('exportResult').innerHTML = 
                    `<div class="error">❌ Error: ${error.message}</div>`;
            }
        }
        
        async function importUsers() {
            try {
                const importData = document.getElementById('importData').value;
                if (!importData.trim()) {
                    alert('Please paste the exported JSON data first');
                    return;
                }
                
                const userData = JSON.parse(importData);
                
                const response = await fetch('/admin/preserve-users', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        action: 'import', 
                        users: userData.users || userData 
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('importResult').innerHTML = 
                        `<div class="success">✅ Imported ${data.imported} users successfully!</div>`;
                } else {
                    document.getElementById('importResult').innerHTML = 
                        `<div class="error">❌ Import failed</div>`;
                }
            } catch (error) {
                document.getElementById('importResult').innerHTML = 
                    `<div class="error">❌ Error: ${error.message}</div>`;
            }
        }
    </script>
</body>
</html>'''
    
    # Create admin templates directory if it doesn't exist
    os.makedirs('templates/admin', exist_ok=True)
    
    with open('templates/admin/preserve_users.html', 'w') as f:
        f.write(template_content)
    
    print("✅ Created user preservation template")

if __name__ == '__main__':
    create_preservation_template()
    print("✅ User preservation system ready!")
    print("\n📋 Next steps:")
    print("1. Add the route code to app.py manually")
    print("2. Access /admin/preserve-users after deployment")
    print("3. Export users before future deployments")
    print("4. Import users after deployments")