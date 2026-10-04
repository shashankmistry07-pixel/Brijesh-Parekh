/* ==========================================================================
   Brijesh Parekh - Official Professional Singer Web Application Scripts
   Optimized for High Performance & Smooth User Experience
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initBackToTop();
  initGalleryLightbox();
  initAjaxBookingForm();
});

/* Navbar scroll performance & Mobile Drawer Toggle */
function initNavbar() {
  const header = document.getElementById('mainHeader');
  const toggle = document.getElementById('mobileToggle');
  const navLinks = document.getElementById('navMenu');

  if (header) {
    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          if (window.scrollY > 40) {
            header.classList.add('scrolled');
          } else {
            header.classList.remove('scrolled');
          }
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  }

  if (toggle && navLinks) {
    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = navLinks.classList.toggle('open');
      const icon = toggle.querySelector('i');
      if (icon) {
        icon.className = isOpen ? 'fa-solid fa-xmark' : 'fa-solid fa-bars';
      }
      toggle.setAttribute('aria-expanded', isOpen);
    });

    // Close mobile menu on link click
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        const icon = toggle.querySelector('i');
        if (icon) icon.className = 'fa-solid fa-bars';
      });
    });

    // Close on click outside
    document.addEventListener('click', (e) => {
      if (navLinks.classList.contains('open') && !navLinks.contains(e.target) && !toggle.contains(e.target)) {
        navLinks.classList.remove('open');
        const icon = toggle.querySelector('i');
        if (icon) icon.className = 'fa-solid fa-bars';
      }
    });
  }
}

/* Floating Back to Top Button */
function initBackToTop() {
  const backToTopBtn = document.getElementById('backToTopBtn');
  if (!backToTopBtn) return;

  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        if (window.scrollY > 350) {
          backToTopBtn.classList.add('visible');
        } else {
          backToTopBtn.classList.remove('visible');
        }
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });

  backToTopBtn.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
}

/* Lightbox Modal & Keyboard Navigation */
function initGalleryLightbox() {
  const filterBtns = document.querySelectorAll('.filter-btn[data-filter]');
  const galleryItems = document.querySelectorAll('.gallery-card');
  const lightbox = document.getElementById('lightboxModal');
  const lightboxImg = document.getElementById('lightboxImg');
  const lightboxClose = document.getElementById('lightboxClose');

  // Client-side category filtering if data-filter exists
  if (filterBtns.length > 0) {
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const cat = btn.getAttribute('data-filter');
        galleryItems.forEach(item => {
          if (cat === 'all' || item.getAttribute('data-category') === cat) {
            item.style.display = 'block';
          } else {
            item.style.display = 'none';
          }
        });
      });
    });
  }

  // Open Lightbox
  document.querySelectorAll('.gallery-card[data-img], .lightbox-trigger').forEach(card => {
    card.addEventListener('click', () => {
      const imgSrc = card.getAttribute('data-img') || card.querySelector('img')?.src;
      if (imgSrc && lightbox && lightboxImg) {
        lightboxImg.src = imgSrc;
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
    });
  });

  // Close Lightbox function
  function closeLightbox() {
    if (lightbox) {
      lightbox.classList.remove('active');
      document.body.style.overflow = '';
    }
  }

  if (lightboxClose) {
    lightboxClose.addEventListener('click', closeLightbox);
  }

  if (lightbox) {
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) {
        closeLightbox();
      }
    });
  }

  // Close on Escape Key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && lightbox && lightbox.classList.contains('active')) {
      closeLightbox();
    }
  });
}

/* Asynchronous AJAX Form Submission */
function initAjaxBookingForm() {
  const form = document.getElementById('bookingInquiryForm');
  const toastContainer = document.getElementById('formToastContainer');

  if (form) {
    form.addEventListener('submit', (e) => {
      // If form doesn't have an action to standard POST, handle via AJAX
      if (!form.hasAttribute('action') || form.getAttribute('action') === '') {
        e.preventDefault();
        const formData = new FormData(form);
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn ? submitBtn.innerHTML : 'Submit Inquiry';

        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Submitting...';
        }

        fetch('/api/inquiry/', {
          method: 'POST',
          body: formData,
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        })
        .then(res => res.json())
        .then(data => {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
          }

          if (toastContainer) {
            if (data.success) {
              toastContainer.innerHTML = `
                <div class="alert-toast success">
                  <i class="fa-solid fa-circle-check"></i>
                  <span>${data.message}</span>
                </div>
              `;
              form.reset();
              toastContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
              toastContainer.innerHTML = `
                <div class="alert-toast error">
                  <i class="fa-solid fa-triangle-exclamation"></i>
                  <span>${data.message}</span>
                </div>
              `;
            }
          }
        })
        .catch(() => {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
          }
          if (toastContainer) {
            toastContainer.innerHTML = `
              <div class="alert-toast error">
                <i class="fa-solid fa-triangle-exclamation"></i>
                <span>Something went wrong. Please check your connection or call directly.</span>
              </div>
            `;
          }
        });
      }
    });
  }
}
