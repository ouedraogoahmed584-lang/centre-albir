/* Centre Al-Bir — main.js PROPRE */
'use strict';

/* THÈMES */
var THEMES = { albir:1, dark:1, academic:1, light:1, heritage:1 };
var THEME_KEY = 'albir-theme-v2';
var THEME_COLORS = { albir:'#043B2C', dark:'#070B14', academic:'#123A7A', light:'#102030', heritage:'#064E3B' };

function setTheme(theme, save) {
  if (!THEMES[theme]) theme = 'albir';
  if (typeof save === 'undefined') save = true;
  document.documentElement.setAttribute('data-theme', theme);
  if (save) localStorage.setItem(THEME_KEY, theme);
  var meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.content = THEME_COLORS[theme] || '#043B2C';
  document.querySelectorAll('.theme-option').forEach(function(btn) {
    btn.classList.toggle('active', btn.dataset.theme === theme);
  });
  if (save) {
    fetch('/admin/api/theme/save', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({theme:theme})
    }).catch(function(){});
  }
}

function loadTheme() {
  var saved = localStorage.getItem(THEME_KEY);
  if (saved && THEMES[saved]) { setTheme(saved, false); return; }
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    setTheme('dark', false);
  } else {
    setTheme('albir', false);
  }
}

function toggleThemeSwitcher() {
  var p = document.getElementById('theme-switcher-panel');
  if (p) p.classList.toggle('open');
}

document.addEventListener('click', function(e) {
  var p = document.getElementById('theme-switcher-panel');
  if (p && p.classList.contains('open') && !p.contains(e.target)) {
    p.classList.remove('open');
  }
});

/* EXPORTS GLOBAUX */
window.setTheme = setTheme;
window.toggleThemeSwitcher = toggleThemeSwitcher;

/* NAVBAR */
function initNavbar() {
  var nav = document.getElementById('navbar');
  if (!nav) return;
  window.addEventListener('scroll', function() {
    nav.classList.toggle('scrolled', window.scrollY > 60);
  }, { passive: true });
}

/* MENU MOBILE */
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

/* DROPDOWN ESPACE */
window.toggleNavEspace = function() {
  var dd = document.getElementById('nav-espace-dd');
  if (dd) dd.style.display = (dd.style.display === 'block') ? 'none' : 'block';
};
document.addEventListener('click', function(e) {
  var c = document.getElementById('nav-espace');
  var d = document.getElementById('nav-espace-dd');
  if (d && c && !c.contains(e.target)) d.style.display = 'none';
});





/* ══ ESPACE PERSONNEL — Menu animé premium ════════════ */
window.toggleFbEspace = function(event) {
  if (event) event.stopPropagation();

  var menu = document.getElementById('fb-espace-menu');
  if (!menu) return;

  var isOpen = menu.style.display === 'block';

  if (isOpen) {
    // Fermeture animée
    menu.style.opacity = '0';
    menu.style.transform = 'scale(0.92) translateX(8px)';
    setTimeout(function() {
      menu.style.display = 'none';
    }, 220);
  } else {
    // Ouverture animée
    menu.style.display = 'block';
    // Forcer reflow pour que la transition se déclenche
    menu.offsetHeight;
    menu.style.opacity = '1';
    menu.style.transform = 'scale(1) translateX(0)';
  }
};

window.toggleFloatEspace = window.toggleFbEspace;

// Fermer si clic extérieur
document.addEventListener('click', function(e) {
  var container = document.getElementById('float-espace');
  var menu      = document.getElementById('fb-espace-menu');
  if (!menu || !container) return;
  if (!container.contains(e.target) && menu.style.display === 'block') {
    menu.style.opacity   = '0';
    menu.style.transform = 'scale(0.92) translateX(8px)';
    setTimeout(function() { menu.style.display = 'none'; }, 220);
  }
});
/* ADMIN SIDEBAR */
var _sidebarOpen = false;
var _touchStartX = 0;
var _touchStartY = 0;

window.openAdminSidebar = function() {
  if (_sidebarOpen) return;
  _sidebarOpen = true;
  var s = document.getElementById('admin-sidebar');
  var o = document.getElementById('admin-overlay');
  if (s) s.classList.add('mobile-open');
  if (o) { o.style.display = 'block'; requestAnimationFrame(function() { o.classList.add('active'); }); }
  document.body.style.overflow = 'hidden';
  history.pushState({ adminMenu: true }, '');
};

window.closeAdminSidebar = function() {
  if (!_sidebarOpen) return;
  _sidebarOpen = false;
  var s = document.getElementById('admin-sidebar');
  var o = document.getElementById('admin-overlay');
  if (s) s.classList.remove('mobile-open');
  if (o) { o.classList.remove('active'); setTimeout(function() { if (!_sidebarOpen) o.style.display = 'none'; }, 320); }
  document.body.style.overflow = '';
};

window.toggleAdminSidebar = function() {
  if (_sidebarOpen) window.closeAdminSidebar();
  else window.openAdminSidebar();
};

