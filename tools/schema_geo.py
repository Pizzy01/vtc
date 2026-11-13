"""Schema.org pour le GEO : un seul graphe par page (entreprise, site, page, fil d'Ariane, service).
Remplace les blocs LocalBusiness et TaxiService ; garde les blocs FAQPage. Ajoute /llms.txt.
Aucun identifiant Google n'est touché."""
import os, re, json, html
os.chdir('/home/claude/vtc')
B = 'https://www.lux-taxi.com'
BIZ = B + '/#business'; SITE = B + '/#website'

def city(n): return {"@type": "City", "name": n}
AREA_ALL = ["Geneva", "Lausanne", "Montreux", "Zurich", "Verbier", "Zermatt", "Gstaad", "Crans-Montana", "Chamonix", "Megève", "Courchevel", "Davos"]

def offer(prix, unite, txt_en, txt_fr, fr):
    return {"@type": "Offer", "priceCurrency": "CHF",
            "priceSpecification": {"@type": "UnitPriceSpecification", "price": prix, "priceCurrency": "CHF",
                                   **({"unitText": unite} if unite else {}), "valueAddedTaxIncluded": True},
            "description": txt_fr if fr else txt_en}

BUSINESS = {
    "@type": ["LocalBusiness", "TaxiService"],
    "@id": BIZ,
    "name": "Prosper & Co.",
    "alternateName": ["Lux Taxi", "Prosper & Co. Private Chauffeur Geneva"],
    "legalName": "FairTransfert Sàrl",
    "taxID": "CHE-495.106.981",
    "url": B + "/",
    "logo": B + "/assets/site/og.jpg",
    "image": B + "/assets/site/og.jpg",
    "description": "Private chauffeur and luxury limousine service in Geneva: Mercedes S-Class, V-Class VIP and E-Class, airport transfers including private aviation terminals, chauffeur by the hour, corporate chauffeurs, delegations, ski resorts and WEF Davos. Fixed price confirmed before the ride. One contact from booking to drop-off.",
    "telephone": "+41766207850",
    "email": "info@lux-taxi.com",
    "contactPoint": {"@type": "ContactPoint", "contactType": "reservations", "telephone": "+41766207850",
                     "email": "info@lux-taxi.com", "availableLanguage": ["English", "French"],
                     "hoursAvailable": {"@type": "OpeningHoursSpecification",
                                        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                        "opens": "07:00", "closes": "23:00"}},
    "address": {"@type": "PostalAddress", "addressLocality": "Geneva", "addressRegion": "GE", "addressCountry": "CH"},
    "areaServed": [city(c) for c in AREA_ALL] + [{"@type": "Country", "name": "Switzerland"}],
    "knowsLanguage": ["en", "fr"],
    "priceRange": "CHF 80–840",
    "currenciesAccepted": "CHF",
    "makesOffer": [
        {"@type": "Offer", "itemOffered": {"@id": B + "/geneva-airport-transfer/#service"}},
        {"@type": "Offer", "itemOffered": {"@id": B + "/chauffeur-by-the-hour/#service"}},
        {"@type": "Offer", "itemOffered": {"@id": B + "/corporate-chauffeur-geneva/#service"}},
        {"@type": "Offer", "itemOffered": {"@id": B + "/ski-transfers/#service"}},
        {"@type": "Offer", "itemOffered": {"@id": B + "/wef-davos-chauffeur/#service"}},
        {"@type": "Offer", "itemOffered": {"@id": B + "/fr/chauffeur-prive-diplomate-geneve/#service"}},
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
     offers=[(100, None, "Geneva city from CHF 100 in a Mercedes E-Class", "")]), None),
 'ski-transfers/index.html': ('en', 'Ski transfers', dict(
     name="Geneva Ski Transfers", type="Private ski resort transfer",
     desc="Private door-to-door transfers from Geneva Airport to Swiss and French ski resorts in a Mercedes V-Class VIP or E-Class, with room for skis and luggage.",
     area=["Verbier", "Zermatt", "Gstaad", "Crans-Montana", "Chamonix", "Megève", "Courchevel", "Méribel", "Val d'Isère"],
     offers=[(500, None, "Geneva Airport to Verbier from CHF 500 in a Mercedes E-Class", ""),
             (720, None, "Geneva Airport to Täsch (Zermatt) from CHF 720 in a Mercedes E-Class", ""),
             (530, None, "Geneva Airport to Courchevel from CHF 530 in a Mercedes E-Class", "")]), None),
 'chauffeur-by-the-hour/index.html': ('en', 'Chauffeur by the hour', dict(
     name="Chauffeur by the Hour in Geneva", type="Hourly chauffeur service",
     desc="A car and a private chauffeur at your disposal in Geneva, by the hour, 20 km included per hour. Meetings, roadshows, dinners and events.",
     area=["Geneva", "Lausanne", "Montreux", "Zurich"],
     offers=[(80, "hour", "Mercedes E-Class from CHF 80 per hour", ""), (100, "hour", "Mercedes V-Class VIP from CHF 100 per hour", ""),
             (130, "hour", "Mercedes S-Class from CHF 130 per hour", "")]), '/fr/chauffeur-a-disposition-geneve/'),
 'corporate-chauffeur-geneva/index.html': ('en', 'Corporate chauffeur', dict(
     name="Corporate Chauffeur Service Geneva", type="Corporate and executive chauffeur service",
     desc="Executive transport for companies, private banks and international organisations in Geneva, invoiced to the company, with one contact for every booking.",
     area=["Geneva", "Lausanne", "Zurich", "Davos"],
     offers=[(80, "hour", "Mercedes E-Class from CHF 80 per hour", ""), (130, "hour", "Mercedes S-Class from CHF 130 per hour", "")]),
     '/fr/chauffeur-prive-business-geneve/'),
 'wef-davos-chauffeur/index.html': ('en', 'WEF Davos', dict(
     name="WEF Davos Chauffeur Service", type="Chauffeur service for the World Economic Forum in Davos",
     desc="One car and one chauffeur by the day for the World Economic Forum week in Davos, quoted as a full programme: car, chauffeur, fuel, tolls and the chauffeur's stay included.",
     area=["Davos", "Klosters", "Zurich", "Geneva"], offers=[]), None),
 'fr/chauffeur-prive-business-geneve/index.html': ('fr', 'Chauffeur privé business', dict(
     name="Chauffeur privé business à Genève", type="Chauffeur privé pour entreprises et dirigeants",
     desc="Transport de dirigeants pour les entreprises, les banques privées et les organisations internationales à Genève, facturé à la société, avec un seul contact.",
     area=["Geneva", "Lausanne", "Zurich", "Davos"],
     offers=[(80, "heure", "", "Mercedes Classe E dès CHF 80 de l'heure"), (130, "heure", "", "Mercedes Classe S dès CHF 130 de l'heure")]),
     '/corporate-chauffeur-geneva/'),
 'fr/chauffeur-a-disposition-geneve/index.html': ('fr', 'Chauffeur à disposition', dict(
     name="Chauffeur à disposition à Genève", type="Mise à disposition de chauffeur à l'heure",
     desc="Une voiture et un chauffeur privé à votre disposition à Genève, à l'heure, 20 km compris par heure. Rendez-vous, roadshows, dîners, galas et événements.",
     area=["Geneva", "Lausanne", "Montreux", "Zurich"],
     offers=[(80, "heure", "", "Mercedes Classe E dès CHF 80 de l'heure"), (100, "heure", "", "Mercedes Classe V VIP dès CHF 100 de l'heure"),
             (130, "heure", "", "Mercedes Classe S dès CHF 130 de l'heure")]), '/chauffeur-by-the-hour/'),
 'fr/chauffeur-prive-diplomate-geneve/index.html': ('fr', 'Délégations et diplomates', dict(
     name="Chauffeur privé pour diplomates et délégations à Genève", type="Chauffeur privé pour diplomates, missions et délégations",
     desc="Chauffeurs privés pour les missions permanentes, les délégations officielles et les organisations internationales à Genève, avec plusieurs véhicules coordonnés par un seul contact.",
     area=["Geneva", "Lausanne", "Zurich", "Davos"], offers=[]), None),
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

