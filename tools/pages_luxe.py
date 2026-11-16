"""16 nov. : 3 pages haute valeur EN + FR (aviation privée, internats et cliniques, flotte Classe V / Classe S).
Coquilles : corporate-chauffeur-geneva (EN) et fr/chauffeur-prive-business-geneve (FR). Aucun identifiant Google touché."""
import os, re, json, html
os.chdir('/home/claude/vtc')
src = open('tools/fr_pages_src.py', encoding='utf-8').read() if os.path.exists('tools/fr_pages_src.py') else open('/home/claude/outils/fr_pages.py', encoding='utf-8').read()
exec(src[:src.index('PAGES = {')])
exec(src[src.index('FR_NAV ='):src.index('for url, c in PAGES.items():')])
SER = "font-family: 'Cormorant Garamond', Georgia, serif; font-style: italic; font-weight: 400; letter-spacing: -0.02em; color: #e9e2d3"
IMG = {'aero': ('hd-aeroport', "Chauffeur waiting beside the open rear door of a black sedan at Geneva Airport", "Chauffeur attendant près de la portière arrière ouverte d'une berline noire à l'aéroport de Genève"),
       'berline': ('hd-berline', "Black chauffeur sedan in a dark studio, golden light along the bodywork", "Berline noire avec chauffeur dans un studio sombre, lumière dorée sur la carrosserie"),
       'van': ('hd-van', "Black luxury van under falling snow", "Van de luxe noir sous la neige")}
W = '24/7 Operations &amp; Flight Monitoring — Priority WhatsApp Dispatch in under 10 minutes.'
WF = 'Opérations 24 h/24, 7 j/7 et suivi des vols — réponse prioritaire sur WhatsApp en moins de 10 minutes.'
EN_A, FR_A = '/private-aviation-jet-transfer-geneva/', '/fr/transfert-aviation-privee-geneve/'
EN_B, FR_B = '/swiss-boarding-schools-medical-chauffeur/', '/fr/chauffeur-internats-cliniques-suisse/'
EN_C, FR_C = '/mercedes-v-class-vip-s-class-fleet-geneva/', '/fr/flotte-mercedes-classe-v-classe-s-geneve/'
def Ae(h, t): return '<a href="%s" style="color: #c6a96b">%s</a>' % (h, t)

