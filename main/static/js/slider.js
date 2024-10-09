let currentSlide = 0;
const slides = document.querySelectorAll('.hero-img');
const totalSlides = slides.length;
const slider = document.querySelector('.hero-slider');
const slideWidth = 100; // percentage width of each slide

document.querySelector('.next').addEventListener('click', () => {
    if (currentSlide < totalSlides - 1) {
        currentSlide++;
        slider.style.transition = 'transform 0.5s ease-in-out';
        slider.style.transform = `translateX(-${currentSlide * slideWidth}%)`;
    }
    if (currentSlide === totalSlides - 1) {
        setTimeout(() => {
            slider.style.transition = 'none';
            currentSlide = 0;
            slider.style.transform = `translateX(0)`;
        }, 500);
    }
});

document.querySelector('.prev').addEventListener('click', () => {
    if (currentSlide > 0) {
        currentSlide--;
        slider.style.transition = 'transform 0.5s ease-in-out';
        slider.style.transform = `translateX(-${currentSlide * slideWidth}%)`;
    } else {
        slider.style.transition = 'none';
        currentSlide = totalSlides - 2;
        slider.style.transform = `translateX(-${currentSlide * slideWidth}%)`;
        setTimeout(() => {
            slider.style.transition = 'transform 0.5s ease-in-out';
            currentSlide--;
            slider.style.transform = `translateX(-${currentSlide * slideWidth}%)`;
        }, 20);
    }
});
