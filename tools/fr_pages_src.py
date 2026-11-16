"""Génère la version française (4 pages) à partir des pages anglaises, ajoute hreflang et le lien de langue."""
import os, re, json, html, glob
os.chdir('/home/claude/vtc')
BASE = 'https://www.lux-taxi.com'
def rd(p): return open(p, encoding='utf-8').read()
def wr(p, s):
    os.makedirs(os.path.dirname(p) or '.', exist_ok=True); open(p, 'w', encoding='utf-8').write(s)
def L(h, t): return '<a href="%s">%s</a>' % (h, t)

U_HOME, U_BIZ, U_HOUR, U_DIP = '/fr/', '/fr/chauffeur-prive-business-geneve/', '/fr/chauffeur-a-disposition-geneve/', '/fr/chauffeur-prive-diplomate-geneve/'

# ---------- blocs générés ----------
def details(title, blocks):
    b = ''.join('<div><h3>%s</h3><p>%s</p></div>' % (h, p) for h, p in blocks)
    return '''  <section id="details" class="ps-pad ps-gap" style="max-width: 1280px; margin: 0 auto; padding: 200px 32px 0; display: flex; flex-direction: column; gap: 48px">
    <h2 style="margin: 0; font-size: clamp(36px, 5vw, 72px); line-height: 1; font-weight: 600; letter-spacing: -0.045em; max-width: 900px">%s</h2>
    <div class="ps-detail">%s</div>
  </section>

''' % (title, b)
def faq_html(qa):
    d = ''.join('<details style="border-top: 1px solid rgba(255,255,255,0.10); padding: 22px 0"><summary style="cursor: pointer; font-size: clamp(18px, 2vw, 24px); font-weight: 500; letter-spacing: -0.02em">%s</summary><p style="margin: 14px 0 0; font-size: 16px; line-height: 1.6; color: #aaa59b; max-width: 760px">%s</p></details>' % (html.escape(q, quote=False), a) for q, a in qa)
    return '''  <section id="faq" class="ps-pad ps-gap" style="max-width: 1080px; margin: 0 auto; padding: 200px 32px 0; display: flex; flex-direction: column; gap: 32px">
    <h2 style="margin: 0; font-size: clamp(36px, 5vw, 72px); line-height: 1; font-weight: 600; letter-spacing: -0.045em">Questions.</h2>
    <div style="border-bottom: 1px solid rgba(255,255,255,0.10)">%s</div>
  </section>

''' % d
def faq_ld(qa):
    strip = lambda a: html.unescape(re.sub(r'<[^>]+>', '', a))
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in qa]}, ensure_ascii=False) + '</script>\n'

CARS = "Mercedes Classe E jusqu'à 3 passagers. Mercedes Classe V VIP jusqu'à 7, avec bagages. Mercedes Classe S pour les dirigeants. Sprinter sur demande. Des véhicules récents, impeccables."
A_WA = '<a href="https://wa.me/41766207850" style="color: #c6a96b">WhatsApp</a>'
def A(h, t): return '<a href="%s" style="color: #c6a96b">%s</a>' % (h, t)

