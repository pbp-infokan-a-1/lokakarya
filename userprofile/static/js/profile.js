async function getProfile() {
    return fetch("/profile/").then((res) => res.json())
}

async function refreshProfile() {
    const profile = await getProfile();
    document.getElementById("nama").innerHTML = profile[0].fields.nama;
    document.getElementById("username").innerHTML = "@" + profile[0].fields.username;
    document.getElementById("deskripsi").innerHTML = profile[0].fields.deskripsi == "" ? "Belum ada bio." : profile[0].fields.deskripsi;
    document.getElementById("avatar").src = profile[0].fields.foto ? "/media/" + profile[0].fields.foto : "/static/images/avatar.png";
}

const modal = document.getElementById('modal');
const modalContent = document.getElementById('modalContent');

function showModal() {
    const modal = document.getElementById('modal');
    const modalContent = document.getElementById('modalContent');

    modal.classList.remove('hidden');
    setTimeout(() => {
        modalContent.classList.remove('opacity-0', 'scale-95');
        modalContent.classList.add('opacity-100', 'scale-100');
    }, 50);
}

function hideModal() {
    const modal = document.getElementById('modal');
    const modalContent = document.getElementById('modalContent');

    modalContent.classList.remove('opacity-100', 'scale-100');
    modalContent.classList.add('opacity-0', 'scale-95');

    setTimeout(() => {
        modal.classList.add('hidden');
    }, 150);
}

document.getElementById("cancelButton").addEventListener("click", hideModal);
document.getElementById("closeModalButton").addEventListener("click", hideModal);

function editProfile() {
    fetch("/profile/", {
        method: "POST",
        body: new FormData(document.querySelector('#profileForm')),
    }).then(response => refreshProfile())

    hideModal();

    return false;
}

document.getElementById("submitProfileForm").onclick = editProfile