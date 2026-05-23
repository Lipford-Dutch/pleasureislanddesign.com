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

// Contact Form Submission via Formspree
document.getElementById("contact-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const message = document.getElementById("message").value.trim();
    const formMessage = document.getElementById("form-message");
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (name === "" || !emailPattern.test(email) || message === "") {
        formMessage.style.display = "block";
        formMessage.style.color = "#cc0000";
        formMessage.innerText = "Please fill in all fields correctly.";
        return;
    }

    const submitButton = this.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    submitButton.innerText = "Sending...";

    fetch("https://formspree.io/f/pleasureislanddesign@gmail.com", {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify({ name, email, message })
    })
    .then(function(response) {
        if (response.ok) {
            formMessage.style.display = "block";
            formMessage.style.color = "#2e7d32";
            formMessage.innerText = "Thank you! We'll be in touch soon.";
            document.getElementById("contact-form").reset();
        } else {
            throw new Error("Form submission failed");
        }
    })
    .catch(function() {
        formMessage.style.display = "block";
        formMessage.style.color = "#cc0000";
        formMessage.innerText = "Something went wrong. Please call us at (910) 444-1230 or email pleasureislanddesign@gmail.com.";
    })
    .finally(function() {
        submitButton.disabled = false;
        submitButton.innerText = "Request a Free Consultation";
    });
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

// Scroll Tracking: Track milestone depths (25%, 50%, 75%, 100%)
(function() {
    var scrollMilestones = {};
    var scrollTimer;
    window.addEventListener('scroll', function() {
        clearTimeout(scrollTimer);
        scrollTimer = setTimeout(function() {
            var depth = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
            var milestones = [25, 50, 75, 100];
            milestones.forEach(function(m) {
                if (depth >= m && !scrollMilestones[m]) {
                    scrollMilestones[m] = true;
                    gtag('event', 'scroll', {
                        'event_category': 'Page Interaction',
                        'event_label': 'Scroll Depth ' + m + '%',
                        'value': m
                    });
                }
            });
        }, 200);
    });
})();

// Gallery Interaction Tracking 
document.querySelectorAll('.gallery-item img').forEach(image => {
    image.addEventListener('click', function() {
        gtag('event', 'click', {
            'event_category': 'Gallery',
            'event_label': this.alt
        });
    });
});



