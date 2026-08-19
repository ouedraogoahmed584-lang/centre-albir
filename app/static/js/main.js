/* ============================================================
   CENTRE AL-BIR — main.js PREMIUM 2026
   Système de thèmes · Navbar intelligente · Compteurs animés
   Sidebar admin · Boutons flottants · Gestes mobile
   ============================================================ */

'use strict';

/* ══════════════════════════════════════════════════════════
   SYSTÈME DE THÈMES PREMIUM
══════════════════════════════════════════════════════════ */
var THEMES = {
  albir:    { name: '🌿 Emerald Luxury Al-Bir',   desc: 'Vert islamique premium' },
  dark:     { name: '🌑 Midnight Gold Premium',   desc: 'Luxe nuit & or champagne' },
  academic: { name: '🔵 Academic Blue',            desc: 'Université internationale' },
  light:    { name: '☀️ Light Professional',       desc: 'Cabinet premium clair' },
  heritage: { name: '✨ Islamic Heritage',          desc: 'Tradition + modernité' },
};
var THEME_KEY = 'albir-theme-v2';
var THEME_META = { albir:'#043B2C', dark:'#070B14', academic:'#123A7A', light:'#102030', heritage:'#064E3B' };

function setTheme(theme, save) {
  if (!THEMES[theme]) theme = 'albir';
  if (typeof save === 'undefined') save = true;

  document.documentElement.setAttribute('data-theme', theme);
  if (save) {
    localStorage.setItem(THEME_KEY, theme);
    // Sauvegarder silencieusement en BDD
    fetch('/admin/api/theme/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ theme: theme }),
    }).catch(function() {});
  }

  // Meta theme-color
  var meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.content = THEME_META[theme] || '#043B2C';

  // Mettre à jour les boutons
  document.querySelectorAll('.theme-option').forEach(function(btn) {
    btn.classList.toggle('active', btn.dataset.theme === theme);
  });
}

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

// Écouter changement système
if (window.matchMedia) {
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
    if (!localStorage.getItem(THEME_KEY)) {
      setTheme(e.matches ? 'dark' : 'albir', false);
    }
  });
}

function toggleThemeSwitcher() {
  var panel = document.getElementById('theme-switcher-panel');
  if (panel) panel.classList.toggle('open');
}

// Fermer panneau thèmes si clic extérieur
document.addEventListener('click', function(e) {
  var panel = document.getElementById('theme-switcher-panel');
  if (panel && panel.classList.contains('open') && !panel.contains(e.target)) {
    panel.classList.remove('open');
  }
});

// Exports globaux
window.setTheme = setTheme;
window.toggleThemeSwitcher = toggleThemeSwitcher;

/* ══════════════════════════════════════════════════════════
   NAVBAR INTELLIGENTE — Transparente → Solide au scroll
══════════════════════════════════════════════════════════ */
function initNavbar() {
  var nav = document.getElementById('navbar');
  if (!nav) return;

  // Pages avec hero sombre → navbar transparente au début
  var hasHero = document.querySelector('.hero, [class*="hero"]');

  function updateNav() {
    if (hasHero) {
      if (window.scrollY > 80) {
        nav.classList.add('scrolled');
        nav.classList.remove('transparent');
      } else {
        nav.classList.remove('scrolled');
        nav.classList.add('transparent');
      }
    } else {
      nav.classList.add('solid', 'scrolled');
    }
  }

  window.addEventListener('scroll', updateNav, { passive: true });
  updateNav();
}
window.toggleMobile = function() {
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
};
window.addEventListener('resize', function() {
  if (window.innerWidth >= 1024) {
    var menu = document.getElementById('mobile-menu');
    if (menu) { menu.classList.remove('open'); menu.style.maxHeight = '0px'; }
    document.body.style.overflow = '';
  }
}, { passive: true });

/* ══════════════════════════════════════════════════════════
   DROPDOWN ESPACE PERSONNEL
══════════════════════════════════════════════════════════ */
window.toggleNavEspace = function() {
  var dd = document.getElementById('nav-espace-dd');
  if (dd) dd.style.display = (dd.style.display === 'block') ? 'none' : 'block';
};
document.addEventListener('click', function(e) {
  var c = document.getElementById('nav-espace');
  var d = document.getElementById('nav-espace-dd');
  if (d && c && !c.contains(e.target)) d.style.display = 'none';
});
window.toggleFloatEspace = function() {
  var m = document.getElementById('fb-espace-menu');
  if (m) m.style.display = (m.style.display === 'block') ? 'none' : 'block';
};
document.addEventListener('click', function(e) {
  var fe = document.getElementById('float-espace');
  var fm = document.getElementById('fb-espace-menu');
  if (fm && fe && !fe.contains(e.target) &&
      e.target.id !== 'fb-espace' && !document.getElementById('fb-espace')?.contains(e.target)) {
    fm.style.display = 'none';
  }
});

