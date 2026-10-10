/**
 * VITESSE PRESTIGE — Light Reactive i18n Engine
 * Handles FR, EN, DE, IT translations without page reload or form input loss.
 */

const VitesseI18n = (function() {
  const supportedLangs = ['fr', 'en', 'de', 'it'];
  let currentLang = 'fr';
  let translations = {};

  // Get nested property value from JSON (e.g., "hero.title_part1")
  function getNestedTranslation(obj, path) {
    return path.split('.').reduce((prev, curr) => prev && prev[curr], obj);
  }

  // Load language JSON dictionary
  async function loadTranslations(lang) {
    try {
      const response = await fetch(`assets/locales/${lang}.json`);
      if (!response.ok) throw new Error(`Failed to load ${lang}.json`);
      translations[lang] = await response.json();
      return true;
    } catch (err) {
      console.warn(`[i18n] Error loading language ${lang}:`, err);
      return false;
    }
  }

  // Apply translations to DOM elements with data-i18n attributes
  function applyDOMTranslations(lang) {
    const langData = translations[lang];
    if (!langData) return;

    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      const val = getNestedTranslation(langData, key);
      if (val) {
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
          if (el.hasAttribute('placeholder')) {
            el.setAttribute('placeholder', val);
          }
        } else {
          el.textContent = val;
        }
      }
    });

    // Update <html lang="...">
    document.documentElement.lang = lang;

    // Update active label in dropdown if present
    const langLabel = document.getElementById('active-lang-code');
    if (langLabel) {
      langLabel.textContent = lang.toUpperCase();
    }
  }

  // Set active language
  async function setLanguage(lang) {
    if (!supportedLangs.includes(lang)) lang = 'fr';
    
    if (!translations[lang]) {
      const success = await loadTranslations(lang);
      if (!success) return;
    }

    currentLang = lang;
    localStorage.setItem('vp_lang', lang);
    applyDOMTranslations(lang);

    // Dispatch event for custom components
    window.dispatchEvent(new CustomEvent('vp-lang-changed', { detail: { lang } }));
  }

  // Initialize engine
  async function init() {
    // Check URL params (?lang=en) or localStorage
    const urlParams = new URLSearchParams(window.location.search);
    const paramLang = urlParams.get('lang');
    const savedLang = localStorage.getItem('vp_lang');
    
    const initialLang = (paramLang && supportedLangs.includes(paramLang)) 
      ? paramLang 
      : (savedLang && supportedLangs.includes(savedLang) ? savedLang : 'fr');

    await setLanguage(initialLang);
  }

  return {
    init,
    setLanguage,
    getLang: () => currentLang
  };
})();

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  VitesseI18n.init();
});