COMMON = {
 'Private Chauffeur · Geneva': 'Chauffeur privé · Genève',
 'Get a quote': 'Devis',
 'Book on WhatsApp': 'Réserver sur WhatsApp',
 'See rates ': 'Voir les tarifs ',
 'Get my price ': 'Obtenir mon prix ',
 'PER HOUR · 20 KM INCLUDED': 'PAR HEURE · 20 KM INCLUS',
 'Mercedes E-Class · 3 pax': 'Mercedes Classe E · 3 pers.',
 'Mercedes V-Class · 7 pax': 'Mercedes Classe V · 7 pers.',
 'Mercedes S-Class · 2 pax': 'Mercedes Classe S · 2 pers.',
 'Discretion, always.': 'La discrétion, toujours.',
 'Leave the driving.': 'Laissez-nous la route.',
 'Prosper &amp; Co. · Private chauffeur in Geneva since 2010': 'Prosper &amp; Co. · Chauffeur privé à Genève depuis 2010',
 'Operated by FairTransfert Sàrl · CHE-495.106.981': 'Exploité par FairTransfert Sàrl · CHE-495.106.981',
 'Airport transfer': 'Transfert aéroport',
 'Ski transfers': 'Transferts ski',
 'By the hour': 'À disposition',
 'Corporate': 'Entreprises',
 '© 2026 Prosper &amp; Co. · Geneva, Switzerland': '© 2026 Prosper &amp; Co. · Genève, Suisse',
 'Call': 'Appeler',
}
ATTR = {
 'aria-label="Main menu"': 'aria-label="Menu principal"',
 'aria-label="Open menu"': 'aria-label="Ouvrir le menu"',
 'aria-label="Start your quote"': 'aria-label="Commencer votre devis"',
 'aria-label="Quote request"': 'aria-label="Demande de devis"',
 'aria-label="Use my current location as pick-up"': 'aria-label="Utiliser ma position comme lieu de prise en charge"',
 'aria-label="Quick contact"': 'aria-label="Contact rapide"',
 'placeholder="Airport, hotel or address"': 'placeholder="Aéroport, hôtel ou adresse"',
 'placeholder="Hotel, resort or address"': 'placeholder="Hôtel, station ou adresse"',
 'placeholder="Your name"': 'placeholder="Votre nom"',
 'placeholder="name@company.com"': 'placeholder="nom@societe.com"',
 'placeholder="Flight number, passengers, luggage, skis, child seat…"': 'placeholder="Numéro de vol, passagers, bagages, skis, siège enfant…"',
 'alt="Black chauffeur sedan in a dark studio, golden light along the bodywork"': 'alt="Berline noire avec chauffeur dans un studio sombre, lumière dorée sur la carrosserie"',
 'alt="Chauffeur\'s gloved hand opening a rear car door"': 'alt="Main gantée d\'un chauffeur ouvrant la portière arrière"',
 'alt="Headlight of a black car in a dark studio"': 'alt="Phare d\'une voiture noire dans un studio sombre"',
 'alt="Black van in a dark studio"': 'alt="Van noir dans un studio sombre"',
 'alt="Rear cabin of a luxury car, black quilted leather"': 'alt="Habitacle arrière d\'une voiture de luxe, cuir noir matelassé"',
}
HOME = {
 'Geneva chauffeur service · Luxury &amp; VIP · Since 2010': 'Chauffeur privé de luxe · Genève · Depuis 2010',
 'Always on time.': 'Toujours à l\'heure.',
 'Never in the way.': 'Jamais de trop.',
 'S-Class. V-Class. One contact.': 'Classe S. Classe V. Un seul contact.',
 'Pick-up': 'Prise en charge', 'Drop-off': 'Destination', 'Date and time': 'Date et heure',
 'Fixed price within the hour · or ': 'Prix fixe dans l\'heure · ou ',
 'book on WhatsApp': 'réserver sur WhatsApp', 'see prices': 'voir les prix',
 'Geneva Airport': 'Aéroport de Genève',
 'You think about the day. ': 'Vous pensez à votre journée. ',
 'We think about the road.': 'Nous pensons à la route.',
 'The door, opened for you.': 'La portière, ouverte pour vous.',
 'Recent cars, kept immaculate.': 'Des véhicules récents, impeccables.',
 'Driving Geneva for over fifteen years.': 'Plus de quinze ans sur les routes de Genève.',
 'To get your fixed price, 7am to 11pm.': 'Pour recevoir votre prix fixe, de 7 h à 23 h.',
 'Contact, from booking to drop-off.': 'Contact, de la réservation à l\'arrivée.',
 'From the runway': 'Du tarmac',
 'to the slopes.': 'aux sommets.',
 'Fixed price confirmed before you ride. Night, weekend and tolls are always included in your quote, never added afterwards.': 'Prix fixe confirmé avant la course. Nuit, week-end et péages sont toujours compris dans le devis, jamais ajoutés après.',
 '01 · AIRPORT': '01 · AÉROPORT', 'From CHF 100 ': 'Dès CHF 100 ',
 '02 · BY THE HOUR': '02 · À DISPOSITION', 'Meetings &amp; events': 'Rendez-vous et événements', 'From CHF 80 / hour ': 'Dès CHF 80 / heure ',
 '03 · SKI RESORTS': '03 · STATIONS DE SKI', 'Alps, both sides': 'Alpes suisses et françaises', 'From CHF 250 ': 'Dès CHF 250 ',
 'Room for seven.': 'De la place pour sept.', 'And the skis.': 'Et pour les skis.',
 'Mercedes V-Class for families and groups. Verbier, Zermatt, Courchevel, Chamonix.': 'Mercedes Classe V pour les familles et les groupes. Verbier, Zermatt, Courchevel, Chamonix.',
 '“': '« ',
 "The first time I used his service, he came to check the address the day before, just to make sure there wouldn't be any problems.": "La première fois que j'ai fait appel à lui, il est venu vérifier l'adresse la veille, simplement pour s'assurer qu'il n'y aurait aucun problème.",
 'LEIF SJOBLOM · REGULAR CLIENT': 'LEIF SJOBLOM · CLIENT RÉGULIER · AVIS TRADUIT DE L\'ANGLAIS',
 'Read our Google reviews ': 'Lire nos avis Google ',
 'Where to?': 'Où allez-vous ?',
 'A fixed price, within the hour.': 'Un prix fixe, dans l\'heure.',
 'Prefer to talk? ': 'Vous préférez parler ? ',
 'PICK-UP': 'PRISE EN CHARGE', 'Use my location': 'Utiliser ma position', 'DROP-OFF': 'DESTINATION', 'DATE AND TIME': 'DATE ET HEURE',
 'NAME': 'NOM', 'PHONE · WHATSAPP': 'TÉLÉPHONE · WHATSAPP', 'EMAIL (OPTIONAL)': 'E-MAIL (FACULTATIF)', 'ANYTHING ELSE? (OPTIONAL)': 'AUTRE CHOSE ? (FACULTATIF)',
 'A hotel name is enough — we confirm the exact place with you.': 'Le nom d\'un hôtel suffit : nous confirmons le lieu exact avec vous.',
 'Leave empty': 'Laisser vide',
 'Get my price →': 'Obtenir mon prix →',
}
BIZ = {
 'Corporate chauffeur service · Geneva': 'Chauffeur privé business · Genève',
 'Your executives,': 'Vos dirigeants,', 'on time.': 'à l\'heure.',
 'Secure, discreet executive transport for companies, banks and international organisations. From CHF 80 / hour.': 'Un transport discret pour les entreprises, les banques et les organisations internationales. Dès CHF 80 / heure.',
 'One account.': 'Un seul compte.',
 'One contact for every booking, invoiced to your company.': 'Un seul contact pour chaque réservation, facturée à votre société.',
 'Confidential conversations stay in the car.': 'Les conversations confidentielles restent dans la voiture.',
 'From one car to a fleet.': 'D\'une voiture à une flotte.',
 'Roadshows and delegations through our network of certified chauffeurs.': 'Roadshows et délégations, grâce à notre réseau de chauffeurs.',
 'Corporate rates.': 'Tarifs entreprises.', 'By the hour.': 'À l\'heure.',
 'Rates from. Fixed price confirmed before the day starts. Transfers and multi-day programmes on quote.': 'Tarifs à partir de. Prix fixe confirmé avant le début de la journée. Transferts et programmes de plusieurs jours sur devis.',
 'Board meetings. Private banks. International organisations. Roadshows. ': 'Conseils d\'administration. Banques privées. Organisations internationales. Roadshows. ',
 'Airport to the Palais des Nations.': 'De l\'aéroport au Palais des Nations.',
 'Delegations.': 'Délégations.', 'Coordinated.': 'Coordonnées.',
 'A board meeting ahead?': 'Un conseil d\'administration en vue ?',
}
DIP = dict(BIZ)
DIP.update({
 'Corporate chauffeur service · Geneva': 'Chauffeur privé diplomate · Délégations · Genève',
 'Your executives,': 'Vos délégations,', 'on time.': 'coordonnées.',
 'Secure, discreet executive transport for companies, banks and international organisations. From CHF 80 / hour.': 'Des chauffeurs privés pour les missions, les délégations officielles et les organisations internationales à Genève. Dès CHF 80 / heure.',
 'One account.': 'Un seul contact.',
 'One contact for every booking, invoiced to your company.': 'Une personne coordonne tous les véhicules et tous les horaires.',
 'Confidential conversations stay in the car.': 'Ce qui se dit dans la voiture y reste.',
 'From one car to a fleet.': 'D\'une voiture à plusieurs.',
 'Roadshows and delegations through our network of certified chauffeurs.': 'Plusieurs véhicules sur le même programme, grâce à notre réseau de chauffeurs.',
 'Corporate rates.': 'Tarifs délégations.',
 'Board meetings. Private banks. International organisations. Roadshows. ': 'Palais des Nations. Missions permanentes. Conférences. Visites officielles. ',
 'Airport to the Palais des Nations.': 'De l\'aéroport à votre hôtel.',
 'Delegations.': 'Arrivées.', 'Coordinated.': 'Accueillies.',
 'A board meeting ahead?': 'Une délégation à recevoir ?',
})
HOUR = {
 'Chauffeur by the hour · Geneva': 'Chauffeur à disposition · Genève',
 'Your day,': 'Votre journée,', 'driven.': 'avec chauffeur.',
 'A chauffeur who waits. Meetings, roadshows, dinners, events. From CHF 80 / hour.': 'Un chauffeur qui vous attend. Rendez-vous, roadshows, dîners, événements. Dès CHF 80 / heure.',
 'Waits for you.': 'Il vous attend.', 'Between meetings, outside the dinner.': 'Entre deux rendez-vous, à la sortie du dîner.',
 'What is said in the car stays there.': 'Ce qui se dit dans la voiture y reste.',
 'One contact.': 'Un seul contact.', 'Your chauffeur, directly. Day or evening.': 'Votre chauffeur, en direct. De jour comme en soirée.',
 'By the hour.': 'À l\'heure.', 'Simply.': 'Simplement.',
 'Rates from. Fixed price confirmed before your day starts.': 'Tarifs à partir de. Prix fixe confirmé avant le début de votre journée.',
 'Meetings across Geneva. International organisations. Roadshows. Galas. ': 'Rendez-vous dans tout Genève. Organisations internationales. Roadshows. Galas. ',
 'Late dinners in Cologny.': 'Dîners tardifs à Cologny.',
 'Plans change.': 'Les plans changent.', 'We follow.': 'Nous suivons.',
 'Big day ahead?': 'Une grande journée en vue ?',
}

