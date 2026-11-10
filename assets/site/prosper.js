/* Prosper & Co. — apparitions au défilement + formulaire de devis */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -10% 0px' });
    document.querySelectorAll('section:not(#top) > *').forEach(function (el) { el.classList.add('ps-reveal'); io.observe(el); });
  }

  var form = document.getElementById('quote-form');
  if (!form) return;
  var status = form.querySelector('.ps-status');
  var btn = form.querySelector('button[type=submit]');
  function say(t, cls) { status.textContent = t; status.className = 'ps-status ' + (cls || ''); }
  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var f = form.elements;
    var contact = (f.contact.value || '').trim();
    var isMail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact);
    if (!f.from.value.trim() || !f.to.value.trim() || !f.when.value || !f.name.value.trim() || !contact) {
      say('Please fill in pick-up, drop-off, date, name and a phone or email.', 'is-err'); return;
    }
    var when = f.when.value.split('T');
    var data = {
      name: f.name.value.trim(), pickup: f.from.value.trim(), dropoff: f.to.value.trim(),
      date: when[0] || '', time: when[1] || '', message: (f.details.value || '').trim(),
      email: isMail ? contact : '', phone: isMail ? '' : contact,
      service: 'Site web — ' + location.pathname, website_check: f.website_check.value
    };
    btn.disabled = true; say('Sending…');
    fetch('/api/contact.php', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
      .then(function (r) { return r.json().catch(function () { return { success: false }; }); })
      .then(function (res) {
        if (res && res.success) {
          say('Thank you. Your request is sent — we reply with a fixed price within the hour (7am–11pm).', 'is-ok');
          form.reset();
          if (window.luxTrack) window.luxTrack('generate_lead', { method: 'form' });
        } else {
          say((res && res.error) || 'Sending failed. Please message us on WhatsApp: +41 76 620 78 50.', 'is-err');
        }
      })
      .catch(function () { say('Sending failed. Please message us on WhatsApp: +41 76 620 78 50.', 'is-err'); })
      .then(function () { btn.disabled = false; });
  });
})();
