"""16 nov. 2026 : Méribel, Val d'Isère, Tignes sur /ski-transfers/ + nouvelle page /fr/transferts-ski/.
Prix = grille de Prosper (hors Suisse 3,50 CHF/km Classe E, 4,00 CHF/km Classe V), validés par Issa :
Méribel 530 / 600, Val d'Isère 610 / 700, Tignes 610 / 700. Rejouable une seule fois (assertions)."""
import os, re, json, html
os.chdir('/home/claude/vtc')
B = 'https://www.lux-taxi.com'
def rd(p): return open(p, encoding='utf-8').read()
def wr(p, s):
    os.makedirs(os.path.dirname(p) or '.', exist_ok=True); open(p, 'w', encoding='utf-8').write(s)
def rep(s, a, b, n=1):
    assert s.count(a) == n, (a[:80], s.count(a)); return s.replace(a, b)

EN = 'ski-transfers/index.html'
s = rd(EN)

# ---------- 1. page anglaise ----------
T_EN = "Geneva Airport Transfer to Verbier, Chamonix, Méribel, Val d'Isère, Tignes &amp; Courchevel"
D_EN = "Private ski transfers from Geneva Airport to Verbier, Chamonix, Méribel, Val d'Isère, Tignes, Courchevel and Zermatt. Fixed prices, V-Class for 7. From CHF 250."
assert len(html.unescape(D_EN)) <= 160, len(D_EN)
s = re.sub(r'<title>.*?</title>', '<title>%s</title>' % T_EN, s, 1)
s = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + D_EN.replace("'", "&#39;") if False else m.group(1) + D_EN, s, 1)
s = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + D_EN, s, 1)
s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + T_EN + ' · Prosper &amp; Co.', s, 1)
HREF = ('  <link rel="alternate" hreflang="en" href="%s/ski-transfers/">\n'
        '  <link rel="alternate" hreflang="fr" href="%s/fr/transferts-ski/">\n'
        '  <link rel="alternate" hreflang="x-default" href="%s/ski-transfers/">\n') % (B, B, B)
s = rep(s, '  <link rel="canonical" href="%s/ski-transfers/">\n' % B, '  <link rel="canonical" href="%s/ski-transfers/">\n' % B + HREF)
s = rep(s, '<a class="ps-navlink ps-lang" href="/fr/" hreflang="fr" lang="fr">FR</a>',
        '<a class="ps-navlink ps-lang" href="/fr/transferts-ski/" hreflang="fr" lang="fr">FR</a>')
s = rep(s, '>Geneva ski transfers · Verbier · Zermatt · Courchevel</h1>',
        ">Geneva Airport transfer to Verbier · Chamonix · Méribel · Val d'Isère · Tignes · Courchevel</h1>")

ROW = ('      <div style="display: grid; grid-template-columns: 1fr auto auto; gap: 24px; align-items: baseline; padding: 22px 0; border-top: 1px solid rgba(255,255,255,0.10)">'
       '<span style="font-size: clamp(20px, 2.2vw, 28px); font-weight: 500; letter-spacing: -0.02em">%s</span>'
       '<span style="font-size: 17px; color: #c6a96b; min-width: 92px; text-align: right">CHF %d</span>'
       '<span class="ps-hidem" style="font-size: 17px; color: #8a857c; min-width: 92px; text-align: right">CHF %d</span></div>\n')
NEW = [("Méribel", 530, 600), ("Val d'Isère", 610, 700), ("Tignes", 610, 700)]
zer = '      <div style="display: grid; grid-template-columns: 1fr auto auto; gap: 24px; align-items: baseline; padding: 22px 0; border-top: 1px solid rgba(255,255,255,0.10);border-bottom'
s = rep(s, zer, ''.join(ROW % r for r in NEW) + zer)
s = rep(s, "Gstaad, Crans-Montana, Saas-Fee, Méribel, Val d'Isère on request.", "Gstaad, Crans-Montana, Saas-Fee on request.")
s = rep(s, "Chamonix, Megève, Courchevel, Méribel and Val d'Isère. One chauffeur", "Chamonix, Megève, Courchevel, Méribel, Val d'Isère and Tignes. One chauffeur")

