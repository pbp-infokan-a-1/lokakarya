function openReviewModal(productId, reviewId = null, existingReviewText = '', existingReviewRating = 0) {
  document.querySelector('.review-section').dataset.productId = productId;
  
  if (reviewId) {
      document.getElementById('review-text').value = existingReviewText;
      const ratingValue = document.querySelector('.rating input');
      ratingValue.value = existingReviewRating;

      // Set the stars based on the existing rating
      const allStar = document.querySelectorAll('.rating .star');
      allStar.forEach((item, idx) => {
          if (idx < existingReviewRating) {
              item.classList.replace('bx-star', 'bxs-star');
              item.classList.add('active');
          } else {
              item.classList.replace('bxs-star', 'bx-star');
              item.classList.remove('active');
          }
      });

      document.querySelector('.review-section').dataset.reviewId = reviewId;
  } else {
      document.getElementById('review-text').value = '';
      document.querySelector('.rating input').value = '';
      allStar.forEach(item => {
          item.classList.replace('bxs-star', 'bx-star');
          item.classList.remove('active');
      });
  }

  document.getElementById('reviewModal').classList.remove('hidden');
}

function closeReviewModal() {
  document.getElementById('reviewModal').classList.add('hidden');
}

// Submit review via AJAX
async function submitReview() {
  const productId = document.querySelector('.review-section').dataset.productId;
  const reviewId = document.querySelector('.review-section').dataset.reviewId || null;
  const reviewText = document.getElementById('review-text').value;
  const reviewRating = document.querySelector('.rating input').value;

  if (!reviewRating) {
      alert('Please provide a rating.');
      return;
  }

  const url = reviewId ? `/api/products/${productId}/update_rate/${reviewId}/` : `/api/products/${productId}/rate/`;

  try {
      const response = await fetch(url, {
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

// Delete review via AJAX
async function deleteReview(productId, reviewId) {
  if (confirm("Are you sure you want to delete this review?")) {
      try {
          const response = await fetch(`/api/products/${productId}/delete_rate/${reviewId}/`, {
              method: 'DELETE',
              headers: {
                  'X-CSRFToken': getCookie('csrftoken'),
              },
          });

          if (!response.ok) {
              throw new Error('Network response was not ok');
          }

          const data = await response.json();
          alert(data.message);
          window.location.reload();
      } catch (error) {
          console.error('Error:', error);
          alert('Something went wrong');
      }
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


var swiper = new Swiper('.swiper-container', {
    slidesPerView: 5,  // Adjust the number of slides visible at once
    spaceBetween: 20,  // Space between slides
    loop: true,  // Enable continuous loop mode
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    breakpoints: {
      640: {
        slidesPerView: 1,
        spaceBetween: 10,
      },
      768: {
        slidesPerView: 3,
        spaceBetween: 15,
      },
      1024: {
        slidesPerView: 4,
        spaceBetween: 20,
      },
    },
  });

  function addToWishlist(productName) {
    const popup = document.getElementById('wishlistPopup');
    const message = document.getElementById('wishlistMessage');

    // Update message and show popup
    message.textContent = `Added ${productName} to Favourites!`;
    popup.classList.remove('hidden');

    // Set a timeout to auto-hide popup after 3 seconds
    clearTimeout(popupTimeout);
    popupTimeout = setTimeout(() => {
        popup.classList.add('hidden');
    }, 3000);
  }

  // Cancel the auto-hide if closed manually
  function closePopup() {
    const popup = document.getElementById('wishlistPopup');
    popup.classList.add('hidden');
    clearTimeout(popupTimeout);
  }

  document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    if (searchInput.value === "None") {
      searchInput.value = "";
    }
  });

  function addToWishlist(productName) {
      document.getElementById('wishlistMessage').innerText = `Added ${productName} to Favourites!`;
      document.getElementById('wishlistPopup').classList.remove('hidden');
      setTimeout(() => {
        closePopup('wishlistPopup');
      }, 2000);
  }

  function closePopup(popupId) {
    const popup = document.getElementById('wishlistPopup');
    popup.classList.add('hidden');
    clearTimeout(popupTimeout);
  }