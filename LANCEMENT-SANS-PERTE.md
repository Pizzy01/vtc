# Mettre en ligne sans perdre le référencement

Le passage du WordPress au site actuel, début novembre 2026, a cassé toutes les anciennes adresses connues de Google (404). Cette procédure sert à ce que ça ne se reproduise pas, notamment au lancement du nouveau site.

## La règle d'or

**Une adresse que Google connaît ne disparaît jamais : elle redirige (301) vers la page qui la remplace, en un seul saut.**

La liste de toutes les redirections est dans `redirects.csv`. C'est la seule source : le bloc du `.htaccess` est généré à partir d'elle.

```
python3 tools/redirects.py build   # régénère le bloc REDIRECTIONS du .htaccess
python3 tools/redirects.py test    # doit afficher « 0 erreur(s) »
```

## Avant chaque mise en ligne qui change des adresses (refonte, nouvelle langue, page renommée)

1. **Inventaire** : exporter depuis la Search Console (Performances → Pages, 16 mois) toutes les adresses qui ont des affichages, plus les pages indexées.
2. **Mise à jour de `redirects.csv`** :
   - ajouter chaque adresse actuelle qui change (par exemple `/pages/services.html` → `/geneva-airport-transfer/`) ;
   - **réécrire la destination des anciennes lignes** pour qu'elles pointent directement vers la nouvelle page, sans chaîne ancien → actuel → nouveau ;
   - revoir les motifs : `motif:^fr/.+$` renvoie tout `/fr/...` vers l'accueil. **Il faut le retirer ou le restreindre** dès que le site a de vraies pages `/fr/`.
3. `build` puis `test` : 0 erreur obligatoire.
4. Vérifier dans chaque page : une seule `canonical` en `https://www.lux-taxi.com/...`, `hreflang` FR et EN croisés si le site est bilingue, balise Analytics G-E1BTELQ36P.
5. Mettre à jour `sitemap.xml` (nouvelles adresses uniquement, en www).
6. Tester le formulaire avec un vrai envoi jusqu'à la boîte du client.

## Le jour J

1. Déployer **depuis GitHub uniquement** : aucune modification directe sur le serveur Infomaniak.
2. Contrôler en direct une vingtaine d'anciennes adresses (301 vers la bonne page), `lux-taxi.com` → `www`, `http` → `https`.
3. Search Console : envoyer `sitemap.xml`, inspecter l'accueil et les 3 pages principales, puis demander l'indexation.
4. Analytics : vérifier dans « Temps réel » qu'une visite et un clic WhatsApp remontent.

## Les 4 semaines suivantes

- Chaque lundi (rapport automatique) : nombre de 404 dans la Search Console, pages indexées, position des requêtes cibles.
- Toute nouvelle 404 qui avait des affichages : l'ajouter dans `redirects.csv` le jour même.
- Garder les redirections **au moins 1 an**, et idéalement toujours.
