
// document.addEventListener('DOMContentLoaded', function() {
//     const slides = document.querySelector('.slides');
//     const slide = document.querySelectorAll('.slide');
//     let currentIndex = 0;
//     const totalSlides = slide.length;
//     let slideInterval = null;

//     const firstSlideClone = slide[0].cloneNode(true);
//     slides.appendChild(firstSlideClone);

//     const indicators = document.querySelector('.indicators');
//     const dots = document.querySelectorAll('.dot');

//     function nextSlide() {
//         currentIndex++;
//         updateSlidePosition();

//         if (currentIndex === totalSlides) {
//             setTimeout(function() {
//                 slides.style.transition = 'none';
//                 currentIndex = 0;
//                 updateSlidePosition();
//                 setTimeout(function() {
//                     slides.style.transition = 'transform 0.5s ease-in-out';
//                 }, 50);
//             }, 500);
//         }
//         updateIndicators();
//     }

//     function updateSlidePosition() {
//         slides.style.transform = 'translateX(' + (-currentIndex * 100) + '%)';
//     }

//     function updateIndicators() {
//         dots.forEach((dot, index) => {
//             dot.classList.remove('active');
//             if (index === currentIndex % totalSlides) {
//                 dot.classList.add('active');
//             }
//         });
//     }

//     function currentSlide(index) {
//         currentIndex = index;
//         updateSlidePosition();
//         updateIndicators();
//     }

//     dots.forEach((dot, index) => {
//         dot.addEventListener('click', () => {
//             currentSlide(index);
//             clearInterval(slideInterval); // Tıklama sonrası otomatik geçişi durdur
//             slideInterval = setInterval(nextSlide, 5000); // Tekrar başlat
//         });
//     });

//     slideInterval = setInterval(nextSlide, 5000); 
// })
//HEADER SLİDER




//KARTLIK SLİDER
const wrapper = document.querySelector(".wrapper");
const carousel = document.querySelector(".carousel");
const firstCardWidth = carousel.querySelector(".card").offsetWidth;
const arrowBtns = document.querySelectorAll(".wrapper i");
const carouselChildrens = [...carousel.children];

let isDragging = false, isAutoPlay = true, startX, startScrollLeft, timeoutId;


let cardPerView = Math.round(carousel.offsetWidth / firstCardWidth);


carouselChildrens.slice(-cardPerView).reverse().forEach(card => {
    carousel.insertAdjacentHTML("afterbegin", card.outerHTML);
});


carouselChildrens.slice(0, cardPerView).forEach(card => {
    carousel.insertAdjacentHTML("beforeend", card.outerHTML);
});


carousel.classList.add("no-transition");
carousel.scrollLeft = carousel.offsetWidth;
carousel.classList.remove("no-transition");


arrowBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        carousel.scrollLeft += btn.id == "left" ? -firstCardWidth : firstCardWidth;
    });
});

const dragStart = (e) => {
    isDragging = true;
    carousel.classList.add("dragging");
    
    startX = e.pageX;
    startScrollLeft = carousel.scrollLeft;
}

const dragging = (e) => {
    if(!isDragging) return; 
    
    carousel.scrollLeft = startScrollLeft - (e.pageX - startX);
}

const dragStop = () => {
    isDragging = false;
    carousel.classList.remove("dragging");
}

const infiniteScroll = () => {
    
    if(carousel.scrollLeft === 0) {
        carousel.classList.add("no-transition");
        carousel.scrollLeft = carousel.scrollWidth - (2 * carousel.offsetWidth);
        carousel.classList.remove("no-transition");
    }
   
    else if(Math.ceil(carousel.scrollLeft) === carousel.scrollWidth - carousel.offsetWidth) {
        carousel.classList.add("no-transition");
        carousel.scrollLeft = carousel.offsetWidth;
        carousel.classList.remove("no-transition");
    }

    
    clearTimeout(timeoutId);
    // if(!wrapper.matches(":hover")) autoPlay();
}



carousel.addEventListener("mousedown", dragStart);
carousel.addEventListener("mousemove", dragging);
document.addEventListener("mouseup", dragStop);
carousel.addEventListener("scroll", infiniteScroll);
wrapper.addEventListener("mouseenter", () => clearTimeout(timeoutId));
// wrapper.addEventListener("mouseleave", autoPlay);
//KARTLIK SLİDER



































document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.dot');
    let currentIndex = 0;
    let slideInterval;

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.remove('active');
            dots[i].classList.remove('active');
            if (i === index) {
                slide.classList.add('active');
                dots[i].classList.add('active');
            }
        });
        currentIndex = index;
    }

    function nextSlide() {
        let nextIndex = (currentIndex + 1) % slides.length;
        showSlide(nextIndex);
    }

    function startSlideShow() {
        slideInterval = setInterval(nextSlide, 3000);
    }

    function stopSlideShow() {
        clearInterval(slideInterval);
    }

    dots.forEach(dot => {
        dot.addEventListener('click', () => {
            let index = parseInt(dot.getAttribute('data-index'));
            showSlide(index);
            stopSlideShow(); // Tıklayınca döngüyü durdur
            startSlideShow(); // Sonra tekrar başlat
        });
    });

    startSlideShow();
});