/* ══════════════════════════════════════════════════════════
   ADMIN SIDEBAR — Tous les modes de fermeture
══════════════════════════════════════════════════════════ */
var _sidebarOpen = false;
var _touchStartX = 0;
var _touchStartY = 0;

function openAdminSidebar() {
  if (_sidebarOpen) return;
  _sidebarOpen = true;
  var sidebar  = document.getElementById('admin-sidebar');
  var overlay  = document.getElementById('admin-overlay');
  if (sidebar) sidebar.classList.add('mobile-open');
  if (overlay) {
    overlay.style.display = 'block';
    requestAnimationFrame(function() { overlay.classList.add('active'); });
  }
  document.body.style.overflow = 'hidden';
  history.pushState({ adminMenu: true }, '');
}

function closeAdminSidebar() {
  if (!_sidebarOpen) return;
  _sidebarOpen = false;
  var sidebar = document.getElementById('admin-sidebar');
  var overlay = document.getElementById('admin-overlay');
  if (sidebar) sidebar.classList.remove('mobile-open');
  if (overlay) {
    overlay.classList.remove('active');
    setTimeout(function() { if (!_sidebarOpen) overlay.style.display = 'none'; }, 320);
  }
  document.body.style.overflow = '';
}

window.openAdminSidebar  = openAdminSidebar;
window.closeAdminSidebar = closeAdminSidebar;
window.toggleAdminSidebar = function() {
  if (_sidebarOpen) closeAdminSidebar(); else openAdminSidebar();
};

// Fermer sur resize desktop
window.addEventListener('resize', function() {
  if (window.innerWidth >= 1024) closeAdminSidebar();
}, { passive: true });

// Bouton retour Android
window.addEventListener('popstate', function(e) {
  if (_sidebarOpen) { closeAdminSidebar(); history.pushState(null, ''); }
});

// Swipe gauche pour fermer
document.addEventListener('touchstart', function(e) {
  _touchStartX = e.touches[0].clientX;
  _touchStartY = e.touches[0].clientY;
}, { passive: true });

document.addEventListener('touchend', function(e) {
  if (!_sidebarOpen) return;
  var dx = e.changedTouches[0].clientX - _touchStartX;
  var dy = Math.abs(e.changedTouches[0].clientY - _touchStartY);
  if (dx < -65 && dy < 85) closeAdminSidebar();
}, { passive: true });

// Touche Échap
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape' && _sidebarOpen) closeAdminSidebar();
});

function closeSidebarOnMobile() {
  if (window.innerWidth < 1024) closeAdminSidebar();
}
window.closeSidebarOnMobile = closeSidebarOnMobile;

/* ══════════════════════════════════════════════════════════
   SCROLL TOP BUTTON
══════════════════════════════════════════════════════════ */
function initScrollTop() {
  var btn = document.getElementById('fb-scroll');
  if (!btn) return;
  window.addEventListener('scroll', function() {
    btn.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });
}

/* ══════════════════════════════════════════════════════════
   DROPDOWN FLOTTANT ESPACE
══════════════════════════════════════════════════════════ */
window.toggleFbEspace = function(e) {
  e && e.stopPropagation();
  var m = document.getElementById('fb-espace-menu');
  if (!m) return;
  m.style.display = (m.style.display === 'block') ? 'none' : 'block';
};

/* ══════════════════════════════════════════════════════════
   COMPTEURS ANIMÉS PREMIUM
══════════════════════════════════════════════════════════ */
function initCounters() {
  var counters = document.querySelectorAll('[data-counter]');
  if (!counters.length) return;

  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (!entry.isIntersecting) return;
      var el       = entry.target;
      var rawValue = el.dataset.counter || '0';
      var suffix   = el.dataset.suffix  || '';
      var prefix   = el.dataset.prefix  || '';

      // Extraire valeur numérique
      var numStr  = rawValue.replace(/[^0-9.]/g, '');
      var target  = parseFloat(numStr) || 0;
      var isFloat = rawValue.includes('.');
      var duration = 1800;
      var startTime = null;

      function animate(timestamp) {
        if (!startTime) startTime = timestamp;
        var progress = Math.min((timestamp - startTime) / duration, 1);
        // Easing out cubic
        var eased = 1 - Math.pow(1 - progress, 3);
        var current = target * eased;
        var display = isFloat ? current.toFixed(1) : Math.round(current).toLocaleString('fr-FR');
        el.textContent = prefix + display + suffix;
        if (progress < 1) requestAnimationFrame(animate);
      }

      requestAnimationFrame(animate);
      observer.unobserve(el);
    });
  }, { threshold: 0.6 });

  counters.forEach(function(el) { observer.observe(el); });
}

/* ══════════════════════════════════════════════════════════
   LOADER PREMIUM
══════════════════════════════════════════════════════════ */
function initLoader() {
  var loader = document.getElementById('page-loader');
  if (!loader) return;
  function hide() { loader.classList.add('hidden'); }
  if (document.readyState === 'complete') { setTimeout(hide, 280); }
  else { window.addEventListener('load', function() { setTimeout(hide, 280); }); }
  setTimeout(hide, 4000);
}

