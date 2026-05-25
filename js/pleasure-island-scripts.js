/* Pleasure Island Design — Main Scripts */
/* jshint esversion: 11 */

(function () {
  'use strict';

  /* ================================================================
     UTILITIES
     ================================================================ */
  function safeGtag(...args) {
    if (typeof gtag === 'function') {gtag(...args);}
  }

  function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
  }

  /* ================================================================
     HEADER: Scroll shadow + active nav highlighting
     ================================================================ */
  function initHeader() {
    const header = document.getElementById('site-header');
    if (!header) {return;}

    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
    const sections = [];

    navLinks.forEach(link => {
      const id = link.getAttribute('href').slice(1);
      const section = document.getElementById(id);
      if (section) {sections.push({ link, section });}
    });

    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          const scrollY = window.scrollY;

          // Header style
          header.classList.toggle('scrolled', scrollY > 60);

          // Active nav link
          let current = '';
          sections.forEach(({ section }) => {
            if (scrollY >= section.offsetTop - 120) {
              current = section.id;
            }
          });

          sections.forEach(({ link, section }) => {
            link.classList.toggle('active', section.id === current);
          });

          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  }

  /* ================================================================
     HAMBURGER MENU
     ================================================================ */
  function initHamburger() {
    const hamburger = document.getElementById('hamburger');
    const nav = document.getElementById('primary-nav');
    if (!hamburger || !nav) {return;}

    hamburger.addEventListener('click', () => {
      const expanded = hamburger.getAttribute('aria-expanded') === 'true';
      hamburger.setAttribute('aria-expanded', String(!expanded));
      nav.classList.toggle('open', !expanded);
    });

    // Close on nav link click (mobile)
    nav.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        hamburger.setAttribute('aria-expanded', 'false');
        nav.classList.remove('open');
      });
    });

    // Close on outside click
    document.addEventListener('click', e => {
      if (!hamburger.contains(e.target) && !nav.contains(e.target)) {
        hamburger.setAttribute('aria-expanded', 'false');
        nav.classList.remove('open');
      }
    });
  }

  /* ================================================================
     HERO: Ken Burns effect trigger + visual img load
     ================================================================ */
  function initHero() {
    const hero = document.querySelector('.hero');
    if (!hero) {return;}
    const img = hero.querySelector('.hero-visual-img');
    if (img && img.complete) {
      hero.classList.add('loaded');
    } else if (img) {
      img.addEventListener('load', () => hero.classList.add('loaded'));
    } else {
      setTimeout(() => hero.classList.add('loaded'), 100);
    }
  }

  /* ================================================================
     MOBILE STICKY CTA BAR
     ================================================================ */
  function initMobileStickyBar() {
    const bar = document.getElementById('mobile-cta-bar');
    if (!bar) {return;}
    let shown = false;

    window.addEventListener('scroll', () => {
      const pastHero = window.scrollY > window.innerHeight * 0.6;
      if (pastHero && !shown) {
        bar.removeAttribute('hidden');
        shown = true;
      } else if (!pastHero && shown) {
        bar.setAttribute('hidden', '');
        shown = false;
      }
    }, { passive: true });
  }

  /* ================================================================
     STAT COUNTERS (IntersectionObserver)
     ================================================================ */
  function initStatCounters() {
    const stats = document.querySelectorAll('.stat-number[data-target]');
    if (!stats.length) {return;}

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) {return;}
        observer.unobserve(entry.target);
        animateCounter(entry.target);
      });
    }, { threshold: 0.5 });

    stats.forEach(el => observer.observe(el));
  }

  function animateCounter(el) {
    const target = parseInt(el.dataset.target, 10);
    const duration = 1600;
    el.textContent = '0'; // Reset to 0 for animation
    const start = performance.now();

    function step(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      el.textContent = Math.round(eased * target);
      if (progress < 1) {requestAnimationFrame(step);}
    }

    requestAnimationFrame(step);
  }

  /* ================================================================
     SCROLL REVEAL (IntersectionObserver)
     ================================================================ */
  function initReveal() {
    const reveals = document.querySelectorAll('.reveal');
    if (!reveals.length) {return;}

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) {return;}
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    reveals.forEach(el => observer.observe(el));
  }

  /* ================================================================
     GALLERY FILTER
     ================================================================ */
  function initGalleryFilter() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const items = document.querySelectorAll('.gallery-item');
    if (!filterBtns.length) {return;}

    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const filter = btn.dataset.filter;

        filterBtns.forEach(b => {
          b.classList.remove('active');
          b.setAttribute('aria-selected', 'false');
        });
        btn.classList.add('active');
        btn.setAttribute('aria-selected', 'true');

        items.forEach(item => {
          const match = filter === 'all' || item.dataset.category === filter;
          item.classList.toggle('hidden', !match);
        });
      });
    });
  }

  /* ================================================================
     BEFORE / AFTER SLIDER
     ================================================================ */
  function initBeforeAfterSliders() {
    document.querySelectorAll('.before-after-slider').forEach(slider => {
      const before = slider.querySelector('.slider-before');
      const handle = slider.querySelector('.slider-handle');
      if (!before || !handle) {return;}

      // Add BEFORE/AFTER labels
      const lblBefore = document.createElement('span');
      lblBefore.className = 'slider-label slider-label-before';
      lblBefore.textContent = 'Before';
      const lblAfter = document.createElement('span');
      lblAfter.className = 'slider-label slider-label-after';
      lblAfter.textContent = 'After';
      slider.appendChild(lblBefore);
      slider.appendChild(lblAfter);

      let dragging = false;

      function setPosition(pct) {
        pct = clamp(pct, 0, 100);
        before.style.clipPath = `inset(0 ${100 - pct}% 0 0)`;
        handle.style.left = `${pct}%`;
        handle.setAttribute('aria-valuenow', Math.round(pct));
      }

      function getPct(clientX) {
        const rect = slider.getBoundingClientRect();
        return ((clientX - rect.left) / rect.width) * 100;
      }

      // Mouse
      handle.addEventListener('mousedown', e => { dragging = true; e.preventDefault(); });
      window.addEventListener('mousemove', e => { if (dragging) {setPosition(getPct(e.clientX));} });
      window.addEventListener('mouseup', () => { dragging = false; });

      // Touch
      handle.addEventListener('touchstart', e => { dragging = true; e.preventDefault(); }, { passive: false });
      window.addEventListener('touchmove', e => {
        if (dragging) {setPosition(getPct(e.touches[0].clientX));}
      }, { passive: true });
      window.addEventListener('touchend', () => { dragging = false; });

      // Keyboard
      handle.addEventListener('keydown', e => {
        const step = e.shiftKey ? 10 : 5;
        const current = parseFloat(handle.getAttribute('aria-valuenow') || 50);
        if (e.key === 'ArrowLeft')  { setPosition(current - step); e.preventDefault(); }
        if (e.key === 'ArrowRight') { setPosition(current + step); e.preventDefault(); }
      });

      setPosition(50);
    });
  }

  /* ================================================================
     TESTIMONIALS CAROUSEL
     ================================================================ */
  function initCarousel() {
    const track = document.getElementById('testimonials-track');
    const prevBtn = document.getElementById('carousel-prev');
    const nextBtn = document.getElementById('carousel-next');
    const dotsContainer = document.getElementById('carousel-dots');
    if (!track) {return;}

    const cards = track.querySelectorAll('.testimonial-card');
    if (!cards.length) {return;}

    let current = 0;
    let autoTimer;

    // Build dots
    cards.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.className = 'carousel-dot' + (i === 0 ? ' active' : '');
      dot.setAttribute('aria-label', `Go to testimonial ${i + 1}`);
      dot.setAttribute('role', 'tab');
      dot.addEventListener('click', () => goTo(i));
      dotsContainer.appendChild(dot);
    });

    const dots = dotsContainer.querySelectorAll('.carousel-dot');

    function goTo(index) {
      current = (index + cards.length) % cards.length;
      track.style.transform = `translateX(calc(-${current * 100}% - ${current} * var(--space-6, 1.5rem)))`;
      dots.forEach((d, i) => d.classList.toggle('active', i === current));
      resetAuto();
    }

    function resetAuto() {
      clearInterval(autoTimer);
      autoTimer = setInterval(() => goTo(current + 1), 5000);
    }

    prevBtn && prevBtn.addEventListener('click', () => goTo(current - 1));
    nextBtn && nextBtn.addEventListener('click', () => goTo(current + 1));

    // Keyboard on carousel region
    const region = document.getElementById('testimonials-carousel');
    if (region) {
      region.addEventListener('keydown', e => {
        if (e.key === 'ArrowLeft')  {goTo(current - 1);}
        if (e.key === 'ArrowRight') {goTo(current + 1);}
      });
    }

    resetAuto();
  }

  /* ================================================================
     LIGHTBOX (for single gallery images)
     ================================================================ */
  function initLightbox() {
    const lightbox = document.getElementById('lightbox');
    const content = document.getElementById('lightbox-content');
    const closeBtn = document.getElementById('lightbox-close');
    const prevBtn = document.getElementById('lightbox-prev');
    const nextBtn = document.getElementById('lightbox-next');
    if (!lightbox || !content) {return;}

    const singleItems = Array.from(document.querySelectorAll('.gallery-item-single'));
    let lightboxImages = [];
    let currentIdx = 0;

    function buildImageList() {
      lightboxImages = singleItems
        .filter(item => !item.classList.contains('hidden'))
        .map(item => {
          const img = item.querySelector('img');
          return { src: img.src, alt: img.alt };
        });
    }

    function openAt(idx) {
      buildImageList();
      currentIdx = clamp(idx, 0, lightboxImages.length - 1);
      showCurrent();
      lightbox.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      closeBtn && closeBtn.focus();
    }

    function showCurrent() {
      if (!lightboxImages.length) {return;}
      const { src, alt } = lightboxImages[currentIdx];
      content.innerHTML = '';
      const img = document.createElement('img');
      img.src = src;
      img.alt = alt;
      content.appendChild(img);
    }

    function closeLightbox() {
      lightbox.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }

    singleItems.forEach((item) => {
      item.addEventListener('click', () => {
        buildImageList();
        const activeItems = singleItems.filter(el => !el.classList.contains('hidden'));
        const activeIdx = activeItems.indexOf(item);
        openAt(activeIdx >= 0 ? activeIdx : 0);
        safeGtag('event', 'click', { event_category: 'Gallery', event_label: item.querySelector('img').alt });
      });
    });

    closeBtn && closeBtn.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', e => { if (e.target === lightbox) {closeLightbox();} });

    prevBtn && prevBtn.addEventListener('click', () => { currentIdx = (currentIdx - 1 + lightboxImages.length) % lightboxImages.length; showCurrent(); });
    nextBtn && nextBtn.addEventListener('click', () => { currentIdx = (currentIdx + 1) % lightboxImages.length; showCurrent(); });

    document.addEventListener('keydown', e => {
      if (lightbox.getAttribute('aria-hidden') === 'false') {
        if (e.key === 'Escape')      {closeLightbox();}
        if (e.key === 'ArrowLeft')   { currentIdx = (currentIdx - 1 + lightboxImages.length) % lightboxImages.length; showCurrent(); }
        if (e.key === 'ArrowRight')  { currentIdx = (currentIdx + 1) % lightboxImages.length; showCurrent(); }
      }
    });
  }

  /* ================================================================
     CONTACT FORM (Formspree)
     ================================================================ */
  function initContactForm() {
    const form = document.getElementById('contact-form');
    const feedback = document.getElementById('form-message');
    if (!form || !feedback) {return;}

    form.addEventListener('submit', async e => {
      e.preventDefault();

      const name = form.querySelector('#name').value.trim();
      const email = form.querySelector('#email').value.trim();
      const message = form.querySelector('#message').value.trim();
      const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      feedback.className = 'form-feedback';

      if (!name || !emailRe.test(email) || !message) {
        feedback.textContent = 'Please fill in all required fields correctly.';
        feedback.classList.add('error');
        return;
      }

      const submitBtn = form.querySelector('button[type="submit"]');
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending…';
      feedback.textContent = '';

      const data = {};
      new FormData(form).forEach((val, key) => { data[key] = val; });

      try {
        const res = await fetch('https://formspree.io/f/pleasureislanddesign@gmail.com', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify(data)
        });

        if (res.ok) {
          feedback.textContent = "Thank you! We'll be in touch within 1-2 business days.";
          feedback.classList.add('success');
          form.reset();
          safeGtag('event', 'form_submit', { event_category: 'Contact', event_label: 'Contact Form' });
        } else {
          throw new Error('server error');
        }
      } catch {
        feedback.textContent = 'Something went wrong. Please call (910) 444-1230 or email pleasureislanddesign@gmail.com.';
        feedback.classList.add('error');
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send Message';
      }
    });
  }

  /* ================================================================
     NEWSLETTER FORM (Formspree)
     ================================================================ */
  function initNewsletterForm() {
    const form = document.getElementById('newsletter-form');
    const msg = document.getElementById('newsletter-message');
    if (!form || !msg) {return;}

    form.addEventListener('submit', async e => {
      e.preventDefault();
      const emailInput = form.querySelector('#newsletter-email');
      const email = emailInput.value.trim();
      const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      if (!emailRe.test(email)) {
        msg.textContent = 'Please enter a valid email address.';
        return;
      }

      const submitBtn = form.querySelector('button[type="submit"]');
      submitBtn.disabled = true;
      msg.textContent = 'Subscribing…';

      try {
        const res = await fetch('https://formspree.io/f/pleasureislanddesign@gmail.com', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ email, _subject: 'Newsletter Signup' })
        });

        if (res.ok) {
          msg.textContent = 'You\'re subscribed! Welcome to the community.';
          form.reset();
          safeGtag('event', 'form_submit', { event_category: 'Newsletter', event_label: 'Newsletter Signup' });
        } else {
          throw new Error('server error');
        }
      } catch {
        msg.textContent = 'Something went wrong. Please try again.';
      } finally {
        submitBtn.disabled = false;
      }
    });
  }

  /* ================================================================
     SCROLL TO TOP
     ================================================================ */
  function initScrollTop() {
    const btn = document.getElementById('scroll-top');
    if (!btn) {return;}

    window.addEventListener('scroll', () => {
      const show = window.scrollY > 500;
      if (show) {
        btn.removeAttribute('hidden');
      } else {
        btn.setAttribute('hidden', '');
      }
    }, { passive: true });

    btn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ================================================================
     COPYRIGHT YEAR
     ================================================================ */
  function initCopyrightYear() {
    const el = document.getElementById('copyright-year');
    if (el) {el.textContent = new Date().getFullYear();}
  }

  /* ================================================================
     CTA CLICK TRACKING
     ================================================================ */
  function initCTATracking() {
    document.querySelectorAll('[data-track]').forEach(el => {
      el.addEventListener('click', () => {
        safeGtag('event', 'click', {
          event_category: 'CTA',
          event_label: el.dataset.track
        });
      });
    });
  }

  /* ================================================================
     SCROLL DEPTH TRACKING
     ================================================================ */
  function initScrollTracking() {
    const milestones = {};
    let timer;

    window.addEventListener('scroll', () => {
      clearTimeout(timer);
      timer = setTimeout(() => {
        const scrollable = document.body.scrollHeight - window.innerHeight;
        if (scrollable <= 0) {return;}
        const depth = Math.round((window.scrollY / scrollable) * 100);
        [25, 50, 75, 100].forEach(m => {
          if (depth >= m && !milestones[m]) {
            milestones[m] = true;
            safeGtag('event', 'scroll', {
              event_category: 'Page Interaction',
              event_label: `Scroll Depth ${m}%`,
              value: m
            });
          }
        });
      }, 200);
    }, { passive: true });
  }

  /* ================================================================
     BOOT
     ================================================================ */
  function boot() {
    initHeader();
    initHamburger();
    initHero();
    initStatCounters();
    initReveal();
    initProcessSteps();
    initGalleryFilter();
    initBeforeAfterSliders();
    initCarousel();
    initLightbox();
    initContactForm();
    initNewsletterForm();
    initScrollTop();
    initMobileStickyBar();
    initCopyrightYear();
    initCTATracking();
    initScrollTracking();
  }

  /* ================================================================
     PROCESS STEPS: staggered reveal via CSS custom property delay
     ================================================================ */
  function initProcessSteps() {
    const steps = document.querySelectorAll('.process-step');
    if (!steps.length) {return;}

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) {return;}
        const delay = entry.target.style.getPropertyValue('--step-delay') || '0ms';
        setTimeout(() => {
          entry.target.classList.add('visible');
        }, parseInt(delay, 10));
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });

    steps.forEach(step => observer.observe(step));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

})();
