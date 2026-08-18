/* ============================================================
   main.js — Centre Al-Bir — Système Thèmes Premium 2026
   Gère : 5 thèmes, détection auto, sauvegarde, navbar,
          mobile menu, admin sidebar, boutons flottants
   ============================================================ */

'use strict';

/* ══════════════════════════════════════════════════════════
   SYSTÈME DE THÈMES PREMIUM
══════════════════════════════════════════════════════════ */

var THEMES = {
  'albir':    { name: '🟢 Al-Bir Institution',    desc: 'Vert islamique officiel' },
  'dark':     { name: '🌑 Dark Emerald Luxury',   desc: 'Sombre premium' },
  'academic': { name: '🔵 Academic Blue',          desc: 'Université internationale' },
  'royal':    { name: '🟡 Gold Royal Prestige',   desc: 'Cérémonies & prestige' },
  'future':   { name: '🟣 Future AI Education',   desc: 'Innovation 2026' },
};

var THEME_KEY  = 'albir-theme';
var THEME_META = '#064E3B';

var THEME_META_COLORS = {
  'albir':    '#064E3B',
  'dark':     '#071A16',
  'academic': '#0F172A',
  'royal':    '#4A2C16',
  'future':   '#060B14',
};

/**
 * Applique un thème — met à jour html[data-theme]
 * Sauvegarde dans localStorage
 */
function setTheme(theme, save) {
  if (typeof save === 'undefined') save = true;
  if (!THEMES[theme]) theme = 'albir';

  // Appliquer
  document.documentElement.setAttribute('data-theme', theme);

  // Sauvegarder
  if (save) localStorage.setItem(THEME_KEY, theme);

  // Meta theme-color (barre mobile)
  var meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.content = THEME_META_COLORS[theme] || '#064E3B';

  // Mettre à jour les boutons du panel
  document.querySelectorAll('.theme-option').forEach(function(btn) {
    btn.classList.toggle('active', btn.dataset.theme === theme);
  });

  // Sauvegarder en BDD si connecté (optionnel - silencieux)
  if (save) {
    fetch('/api/theme/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ theme: theme }),
    }).catch(function() {}); // Silencieux si erreur
  }
}

/**
 * Charge le thème sauvegardé ou détecte le système
 */
function loadTheme() {
  var saved = localStorage.getItem(THEME_KEY);

  if (saved && THEMES[saved]) {
    setTheme(saved, false);
    return;
  }

  // Détection automatique préférence système
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    setTheme('dark', false);
  } else {
    setTheme('albir', false);
  }
}

// Écouter changement préférence système
if (window.matchMedia) {
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
    var saved = localStorage.getItem(THEME_KEY);
    // Changer auto seulement si pas de préférence sauvegardée
    if (!saved) {
      setTheme(e.matches ? 'dark' : 'albir', false);
    }
  });
}

/**
 * Ouvre / ferme le panneau de thèmes
 */
function toggleThemeSwitcher() {
  var panel = document.getElementById('theme-switcher-panel');
  if (panel) panel.classList.toggle('open');
}

// Fermer si clic extérieur
document.addEventListener('click', function(e) {
  var panel = document.getElementById('theme-switcher-panel');
  if (panel && panel.classList.contains('open') && !panel.contains(e.target)) {
    panel.classList.remove('open');
  }
});

/* ══════════════════════════════════════════════════════════
   NAVBAR
══════════════════════════════════════════════════════════ */
function initNavbar() {
  var nav = document.getElementById('navbar');
  if (!nav) return;
  window.addEventListener('scroll', function() {
    nav.classList.toggle('scrolled', window.scrollY > 60);
  }, { passive: true });
}

/* ══════════════════════════════════════════════════════════
   MENU MOBILE
══════════════════════════════════════════════════════════ */
function toggleMobile() {
  var menu = document.getElementById('mobile-menu');
  var icon = document.getElementById('burger-icon');
  if (!menu) return;
  var open = menu.classList.contains('open');
  if (open) {
    menu.classList.remove('open');
    menu.style.maxHeight = '0px';
    document.body.style.overflow = '';
    if (icon) icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>';
  } else {
    menu.classList.add('open');
    menu.style.maxHeight = '100vh';
    document.body.style.overflow = 'hidden';
    if (icon) icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>';
  }
}
window.addEventListener('resize', function() {
  if (window.innerWidth >= 1024) {
    var menu = document.getElementById('mobile-menu');
    if (menu) { menu.classList.remove('open'); menu.style.maxHeight = '0px'; }
    document.body.style.overflow = '';
  }
}, { passive: true });

/* ══════════════════════════════════════════════════════════
   DROPDOWN ESPACE (navbar + flottant)
══════════════════════════════════════════════════════════ */
function toggleNavEspace() {
  var dd = document.getElementById('nav-espace-dd');
  if (dd) dd.style.display = (dd.style.display === 'block') ? 'none' : 'block';
}
document.addEventListener('click', function(e) {
  var c = document.getElementById('nav-espace');
  var d = document.getElementById('nav-espace-dd');
  if (d && c && !c.contains(e.target)) d.style.display = 'none';
});

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
  var s = document.getElementById('admin-sidebar');
  var o = document.getElementById('admin-overlay');
  if (!s) return;
  var open = s.classList.contains('mobile-open');
  if (open) {
    s.classList.remove('mobile-open');
    if (o) o.classList.remove('active');
    document.body.style.overflow = '';
  } else {
    s.classList.add('mobile-open');
    if (o) o.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}
