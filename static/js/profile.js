// Fetch profile data
async function getProfile() {
    return fetch("update/ajax", {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include'
    }).then((res) => res.json());
}

// Update profile data via POST
async function updateProfile() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const formData = new FormData(document.querySelector('#profileForm'));  // Assuming you have a form with id 'profileForm'
    
    return fetch("update/ajax", {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData,  // Send the form data (including files)
        credentials: 'include'
    }).then((res) => res.json());
}

// Refresh the displayed profile
async function refreshProfile() {
    const profile = await getProfile();  // Fetch the profile data using GET

    if (profile) {
        // Set the username in an h2 tag
        document.getElementById("username").innerHTML = `<h2 class="font-bold text-3xl text-black">${profile.username}</h2>`;
        
        // Set the bio, ensuring there's a label before the bio content
        document.getElementById("bio").innerHTML = `<strong>Bio:</strong> ${profile.bio === "" ? "No bio available" : profile.bio}`;
        
        // Set the location, ensuring it has an icon and is displayed as 'inline-item'
        document.getElementById("location").innerHTML = `<i class="fas fa-map-marker-alt"></i> ${profile.location === "" ? "Not specified" : profile.location}`;
        
        // Format the birth date in the 'F d, Y' format (e.g., 'October 25, 2024')
        let birthDateFormatted = "Birth date not available";
        if (profile.birth_date) {
            const birthDate = new Date(profile.birth_date);
            const options = { year: 'numeric', month: 'long', day: 'numeric' };
            birthDateFormatted = birthDate.toLocaleDateString('en-US', options);  // Format as 'October 25, 2024'
        }
        
        // Set the birth date with the formatted date
        document.getElementById("birth_date").innerHTML = `<i class="fas fa-birthday-cake ml-5"></i> ${birthDateFormatted}`;
    } else {
        console.error('Profile data is unavailable');
    }
}

const modal = document.getElementById('modal');
const modalContent = document.getElementById('modalContent');

function showModal() {
    modal.classList.remove('hidden');
    setTimeout(() => {
        modalContent.classList.remove('opacity-0', 'scale-95');
        modalContent.classList.add('opacity-100', 'scale-100');
    }, 50);
}

function hideModal() {
    modalContent.classList.remove('opacity-100', 'scale-100');
    modalContent.classList.add('opacity-0', 'scale-95');
    setTimeout(() => {
        modal.classList.add('hidden');
    }, 150);
}

document.getElementById("cancelButton").addEventListener("click", hideModal);
document.getElementById("closeModalButton").addEventListener("click", hideModal);

// Submit the profile form
document.getElementById('submitProfileForm').addEventListener('click', async function (e) {
    e.preventDefault();
    const result = await updateProfile();
    if (result.message === "UPDATED") {
        await refreshProfile();  // Reload profile data after update
        hideModal();
    } else {
        alert("Failed to update profile!");
    }
});