PAGES = {
 U_HOME: dict(src='index.html', en='/', tr=HOME,
  title='Chauffeur privé de luxe à Genève · Limousine | Prosper &amp; Co.',
  desc='Chauffeur privé de luxe et limousine à Genève depuis 2010. Mercedes Classe S et Classe V VIP, chauffeur discret, un seul contact. Affaires, jets privés, Alpes.',
  before='  <section id="quote"',
  det=("Chauffeur privé à Genève,<br>en détail.", [
   ("Les véhicules", CARS),
   ("Le chauffeur", "Un chauffeur privé professionnel, en français et en anglais. La portière ouverte, les bagages pris en charge, la voiture qui attend là où vous en avez besoin. Discret : ce qui se dit dans la voiture y reste."),
   ("Où nous roulons", "Genève et son aéroport, les organisations internationales, Palexpo et le CERN. Lausanne, Montreux et Zurich. Les Alpes suisses et françaises : Verbier, Zermatt, Gstaad, Courchevel, Chamonix et Megève."),
   ("Nos services", "Transferts depuis l'" + L('/geneva-airport-transfer/', 'aéroport de Genève') + " et les terminaux d'aviation privée. " + L(U_HOUR, 'Chauffeur à disposition') + " pour vos rendez-vous et vos dîners. " + L(U_BIZ, 'Chauffeur privé business') + " pour les dirigeants. " + L(U_DIP, 'Délégations et diplomates') + ". Transferts vers les " + L('/ski-transfers/', 'stations de ski') + "."),
   ("Le prix", "Un prix fixe, confirmé avant la course. Nuit, week-end et péages sont compris dans le devis, jamais ajoutés après. Transferts dès CHF 100, mise à disposition dès CHF 80 de l'heure."),
   ("L'entreprise", "Prosper &amp; Co. est un service de chauffeur privé de luxe et de limousine à Genève, en activité depuis 2010 et exploité par FairTransfert Sàrl, société suisse. Un seul contact, de la réservation à l'arrivée. Réponse dans l'heure, de 7 h à 23 h."),
  ]),
  faq=[
   ("Que comprend un service de chauffeur privé de luxe à Genève ?", "Une Mercedes Classe S ou Classe V VIP, un chauffeur professionnel et discret, et un seul contact de la réservation à l'arrivée. Votre prix est fixe et confirmé avant la course."),
   ("Combien coûte un chauffeur privé à Genève ?", "Les transferts commencent à CHF 100 en Mercedes Classe E. En " + A(U_HOUR, 'mise à disposition') + ", comptez dès CHF 80 de l'heure en Classe E, CHF 100 en Classe V et CHF 130 en Classe S, avec 20 km compris par heure."),
   ("Accueillez-vous les passagers de jets privés ?", "Oui. Votre chauffeur vous accueille à Genève ou à Zurich, y compris aux terminaux d'aviation privée."),
   ("Proposez-vous un service de limousine pour les entreprises et les délégations ?", "Oui. D'une voiture à plusieurs véhicules grâce à notre réseau de chauffeurs, avec un seul contact. Voir " + A(U_BIZ, 'chauffeur privé business') + " et " + A(U_DIP, 'délégations et diplomates') + "."),
   ("Où roulez-vous ?", "Genève, Lausanne, Montreux et Zurich, ainsi que les Alpes suisses et françaises : Verbier, Zermatt, Gstaad, Courchevel, Chamonix et Megève."),
   ("Comment réserver ?", "Envoyez votre lieu de prise en charge, votre destination et la date par le formulaire ou sur WhatsApp. Nous répondons avec un prix fixe dans l'heure, de 7 h à 23 h."),
  ]),
 U_BIZ: dict(src='corporate-chauffeur-geneva/index.html', en='/corporate-chauffeur-geneva/', tr=BIZ,
  title='Chauffeur privé business à Genève | Prosper &amp; Co.',
  desc='Chauffeur privé business à Genève : dirigeants, banques, organisations internationales. Mercedes Classe S et Classe V, facturation société.',
  svc=('Chauffeur privé business Genève', 'Chauffeur privé pour entreprises et dirigeants'),
  before='  <section id="contact"',
  det=("Chauffeur privé business,<br>en détail.", [
   ("Pour qui", "Les entreprises, les banques privées et les organisations internationales à Genève. Dirigeants, administrateurs, clients en visite. Les assistantes et les équipes voyages qui veulent un seul contact fiable."),
   ("Nos services", "Transferts de dirigeants depuis les aéroports de Genève et de Zurich. " + L(U_HOUR, 'Chauffeur à disposition') + " pour une journée de rendez-vous. Roadshows, " + L(U_DIP, 'délégations') + " et événements."),
   ("Les véhicules", "Mercedes Classe S pour les dirigeants. Mercedes Classe V VIP pour les équipes jusqu'à 7 personnes. Mercedes Classe E. Plusieurs véhicules sur le même programme grâce à notre réseau de chauffeurs."),
   ("La facturation", "Des courses facturées à votre société. Un seul contact pour chaque réservation, chaque changement et chaque facture."),
   ("La confidentialité", "Nos chauffeurs ne parlent jamais des clients, des agendas ni des conversations. Vous pouvez passer vos appels dans la voiture."),
   ("Où", "Genève, Lausanne, Montreux et Zurich. Le Palais des Nations, Palexpo, le CERN. En janvier, le " + L('/wef-davos-chauffeur/', 'WEF de Davos') + "."),
  ]),
  faq=[
   ("Pouvez-vous facturer notre société ?", "Oui. Les courses sont facturées à votre société, avec un seul contact pour vos assistantes et votre équipe voyages."),
   ("Peut-on garder le même chauffeur plusieurs jours ?", "Oui. Pour les roadshows et les dirigeants en visite, nous gardons le même chauffeur et la même voiture pour tout le programme, chaque fois que c'est possible."),
   ("Pouvez-vous transporter toute une délégation ?", "Oui. D'une voiture à plusieurs véhicules grâce à notre réseau de chauffeurs, coordonnés par un seul contact."),
   ("Accueillez-vous nos invités aux terminaux d'aviation privée ?", "Oui. Votre chauffeur accueille vos invités à Genève ou à Zurich, y compris aux terminaux d'aviation privée."),
   ("Comment garantissez-vous la confidentialité ?", "Nos chauffeurs ne parlent jamais des clients, des agendas ni des conversations. La discrétion fait partie du service."),
  ]),
 U_HOUR: dict(src='chauffeur-by-the-hour/index.html', en='/chauffeur-by-the-hour/', tr=HOUR,
  title='Chauffeur à disposition à Genève, à l\'heure | Prosper &amp; Co.',
  desc='Mise à disposition d\'un chauffeur privé à Genève : rendez-vous, roadshows, événements, galas et dîners. Dès CHF 80 de l\'heure, 20 km compris.',
  svc=('Chauffeur à disposition Genève', 'Mise à disposition de chauffeur à l\'heure'),
  before='  <section id="contact"',
  det=("Chauffeur à disposition,<br>en détail.", [
   ("Le principe", "Une voiture et un chauffeur privé à votre disposition à Genève, à l'heure. 20 km sont compris par heure. Votre chauffeur vous attend entre deux étapes et suit votre journée quand elle change."),
   ("Pour quoi", "Rendez-vous dans tout Genève et dans les organisations internationales. Roadshows. Dîners et soirées. Événements à Palexpo, galas. Une journée entre Genève, Lausanne et Montreux."),
   ("Les véhicules", "Mercedes Classe E dès CHF 80 de l'heure. Mercedes Classe V VIP dès CHF 100, jusqu'à 7 personnes. Mercedes Classe S dès CHF 130. Des véhicules récents, impeccables."),
   ("Le chauffeur", "Professionnel et discret, en français et en anglais. Ce qui se dit dans la voiture y reste."),
   ("Au-delà de Genève", "Lausanne, Montreux, Zurich ou une journée dans les Alpes. Pour les sociétés, voir " + L(U_BIZ, 'chauffeur privé business') + " ; pour les missions, " + L(U_DIP, 'délégations et diplomates') + "."),
   ("Réserver", "Envoyez votre date et votre programme. Nous répondons avec un prix fixe dans l'heure, de 7 h à 23 h. Un seul contact, de la réservation à la dernière étape."),
  ]),
  faq=[
   ("Combien coûte un chauffeur à disposition à Genève ?", "Dès CHF 80 de l'heure en Mercedes Classe E, CHF 100 en Classe V et CHF 130 en Classe S, avec 20 km compris par heure."),
   ("Le chauffeur attend-il pendant les rendez-vous et les dîners ?", "Oui. C'est le principe : votre chauffeur et la voiture restent avec vous entre deux rendez-vous et à la sortie du dîner, jusqu'à la fin de votre journée."),
   ("Proposez-vous un chauffeur privé pour un événement à Genève ?", "Oui. Galas, soirées, salons à Palexpo, réceptions : un chauffeur à disposition pour la durée de l'événement, et plusieurs véhicules si nécessaire."),
   ("Peut-on sortir de Genève ?", "Oui. Lausanne, Montreux, Zurich ou les Alpes. Votre prix est fixe et confirmé avant le début de la journée."),
   ("Comment réserver ?", "Envoyez votre date et votre programme par le formulaire ou sur WhatsApp. Nous répondons dans l'heure, de 7 h à 23 h."),
  ]),
 U_DIP: dict(src='corporate-chauffeur-geneva/index.html', en=None, tr=DIP,
  title='Chauffeur privé diplomate Genève | Prosper &amp; Co.',
  desc='Chauffeur privé pour diplomates et délégations à Genève : Palais des Nations, conférences, visites officielles. Mercedes Classe S et V, un seul contact.',
  svc=('Chauffeur privé diplomate Genève', 'Chauffeur privé pour diplomates, missions et délégations'),
  before='  <section id="contact"',
  det=("Délégations et diplomates,<br>en détail.", [
   ("Pour qui", "Les missions permanentes, les délégations officielles, les organisations internationales et leurs invités à Genève."),
   ("L'accueil", "Votre chauffeur accueille vos invités à l'aéroport de Genève, à l'arrivée ou au terminal d'aviation privée. Le vol est suivi : une avance ou un retard ne change rien."),
   ("Pendant la visite", L(U_HOUR, 'Chauffeur à disposition') + " à la journée, entre l'hôtel, le Palais des Nations, les missions et les dîners. Le même chauffeur pour tout le séjour, chaque fois que c'est possible."),
   ("Les véhicules", "Mercedes Classe S pour les chefs de délégation. Mercedes Classe V VIP jusqu'à 7 personnes pour les équipes. Plusieurs véhicules sur le même programme grâce à notre réseau de chauffeurs."),
   ("La discrétion", "Nos chauffeurs ne parlent jamais des passagers, des agendas ni des conversations. L'accès aux zones sécurisées dépend de vos accréditations : dites-nous lesquelles vous détenez, nous organisons les trajets en conséquence."),
   ("Le devis", "Un programme chiffré à l'avance, avec un prix fixe et un seul contact pour tous les véhicules. Voir aussi " + L(U_BIZ, 'chauffeur privé business') + "."),
  ]),
  faq=[
   ("Proposez-vous des chauffeurs privés pour les diplomates à Genève ?", "Oui. Nous conduisons des diplomates, des membres de missions et des délégations en visite, avec un chauffeur discret et un seul contact."),
   ("Pouvez-vous coordonner plusieurs véhicules pour une délégation ?", "Oui. D'une voiture à plusieurs véhicules grâce à notre réseau de chauffeurs, coordonnés par une seule personne."),
   ("Peut-on garder le même chauffeur pendant toute la visite ?", "Oui. À la journée, le même chauffeur et la même voiture restent avec vous pendant tout le séjour, chaque fois que c'est possible."),
   ("Accueillez-vous les arrivées en jet privé ?", "Oui. Votre chauffeur vous attend au terminal d'aviation privée de Genève ou de Zurich."),
   ("Pouvez-vous entrer dans les zones sécurisées ?", "L'accès dépend des accréditations délivrées par les organisateurs. Dites-nous ce que vous détenez et nous planifions les prises en charge autour."),
  ]),
}
FR_NAV = ('<a class="ps-navlink" href="%s">Entreprises</a>\n        <a class="ps-navlink" href="%s">À disposition</a>\n        <a class="ps-navlink" href="%s">Délégations</a>\n        ' % (U_BIZ, U_HOUR, U_DIP))
NAV_RX = re.compile(r'(?:<a class="ps-navlink" href="[^"]*">[^<]*</a>\s*)+')
def lang_link(href, code): return '<a class="ps-navlink ps-lang" href="%s" hreflang="%s" lang="%s">%s</a>\n        ' % (href, code, code, code.upper())
def hreflang(en, fr):
    return '  <link rel="alternate" hreflang="en" href="%s%s">\n  <link rel="alternate" hreflang="fr" href="%s%s">\n  <link rel="alternate" hreflang="x-default" href="%s%s">\n' % (BASE, en, BASE, fr, BASE, en)