Q_EN = "How much is a transfer from Geneva to Méribel, Val d'Isère or Tignes?"
A_EN = "Méribel from CHF 530 in an E-Class and CHF 600 in a V-Class, about 2 hours 15 minutes. Val d'Isère and Tignes from CHF 610 in an E-Class and CHF 700 in a V-Class, about 3 hours, depending on traffic and snow."
DET = ('<details style="border-top: 1px solid rgba(255,255,255,0.10); padding: 22px 0"><summary style="cursor: pointer; font-size: clamp(18px, 2vw, 24px); font-weight: 500; letter-spacing: -0.02em">%s</summary>'
       '<p style="margin: 14px 0 0; font-size: 16px; line-height: 1.6; color: #aaa59b; max-width: 760px">%s</p></details>')
anchor = 'Allow about 2 hours 30 minutes, depending on traffic and snow.</p></details>'
s = rep(s, anchor, anchor + DET % (Q_EN, A_EN))

LD = re.compile(r'<script type="application/ld\+json">(\{"@context": "https://schema.org", "@type": "FAQPage".*?)</script>', re.S)
def add_faq(m, q, a, after):
    j = json.loads(m.group(1)); ents = j['mainEntity']
    i = next(k for k, e in enumerate(ents) if e['name'] == after)
    ents.insert(i + 1, {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + '</script>'
s, n = LD.subn(lambda m: add_faq(m, Q_EN, A_EN, "How much is a transfer from Geneva to Courchevel?"), s); assert n == 1
wr(EN, s)
print(EN, 'ok')

# ---------- 2. page française ----------
FA = rd('fr/transfert-aeroport-geneve/index.html')
f = s
f = rep(f, '<html lang="en">', '<html lang="fr">')
T_FR = "Transferts Privés Aéroport de Genève vers les Stations de Ski : Courchevel, Megève, Verbier, Chamonix, Méribel, Val d'Isère, Tignes, Gstaad &amp; Zermatt"
D_FR = "Transferts privés de l'aéroport de Genève vers Courchevel, Méribel, Val d'Isère, Tignes, Verbier, Chamonix et Zermatt. Tarif forfaitaire garanti dès CHF 250."
assert len(html.unescape(D_FR)) <= 160, len(D_FR)
f = re.sub(r'<title>.*?</title>', '<title>%s</title>' % T_FR, f, 1)
f = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + D_FR, f, 1)
f = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + D_FR, f, 1)
f = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + "Transferts privés Aéroport de Genève vers les stations de ski · Prosper &amp; Co.", f, 1)
f = rep(f, '<link rel="canonical" href="%s/ski-transfers/">' % B, '<link rel="canonical" href="%s/fr/transferts-ski/">' % B)
f = rep(f, '<meta property="og:url" content="%s/ski-transfers/">' % B, '<meta property="og:url" content="%s/fr/transferts-ski/">' % B)
f = rep(f, '<meta property="og:locale" content="en_GB">', '<meta property="og:locale" content="fr_CH">') if '<meta property="og:locale" content="en_GB">' in f else f
# en-tête et pied de page = ceux des pages FR, avec la nouvelle entrée de menu
hdr = lambda x: re.search(r'    <header .*?</header>\n', x, re.S).group(0)
ftr = lambda x: re.search(r'  <footer .*?</nav>\n\n', x, re.S).group(0)
fr_hdr = hdr(FA).replace('href="/geneva-airport-transfer/" hreflang="en"', 'href="/ski-transfers/" hreflang="en"')
f = f.replace(hdr(f), fr_hdr, 1)
f = f.replace(ftr(f), ftr(FA), 1)
assert 'Menu principal' in f and 'Appeler' in f