PAGES = [
 # ---------------- A : aviation privée ----------------
 dict(url=EN_A, twin=FR_A, lang='en', img='aero',
  title='Private Jet Transfer Geneva · Tarmac &amp; FBO | Prosper &amp; Co.',
  desc='Private aviation chauffeur in Geneva: C3 terminal, Jet Aviation, TAG Aviation, Signature, plus Sion and Zurich. Tarmac access, absolute discretion, 24/7.',
  kicker='Private jet transfer · Geneva · Tarmac &amp; FBO', big=('Wheels down.', 'Door open.'),
  sub='Your chauffeur waits at the aircraft or the private terminal. Geneva, Sion, Zurich. ' + '24/7.',
  li=[('At the aircraft.', 'Tarmac access at Geneva, at the foot of the stairs when the FBO allows it.'),
      ('Every FBO.', 'C3 private aviation terminal, Jet Aviation, TAG Aviation, Signature Flight Support.'),
      ('No names, no photos.', 'Absolute discretion for principals, diplomats and family offices.')],
  rates=('Private aviation.', 'Fixed price.'), note='Hourly rates from. Jet arrivals: fixed transfer price confirmed before landing, airport fees passed on at cost. Sion and Zurich on quote.',
  stmt=('UHNW families. Heads of state. Family offices. Crews. ', 'From the stairs to the chalet.'), mount=('Flight tracked.', 'Car ready.'),
  contact=('Wheels up soon?', 'Send your tail number.'),
  det=("Private jet transfer in Geneva,<br>in detail.", [
   ("Tarmac and FBO", "We meet you at the aircraft at Geneva Airport when the FBO and handling agent allow airside access, or inside the private aviation terminal: C3, Jet Aviation, TAG Aviation and Signature Flight Support."),
   ("Sion and Zurich", "The same service at Sion Airport for Verbier, Crans-Montana and Zermatt, and at Zurich Airport for Davos, Gstaad or a business programme in Zurich."),
   ("Flight monitoring", W + " Early or late, your chauffeur follows the flight and adjusts."),
   ("The cars", "Mercedes S-Class First Class for principals. Mercedes V-Class VIP Van for families, crews and luggage. Several cars on the same arrival through our network of chauffeurs: see the " + L(EN_C, 'fleet') + "."),
   ("Discretion", "No names on signs when you ask, no photos, no social media. What is said in the car stays in the car. Our chauffeurs drive UHNW families, diplomats and family offices since 2010."),
   ("After landing", L('/chauffeur-by-the-hour/', 'Chauffeur by the hour') + " for your stay, " + L('/ski-transfers/', 'ski transfers') + " to the resorts, " + L('/wef-davos-chauffeur/', 'WEF Davos') + " in January."),
  ]),
  faq=[("Can your chauffeur meet me at the aircraft in Geneva?", "Yes. We have tarmac access at Geneva Airport: your chauffeur meets you at the foot of the stairs when the FBO and handling agent allow it, otherwise inside the private aviation terminal."),
       ("Which private terminals do you serve in Geneva?", "The C3 private aviation terminal, Jet Aviation, TAG Aviation and Signature Flight Support, plus Sion Airport and Zurich Airport."),
       ("Do you work 24/7 for private jet arrivals?", "Yes. 24/7 operations and flight monitoring, with priority WhatsApp dispatch in under 10 minutes."),
       ("Can you send several cars for one arrival?", "Yes. Mercedes S-Class and V-Class VIP vans on the same arrival, coordinated by one contact. See our " + Ae(EN_C, 'fleet') + "."),
       ("Which currencies do you accept?", "Swiss francs, euros and US dollars."),
       ("How do I book?", "Send your tail number or flight, the FBO and the time on " + A_WA + ". You receive a fixed price before landing.")]),
 dict(url=FR_A, twin=EN_A, lang='fr', img='aero',
  title='Transfert aviation privée Genève · Jet | Prosper &amp; Co.',
  desc="Chauffeur pour l'aviation privée à Genève : terminal C3, Jet Aviation, TAG Aviation, Signature, Sion et Zurich. Accès tarmac, discrétion absolue, 24 h/24.",
  kicker='Transfert aviation privée · Genève · Tarmac et FBO', big=("L'avion se pose.", 'La portière est ouverte.'),
  sub="Votre chauffeur vous attend au pied de l'avion ou au terminal privé. Genève, Sion, Zurich. 24 h/24.",
  li=[("Au pied de l'avion.", "Accès tarmac à Genève, au pied de la passerelle quand le FBO l'autorise."),
      ('Tous les FBO.', "Terminal d'aviation privée C3, Jet Aviation, TAG Aviation, Signature Flight Support."),
      ('Ni nom, ni photo.', 'Discrétion absolue pour les grandes fortunes, les diplomates et les family offices.')],
  rates=('Aviation privée,', 'prix ferme.'), note="Tarifs horaires de base. Arrivées en jet : prix de transfert ferme confirmé avant l'atterrissage, frais d'aéroport refacturés au coût réel. Sion et Zurich sur devis.",
  stmt=('Grandes familles. Chefs d\'État. Family offices. Équipages. ', 'De la passerelle au chalet.'), mount=('Le vol est suivi.', 'La voiture est prête.'),
  contact=('Vous décollez bientôt ?', 'Envoyez votre immatriculation.'),
  det=("Transfert aviation privée,<br>en détail.", [
   ("Tarmac et FBO", "Votre chauffeur vous accueille au pied de l'avion à l'aéroport de Genève quand le FBO et l'agent de handling autorisent l'accès côté piste, ou dans le terminal d'aviation privée : C3, Jet Aviation, TAG Aviation et Signature Flight Support."),
   ("Sion et Zurich", "Le même service à l'aéroport de Sion pour Verbier, Crans-Montana et Zermatt, et à l'aéroport de Zurich pour Davos, Gstaad ou un programme d'affaires à Zurich."),
   ("Suivi des vols", WF + " En avance ou en retard, votre chauffeur suit le vol et s'adapte."),
   ("Les véhicules", "Mercedes Classe S First Class pour le passager principal. Mercedes Classe V VIP Van pour les familles, les équipages et les bagages. Plusieurs voitures sur la même arrivée grâce à notre réseau de chauffeurs : voir la " + L(FR_C, 'flotte') + "."),
   ("La discrétion", "Pas de nom sur la pancarte si vous le souhaitez, ni photo ni réseaux sociaux. Ce qui se dit à bord reste à bord. Nos chauffeurs conduisent grandes familles, diplomates et family offices depuis 2010."),
   ("Après l'atterrissage", L('/fr/chauffeur-a-disposition-geneve/', 'Chauffeur à disposition') + " pendant votre séjour, " + L('/ski-transfers/', 'transferts ski') + " vers les stations, " + L('/wef-davos-chauffeur/', 'WEF de Davos') + " en janvier."),
  ]),
  faq=[("Votre chauffeur peut-il m'attendre au pied de l'avion à Genève ?", "Oui. Nous avons l'accès tarmac à l'aéroport de Genève : votre chauffeur vous attend au pied de la passerelle quand le FBO et l'agent de handling l'autorisent, sinon dans le terminal d'aviation privée."),
       ("Quels terminaux privés desservez-vous à Genève ?", "Le terminal d'aviation privée C3, Jet Aviation, TAG Aviation et Signature Flight Support, ainsi que les aéroports de Sion et de Zurich."),
       ("Travaillez-vous 24 h/24 pour les arrivées en jet privé ?", "Oui. Opérations 24 h/24, 7 j/7 et suivi des vols, avec une réponse prioritaire sur WhatsApp en moins de 10 minutes."),
       ("Pouvez-vous envoyer plusieurs voitures pour une même arrivée ?", "Oui. Mercedes Classe S et Classe V VIP Van sur la même arrivée, coordonnées par un seul contact. Voir notre " + Ae(FR_C, 'flotte') + "."),
       ("Quelles devises acceptez-vous ?", "Le franc suisse, l'euro et le dollar américain."),
       ("Comment réserver ?", "Envoyez l'immatriculation ou le vol, le FBO et l'heure sur " + A_WA + ". Vous recevez un prix ferme avant l'atterrissage.")]),
 # ---------------- B : internats et cliniques ----------------
 dict(url=EN_B, twin=FR_B, lang='en', img='berline',
  title='Swiss Boarding School &amp; Clinic Chauffeur | Prosper &amp; Co.',
  desc='Trusted private chauffeur to Swiss boarding schools (Le Rosey, Collège du Léman, Aiglon, Beau Soleil) and private clinics (La Prairie, Genolier, La Colline).',
  kicker='Boarding schools &amp; private clinics · Switzerland', big=('Your family,', 'in trusted hands.'),
  sub='Term starts, weekends, exeats and clinic stays. One trusted chauffeur, a fixed price, 24/7.',
  li=[('The same chauffeur.', 'Wherever possible, one chauffeur your family knows, term after term.'),
      ('You are kept informed.', 'A WhatsApp message at pick-up and at arrival.'),
      ('Calm and discreet.', 'For clinic stays: door to door, at your pace, no questions asked.')],
  rates=('By the hour', 'or per transfer.'), note='Hourly rates from. School and clinic transfers: fixed price confirmed before the ride. This is a private chauffeur service, not medical transport.',
  stmt=('Rolle. Gstaad. Versoix. Villars. Montreux. Genolier. ', 'From Geneva Airport to the campus.'), mount=('Term starts.', 'Handled.'),
  contact=('Term starting soon?', 'Send us the dates.'),
  det=("Boarding schools and clinics,<br>in detail.", [
   ("Boarding schools", "We drive students and parents to and from Swiss boarding schools: Institut Le Rosey in Rolle and its winter campus in Gstaad, Collège du Léman in Versoix, Aiglon College and Beau Soleil in Villars-sur-Ollon. Term starts, weekends, exeats and end-of-term departures."),
   ("From the airport", "Pick-up at Geneva or Zurich Airport, including the " + L(EN_A, 'private aviation terminals') + ", with luggage, trunks and sports equipment. " + W),
   ("Private clinics", "Discreet transfers to and from private clinics: Clinique La Prairie in Montreux, Clinique de Genolier and Clinique La Colline in Geneva. Door to door, at your pace. This is a private chauffeur service, not medical or ambulance transport."),
   ("The cars", "Mercedes S-Class First Class, Mercedes E-Class Business, and the Mercedes V-Class VIP Van for families and luggage, up to 7 passengers."),
   ("Trust", "Since 2010 in Geneva. Wherever possible, the same chauffeur term after term, and one contact for the whole family."),
   ("The price", "A fixed price confirmed before the ride, in Swiss francs, euros or US dollars. Hourly rates from CHF 90."),
  ]),
  faq=[("Do you drive students to Swiss boarding schools?", "Yes. Institut Le Rosey (Rolle and Gstaad), Collège du Léman (Versoix), Aiglon College and Beau Soleil (Villars-sur-Ollon), from Geneva or Zurich Airport or between campus and home."),
       ("Can parents follow the ride?", "Yes. You receive a WhatsApp message at pick-up and at arrival, and you can reach the chauffeur directly."),
       ("Do you drive to private clinics?", "Yes. Clinique La Prairie in Montreux, Clinique de Genolier and Clinique La Colline in Geneva, door to door and with discretion. We are a private chauffeur service, not medical transport."),
       ("Can we keep the same chauffeur?", "Yes, wherever possible: one chauffeur your family knows, term after term."),
       ("How much does it cost?", "A fixed price confirmed before the ride. Hourly rates from CHF 90 in a Mercedes E-Class Business, CHF 110 in a V-Class VIP Van and CHF 140 in an S-Class First Class.")]),
 dict(url=FR_B, twin=EN_B, lang='fr', img='berline',
  title='Chauffeur internats et cliniques privées | Prosper &amp; Co.',
  desc='Chauffeur de confiance pour les internats suisses (Le Rosey, Collège du Léman, Aiglon, Beau Soleil) et les cliniques privées (La Prairie, Genolier, La Colline).',
  kicker='Internats et cliniques privées · Suisse', big=('Votre famille,', 'en de bonnes mains.'),
  sub='Rentrées, week-ends, sorties et séjours en clinique. Un chauffeur de confiance, un prix ferme, 24 h/24.',
  li=[('Le même chauffeur.', "Autant que possible, un chauffeur que votre famille connaît, d'un trimestre à l'autre."),
      ('Vous êtes informé.', "Un message WhatsApp à la prise en charge et à l'arrivée."),
      ('Calme et discrétion.', 'Pour un séjour en clinique : de porte à porte, à votre rythme.')],
  rates=("À l'heure", 'ou au trajet.'), note="Tarifs horaires de base. Trajets vers les internats et les cliniques : prix ferme confirmé avant le départ. Service de chauffeur privé, pas de transport médical.",
  stmt=('Rolle. Gstaad. Versoix. Villars. Montreux. Genolier. ', "De l'aéroport de Genève au campus."), mount=('La rentrée,', "c'est réglé."),
  contact=('La rentrée approche ?', 'Envoyez-nous les dates.'),
  det=("Internats et cliniques,<br>en détail.", [
   ("Les internats", "Nous conduisons élèves et parents vers les internats suisses et depuis ceux-ci : l'Institut Le Rosey à Rolle et son campus d'hiver à Gstaad, le Collège du Léman à Versoix, Aiglon College et Beau Soleil à Villars-sur-Ollon. Rentrées, week-ends, sorties et départs de fin de trimestre."),
   ("Depuis l'aéroport", "Prise en charge à l'aéroport de Genève ou de Zurich, y compris aux " + L(FR_A, "terminaux d'aviation privée") + ", avec bagages, malles et équipement de sport. " + WF),
   ("Les cliniques privées", "Des trajets discrets vers les cliniques privées et depuis celles-ci : Clinique La Prairie à Montreux, Clinique de Genolier et Clinique La Colline à Genève. De porte à porte, à votre rythme. Il s'agit d'un service de chauffeur privé, pas d'un transport médical ni d'une ambulance."),
   ("Les véhicules", "Mercedes Classe S First Class, Mercedes Classe E Business et Mercedes Classe V VIP Van pour les familles et les bagages, jusqu'à 7 passagers."),
   ("La confiance", "À Genève depuis 2010. Autant que possible, le même chauffeur d'un trimestre à l'autre, et un seul contact pour toute la famille."),
   ("Le prix", "Un prix ferme confirmé avant le départ, en francs suisses, en euros ou en dollars américains. Tarifs horaires dès CHF 90."),
  ]),
  faq=[("Conduisez-vous les élèves vers les internats suisses ?", "Oui. Institut Le Rosey (Rolle et Gstaad), Collège du Léman (Versoix), Aiglon College et Beau Soleil (Villars-sur-Ollon), depuis l'aéroport de Genève ou de Zurich, ou entre le campus et la maison."),
       ("Les parents peuvent-ils suivre le trajet ?", "Oui. Vous recevez un message WhatsApp à la prise en charge et à l'arrivée, et vous pouvez joindre le chauffeur directement."),
       ("Allez-vous vers les cliniques privées ?", "Oui. Clinique La Prairie à Montreux, Clinique de Genolier et Clinique La Colline à Genève, de porte à porte et en toute discrétion. Nous sommes un service de chauffeur privé, pas un transport médical."),
       ("Peut-on garder le même chauffeur ?", "Oui, autant que possible : un chauffeur que votre famille connaît, d'un trimestre à l'autre."),
       ("Combien cela coûte-t-il ?", "Un prix ferme confirmé avant le départ. Tarifs horaires dès CHF 90 en Mercedes Classe E Business, CHF 110 en Classe V VIP Van et CHF 140 en Classe S First Class.")]),
 # ---------------- C : flotte ----------------
 dict(url=EN_C, twin=FR_C, lang='en', img='van',
  title='Mercedes V-Class VIP &amp; S-Class Fleet Geneva | Prosper &amp; Co.',
  desc='Several Mercedes V-Class VIP vans and S-Class cars at once in Geneva since 2010: delegations, UN and diplomatic missions, banking roadshows and large families.',
  kicker='Mercedes V-Class VIP &amp; S-Class fleet · Geneva', big=('One car.', 'Or ten.'),
  sub='Several Mercedes V-Class VIP and S-Class at once, one contact, since 2010. 24/7.',
  li=[('Dispatch since 2010.', 'Several cars on the same programme through our network of chauffeurs.'),
      ('One contact.', 'One person coordinates every car, every timing, every change.'),
      ('Same standard.', 'Recent black Mercedes, professional chauffeurs, the same dress code.')],
  rates=('Fleet rates,', 'by the hour.'), note='Hourly rates from, per car. Multi-car and multi-day programmes on quote, invoiced in CHF, EUR or USD.',
  stmt=('African and diplomatic delegations. UN conferences. Banking roadshows. Large families. ', 'Every car, on time.'), mount=('Ten arrivals.', 'One plan.'),
  contact=('A delegation to move?', 'Send us the programme.'),
  det=("Mercedes fleet in Geneva,<br>in detail.", [
   ("Several cars at once", "Since 2010 we coordinate several Mercedes on the same programme through our network of chauffeurs: Mercedes V-Class VIP vans for up to 7 passengers with luggage, Mercedes S-Class First Class for heads of delegation, Mercedes E-Class Business for staff."),
   ("Delegations and the UN", "African and diplomatic delegations, permanent missions, UN and international conferences at the Palais des Nations: airport arrivals, hotel to venue, evening receptions."),
   ("Banking roadshows", "Several cars for a roadshow across Geneva, Lausanne and Zurich, with the same chauffeurs for the whole programme wherever possible. See " + L('/corporate-chauffeur-geneva/', 'corporate chauffeur') + "."),
   ("Large families", "Two or three V-Class VIP vans for a family arriving by " + L(EN_A, 'private jet') + ", with all the luggage, to Geneva or the ski resorts."),
   ("Coordination", "One contact for all cars. " + W),
   ("The price", "Hourly rates from CHF 90 (E-Class Business), CHF 110 (V-Class VIP Van) and CHF 140 (S-Class First Class), per car. Multi-car programmes on a fixed quote, in CHF, EUR or USD."),
  ]),
  faq=[("Can you provide several Mercedes V-Class at the same time in Geneva?", "Yes. Since 2010 we coordinate several Mercedes V-Class VIP vans and S-Class cars on the same programme through our network of chauffeurs, with one contact."),
       ("Do you drive delegations and UN conferences?", "Yes. African and diplomatic delegations, permanent missions and conferences at the Palais des Nations, from the airport to the hotel and the venue."),
       ("Do you handle banking roadshows?", "Yes. Several cars across Geneva, Lausanne and Zurich, ideally with the same chauffeurs for the whole programme."),
       ("How much does a Mercedes V-Class VIP cost per hour?", "From CHF 110 per hour, per car. E-Class Business from CHF 90 and S-Class First Class from CHF 140."),
       ("How do I book a fleet?", "Send the programme, the number of passengers and the dates on " + A_WA + ". We reply with a fixed quote for all cars.")]),
 dict(url=FR_C, twin=EN_C, lang='fr', img='van',
  title='Flotte Mercedes Classe V et Classe S Genève | Prosper &amp; Co.',
  desc='Plusieurs Mercedes Classe V VIP et Classe S en même temps à Genève depuis 2010 : délégations, missions diplomatiques, ONU, roadshows bancaires, familles.',
  kicker='Flotte Mercedes Classe V VIP et Classe S · Genève', big=('Une voiture.', 'Ou dix.'),
  sub='Plusieurs Mercedes Classe V VIP et Classe S en même temps, un seul contact, depuis 2010. 24 h/24.',
  li=[('Depuis 2010.', 'Plusieurs voitures sur le même programme grâce à notre réseau de chauffeurs.'),
      ('Un seul contact.', 'Une personne coordonne chaque voiture, chaque horaire, chaque changement.'),
      ('Le même niveau.', 'Des Mercedes noires récentes, des chauffeurs professionnels, la même tenue.')],
  rates=('Tarifs flotte,', "à l'heure."), note="Tarifs horaires de base, par voiture. Programmes à plusieurs voitures ou sur plusieurs jours : sur devis, facturés en CHF, EUR ou USD.",
  stmt=('Délégations africaines et diplomatiques. Conférences de l\'ONU. Roadshows bancaires. Grandes familles. ', "Chaque voiture, à l'heure."), mount=('Dix arrivées,', 'un seul plan.'),
  contact=('Une délégation à transporter ?', 'Envoyez-nous le programme.'),
  det=("Flotte Mercedes à Genève,<br>en détail.", [
   ("Plusieurs voitures à la fois", "Depuis 2010, nous coordonnons plusieurs Mercedes sur un même programme grâce à notre réseau de chauffeurs : Mercedes Classe V VIP Van jusqu'à 7 passagers avec bagages, Mercedes Classe S First Class pour les chefs de délégation, Mercedes Classe E Business pour les équipes."),
   ("Délégations et ONU", "Délégations africaines et diplomatiques, missions permanentes, conférences de l'ONU et internationales au Palais des Nations : arrivées à l'aéroport, trajets hôtel-lieu de réunion, réceptions du soir. Voir " + L('/fr/chauffeur-prive-diplomate-geneve/', 'délégations et diplomates') + "."),
   ("Roadshows bancaires", "Plusieurs voitures pour un roadshow entre Genève, Lausanne et Zurich, avec les mêmes chauffeurs pendant tout le programme autant que possible. Voir " + L('/fr/chauffeur-prive-business-geneve/', 'chauffeur privé business') + "."),
   ("Grandes familles", "Deux ou trois Classe V VIP Van pour une famille qui arrive en " + L(FR_A, 'jet privé') + ", avec tous les bagages, vers Genève ou les stations de ski."),
   ("La coordination", "Un seul contact pour toutes les voitures. " + WF),
   ("Le prix", "Tarifs horaires dès CHF 90 (Classe E Business), CHF 110 (Classe V VIP Van) et CHF 140 (Classe S First Class), par voiture. Programmes à plusieurs voitures sur devis ferme, en CHF, EUR ou USD."),
  ]),
  faq=[("Pouvez-vous fournir plusieurs Mercedes Classe V en même temps à Genève ?", "Oui. Depuis 2010, nous coordonnons plusieurs Mercedes Classe V VIP Van et Classe S sur un même programme grâce à notre réseau de chauffeurs, avec un seul contact."),
       ("Transportez-vous des délégations et des conférences de l'ONU ?", "Oui. Délégations africaines et diplomatiques, missions permanentes et conférences au Palais des Nations, de l'aéroport à l'hôtel et au lieu de réunion."),
       ("Gérez-vous des roadshows bancaires ?", "Oui. Plusieurs voitures entre Genève, Lausanne et Zurich, idéalement avec les mêmes chauffeurs pendant tout le programme."),
       ("Combien coûte une Mercedes Classe V VIP à l'heure ?", "Dès CHF 110 de l'heure, par voiture. Classe E Business dès CHF 90 et Classe S First Class dès CHF 140."),
       ("Comment réserver plusieurs voitures ?", "Envoyez le programme, le nombre de passagers et les dates sur " + A_WA + ". Nous répondons avec un devis ferme pour toutes les voitures.")]),
]

