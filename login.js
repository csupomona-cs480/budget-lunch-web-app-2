document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const loginBtn = document.getElementById('loginBtn');
    const signupBtn = document.getElementById('signupBtn');
    const loading = document.getElementById('loading');
    const signupLoading = document.getElementById('signupLoading');
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');
    const loginToggle = document.getElementById('loginToggle');
    const signupToggle = document.getElementById('signupToggle');
    const pageTitle = document.getElementById('pageTitle');
    const pageSubtitle = document.getElementById('pageSubtitle');
    
    // Check if user is already authenticated
    checkAuthStatus();
    
    // Handle form submissions
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        handleLogin();
    });
    
    signupForm.addEventListener('submit', function(e) {
        e.preventDefault();
        handleSignup();
    });
    
    // Handle toggle between login and signup
    loginToggle.addEventListener('click', function() {
        switchToLogin();
    });
    
    signupToggle.addEventListener('click', function() {
        switchToSignup();
    });
    
    // Handle Enter key in password fields
    document.getElementById('password').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleLogin();
        }
    });
    
    document.getElementById('signupPassword').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleSignup();
        }
    });
    
    // Password confirmation validation
    document.getElementById('confirmPassword').addEventListener('input', function() {
        const password = document.getElementById('signupPassword').value;
        const confirmPassword = this.value;
        
        if (confirmPassword && password !== confirmPassword) {
            this.setCustomValidity('Passwords do not match');
        } else {
            this.setCustomValidity('');
        }
    });
});

function checkAuthStatus() {
    fetch('/check-auth')
        .then(response => response.json())
        .then(data => {
            if (data.authenticated) {
                // User is already logged in, redirect to admin
                window.location.href = '/admin.html';
            }
        })
        .catch(error => {
            console.log('Auth check failed:', error);
        });
}

function switchToLogin() {
    document.getElementById('loginToggle').classList.add('active');
    document.getElementById('signupToggle').classList.remove('active');
    document.getElementById('loginForm').classList.add('active');
    document.getElementById('signupForm').classList.remove('active');
    document.getElementById('pageTitle').textContent = '🔐 Admin Login';
    document.getElementById('pageSubtitle').textContent = 'Budget Lunch Management Portal';
    hideMessages();
}

function switchToSignup() {
    document.getElementById('signupToggle').classList.add('active');
    document.getElementById('loginToggle').classList.remove('active');
    document.getElementById('signupForm').classList.add('active');
    document.getElementById('loginForm').classList.remove('active');
    document.getElementById('pageTitle').textContent = '📝 Create Account';
    document.getElementById('pageSubtitle').textContent = 'Join Budget Lunch Admin Portal';
    hideMessages();
}

function handleLogin() {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const loginBtn = document.getElementById('loginBtn');
    const loading = document.getElementById('loading');
    
    // Clear previous messages
    hideMessages();
    
    // Validation
    if (!email) {
        showError('Please enter your email address.');
        document.getElementById('email').focus();
        return;
    }
    
    if (!password) {
        showError('Please enter your password.');
        document.getElementById('password').focus();
        return;
    }
    
    // Show loading state
    loginBtn.disabled = true;
    loading.style.display = 'block';
    
    // Make login request
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess('Login successful! Redirecting...');
            // Redirect to admin page after a short delay
            setTimeout(() => {
                window.location.href = '/admin.html';
            }, 1000);
        } else {
            showError(data.message || 'Login failed. Please check your credentials.');
        }
    })
    .catch(error => {
        console.error('Login error:', error);
        showError('An error occurred during login. Please try again.');
    })
    .finally(() => {
        // Hide loading state
        loginBtn.disabled = false;
        loading.style.display = 'none';
    });
}

function handleSignup() {
    const email = document.getElementById('signupEmail').value.trim();
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const signupBtn = document.getElementById('signupBtn');
    const signupLoading = document.getElementById('signupLoading');
    
    // Clear previous messages
    hideMessages();
    
    // Validation
    if (!email) {
        showError('Please enter your email address.');
        document.getElementById('signupEmail').focus();
        return;
    }
    
    if (!password) {
        showError('Please enter a password.');
        document.getElementById('signupPassword').focus();
        return;
    }
    
    if (password.length < 6) {
        showError('Password must be at least 6 characters long.');
        document.getElementById('signupPassword').focus();
        return;
    }
    
    if (password !== confirmPassword) {
        showError('Passwords do not match.');
        document.getElementById('confirmPassword').focus();
        return;
    }
    
    // Show loading state
    signupBtn.disabled = true;
    signupLoading.style.display = 'block';
    
    // Make signup request
    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess(data.message);
            // Clear form
            document.getElementById('signupEmail').value = '';
            document.getElementById('signupPassword').value = '';
            document.getElementById('confirmPassword').value = '';
            // Switch to login form after a delay
            setTimeout(() => {
                switchToLogin();
            }, 2000);
        } else {
            showError(data.message || 'Failed to create account. Please try again.');
        }
    })
    .catch(error => {
        console.error('Signup error:', error);
        showError('An error occurred during signup. Please try again.');
    })
    .finally(() => {
        // Hide loading state
        signupBtn.disabled = false;
        signupLoading.style.display = 'none';
    });
}

function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        errorMessage.style.display = 'none';
    }, 5000);
}

function showSuccess(message) {
    const successMessage = document.getElementById('successMessage');
    successMessage.textContent = message;
    successMessage.style.display = 'block';
}

function hideMessages() {
    document.getElementById('errorMessage').style.display = 'none';
    document.getElementById('successMessage').style.display = 'none';
}
