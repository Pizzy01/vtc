"""Schema.org pour le GEO : un seul graphe par page (entreprise, site, page, fil d'Ariane, service).
Remplace les blocs LocalBusiness et TaxiService ; garde les blocs FAQPage. Ajoute /llms.txt.
Aucun identifiant Google n'est touché."""
import os, re, json, html
os.chdir('/home/claude/vtc')
B = 'https://www.lux-taxi.com'
BIZ = B + '/#business'; SITE = B + '/#website'

def city(n): return {"@type": "City", "name": n}
AREA_ALL = ["Geneva", "Lausanne", "Montreux", "Zurich", "Verbier", "Zermatt", "Gstaad", "Crans-Montana", "Chamonix", "Megève", "Courchevel", "Méribel", "Val d'Isère", "Tignes", "Davos", "Rolle", "Sion", "Villars-sur-Ollon"]

def offer(prix, unite, txt_en, txt_fr, fr):
    return {"@type": "Offer", "priceCurrency": "CHF",
            "priceSpecification": {"@type": "UnitPriceSpecification", "price": prix, "priceCurrency": "CHF",
                                   **({"unitText": unite} if unite else {}), "valueAddedTaxIncluded": True},
            "description": txt_fr if fr else txt_en}

BUSINESS = {
    "@type": ["LocalBusiness", "TaxiService"],
    "@id": BIZ,
    "name": "Prosper & Co.",
    "alternateName": ["Lux Taxi", "Prosper & Co. (FairTransfert Sàrl - Founded 2010)", "Prosper & Co. Private Chauffeur Geneva"],
    "additionalType": "https://en.wikipedia.org/wiki/Limousine_service",
    "legalName": "FairTransfert Sàrl",
    "taxID": "CHE-495.106.981",
    "foundingDate": "2010",
    "url": B + "/",
    "logo": B + "/assets/site/og.jpg",
    "image": B + "/assets/site/og.jpg",
    "description": "Private chauffeur and luxury limousine service in Geneva: Mercedes S-Class, V-Class VIP and E-Class, airport transfers including private aviation terminals, chauffeur by the hour, corporate chauffeurs, delegations, ski resorts and WEF Davos. Fixed price confirmed before the ride. 24/7 operations and flight monitoring, priority WhatsApp dispatch in under 10 minutes. Founded in 2010.",
    "telephone": "+41766207850",
    "email": "info@lux-taxi.com",
    "contactPoint": {"@type": "ContactPoint", "contactType": "reservations", "telephone": "+41766207850",
                     "email": "info@lux-taxi.com", "availableLanguage": ["English", "French"],
                     "hoursAvailable": {"@type": "OpeningHoursSpecification",
                                        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                        "opens": "00:00", "closes": "23:59"}},
    "address": {"@type": "PostalAddress", "addressLocality": "Geneva", "addressRegion": "GE", "addressCountry": "CH"},
    "areaServed": [city(c) for c in AREA_ALL] + [{"@type": "Country", "name": "Switzerland"}],
    "knowsLanguage": ["en", "fr"],
    "priceRange": "CHF 90–840",
    "currenciesAccepted": "CHF, EUR, USD",
    "paymentAccepted": "Cash, Credit Card, Bank Transfer",
    "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Fixed prices in CHF", "itemListElement": [
        offer(100, None, "Geneva Airport to Geneva city, Mercedes E-Class Business, fixed price", "", False),
        offer(120, None, "Geneva Airport to Geneva city, Mercedes V-Class VIP Van, fixed price", "", False),
        offer(180, None, "Geneva Airport to Lausanne, Mercedes E-Class Business, fixed price", "", False),
        offer(290, None, "Geneva Airport to Montreux, Mercedes E-Class Business, fixed price", "", False),
        offer(500, None, "Geneva Airport to Verbier, Mercedes E-Class Business, fixed price", "", False),
        offer(530, None, "Geneva Airport to Courchevel, Mercedes E-Class Business, fixed price", "", False),
        offer(530, None, "Geneva Airport to Méribel, Mercedes E-Class Business, fixed price", "", False),
        offer(610, None, "Geneva Airport to Val d'Isère, Mercedes E-Class Business, fixed price", "", False),
        offer(610, None, "Geneva Airport to Tignes, Mercedes E-Class Business, fixed price", "", False),
        offer(720, None, "Geneva Airport to Zermatt, Mercedes E-Class Business, fixed price", "", False),
        offer(90, "hour", "Chauffeur by the hour, Mercedes E-Class Business, 20 km included per hour", "", False),
        offer(110, "hour", "Chauffeur by the hour, Mercedes V-Class VIP Van (7 pax), 20 km included per hour", "", False),
        offer(140, "hour", "Chauffeur by the hour, Mercedes S-Class First Class, 20 km included per hour", "", False)]},
    "makesOffer": [
        {"@type": "Offer", "itemOffered": {"@id": B + "/geneva-airport-transfer/#service"}},
        {"@type": "Offer", "itemOffered": {"@id": B + "/chauffeur-by-the-hour/#service"}},
        {"@type": "Offer", "itemOffered": {"@id": B + "/corporate-chauffeur-geneva/#service"}},
        {"@type": "Offer", "itemOffered": {"@id": B + "/ski-transfers/#service"}},
        {"@type": "Offer", "itemOffered": {"@id": B + "/wef-davos-chauffeur/#service"}},
        {"@type": "Offer", "itemOffered": {"@id": B + "/fr/chauffeur-prive-diplomate-geneve/#service"}},
        {"@type": "Offer", "itemOffered": {"@id": B + "/private-aviation-jet-transfer-geneva/#service"}},
        {"@type": "Offer", "itemOffered": {"@id": B + "/swiss-boarding-schools-medical-chauffeur/#service"}},
        {"@type": "Offer", "itemOffered": {"@id": B + "/mercedes-v-class-vip-s-class-fleet-geneva/#service"}},
    ],
}
WEBSITE = {"@type": "WebSite", "@id": SITE, "url": B + "/", "name": "Prosper & Co.", "alternateName": "Lux Taxi",
           "publisher": {"@id": BIZ}, "inLanguage": ["en", "fr"]}

