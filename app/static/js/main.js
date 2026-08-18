// ============================================================
// FICHIER #52 — static/js/main.js
// Script JavaScript global du Centre Al-Bir. Contient toutes
// les interactions communes à toutes les pages : compteur animé
// pour les statistiques, lazy loading des images, fermeture
// automatique des messages flash, animation de smooth scroll,
// détection de la connexion réseau et utilitaires généraux.
// ============================================================

'use strict';

/* ══════════════════════════════════════════════════════════
   INITIALISATION AU CHARGEMENT
══════════════════════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', function () {
  initCounters();
  initLazyImages();
  initSmoothScroll();
  initAutoCloseFlash();
  initNetworkStatus();
  initCopyToClipboard();
});


/* ══════════════════════════════════════════════════════════
   COMPTEUR ANIMÉ — Statistiques de la page d'accueil
   Anime les chiffres de 0 jusqu'à leur valeur cible
   lors de leur apparition dans le viewport.
══════════════════════════════════════════════════════════ */
function initCounters() {
  const counters = document.querySelectorAll('[data-counter]');
  if (!counters.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el      = entry.target;
        const target  = parseInt(el.dataset.counter, 10);
        const suffix  = el.dataset.suffix || '';
        const duration = 1800;
        const step    = Math.ceil(target / (duration / 16));
        let current   = 0;

        const timer = setInterval(() => {
          current = Math.min(current + step, target);
          el.textContent = current.toLocaleString('fr-FR') + suffix;
          if (current >= target) clearInterval(timer);
        }, 16);

        observer.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(el => observer.observe(el));
}


/* ══════════════════════════════════════════════════════════
   LAZY LOADING — Chargement différé des images
   Charge les images uniquement quand elles entrent dans
   le viewport, améliorant les performances sur mobile.
══════════════════════════════════════════════════════════ */
function initLazyImages() {
  if (!('IntersectionObserver' in window)) return;

  const lazyImages = document.querySelectorAll('img[data-src]');
  if (!lazyImages.length) return;

  const imageObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.classList.add('animate-fade-in');
        img.removeAttribute('data-src');
        imageObserver.unobserve(img);
      }
    });
  }, { rootMargin: '100px' });

  lazyImages.forEach(img => imageObserver.observe(img));
}


/* ══════════════════════════════════════════════════════════
   SMOOTH SCROLL — Navigation fluide vers les ancres
   Intercepte les liens internes (#section) pour une
   navigation animée et prend en compte la hauteur de navbar.
══════════════════════════════════════════════════════════ */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        const navHeight = document.getElementById('navbar')
          ? document.getElementById('navbar').offsetHeight
          : 70;
        const top = target.getBoundingClientRect().top
          + window.pageYOffset
          - navHeight
          - 20;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });
  });
}


/* ══════════════════════════════════════════════════════════
   MESSAGES FLASH — Fermeture automatique
   Ferme automatiquement les alertes après 6 secondes
   avec une transition douce. L'utilisateur peut aussi
   fermer manuellement en cliquant.
══════════════════════════════════════════════════════════ */
function initAutoCloseFlash() {
  const flashContainer = document.getElementById('flash-container');
  if (!flashContainer) return;

  setTimeout(() => {
    flashContainer.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    flashContainer.style.opacity    = '0';
    flashContainer.style.transform  = 'translateX(20px)';
    setTimeout(() => {
      if (flashContainer.parentNode) {
        flashContainer.parentNode.removeChild(flashContainer);
      }
    }, 500);
  }, 6000);
}


/* ══════════════════════════════════════════════════════════
   STATUT RÉSEAU — Détection hors-ligne
   Affiche un avertissement discret si la connexion internet
   est perdue. Particulièrement utile en Afrique de l'Ouest
   où la connectivité peut être intermittente.
══════════════════════════════════════════════════════════ */
function initNetworkStatus() {
  const banner = createNetworkBanner();

  window.addEventListener('offline', () => {
    banner.style.display = 'flex';
    banner.classList.add('animate-fade-in');
  });

  window.addEventListener('online', () => {
    banner.style.opacity    = '0';
    banner.style.transition = 'opacity 0.5s ease';
    setTimeout(() => { banner.style.display = 'none'; banner.style.opacity = '1'; }, 500);
  });
}

function createNetworkBanner() {
  const banner = document.createElement('div');
  banner.id    = 'network-banner';
  banner.style.cssText = `
    display: none;
    position: fixed;
    bottom: 80px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 9999;
    background: #1F2937;
    color: white;
    padding: 12px 24px;
    border-radius: 50px;
    font-size: 13px;
    font-weight: 600;
    align-items: center;
    gap: 8px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
    white-space: nowrap;
  `;
  banner.innerHTML = '📡 Connexion perdue — Vérifiez votre réseau';
  document.body.appendChild(banner);
  return banner;
}


/* ══════════════════════════════════════════════════════════
   COPIE AU PRESSE-PAPIERS — Numéros de téléphone
   Permet de copier rapidement un numéro ou texte en
   cliquant sur un élément avec data-copy. Affiche une
   confirmation visuelle brève.
══════════════════════════════════════════════════════════ */
function initCopyToClipboard() {
  document.querySelectorAll('[data-copy]').forEach(el => {
    el.style.cursor = 'pointer';
    el.addEventListener('click', function () {
      const text = this.dataset.copy;
      navigator.clipboard.writeText(text).then(() => {
        const original = this.textContent;
        this.textContent = '✅ Copié !';
        this.style.color = '#059669';
        setTimeout(() => {
          this.textContent = original;
          this.style.color = '';
        }, 2000);
      }).catch(() => {
        // Fallback pour les navigateurs sans clipboard API
        const input = document.createElement('input');
        input.value = text;
        document.body.appendChild(input);
        input.select();
        document.execCommand('copy');
        document.body.removeChild(input);
      });
    });
  });
}


/* ══════════════════════════════════════════════════════════
   UTILITAIRES GLOBAUX
══════════════════════════════════════════════════════════ */

/**
 * Formate un montant en FCFA
 * @param {number} amount
 * @returns {string}
 */
function formatFCFA(amount) {
  return new Intl.NumberFormat('fr-BF', {
    style: 'currency',
    currency: 'XOF',
    minimumFractionDigits: 0,
  }).format(amount);
}

/**
 * Formate une date en français
 * @param {string|Date} date
 * @returns {string}
 */
function formatDateFR(date) {
  return new Intl.DateTimeFormat('fr-BF', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  }).format(new Date(date));
}

/**
 * Debounce — limite la fréquence d'appel d'une fonction
 * @param {Function} fn
 * @param {number} delay
 * @returns {Function}
 */
function debounce(fn, delay = 300) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

/**
 * Affiche un toast de notification rapide
 * @param {string} message
 * @param {string} type — 'success' | 'error' | 'info'
 */
function showToast(message, type = 'success') {
  const colors = {
    success: 'bg-green-600',
    error:   'bg-red-600',
    info:    'bg-primary-900',
  };
  const toast = document.createElement('div');
  toast.className = `
    fixed bottom-24 left-1/2 -translate-x-1/2 z-[9998]
    ${colors[type] || colors.info} text-white
    px-6 py-3 rounded-full text-sm font-bold shadow-2xl
    animate-fade-in whitespace-nowrap
  `;
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity    = '0';
    toast.style.transition = 'opacity 0.4s ease';
    setTimeout(() => {
      if (toast.parentNode) toast.parentNode.removeChild(toast);
    }, 400);
  }, 3500);
}