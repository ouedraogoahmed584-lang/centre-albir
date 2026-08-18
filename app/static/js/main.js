// ══════════════════════════════════════════════════════════════
// main.js — Centre Al-Bir — JavaScript Global Responsive
// Gère : thèmes, navbar, mobile menu, admin sidebar,
//        boutons flottants, scroll, réseau, animations
// ══════════════════════════════════════════════════════════════

'use strict';

/* ══════════════════════════════════════════════════════════
   THÈMES PREMIUM
══════════════════════════════════════════════════════════ */
const THEMES  = ['classic','dark','gold','emerald','midnight'];
const THEME_KEY = 'albir-theme';

function setTheme(theme) {
  if (!THEMES.includes(theme)) theme = 'classic';
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem(THEME_KEY, theme);

  // Mettre à jour les boutons du panel
  document.querySelectorAll('.theme-option').forEach(function(opt) {
    opt.classList.toggle('active', opt.id === 'opt-' + theme);
  });

  // Meta theme-color
  var colors = {
    classic:'#064E3B', dark:'#111111',
    gold:'#1A1409', emerald:'#059669', midnight:'#0A0E1A'
  };
  var meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.content = colors[theme] || '#064E3B';
}

function loadSavedTheme() {
  var saved = localStorage.getItem(THEME_KEY) || 'classic';
  setTheme(saved);
}

function toggleThemePanel() {
  var panel = document.getElementById('theme-panel');
  if (panel) panel.classList.toggle('open');
}

// Fermer panel thème si clic extérieur
document.addEventListener('click', function(e) {
  var panel = document.getElementById('theme-panel');
  if (panel && panel.classList.contains('open') && !panel.contains(e.target)) {
    panel.classList.remove('open');
  }
});


/* ══════════════════════════════════════════════════════════
   NAVBAR SCROLL
══════════════════════════════════════════════════════════ */
function initNavbar() {
  var navbar = document.getElementById('navbar');
  if (!navbar) return;

  function updateNavbar() {
    if (window.scrollY > 60) {
      navbar.style.boxShadow = '0 4px 30px rgba(0,0,0,0.25)';
      navbar.style.borderBottom = '1px solid rgba(200,155,60,0.15)';
    } else {
      navbar.style.boxShadow = 'none';
      navbar.style.borderBottom = '1px solid rgba(255,255,255,0.08)';
    }
  }

  window.addEventListener('scroll', updateNavbar, { passive: true });
  updateNavbar();
}


/* ══════════════════════════════════════════════════════════
   MENU MOBILE
══════════════════════════════════════════════════════════ */
function toggleMobile() {
  var menu   = document.getElementById('mobile-menu');
  var icon   = document.getElementById('burger-icon');
  if (!menu) return;

  var isOpen = menu.classList.contains('open');

  if (isOpen) {
    menu.classList.remove('open');
    menu.style.maxHeight = '0px';
    document.body.style.overflow = '';
    if (icon) icon.innerHTML =
      '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>';
  } else {
    menu.classList.add('open');
    menu.style.maxHeight = '100vh';
    document.body.style.overflow = 'hidden';
    if (icon) icon.innerHTML =
      '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>';
  }
}

// Fermer menu mobile sur resize desktop
window.addEventListener('resize', function() {
  if (window.innerWidth >= 1024) {
    var menu = document.getElementById('mobile-menu');
    var icon = document.getElementById('burger-icon');
    if (menu) {
      menu.classList.remove('open');
      menu.style.maxHeight = '0px';
    }
    document.body.style.overflow = '';
    if (icon) icon.innerHTML =
      '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>';
  }
}, { passive: true });


/* ══════════════════════════════════════════════════════════
   DROPDOWN NAVBAR ESPACE
══════════════════════════════════════════════════════════ */
function toggleNavEspace() {
  var dd = document.getElementById('nav-espace-dd');
  if (dd) dd.style.display = (dd.style.display === 'block') ? 'none' : 'block';
}

document.addEventListener('click', function(e) {
  var container = document.getElementById('nav-espace');
  var dd = document.getElementById('nav-espace-dd');
  if (dd && container && !container.contains(e.target)) {
    dd.style.display = 'none';
  }
});


