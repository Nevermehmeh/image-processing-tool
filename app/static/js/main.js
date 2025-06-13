// Main JavaScript file for common functionality

document.addEventListener('DOMContentLoaded', function() {
    // Enable Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Enable Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-dismiss alerts after 5 seconds
    var alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Initialize any other common functionality here
});

// Helper function to show loading state
function showLoading(message = 'Processing...') {
    const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    document.getElementById('loading-message').textContent = message;
    loadingModal.show();
    return loadingModal;
}

// Helper function to hide loading
function hideLoading(modal) {
    if (modal) {
        modal.hide();
    } else {
        const loadingModal = bootstrap.Modal.getInstance(document.getElementById('loadingModal'));
        if (loadingModal) {
            loadingModal.hide();
        }
    }
}

// Helper function to handle API errors
function handleApiError(error) {
    console.error('API Error:', error);
    let errorMessage = 'An error occurred. Please try again.';
    
    if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        const responseData = error.response.data;
        errorMessage = responseData.error || errorMessage;
        console.error('Error data:', responseData);
        console.error('Status:', error.response.status);
        console.error('Headers:', error.response.headers);
    } else if (error.request) {
        // The request was made but no response was received
        console.error('No response received:', error.request);
        errorMessage = 'No response from server. Please check your connection.';
    } else {
        // Something happened in setting up the request that triggered an Error
        console.error('Error:', error.message);
        errorMessage = error.message || errorMessage;
    }
    
    // Show error message to user
    showAlert('danger', errorMessage);
}

// Helper function to show alert messages
function showAlert(type, message, container = null, dismissible = true) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        ${dismissible ? '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' : ''}
    `;
    
    const targetContainer = container || document.querySelector('main');
    if (targetContainer) {
        targetContainer.insertBefore(alertDiv, targetContainer.firstChild);
        
        // Auto-dismiss after 5 seconds
        if (dismissible) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alertDiv);
                bsAlert.close();
            }, 5000);
        }
    }
    
    return alertDiv;
}

// Helper function to format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Helper function to validate image file
function validateImageFile(file, maxSizeMB = 10) {
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg'];
    const maxSize = maxSizeMB * 1024 * 1024; // Convert MB to bytes
    
    if (!allowedTypes.includes(file.type)) {
        return { valid: false, message: 'Invalid file type. Please upload a PNG or JPG image.' };
    }
    
    if (file.size > maxSize) {
        return { valid: false, message: `File is too large. Maximum size is ${maxSizeMB}MB.` };
    }
    
    return { valid: true };
}

// Helper function to read file as data URL
function readFileAsDataURL(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = (e) => reject(e);
        reader.readAsDataURL(file);
    });
}

// Helper function to create a debounced version of a function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
