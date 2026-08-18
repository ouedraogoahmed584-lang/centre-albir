'use strict';

// ── THÈMES ────────────────────────────────────────────
var THEMES = ['classic','dark','gold','emerald','midnight'];

function setTheme(theme) {
  if (THEMES.indexOf(theme) === -1) theme = 'classic';
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('albir-theme', theme);
  document.querySelectorAll('.theme-option').forEach(function(opt) {
    opt.classList.toggle('active', opt.id === 'opt-' + theme);
  });
  var colors = {classic:'#064E3B',dark:'#111111',gold:'#1A1409',
    emerald:'#059669',midnight:'#0A0E1A'};
  var meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.content = colors[theme] || '#064E3B';
}

function loadSavedTheme() {
  setTheme(localStorage.getItem('albir-theme') || 'classic');
}

function toggleThemePanel() {
  var p = document.getElementById('theme-panel');
  if (p) p.classList.toggle('open');
}

document.addEventListener('click', function(e) {
  var p = document.getElementById('theme-panel');
  if (p && p.classList.contains('open') && !p.contains(e.target))
    p.classList.remove('open');
});

// ── NAVBAR SCROLL ─────────────────────────────────────
function initNavbar() {
  var nav = document.getElementById('navbar');
  if (!nav) return;
  window.addEventListener('scroll', function() {
    if (window.scrollY > 60) {
      nav.style.boxShadow = '0 4px 30px rgba(0,0,0,0.25)';
      nav.classList.add('scrolled');
    } else {
      nav.style.boxShadow = 'none';
      nav.classList.remove('scrolled');
    }
  }, {passive:true});
}

// ── MENU MOBILE ───────────────────────────────────────
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
    var icon = document.getElementById('burger-icon');
    if (menu) { menu.classList.remove('open'); menu.style.maxHeight = '0px'; }
    document.body.style.overflow = '';
    if (icon) icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>';
  }
}, {passive:true});

// ── DROPDOWN NAVBAR ESPACE ────────────────────────────
function toggleNavEspace() {
  var dd = document.getElementById('nav-espace-dd');
  if (dd) dd.style.display = (dd.style.display === 'block') ? 'none' : 'block';
}
document.addEventListener('click', function(e) {
  var c = document.getElementById('nav-espace');
  var d = document.getElementById('nav-espace-dd');
  if (d && c && !c.contains(e.target)) d.style.display = 'none';
});

// ── DROPDOWN FLOTTANT ESPACE ──────────────────────────
function toggleFloatEspace() {
  var m = document.getElementById('float-espace-menu');
  if (m) m.style.display = (m.style.display === 'block') ? 'none' : 'block';
}
document.addEventListener('click', function(e) {
  var fe = document.getElementById('float-espace');
  var fm = document.getElementById('float-espace-menu');
  if (fm && fe && !fe.contains(e.target)) fm.style.display = 'none';
});

// ── ADMIN SIDEBAR MOBILE ──────────────────────────────
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
window.addEventListener('resize', function() {
  if (window.innerWidth >= 1024) {
    var s = document.querySelector('.admin-sidebar');
    var o = document.getElementById('admin-overlay');
    if (s) s.classList.remove('mobile-open');
    if (o) o.classList.remove('active');
    document.body.style.overflow = '';
  }
}, {passive:true});

// ── SCROLL TOP ────────────────────────────────────────
function initScrollTop() {
  var btn = document.getElementById('btn-scroll-top');
  if (!btn) return;
  window.addEventListener('scroll', function() {
    btn.classList.toggle('visible', window.scrollY > 400);
  }, {passive:true});
}

// ── LOADER ────────────────────────────────────────────
function initLoader() {
  var loader = document.getElementById('page-loader');
  if (!loader) return;
  function hide() {
    loader.style.opacity = '0';
    loader.style.visibility = 'hidden';
    setTimeout(function() { loader.style.display = 'none'; }, 500);
  }
  if (document.readyState === 'complete') { setTimeout(hide, 300); }
  else { window.addEventListener('load', function() { setTimeout(hide, 300); }); }
  setTimeout(hide, 3000);
}

// ── FLASH AUTO-CLOSE ──────────────────────────────────
function initFlashMessages() {
  var c = document.getElementById('flash-container');
  if (!c) return;
  setTimeout(function() {
    c.style.transition = 'opacity 0.5s ease';
    c.style.opacity = '0';
    setTimeout(function() { if (c.parentNode) c.parentNode.removeChild(c); }, 500);
  }, 6000);
}

// ── RÉSEAU ────────────────────────────────────────────
function initNetworkStatus() {
  var banner = null;
  window.addEventListener('offline', function() {
    if (!banner) {
      banner = document.createElement('div');
      banner.textContent = '📡 Connexion perdue';
      Object.assign(banner.style, {
        position:'fixed',bottom:'5.5rem',left:'50%',
        transform:'translateX(-50%)',background:'#1F2937',color:'#fff',
        padding:'0.625rem 1.25rem',borderRadius:'999px',fontSize:'0.8125rem',
        fontWeight:'700',zIndex:'99999',whiteSpace:'nowrap',
        boxShadow:'0 8px 30px rgba(0,0,0,0.3)',maxWidth:'calc(100vw - 2rem)'
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

// ── TOAST ────────────────────────────────────────────
function showToast(msg, type) {
  var colors = {success:'#059669',error:'#DC2626',info:'#2563EB',warning:'#D97706'};
  var t = document.createElement('div');
  Object.assign(t.style, {
    position:'fixed',bottom:'5rem',left:'50%',
    transform:'translateX(-50%) translateY(8px)',
    background:colors[type||'success'],color:'#fff',
    padding:'0.75rem 1.5rem',borderRadius:'999px',
    fontSize:'0.875rem',fontWeight:'700',zIndex:'99999',
    boxShadow:'0 8px 30px rgba(0,0,0,0.25)',whiteSpace:'nowrap',
    opacity:'0',transition:'all 0.3s ease',maxWidth:'calc(100vw - 2rem)'
  });
  t.textContent = msg;
  document.body.appendChild(t);
  requestAnimationFrame(function() {
    t.style.opacity = '1';
    t.style.transform = 'translateX(-50%) translateY(0)';
  });
  setTimeout(function() {
    t.style.opacity = '0';
    t.style.transform = 'translateX(-50%) translateY(8px)';
    setTimeout(function() { if (t.parentNode) t.parentNode.removeChild(t); }, 300);
  }, 3500);
}

// ── COPY ─────────────────────────────────────────────
function initCopyButtons() {
  document.querySelectorAll('[data-copy]').forEach(function(el) {
    el.style.cursor = 'pointer';
    el.addEventListener('click', function() {
      var text = this.dataset.copy;
      if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function() { showToast('✅ Copié !'); });
      } else {
        var inp = document.createElement('input');
        inp.value = text; document.body.appendChild(inp);
        inp.select(); document.execCommand('copy');
        inp.remove(); showToast('✅ Copié !');
      }
    });
  });
}

// ── INIT GLOBAL ───────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
  loadSavedTheme();
  initLoader();
  initNavbar();
  initScrollTop();
  initFlashMessages();
  initNetworkStatus();
  initCopyButtons();
});
