"""16 nov. : vocabulaire Grande Remise sur les 8 pages FR (demande d'Issa). Pas de promesse nouvelle non confirmée
(« gratuitement » pour les sièges auto et « en costume » laissés de côté en attendant Prosper)."""
import re, glob, os, json
os.chdir('/home/claude/vtc')
CR = "Centrale de réservation 24 h/24 et suivi des vols en temps réel — réponse WhatsApp en moins de 10 min"
T = [
 # menu et pied de page
 ('<a class="ps-navlink" href="/fr/transfert-aeroport-geneve/">Aéroport</a>', '<a class="ps-navlink" href="/fr/transfert-aeroport-geneve/">Aéroport &amp; VIP</a>'),
 ('<a class="ps-navlink" href="/fr/chauffeur-a-disposition-geneve/">À disposition</a>', '<a class="ps-navlink" href="/fr/chauffeur-a-disposition-geneve/">Mise à disposition</a>'),
 ('<a class="ps-navlink" href="/fr/chauffeur-prive-diplomate-geneve/">Délégations</a>', '<a class="ps-navlink" href="/fr/chauffeur-prive-diplomate-geneve/">Délégations &amp; Diplomatie</a>'),
 ('style="color: #8a857c">Transfert aéroport</a>', 'style="color: #8a857c">Transferts Aéroport &amp; VIP</a>'),
 ('style="color: #8a857c">Transferts ski</a>', 'style="color: #8a857c">Stations de Ski</a>'),
 ('style="color: #8a857c">À disposition</a>', 'style="color: #8a857c">Mise à disposition</a>'),
 ('style="color: #8a857c">Délégations</a>', 'style="color: #8a857c">Délégations &amp; Diplomatie</a>'),
 # titres visibles
 ('>Transfert aéroport Genève · Chauffeur privé<', '>Transfert aéroport Genève · Accueil VIP<'),
 ("Facturé à l'heure,<br>", "Mise à disposition,<br>"),
 ("tout simplement.</span></h2>", "facturée à l'heure.</span></h2>"),
 (">À l'heure<br><span", ">Mise à disposition<br><span"),
 (">ou au trajet.</span>", ">ou forfait au trajet.</span>"),
 (">à l'heure.\"</span>", ">à l'heure.\"</span>"),
 ("Tarifs flotte,<br>", "Tarifs flotte<br>"),
 # corps du texte
 ("Une voiture et un chauffeur privé à votre disposition à Genève, à l'heure.", "Une voiture et un chauffeur privé mis à votre disposition à Genève, facturés à l'heure."),
 ("Combien coûte une Mercedes Classe V VIP à l'heure ?", "Combien coûte la mise à disposition d'une Mercedes Classe V VIP ?"),
 ("une pancarte à votre nom", "pour un accueil personnalisé avec pancarte nominative"),
 ("avec une pancarte à votre nom", "avec un accueil personnalisé et une pancarte nominative"),
 ("Pas de nom sur la pancarte si vous le souhaitez", "Pancarte nominative ou anonyme, selon votre souhait"),
 ("Opérations 24 h/24, 7 j/7 et suivi des vols — réponse prioritaire sur WhatsApp en moins de 10 minutes", CR),
 ("Opérations 24 h/24 et suivi des vols — réponse prioritaire sur WhatsApp.", "Centrale de réservation 24 h/24 et suivi des vols en temps réel — réponse prioritaire sur WhatsApp."),
 ("Oui. Opérations 24 h/24, 7 j/7 et suivi des vols, avec une réponse prioritaire sur WhatsApp en moins de 10 minutes.", "Oui. " + CR + "."),
 ("Un prix ferme, confirmé avant le départ. Nuit, week-end et péages sont compris", "Un tarif forfaitaire fixe, garanti à l'avance. Nuit, week-end et péages sont compris"),
 ("Des Mercedes noires récentes, des chauffeurs professionnels, la même tenue.", "Des Mercedes-Benz noires récentes, des chauffeurs professionnels bilingues français-anglais."),
 ("Mercedes Classe E jusqu'à 3 passagers. Mercedes Classe V VIP jusqu'à 7, avec bagages.", "Flotte Mercedes-Benz : Classe E jusqu'à 3 passagers, Vans Classe V VIP 7 places avec bagages."),
 ("Rentrées, week-ends, sorties et séjours en clinique. Un chauffeur de confiance, un prix ferme, 24 h/24.", "Rentrées, week-ends, sorties et séjours en clinique. Un chauffeur de confiance, un tarif forfaitaire garanti à l'avance, 24 h/24."),
]
LD = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)
def plain(x): return x.replace('&amp;', '&')
for f in sorted(glob.glob('fr/**/index.html', recursive=True)):
    s = open(f, encoding='utf-8').read(); o = s
    for a, b in T: s = s.replace(a, b)
    s = LD.sub(lambda m: m.group(1) + ''.join(m.group(2).replace(plain(a), plain(b)) if False else m.group(2) for _ in [0]) + m.group(3), s)
    def fixld(m):
        t = m.group(2)
        for a, b in T: t = t.replace(plain(a), plain(b))
        return m.group(1) + t + m.group(3)
    s = LD.sub(fixld, s)
    if s != o: open(f, 'w', encoding='utf-8').write(s); print('modifié', f)
