// store-ajax.js
import { Toast, validateForm, showFieldError, clearFieldErrors } from './store-utils.js';

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const STORE_API = {
    get: (id) => `/api/store/${id}/`,
    create: `/api/store/create/`,
    update: (id) => `/api/store/update/${id}/`,
    delete: (id) => `/api/store/delete/${id}/`
}


let currentStoreId = null;

function showAddStoreForm() {
    currentStoreId = null;
    document.getElementById('modalTitle').textContent = 'Add New Store';
    document.getElementById('storeForm').reset();
    document.getElementById('imagePreview').style.display = 'none';
    document.getElementById('storeModal').classList.remove('hidden');
    
    const createButton = document.getElementById("createButton");
    if (createButton) {
        createButton.addEventListener("click", function() {
            openModal("Add New Store");
        });
    } else {
        console.error('Create button not found');
    }
}

async function showEditStoreForm(storeId) {
    currentStoreId = storeId;
    document.querySelectorAll(".editButton").forEach(button => {
        button.addEventListener("click", function() {
            openModal("Edit Store");
        });
    });
    document.getElementById('modalTitle').textContent = 'Edit Store';
    
    try {
        const response = await fetch(STORE_API.get(storeId));
        if (!response.ok) throw new Error('Failed to fetch store data');
        
        const data = await response.json();
        const form = document.getElementById('storeForm');
        
        // Populate form fields
        Object.keys(data).forEach(key => {
            const input = form.elements[key];
            if (input) {
                input.value = data[key] || '';
            }
        });
        
        // Handle image preview

        document.getElementById('storeModal').classList.remove('hidden');
        
    } catch (error) {
        Toast.show(error.message, 'error');
    }
}


function closeModal() {
    clearFieldErrors();
    document.getElementById('storeModal').classList.add('hidden');
    document.getElementById('storeForm').reset();
    document.getElementById('imagePreview').style.display = 'none';
}

async function handleSubmit(e) {
    e.preventDefault();
    clearFieldErrors();
    
    const formData = new FormData(e.target);
    const errors = validateForm(formData);
    
    if (Object.keys(errors).length > 0) {
        Object.entries(errors).forEach(([field, message]) => {
            showFieldError(field, message);
        });
        return;
    }
    
    const url = currentStoreId ? STORE_API.update(currentStoreId) : STORE_API.create;
    const method = currentStoreId ? 'PUT' : 'POST';
    
    try {
        const response = await fetch(url, {
            method,
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.message || 'An error occurred');
        }
        
        Toast.show(currentStoreId ? 'Store updated successfully' : 'Store created successfully');
        closeModal();
        setTimeout(() => window.location.reload(), 1000);
        
    } catch (error) {
        Toast.show(error.message, 'error');
    }
}

async function deleteStore(storeId) {
    if (!confirm('Are you sure you want to delete this store?')) return;
    
    try {
        const response = await fetch(STORE_API.delete(storeId), {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.message || 'Failed to delete store');
        }
        
        Toast.show('Store deleted successfully');
        const storeElement = document.getElementById(`store-${storeId}`);
        storeElement.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => storeElement.remove(), 300);
        
    } catch (error) {
        Toast.show(error.message, 'error');
    }
}

export { showAddStoreForm, showEditStoreForm, closeModal, handleSubmit, deleteStore };
