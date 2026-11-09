#!/usr/bin/env python3
"""Applique les correctifs SEO (9 nov. 2026) sur la version EN LIGNE du site, sans écraser
les modifications faites directement sur le serveur.

  python3 tools/appliquer_correctifs_serveur.py --cible ~/sites/lux-taxi.com          # à blanc
  python3 tools/appliquer_correctifs_serveur.py --cible ~/sites/lux-taxi.com --ecrire # applique

Ce que fait le script (idempotent : on peut le relancer sans effet de bord) :
  1. .htaccess et sitemap.xml : remplacés par ceux du dépôt (redirections 301, version www)
  2. robots.txt et pages HTML : https://lux-taxi.com -> https://www.lux-taxi.com
  3. Pages HTML : retire la balise Analytics G-KPG7Y6MRC7, ajoute G-E1BTELQ36P + analytics.js
  4. Page Contact : ajoute la canonique et og:url si absentes
  5. Accueil : événement generate_lead sur la réservation WhatsApp
  6. assets/js/analytics.js : copié
"""
import argparse
import re
import shutil
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
OLD_GA = re.compile(
    r'[ \t]*<!-- Google tag \(gtag\.js\) -->\s*'
    r'<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-KPG7Y6MRC7"></script>\s*'
    r'<script>.*?G-KPG7Y6MRC7.*?</script>[ \t]*\n?', re.S)
OLD_GA_LOOSE = re.compile(r'<script[^>]*G-KPG7Y6MRC7[^>]*></script>|<script>(?:(?!</script>).)*G-KPG7Y6MRC7.*?</script>', re.S)
NEW_GA = """  <!-- Google Analytics 4 (G-E1BTELQ36P). Consentement refusé par défaut pour l'UE/EEE et le Royaume-Uni tant qu'il n'y a pas de bannière. -->
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('consent', 'default', {ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', analytics_storage: 'denied',
      region: ['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IE','IT','LV','LT','LU','MT','NL','PL','PT','RO','SK','SI','ES','SE','IS','LI','NO','GB']});
    gtag('consent', 'default', {ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', analytics_storage: 'granted'});
    try { var luxChoix = localStorage.getItem('lux_consent'); if (luxChoix === 'granted' || luxChoix === 'denied') gtag('consent', 'update', {analytics_storage: luxChoix}); } catch (e) {}
    gtag('js', new Date());
    gtag('config', 'G-E1BTELQ36P');
  </script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-E1BTELQ36P"></script>
  <script defer src="/assets/js/analytics.js?v=20261109b"></script>
"""
WA_OPEN = "window.open(`https://wa.me/41766207850?text=${encodeURIComponent(msg)}`, '_blank');"


def www(text):
    return re.sub(r'https?://lux-taxi\.com', 'https://www.lux-taxi.com', text)


def fix_html(path, text):
    notes = []
    t = text
    if 'G-KPG7Y6MRC7' in t:
        t, n = OLD_GA.subn('', t)
        if n == 0:
            t, n = OLD_GA_LOOSE.subn('', t)
        notes.append(f'ancienne balise G-KPG7Y6MRC7 retirée ({n} bloc)')
        if 'G-KPG7Y6MRC7' in t:
            raise SystemExit(f'{path}: G-KPG7Y6MRC7 encore présent, arrêt')
    t2 = www(t)
    if t2 != t:
        notes.append(f'{len(re.findall(r"https?://lux-taxi[.]com", t))} adresse(s) passées en www')
        t = t2
    if 'G-E1BTELQ36P' not in t:
        if t.count('</head>') != 1:
            raise SystemExit(f'{path}: </head> introuvable ou multiple, arrêt')
        t = t.replace('</head>', NEW_GA + '</head>', 1)
        notes.append('balise G-E1BTELQ36P ajoutée')
    if path.name == 'contact.html' and 'rel="canonical"' not in t:
        tag = ('  <link rel="canonical" href="https://www.lux-taxi.com/pages/contact.html"/>\n'
               '  <meta property="og:url" content="https://www.lux-taxi.com/pages/contact.html"/>\n')
        t = t.replace('</head>', tag + '</head>', 1) if 'og:url' not in t else t.replace('</head>', tag.splitlines()[0] + '\n</head>', 1)
        notes.append('canonique ajoutée')
    if path.name == 'index.html' and WA_OPEN in t and "method: 'reservation_whatsapp'" not in t:
        t = t.replace(WA_OPEN, "if (window.luxTrack) window.luxTrack('generate_lead', { method: 'reservation_whatsapp' });\n      " + WA_OPEN, 1)
        notes.append('generate_lead sur la réservation WhatsApp')
    return t, notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cible', required=True)
    ap.add_argument('--ecrire', action='store_true')
    a = ap.parse_args()
    dst = Path(a.cible).expanduser()
    if not (dst / 'index.html').is_file():
        raise SystemExit(f'{dst} ne ressemble pas au site (index.html absent)')
    plan = []
    for name in ['.htaccess', 'sitemap.xml', 'assets/js/analytics.js']:
        s, d = SRC / name, dst / name
        if not d.exists() or d.read_bytes() != s.read_bytes():
            plan.append((d, s.read_bytes(), [f'remplacé par la version du dépôt']))
    rb = dst / 'robots.txt'
    if rb.exists():
        t = rb.read_text(encoding='utf-8')
        if www(t) != t:
            plan.append((rb, www(t).encode('utf-8'), ['sitemap en www']))
    for p in [dst / 'index.html', dst / '404.html', *sorted((dst / 'pages').glob('*.html'))]:
        t = p.read_text(encoding='utf-8')
        t2, notes = fix_html(p, t)
        if t2 != t:
            plan.append((p, t2.encode('utf-8'), notes))
    for d, data, notes in plan:
        print(f'{d.relative_to(dst)} : ' + ' ; '.join(notes))
        if a.ecrire:
            d.parent.mkdir(parents=True, exist_ok=True)
            d.write_bytes(data)
    print(('ÉCRIT' if a.ecrire else 'À BLANC (rien écrit)') + f' : {len(plan)} fichier(s)')


if __name__ == '__main__':
    main()
