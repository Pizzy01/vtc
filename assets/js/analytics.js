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
    fr: { h: 'Votre vie privée', t: 'Nous utilisons des cookies de mesure d’audience (Google Analytics) pour comprendre l’usage du site et l’améliorer. Aucune publicité, aucune revente de vos données. Vous pouvez changer d’avis à tout moment avec le lien « Cookies » en bas de page.', ok: 'Tout accepter', non: 'Refuser' },
    en: { h: 'Your privacy', t: 'We use audience measurement cookies (Google Analytics) to understand how this site is used and improve it. No advertising, no resale of your data. You can change your choice at any time with the “Cookies” link at the bottom of the page.', ok: 'Accept all', non: 'Decline' },
    de: { h: 'Ihre Privatsphäre', t: 'Wir verwenden Cookies zur Reichweitenmessung (Google Analytics), um die Nutzung der Website zu verstehen und sie zu verbessern. Keine Werbung, kein Verkauf Ihrer Daten. Sie können Ihre Wahl jederzeit über den Link „Cookies“ unten auf der Seite ändern.', ok: 'Alle akzeptieren', non: 'Ablehnen' },
    it: { h: 'La tua privacy', t: 'Utilizziamo cookie di misurazione del pubblico (Google Analytics) per capire come viene usato il sito e migliorarlo. Nessuna pubblicità, nessuna vendita dei tuoi dati. Puoi cambiare scelta in qualsiasi momento con il link «Cookies» in fondo alla pagina.', ok: 'Accetta tutto', non: 'Rifiuta' }
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

  // Grand panneau en bas de l'écran sur fond assombri (modèle Blacklane, 11 nov. 2026).
  // « Refuser » reste aussi visible et accessible qu'« Accepter » (règle européenne du consentement).
  function ouvrir() {
    if (document.getElementById('lux-consent')) return;
    var tx = TEXTES[langue()];
    var fond = document.createElement('div');
    fond.id = 'lux-consent';
    fond.style.cssText = 'position:fixed;inset:0;z-index:10000;background:rgba(0,0,0,.55);' +
      'display:flex;align-items:flex-end;justify-content:center';
    var b = document.createElement('div');
    b.setAttribute('role', 'dialog');
    b.setAttribute('aria-modal', 'true');
    b.setAttribute('aria-labelledby', 'lux-consent-titre');
    b.style.cssText = 'width:100%;max-width:640px;box-sizing:border-box;background:#F5F1E8;color:#0B0B0C;' +
      'border-radius:22px 22px 0 0;padding:28px 24px calc(24px + env(safe-area-inset-bottom));' +
      'font:16px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;box-shadow:0 -12px 40px rgba(0,0,0,.35)';
    var marque = document.createElement('div');
    marque.textContent = 'Prosper & Co.';
    marque.style.cssText = 'font:600 30px/1.1 Georgia,"Times New Roman",serif;letter-spacing:-.01em;margin:0 0 14px';
    var h = document.createElement('h2');
    h.id = 'lux-consent-titre';
    h.textContent = tx.h;
    h.style.cssText = 'margin:0 0 8px;font:700 20px/1.25 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#0B0B0C';
    var p = document.createElement('p');
    p.textContent = tx.t;
    p.style.cssText = 'margin:0 0 22px;color:#2a2a2a';
    function bouton(label, principal, valeur) {
      var x = document.createElement('button');
      x.type = 'button';
      x.textContent = label;
      x.style.cssText = 'display:block;width:100%;cursor:pointer;border-radius:12px;padding:16px;margin:0 0 10px;' +
        'font:700 17px/1 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;border:0;' +
        (principal ? 'background:#0B0B0C;color:#F5F1E8' : 'background:#E2DCCF;color:#0B0B0C');
      x.addEventListener('click', function () { enregistrer(valeur); fond.remove(); });
      return x;
    }
    b.appendChild(marque);
    b.appendChild(h);
    b.appendChild(p);
    b.appendChild(bouton(tx.ok, true, 'granted'));
    b.appendChild(bouton(tx.non, false, 'denied'));
    fond.appendChild(b);
    document.body.appendChild(fond);
    try { b.querySelector('button').focus({ preventScroll: true }); } catch (e) {}
  }

  window.luxConsent = { ouvrir: ouvrir };
  var choix = lireChoix();
  if (choix !== 'granted' && choix !== 'denied') {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ouvrir);
    else ouvrir();
  }
})();