for url, c in PAGES.items():
    s = rd(c['src'])
    s = re.sub(r'  <section id="details".*?</section>\n\n', '', s, flags=re.S)
    s = re.sub(r'  <section id="faq".*?</section>\n\n', '', s, flags=re.S)
    s = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage".*?</script>\n', '', s, flags=re.S)
    assert 'id="faq"' not in s and 'FAQPage' not in s and 'id="details"' not in s, url
    # tête
    s = s.replace('<html lang="en">', '<html lang="fr">').replace('content="en_GB"', 'content="fr_CH"')
    s = re.sub(r'<title>.*?</title>', '<title>%s</title>' % c['title'], s, count=1)
    s = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + c['desc'], s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + c['desc'], s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + c['title'].replace(' | ', ' · '), s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s%s">\n%s' % (BASE, url, hreflang(c['en'], url).rstrip('\n') if c['en'] else '  <link rel="alternate" hreflang="fr" href="%s%s">' % (BASE, url)), s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + BASE + url, s, count=1)
    if 'svc' in c:
        s, n = re.subn(r'"@type": "TaxiService", "name": "[^"]*", "serviceType": "[^"]*"', '"@type": "TaxiService", "name": "%s", "serviceType": "%s"' % c['svc'], s); assert n == 1
        s, n = re.subn(r'("areaServed": \[[^\]]*\], "url": ")[^"]*', lambda m: m.group(1) + BASE + url, s); assert n == 1
    # navigation
    s, n = NAV_RX.subn(lambda m: FR_NAV + lang_link(c['en'] or '/', 'en'), s, count=1); assert n == 1
    # textes
    tr = dict(COMMON); tr.update(c['tr'])
    for en, fr in tr.items():
        k = s.count('>' + en + '<')
        if k == 0 and en in c['tr']: print('  ! introuvable', url, repr(en[:50]))
        s = s.replace('>' + en + '<', '>' + fr + '<')
    for en, fr in ATTR.items(): s = s.replace(en, fr)
    # liens
    s = s.replace('href="/#quote"', 'href="/fr/#quote"').replace('href="/chauffeur-by-the-hour/"', 'href="%s"' % U_HOUR).replace('href="/corporate-chauffeur-geneva/"', 'href="%s"' % U_BIZ)
    s = s.replace('<a href="/" style="display: flex; align-items: center; gap: 12px; color: #f5f1e8">', '<a href="/fr/" style="display: flex; align-items: center; gap: 12px; color: #f5f1e8">')
    assert 'href="/fr/" style="display: flex' in s, url
    s = s.replace('action="/#quote"', 'action="/fr/#quote"')
    # pied de page : lien Délégations
    s = s.replace('<a href="/wef-davos-chauffeur/" style="color: #8a857c">WEF Davos</a></nav>', '<a href="%s" style="color: #8a857c">Délégations</a><a href="/wef-davos-chauffeur/" style="color: #8a857c">WEF Davos</a></nav>' % U_DIP)
    # blocs
    assert s.count(c['before']) == 1, url
    s = s.replace(c['before'], details(*c['det']) + faq_html(c['faq']) + c['before'])
    s = s.replace('</head>', faq_ld(c['faq']) + '</head>', 1)
    wr(url.strip('/') + '/index.html', s)
    print('écrit', url)

