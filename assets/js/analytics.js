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
})();
