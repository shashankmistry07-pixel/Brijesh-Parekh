/* ==========================================================================
   Brijesh Parekh - Official Professional Singer Interactive Scripts
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initAudioPlayer();
  initGallery();
  initAjaxForm();
});

/* Navbar scroll and mobile toggle */
function initNavbar() {
  const header = document.querySelector('header.navbar-header');
  const toggle = document.querySelector('.mobile-toggle');
  const navLinks = document.querySelector('.nav-links');

  if (header) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 50) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    });
  }

  if (toggle && navLinks) {
    toggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      const icon = toggle.querySelector('i');
      if (icon) {
        if (navLinks.classList.contains('open')) {
          icon.className = 'fa-solid fa-xmark';
        } else {
          icon.className = 'fa-solid fa-bars';
        }
      }
    });
  }
}

/* Persistent Sticky Audio Player Logic */
function initAudioPlayer() {
  const audio = new Audio();
  const mainPlayBtn = document.getElementById('mainPlayBtn');
  const mainPlayIcon = mainPlayBtn ? mainPlayBtn.querySelector('i') : null;
  const nowPlayingTitle = document.getElementById('nowPlayingTitle');
  const nowPlayingSub = document.getElementById('nowPlayingSub');
  const nowPlayingCover = document.getElementById('nowPlayingCover');
  const progressBar = document.getElementById('playerProgressBar');
  const progressFill = document.getElementById('playerProgressFill');
  const currentTimeEl = document.getElementById('currentTime');
  const totalTimeEl = document.getElementById('totalTime');

  let currentTrackUrl = "";

  // Attach click to track play buttons across the app
  const trackPlayBtns = document.querySelectorAll('.play-track-btn, .btn-play-trigger');
  
  trackPlayBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const url = btn.getAttribute('data-audio');
      const title = btn.getAttribute('data-title') || 'Song Track';
      const sub = btn.getAttribute('data-sub') || 'Brijesh Parekh';
      const cover = btn.getAttribute('data-cover') || '/static/pics/solo3.jpg';

      if (currentTrackUrl === url && !audio.paused) {
        audio.pause();
        updatePlayIcons(false);
      } else if (currentTrackUrl === url && audio.paused) {
        audio.play();
        updatePlayIcons(true);
      } else {
        currentTrackUrl = url;
        audio.src = url;
        if (nowPlayingTitle) nowPlayingTitle.textContent = title;
        if (nowPlayingSub) nowPlayingSub.textContent = sub;
        if (nowPlayingCover) nowPlayingCover.src = cover;
        
        audio.play();
        updatePlayIcons(true);
      }
    });
  });

  if (mainPlayBtn) {
    mainPlayBtn.addEventListener('click', () => {
      if (!currentTrackUrl) {
        // Pick first available track
        const firstBtn = document.querySelector('.play-track-btn');
        if (firstBtn) firstBtn.click();
        return;
      }
      if (audio.paused) {
        audio.play();
        updatePlayIcons(true);
      } else {
        audio.pause();
        updatePlayIcons(false);
      }
    });
  }

  // Time & Progress Updates
  audio.addEventListener('timeupdate', () => {
    if (!isNaN(audio.duration) && audio.duration > 0) {
      const pct = (audio.currentTime / audio.duration) * 100;
      if (progressFill) progressFill.style.width = pct + '%';
      if (currentTimeEl) currentTimeEl.textContent = formatTime(audio.currentTime);
      if (totalTimeEl) totalTimeEl.textContent = formatTime(audio.duration);
    }
  });

  audio.addEventListener('ended', () => {
    updatePlayIcons(false);
    if (progressFill) progressFill.style.width = '0%';
  });

  if (progressBar) {
    progressBar.addEventListener('click', (e) => {
      const rect = progressBar.getBoundingClientRect();
      const pos = (e.clientX - rect.left) / rect.width;
      if (!isNaN(audio.duration)) {
        audio.currentTime = pos * audio.duration;
      }
    });
  }

  function updatePlayIcons(isPlaying) {
    if (mainPlayIcon) {
      mainPlayIcon.className = isPlaying ? 'fa-solid fa-pause' : 'fa-solid fa-play';
    }
  }

  function formatTime(secs) {
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  }
}

/* Lightbox & Gallery Filter */
function initGallery() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const galleryItems = document.querySelectorAll('.gallery-card');
  const lightbox = document.getElementById('lightboxModal');
  const lightboxImg = document.getElementById('lightboxImg');
  const lightboxClose = document.getElementById('lightboxClose');

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

  // Lightbox click
  document.querySelectorAll('.gallery-card, .lightbox-trigger').forEach(card => {
    card.addEventListener('click', () => {
      const imgSrc = card.getAttribute('data-img') || card.querySelector('img')?.src;
      if (imgSrc && lightbox && lightboxImg) {
        lightboxImg.src = imgSrc;
        lightbox.classList.add('active');
      }
    });
  });

  if (lightboxClose && lightbox) {
    lightboxClose.addEventListener('click', () => {
      lightbox.classList.remove('active');
    });
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) {
        lightbox.classList.remove('active');
      }
    });
  }
}

/* AJAX Form Submit */
function initAjaxForm() {
  const form = document.getElementById('bookingInquiryForm');
  const toastContainer = document.getElementById('formToastContainer');

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const formData = new FormData(form);
      const submitBtn = form.querySelector('button[type="submit"]');
      const originalText = submitBtn ? submitBtn.innerHTML : 'Send Inquiry';

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
      .catch(err => {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalText;
        }
        if (toastContainer) {
          toastContainer.innerHTML = `
            <div class="alert-toast error">
              <i class="fa-solid fa-triangle-exclamation"></i>
              <span>Something went wrong. Please check your internet connection or try again.</span>
            </div>
          `;
        }
      });
    });
  }
}