# page -> (langue, nom dans le fil d'Ariane, service ou None, page jumelle)
P = {
 'index.html': ('en', None, None, '/fr/'),
 'fr/index.html': ('fr', None, None, '/'),
 'geneva-airport-transfer/index.html': ('en', 'Geneva airport transfer', dict(
     name="Geneva Airport Transfer", type="Airport transfer with private chauffeur",
     desc="Private chauffeur from Geneva Airport (GVA) arrivals or the private aviation terminal to your hotel, home or resort. Flight tracked, name sign, 60 minutes of waiting included.",
     area=["Geneva", "Lausanne", "Montreux", "Zurich", "Gstaad", "Verbier", "Zermatt", "Chamonix", "Megève", "Courchevel"],
     offers=[(100, None, "Geneva city from CHF 100 in a Mercedes E-Class", "")]), '/fr/transfert-aeroport-geneve/'),
 'fr/transfert-aeroport-geneve/index.html': ('fr', 'Transfert aéroport', dict(
     name="Transfert aéroport Genève", type="Transfert aéroport avec chauffeur privé",
     desc="Chauffeur privé depuis les arrivées de l'aéroport de Genève (GVA) ou le terminal d'aviation privée vers votre hôtel, votre domicile ou votre station. Vol suivi, accueil personnalisé avec pancarte nominative, 60 minutes d'attente comprises.",
     area=["Geneva", "Lausanne", "Montreux", "Zurich", "Gstaad", "Verbier", "Zermatt", "Chamonix", "Megève", "Courchevel"],
     offers=[(100, None, "", "Genève ville dès CHF 100 en Mercedes Classe E"), (180, None, "", "Lausanne dès CHF 180 en Mercedes Classe E"), (500, None, "", "Verbier dès CHF 500 en Mercedes Classe E")]), '/geneva-airport-transfer/'),
 'ski-transfers/index.html': ('en', 'Ski transfers', dict(
     name="Geneva Ski Transfers", type="Private ski resort transfer",
     desc="Private door-to-door transfers from Geneva Airport to Swiss and French ski resorts in a Mercedes V-Class VIP or E-Class, with room for skis and luggage.",
     area=["Verbier", "Zermatt", "Gstaad", "Crans-Montana", "Chamonix", "Megève", "Courchevel", "Méribel", "Val d'Isère", "Tignes"],
     offers=[(500, None, "Geneva Airport to Verbier from CHF 500 in a Mercedes E-Class", ""),
             (720, None, "Geneva Airport to Täsch (Zermatt) from CHF 720 in a Mercedes E-Class", ""),
             (530, None, "Geneva Airport to Courchevel from CHF 530 in a Mercedes E-Class", ""),
             (530, None, "Geneva Airport to Méribel from CHF 530 in a Mercedes E-Class", ""),
             (610, None, "Geneva Airport to Val d'Isère from CHF 610 in a Mercedes E-Class", ""),
             (610, None, "Geneva Airport to Tignes from CHF 610 in a Mercedes E-Class", "")]), '/fr/transferts-ski/'),
 'fr/transferts-ski/index.html': ('fr', 'Stations de ski', dict(
     name="Transferts privés Aéroport de Genève vers les stations de ski", type="Transfert privé vers les stations de ski",
     desc="Transferts privés de porte à porte depuis l'aéroport de Genève vers les stations de ski suisses et françaises, en Van Mercedes Classe V VIP ou Classe E, avec de la place pour les skis et les bagages. Tarif forfaitaire garanti.",
     area=["Verbier", "Zermatt", "Gstaad", "Crans-Montana", "Chamonix", "Megève", "Courchevel", "Méribel", "Val d'Isère", "Tignes"],
     offers=[(250, None, "", "Megève dès CHF 250 en Mercedes Classe E"), (300, None, "", "Chamonix dès CHF 300 en Mercedes Classe E"),
             (500, None, "", "Verbier dès CHF 500 en Mercedes Classe E"), (530, None, "", "Courchevel dès CHF 530 en Mercedes Classe E"),
             (530, None, "", "Méribel dès CHF 530 en Mercedes Classe E"), (610, None, "", "Val d'Isère dès CHF 610 en Mercedes Classe E"),
             (610, None, "", "Tignes dès CHF 610 en Mercedes Classe E"), (720, None, "", "Täsch (Zermatt) dès CHF 720 en Mercedes Classe E")]), '/ski-transfers/'),
 'chauffeur-by-the-hour/index.html': ('en', 'Chauffeur by the hour', dict(
     name="Chauffeur by the Hour in Geneva", type="Hourly chauffeur service",
     desc="A car and a private chauffeur at your disposal in Geneva, by the hour, 20 km included per hour. Meetings, roadshows, dinners and events.",
     area=["Geneva", "Lausanne", "Montreux", "Zurich"],
     offers=[(90, "hour", "Mercedes E-Class Business from CHF 90 per hour", ""), (110, "hour", "Mercedes V-Class VIP Van from CHF 110 per hour", ""),
             (140, "hour", "Mercedes S-Class First Class from CHF 140 per hour", "")]), '/fr/chauffeur-a-disposition-geneve/'),
 'corporate-chauffeur-geneva/index.html': ('en', 'Corporate chauffeur', dict(
     name="Corporate Chauffeur Service Geneva", type="Corporate and executive chauffeur service",
     desc="Executive transport for companies, private banks and international organisations in Geneva, invoiced to the company, with one contact for every booking.",
     area=["Geneva", "Lausanne", "Zurich", "Davos"],
     offers=[(90, "hour", "Mercedes E-Class Business from CHF 90 per hour", ""), (140, "hour", "Mercedes S-Class First Class from CHF 140 per hour", "")]),
     '/fr/chauffeur-prive-business-geneve/'),
 'wef-davos-chauffeur/index.html': ('en', 'WEF Davos', dict(
     name="WEF Davos Chauffeur Service", type="Chauffeur service for the World Economic Forum in Davos",
     desc="One car and one chauffeur by the day for the World Economic Forum week in Davos, quoted as a full programme: car, chauffeur, fuel, tolls and the chauffeur's stay included.",
     area=["Davos", "Klosters", "Zurich", "Geneva"], offers=[]), None),
 'fr/chauffeur-prive-business-geneve/index.html': ('fr', 'Chauffeur privé business', dict(
     name="Chauffeur privé business à Genève", type="Chauffeur privé pour entreprises et dirigeants",
     desc="Transport de dirigeants pour les entreprises, les banques privées et les organisations internationales à Genève, facturé à la société, avec un seul contact.",
     area=["Geneva", "Lausanne", "Zurich", "Davos"],
     offers=[(90, "heure", "", "Mercedes Classe E Business dès CHF 90 de l'heure"), (140, "heure", "", "Mercedes Classe S First Class dès CHF 140 de l'heure")]),
     '/corporate-chauffeur-geneva/'),
 'fr/chauffeur-a-disposition-geneve/index.html': ('fr', 'Chauffeur à disposition', dict(
     name="Chauffeur à disposition à Genève", type="Mise à disposition de chauffeur à l'heure",
     desc="Une voiture et un chauffeur privé à votre disposition à Genève, à l'heure, 20 km compris par heure. Rendez-vous, roadshows, dîners, galas et événements.",
     area=["Geneva", "Lausanne", "Montreux", "Zurich"],
     offers=[(90, "heure", "", "Mercedes Classe E Business dès CHF 90 de l'heure"), (110, "heure", "", "Mercedes Classe V VIP Van dès CHF 110 de l'heure"),
             (140, "heure", "", "Mercedes Classe S First Class dès CHF 140 de l'heure")]), '/chauffeur-by-the-hour/'),
 'fr/chauffeur-prive-diplomate-geneve/index.html': ('fr', 'Délégations et diplomates', dict(
     name="Chauffeur privé pour diplomates et délégations à Genève", type="Chauffeur privé pour diplomates, missions et délégations",
     desc="Chauffeurs privés pour les missions permanentes, les délégations officielles et les organisations internationales à Genève, avec plusieurs véhicules coordonnés par un seul contact.",
     area=["Geneva", "Lausanne", "Zurich", "Davos"], offers=[]), None),
 'private-aviation-jet-transfer-geneva/index.html': ('en', 'Private jet transfer', dict(
     name="Private Jet Transfer Geneva", type="Private aviation chauffeur and FBO transfer",
     desc="Chauffeur for private jet arrivals at Geneva Airport (C3 terminal, Jet Aviation, TAG Aviation, Signature Flight Support), Sion and Zurich. Tarmac access, 24/7 flight monitoring, absolute discretion for UHNW families, diplomats and family offices.",
     area=["Geneva", "Sion", "Zurich", "Verbier", "Gstaad", "Zermatt", "Courchevel", "Davos"],
     offers=[(140, "hour", "Mercedes S-Class First Class from CHF 140 per hour", ""), (110, "hour", "Mercedes V-Class VIP Van from CHF 110 per hour", "")]), '/fr/transfert-aviation-privee-geneve/'),
 'fr/transfert-aviation-privee-geneve/index.html': ('fr', 'Aviation privée', dict(
     name="Transfert aviation privée Genève", type="Chauffeur pour l'aviation privée et les FBO",
     desc="Chauffeur pour les arrivées en jet privé à l'aéroport de Genève (terminal C3, Jet Aviation, TAG Aviation, Signature Flight Support), Sion et Zurich. Accès tarmac, suivi des vols 24 h/24, discrétion absolue.",
     area=["Geneva", "Sion", "Zurich", "Verbier", "Gstaad", "Zermatt", "Courchevel", "Davos"],
     offers=[(140, "heure", "", "Mercedes Classe S First Class dès CHF 140 de l'heure"), (110, "heure", "", "Mercedes Classe V VIP Van dès CHF 110 de l'heure")]), '/private-aviation-jet-transfer-geneva/'),
 'swiss-boarding-schools-medical-chauffeur/index.html': ('en', 'Boarding schools and clinics', dict(
     name="Swiss Boarding School and Private Clinic Chauffeur", type="Private chauffeur for boarding schools and private clinics",
     desc="Trusted private chauffeur to Swiss boarding schools (Institut Le Rosey in Rolle and Gstaad, Collège du Léman in Versoix, Aiglon College and Beau Soleil in Villars-sur-Ollon) and private clinics (Clinique La Prairie in Montreux, Clinique de Genolier, Clinique La Colline in Geneva). Not medical transport.",
     area=["Geneva", "Rolle", "Gstaad", "Versoix", "Villars-sur-Ollon", "Montreux", "Genolier", "Zurich"],
     offers=[(90, "hour", "Mercedes E-Class Business from CHF 90 per hour", ""), (110, "hour", "Mercedes V-Class VIP Van from CHF 110 per hour", ""), (140, "hour", "Mercedes S-Class First Class from CHF 140 per hour", "")]), '/fr/chauffeur-internats-cliniques-suisse/'),
 'fr/chauffeur-internats-cliniques-suisse/index.html': ('fr', 'Internats et cliniques', dict(
     name="Chauffeur pour internats suisses et cliniques privées", type="Chauffeur privé pour internats et cliniques privées",
     desc="Chauffeur de confiance vers les internats suisses (Institut Le Rosey à Rolle et Gstaad, Collège du Léman à Versoix, Aiglon College et Beau Soleil à Villars-sur-Ollon) et les cliniques privées (Clinique La Prairie à Montreux, Clinique de Genolier, Clinique La Colline à Genève). Pas de transport médical.",
     area=["Geneva", "Rolle", "Gstaad", "Versoix", "Villars-sur-Ollon", "Montreux", "Genolier", "Zurich"],
     offers=[(90, "heure", "", "Mercedes Classe E Business dès CHF 90 de l'heure"), (110, "heure", "", "Mercedes Classe V VIP Van dès CHF 110 de l'heure"), (140, "heure", "", "Mercedes Classe S First Class dès CHF 140 de l'heure")]), '/swiss-boarding-schools-medical-chauffeur/'),
 'mercedes-v-class-vip-s-class-fleet-geneva/index.html': ('en', 'Mercedes fleet', dict(
     name="Mercedes V-Class VIP and S-Class Fleet Geneva", type="Multi-vehicle chauffeur dispatch",
     desc="Several Mercedes V-Class VIP vans and S-Class cars at the same time in Geneva since 2010, coordinated by one contact: African and diplomatic delegations, UN conferences, banking roadshows and large families.",
     area=["Geneva", "Lausanne", "Montreux", "Zurich", "Davos"],
     offers=[(90, "hour", "Mercedes E-Class Business from CHF 90 per hour per car", ""), (110, "hour", "Mercedes V-Class VIP Van from CHF 110 per hour per car", ""), (140, "hour", "Mercedes S-Class First Class from CHF 140 per hour per car", "")]), '/fr/flotte-mercedes-classe-v-classe-s-geneve/'),
 'fr/flotte-mercedes-classe-v-classe-s-geneve/index.html': ('fr', 'Flotte Mercedes', dict(
     name="Flotte Mercedes Classe V VIP et Classe S à Genève", type="Mise à disposition de plusieurs véhicules avec chauffeur",
     desc="Plusieurs Mercedes Classe V VIP Van et Classe S en même temps à Genève depuis 2010, coordonnées par un seul contact : délégations africaines et diplomatiques, conférences de l'ONU, roadshows bancaires, grandes familles.",
     area=["Geneva", "Lausanne", "Montreux", "Zurich", "Davos"],
     offers=[(90, "heure", "", "Mercedes Classe E Business dès CHF 90 de l'heure par voiture"), (110, "heure", "", "Mercedes Classe V VIP Van dès CHF 110 de l'heure par voiture"), (140, "heure", "", "Mercedes Classe S First Class dès CHF 140 de l'heure par voiture")]), '/mercedes-v-class-vip-s-class-fleet-geneva/'),
}
HOME_NAME = {'en': 'Home', 'fr': 'Accueil'}

