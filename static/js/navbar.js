document.addEventListener('DOMContentLoaded', function () {
    const hamburger = document.querySelector('.hamburger');
    const navLinksMobile = document.querySelector('.nav-links-mobile');

    hamburger.addEventListener('click', () => {
        navLinksMobile.classList.toggle('hidden');
    });
});