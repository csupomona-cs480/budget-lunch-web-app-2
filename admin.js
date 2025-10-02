document.addEventListener('DOMContentLoaded', function() {
    // Check authentication status first
    checkAuthStatus();
    
    // Event listeners
    document.getElementById('addBtn').addEventListener('click', addItem);
    document.getElementById('refreshBtn').addEventListener('click', loadAllItems);
    
    // Load all items on page load
    loadAllItems();
});

function checkAuthStatus() {
    fetch('/check-auth')
        .then(response => response.json())
        .then(data => {
            if (!data.authenticated) {
                // User is not authenticated, redirect to login
                window.location.href = '/login';
            }
        })
        .catch(error => {
            console.error('Auth check failed:', error);
            // On error, redirect to login for security
            window.location.href = '/login';
        });
}

function logout() {
    if (confirm('Are you sure you want to logout?')) {
        fetch('/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = '/login';
            } else {
                // Force redirect even if logout fails
                window.location.href = '/login';
            }
        })
        .catch(error => {
            console.error('Logout error:', error);
            // Force redirect even if logout fails
            window.location.href = '/login';
        });
    }
}

function showStatusMessage(message, isError = false) {
    const statusDiv = document.getElementById('statusMessage');
    statusDiv.textContent = message;
    statusDiv.className = `status-message ${isError ? 'status-error' : 'status-success'}`;
    statusDiv.style.display = 'block';
    
    // Hide message after 3 seconds
    setTimeout(() => {
        statusDiv.style.display = 'none';
    }, 3000);
}

