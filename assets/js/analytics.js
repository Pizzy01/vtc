/*
 * Mesure des actions importantes pour Google Analytics 4 (propriété G-E1BTELQ36P).
 * Événements envoyés :
 *   - click_whatsapp : clic sur un lien wa.me
 *   - click_phone    : clic sur un lien tel:
 *   - click_email    : clic sur un lien mailto:
 *   - generate_lead  : demande envoyée (formulaire de contact, ou réservation WhatsApp de l'accueil),
 *                      déclenché depuis le code des pages via window.luxTrack('generate_lead', {...})
 * À déclarer comme « événements clés » dans GA4 : generate_lead, click_whatsapp, click_phone.
 */
(function () {
  function send(name, params) {
    if (typeof window.gtag !== 'function') return;
    window.gtag('event', name, Object.assign({ page_path: location.pathname }, params || {}));
  }
  window.luxTrack = send;

  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (href.indexOf('wa.me') !== -1 || href.indexOf('api.whatsapp.com') !== -1) {
      send('click_whatsapp', { link_text: (a.textContent || '').trim().slice(0, 60) });
    } else if (href.indexOf('tel:') === 0) {
      send('click_phone', { link_text: (a.textContent || '').trim().slice(0, 60) });
    } else if (href.indexOf('mailto:') === 0) {
      send('click_email', {});
    }
  }, true);

  /* ---------- Bannière de consentement (mesure d'audience) ----------
   * Choix enregistré dans localStorage « lux_consent » = granted | denied.
   * Le choix est appliqué dès le <head> de chaque page (voir le bloc Google Analytics).
   * Pour rouvrir la bannière : window.luxConsent.ouvrir()
   */
  var CLE = 'lux_consent';
  var TEXTES = {
    fr: { t: 'Nous utilisons des cookies de mesure d’audience (Google Analytics) pour améliorer le site. Aucune publicité.', ok: 'Accepter', non: 'Refuser' },
    en: { t: 'We use audience measurement cookies (Google Analytics) to improve this site. No advertising.', ok: 'Accept', non: 'Decline' },
    de: { t: 'Wir verwenden Cookies zur Reichweitenmessung (Google Analytics), um die Website zu verbessern. Keine Werbung.', ok: 'Akzeptieren', non: 'Ablehnen' },
    it: { t: 'Utilizziamo cookie di misurazione del pubblico (Google Analytics) per migliorare il sito. Nessuna pubblicità.', ok: 'Accetta', non: 'Rifiuta' }
  };

  function lireChoix() { try { return localStorage.getItem(CLE); } catch (e) { return null; } }
  function enregistrer(v) {
    try { localStorage.setItem(CLE, v); } catch (e) {}
    if (typeof window.gtag === 'function') window.gtag('consent', 'update', { analytics_storage: v });
  }
  function langue() {
    var l = '';
    try { l = localStorage.getItem('vp_lang') || ''; } catch (e) {}
    l = (l || document.documentElement.lang || 'fr').slice(0, 2).toLowerCase();
    return TEXTES[l] ? l : 'fr';
  }

  function ouvrir() {
    if (document.getElementById('lux-consent')) return;
    var tx = TEXTES[langue()];
    var b = document.createElement('div');
    b.id = 'lux-consent';
    b.setAttribute('role', 'dialog');
    b.setAttribute('aria-live', 'polite');
    b.setAttribute('aria-label', 'Cookies');
    b.style.cssText = 'position:fixed;left:16px;right:16px;bottom:16px;z-index:9999;max-width:560px;margin:0 auto;' +
      'background:#111113;color:#F5F1E8;border:1px solid rgba(198,169,107,.45);border-radius:16px;' +
      'padding:14px 16px;font:13px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;' +
      'box-shadow:0 12px 40px rgba(0,0,0,.5);display:flex;flex-wrap:wrap;gap:10px 14px;align-items:center';
    var p = document.createElement('p');
    p.style.cssText = 'margin:0;flex:1 1 260px';
    p.textContent = tx.t;
    var zone = document.createElement('div');
    zone.style.cssText = 'display:flex;gap:8px;flex:0 0 auto';
    function bouton(label, plein, valeur) {
      var x = document.createElement('button');
      x.type = 'button';
      x.textContent = label;
      x.style.cssText = 'cursor:pointer;border-radius:999px;padding:8px 16px;font:600 12px/1 system-ui,sans-serif;' +
        (plein ? 'background:#C6A96B;color:#0B0B0C;border:1px solid #C6A96B'
               : 'background:transparent;color:#F5F1E8;border:1px solid #3a3a3a');
      x.addEventListener('click', function () { enregistrer(valeur); b.remove(); });
      return x;
    }
    zone.appendChild(bouton(tx.non, false, 'denied'));
    zone.appendChild(bouton(tx.ok, true, 'granted'));
    b.appendChild(p);
    b.appendChild(zone);
    // Sur mobile, ne pas cacher la barre WhatsApp / Appel du bas de l'écran
    var barre = document.getElementById('mobile-sticky-bar');
    if (barre && barre.offsetParent !== null && barre.getBoundingClientRect().height > 0) {
      b.style.bottom = (Math.round(barre.getBoundingClientRect().height) + 12) + 'px';
    }
    document.body.appendChild(b);
  }

  window.luxConsent = { ouvrir: ouvrir };
  var choix = lireChoix();
  if (choix !== 'granted' && choix !== 'denied') {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ouvrir);
    else ouvrir();
  }
})();