def one(rx, rep, s, flags=re.S):
    s2, n = re.subn(rx, rep, s, count=1, flags=flags); assert n == 1, rx[:60]; return s2
for c in PAGES:
    fr = c['lang'] == 'fr'
    s = open('fr/chauffeur-prive-business-geneve/index.html' if fr else 'corporate-chauffeur-geneva/index.html', encoding='utf-8').read()
    s = re.sub(r'  <section id="details".*?</section>\n\n', '', s, flags=re.S)
    s = re.sub(r'  <section id="faq".*?</section>\n\n', '', s, flags=re.S)
    s = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage".*?</script>\n', '', s, flags=re.S)
    s = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@graph".*?</script>\n', '', s, flags=re.S)
    s = re.sub(r'  <link rel="alternate" hreflang="[^"]*" href="[^"]*">\n', '', s)
    s = one(r'<title>.*?</title>', '<title>%s</title>' % c['title'], s)
    for k, v in (('name="description"', c['desc']), ('property="og:description"', c['desc']), ('property="og:title"', c['title'].replace(' | ', ' · '))):
        s = one(r'(<meta %s content=")[^"]*' % k, lambda m: m.group(1) + v, s)
    en, frr = (c['twin'], c['url']) if fr else (c['url'], c['twin'])
    s = one(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s%s">\n%s' % (BASE, c['url'], hreflang(en, frr).rstrip('\n')), s)
    s = one(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + BASE + c['url'], s)
    s = one(r'(<a class="ps-navlink ps-lang" href=")[^"]*', lambda m: m.group(1) + c['twin'], s)
    b, a_en, a_fr = IMG[c['img']]
    s = one(r'(<img class="ps-heroimg" src=")[^"]*(" srcset=")[^"]*(" sizes="[^"]*" width="2912" height="1632" alt=")[^"]*',
            lambda m: m.group(1) + '/assets/site/%s-2000.webp' % b + m.group(2) + '/assets/site/{0}-1200.webp 1200w, /assets/site/{0}-2000.webp 2000w, /assets/site/{0}-2912.webp 2912w'.format(b) + m.group(3) + (a_fr if fr else a_en), s)
    s = one(r'(<h1 class="ps-rise ps-d1 ps-kicker"[^>]*>)[^<]*(</h1>)', lambda m: m.group(1) + c['kicker'] + m.group(2), s)
    s = one(r'(<p class="ps-rise ps-d2 ps-big"[^>]*>)[^<]*<br><span([^>]*)>[^<]*(</span></p>)', lambda m: m.group(1) + c['big'][0] + '<br><span' + m.group(2) + '>' + c['big'][1] + m.group(3), s)
    s = one(r'(<p style="margin: 0; font-size: clamp\(17px, 1.6vw, 20px\)[^>]*>)[^<]*(</p>)', lambda m: m.group(1) + c['sub'] + m.group(2), s)
    for t, d in c['li']:
        s = one(r'(<li style="display: flex; gap: 28px[^>]*><span[^>]*>\d\d</span><span[^>]*><span style="font-size: clamp\(26px, 3vw, 40px\)[^>]*>)(?!@)[^<@]*(</span><span style="font-size: 16px; color: #aaa59b">)[^<@]*(</span>)',
                lambda m: m.group(1) + '@' + t + m.group(2) + '@' + d + m.group(3), s)
    s = s.replace('>@', '>')
    s = one(r'(<section id="rates".*?<h2[^>]*>)[^<]*<br><span([^>]*)>[^<]*(</span></h2>)', lambda m: m.group(1) + c['rates'][0] + '<br><span' + m.group(2) + '>' + c['rates'][1] + m.group(3), s)
    s = one(r'(<p style="margin: 0; font-size: 14px; line-height: 1.5; color: #8a857c; max-width: 560px">)[^<]*(</p>)', lambda m: m.group(1) + c['note'] + m.group(2), s)
    s = one(r'(<p style="margin: 0; font-size: clamp\(30px, 4.4vw, 64px\)[^>]*>)[^<]*<span style="color: #6f6a61">[^<]*(</span></p>)', lambda m: m.group(1) + c['stmt'][0] + '<span style="color: #6f6a61">' + c['stmt'][1] + m.group(2), s)
    s = one(r'(<div class="ps-mounttext"[^>]*>\s*<h2[^>]*>)[^<]*<br><span([^>]*)>[^<]*(</span></h2>)', lambda m: m.group(1) + c['mount'][0] + '<br><span' + m.group(2) + '>' + c['mount'][1] + m.group(3), s)
    s = one(r'(<section id="contact".*?<h2[^>]*>)[^<]*<br><span([^>]*)>[^<]*(</span></h2>)', lambda m: m.group(1) + c['contact'][0] + '<br><span' + m.group(2) + '>' + c['contact'][1] + m.group(3), s)
    s = s.replace('href="#rates" class="ps-card"', 'href="#details" class="ps-card"')
    s = s.replace('>See rates <', '>In detail <').replace('>Voir les tarifs <', '>En détail <')
    assert s.count('  <section id="contact"') == 1
    s = s.replace('  <section id="contact"', details(*c['det']) + faq_html(c['faq']) + '  <section id="contact"')
    s = s.replace('</head>', faq_ld(c['faq']) + '</head>', 1)
    p = c['url'].strip('/') + '/index.html'; os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(s); print('écrit', c['url'])

# ---------- pied de page « Services » : liens vers les 3 pages sur toutes les pages ----------
import glob
for p in glob.glob('**/index.html', recursive=True):
    s = open(p, encoding='utf-8').read()
    fr = '<html lang="fr">' in s
    a, b2, c2 = (FR_A, FR_B, FR_C) if fr else (EN_A, EN_B, EN_C)
    la, lb, lc = ('Aviation privée', 'Internats et cliniques', 'Flotte') if fr else ('Private aviation', 'Schools &amp; clinics', 'Fleet')
    add = '<a href="%s" style="color: #8a857c">%s</a><a href="%s" style="color: #8a857c">%s</a><a href="%s" style="color: #8a857c">%s</a>' % (a, la, b2, lb, c2, lc)
    if a not in s.split('aria-label="Services"')[-1][:2000]:
        s, n = re.subn(r'(<nav aria-label="Services"[^>]*>.*?)(</nav>)', lambda m: m.group(1) + add + m.group(2), s, count=1, flags=re.S)
        if n: open(p, 'w', encoding='utf-8').write(s)
# ---------- sitemap ----------
sm = open('sitemap.xml', encoding='utf-8').read()
for u in (EN_A, FR_A, EN_B, FR_B, EN_C, FR_C):
    if BASE + u + '<' not in sm:
        sm = sm.replace('</urlset>', '  <url>\n    <loc>%s%s</loc>\n    <lastmod>2026-11-16</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n</urlset>' % (BASE, u))
open('sitemap.xml', 'w', encoding='utf-8').write(sm)
# ---------- redirections : les 3 pages FR ne doivent pas être renvoyées vers /fr/ ----------
r = open('redirects.csv', encoding='utf-8').read()
if 'transfert-aviation-privee-geneve' not in r:
    r = r.replace('|transfert-aeroport-geneve)/?$).+$,/fr/', '|transfert-aeroport-geneve|transfert-aviation-privee-geneve|chauffeur-internats-cliniques-suisse|flotte-mercedes-classe-v-classe-s-geneve)/?$).+$,/fr/')
    assert 'flotte-mercedes' in r
open('redirects.csv', 'w', encoding='utf-8').write(r)
print('fini')
