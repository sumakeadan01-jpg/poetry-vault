// Tutorial/Onboarding Feature
// Shows tooltips for new users to explain key features

const tutorialSteps = [
    {
        element: 'a[href="/search"]',
        title: '🔍 Search',
        message: 'Search for your favorite poets and poems here. Give it a shot!',
        position: 'bottom'
    },
    {
        element: 'a[href="/new-poem"]',
        title: '✍️ New Poem',
        message: 'Share your own poetry with the world. Express yourself!',
        position: 'bottom'
    },
    {
        element: 'a[href="/saved-poems"]',
        title: '📚 Your Vault',
        message: 'Save your favorite poems here to read anytime.',
        position: 'bottom'
    }
];

let currentStep = 0;
let tooltipElement = null;
let overlayElement = null;

function createTooltip(step) {
    // Create overlay
    overlayElement = document.createElement('div');
    overlayElement.className = 'tutorial-overlay';
    document.body.appendChild(overlayElement);

    // Create tooltip
    tooltipElement = document.createElement('div');
    tooltipElement.className = 'tutorial-tooltip';
    tooltipElement.innerHTML = `
        <div class="tutorial-header">
            <h3>${step.title}</h3>
            <button class="tutorial-skip" onclick="skipTutorial()">Skip</button>
        </div>
        <p>${step.message}</p>
        <div class="tutorial-footer">
            <span class="tutorial-progress">${currentStep + 1} of ${tutorialSteps.length}</span>
            <button class="tutorial-next" onclick="nextStep()">${currentStep === tutorialSteps.length - 1 ? 'Got it!' : 'Next'}</button>
        </div>
    `;
    document.body.appendChild(tooltipElement);

    // Position tooltip
    const targetElement = document.querySelector(step.element);
    if (targetElement) {
        // Highlight target element
        targetElement.classList.add('tutorial-highlight');
        targetElement.style.position = 'relative';
        targetElement.style.zIndex = '1001';

        const rect = targetElement.getBoundingClientRect();
        const tooltipRect = tooltipElement.getBoundingClientRect();

        if (step.position === 'bottom') {
            let top = rect.bottom + 10;
            let left = rect.left + (rect.width / 2) - (tooltipRect.width / 2);
            
            // Keep tooltip on screen
            if (left < 10) left = 10;
            if (left + tooltipRect.width > window.innerWidth - 10) {
                left = window.innerWidth - tooltipRect.width - 10;
            }
            
            tooltipElement.style.top = `${top}px`;
            tooltipElement.style.left = `${left}px`;
        }

        // Add arrow
        tooltipElement.classList.add('tooltip-' + step.position);
    } else {
        // Element not found, skip to next step
        console.warn('Tutorial element not found:', step.element);
        nextStep();
    }
}

function removeTooltip() {
    if (tooltipElement) {
        tooltipElement.remove();
        tooltipElement = null;
    }
    if (overlayElement) {
        overlayElement.remove();
        overlayElement = null;
    }
    // Remove highlights
    document.querySelectorAll('.tutorial-highlight').forEach(el => {
        el.classList.remove('tutorial-highlight');
        el.style.zIndex = '';
    });
}

function nextStep() {
    removeTooltip();
    currentStep++;
    
    if (currentStep < tutorialSteps.length) {
        setTimeout(() => createTooltip(tutorialSteps[currentStep]), 300);
    } else {
        completeTutorial();
    }
}

function skipTutorial() {
    removeTooltip();
    completeTutorial();
}

function completeTutorial() {
    // Mark tutorial as seen in backend
    fetch('/mark-tutorial-seen', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            console.log('Tutorial completed');
        } else {
            console.error('Failed to mark tutorial as seen');
        }
    })
    .catch(error => {
        console.error('Error marking tutorial as seen:', error);
    });
}

function startTutorial() {
    // Wait a bit for page to load
    setTimeout(() => {
        createTooltip(tutorialSteps[0]);
    }, 500);
}

// Auto-start if showTutorial is true (set by backend)
if (typeof showTutorial !== 'undefined' && showTutorial) {
    startTutorial();
}
