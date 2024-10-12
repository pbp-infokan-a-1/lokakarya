let currentSlide = 0;
const slides = document.querySelectorAll('.hero-img');
const totalSlides = slides.length;
const slider = document.querySelector('.hero-slider');
const slideWidth = 100; // percentage width of each slide
const autoSlideInterval = 5000;

// Clone the first and last slide
const firstClone = slides[0].cloneNode(true);
const lastClone = slides[slides.length - 1].cloneNode(true);
slider.appendChild(firstClone);
slider.insertBefore(lastClone, slides[0]);

// Update total slides to include clones
const totalSlidesWithClones = totalSlides + 2;

// Adjust the initial position to show the first slide properly
slider.style.transform = `translateX(-${slideWidth}%)`;

// Function to move to the next slide
function goToNextSlide() {
    if (currentSlide < totalSlides - 1) {
        currentSlide++;
        slider.style.transition = 'transform 0.5s ease-in-out';
        slider.style.transform = `translateX(-${(currentSlide + 1) * slideWidth}%)`;
    } else {
        // Move to the cloned first slide
        currentSlide++;
        slider.style.transition = 'transform 0.5s ease-in-out';
        slider.style.transform = `translateX(-${(currentSlide + 1) * slideWidth}%)`;

        // After the transition, jump back to the real first slide without animation
        setTimeout(() => {
            slider.style.transition = 'none';
            currentSlide = 0;
            slider.style.transform = `translateX(-${slideWidth}%)`;
        }, 500);
    }
}

// Function to move to the previous slide
function goToPrevSlide() {
    if (currentSlide > 0) {
        currentSlide--;
        slider.style.transition = 'transform 0.5s ease-in-out';
        slider.style.transform = `translateX(-${(currentSlide + 1) * slideWidth}%)`;
    } else {
        // Move to the cloned last slide
        slider.style.transition = 'transform 0.5s ease-in-out';
        currentSlide--;
        slider.style.transform = `translateX(0%)`;
        // After the transition, jump back to the real last slide without animation
        setTimeout(() => {
            slider.style.transition = 'none';
            currentSlide = totalSlides - 1;
            slider.style.transform = `translateX(-${totalSlides * slideWidth}%)`;
        }, 500);
    }
}

// Event listeners for the next and prev buttons
document.querySelector('.next').addEventListener('click', goToNextSlide);
document.querySelector('.prev').addEventListener('click', goToPrevSlide);

// Automatically switch slides every few seconds
let autoSlide = setInterval(goToNextSlide, autoSlideInterval);

// Pause auto-slide when the user interacts with the slider (optional)
slider.addEventListener('mouseover', () => clearInterval(autoSlide));
slider.addEventListener('mouseout', () => {
    autoSlide = setInterval(goToNextSlide, autoSlideInterval);
});