TR = [
 (">Geneva Airport transfer to Verbier · Chamonix · Méribel · Val d'Isère · Tignes · Courchevel</h1>",
  ">Transferts Privés Aéroport de Genève vers les Stations de Ski : Courchevel, Megève, Verbier, Chamonix, Méribel, Val d'Isère, Tignes, Gstaad &amp; Zermatt</h1>"),
 ('The Alps.<br>', 'Les Alpes.<br>'),
 ('>Door to chalet.<', ">Jusqu'au chalet.<"),
 ('From Geneva Airport to your resort, in Switzerland or France. From CHF 250.',
  "De l'aéroport de Genève à votre station, en Suisse ou en France. Tarif forfaitaire dès CHF 250."),
 ('>Book on WhatsApp<', '>Réserver sur WhatsApp<', 2),
 ('>See resorts', '>Voir les stations'),
 ('>Room for skis.<', '>Place pour les skis.<'),
 ('>V-Class for up to 7, with luggage.<', ">Van Classe V VIP 7 places, avec bagages.<"),
 ('>Both sides of the border.<', '>Des deux côtés de la frontière.<'),
 ('>Switzerland and France, one price.<', '>Suisse et France, un seul prix.<'),
 ('>Straight to the door.<', ">Jusqu'à votre porte.<"),
 ('>Chalet, hotel or lift. Your call.<', '>Chalet, hôtel ou remontées : vous choisissez.<'),
 ('From the airport<br>', "De l'aéroport<br>"),
 ('>to the snow.<', '>à la neige.<'),
 ('>E-CLASS · 3 PAX<', '>CLASSE E · 3 PASSAGERS<'),
 ('&#160;&#160;&#160; V-CLASS · 7 PAX<', '&#160;&#160;&#160; CLASSE V VIP · 7 PASSAGERS<'),
 ('Prices from. Fixed price confirmed before you ride. Night, weekend and tolls always included. Gstaad, Crans-Montana, Saas-Fee on request.',
  "Tarifs de base. Tarif forfaitaire garanti, confirmé avant le départ. Nuit, week-end et péages inclus. Gstaad, Crans-Montana, Saas-Fee sur demande."),
 ('Seven seats.<br>', 'Sept places.<br>'),
 ('>One trip.<', '>Un seul trajet.<'),
 ('Private ski transfers,<br>', 'Transferts privés vers les stations,<br>'),
 ('>in detail.<', '>en détail.<'),
 ('<h3>Swiss resorts</h3><p>Private transfers from Geneva Airport to Verbier, Zermatt (via Täsch), Gstaad, Crans-Montana, Saas-Fee and Villars-sur-Ollon.</p>',
  "<h3>Stations suisses</h3><p>Transferts privés depuis l'aéroport de Genève vers Verbier, Zermatt (via Täsch), Gstaad, Crans-Montana, Saas-Fee et Villars-sur-Ollon.</p>"),
 ("<h3>French resorts</h3><p>Chamonix, Megève, Courchevel, Méribel, Val d'Isère and Tignes. One chauffeur across the border, one fixed price.</p>",
  "<h3>Stations françaises</h3><p>Chamonix, Megève, Courchevel, Méribel, Val d'Isère et Tignes. Un seul chauffeur de part et d'autre de la frontière, un tarif forfaitaire fixe.</p>"),
 ('<h3>Private, door to door</h3><p>Not a shared shuttle. Your own car and chauffeur, no other passengers, no other stops. From arrivals straight to your chalet or hotel.</p>',
  "<h3>Privé, de porte à porte</h3><p>Pas une navette partagée : votre voiture et votre chauffeur, sans autres passagers ni autres arrêts. De la sortie des arrivées directement à votre chalet ou à votre hôtel.</p>"),
 ('<h3>The cars</h3><p>Mercedes V-Class VIP for up to 7 passengers with luggage and skis. Mercedes E-Class for up to 3. Mercedes S-Class on request. Child seats on request.</p>',
  "<h3>Les véhicules</h3><p>Van Mercedes Classe V VIP jusqu'à 7 passagers avec bagages et skis. Mercedes Classe E jusqu'à 3 passagers. Mercedes Classe S sur demande. Sièges auto sur demande.</p>"),
 ('<h3>From the airport</h3><p>Your chauffeur waits at arrivals with your name. Your flight is tracked and 60 minutes of waiting are included. See',
  "<h3>Depuis l'aéroport</h3><p>Votre chauffeur vous attend à la sortie des arrivées avec une pancarte nominative. Votre vol est suivi et 60 minutes d'attente sont comprises. Voir"),
 ('<h3>Also from Zurich</h3><p>From Zurich Airport to St. Moritz, Andermatt, Zermatt and Gstaad. For Davos in January, see',
  "<h3>Aussi depuis Zurich</h3><p>De l'aéroport de Zurich vers St-Moritz, Andermatt, Zermatt et Gstaad. Pour Davos en janvier, voir"),
 ('>First run tomorrow?<', '>Première descente demain ?<'),
 ('>Book tonight.<', '>Réservez ce soir.<'),
 ('>Get my price', '>Recevoir mon prix'),
 ('alt="Black luxury van under falling snow"', 'alt="Van noir de luxe sous la neige"'),
 ('alt="Chauffeur\'s gloved hand opening a rear car door"', 'alt="Main gantée du chauffeur ouvrant la portière arrière"'),
 ('alt="Black van in a dark studio"', 'alt="Van noir dans un studio sombre"'),
]
for t in TR:
    a, b = t[0], t[1]; n = t[2] if len(t) > 2 else 1
    f = rep(f, a, b, n)
