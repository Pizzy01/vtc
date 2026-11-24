"""Lot du 24 nov. 2026 (SEO) — à lancer depuis la racine du dépôt, puis tools/schema_geo.py et tools/redirects.py build.

1. Page WEF anglaise renforcée (blocs « in detail » et questions en plus, hreflang EN/FR, lien FR).
2. Nouvelle page française /fr/chauffeur-wef-davos/ (même mise en page, texte français natif).
3. Liens WEF des pages FR vers la page FR.
4. Liens « EN » corrigés sur 3 pages FR qui pointaient vers elles-mêmes.
5. hreflang en double retiré sur /fr/transfert-aeroport-geneve/.
6. /fr/ : un bloc et une question en plus sur le chauffeur privé de luxe.
7. Sitemap (19 pages), redirects.csv (page FR autorisée), fichier-clé IndexNow.
Seules des promesses confirmées par Prosper : 24/7, WhatsApp < 10 min, grille 90/110/140, accès tarmac à Genève, CHF/EUR/USD.
"""
import html
import json
import os
import re

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
B = 'https://www.lux-taxi.com'
EN = 'wef-davos-chauffeur/index.html'
FR_SLUG = '/fr/chauffeur-wef-davos/'
FR = 'fr/chauffeur-wef-davos/index.html'

def rd(p): return open(p, encoding='utf-8').read()
def wr(p, s):
    os.makedirs(os.path.dirname(p) or '.', exist_ok=True)
    open(p, 'w', encoding='utf-8').write(s)
def once(s, old, new, label):
    assert s.count(old) == 1, f'{label}: {s.count(old)} occurrence(s)'
    return s.replace(old, new)

DET = '<details style="border-top: 1px solid rgba(255,255,255,0.10); padding: 22px 0"><summary style="cursor: pointer; font-size: clamp(18px, 2vw, 24px); font-weight: 500; letter-spacing: -0.02em">{q}</summary><p style="margin: 14px 0 0; font-size: 16px; line-height: 1.6; color: #aaa59b; max-width: 760px">{a}</p></details>'
def det(q, a): return DET.format(q=q, a=a)
def blk(h, p): return f'<div><h3>{h}</h3><p>{p}</p></div>'