# sièges auto : question ajoutée à la page aéroport FR (même promesse que l'EN : « on request »)
p = 'fr/transfert-aeroport-geneve/index.html'; s = open(p, encoding='utf-8').read()
if 'rehausseurs' not in s:
    q, r = "Avez-vous des sièges auto pour les enfants ?", "Oui. Sièges auto et rehausseurs homologués sur demande : précisez l'âge des enfants à la réservation."
    s, n = re.subn(r'(<details[^>]*>\s*<summary[^>]*>Comment réserver \?)', lambda m: m.group(0), s, count=1)
    i = s.find('Comment réserver ?'); j = s.rfind('<', 0, s.rfind('<div', 0, i))
    blk_start = s.rfind('<div', 0, s.rfind('<h3', 0, i))
    blk = s[blk_start:s.index('</div>', s.index('</p>', i)) + 6]
    new = blk.replace('Comment réserver ?', q)
    new = re.sub(r'(<p[^>]*>).*?(</p>)', lambda m: m.group(1) + r + m.group(2), new, count=1, flags=re.S)
    s = s.replace(blk, new + blk, 1)
    s = s.replace('{"@type": "Question", "name": "Comment réserver ?"', '{"@type": "Question", "name": "%s", "acceptedAnswer": {"@type": "Answer", "text": "%s"}}, {"@type": "Question", "name": "Comment réserver ?"' % (q, r), 1)
    open(p, 'w', encoding='utf-8').write(s); print('sièges auto ajoutés')
# EN : la dernière contradiction avec le 24/7
p = 'geneva-airport-transfer/index.html'; s = open(p, encoding='utf-8').read()
s = s.replace("Yes. Book ahead: night requests are answered from 7am.", "Yes. 24/7 operations and flight monitoring — priority WhatsApp dispatch in under 10 minutes, day and night.")
open(p, 'w', encoding='utf-8').write(s)
# menu mobile (prosper.js)
p = 'assets/site/prosper.js'; s = open(p, encoding='utf-8').read()
s = s.replace("'/fr/chauffeur-a-disposition-geneve/': ['À disposition',", "'/fr/chauffeur-a-disposition-geneve/': ['Mise à disposition',").replace("'/fr/chauffeur-prive-diplomate-geneve/': ['Délégations',", "'/fr/chauffeur-prive-diplomate-geneve/': ['Délégations & Diplomatie',")
open(p, 'w', encoding='utf-8').write(s)
