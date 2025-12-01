// Hidden Instagram Tracker
// Automatically detects Instagram visitors and tracks them

(function() {
    // Check if this is the first page load
    if (window.location.pathname === '/' || window.location.pathname === '/login' || window.location.pathname === '/register') {
        
        // Check if we haven't already tracked this session
        if (!sessionStorage.getItem('tracked')) {
            
            // Detect Instagram in multiple ways
            const userAgent = navigator.userAgent || '';
            const isInstagramApp = userAgent.includes('Instagram');
            const isInstagramBrowser = userAgent.includes('FBAN') || userAgent.includes('FBAV');
            
            // Check if coming from Instagram (some browsers preserve this)
            const referrer = document.referrer || '';
            const fromInstagram = referrer.includes('instagram.com') || referrer.includes('ig.me');
            
            // Get nickname from URL parameters (e.g., ?from=john or ?ref=sarah)
            const urlParams = new URLSearchParams(window.location.search);
            const nickname = urlParams.get('from') || urlParams.get('ref') || urlParams.get('u');
            
            // If detected as Instagram, send tracking request
            if (isInstagramApp || isInstagramBrowser || fromInstagram || nickname) {
                // Send tracking request to backend
                fetch('/api/track-instagram-visitor', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        userAgent: userAgent,
                        referrer: referrer,
                        source: 'instagram',
                        nickname: nickname
                    })
                }).catch(err => console.log('Tracking error:', err));
                
                // Mark as tracked for this session
                sessionStorage.setItem('tracked', nickname || 'instagram');
            } else {
                // Mark as tracked (non-Instagram)
                sessionStorage.setItem('tracked', 'direct');
            }
        }
    }
})();
