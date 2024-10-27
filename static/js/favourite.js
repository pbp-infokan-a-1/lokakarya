console.log("hi");
function get_csrf() {
  const csrfToken = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="))
    ?.split("=")[1];
  return csrfToken || "";
}

function toggleFavorite(productId) {
  fetch(`/favourites/toggle/${productId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": get_csrf(), // Include CSRF token for security
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        const button = document.getElementById("toggle-favorite");
        button.textContent = data.is_favorited
          ? "Remove from Favorites"
          : "Add to Favorites";
      } else {
        alert(data.message);
      }
    })
    .catch((error) => console.error("Error:", error));
}
