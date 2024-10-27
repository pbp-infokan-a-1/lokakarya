// store-utils.js
const Toast = {
    show(message, type = 'success') {
        const container = document.querySelector('.toast-container') || createToastContainer();
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        const icon = document.createElement('span');
        icon.className = type === 'success' ? 'text-green-500' : 'text-red-500';
        icon.innerHTML = type === 'success' ? '✓' : '✕';
        
        const text = document.createElement('span');
        text.textContent = message;
        
        toast.appendChild(icon);
        toast.appendChild(text);
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
            if (container.children.length === 0) {
                container.remove();
            }
        }, 3000);
    }
};

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}

function validateForm(formData) {
    const errors = {};
    const requiredFields = ['nama', 'alamat', 'hari_buka', 'email', 'telepon'];
    
    requiredFields.forEach(field => {
        if (!formData.get(field)) {
            errors[field] = `${field.charAt(0).toUpperCase() + field.slice(1)} is required`;
        }
    });
    
    const email = formData.get('email');
    if (email && !email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
        errors.email = 'Invalid email format';
    }
    
    return errors;
}

function showFieldError(field, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    const inputElement = document.querySelector(`[name="${field}"]`);
    const existingError = inputElement.parentElement.querySelector('.error-message');
    
    if (existingError) {
        existingError.remove();
    }
    
    inputElement.parentElement.appendChild(errorDiv);
    inputElement.classList.add('border-red-500');
}

function clearFieldErrors() {
    document.querySelectorAll('.error-message').forEach(el => el.remove());
    document.querySelectorAll('.form-input').forEach(el => {
        el.classList.remove('border-red-500');
    });
}

export { Toast, validateForm, showFieldError, clearFieldErrors };
