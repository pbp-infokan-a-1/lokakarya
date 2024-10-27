// Store CRUD operations
let currentStoreId = null;

function showAddStoreForm() {
    currentStoreId = null;
    document.getElementById('modalTitle').textContent = 'Add New Store';
    document.getElementById('storeForm').reset();
    document.getElementById('storeModal').classList.remove('hidden');
}

function showEditStoreForm(storeId) {
    currentStoreId = storeId;
    document.getElementById('modalTitle').textContent = 'Edit Store';
    
    // Fetch store data and populate form
    fetch(`/api/store/${storeId}/`)
        .then(response => response.json())
        .then(data => {
            const form = document.getElementById('storeForm');
            form.nama.value = data.nama;
            form.alamat.value = data.alamat;
            form.hari_buka.value = data.hari_buka;
            form.email.value = data.email;
            form.telepon.value = data.telepon;
            form.gmaps_link.value = data.gmaps_link || '';
        });
    
    document.getElementById('storeModal').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('storeModal').classList.add('hidden');
}

document.getElementById('storeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    const url = currentStoreId 
        ? `/store/update/${currentStoreId}/`
        : '/store/create/';
        
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            window.location.reload();
        } else {
            alert('An error occurred');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred');
    }
});

async function deleteStore(storeId) {
    if (!confirm('Are you sure you want to delete this store?')) return;
    
    try {
        const response = await fetch(`/store/delete/${storeId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        if (response.ok) {
            document.getElementById(`store-${storeId}`).remove();
        } else {
            alert('An error occurred');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred');
    }
}

// Tambahkan ini di file JavaScript
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

// Gunakan saat membuat request
const csrftoken = getCookie('csrftoken');
fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
    },
    body: JSON.stringify(data)
});

document.getElementById('storeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    const url = currentStoreId 
        ? `/store/update/${currentStoreId}/`
        : '/store/create/';
        
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            window.location.reload();
        } else {
            alert('An error occurred');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred');
    }
});

console.log("ajax.js loaded successfully");