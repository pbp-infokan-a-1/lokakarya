document.addEventListener('DOMContentLoaded', function () {
    const hamburger = document.querySelector('.hamburger');
    const mobileMenu = document.querySelector('.mobile-menu');
    const categoriesTab = document.getElementById('categories-tab');
    const menuTab = document.getElementById('menu-tab');
    const categoriesList = document.getElementById('categories-list');
    const menuList = document.getElementById('menu-list');

    // Toggle mobile menu visibility
    hamburger.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
    });

    menuTab.addEventListener('click', () => {
        menuList.classList.remove('hidden');
        categoriesList.classList.add('hidden');
        menuTab.classList.add('active-tab');
        categoriesTab.classList.remove('active-tab');
    });

    // Switch between Categories and Menu lists
    categoriesTab.addEventListener('click', () => {
        categoriesList.classList.remove('hidden');
        menuList.classList.add('hidden');
        categoriesTab.classList.add('active-tab');
        menuTab.classList.remove('active-tab');
    });
});
