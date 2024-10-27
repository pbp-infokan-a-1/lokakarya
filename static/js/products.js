// Static/js/products.js
function openProductModal() {
    document.getElementById('productModal').classList.remove('hidden');
}

function closeProductModal() {
    document.getElementById('productModal').classList.add('hidden');
}

document.addEventListener('DOMContentLoaded', function() {
    const productForm = document.getElementById('productForm');
    
    productForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        
        fetch('/add_product/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Close modal and refresh product list
                closeProductModal();
                refreshProductList();
            } else {
                // Handle errors
                alert(data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while saving the product');
        });
    });
});

function refreshProductList() {
    fetch('/products/')
        .then(response => response.json())
        .then(data => {
            // Update your product list UI here
            const productList = document.querySelector('#productList');
            // Clear existing products
            productList.innerHTML = '';
            
            // Add new products
            data.products.forEach(product => {
                const productElement = createProductElement(product);
                productList.appendChild(productElement);
            });
        })
        .catch(error => console.error('Error:', error));
}

function createProductElement(product) {
    // Create and return a DOM element for the product
    const div = document.createElement('div');
    div.className = 'product-item';
    div.innerHTML = `
        <div class="flex items-center justify-between p-4 border-b">
            <div>
                <h3 class="text-lg font-medium">${product.name}</h3>
                <p class="text-sm text-gray-500">${product.description}</p>
                <p class="text-sm">Price: $${product.min_price} - $${product.max_price}</p>
            </div>
            <div>
                <button onclick="editProduct('${product.id}')" class="text-indigo-600 hover:text-indigo-900 mr-3">Edit</button>
                <button onclick="deleteProduct('${product.id}')" class="text-red-600 hover:text-red-900">Delete</button>
            </div>
        </div>
    `;
    return div;
}