# ---------- pages anglaises : hreflang + lien FR ----------
PAIR = {'index.html': ('/', U_HOME), 'corporate-chauffeur-geneva/index.html': ('/corporate-chauffeur-geneva/', U_BIZ), 'chauffeur-by-the-hour/index.html': ('/chauffeur-by-the-hour/', U_HOUR)}
for p in ['index.html', 'geneva-airport-transfer/index.html', 'ski-transfers/index.html', 'chauffeur-by-the-hour/index.html', 'corporate-chauffeur-geneva/index.html', 'wef-davos-chauffeur/index.html']:
    s = rd(p)
    if 'ps-lang' not in s:
        fr = PAIR.get(p, (None, U_HOME))[1]
        a = '<a class="ps-navlink" href="/wef-davos-chauffeur/">WEF Davos</a>\n        '
        assert s.count(a) == 1, p
        s = s.replace(a, a + lang_link(fr, 'fr'))
        if p in PAIR and 'hreflang="x-default"' not in s:
            s, n = re.subn(r'(<link rel="canonical" href="[^"]*">\n)', lambda m: m.group(1) + hreflang(*PAIR[p]), s, count=1); assert n == 1
    wr(p, s)

# ---------- versions des fichiers communs ----------
for p in ['index.html'] + glob.glob('*/index.html') + glob.glob('fr/*/index.html'):
    s = rd(p)
    s = re.sub(r'prosper\.css\?v=\w+', 'prosper.css?v=20261112d', s); s = re.sub(r'prosper\.js\?v=\w+', 'prosper.js?v=20261112d', s)
    wr(p, s)

# ---------- sitemap ----------
sm = rd('sitemap.xml')
for u in PAGES:
    if BASE + u + '<' not in sm:
        sm = sm.replace('</urlset>', '  <url>\n    <loc>%s%s</loc>\n    <lastmod>2026-11-12</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n  </url>\n</urlset>' % (BASE, u, '0.9' if u == U_HOME else '0.8'))
wr('sitemap.xml', sm)

# ---------- redirections ----------
r = rd('redirects.csv')
r = r.replace('\n/fr/,/\n', '\n').replace('/fr/chauffeur-prive-a-geneve/,/\n', '/fr/chauffeur-prive-a-geneve/,/fr/\n')
old = 'motif:^fr/.+$,/'
new = 'motif:^fr/(?!(chauffeur-prive-business-geneve|chauffeur-a-disposition-geneve|chauffeur-prive-diplomate-geneve)/?$).+$,/fr/'
assert old in r or new in r
r = r.replace(old + '\n', new + '\n') if old + '\n' in r else r.replace(old, new)
wr('redirects.csv', r)
t = rd('tools/redirects.py')
t = t.replace('"/fr/une-page-inconnue/": "/",', '"/fr/une-page-inconnue/": "/fr/",')
wr('tools/redirects.py', t)
print('fini')
