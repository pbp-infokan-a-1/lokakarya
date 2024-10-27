$(document).ready(function() {
    // Create Product
    $('#create-product-form').on('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        $.ajax({
            url: '{% url "productpage:create_product_ajax" %}', // Django URL for creating a product
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                name: $('#product-name').val(),
                category: $('#product-category').val(),
                description: $('#product-description').val(),
                min_price: $('#product-min-price').val(),
                max_price: $('#product-max-price').val()
            }),
            success: function(response) {
                alert(response.message); // Show success message
                window.location.reload(); // Reload the page to show the new product
            },
            error: function(xhr) {
                alert(xhr.responseJSON.error); // Show error message
            }
        });
    });

    // Update Product
    $('.update-product-form').on('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
        const productId = $(this).data('product-id'); // Get the product ID from data attribute

        $.ajax({
            url: `/product/update/${productId}/`, // URL for updating a product
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                name: $(`#product-name-${productId}`).val(),
                category: $(`#product-category-${productId}`).val(),
                description: $(`#product-description-${productId}`).val(),
                min_price: $(`#product-min-price-${productId}`).val(),
                max_price: $(`#product-max-price-${productId}`).val()
            }),
            success: function(response) {
                alert(response.message); // Show success message
                window.location.reload(); // Reload the page to show the updated product
            },
            error: function(xhr) {
                alert(xhr.responseJSON.error); // Show error message
            }
        });
    });

    // Delete Product
    $('.delete-product-btn').on('click', function() {
        const productId = $(this).data('product-id'); // Get the product ID from data attribute

        if (confirm('Are you sure you want to delete this product?')) {
            $.ajax({
                url: `/product/delete/${productId}/`, // URL for deleting a product
                type: 'DELETE',
                success: function(response) {
                    alert(response.message); // Show success message
                    $(`#product-${productId}`).remove(); // Remove the product element
                },
                error: function(xhr) {
                    alert(xhr.responseJSON.error); // Show error message
                }
            });
        }
    });

    // Add Review
    $('#add-review-form').on('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
        const productId = $(this).data('product-id'); // Get the product ID from data attribute

        $.ajax({
            url: `/product/${productId}/add_review/`, // URL for adding a review
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                review: $('#review-text').val(),
                rating: $('#review-rating').val()
            }),
            success: function(response) {
                alert(response.message); // Show success message
                window.location.reload(); // Reload the page to show the new review
            },
            error: function(xhr) {
                alert(xhr.responseJSON.error); // Show error message
            }
        });
    });
});
