// ============================================================
// FICHIER #58 — static/js/main.js (VERSION COMPLÈTE)
// JavaScript global du Centre Al-Bir. Gère le système de thèmes
// multi-couleurs avec persistance localStorage, les boutons
// flottants responsives, les animations au scroll, le menu
// mobile, et toutes les interactions premium du site.
// ============================================================

'use strict';

/* ══════════════════════════════════════════════════════════
   SYSTÈME DE THÈMES PREMIUM
══════════════════════════════════════════════════════════ */
const THEMES = ['classic', 'dark', 'gold', 'emerald', 'midnight'];
const THEME_KEY = 'albir-theme';

/**
 * Applique un thème et le sauvegarde en localStorage
 */
function setTheme(theme) {
  if (!THEMES.includes(theme)) theme = 'classic';

  // Appliquer le thème
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem(THEME_KEY, theme);

  // Mettre à jour les boutons du panel
  document.querySelectorAll('.theme-option').forEach(opt => {
    const optTheme = opt.id.replace('opt-', '');
    if (optTheme === theme) {
      opt.classList.add('active');
    } else {
      opt.classList.remove('active');
    }
  });

  // Changer la meta theme-color
  const metaTheme = document.querySelector('meta[name="theme-color"]');
  const colors = {
    classic:  '#064E3B',
    dark:     '#111111',
    gold:     '#1A1409',
    emerald:  '#059669',
    midnight: '#0A0E1A',
  };
  if (metaTheme) metaTheme.content = colors[theme] || colors.classic;
}

/**
 * Charge le thème sauvegardé (ou "classic" par défaut)
 */
function loadSavedTheme() {
  const saved = localStorage.getItem(THEME_KEY) || 'classic';
  setTheme(saved);
}

/**
 * Ouvre/ferme le panneau de thèmes
 */
function toggleThemePanel() {
  const panel = document.getElementById('theme-panel');
  if (panel) panel.classList.toggle('open');
}

// Fermer le panel si on clique ailleurs
document.addEventListener('click', function(e) {
  const panel = document.getElementById('theme-panel');
  if (panel && panel.classList.contains('open')) {
    if (!panel.contains(e.target)) {
      panel.classList.remove('open');
    }
  }
});


/* ══════════════════════════════════════════════════════════
   SCROLL TOP BUTTON
══════════════════════════════════════════════════════════ */
function initScrollTop() {
  const btn = document.getElementById('btn-scroll-top');
  if (!btn) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 400) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  }, { passive: true });
}


/* ══════════════════════════════════════════════════════════
   ESPACE PERSONNEL — DROPDOWN
══════════════════════════════════════════════════════════ */
let espaceOpen = false;

function toggleEspaceMenu() {
  const menu = document.getElementById('espace-menu');
  const btn  = document.getElementById('btn-espace');
  if (!menu) return;

  espaceOpen = !espaceOpen;
  menu.style.display = espaceOpen ? 'block' : 'none';

  // Rotation icône
  if (btn) {
    btn.style.transform = espaceOpen ? 'scale(1.1) rotate(10deg)' : 'scale(1) rotate(0)';
    btn.style.background = espaceOpen
      ? 'linear-gradient(135deg,#C89B3C,#E8C472)'
      : 'var(--gradient-button)';
  }
}

// Fermer si clic extérieur
document.addEventListener('click', function(e) {
  const container = document.getElementById('espace-container');
  if (container && !container.contains(e.target) && espaceOpen) {
    espaceOpen = false;
    const menu = document.getElementById('espace-menu');
    const btn  = document.getElementById('btn-espace');
    if (menu) menu.style.display = 'none';
    if (btn) {
      btn.style.transform = 'scale(1)';
      btn.style.background = '';
    }
  }
});


/* ══════════════════════════════════════════════════════════
   NAVBAR SCROLL EFFECT
══════════════════════════════════════════════════════════ */
function initNavbar() {
  const navbar = document.getElementById('navbar');
  if (!navbar) return;

  let lastScroll = 0;

  window.addEventListener('scroll', () => {
    const currentScroll = window.scrollY;

    if (currentScroll > 60) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }

    lastScroll = currentScroll;
  }, { passive: true });
}