# lien vers la page aéroport FR
f = re.sub(r'<a href="/geneva-airport-transfer/"([^>]*)>Geneva airport transfer</a>', r'<a href="/fr/transfert-aeroport-geneve/"\1>transfert aéroport Genève</a>', f, 1)
f = f.replace('href="/#quote"', 'href="/fr/#quote"')

FAQ_FR = [
 ("Combien coûte un transfert de l'aéroport de Genève à Verbier ?", "Dès CHF 500 en Mercedes Classe E (jusqu'à 3 passagers) et CHF 580 en Van Classe V VIP (jusqu'à 7). Comptez environ 2 heures de route."),
 ("Comment aller à Zermatt depuis Genève ?", "Zermatt est sans voitures. Nous vous conduisons à Täsch en 3 heures environ, dès CHF 720 en Classe E et CHF 840 en Classe V. De Täsch, la navette ferroviaire rejoint Zermatt en 12 minutes."),
 ("Combien coûte un transfert de Genève à Courchevel ?", "Dès CHF 530 en Classe E et CHF 600 en Classe V. Comptez environ 2 h 30, selon la circulation et la neige."),
 ("Et pour Méribel, Val d'Isère ou Tignes ?", "Méribel dès CHF 530 en Classe E et CHF 600 en Classe V, environ 2 h 15. Val d'Isère et Tignes dès CHF 610 en Classe E et CHF 700 en Classe V, environ 3 heures, selon la circulation et la neige."),
 ("Et pour Chamonix ou Megève ?", "Chamonix dès CHF 300 et Megève dès CHF 250 en Classe E. Les deux stations sont à un peu plus d'une heure de l'aéroport de Genève."),
 ("Y a-t-il de la place pour les skis et les bagages ?", "Oui. Le Van Classe V VIP accueille jusqu'à 7 passagers avec bagages et skis. Dites-nous ce que vous transportez, nous choisissons le bon véhicule."),
 ("Les prix sont-ils fixes ?", "Oui. Tarif forfaitaire garanti, confirmé avant le départ. Nuit, week-end et péages sont toujours compris."),
]
qs = list(re.finditer(r'<details style="border-top.*?</details>', f, re.S))
assert len(qs) == 7, len(qs)
f = f[:qs[0].start()] + ''.join(DET % (html.escape(q, quote=False), a) for q, a in FAQ_FR) + f[qs[-1].end():]
ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ_FR]}, ensure_ascii=False) + '</script>'
f, n = LD.subn(lambda m: ld, f); assert n == 1
# reste-t-il de l'anglais visible ?
body = f[f.find('<body'):]
left = [t.strip() for t in re.findall(r'>([^<>]*)<', body) if re.search(r'\b(the|your|from|and|with|book|price|our)\b', t, re.I)]
print('textes anglais restants :', left)
wr('fr/transferts-ski/index.html', f)
print('fr/transferts-ski/index.html ok')

# ---------- 3. liens des pages FR vers la page ski FR + menu ----------
import glob
for p in glob.glob('fr/*/index.html') + ['fr/index.html']:
    x = rd(p); x0 = x
    x = x.replace('href="/ski-transfers/"', 'href="/fr/transferts-ski/"')
    if '>Stations de Ski</a>\n        <a class="ps-navlink" href="/fr/chauffeur-prive-business-geneve/">' not in x:
        x = rep(x, '<a class="ps-navlink" href="/fr/chauffeur-prive-business-geneve/">Entreprises</a>',
                '<a class="ps-navlink" href="/fr/transferts-ski/">Stations de Ski</a>\n        <a class="ps-navlink" href="/fr/chauffeur-prive-business-geneve/">Entreprises</a>')
    if x != x0: wr(p, x); print(p, 'liens ski FR')

# ---------- 4. sitemap ----------
sm = rd('sitemap.xml')
sm = rep(sm, '<loc>%s/ski-transfers/</loc>\n    <lastmod>2026-11-10</lastmod>' % B, '<loc>%s/ski-transfers/</loc>\n    <lastmod>2026-11-16</lastmod>' % B)
sm = rep(sm, '</urlset>', '  <url>\n    <loc>%s/fr/transferts-ski/</loc>\n    <lastmod>2026-11-16</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n</urlset>' % B)
wr('sitemap.xml', sm)
print('sitemap ok')
