// Feedback Form JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const submitButton = document.querySelector('button[type="submit"]');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const messageInput = document.getElementById('message');

    // Form validation
    function validateForm() {
        let isValid = true;
        
        // Clear previous error styles
        clearErrors();
        
        // Validate name
        if (nameInput.value.trim().length < 2) {
            showError(nameInput, 'Name must be at least 2 characters long');
            isValid = false;
        }
        
        // Validate email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailInput.value.trim())) {
            showError(emailInput, 'Please enter a valid email address');
            isValid = false;
        }
        
        // Validate message
        if (messageInput.value.trim().length < 10) {
            showError(messageInput, 'Message must be at least 10 characters long');
            isValid = false;
        }
        
        return isValid;
    }
    
    // Show error message
    function showError(input, message) {
        input.style.borderColor = '#f56565';
        input.style.boxShadow = '0 0 10px rgba(245, 101, 101, 0.3)';
        
        // Create error message element
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-text';
        errorDiv.textContent = message;
        errorDiv.style.color = '#fc8181';
        errorDiv.style.fontSize = '0.9rem';
        errorDiv.style.marginTop = '5px';
        
        input.parentNode.appendChild(errorDiv);
    }
    
    // Clear all errors
    function clearErrors() {
        const errorTexts = document.querySelectorAll('.error-text');
        errorTexts.forEach(error => error.remove());
        
        [nameInput, emailInput, messageInput].forEach(input => {
            input.style.borderColor = 'rgba(212, 175, 55, 0.3)';
            input.style.boxShadow = 'none';
        });
    }
    
    // Real-time validation
    nameInput.addEventListener('blur', function() {
        if (this.value.trim().length > 0 && this.value.trim().length < 2) {
            clearErrors();
            showError(this, 'Name must be at least 2 characters long');
        }
    });
    
    emailInput.addEventListener('blur', function() {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (this.value.trim().length > 0 && !emailRegex.test(this.value.trim())) {
            clearErrors();
            showError(this, 'Please enter a valid email address');
        }
    });
    
    messageInput.addEventListener('blur', function() {
        if (this.value.trim().length > 0 && this.value.trim().length < 10) {
            clearErrors();
            showError(this, 'Message must be at least 10 characters long');
        }
    });
    
    // Clear errors on focus
    [nameInput, emailInput, messageInput].forEach(input => {
        input.addEventListener('focus', function() {
            this.style.borderColor = '#d4af37';
            this.style.boxShadow = '0 0 10px rgba(212, 175, 55, 0.3)';
        });
    });
    
    // Form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (!validateForm()) {
            return;
        }
        
        // Show loading state
        submitButton.textContent = 'Submitting...';
        submitButton.disabled = true;
        form.classList.add('loading');
        
        // Create form data
        const formData = new FormData(form);
        
        // Submit form (you'll need to implement the backend route)
        fetch(form.action, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showSuccessMessage('Thank you for your feedback! We appreciate your input.');
                form.reset();
            } else {
                showErrorMessage(data.message || 'Something went wrong. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showErrorMessage('Network error. Please check your connection and try again.');
        })
        .finally(() => {
            // Reset button state
            submitButton.textContent = 'Submit Feedback';
            submitButton.disabled = false;
            form.classList.remove('loading');
        });
    });
    
    // Show success message
    function showSuccessMessage(message) {
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.textContent = message;
        
        form.parentNode.insertBefore(successDiv, form);
        
        // Remove after 5 seconds
        setTimeout(() => {
            successDiv.remove();
        }, 5000);
    }
    
    // Show error message
    function showErrorMessage(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        
        form.parentNode.insertBefore(errorDiv, form);
        
        // Remove after 5 seconds
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }
    
    // Character counter for message
    const charCounter = document.createElement('div');
    charCounter.style.textAlign = 'right';
    charCounter.style.fontSize = '0.9rem';
    charCounter.style.color = '#a0aec0';
    charCounter.style.marginTop = '5px';
    messageInput.parentNode.appendChild(charCounter);
    
    function updateCharCounter() {
        const length = messageInput.value.length;
        const maxLength = 1000; // Set a reasonable max length
        charCounter.textContent = `${length}/${maxLength} characters`;
        
        if (length > maxLength * 0.9) {
            charCounter.style.color = '#f56565';
        } else if (length > maxLength * 0.7) {
            charCounter.style.color = '#f6ad55';
        } else {
            charCounter.style.color = '#a0aec0';
        }
    }
    
    messageInput.addEventListener('input', updateCharCounter);
    updateCharCounter(); // Initial call
    
    // Add smooth animations
    const inputs = [nameInput, emailInput, messageInput];
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        input.addEventListener('blur', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});