def graph(path, lang, crumb, svc, twin):
    url = B + '/' + (path[:-len('index.html')] if path != 'index.html' else '')
    s = open(path, encoding='utf-8').read()
    title = html.unescape(re.search(r'<title>(.*?)</title>', s).group(1))
    desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', s).group(1))
    fr = lang == 'fr'
    page = {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc,
            "inLanguage": lang, "isPartOf": {"@id": SITE}, "about": {"@id": BIZ},
            "primaryImageOfPage": B + "/assets/site/og.jpg"}
    if twin: page["workTranslation" if lang == 'en' else "translationOfWork"] = {"@id": B + twin + "#webpage"}
    g = [BUSINESS, WEBSITE, page]
    if crumb:
        home = B + ('/fr/' if fr else '/')
        page["breadcrumb"] = {"@id": url + "#breadcrumb"}
        g.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": HOME_NAME[lang], "item": home},
            {"@type": "ListItem", "position": 2, "name": crumb, "item": url}]})
    if svc:
        sv = {"@type": "Service", "@id": url + "#service", "name": svc['name'], "serviceType": svc['type'],
              "description": svc['desc'], "provider": {"@id": BIZ}, "url": url, "inLanguage": lang,
              "areaServed": [city(c) for c in svc['area']]}
        if svc['offers']:
            sv["offers"] = [offer(p, u, te, tf, fr) for p, u, te, tf in svc['offers']]
        page["mainEntity"] = {"@id": url + "#service"}
        g.append(sv)
    return {"@context": "https://schema.org", "@graph": g}