> Private chauffeur and luxury limousine service in Geneva, Switzerland, operated by FairTransfert Sàrl (CHE-495.106.981). Mercedes S-Class, V-Class VIP and E-Class. Fixed price confirmed before the ride. English and French. Bookings 7am to 11pm: +41 76 620 78 50, WhatsApp, info@lux-taxi.com.

## Services (English)
- [Geneva chauffeur service](https://www.lux-taxi.com/): luxury and VIP private chauffeur in Geneva
- [Geneva airport transfer](https://www.lux-taxi.com/geneva-airport-transfer/): Geneva Airport arrivals and private aviation terminal, from CHF 100
- [Chauffeur by the hour](https://www.lux-taxi.com/chauffeur-by-the-hour/): from CHF 80 per hour, 20 km included per hour
- [Corporate chauffeur service](https://www.lux-taxi.com/corporate-chauffeur-geneva/): executives, banks, international organisations
- [Ski transfers](https://www.lux-taxi.com/ski-transfers/): Verbier, Zermatt, Gstaad, Chamonix, Megève, Courchevel
- [WEF Davos chauffeur](https://www.lux-taxi.com/wef-davos-chauffeur/): World Economic Forum week, quoted as a full programme

## Services (français)
- [Chauffeur privé de luxe à Genève](https://www.lux-taxi.com/fr/)
- [Chauffeur privé business](https://www.lux-taxi.com/fr/chauffeur-prive-business-geneve/)
- [Chauffeur à disposition](https://www.lux-taxi.com/fr/chauffeur-a-disposition-geneve/)
- [Chauffeur privé pour diplomates et délégations](https://www.lux-taxi.com/fr/chauffeur-prive-diplomate-geneve/)

## Areas served
Geneva, Lausanne, Montreux, Zurich, Verbier, Zermatt, Gstaad, Crans-Montana, Davos, and the French Alps (Chamonix, Megève, Courchevel).
""")
print('llms.txt ok')
