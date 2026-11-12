/* Prosper & Co. — apparitions au défilement + formulaire de devis */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -10% 0px' });
    document.querySelectorAll('section:not(#top) > *').forEach(function (el) { el.classList.add('ps-reveal'); io.observe(el); });
  }

  // Barre WhatsApp / Call : visible seulement après le haut de page (évite le doublon avec les boutons du haut)
  var bar = document.getElementById('mobile-sticky-bar'), top = document.getElementById('top');
  if (bar) {
    if ('IntersectionObserver' in window && top) {
      new IntersectionObserver(function (e) { bar.classList.toggle('is-on', !e[0].isIntersecting); }, { threshold: 0.05 }).observe(top);
    } else { bar.classList.add('is-on'); }
  }

  // Menu (burger) : panneau plein écran construit à partir des liens de l'en-tête
  var burger = document.querySelector('.ps-burger');
  if (burger) {
    var LABELS = { '/geneva-airport-transfer/': ['Airport transfer', 'Geneva · Zurich · Lyon'], '/ski-transfers/': ['Ski transfers', 'Verbier · Courchevel'], '/chauffeur-by-the-hour/': ['By the hour', 'From CHF 80 / hour'], '/corporate-chauffeur-geneva/': ['Corporate', 'Executives · roadshows'], '/wef-davos-chauffeur/': ['WEF Davos', 'January 2027'] };
    var menu = document.createElement('div');
    menu.id = 'ps-menu'; menu.className = 'ps-menu'; menu.setAttribute('role', 'dialog'); menu.setAttribute('aria-modal', 'true'); menu.setAttribute('aria-label', 'Menu');
    var html = '<div class="ps-menutop"><span>Prosper &amp; Co.</span><button type="button" class="ps-menuclose" aria-label="Close menu">×</button></div><nav class="ps-menulinks" aria-label="Services">';
    document.querySelectorAll('header .ps-navlink').forEach(function (a) {
      var h = a.getAttribute('href'), l = LABELS[h] || [a.textContent, ''];
      html += '<a href="' + h + '"' + (location.pathname === h ? ' aria-current="page"' : '') + '>' + l[0] + '<small>' + l[1] + '</small></a>';
    });
    html += '</nav><div class="ps-menucta"><a href="/#quote">Get a quote</a><div><a href="https://wa.me/41766207850">WhatsApp</a><a href="tel:+41766207850">Call</a></div></div>';
    menu.innerHTML = html;
    document.body.appendChild(menu);
    var setMenu = function (open) {
      menu.classList.toggle('is-open', open);
      document.documentElement.classList.toggle('ps-lock', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) menu.querySelector('.ps-menuclose').focus(); else burger.focus();
    };
    burger.addEventListener('click', function () { setMenu(true); });
    menu.querySelector('.ps-menuclose').addEventListener('click', function () { setMenu(false); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) { menu.classList.remove('is-open'); document.documentElement.classList.remove('ps-lock'); burger.setAttribute('aria-expanded', 'false'); } });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && menu.classList.contains('is-open')) setMenu(false); });
  }

  var form = document.getElementById('quote-form');
  if (!form) return;
  var status = form.querySelector('.ps-status');
  var btn = form.querySelector('button[type=submit]');
  var f = form.elements;
  var MSG_FAIL = 'Sending failed. Please message us on WhatsApp: +41 76 620 78 50.';
  function say(t, cls) { status.textContent = t; status.className = 'ps-status ' + (cls || ''); }

  // Date : pas de date passée
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function localNow() { var d = new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()) + 'T' + pad(d.getHours()) + ':' + pad(d.getMinutes()); }
  f.when.min = localNow();

  // Contrôles
  function cleanPhone(v) {
    var c = v.replace(/[\s.\-()\/]/g, '');
    if (c.indexOf('00') === 0) c = '+' + c.slice(2);
    var ok = /^\+[1-9]\d{7,14}$/.test(c) || /^0[1-9]\d{8}$/.test(c);
    if (ok && new Set(c.replace(/\D/g, '').split('')).size < 3) ok = false;
    return ok ? c : '';
  }
  var TYPO = { 'gmial.com': 'gmail.com', 'gmai.com': 'gmail.com', 'gmail.co': 'gmail.com', 'gmail.fr': 'gmail.com', 'gamil.com': 'gmail.com', 'hotmial.com': 'hotmail.com', 'hotmail.co': 'hotmail.com', 'outlok.com': 'outlook.com', 'yahoo.co': 'yahoo.com', 'iclod.com': 'icloud.com', 'icloud.co': 'icloud.com', 'bluewin.c': 'bluewin.ch' };
  function checkEmail(v) {
    if (!v) return '';
    if (!/^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(v)) return 'This email address does not look valid.';
    var dom = v.split('@')[1].toLowerCase();
    if (TYPO[dom]) return 'Did you mean ' + v.split('@')[0] + '@' + TYPO[dom] + '?';
    return '';
  }
  var rules = {
    from: function (v) { return v.length < 2 ? 'Please enter a pick-up place — a hotel name is enough.' : ''; },
    to: function (v) { return v.length < 2 ? 'Please enter a drop-off place — a hotel or resort name is enough.' : ''; },
    when: function (v) { if (!v) return 'Please choose a date and time.'; return new Date(v).getTime() < Date.now() - 5 * 60000 ? 'Please choose a date and time in the future.' : ''; },
    name: function (v) { return v.length < 2 ? 'Please enter your name.' : ''; },
    phone: function (v) { if (!v) return 'We need a phone number to reach you on the day.'; return cleanPhone(v) ? '' : 'Please enter a valid phone number with country code, e.g. +41 79 123 45 67.'; },
    email: checkEmail
  };
  function mark(name, msg) {
    var box = f[name] && f[name].closest('.ps-field'); if (!box) return;
    box.classList.toggle('is-bad', !!msg);
    box.classList.toggle('is-ok', !msg && !!f[name].value.trim());
    f[name].setAttribute('aria-invalid', msg ? 'true' : 'false');
    box.querySelector('.ps-err').textContent = msg || '';
    box.querySelector('.ps-err').classList.toggle('is-hint', /^Did you mean/.test(msg || ''));
  }
  function check(name) { var m = rules[name]((f[name].value || '').trim()); mark(name, m); return m; }
  Object.keys(rules).forEach(function (n) {
    f[n].addEventListener('blur', function () { if (f[n].value.trim() || n === 'phone') check(n); });
    f[n].addEventListener('input', function () { if (f[n].closest('.ps-field').classList.contains('is-bad')) check(n); });
  });
  // Clic sur la suggestion « Did you mean … »
  f.email.closest('.ps-field').querySelector('.ps-err').addEventListener('click', function () {
    var m = /Did you mean (\S+)\?/.exec(this.textContent); if (m) { f.email.value = m[1]; check('email'); }
  });
  f.from.addEventListener('input', function () { if (f.lat.value && f.from.value !== 'My current location (GPS)') { f.lat.value = ''; f.lng.value = ''; } });

  // Devis rapide du haut de l'accueil : reporte les 3 champs dans le formulaire complet
  var quick = document.getElementById('quick-quote');
  if (quick) {
    var q = function (n) { return quick.querySelector('[data-q="' + n + '"]'); };
    q('when').min = localNow();
    quick.addEventListener('submit', function (ev) {
      ev.preventDefault();
      ['from', 'to', 'when'].forEach(function (n) { var v = q(n).value.trim(); if (v) { f[n].value = v; check(n); } });
      var next = !f.from.value.trim() ? f.from : !f.to.value.trim() ? f.to : !f.when.value ? f.when : f.name;
      document.getElementById('quote').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
      setTimeout(function () { next.focus({ preventScroll: true }); }, reduce ? 0 : 700);
      if (window.luxTrack) window.luxTrack('begin_quote', { method: 'hero' });
    });
  }


  // « Use my location » : position envoyée seulement si le client appuie sur le bouton
  var geo = form.querySelector('.ps-geo');
  if (geo) {
    if (!('geolocation' in navigator)) { geo.hidden = true; }
    geo.addEventListener('click', function () {
      geo.setAttribute('aria-busy', 'true'); geo.textContent = 'Locating…';
      navigator.geolocation.getCurrentPosition(function (p) {
        f.lat.value = p.coords.latitude.toFixed(6); f.lng.value = p.coords.longitude.toFixed(6);
        f.from.value = 'My current location (GPS)'; check('from');
        geo.removeAttribute('aria-busy'); geo.textContent = 'Location added ✓';
      }, function () {
        geo.removeAttribute('aria-busy'); geo.textContent = 'Use my location';
        mark('from', 'Location not available — please type your hotel or address.');
      }, { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 });
    });
  }

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var first = null;
    Object.keys(rules).forEach(function (n) { if (check(n) && !first) first = f[n]; });
    if (first) { say('Please check the highlighted fields.', 'is-err'); first.focus({ preventScroll: true }); first.scrollIntoView({ behavior: 'smooth', block: 'center' }); return; }
    var when = f.when.value.split('T');
    var data = {
      name: f.name.value.trim(), pickup: f.from.value.trim(), dropoff: f.to.value.trim(),
      date: when[0] || '', time: when[1] || '', message: (f.details.value || '').trim(),
      phone: cleanPhone(f.phone.value.trim()), email: f.email.value.trim(),
      lat: f.lat.value, lng: f.lng.value,
      service: 'Site web — ' + location.pathname, website_check: f.website_check.value
    };
    btn.disabled = true; say('Sending…');
    fetch('/api/contact.php', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
      .then(function (r) { return r.json().catch(function () { return { success: false }; }); })
      .then(function (res) {
        if (res && res.success) {
          say('Thank you. Your request is sent — we reply with a fixed price within the hour (7am–11pm).', 'is-ok');
          form.reset(); f.lat.value = ''; f.lng.value = ''; f.when.min = localNow();
          form.querySelectorAll('.ps-field').forEach(function (b) { b.classList.remove('is-ok', 'is-bad'); });
          if (geo) geo.textContent = 'Use my location';
          if (window.luxTrack) window.luxTrack('generate_lead', { method: 'form' });
        } else if (res && res.fields) {
          Object.keys(res.fields).forEach(function (n) { mark(n, res.fields[n]); });
          say(res.error || 'Please check the highlighted fields.', 'is-err');
        } else {
          say((res && res.error) || MSG_FAIL, 'is-err');
        }
      })
      .catch(function () { say(MSG_FAIL, 'is-err'); })
      .then(function () { btn.disabled = false; });
  });
})();