LD = re.compile(r'<script type="application/ld\+json">(.*?)</script>\n?', re.S)
for path, (lang, crumb, svc, twin) in P.items():
    s = open(path, encoding='utf-8').read()
    kept, removed = [], 0
    def sub(m):
        global removed
        j = json.loads(m.group(1))
        if j.get('@type') in ('LocalBusiness', 'TaxiService') or '@graph' in j:
            return ''
        return m.group(0)
    s2 = LD.sub(sub, s)
    assert s2.count('"FAQPage"') == 1, path
    block = '<script type="application/ld+json">' + json.dumps(graph(path, lang, crumb, svc, twin), ensure_ascii=False) + '</script>\n'
    s2 = s2.replace('</head>', block + '</head>', 1)
    open(path, 'w', encoding='utf-8').write(s2)
    print(path, 'ok')

open('llms.txt', 'w', encoding='utf-8').write("""# Prosper & Co. (Lux Taxi)

> Private chauffeur and luxury limousine service in Geneva, Switzerland, founded in 2010, operated by FairTransfert Sàrl (CHE-495.106.981). Mercedes S-Class, V-Class VIP and E-Class. Fixed price confirmed before the ride. English and French. Payment in CHF, EUR or USD. 24/7 operations and flight monitoring, priority WhatsApp dispatch in under 10 minutes: +41 76 620 78 50, WhatsApp, info@lux-taxi.com.

## Services (English)
- [Geneva chauffeur service](https://www.lux-taxi.com/): luxury and VIP private chauffeur in Geneva
- [Geneva airport transfer](https://www.lux-taxi.com/geneva-airport-transfer/): Geneva Airport arrivals and private aviation terminal, from CHF 100
- [Chauffeur by the hour](https://www.lux-taxi.com/chauffeur-by-the-hour/): E-Class Business from CHF 90, V-Class VIP Van from CHF 110, S-Class First Class from CHF 140 per hour, 20 km included per hour
- [Corporate chauffeur service](https://www.lux-taxi.com/corporate-chauffeur-geneva/): executives, banks, international organisations
- [Ski transfers](https://www.lux-taxi.com/ski-transfers/): Verbier, Zermatt, Gstaad, Chamonix, Megève, Courchevel, Méribel, Val d'Isère, Tignes
- [Private jet transfer Geneva](https://www.lux-taxi.com/private-aviation-jet-transfer-geneva/): tarmac access, C3, Jet Aviation, TAG Aviation, Signature, Sion and Zurich
- [Boarding schools and private clinics](https://www.lux-taxi.com/swiss-boarding-schools-medical-chauffeur/): Le Rosey, Collège du Léman, Aiglon, Beau Soleil; La Prairie, Genolier, La Colline
- [Mercedes V-Class VIP and S-Class fleet](https://www.lux-taxi.com/mercedes-v-class-vip-s-class-fleet-geneva/): several cars at once for delegations, UN, roadshows, families
- [WEF Davos chauffeur](https://www.lux-taxi.com/wef-davos-chauffeur/): World Economic Forum week, quoted as a full programme

## Services (français)
- [Chauffeur privé de luxe à Genève](https://www.lux-taxi.com/fr/)
- [Transfert aéroport Genève](https://www.lux-taxi.com/fr/transfert-aeroport-geneve/): dès CHF 100, vol suivi, terminal d'aviation privée
- [Transferts stations de ski](https://www.lux-taxi.com/fr/transferts-ski/): Courchevel, Méribel, Val d'Isère, Tignes, Verbier, Chamonix, Megève, Zermatt, dès CHF 250
- [Chauffeur privé business](https://www.lux-taxi.com/fr/chauffeur-prive-business-geneve/)
- [Chauffeur à disposition](https://www.lux-taxi.com/fr/chauffeur-a-disposition-geneve/)
- [Transfert aviation privée](https://www.lux-taxi.com/fr/transfert-aviation-privee-geneve/)
- [Chauffeur internats et cliniques privées](https://www.lux-taxi.com/fr/chauffeur-internats-cliniques-suisse/)
- [Flotte Mercedes Classe V et Classe S](https://www.lux-taxi.com/fr/flotte-mercedes-classe-v-classe-s-geneve/)
- [Chauffeur privé pour diplomates et délégations](https://www.lux-taxi.com/fr/chauffeur-prive-diplomate-geneve/)

## Areas served
Geneva, Lausanne, Montreux, Rolle, Zurich, Sion, Verbier, Zermatt, Gstaad, Crans-Montana, Davos, and the French Alps (Chamonix, Megève, Courchevel, Méribel, Val d'Isère, Tignes).
""")
print('llms.txt ok')