/* ══════════════════════════════════════════════════════════
   DROPDOWN FLOTTANT ESPACE
══════════════════════════════════════════════════════════ */
function toggleFloatEspace() {
  var m = document.getElementById('float-espace-menu');
  if (m) m.style.display = (m.style.display === 'block') ? 'none' : 'block';
}

document.addEventListener('click', function(e) {
  var fe = document.getElementById('float-espace');
  var fm = document.getElementById('float-espace-menu');
  if (fm && fe && !fe.contains(e.target)) fm.style.display = 'none';
});


/* ══════════════════════════════════════════════════════════
   ADMIN SIDEBAR MOBILE
══════════════════════════════════════════════════════════ */
function toggleAdminSidebar() {
  var sidebar  = document.querySelector('.admin-sidebar');
  var overlay  = document.getElementById('admin-overlay');

  if (!sidebar) return;

  var isOpen = sidebar.classList.contains('mobile-open');

  if (isOpen) {
    sidebar.classList.remove('mobile-open');
    if (overlay) overlay.classList.remove('active');
    document.body.style.overflow = '';
  } else {
    sidebar.classList.add('mobile-open');
    if (overlay) overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

// Fermer sidebar admin sur resize desktop
window.addEventListener('resize', function() {
  if (window.innerWidth >= 1024) {
    var sidebar = document.querySelector('.admin-sidebar');
    var overlay = document.getElementById('admin-overlay');
    if (sidebar) sidebar.classList.remove('mobile-open');
    if (overlay) overlay.classList.remove('active');
    document.body.style.overflow = '';
  }
}, { passive: true });


/* ══════════════════════════════════════════════════════════
   SCROLL TOP BUTTON
══════════════════════════════════════════════════════════ */
function initScrollTop() {
  var btn = document.getElementById('btn-scroll-top');
  if (!btn) return;

  window.addEventListener('scroll', function() {
    if (window.scrollY > 400) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  }, { passive: true });
}


/* ══════════════════════════════════════════════════════════
   LOADER DE PAGE
══════════════════════════════════════════════════════════ */
function initLoader() {
  var loader = document.getElementById('page-loader');
  if (!loader) return;

  function hide() {
    loader.style.opacity    = '0';
    loader.style.visibility = 'hidden';
    loader.style.transition = 'opacity 0.5s ease, visibility 0.5s ease';
    setTimeout(function() { loader.style.display = 'none'; }, 500);
  }

  if (document.readyState === 'complete') {
    setTimeout(hide, 400);
  } else {
    window.addEventListener('load', function() { setTimeout(hide, 400); });
  }

  // Fallback
  setTimeout(hide, 3000);
}


/* ══════════════════════════════════════════════════════════
   FLASH MESSAGES AUTO-CLOSE
══════════════════════════════════════════════════════════ */
function initFlashMessages() {
  var container = document.getElementById('flash-container');
  if (!container) return;

  setTimeout(function() {
    container.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    container.style.opacity    = '0';
    container.style.transform  = 'translateX(20px)';
    setTimeout(function() {
      if (container.parentNode) container.parentNode.removeChild(container);
    }, 500);
  }, 6000);
}


/* ══════════════════════════════════════════════════════════
   RÉSEAU HORS-LIGNE
══════════════════════════════════════════════════════════ */
function initNetworkStatus() {
  var banner = null;

  function createBanner() {
    if (banner) return;
    banner = document.createElement('div');
    banner.textContent = '📡 Connexion perdue';
    Object.assign(banner.style, {
      position: 'fixed', bottom: '5.5rem',
      left: '50%', transform: 'translateX(-50%)',
      background: '#1F2937', color: '#fff',
      padding: '0.625rem 1.25rem',
      borderRadius: '999px', fontSize: '0.8125rem',
      fontWeight: '700', zIndex: '99999',
      display: 'none', whiteSpace: 'nowrap',
      boxShadow: '0 8px 30px rgba(0,0,0,0.3)',
      maxWidth: 'calc(100vw - 2rem)',
    });
    document.body.appendChild(banner);
  }

  window.addEventListener('offline', function() {
    createBanner();
    if (banner) banner.style.display = 'block';
  });

  window.addEventListener('online', function() {
    if (banner) {
      banner.textContent     = '✅ Reconnecté !';
      banner.style.background = '#059669';
      setTimeout(function() {
        if (banner) banner.style.display = 'none';
      }, 2500);
    }
  });
}


/* ══════════════════════════════════════════════════════════
   SMOOTH SCROLL
══════════════════════════════════════════════════════════ */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
      var id = this.getAttribute('href');
      if (!id || id === '#') return;
      var el = document.querySelector(id);
      if (!el) return;
      e.preventDefault();
      var nav    = document.getElementById('navbar');
      var offset = nav ? nav.offsetHeight + 16 : 80;
      window.scrollTo({
        top: el.getBoundingClientRect().top + window.pageYOffset - offset,
        behavior: 'smooth'
      });
    });
  });
}