FAQ_LD = re.compile(r'<script type="application/ld\+json">(\{"@context": "https://schema.org", "@type": "FAQPage".*?)</script>', re.S)
def refaire_faq(s):
    """Recalcule le bloc FAQPage à partir des questions visibles de la page."""
    qa = re.findall(r'<summary[^>]*>(.*?)</summary><p[^>]*>(.*?)</p>', s, re.S)
    clean = lambda t: html.unescape(re.sub(r'<[^>]+>', '', t)).strip()
    j = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": clean(q), "acceptedAnswer": {"@type": "Answer", "text": clean(a)}} for q, a in qa]}
    assert len(FAQ_LD.findall(s)) == 1
    return FAQ_LD.sub(lambda m: '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + '</script>', s)

def hreflang(en, fr):
    return (f'\n  <link rel="alternate" hreflang="en" href="{B}{en}">'
            f'\n  <link rel="alternate" hreflang="fr" href="{B}{fr}">'
            f'\n  <link rel="alternate" hreflang="x-default" href="{B}{en}">')

# ---------------------------------------------------------------- 1. page WEF anglaise
en = rd(EN)
en_orig = en
canon_en = f'<link rel="canonical" href="{B}/wef-davos-chauffeur/">'
if 'hreflang="fr" href="' + B + FR_SLUG not in en:
    en = once(en, canon_en, canon_en + hreflang('/wef-davos-chauffeur/', FR_SLUG), 'EN hreflang')
en = once(en, '<a class="ps-navlink ps-lang" href="/fr/" hreflang="fr"', f'<a class="ps-navlink ps-lang" href="{FR_SLUG}" hreflang="fr"', 'EN lien FR')
EN_BLOCS = (
    blk('Private jets', 'Arriving by private jet? Your chauffeur meets you at the private aviation terminal in Zurich or Geneva. In Geneva, we have tarmac access. See <a href="/private-aviation-jet-transfer-geneva/">private aviation transfers</a>.')
    + blk('Winter roads', 'In January the roads to Davos can be snowy. Your chauffeur follows traffic and weather, and moves the pick-up time if needed. You know before you leave.')
    + blk('Bookings and changes', 'One contact, 24/7, on WhatsApp or by phone. A reply in under 10 minutes. Change a time, add a car, send us the new schedule.')
    + blk('Payment', 'One quote for the whole programme, in Swiss francs. Payment in CHF, EUR or USD.')
)
if 'Winter roads' not in en:
    en = once(en, 'Availability is limited in January. Book early.</p></div></div>', 'Availability is limited in January. Book early.</p></div>' + EN_BLOCS + '</div>', 'EN blocs')
EN_FAQ = (
    det('Can you pick us up from a private jet?', 'Yes. Your chauffeur meets you at the private aviation terminal in Zurich or Geneva. In Geneva, we have tarmac access.')
    + det('Can you drive us from Geneva to Davos?', 'Yes. The drive takes about 4 hours 30 minutes. Many guests fly into Geneva and go to Davos by car, without changing at Zurich.')
    + det('Can we pay in euros or dollars?', 'Yes. The quote is in Swiss francs, and you can pay in CHF, EUR or USD.')
)
if 'pick us up from a private jet' not in en:
    en = once(en, 'Mercedes S-Class for executives and Mercedes V-Class VIP for teams and delegations.</p></details></div>',
              'Mercedes S-Class for executives and Mercedes V-Class VIP for teams and delegations.</p></details>' + EN_FAQ + '</div>', 'EN FAQ')
en = refaire_faq(en)
wr(EN, en)

# ---------------------------------------------------------------- 2. page WEF française
# Base : la page anglaise (mise en page), avec en-tête et pied de page français repris de la page business FR.
biz = rd('fr/chauffeur-prive-business-geneve/index.html')
TITLE = 'Chauffeur privé WEF Davos 2027 | Prosper &amp; Co.'
DESC = 'Chauffeur privé pour le Forum économique mondial de Davos, janvier 2027. Mercedes Classe S et Classe V VIP, à la journée ou au transfert, de Zurich ou Genève.'
assert len(html.unescape(TITLE)) <= 60 and len(DESC) <= 160, (len(html.unescape(TITLE)), len(DESC))
fr = en_orig  # repart de la version d'origine pour ne pas traduire deux fois
fr = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@graph".*?</script>\n?', '', fr, flags=re.S)
fr = once(fr, '<html lang="en">', '<html lang="fr">', 'lang')
fr = re.sub(r'<title>.*?</title>', f'<title>{TITLE}</title>', fr)
fr = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', fr)
fr = once(fr, canon_en, f'<link rel="canonical" href="{B}{FR_SLUG}">' + hreflang('/wef-davos-chauffeur/', FR_SLUG), 'FR canonical')
fr = once(fr, f'<meta property="og:url" content="{B}/wef-davos-chauffeur/">', f'<meta property="og:url" content="{B}{FR_SLUG}">', 'og:url')
fr = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="Chauffeur privé WEF Davos 2027 · Prosper &amp; Co.">', fr)
fr = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{DESC}">', fr)
fr = once(fr, '<meta property="og:locale" content="en_GB">', '<meta property="og:locale" content="fr_CH">', 'locale')
hdr_fr = re.search(r'<header .*?</header>', biz, re.S).group(0)
hdr_fr = hdr_fr.replace('<a class="ps-navlink ps-lang" href="/fr/chauffeur-prive-business-geneve/"', '<a class="ps-navlink ps-lang" href="/wef-davos-chauffeur/"')
hdr_fr = hdr_fr.replace('<a class="ps-navlink ps-lang" href="/corporate-chauffeur-geneva/"', '<a class="ps-navlink ps-lang" href="/wef-davos-chauffeur/"')
biz = biz.replace('href="/wef-davos-chauffeur/"', f'href="{FR_SLUG}"')  # pied de page FR : lien WEF vers la page FR
fr = re.sub(r'<header .*?</header>', lambda m: hdr_fr, fr, count=1, flags=re.S)
fr = re.sub(r'<footer.*?</footer>', lambda m: re.search(r'<footer.*?</footer>', biz, re.S).group(0), fr, count=1, flags=re.S)
fr = re.sub(r'<nav id="mobile-sticky-bar".*?</nav>', lambda m: re.search(r'<nav id="mobile-sticky-bar".*?</nav>', biz, re.S).group(0), fr, count=1, flags=re.S)

T = [  # (anglais, français) — remplacements exacts dans le corps
 ('alt="Black chauffeur sedan in a dark studio, golden light along the bodywork"', 'alt="Berline noire avec chauffeur dans un studio sombre, lumière dorée le long de la carrosserie"'),
 ('WEF Davos chauffeur service · January 2027', 'Chauffeur privé WEF Davos · Janvier 2027'),
 ('Davos week,<br>', 'La semaine de Davos,<br>'),
 ('>handled.</span>', '>sans souci.</span>'),
 ('A chauffeur for the whole World Economic Forum week, from Zurich or Geneva. Mercedes S-Class and V-Class VIP.',
  'Un chauffeur pour toute la semaine du Forum économique mondial, depuis Zurich ou Genève. Mercedes Classe S et Classe V VIP.'),
 ('>Book on WhatsApp</a>', '>Réserver sur WhatsApp</a>'),
 ('href="/#quote" class="ps-card" style="font-size: 16px; font-weight: 500">Request availability', 'href="/fr/#quote" class="ps-card" style="font-size: 16px; font-weight: 500">Demander une disponibilité'),
 ('href="/#quote" class="ps-card" style="font-size: 16px; font-weight: 500">Get my price', 'href="/fr/#quote" class="ps-card" style="font-size: 16px; font-weight: 500">Recevoir mon prix'),
 ('alt="Headlight of a black car in a dark studio"', 'alt="Phare d\'une voiture noire dans un studio sombre"'),
 ('>Airport to Davos.<', '>De l\'aéroport à Davos.<'),
 ('>Zurich, Geneva and the private aviation terminals.<', '>Zurich, Genève et les terminaux d\'aviation privée.<'),
 ('>By the day.</span><span', '>À la journée.</span><span'),
 ('>One car, one chauffeur, your schedule all week.<', '>Une voiture, un chauffeur, votre agenda toute la semaine.<'),
 ('>Delegations.<', '>Délégations.<'),
 ('>Several vehicles, one contact, through our network.<', '>Plusieurs véhicules, un seul contact, grâce à notre réseau.<'),
 ('>Davos week.<br>', '>Semaine de Davos.<br>'),
 ('color: #e9e2d3">By the day.</span></h2>', 'color: #e9e2d3">À la journée.</span></h2>'),
 ('PER HOUR · 20 KM INCLUDED', 'À L\'HEURE · 20 KM INCLUS'),
 ('Mercedes E-Class Business · 3 pax', 'Mercedes Classe E Business · 3 pers.'),
 ('Mercedes V-Class VIP Van · 7 pax', 'Mercedes Classe V VIP Van · 7 pers.'),
 ('Mercedes S-Class First Class · 2 pax', 'Mercedes Classe S First Class · 2 pers.'),
 ('from CHF 90 / hour', 'dès CHF 90 / heure'), ('from CHF 110 / hour', 'dès CHF 110 / heure'), ('from CHF 140 / hour', 'dès CHF 140 / heure'),
 ('Hourly rates from. WEF week is quoted as a full programme: car, chauffeur, fuel, tolls and the chauffeur\'s stay included. Availability is limited, book early.',
  'Tarifs horaires de départ. La semaine du WEF fait l\'objet d\'un devis global : voiture, chauffeur, carburant, péages et hébergement du chauffeur compris. Disponibilités limitées, réservez tôt.'),
 ('Zurich Airport. The Congress Centre. Hotel meetings. <span style="color: #6f6a61">Dinners in Klosters. One chauffeur, all week.</span>',
  'L\'aéroport de Zurich. Le Centre des congrès. Les rendez-vous à l\'hôtel. <span style="color: #6f6a61">Les dîners à Klosters. Un seul chauffeur, toute la semaine.</span>'),
 ('alt="Black van in a dark studio"', 'alt="Van noir dans un studio sombre"'),
 ('Room for the team.<br>', 'De la place pour l\'équipe.<br>'),
 ('>And the luggage.<', '>Et les bagages.<'),
 ('WEF Davos chauffeur service,<br>in detail.', 'Chauffeur privé au WEF de Davos,<br>en détail.'),
 ('Questions.</h2>', 'Questions.</h2>'),
 ('Going to Davos?<br>', 'Vous allez à Davos ?<br>'),
 ('>Book before January.<', '>Réservez avant janvier.<'),
]
for a, b in T:
    assert a in fr, 'manque : ' + a[:60]
    fr = fr.replace(a, b)

FR_BLOCS = (
    blk('Le trajet', 'Davos est à environ 2 h 30 de l\'aéroport de Zurich et à environ 4 h 30 de Genève. Votre chauffeur vous attend aux arrivées ou au terminal d\'aviation privée.')
    + blk('La semaine', 'Une voiture et un chauffeur, à la journée, pendant toute la semaine du Forum économique mondial. Votre agenda, vos changements.')
    + blk('Les véhicules', 'Mercedes Classe S pour les dirigeants. Mercedes Classe V VIP pour les équipes et les délégations jusqu\'à 7 personnes, avec les bagages.')
    + blk('Les délégations', 'Plusieurs véhicules coordonnés par un seul contact, grâce à notre réseau de chauffeurs. Voir aussi <a href="/fr/chauffeur-prive-diplomate-geneve/">délégations et diplomatie</a> et <a href="/fr/chauffeur-prive-business-geneve/">chauffeur privé business</a>.')
    + blk('Autour de Davos', 'Rendez-vous à l\'hôtel, dîners à Klosters, soirées. L\'accès aux zones sécurisées dépend de votre accréditation officielle : dites-nous ce que vous avez, nous organisons les trajets en conséquence.')
    + blk('Jets privés', 'Vous arrivez en jet privé ? Votre chauffeur vous attend au terminal d\'aviation privée de Zurich ou de Genève. À Genève, nous avons l\'accès au tarmac. Voir <a href="/fr/transfert-aviation-privee-geneve/">transfert aviation privée</a>.')
    + blk('Routes d\'hiver', 'En janvier, la route de Davos peut être enneigée. Votre chauffeur suit le trafic et la météo, et avance l\'heure de départ si besoin. Vous êtes prévenu avant de partir.')
    + blk('Réservations et changements', 'Un seul contact, 24 h/24, sur WhatsApp ou par téléphone. Réponse en moins de 10 minutes. Une heure à changer, une voiture à ajouter : envoyez-nous le nouveau programme.')
    + blk('Le devis', 'La semaine du WEF fait l\'objet d\'un devis global en francs suisses : voiture, chauffeur, carburant, péages et hébergement du chauffeur compris. Paiement en CHF, EUR ou USD.')
)
fr = re.sub(r'<div class="ps-detail">.*?</div></div>\n', lambda m: '<div class="ps-detail">' + FR_BLOCS + '</div>\n', fr, count=1, flags=re.S)
FR_FAQ = (
    det('Quelle distance entre Davos, Zurich et Genève ?', 'Davos est à environ 2 h 30 de route de l\'aéroport de Zurich et à environ 4 h 30 de Genève, selon le trafic et la météo.')
    + det('Peut-on garder le même chauffeur toute la semaine ?', 'Oui. En réservation à la journée, le même chauffeur et la même voiture restent avec vous toute la semaine du WEF.')
    + det('Organisez-vous le transport des délégations ?', 'Oui. Nous coordonnons plusieurs véhicules pour les délégations et leurs équipes, avec un seul contact pour toutes les réservations.')
    + det('Quand faut-il réserver ?', 'Le plus tôt possible. La demande de chauffeurs à Davos atteint son pic pendant la semaine du WEF, et les disponibilités sont limitées.')
    + det('Quelles voitures utilisez-vous ?', 'Mercedes Classe S pour les dirigeants et Mercedes Classe V VIP pour les équipes et les délégations.')
    + det('Venez-vous chercher les passagers de jets privés ?', 'Oui. Votre chauffeur vous attend au terminal d\'aviation privée de Zurich ou de Genève. À Genève, nous avons l\'accès au tarmac.')
    + det('Pouvez-vous nous conduire de Genève à Davos ?', 'Oui. Le trajet dure environ 4 h 30. Beaucoup de participants arrivent à Genève et rejoignent Davos en voiture, sans changer à Zurich.')
    + det('Peut-on payer en euros ou en dollars ?', 'Oui. Le devis est en francs suisses, et vous pouvez payer en CHF, EUR ou USD.')
)
fr = re.sub(r'(<section id="faq".*?<div style="border-bottom: 1px solid rgba\(255,255,255,0.10\)">).*?(</div>\n  </section>)', lambda m: m.group(1) + FR_FAQ + m.group(2), fr, count=1, flags=re.S)
fr = refaire_faq(fr)
for mot in ['Book on', 'Get a quote', 'Request availability', 'in detail', 'How far', 'Which cars', 'Getting there']:
    assert mot not in re.sub(r'<script.*?</script>', '', fr, flags=re.S), 'anglais restant : ' + mot
wr(FR, fr)

# ---------------------------------------------------------------- 3 et 4. pages FR : liens WEF et liens EN
EN_TWIN = {'fr/chauffeur-a-disposition-geneve/index.html': '/chauffeur-by-the-hour/',
           'fr/transferts-ski/index.html': '/ski-transfers/',
           'fr/chauffeur-prive-business-geneve/index.html': '/corporate-chauffeur-geneva/'}
for root, _, files in os.walk('fr'):
    for f in files:
        if f != 'index.html': continue
        p = os.path.join(root, f)
        if p == FR: continue
        s = rd(p); s0 = s
        s = s.replace('href="/wef-davos-chauffeur/"', f'href="{FR_SLUG}"')
        if p in EN_TWIN:
            self_url = '/' + p[:-len('index.html')]
            s = once(s, f'<a class="ps-navlink ps-lang" href="{self_url}" hreflang="en"', f'<a class="ps-navlink ps-lang" href="{EN_TWIN[p]}" hreflang="en"', 'lien EN ' + p)
        if s != s0: wr(p, s); print('maj', p)

# ---------------------------------------------------------------- 5. hreflang en double
p = 'fr/transfert-aeroport-geneve/index.html'
s = rd(p)
bloc = hreflang('/geneva-airport-transfer/', '/fr/transfert-aeroport-geneve/')
if s.count(bloc) == 2:
    s = s.replace(bloc + bloc, bloc); assert s.count(bloc) == 1; wr(p, s); print('hreflang dédoublé', p)

# ---------------------------------------------------------------- 6. /fr/ : chauffeur privé de luxe
p = 'fr/index.html'
s = rd(p)
LUXE = blk('Chauffeur privé de luxe ou taxi ?', 'Un taxi vous emmène d\'un point à un autre. Un chauffeur privé de luxe vous attend, connaît votre programme et s\'y adapte : une Mercedes Classe S ou Classe V VIP réservée pour vous, un chauffeur en costume, discret, qui parle français et anglais, un prix fixe connu avant de partir. C\'est le service que demandent les dirigeants, les familles et les délégations à Genève.')
if 'Chauffeur privé de luxe ou taxi' not in s:
    s = once(s, '<div class="ps-detail"><div><h3>Les véhicules</h3>', '<div class="ps-detail">' + LUXE + '<div><h3>Les véhicules</h3>', '/fr/ bloc')
Q = det('Quelle différence entre un chauffeur privé de luxe, un taxi et un VTC ?', 'Avec un chauffeur privé de luxe, la voiture et le chauffeur sont réservés pour vous seul : Mercedes Classe S ou Classe V VIP, prix fixe confirmé avant la course, attente comprise dans le programme, un seul contact 24 h/24. Un taxi ou un VTC prend la course suivante, au compteur ou au tarif de l\'application.')
if 'un taxi et un VTC' not in s:
    s = once(s, '<summary style="cursor: pointer; font-size: clamp(18px, 2vw, 24px); font-weight: 500; letter-spacing: -0.02em">Combien coûte un chauffeur privé à Genève ?</summary>',
             '<summary style="cursor: pointer; font-size: clamp(18px, 2vw, 24px); font-weight: 500; letter-spacing: -0.02em">Combien coûte un chauffeur privé à Genève ?</summary>', 'repère')
    i = s.find('Combien coûte un chauffeur privé à Genève ?</summary>')
    i = s.rfind('<details', 0, i)
    s = s[:i] + Q + s[i:]
s = refaire_faq(s)
wr(p, s)

# ---------------------------------------------------------------- 7. sitemap, redirections, IndexNow
s = rd('sitemap.xml')
if FR_SLUG not in s:
    s = s.replace('</urlset>', f'  <url>\n    <loc>{B}{FR_SLUG}</loc>\n    <lastmod>2026-11-24</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n</urlset>')
for u in ['/wef-davos-chauffeur/', '/fr/']:
    s = re.sub(r'(<loc>' + re.escape(B + u) + r'</loc>\n    <lastmod>)[^<]*', r'\g<1>2026-11-24', s)
wr('sitemap.xml', s)
r = rd('redirects.csv')
if 'chauffeur-wef-davos' not in r:
    r = once(r, '|transferts-ski)/?$', '|transferts-ski|chauffeur-wef-davos)/?$', 'liste FR')
    wr('redirects.csv', r)
KEY = '6f1c2d9a8e4b47c3a5d0e9f2b7c41a68'
wr(f'{KEY}.txt', KEY)
print('ok —', FR, '— clé IndexNow', KEY)
