const carousel = document.getElementById('carouselExample');
const items = carousel.querySelectorAll('.carousel-item');

const nextButton = document.querySelector('.carousel-control-next');
const prevButton = document.querySelector('.carousel-control-prev');

nextButton.addEventListener('click', () => {
  const activeItem = carousel.querySelector('.carousel-item.active');
  const currentIndex = Array.from(items).indexOf(activeItem);
  const nextIndex = (currentIndex + 1) % items.length;
  items[nextIndex].classList.add('active');
  activeItem.classList.remove('active');
});

prevButton.addEventListener('click', () => {
  const activeItem = carousel.querySelector('.carousel-item.active');
  const currentIndex = Array.from(items).indexOf(activeItem);
  const prevIndex = (currentIndex - 1 + items.length) % items.length;
  items[prevIndex].classList.add('active');
  activeItem.classList.remove('active');
});
