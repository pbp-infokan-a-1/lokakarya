// Open and close modal functions
function openReviewModal(productId) {
    document.querySelector('.review-section').dataset.productId = productId;
    document.getElementById('reviewModal').classList.remove('hidden');
}

function closeReviewModal() {
    document.getElementById('reviewModal').classList.add('hidden');
}

// Submit review via AJAX
async function submitReview() {
    const productId = document.querySelector('.review-section').dataset.productId;
    const reviewText = document.getElementById('review-text').value;
    const reviewRating = document.querySelector('.rating input').value;

    if (!reviewRating) {
        alert('Please provide a rating.');
        return;
    }

    try {
        const response = await fetch(`/api/products/${productId}/rate/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                review: reviewText,
                rating: reviewRating
            }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        alert(data.message);
        closeReviewModal();
        window.location.reload();
    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong');
    }
}

// Star rating interaction
const allStar = document.querySelectorAll('.rating .star');
const ratingValue = document.querySelector('.rating input');

allStar.forEach((item, idx) => {
    item.addEventListener('click', function () {
        let click = 0;
        ratingValue.value = idx + 1;

        allStar.forEach(i => {
            i.classList.replace('bxs-star', 'bx-star');
            i.classList.remove('active');
        });
        for (let i = 0; i < allStar.length; i++) {
            if (i <= idx) {
                allStar[i].classList.replace('bx-star', 'bxs-star');
                allStar[i].classList.add('active');
            } else {
                allStar[i].style.setProperty('--i', click);
                click++;
            }
        }
    });
});

// CSRF Token Helper
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

document.addEventListener("DOMContentLoaded", function() {
    // Load initial reviews
    loadReviews();

    // AJAX form submission for adding a review
    document.getElementById("add-review-form").onsubmit = function(event) {
        event.preventDefault();
        const url = this.getAttribute("data-url");
        const formData = new FormData(this);

        fetch(url, {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": "{{ csrf_token }}" }
        })
        .then(response => response.json())
        .then(data => {
            if (data.errors) {
                console.error("Form errors:", data.errors);
            } else {
                // Insert the new review at the top of the list
                document.getElementById("reviews-list").insertAdjacentHTML('afterbegin', `
                    <div class="review flex items-start my-4">
                        <img src="${data.profile_pic}" alt="${data.username}" class="w-10 h-10 rounded-full mr-3">
                        <div>
                            <p><strong>${data.username}</strong> <span class="text-gray-500 text-sm">(${data.created_at})</span></p>
                            <div class="star-rating text-yellow-500">${renderStars(data.rating)}</div>
                            ${data.comment ? `<p>${data.comment}</p>` : ''}
                        </div>
                    </div>
                `);
                document.getElementById("add-review-form").reset();
            }
        });
    };

    // Load reviews with pagination
    let page = 1;
    document.getElementById("load-more-reviews").onclick = function() {
        page++;
        loadReviews(page);
    };

    function loadReviews(page = 1) {
        fetch(`/api/products/{{ product.id }}/reviews/?page=${page}`)
        .then(response => response.json())
        .then(data => {
            data.reviews.forEach(review => {
                document.getElementById("reviews-list").insertAdjacentHTML('beforeend', `
                    <div class="review flex items-start my-4">
                        <img src="${review.profile_pic}" alt="${review.username}" class="w-10 h-10 rounded-full mr-3">
                        <div>
                            <p><strong>${review.username}</strong> <span class="text-gray-500 text-sm">(${review.created_at})</span></p>
                            <div class="star-rating text-yellow-500">${renderStars(review.rating)}</div>
                            ${review.comment ? `<p>${review.comment}</p>` : ''}
                        </div>
                    </div>
                `);
            });

            if (!data.has_next) {
                document.getElementById("load-more-reviews").style.display = 'none'; // Hide button if no more reviews
            }
        });
    }

    // Helper function to render star ratings
    function renderStars(rating) {
        return "★".repeat(rating) + "☆".repeat(5 - rating);
    }
});


// $(document).ready(function() {
//     // Create Product
//     $('#create-product-form').on('submit', function(event) {
//         event.preventDefault(); // Prevent the default form submission

//         $.ajax({
//             url: '/api/products/create/', // Updated API URL for creating a product
//             type: 'POST',
//             contentType: 'application/json',
//             data: JSON.stringify({
//                 name: $('#product-name').val(),
//                 category: $('#product-category').val(),
//                 description: $('#product-description').val(),
//                 min_price: $('#product-min-price').val(),
//                 max_price: $('#product-max-price').val()
//             }),
//             success: function(response) {
//                 alert(response.message); // Show success message
//                 window.location.reload(); // Reload the page to show the new product
//             },
//             error: function(xhr) {
//                 alert(xhr.responseJSON.error); // Show error message
//             }
//         });
//     });

//     // Update Product
//     $('.update-product-form').on('submit', function(event) {
//         event.preventDefault(); // Prevent the default form submission
//         const productId = $(this).data('product-id'); // Get the product ID from data attribute

//         $.ajax({
//             url: `/api/products/${productId}/update/`, // Updated API URL for updating a product
//             type: 'POST',
//             contentType: 'application/json',
//             data: JSON.stringify({
//                 name: $(`#product-name-${productId}`).val(),
//                 category: $(`#product-category-${productId}`).val(),
//                 description: $(`#product-description-${productId}`).val(),
//                 min_price: $(`#product-min-price-${productId}`).val(),
//                 max_price: $(`#product-max-price-${productId}`).val()
//             }),
//             success: function(response) {
//                 alert(response.message); // Show success message
//                 window.location.reload(); // Reload the page to show the updated product
//             },
//             error: function(xhr) {
//                 alert(xhr.responseJSON.error); // Show error message
//             }
//         });
//     });

//     // Delete Product
//     $('.delete-product-btn').on('click', function() {
//         const productId = $(this).data('product-id'); // Get the product ID from data attribute

//         if (confirm('Are you sure you want to delete this product?')) {
//             $.ajax({
//                 url: `/api/products/${productId}/delete/`, // Updated API URL for deleting a product
//                 type: 'DELETE',
//                 success: function(response) {
//                     alert(response.message); // Show success message
//                     $(`#product-${productId}`).remove(); // Remove the product element
//                 },
//                 error: function(xhr) {
//                     alert(xhr.responseJSON.error); // Show error message
//                 }
//             });
//         }
//     });

//     // Add Review
//     $('#add-review-form').on('submit', function(event) {
//         event.preventDefault(); // Prevent the default form submission
//         const productId = $(this).data('product-id'); // Get the product ID from data attribute

//         $.ajax({
//             url: `/api/products/${productId}/rate/`, // Updated API URL for adding a review
//             type: 'POST',
//             contentType: 'application/json',
//             data: JSON.stringify({
//                 review: $('#review-text').val(),
//                 rating: $('#review-rating').val()
//             }),
//             success: function(response) {
//                 alert(response.message); // Show success message
//                 window.location.reload(); // Reload the page to show the new review
//             },
//             error: function(xhr) {
//                 alert(xhr.responseJSON.error); // Show error message
//             }
//         });
//     });
// });