/* ══════════════════════════════════════════════════════════
   TOAST NOTIFICATION
══════════════════════════════════════════════════════════ */
function showToast(message, type) {
  type = type || 'success';
  var colors = {
    success: '#059669', error: '#DC2626',
    info: '#2563EB', warning: '#D97706'
  };
  var toast = document.createElement('div');
  Object.assign(toast.style, {
    position: 'fixed', bottom: '5rem',
    left: '50%', transform: 'translateX(-50%) translateY(8px)',
    background: colors[type] || colors.success,
    color: '#fff', padding: '0.75rem 1.5rem',
    borderRadius: '999px', fontSize: '0.875rem',
    fontWeight: '700', zIndex: '99999',
    boxShadow: '0 8px 30px rgba(0,0,0,0.25)',
    whiteSpace: 'nowrap', opacity: '0',
    transition: 'all 0.3s ease',
    maxWidth: 'calc(100vw - 2rem)',
  });
  toast.textContent = message;
  document.body.appendChild(toast);

  requestAnimationFrame(function() {
    toast.style.opacity   = '1';
    toast.style.transform = 'translateX(-50%) translateY(0)';
  });

  setTimeout(function() {
    toast.style.opacity   = '0';
    toast.style.transform = 'translateX(-50%) translateY(8px)';
    setTimeout(function() {
      if (toast.parentNode) toast.parentNode.removeChild(toast);
    }, 300);
  }, 3500);
}


/* ══════════════════════════════════════════════════════════
   COPY TO CLIPBOARD
══════════════════════════════════════════════════════════ */
function initCopyButtons() {
  document.querySelectorAll('[data-copy]').forEach(function(el) {
    el.style.cursor = 'pointer';
    el.addEventListener('click', function() {
      var text = this.dataset.copy;
      if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function() {
          showToast('✅ Copié !');
        }).catch(function() {
          fallbackCopy(text);
        });
      } else {
        fallbackCopy(text);
      }
    });
  });
}

function fallbackCopy(text) {
  var input = document.createElement('input');
  input.value = text;
  document.body.appendChild(input);
  input.select();
  try { document.execCommand('copy'); showToast('✅ Copié !'); } catch(e) {}
  input.remove();
}


/* ══════════════════════════════════════════════════════════
   RESPONSIVE DETECTION
══════════════════════════════════════════════════════════ */
function updateBreakpoint() {
  var w  = window.innerWidth;
  var bp = w < 640 ? 'xs' : w < 768 ? 'sm' : w < 1024 ? 'md' : w < 1280 ? 'lg' : 'xl';
  var body = document.body;
  ['xs','sm','md','lg','xl'].forEach(function(c) { body.classList.remove('bp-'+c); });
  body.classList.add('bp-'+bp);

  // Appliquer display:flex sur nav desktop si lg+
  var navDesktop = document.querySelector('.nav-desktop');
  if (navDesktop) {
    navDesktop.style.display = w >= 1024 ? 'flex' : 'none';
  }

  // Bouton S'inscrire navbar
  var navCta = document.querySelector('.nav-cta-btn');
  if (navCta) {
    navCta.style.display = w >= 640 ? 'inline-flex' : 'none';
  }

  // Burger visible sous lg
  var burger = document.querySelector('.nav-burger');
  if (burger) {
    burger.style.display = w >= 1024 ? 'none' : 'flex';
  }
}


/* ══════════════════════════════════════════════════════════
   INIT GLOBAL
══════════════════════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', function() {
  loadSavedTheme();
  initLoader();
  initNavbar();
  initScrollTop();
  initFlashMessages();
  initNetworkStatus();
  initSmoothScroll();
  initCopyButtons();
  updateBreakpoint();

  window.addEventListener('resize', updateBreakpoint, { passive: true });
});