// Desktop Push Notifications for Poetry Vault
// Asks permission and sends notifications for likes, follows, comments

let notificationPermission = false;

// Request notification permission
async function requestNotificationPermission() {
    if (!('Notification' in window)) {
        console.log('This browser does not support notifications');
        return false;
    }
    
    if (Notification.permission === 'granted') {
        notificationPermission = true;
        return true;
    }
    
    if (Notification.permission !== 'denied') {
        const permission = await Notification.requestPermission();
        notificationPermission = (permission === 'granted');
        return notificationPermission;
    }
    
    return false;
}

// Show desktop notification
function showDesktopNotification(title, body, icon = '/static/images/feather.png') {
    if (!notificationPermission) return;
    
    const notification = new Notification(title, {
        body: body,
        icon: icon,
        badge: icon,
        tag: 'poetry-vault',
        requireInteraction: false
    });
    
    // Auto-close after 5 seconds
    setTimeout(() => notification.close(), 5000);
    
    // Click to open app
    notification.onclick = function() {
        window.focus();
        notification.close();
    };
}

// Check for new notifications periodically
let lastNotificationId = 0;

async function checkForNewNotifications() {
    try {
        const response = await fetch('/api/check-new-notifications');
        const data = await response.json();
        
        if (data.notifications && data.notifications.length > 0) {
            data.notifications.forEach(notif => {
                if (notif.id > lastNotificationId) {
                    // Show desktop notification
                    let title = '📚 Poetry Vault';
                    let body = notif.message;
                    
                    if (notif.type === 'like') {
                        title = '❤️ New Like!';
                    } else if (notif.type === 'follow') {
                        title = '👤 New Follower!';
                    } else if (notif.type === 'comment') {
                        title = '💬 New Comment!';
                    }
                    
                    showDesktopNotification(title, body);
                    lastNotificationId = notif.id;
                }
            });
        }
    } catch (error) {
        console.error('Error checking notifications:', error);
    }
}

// Initialize notifications
async function initNotifications() {
    // Ask for permission on first visit
    const hasAsked = localStorage.getItem('notificationAsked');
    
    if (!hasAsked) {
        // Show a friendly prompt first
        setTimeout(async () => {
            if (confirm('📬 Would you like to receive desktop notifications when someone likes your poems, follows you, or comments?')) {
                const granted = await requestNotificationPermission();
                if (granted) {
                    console.log('✅ Notifications enabled!');
                    // Start checking for notifications
                    setInterval(checkForNewNotifications, 30000); // Check every 30 seconds
                }
            }
            localStorage.setItem('notificationAsked', 'true');
        }, 3000); // Ask after 3 seconds
    } else if (Notification.permission === 'granted') {
        notificationPermission = true;
        // Start checking for notifications
        setInterval(checkForNewNotifications, 30000); // Check every 30 seconds
    }
}

// Auto-initialize when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initNotifications);
} else {
    initNotifications();
}
