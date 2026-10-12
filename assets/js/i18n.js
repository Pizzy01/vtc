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

// Global Helper: Localized WhatsApp Booking Funnel
function openWhatsAppBooking(service = '') {
  const lang = (typeof VitesseI18n !== 'undefined' && VitesseI18n.getLang()) ? VitesseI18n.getLang() : 'fr';
  const serviceSuffix = service ? ` (${service})` : '';
  const templates = {
    fr: `Bonjour Lux-Taxi,\n\nJe souhaite réserver un transfert privé.\n\nDate et heure : \nLieu de prise en charge : \nDestination : \nNombre de passagers : \nBagages : \nType de véhicule souhaité : ${serviceSuffix}\n\nMerci de me confirmer le tarif et la disponibilité.`,
    en: `Hello Lux-Taxi,\n\nI would like to book a private transfer.\n\nDate & time: \nPick-up location: \nDestination: \nNumber of passengers: \nLuggage count: \nPreferred vehicle: ${serviceSuffix}\n\nThank you for confirming the fixed price and availability.`,
    de: `Guten Tag Lux-Taxi,\n\nich möchte eine private Fahrt buchen.\n\nDatum & Uhrzeit: \nAbholort: \nZielort: \nAnzahl der Fahrgäste: \nGepäck: \nGewünschter Fahrzeugtyp: ${serviceSuffix}\n\nBitte bestätigen Sie mir den Festpreis und die Verfügbarkeit.`,
    it: `Buongiorno Lux-Taxi,\n\nvorrei prenotare un trasferimento privato.\n\nData e ora: \nLuogo di partenza: \nDestinazione: \nNumero di passeggeri: \nBagagli: \nTipo di veicolo desiderato: ${serviceSuffix}\n\nGrazie di confermarmi la tariffa fissa e la disponibilità.`
  };
  const message = templates[lang] || templates.fr;
  window.open(`https://wa.me/41766207850?text=${encodeURIComponent(message)}`, '_blank');
}

// Global Helper: Pre-filled Corporate Email Funnel
function openCorporateMail() {
  const subject = encodeURIComponent("Demande de transfert corporate – Lux-Taxi");
  const body = encodeURIComponent(`Bonjour,\n\nJe souhaite obtenir une proposition pour un transport professionnel.\n\nEntreprise : \nNom du contact : \nTéléphone : \nDate(s) et horaire(s) : \nLieu de prise en charge : \nDestination : \nNombre de personnes : \nType de service : transfert aéroport / événement / mise à disposition / autre\nBesoin spécifique (facturation mensuelle, protocole VIP, accueil salon) : \n\nMerci de me transmettre votre proposition.`);
  window.location.href = `mailto:info@lux-taxi.com?subject=${subject}&body=${body}`;
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  VitesseI18n.init();
});