/* ══════════════════════════════════════════════════════════
   AOS INIT ROBUSTE
══════════════════════════════════════════════════════════ */
);
  } else {
    // Fallback : rendre tout visible
    document.querySelectorAll('[data-aos]').forEach(function(el) {
      el.style.opacity = '1';
      el.style.transform = 'none';
    });
  }
  // Fallback après 1.5s
  setTimeout(function() {
    document.querySelectorAll('[data-aos]').forEach(function(el) {
      el.style.opacity = '1';
      el.style.transform = 'none';
    });
  }, 1500);
}

/* ══════════════════════════════════════════════════════════
   FLASH AUTO-CLOSE
══════════════════════════════════════════════════════════ */
function initFlashMessages() {
  var c = document.getElementById('flash-container');
  if (!c) return;
  setTimeout(function() {
    c.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    c.style.opacity = '0'; c.style.transform = 'translateX(20px)';
    setTimeout(function() { if (c.parentNode) c.parentNode.removeChild(c); }, 500);
  }, 6000);
}

/* ══════════════════════════════════════════════════════════
   RÉSEAU HORS-LIGNE
══════════════════════════════════════════════════════════ */
function initNetwork() {
  var banner = null;
  window.addEventListener('offline', function() {
    if (!banner) {
      banner = document.createElement('div');
      banner.textContent = '📡 Connexion perdue';
      Object.assign(banner.style, {
        position:'fixed', bottom:'5.5rem', left:'50%',
        transform:'translateX(-50%)', background:'#1F2937',
        color:'#fff', padding:'0.625rem 1.375rem',
        borderRadius:'999px', fontSize:'0.8125rem',
        fontWeight:'700', zIndex:'99999', display:'none',
        whiteSpace:'nowrap', boxShadow:'0 8px 32px rgba(0,0,0,0.3)',
        maxWidth:'calc(100vw - 2rem)',
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
   TOAST NOTIFICATION
══════════════════════════════════════════════════════════ */
window.showToast = function(msg, type) {
  var colors = { success:'#059669', error:'#DC2626', info:'#2563EB', warning:'#D97706' };
  var t = document.createElement('div');
  Object.assign(t.style, {
    position:'fixed', bottom:'5rem', left:'50%',
    transform:'translateX(-50%) translateY(10px)',
    background: colors[type||'success'], color:'#fff',
    padding:'0.75rem 1.625rem', borderRadius:'999px',
    fontSize:'0.875rem', fontWeight:'700', zIndex:'99999',
    boxShadow:'0 8px 32px rgba(0,0,0,0.28)',
    whiteSpace:'nowrap', opacity:'0',
    transition:'all 0.32s cubic-bezier(0.34,1.56,0.64,1)',
    maxWidth:'calc(100vw - 2rem)',
  });
  t.textContent = msg;
  document.body.appendChild(t);
  requestAnimationFrame(function() {
    t.style.opacity = '1'; t.style.transform = 'translateX(-50%) translateY(0)';
  });
  setTimeout(function() {
    t.style.opacity = '0'; t.style.transform = 'translateX(-50%) translateY(8px)';
    setTimeout(function() { if (t.parentNode) t.parentNode.removeChild(t); }, 320);
  }, 3800);
};

/* ══════════════════════════════════════════════════════════
   LIAISON BOUTON THÈME NAVBAR
══════════════════════════════════════════════════════════ */
function bindNavbarThemeBtn() {
  var btn   = document.getElementById('navbar-theme-btn');
  var panel = document.getElementById('theme-switcher-panel');
  if (!btn || !panel) return;
  btn.addEventListener('click', function(e) {
    e.stopPropagation();
    panel.classList.toggle('open');
  });
}


/* ══════════════════════════════════════════════════════════
   AOS INIT — Animations au scroll
   Version correcte : laisse AOS masquer/révéler les éléments
══════════════════════════════════════════════════════════ */
function initAOS() {
  if (typeof AOS !== 'undefined') {
    AOS.init({
      duration: 700,
      easing:   'ease-out-cubic',
      once:     true,
      offset:   60,
      delay:    0,
    });
  } else {
    // AOS non chargé (CDN bloqué) — rendre visible proprement
    document.body.classList.add('aos-failed');
    console.warn('[Al-Bir] AOS CDN non disponible - fallback activé');
  }
}
/* ══════════════════════════════════════════════════════════
   INITIALISATION GLOBALE
══════════════════════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', function() {
  // 1. Thème en premier (anti-FOUC)
  loadTheme();

  // 2. Modules
  initLoader();
  initNavbar();
  initScrollTop();
  initFlashMessages();
  initNetwork();
  initCounters();
  bindNavbarThemeBtn();

  // 3. AOS après chargement complet
  if (document.readyState === 'complete') { initAOS(); }
  else { window.addEventListener('load', initAOS); }

  // 4. Resize
  window.addEventListener('resize', function() {
    if (window.innerWidth >= 1024) closeAdminSidebar();
  }, { passive: true });
});
