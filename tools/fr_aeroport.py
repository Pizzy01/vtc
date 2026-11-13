"""Crée /fr/transfert-aeroport-geneve/ à partir de la page anglaise de l'aéroport (textes français natifs),
relie les pages FR et EN, sitemap, redirections. Aucun identifiant Google touché."""
import os, re
os.chdir('/home/claude/vtc')
src = open('/home/claude/outils/fr_pages.py', encoding='utf-8').read()
exec(src[:src.index('PAGES = {')])          # details(), faq_html(), faq_ld(), COMMON, ATTR, CARS, A(), L(), U_*
exec(src[src.index('FR_NAV ='):src.index('for url, c in PAGES.items():')])   # FR_NAV, NAV_RX, lang_link, hreflang
cp = open('/home/claude/outils/fr_copy.py', encoding='utf-8').read()
ns = {}; exec(cp[cp.index('ALL={'):cp.index('PAGE={')], ns); ALLFR = {k: v for k, v in ns['ALL'].items() if v}

U_AIR = '/fr/transfert-aeroport-geneve/'
AIR = {
 'Geneva airport transfer · Private chauffeur': 'Transfert aéroport Genève · Chauffeur privé',
 'Geneva Airport.': 'Aéroport de Genève.',
 'Already handled.': 'Tout est prévu.',
 'Your chauffeur waits at arrivals. Fixed price from CHF 100.': 'Votre chauffeur vous attend à la sortie. Prix ferme dès CHF 100.',
 'See prices': 'Voir les tarifs',
 'Flight tracked.': 'Votre vol, suivi.',
 'Early or late, we adjust.': 'En avance ou en retard, nous nous adaptons.',
 '60 minutes on us.': '60 minutes d\'attente offertes.',
 'Baggage claim at your pace.': 'Le temps de récupérer vos bagages.',
 'Your name, at arrivals.': 'Votre nom, à la sortie.',
 'Then straight to the car.': 'Puis directement à la voiture.',
 'From the airport': 'De l\'aéroport',
 'to anywhere.': 'jusqu\'à votre porte.',
 'E-CLASS · 3 PAX': 'CLASSE E · 3 PASSAGERS',
 '&#160;&#160;&#160; V-CLASS · 7 PAX': '&#160;&#160;&#160; CLASSE V · 7 PASSAGERS',
 'Geneva city': 'Genève ville',
 'Prices from. Fixed price confirmed before you ride. Night, weekend and tolls always included. Other destinations on request.':
   'Tarifs de base. Le prix est ferme et confirmé avant le départ. Nuit, week-end et péages inclus. Autres destinations sur demande.',
 'Family of five?': 'En famille, à cinq ?',
 'Skis included.': 'Les skis aussi.',
 'Landing soon?': 'Vous atterrissez bientôt ?',
 'Send your flight.': 'Envoyez-nous votre vol.',
 'Get my price': 'Recevoir mon prix',
}
ATTR2 = {'alt="Chauffeur waiting beside the open rear door of a black sedan at Geneva Airport"':
         'alt="Chauffeur attendant près de la portière arrière ouverte d\'une berline noire à l\'aéroport de Genève"'}
