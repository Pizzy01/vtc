"""16 nov. : 24/7 + WhatsApp < 10 min (confirmé par Prosper via Issa) ; nouvelle grille à l'heure 90 / 110 / 140 CHF."""
import re, glob, os
os.chdir('/home/claude/vtc')
PEN = "24/7 Operations & Flight Monitoring — Priority WhatsApp Dispatch in under 10 minutes"
PFR = "Opérations 24 h/24, 7 j/7 et suivi des vols — réponse prioritaire sur WhatsApp en moins de 10 minutes"
TXT = [
 # horaires
 ("We reply with a fixed price within the hour, from 7am to 11pm.", "We reply with a fixed price. " + PEN + "."),
 ("We reply with a fixed price within the hour, 7am to 11pm.", "We reply with a fixed price. " + PEN + "."),
 ("We reply within the hour, from 7am to 11pm.", PEN + "."),
 ("We reply within the hour, 7am to 11pm.", PEN + "."),
 ("Nous répondons avec un prix fixe dans l'heure, de 7 h à 23 h.", "Nous répondons avec un prix fixe. " + PFR + "."),
 ("Nous répondons avec un prix ferme en moins d'une heure, de 7 h à 23 h.", "Nous répondons avec un prix ferme. " + PFR + "."),
 ("Nous répondons dans l'heure, de 7 h à 23 h.", PFR + "."),
 ("Réponse dans l'heure, de 7 h à 23 h.", PFR + "."),
 (">&lt; 1 h</span><span ", ">&lt; 10 min</span><span "),
 ("To get your fixed price, 7am to 11pm.", "24/7 operations &amp; flight monitoring — priority WhatsApp dispatch."),
 ("Pour recevoir votre prix ferme, de 7 h à 23 h.", "Opérations 24 h/24 et suivi des vols — réponse prioritaire sur WhatsApp."),
 ("Fixed price within the hour · or ", "24/7 · fixed price in under 10 minutes on WhatsApp · or "),
 ("Prix ferme en moins d'une heure · ou ", "24 h/24 · prix ferme en moins de 10 minutes sur WhatsApp · ou "),
 ("A fixed price, within the hour.", "A fixed price, in under 10 minutes."),
 ("Votre prix ferme, en moins d'une heure.", "Votre prix ferme, en moins de 10 minutes."),
 # tarifs à l'heure (phrases)
 ("Mercedes E-Class from CHF 80 per hour. Mercedes V-Class VIP from CHF 100, for up to 7. Mercedes S-Class from CHF 130.",
  "Mercedes E-Class Business from CHF 90 per hour. Mercedes V-Class VIP Van from CHF 110, for up to 7. Mercedes S-Class First Class from CHF 140."),
 ("From CHF 80 per hour in a Mercedes E-Class, CHF 100 in a V-Class and CHF 130 in an S-Class",
  "From CHF 90 per hour in a Mercedes E-Class Business, CHF 110 in a V-Class VIP Van and CHF 140 in an S-Class First Class"),
 ("rates start from CHF 80 in an E-Class, CHF 100 in a V-Class and CHF 130 in an S-Class",
  "rates start from CHF 90 in an E-Class Business, CHF 110 in a V-Class VIP Van and CHF 140 in an S-Class First Class"),
 ("Mercedes Classe E dès CHF 80 de l'heure. Mercedes Classe V VIP dès CHF 100, jusqu'à 7 personnes. Mercedes Classe S dès CHF 130.",
  "Mercedes Classe E Business dès CHF 90 de l'heure. Mercedes Classe V VIP Van dès CHF 110, jusqu'à 7 personnes. Mercedes Classe S First Class dès CHF 140."),
 ("Dès CHF 80 de l'heure en Mercedes Classe E, CHF 100 en Classe V et CHF 130 en Classe S",
  "Dès CHF 90 de l'heure en Mercedes Classe E Business, CHF 110 en Classe V VIP Van et CHF 140 en Classe S First Class"),
 ("dès CHF 80 de l'heure en Classe E, CHF 100 en Classe V et CHF 130 en Classe S",
  "dès CHF 90 de l'heure en Classe E Business, CHF 110 en Classe V VIP Van et CHF 140 en Classe S First Class"),
 ("CHF 80", "CHF 90"),   # CHF 80 n'est utilisé que pour l'heure
]
GRID = [(r'(>)Mercedes E-Class · 3 pax(</span><span[^>]*>)CHF \d+(<)', r'\1Mercedes E-Class Business · 3 pax\2from CHF 90 / hour\3'),
        (r'(>)Mercedes V-Class · 7 pax(</span><span[^>]*>)CHF \d+(<)', r'\1Mercedes V-Class VIP Van · 7 pax\2from CHF 110 / hour\3'),
        (r'(>)Mercedes S-Class · 2 pax(</span><span[^>]*>)CHF \d+(<)', r'\1Mercedes S-Class First Class · 2 pax\2from CHF 140 / hour\3'),
        (r'(>)Mercedes Classe E · 3 passagers(</span><span[^>]*>)CHF \d+(<)', r'\1Mercedes Classe E Business · 3 passagers\2dès CHF 90 / heure\3'),
        (r'(>)Mercedes Classe V · 7 passagers(</span><span[^>]*>)CHF \d+(<)', r'\1Mercedes Classe V VIP Van · 7 passagers\2dès CHF 110 / heure\3'),
        (r'(>)Mercedes Classe S · 2 passagers(</span><span[^>]*>)CHF \d+(<)', r'\1Mercedes Classe S First Class · 2 passagers\2dès CHF 140 / heure\3')]
LD = re.compile(r'<script type="application/ld\+json">.*?</script>', re.S)
for f in glob.glob('**/index.html', recursive=True) + ['404.html']:
    s = open(f, encoding='utf-8').read(); o = s
    parts = LD.split(s); lds = LD.findall(s)
    out = []
    for p in parts:
        for a, b in TXT: p = p.replace(a, b)
        for a, b in GRID: p = re.sub(a, b, p)
        out.append(p)
    s = out[0] + ''.join(l + p for l, p in zip(lds, out[1:]))
    # FAQPage JSON-LD : mêmes phrases (texte sans balises)
    def fixld(m):
        t = m.group(0)
        if '"FAQPage"' not in t: return t
        for a, b in TXT: t = t.replace(a.replace('&amp;', '&'), b.replace('&amp;', '&'))
        return t
    s = LD.sub(fixld, s)
    if s != o: open(f, 'w', encoding='utf-8').write(s); print('modifié', f)
# JS
p = 'assets/site/prosper.js'; s = open(p, encoding='utf-8').read()
s = s.replace("'Dès CHF 80 / heure'", "'Dès CHF 90 / heure'").replace("'From CHF 80 / hour'", "'From CHF 90 / hour'")
s = s.replace("we reply with a fixed price within the hour (7am–11pm).", "we reply with a fixed price shortly. For priority dispatch in under 10 minutes, message us on WhatsApp (24/7).")
s = re.sub(r"nous répondons avec un prix fixe dans l'heure \(7 h – 23 h\)\.", "nous répondons rapidement avec un prix fixe. Pour une réponse prioritaire en moins de 10 minutes, écrivez-nous sur WhatsApp (24 h/24).", s)
open(p, 'w', encoding='utf-8').write(s)