function addItem() {
    const name = document.getElementById('addName').value.trim();
    const price = document.getElementById('addPrice').value;
    const imageurl = document.getElementById('addImageUrl').value.trim();
    const addBtn = document.getElementById('addBtn');
    
    // Validation
    if (!name) {
        showStatusMessage('Please enter a food name.', true);
        document.getElementById('addName').focus();
        return;
    }
    
    if (!price || price <= 0) {
        showStatusMessage('Please enter a valid price.', true);
        document.getElementById('addPrice').focus();
        return;
    }
    
    // Show loading state
    addBtn.disabled = true;
    addBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';
    
    // Make API call
    fetch(`/add/${encodeURIComponent(name)}/${price}?imageurl=${encodeURIComponent(imageurl)}`)
        .then(response => {
            if (response.ok) {
                showStatusMessage(`"${name}" added successfully!`);
                // Clear form
                document.getElementById('addName').value = '';
                document.getElementById('addPrice').value = '';
                document.getElementById('addImageUrl').value = '';
                // Refresh the list
                loadAllItems();
            } else {
                throw new Error('Failed to add item');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showStatusMessage('Error adding item. Please try again.', true);
        })
        .finally(() => {
            // Reset button state
            addBtn.disabled = false;
            addBtn.innerHTML = '<i class="fas fa-plus"></i> Add Item';
        });
}

function loadAllItems() {
    fetch('/list')
        .then(response => response.json())
        .then(data => {
            displayItems(data);
        })
        .catch(error => {
            console.error('Error:', error);
            showStatusMessage('Error loading items. Please try again.', true);
        });
}

function displayItems(items) {
    const itemsListDiv = document.getElementById('itemsList');
    
    if (items.length === 0) {
        itemsListDiv.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-inbox"></i>
                <h3>No items found</h3>
                <p>Your database is empty. Add some items to get started!</p>
            </div>
        `;
        return;
    }
    
    let html = `
        <div class="items-table-container">
            <table class="items-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Image</th>
                        <th>Name</th>
                        <th>Price</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    items.forEach(item => {
        const imageHtml = item.imageurl ? 
            `<img src="${item.imageurl}" alt="${item.name}" class="item-image" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">` : 
            '';
        
        const imagePlaceholder = !item.imageurl ? 
            `<div class="item-image-placeholder"><i class="fas fa-utensils"></i></div>` : 
            `<div class="item-image-placeholder" style="display: none;"><i class="fas fa-utensils"></i></div>`;
        
        html += `
            <tr id="item-${item.id}">
                <td><span style="font-weight: 600; color: var(--gray-600);">#${item.id}</span></td>
                <td>${imageHtml}${imagePlaceholder}</td>
                <td><span class="item-name">${item.name}</span></td>
                <td><span class="item-price">$${parseFloat(item.price).toFixed(2)}</span></td>
                <td>
                    <div class="item-actions">
                        <button class="btn btn-warning" onclick="editItem(${item.id}, '${item.name.replace(/'/g, "\\'")}', ${item.price}, '${item.imageurl ? item.imageurl.replace(/'/g, "\\'") : ''}')">
                            <i class="fas fa-edit"></i>
                            Edit
                        </button>
                        <button class="btn btn-danger" onclick="deleteItem(${item.id}, '${item.name.replace(/'/g, "\\'")}')">
                            <i class="fas fa-trash"></i>
                            Delete
                        </button>
                    </div>
                </td>
            </tr>
            <tr id="edit-form-${item.id}" class="edit-form">
                <td colspan="5">
                    <div class="edit-form-grid">
                        <div class="form-group">
                            <label>Name</label>
                            <input type="text" id="editName-${item.id}" value="${item.name}">
                        </div>
                        <div class="form-group">
                            <label>Price ($)</label>
                            <input type="number" id="editPrice-${item.id}" value="${item.price}" step="0.01" min="0">
                        </div>
                        <div class="form-group">
                            <label>Image URL</label>
                            <input type="text" id="editImageUrl-${item.id}" value="${item.imageurl || ''}">
                        </div>
                    </div>
                    <div class="edit-form-actions">
                        <button class="btn btn-success" onclick="updateItem(${item.id})">
                            <i class="fas fa-save"></i>
                            Save Changes
                        </button>
                        <button class="btn btn-secondary" onclick="cancelEdit(${item.id})">
                            <i class="fas fa-times"></i>
                            Cancel
                        </button>
                    </div>
                </td>
            </tr>
        `;
    });
    
    html += `
                </tbody>
            </table>
        </div>
    `;
    
    itemsListDiv.innerHTML = html;
}

function editItem(id, name, price, imageurl) {
    // Hide all other edit forms
    document.querySelectorAll('.edit-form').forEach(form => {
        form.classList.remove('active');
    });
    
    // Show this edit form
    const editForm = document.getElementById(`edit-form-${id}`);
    editForm.classList.add('active');
    
    // Populate form fields
    document.getElementById(`editName-${id}`).value = name;
    document.getElementById(`editPrice-${id}`).value = price;
    document.getElementById(`editImageUrl-${id}`).value = imageurl;
}

function cancelEdit(id) {
    const editForm = document.getElementById(`edit-form-${id}`);
    editForm.classList.remove('active');
}

function updateItem(id) {
    const name = document.getElementById(`editName-${id}`).value.trim();
    const price = document.getElementById(`editPrice-${id}`).value;
    const imageurl = document.getElementById(`editImageUrl-${id}`).value.trim();
    
    // Validation
    if (!name) {
        showStatusMessage('Please enter a food name.', true);
        document.getElementById(`editName-${id}`).focus();
        return;
    }
    
    if (!price || price <= 0) {
        showStatusMessage('Please enter a valid price.', true);
        document.getElementById(`editPrice-${id}`).focus();
        return;
    }
    
    // Show loading state on save button
    const saveBtn = document.querySelector(`#edit-form-${id} .btn-success`);
    const originalText = saveBtn.innerHTML;
    saveBtn.disabled = true;
    saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
    
    // Make API call
    fetch(`/update/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: name,
            price: parseFloat(price),
            imageurl: imageurl
        })
    })
    .then(response => {
        if (response.ok) {
            showStatusMessage(`"${name}" updated successfully!`);
            // Hide edit form
            cancelEdit(id);
            // Refresh the list
            loadAllItems();
        } else {
            throw new Error('Failed to update item');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showStatusMessage('Error updating item. Please try again.', true);
    })
    .finally(() => {
        // Reset button state
        saveBtn.disabled = false;
        saveBtn.innerHTML = originalText;
    });
}

function deleteItem(id, name) {
    if (confirm(`Are you sure you want to delete "${name}"? This action cannot be undone.`)) {
        // Find the delete button and show loading state
        const deleteBtn = document.querySelector(`button[onclick="deleteItem(${id}, '${name.replace(/'/g, "\\'")}')"]`);
        const originalText = deleteBtn.innerHTML;
        deleteBtn.disabled = true;
        deleteBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Deleting...';
        
        fetch(`/delete/${id}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                showStatusMessage(`"${name}" deleted successfully!`);
                // Refresh the list
                loadAllItems();
            } else {
                throw new Error('Failed to delete item');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showStatusMessage('Error deleting item. Please try again.', true);
        })
        .finally(() => {
            // Reset button state
            deleteBtn.disabled = false;
            deleteBtn.innerHTML = originalText;
        });
    }
}