window.closeSidebarOnMobile = function() {
  if (window.innerWidth < 1024) window.closeAdminSidebar();
};

window.addEventListener('resize', function() {
  if (window.innerWidth >= 1024) window.closeAdminSidebar();
}, { passive: true });

window.addEventListener('popstate', function() {
  if (_sidebarOpen) { window.closeAdminSidebar(); history.pushState(null, ''); }
});

document.addEventListener('touchstart', function(e) {
  _touchStartX = e.touches[0].clientX;
  _touchStartY = e.touches[0].clientY;
}, { passive: true });

document.addEventListener('touchend', function(e) {
  if (!_sidebarOpen) return;
  var dx = e.changedTouches[0].clientX - _touchStartX;
  var dy = Math.abs(e.changedTouches[0].clientY - _touchStartY);
  if (dx < -65 && dy < 85) window.closeAdminSidebar();
}, { passive: true });

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape' && _sidebarOpen) window.closeAdminSidebar();
});

/* SCROLL TOP */
function initScrollTop() {
  var btn = document.getElementById('fb-scroll');
  if (!btn) return;
  window.addEventListener('scroll', function() {
    btn.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });
}

/* LOADER */
function initLoader() {
  var loader = document.getElementById('page-loader');
  if (!loader) return;
  function hide() { loader.classList.add('hidden'); }
  if (document.readyState === 'complete') { setTimeout(hide, 280); }
  else { window.addEventListener('load', function() { setTimeout(hide, 280); }); }
  setTimeout(hide, 4000);
}

/* AOS INIT */
function initAOS() {
  if (typeof AOS !== 'undefined') {
    AOS.init({ duration: 700, easing: 'ease-out-cubic', once: true, offset: 60 });
  } else {
    document.body.classList.add('aos-failed');
  }
}

/* COMPTEURS ANIMÉS */
function initCounters() {
  var counters = document.querySelectorAll('[data-counter]');
  if (!counters.length) return;
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (!entry.isIntersecting) return;
      var el = entry.target;
      var target = parseFloat((el.dataset.counter || '0').replace(/[^0-9.]/g, '')) || 0;
      var suffix = el.dataset.suffix || '';
      var start = null;
      var duration = 1800;
      function step(ts) {
        if (!start) start = ts;
        var progress = Math.min((ts - start) / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.round(target * eased).toLocaleString('fr-FR') + suffix;
        if (progress < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
      observer.unobserve(el);
    });
  }, { threshold: 0.6 });
  counters.forEach(function(el) { observer.observe(el); });
}

/* FLASH */
function initFlash() {
  var c = document.getElementById('flash-container');
  if (!c) return;
  setTimeout(function() {
    c.style.transition = 'opacity 0.5s ease';
    c.style.opacity = '0';
    setTimeout(function() { if (c.parentNode) c.parentNode.removeChild(c); }, 500);
  }, 6000);
}

/* RÉSEAU */
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
        borderRadius:'999px', fontSize:'0.8rem', fontWeight:'700',
        zIndex:'99999', display:'none', whiteSpace:'nowrap',
        boxShadow:'0 8px 32px rgba(0,0,0,0.3)', maxWidth:'calc(100vw - 2rem)'
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

/* TOAST */
window.showToast = function(msg, type) {
  var colors = { success:'#059669', error:'#DC2626', info:'#2563EB', warning:'#D97706' };
  var t = document.createElement('div');
  Object.assign(t.style, {
    position:'fixed', bottom:'5rem', left:'50%',
    transform:'translateX(-50%) translateY(10px)',
    background: colors[type||'success'], color:'#fff',
    padding:'0.75rem 1.625rem', borderRadius:'999px',
    fontSize:'0.875rem', fontWeight:'700', zIndex:'99999',
    boxShadow:'0 8px 32px rgba(0,0,0,0.28)', whiteSpace:'nowrap',
    opacity:'0', transition:'all 0.32s ease',
    maxWidth:'calc(100vw - 2rem)'
  });
  t.textContent = msg;
  document.body.appendChild(t);
  requestAnimationFrame(function() {
    t.style.opacity = '1';
    t.style.transform = 'translateX(-50%) translateY(0)';
  });
  setTimeout(function() {
    t.style.opacity = '0';
    setTimeout(function() { if (t.parentNode) t.parentNode.removeChild(t); }, 320);
  }, 3800);
};

/* BOUTON THÈME NAVBAR */
function bindNavThemeBtn() {
  var btn   = document.getElementById('navbar-theme-btn');
  var panel = document.getElementById('theme-switcher-panel');
  if (!btn || !panel) return;
  btn.addEventListener('click', function(e) {
    e.stopPropagation();
    panel.classList.toggle('open');
  });
}

/* INIT GLOBAL */
document.addEventListener('DOMContentLoaded', function() {
  loadTheme();
  initLoader();
  initNavbar();
  initScrollTop();
  initFlash();
  initNetwork();
  initCounters();
  bindNavThemeBtn();
  if (document.readyState === 'complete') { initAOS(); }
  else { window.addEventListener('load', initAOS); }
});