TITLE = 'Transfert aéroport Genève dès CHF 100 | Prosper &amp; Co.'
DESC = 'Chauffeur privé depuis l\'aéroport de Genève vers votre hôtel, votre domicile ou votre station de ski. Vol suivi, accueil à la sortie, prix ferme dès CHF 100.'
DET = ("Transfert aéroport Genève,<br>en détail.", [
 ("L'accueil", "Votre chauffeur suit votre vol et vous attend à la sortie des arrivées de l'aéroport de Genève, une pancarte à votre nom. 60 minutes d'attente sont comprises : vous récupérez vos bagages sans vous presser."),
 ("L'aviation privée", "Vous arrivez en jet privé ? Votre chauffeur vous attend au terminal d'aviation privée de Genève. Même service à Zurich."),
 ("Les véhicules", CARS),
 ("Les destinations", "Genève ville dès CHF 100, Lausanne dès CHF 180, Montreux dès CHF 290. Les stations de ski : Megève, Chamonix, Verbier, Courchevel, Zermatt. Le détail est dans la page " + L('/ski-transfers/', 'transferts ski') + "."),
 ("Le prix", "Un prix ferme, confirmé avant le départ. Nuit, week-end et péages sont compris : rien ne s'ajoute ensuite. Le vol est suivi : l'heure de prise en charge suit votre atterrissage."),
 ("Après l'arrivée", "Besoin d'une voiture pendant votre séjour ? " + L(U_HOUR, 'Chauffeur à disposition') + " à l'heure, " + L(U_BIZ, 'chauffeur privé business') + " pour vos rendez-vous, " + L(U_DIP, 'délégations') + " pour les visites officielles."),
])
FAQ = [
 ("Combien coûte un transfert depuis l'aéroport de Genève ?", "Dès CHF 100 pour Genève ville en Mercedes Classe E, CHF 120 en Classe V. Lausanne dès CHF 180, Montreux dès CHF 290, Verbier dès CHF 500. Le prix est ferme et confirmé avant le départ."),
 ("Que se passe-t-il si mon vol a du retard ?", "Votre vol est suivi : votre chauffeur ajuste l'heure de prise en charge à votre atterrissage. 60 minutes d'attente sont comprises."),
 ("Où le chauffeur m'attend-il ?", "À la sortie des arrivées de l'aéroport de Genève, avec une pancarte à votre nom. Pour les jets privés, au terminal d'aviation privée."),
 ("Pouvez-vous aller directement à une station de ski ?", "Oui. Verbier, Zermatt, Courchevel, Chamonix et Megève, avec de la place pour les skis en Mercedes Classe V. Voir les " + A('/ski-transfers/', 'transferts ski') + "."),
 ("Comment réserver ?", "Envoyez votre numéro de vol, votre destination et le nombre de passagers par le formulaire ou sur " + A_WA + ". Nous répondons avec un prix ferme en moins d'une heure, de 7 h à 23 h."),
]
FR_NAV2 = '<a class="ps-navlink" href="%s">Aéroport</a>\n        ' % U_AIR + FR_NAV

def tr(body, m):
    for old, new in sorted(m.items(), key=lambda kv: -len(kv[0])):
        body = re.sub(r'>(\s*)' + re.escape(old) + r'(\s*)<', lambda mm: '>' + mm.group(1) + new + mm.group(2) + '<', body)
    return body

# ---------- la nouvelle page ----------
s = open('geneva-airport-transfer/index.html', encoding='utf-8').read()
s = re.sub(r'  <section id="details".*?</section>\n\n', '', s, flags=re.S)
s = re.sub(r'  <section id="faq".*?</section>\n\n', '', s, flags=re.S)
s = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage".*?</script>\n', '', s, flags=re.S)
s = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@graph".*?</script>\n', '', s, flags=re.S)
assert 'FAQPage' not in s and '@graph' not in s
s = s.replace('<html lang="en">', '<html lang="fr">').replace('content="en_GB"', 'content="fr_CH"')
s = re.sub(r'<title>.*?</title>', '<title>%s</title>' % TITLE, s, count=1)
for k, v in (('name="description"', DESC), ('property="og:description"', DESC), ('property="og:title"', TITLE.replace(' | ', ' · '))):
    s = re.sub(r'(<meta %s content=")[^"]*' % k, lambda m: m.group(1) + v, s, count=1)
s = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s%s">\n%s' % (BASE, U_AIR, hreflang('/geneva-airport-transfer/', U_AIR).rstrip('\n')), s, count=1)
s = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + BASE + U_AIR, s, count=1)
s = re.sub(r'(?:<a class="ps-navlink[^"]*" href="[^"]*"[^>]*>[^<]*</a>\s*)+', lambda m: FR_NAV2 + lang_link('/geneva-airport-transfer/', 'en'), s, count=1)
head, body = s[:s.index('<body')], s[s.index('<body'):]
m = dict(COMMON); m.update(AIR); body = tr(body, m); body = tr(body, ALLFR)
for a, b in list(ATTR.items()) + list(ATTR2.items()): body = body.replace(a, b)
s = head + body
s = s.replace('href="/#quote"', 'href="/fr/#quote"').replace('action="/#quote"', 'action="/fr/#quote"')
s = s.replace('href="/chauffeur-by-the-hour/"', 'href="%s"' % U_HOUR).replace('href="/corporate-chauffeur-geneva/"', 'href="%s"' % U_BIZ).replace('href="/geneva-airport-transfer/" style', 'href="%s" style' % U_AIR)
s = s.replace('<a href="/" style="display: flex; align-items: center; gap: 12px; color: #f5f1e8">', '<a href="/fr/" style="display: flex; align-items: center; gap: 12px; color: #f5f1e8">')
s = s.replace('<a href="/wef-davos-chauffeur/" style="color: #8a857c">WEF Davos</a></nav>', '<a href="%s" style="color: #8a857c">Délégations</a><a href="/wef-davos-chauffeur/" style="color: #8a857c">WEF Davos</a></nav>' % U_DIP)
assert s.count('  <section id="contact"') == 1
s = s.replace('  <section id="contact"', details(*DET) + faq_html(FAQ) + '  <section id="contact"')
s = s.replace('</head>', faq_ld(FAQ) + '</head>', 1)
os.makedirs('fr/transfert-aeroport-geneve', exist_ok=True)
open('fr/transfert-aeroport-geneve/index.html', 'w', encoding='utf-8').write(s)
print('écrit', U_AIR)

# ---------- autres pages FR : lien Aéroport dans le menu, liens aéroport vers la page FR ----------
for p in ['fr/index.html', 'fr/chauffeur-prive-business-geneve/index.html', 'fr/chauffeur-a-disposition-geneve/index.html', 'fr/chauffeur-prive-diplomate-geneve/index.html']:
    t = open(p, encoding='utf-8').read()
    if U_AIR not in t.split('ps-lang')[0]:
        t, n = re.subn(r'(<a class="ps-navlink" href="/fr/chauffeur-prive-business-geneve/">)', '<a class="ps-navlink" href="%s">Aéroport</a>\n        \\1' % U_AIR, t, count=1); assert n == 1, p
    t = t.replace('href="/geneva-airport-transfer/"', 'href="%s"' % U_AIR)
    open(p, 'w', encoding='utf-8').write(t)
# ---------- page EN : lien FR + hreflang ----------
p = 'geneva-airport-transfer/index.html'; t = open(p, encoding='utf-8').read()
t = t.replace('<a class="ps-navlink ps-lang" href="/fr/" hreflang="fr" lang="fr">FR</a>', '<a class="ps-navlink ps-lang" href="%s" hreflang="fr" lang="fr">FR</a>' % U_AIR)
if 'hreflang="x-default"' not in t:
    t, n = re.subn(r'(<link rel="canonical" href="[^"]*">\n)', lambda mm: mm.group(1) + hreflang('/geneva-airport-transfer/', U_AIR), t, count=1); assert n == 1
open(p, 'w', encoding='utf-8').write(t)
# ---------- sitemap ----------
sm = open('sitemap.xml', encoding='utf-8').read()
if BASE + U_AIR + '<' not in sm:
    sm = sm.replace('</urlset>', '  <url>\n    <loc>%s%s</loc>\n    <lastmod>2026-11-13</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n</urlset>' % (BASE, U_AIR))
open('sitemap.xml', 'w', encoding='utf-8').write(sm)
# ---------- redirections ----------
r = open('redirects.csv', encoding='utf-8').read()
r = r.replace('/fr/transfert-aeroport-geneve/,/geneva-airport-transfer/\n', '')
r = r.replace('/fr/service/transfert-aeroport-geneve/,/geneva-airport-transfer/', '/fr/service/transfert-aeroport-geneve/,' + U_AIR)
r = r.replace('/fr/combien-coute-reellement-un-chauffeur-prive-a-geneve/,/geneva-airport-transfer/', '/fr/combien-coute-reellement-un-chauffeur-prive-a-geneve/,' + U_AIR)
r = r.replace('chauffeur-prive-diplomate-geneve)/?$).+$,/fr/', 'chauffeur-prive-diplomate-geneve|transfert-aeroport-geneve)/?$).+$,/fr/')
assert 'transfert-aeroport-geneve)/?$' in r
open('redirects.csv', 'w', encoding='utf-8').write(r)
print('fini')