function closeAdminSidebar() {
  var s = document.getElementById('admin-sidebar');
  var o = document.getElementById('admin-overlay');
  if (s) s.classList.remove('mobile-open');
  if (o) o.classList.remove('active');
  document.body.style.overflow = '';
}
window.addEventListener('resize', function() {
  if (window.innerWidth >= 1024) closeAdminSidebar();
}, { passive: true });

/* ══════════════════════════════════════════════════════════
   SCROLL TOP
══════════════════════════════════════════════════════════ */
function initScrollTop() {
  var btn = document.getElementById('btn-scroll-top');
  if (!btn) return;
  window.addEventListener('scroll', function() {
    btn.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });
}

/* ══════════════════════════════════════════════════════════
   LOADER
══════════════════════════════════════════════════════════ */
function initLoader() {
  var loader = document.getElementById('page-loader');
  if (!loader) return;
  function hide() { loader.classList.add('hidden'); }
  if (document.readyState === 'complete') { setTimeout(hide, 250); }
  else { window.addEventListener('load', function() { setTimeout(hide, 250); }); }
  setTimeout(hide, 4000);
}

/* ══════════════════════════════════════════════════════════
   FLASH AUTO-CLOSE
══════════════════════════════════════════════════════════ */
function initFlashMessages() {
  var c = document.getElementById('flash-container');
  if (!c) return;
  setTimeout(function() {
    c.style.transition = 'opacity 0.5s ease';
    c.style.opacity = '0';
    setTimeout(function() { if (c.parentNode) c.parentNode.removeChild(c); }, 500);
  }, 6000);
}

/* ══════════════════════════════════════════════════════════
   RÉSEAU
══════════════════════════════════════════════════════════ */
function initNetwork() {
  var banner = null;
  window.addEventListener('offline', function() {
    if (!banner) {
      banner = document.createElement('div');
      banner.textContent = '📡 Connexion perdue';
      Object.assign(banner.style, {
        position:'fixed', bottom:'5.5rem', left:'50%',
        transform:'translateX(-50%)',
        background:'#1F2937', color:'#fff', padding:'0.625rem 1.25rem',
        borderRadius:'999px', fontSize:'0.8rem', fontWeight:'700',
        zIndex:'99999', display:'none', whiteSpace:'nowrap',
        boxShadow:'0 8px 30px rgba(0,0,0,0.3)', maxWidth:'calc(100vw - 2rem)',
      });
      document.body.appendChild(banner);
    }
    banner.style.display = 'block';
  });
  window.addEventListener('online', function() {
    if (banner) {
      banner.textContent = '✅ Reconnecté !';
      banner.style.background = '#059669';
      setTimeout(function() { banner.style.display = 'none'; }, 2500);
    }
  });
}

/* ══════════════════════════════════════════════════════════
   TOAST
══════════════════════════════════════════════════════════ */
function showToast(msg, type) {
  var colors = { success:'#059669', error:'#DC2626', info:'#2563EB', warning:'#D97706' };
  var t = document.createElement('div');
  Object.assign(t.style, {
    position:'fixed', bottom:'5rem', left:'50%',
    transform:'translateX(-50%) translateY(8px)',
    background: colors[type||'success'] || colors.success,
    color:'#fff', padding:'0.75rem 1.5rem', borderRadius:'999px',
    fontSize:'0.875rem', fontWeight:'700', zIndex:'99999',
    boxShadow:'0 8px 30px rgba(0,0,0,0.25)', whiteSpace:'nowrap',
    opacity:'0', transition:'all 0.3s ease', maxWidth:'calc(100vw - 2rem)',
  });
  t.textContent = msg;
  document.body.appendChild(t);
  requestAnimationFrame(function() {
    t.style.opacity = '1';
    t.style.transform = 'translateX(-50%) translateY(0)';
  });
  setTimeout(function() {
    t.style.opacity = '0';
    setTimeout(function() { if (t.parentNode) t.parentNode.removeChild(t); }, 300);
  }, 3500);
}

/* ══════════════════════════════════════════════════════════
   INIT GLOBAL — DOMContentLoaded
══════════════════════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', function() {
  loadTheme();       // PREMIER — évite le flash
  initLoader();
  initNavbar();
  initScrollTop();
  initFlashMessages();
  initNetwork();
});

/* ══════════════════════════════════════════════════════════
   EXPORTS GLOBAUX — Fonctions accessibles depuis HTML onclick
   Nécessaire pour que les boutons HTML puissent les appeler
══════════════════════════════════════════════════════════ */
window.setTheme            = setTheme;
window.toggleThemeSwitcher = function() {
  var panel = document.getElementById('theme-switcher-panel');
  if (panel) panel.classList.toggle('open');
};
window.toggleMobile        = toggleMobile;
window.toggleNavEspace     = toggleNavEspace;
window.toggleFloatEspace   = toggleFloatEspace;
window.toggleAdminSidebar  = toggleAdminSidebar;
window.closeAdminSidebar   = closeAdminSidebar;
window.showToast           = showToast;