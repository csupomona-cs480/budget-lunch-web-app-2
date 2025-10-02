document.addEventListener('DOMContentLoaded', function() {
    // Search button click event
    document.getElementById('search').addEventListener('click', function() {
        performSearch();
    });

    // Enter key support for search input
    document.getElementById('price').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });

    // Add loading state to search button
    const searchButton = document.getElementById('search');
    const searchInput = document.getElementById('price');
    
    // Add input validation styling
    searchInput.addEventListener('input', function() {
        if (this.value && this.value > 0) {
            this.style.borderColor = '#10b981';
        } else {
            this.style.borderColor = '#e5e7eb';
        }
    });
});

function performSearch() {
    const budget = document.getElementById('price').value;
    const searchButton = document.getElementById('search');
    const searchInput = document.getElementById('price');
    
    if (!budget || budget <= 0) {
        showNotification('Please enter a valid budget amount', 'error');
        searchInput.focus();
        return;
    }
    
    // Show loading state
    setLoadingState(true);
    
    fetch(`/search/${budget}`)
        .then(response => response.json())
        .then(data => {
            displayResults(data, budget);
            showNotification(`Found ${data.length} meal${data.length !== 1 ? 's' : ''} within your budget!`, 'success');
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error loading results. Please try again.', 'error');
            document.getElementById('result').innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">
                        <i class="fas fa-exclamation-triangle"></i>
                    </div>
                    <h3>Oops! Something went wrong</h3>
                    <p>We couldn't load the results. Please try again.</p>
                </div>
            `;
        })
        .finally(() => {
            setLoadingState(false);
        });
}

// Remove addItem function as it's not needed in the main page

function displayResults(foods, budget) {
    const resultDiv = document.getElementById('result');
    
    if (foods.length === 0) {
        resultDiv.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">
                    <i class="fas fa-search"></i>
                </div>
                <h3>No meals found within your budget</h3>
                <p>We couldn't find any meals under $${budget}. Try increasing your budget to see more options!</p>
            </div>
        `;
        return;
    }
    
    let html = `
        <div class="results-header">
            <h2>🍽️ Meals within your budget of $${budget}</h2>
            <p class="results-count">${foods.length} delicious option${foods.length !== 1 ? 's' : ''} found</p>
        </div>
        <div class="food-grid">
    `;
    
    foods.forEach(food => {
        const imageHtml = food.imageurl ? 
            `<img src="${food.imageurl}" alt="${food.name}" class="food-image" onerror="this.style.display='none'">` : 
            `<div class="food-image-placeholder"><i class="fas fa-utensils"></i></div>`;
        
        html += `
            <div class="food-item">
                ${imageHtml}
                <div class="food-details">
                    <div class="food-name">${food.name}</div>
                    <div class="food-price">$${parseFloat(food.price).toFixed(2)}</div>
                </div>
            </div>
        `;
    });
    
    html += `</div>`;
    resultDiv.innerHTML = html;
}

function setLoadingState(isLoading) {
    const searchButton = document.getElementById('search');
    const searchInput = document.getElementById('price');
    
    if (isLoading) {
        searchButton.disabled = true;
        searchButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span>Searching...</span>';
        searchInput.disabled = true;
    } else {
        searchButton.disabled = false;
        searchButton.innerHTML = '<i class="fas fa-search"></i> <span>Find Meals</span>';
        searchInput.disabled = false;
    }
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#6366f1'};
        color: white;
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s ease-in-out;
        max-width: 400px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    `;
    
    notification.querySelector('.notification-content').style.cssText = `
        display: flex;
        align-items: center;
        gap: 12px;
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 4 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 4000);
}
