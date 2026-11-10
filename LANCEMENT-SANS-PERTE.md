# Mettre en ligne sans perdre le référencement

Le passage du WordPress au site actuel, début novembre 2026, a cassé toutes les anciennes adresses connues de Google (404). Cette procédure sert à ce que ça ne se reproduise pas, notamment au lancement du nouveau site.

## Mettre en ligne (depuis le 9 nov. 2026)

La branche `serveur/en-ligne-2026-11-09` contient **exactement la version en ligne** : c'est la base de travail. Pour mettre en ligne une branche, dans la console SSH Infomaniak (hébergement taxi-driver-geneva.ch → FTP / SSH → Console SSH) :

```
git clone -q --depth 1 -b <branche> github-vtc:Pizzy01/vtc.git ~/tmp/vtc-deploy && bash ~/tmp/vtc-deploy/tools/deployer.sh <branche> --essai
bash ~/tmp/vtc-deploy/tools/deployer.sh <branche>
```

Le script teste les redirections, fait une sauvegarde dans `~/sauvegardes/`, met à jour `~/sites/lux-taxi.com` sans toucher aux demandes clients (`api/data/*.csv`) ni au fichier de vérification Google, puis contrôle 5 adresses.

## État au 9 novembre 2026

- Les correctifs SEO sont **en ligne** depuis le 9 nov. : 57 redirections exactes + motifs, testées en direct, version unique `https://www.lux-taxi.com`, Analytics G-E1BTELQ36P (vérifié : les visites arrivent), sitemap envoyé à la Search Console.
- Ils ont été appliqués avec `tools/appliquer_correctifs_serveur.py`, **par-dessus les fichiers du serveur**. En effet, le serveur contient une version plus récente que GitHub, venue de l'archive « MISE-A-JOUR 2026-11-06 » : nouveau `api/contact.php` qui enregistre les demandes dans `api/data/demandes.csv`, formulaire qui gère les échecs, traductions et `i18n.js` modifiés.
- La version du serveur a été réimportée dans GitHub le 9 nov. (branche `serveur/en-ligne-2026-11-09`). Les branches plus anciennes (`main`, `claude/audit-corrections`, `seo/redirections-301`) ont des fichiers HTML/PHP **périmés** : ne jamais les mettre en ligne.
- Sauvegarde complète du site avant correctifs : `~/sauvegardes/lux-taxi.com-avant-seo-2026-11-09.tar.gz` sur l'hébergement (avec l'archive .zip, retirée du dossier public).

## Nouveau site (10 nov. 2026)

- Branche `site/studio-2026-11-10` : site Prosper & Co. en anglais, 4 pages à adresses propres (`/`, `/geneva-airport-transfer/`, `/ski-transfers/`, `/chauffeur-by-the-hour/`).
- Les anciennes pages `/pages/*.html` et toutes les anciennes adresses WordPress redirigent en un saut vers la nouvelle page la plus proche. Le motif `^fr/.+$` est gardé tant qu'il n'y a pas de pages `/fr/`.
- Pages légales et page Flotte : pas encore créées.

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