/* ══════════════════════════════════════════════════════════
   MENU MOBILE
══════════════════════════════════════════════════════════ */
function toggleMobile() {
  const menu = document.getElementById('mobile-menu');
  const icon = document.getElementById('burger-icon');
  if (!menu) return;

  const isOpen = menu.classList.toggle('open');

  // Changer l'icône burger → croix
  if (icon) {
    icon.innerHTML = isOpen
      ? '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>'
      : '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>';
  }

  // Bloquer scroll body
  document.body.style.overflow = isOpen ? 'hidden' : '';
}


/* ══════════════════════════════════════════════════════════
   SIDEBAR ADMIN MOBILE
══════════════════════════════════════════════════════════ */
function toggleAdminSidebar() {
  const sidebar = document.querySelector('.admin-sidebar');
  if (sidebar) sidebar.classList.toggle('mobile-open');
}


/* ══════════════════════════════════════════════════════════
   LOADER DE PAGE
══════════════════════════════════════════════════════════ */
function initLoader() {
  const loader = document.getElementById('page-loader');
  if (!loader) return;

  window.addEventListener('load', () => {
    setTimeout(() => {
      loader.classList.add('hidden');
    }, 700);
  });

  // Fallback si load ne se déclenche pas
  setTimeout(() => {
    if (loader && !loader.classList.contains('hidden')) {
      loader.classList.add('hidden');
    }
  }, 3000);
}


/* ══════════════════════════════════════════════════════════
   MESSAGES FLASH AUTO-CLOSE
══════════════════════════════════════════════════════════ */
function initFlashMessages() {
  const container = document.getElementById('flash-container');
  if (!container) return;

  setTimeout(() => {
    container.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    container.style.opacity    = '0';
    container.style.transform  = 'translateX(20px)';
    setTimeout(() => container.remove(), 500);
  }, 6000);
}


/* ══════════════════════════════════════════════════════════
   RÉSEAU HORS-LIGNE
══════════════════════════════════════════════════════════ */
function initNetworkStatus() {
  let banner = null;

  function createBanner() {
    if (banner) return;
    banner = document.createElement('div');
    banner.innerHTML = '📡 Connexion perdue';
    Object.assign(banner.style, {
      position: 'fixed', bottom: '90px', left: '50%',
      transform: 'translateX(-50%)',
      background: '#1F2937', color: 'white',
      padding: '10px 20px', borderRadius: '50px',
      fontSize: '13px', fontWeight: '700',
      zIndex: '99999', display: 'none',
      whiteSpace: 'nowrap',
      boxShadow: '0 8px 30px rgba(0,0,0,0.3)',
    });
    document.body.appendChild(banner);
  }

  window.addEventListener('offline', () => {
    createBanner();
    if (banner) { banner.style.display = 'block'; }
  });

  window.addEventListener('online', () => {
    if (banner) {
      banner.textContent     = '✅ Reconnecté !';
      banner.style.background = '#059669';
      setTimeout(() => { banner.style.display = 'none'; }, 2500);
    }
  });
}


/* ══════════════════════════════════════════════════════════
   SMOOTH SCROLL
══════════════════════════════════════════════════════════ */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const id  = this.getAttribute('href');
      if (id === '#') return;
      const el  = document.querySelector(id);
      if (!el) return;
      e.preventDefault();
      const nav    = document.getElementById('navbar');
      const offset = nav ? nav.offsetHeight + 16 : 80;
      window.scrollTo({
        top: el.getBoundingClientRect().top + window.pageYOffset - offset,
        behavior: 'smooth',
      });
    });
  });
}


