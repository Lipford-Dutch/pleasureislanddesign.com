// Sticky Header with Shrink Effect
window.addEventListener("scroll", function() {
    const header = document.querySelector(".header");
    if (window.scrollY > 50) {
        header.classList.add("shrink");
    } else {
        header.classList.remove("shrink");
    }
});

// Mobile Navigation Toggle
const hamburger = document.querySelector(".hamburger");
const navbar = document.querySelector(".navbar");

if (hamburger && navbar) {
    hamburger.addEventListener("click", () => {
        navbar.classList.toggle("active");
        hamburger.classList.toggle("toggle");
        hamburger.setAttribute('aria-expanded', hamburger.classList.contains('toggle'));
    });
}

// Scroll-Triggered Animations
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

function animateOnScroll() {
    const sections = document.querySelectorAll('.fade-in, .slide-up, .scale-in');
    sections.forEach(section => {
        if (isInViewport(section)) {
            section.classList.add('active');
        }
    });
}

window.addEventListener('scroll', animateOnScroll);
window.addEventListener('DOMContentLoaded', animateOnScroll);

// Lightbox for Gallery Images
const lightbox = document.createElement("div");
lightbox.id = "lightbox";
document.body.appendChild(lightbox);

lightbox.addEventListener("click", () => {
    lightbox.classList.remove("active");
});

const galleryImages = document.querySelectorAll(".gallery-item img");

galleryImages.forEach(image => {
    image.addEventListener("click", (e) => {
        lightbox.classList.add("active");
        const img = document.createElement("img");
        img.src = e.target.src;
        while (lightbox.firstChild) {
            lightbox.removeChild(lightbox.firstChild);
        }
        lightbox.appendChild(img);
    });
});

// Contact Form Validation
document.getElementById("contact-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form submission to check validation

    // Retrieve form fields
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const message = document.getElementById("message").value.trim();
    const formMessage = document.getElementById("form-message");

    // Regular expression for validating email format
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // Validation checks
    if (name === "" || !emailPattern.test(email) || message === "") {
        formMessage.style.display = "block";
        formMessage.innerText = "Please fill in all fields correctly.";
    } else {
        formMessage.style.display = "none";

        // If validation passes, simulate form submission
        alert("Form submitted successfully!"); // Replace with actual submission logic (e.g., AJAX call)
        document.getElementById("contact-form").reset(); // Clear the form
    }
});

// Activate Testimonials Section
document.addEventListener('DOMContentLoaded', () => {
    const testimonials = document.querySelector('.testimonial-grid');

    function activateTestimonials() {
        const rect = testimonials.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom >= 0) {
            testimonials.classList.add('active');
        }
    }

    window.addEventListener('scroll', activateTestimonials);
    activateTestimonials(); // Run initially in case it's already in view
});

// Tracks user interactions like button clicks or form submissions.
document.querySelector('.cta-button').addEventListener('click', function() {
  gtag('event', 'click', {
    'event_category': 'Button',
    'event_label': 'Explore Our Services'
  });
});

// Scroll Tracking: Track how far users scroll on long pages.
window.addEventListener('scroll', function() {
    let scrollDepth = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
    gtag('event', 'scroll', {
        'event_category': 'Page Interaction',
        'event_label': 'Scroll Depth',
        'value': scrollDepth
    });
});

// Gallery Interaction Tracking 
document.querySelectorAll('.gallery-item img').forEach(image => {
    image.addEventListener('click', function() {
        gtag('event', 'click', {
            'event_category': 'Gallery',
            'event_label': this.alt
        });
    });
});



