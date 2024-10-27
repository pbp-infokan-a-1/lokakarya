console.log('Admin Dashboard JS Loaded');

// Utility function for CSRF token
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Product CRUD Operations
const productOperations = {
    add: async function(formData) {
        const response = await fetch('/add_product/', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCSRFToken()
            },
            body: formData
        }).then(response => response.json());
    },

    edit: async function(productId, formData) {
        const response = await fetch(`/edit_product/${productId}/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCSRFToken()
            },
            body: formData
        }).then(response => response.json());
    },

    delete: async function(productId) {
        const response = await fetch(`/delete_product/${productId}/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCSRFToken()
            }
        }).then(response => response.json());
    },

    refreshTable: function () {
        fetch('/products/', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('productsTableBody');
            tbody.innerHTML = data.products.map(product => `
                <tr data-product-id="${product.id}">
                    <td class="px-6 py-4 whitespace-nowrap">${product.name}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${product.category}</td>
                    <td class="px-6 py-4 whitespace-nowrap">Rp${product.min_price} - Rp${product.max_price}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${product.stores.join(', ')}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <button onclick="editProduct('${product.id}')" class="text-indigo-600 hover:text-indigo-900">Edit</button>
                        <button onclick="deleteProduct('${product.id}')" class="ml-2 text-red-600 hover:text-red-900">Delete</button>
                    </td>
                </tr>
            `).join('');

            // Update counter
            const productsCountElement = document.getElementById('products-count');
            if (productsCountElement) {
                productsCountElement.textContent = data.products.length;
            }
        });
    }
};

// Store CRUD Operations
const storeOperations = {
    add: async function(formData) {
        const response = await fetch('/add_store/', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCSRFToken()
            },
            body: formData
        }).then(response => response.json());
    },

    edit: async function(storeId, formData) {
        const response = await fetch(`/edit_store/${storeId}/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCSRFToken()
            },
            body: formData
        }).then(response => response.json());
    },

    delete: async function(storeId) {
        const response = await fetch(`/delete_store/${storeId}/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCSRFToken()
            }
        }).then(response => response.json());
    },

    refreshTable: function() {
        fetch('/stores/', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const tbody = document.getElementById('storesTableBody');
            tbody.innerHTML = data.stores.map(store => `
                <tr data-store-id="${store.id}">
                    <td class="px-6 py-4">
                        <div class="flex items-center">
                            ${store.image_url ? `<img src="${store.image_url}" class="h-10 w-10 rounded-full">` : ''}
                            <div class="ml-4">
                                <div class="text-sm font-medium text-gray-900">${store.nama}</div>
                            </div>
                        </div>
                    </td>
                    <td class="px-6 py-4">${store.hari_buka}</td>
                    <td class="px-6 py-4">
                        <div>📧 ${store.email}</div>
                        <div>📱 ${store.telepon}</div>
                    </td>
                    <td class="px-6 py-4">
                        ${store.gmaps_link ? `<a href="${store.gmaps_link}" class="text-blue-600 hover:text-blue-900 block" target="_blank">🗺 Maps</a>` : ''}
                        <!-- Removed page_link as it doesn't exist in the models -->
                    </td>
                    <td class="px-6 py-4">
                        <button onclick="editStore(${store.id})" class="text-indigo-600 hover:text-indigo-900">Edit</button>
                        <button onclick="deleteStore(${store.id})" class="ml-2 text-red-600 hover:text-red-900">Delete</button>
                    </td>
                </tr>
            `).join('');
            
            // Update counter
            const storesCountElement = document.getElementById('stores-count');
            if (storesCountElement) {
                storesCountElement.textContent = data.stores.length;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
};

// Modal Management
function openProductModal(productId = null) {
    const modal = document.getElementById('productModal');
    const form = modal.querySelector('form');
    const title = modal.querySelector('#productModalTitle');
    
    if (productId) {
        title.textContent = 'Edit Product';
        // Populate form with product data
        fetch(`/edit_product/${productId}/`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            // Populate form fields
            Object.keys(data.product).forEach(key => {
                const input = form.querySelector(`[name="${key}"]`);
                if (input) input.value = data.product[key];
            });
        });
    } else {
        title.textContent = 'Add Product';
        form.reset();
    }
    
    modal.classList.remove('hidden');
}

function openStoreModal(storeId = null) {
    const modal = document.getElementById('storeModal');
    const form = modal.querySelector('form');
    const title = modal.querySelector('#storeModalTitle');
    
    if (storeId) {
        title.textContent = 'Edit Store';
        fetch(`/edit_store/${storeId}/`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            Object.keys(data.store).forEach(key => {
                const input = form.querySelector(`[name="${key}"]`);
                if (input) input.value = data.store[key];
            });
        });
    } else {
        title.textContent = 'Add Store';
        form.reset();
    }
    
    modal.classList.remove('hidden');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.add('hidden');
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Product form submission
    document.querySelector('#productModal form').addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const productId = this.dataset.productId;
        
        (productId ? productOperations.edit(productId, formData) : productOperations.add(formData))
            .then(response => {
                if (response.success) {
                    closeModal('productModal');
                    productOperations.refreshTable();
                } else {
                    // Handle errors
                    Object.keys(response.errors).forEach(key => {
                        const input = this.querySelector(`[name="${key}"]`);
                        if (input) input.classList.add('border-red-500');
                    });
                }
            });
    });

    // Store form submission
    document.querySelector('#storeModal form').addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const storeId = this.dataset.storeId;
        
        (storeId ? storeOperations.edit(storeId, formData) : storeOperations.add(formData))
            .then(response => {
                if (response.success) {
                    closeModal('storeModal');
                    storeOperations.refreshTable();
                } else {
                    // Handle errors
                    Object.keys(response.errors).forEach(key => {
                        const input = this.querySelector(`[name="${key}"]`);
                        if (input) input.classList.add('border-red-500');
                    });
                }
            });
    });

    // Initial load of tables
    productOperations.refreshTable();
    storeOperations.refreshTable();
});

// Define editProduct and deleteProduct in the global scope
function editProduct(productId) {
    openProductModal(productId);
}

function deleteProduct(productId) {
    if (confirm('Are you sure you want to delete this product?')) {
        fetch(`/delete_product/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove the row from the table
                document.querySelector(`tr[data-product-id="${productId}"]`).remove();
            } else {
                alert('Error deleting product');
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

// Define editStore and deleteStore in the global scope
function editStore(storeId) {
    openStoreModal(storeId);
}

function deleteStore(storeId) {
    if (confirm('Are you sure you want to delete this store?')) {
        fetch(`/delete_store/${storeId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove the row from the table
                document.querySelector(`tr[data-store-id="${storeId}"]`).remove();
            } else {
                alert('Error deleting store');
            }
        })
        .catch(error => console.error('Error:', error));
    }
}