/* ══════════════════════════════════════════════════════════
   TOAST NOTIFICATIONS
══════════════════════════════════════════════════════════ */
function showToast(message, type = 'success') {
  const colors = {
    success: '#059669',
    error:   '#DC2626',
    info:    '#2563EB',
    warning: '#D97706',
  };

  const toast = document.createElement('div');
  Object.assign(toast.style, {
    position: 'fixed',
    bottom: '6rem',
    left: '50%',
    transform: 'translateX(-50%) translateY(10px)',
    background: colors[type] || colors.success,
    color: 'white',
    padding: '0.75rem 1.5rem',
    borderRadius: '50px',
    fontSize: '0.875rem',
    fontWeight: '700',
    zIndex: '99999',
    boxShadow: '0 8px 30px rgba(0,0,0,0.25)',
    whiteSpace: 'nowrap',
    transition: 'all 0.3s ease',
  });
  toast.textContent = message;
  document.body.appendChild(toast);

  requestAnimationFrame(() => {
    toast.style.transform = 'translateX(-50%) translateY(0)';
    toast.style.opacity   = '1';
  });

  setTimeout(() => {
    toast.style.opacity   = '0';
    toast.style.transform = 'translateX(-50%) translateY(8px)';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}


/* ══════════════════════════════════════════════════════════
   COPIE PRESSE-PAPIERS
══════════════════════════════════════════════════════════ */
function initCopyButtons() {
  document.querySelectorAll('[data-copy]').forEach(el => {
    el.style.cursor = 'pointer';
    el.addEventListener('click', function() {
      const text = this.dataset.copy;
      navigator.clipboard.writeText(text).then(() => {
        showToast('✅ Copié !', 'success');
      }).catch(() => {
        const input = document.createElement('input');
        input.value = text;
        document.body.appendChild(input);
        input.select();
        document.execCommand('copy');
        input.remove();
        showToast('✅ Copié !', 'success');
      });
    });
  });
}


/* ══════════════════════════════════════════════════════════
   RESPONSIVE — DÉTECTION TAILLE ÉCRAN
══════════════════════════════════════════════════════════ */
function getBreakpoint() {
  const w = window.innerWidth;
  if (w < 640)  return 'xs';
  if (w < 768)  return 'sm';
  if (w < 1024) return 'md';
  if (w < 1280) return 'lg';
  return 'xl';
}

// Ajouter class au body pour ciblage CSS
function updateBreakpoint() {
  const bp = getBreakpoint();
  ['xs','sm','md','lg','xl'].forEach(c => document.body.classList.remove('bp-' + c));
  document.body.classList.add('bp-' + bp);
}


/* ══════════════════════════════════════════════════════════
   INITIALISATION GLOBALE
══════════════════════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', function() {
  // Thème — PREMIER pour éviter le flash
  loadSavedTheme();

  // Initialiser tous les modules
  initLoader();
  initNavbar();
  initScrollTop();
  initFlashMessages();
  initNetworkStatus();
  initSmoothScroll();
  initCopyButtons();
  updateBreakpoint();

  // Resize listener
  window.addEventListener('resize', updateBreakpoint, { passive: true });

  // Fermer menu mobile sur resize
  window.addEventListener('resize', () => {
    if (window.innerWidth >= 1024) {
      const menu = document.getElementById('mobile-menu');
      if (menu) menu.classList.remove('open');
      document.body.style.overflow = '';
    }
  }, { passive: true });
});
/* ============================================================
   FONCTIONS RESPONSIVE AJOUTÉES — CENTRE AL-BIR
   ============================================================ */

// Sidebar admin mobile
function toggleAdminSidebar() {
  var sidebar = document.querySelector('.admin-sidebar');
  var overlay = document.getElementById('admin-overlay');
  if (!sidebar) return;
  var open = sidebar.classList.contains('mobile-open');
  if (open) {
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
    var s = document.querySelector('.admin-sidebar');
    var o = document.getElementById('admin-overlay');
    if (s) s.classList.remove('mobile-open');
    if (o) o.classList.remove('active');
    document.body.style.overflow = '';
  }
}, { passive: true });

/* ============================================================
   FIX FOUC — Spacer dynamique + page-ready
   Calcule la vraie hauteur navbar+bannière
   Révèle les éléments seulement quand tout est prêt
   ============================================================ */

function fixNavSpacer() {
  var spacer  = document.getElementById('nav-spacer');
  var navbar  = document.getElementById('navbar');
  if (!spacer || !navbar) return;

  // Calculer hauteur réelle de la navbar (navbar + bannière intégrée)
  var navH = navbar.offsetHeight;
  spacer.style.height = navH + 'px';
}

function markPageReady() {
  // Révèle tous les éléments cachés anti-FOUC
  document.body.classList.add('page-ready');

  // Corriger le spacer
  fixNavSpacer();

  // Cacher le loader
  var loader = document.getElementById('page-loader');
  if (loader) {
    loader.classList.add('hidden');
  }
}

// Lancer quand DOM + images chargés
window.addEventListener('load', function() {
  // Petit délai pour que Tailwind CDN applique ses styles
  setTimeout(markPageReady, 300);
});

// Fallback de sécurité
setTimeout(markPageReady, 2500);

// Recalculer spacer si resize
window.addEventListener('resize', fixNavSpacer, { passive: true });

// Recalculer spacer si bannière fermée
document.addEventListener('click', function(e) {
  var banner = document.getElementById('enroll-banner');
  if (banner && e.target.closest && e.target.closest('[onclick*="enroll-banner"]')) {
    setTimeout(fixNavSpacer, 50);
  }
});
