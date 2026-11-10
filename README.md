# Prosper & Co. — Private Chauffeur Geneva (lux-taxi.com)

Site statique, léger, en anglais (version française prévue ensuite).

## Pages

- `index.html` : accueil (vidéo, services, prix « from », avis, formulaire de devis `#quote`)
- `geneva-airport-transfer/` : transfert aéroport de Genève
- `ski-transfers/` : stations de ski (Suisse et France)
- `chauffeur-by-the-hour/` : chauffeur à l'heure, affaires et événements
- `404.html` : page d'erreur

## Fichiers communs

- `assets/site/prosper.css` et `prosper.js` : styles, animations, apparitions au défilement, envoi du formulaire.
  À chaque modification, changer le numéro `?v=` dans les pages (cache navigateur d'un an).
- `assets/site/*.webp` (800 et 1600 px), `hero.mp4` (200 Ko), `og.jpg` (partage).
- `assets/js/analytics.js` : Google Analytics G-E1BTELQ36P et bannière cookies (inchangés).
- `api/contact.php` : enregistre chaque demande dans `api/data/demandes.csv` puis l'envoie à info@lux-taxi.com.

Les pages sont générées à partir de la maquette Claude (artifact « Lux Taxi — accueil minimaliste »).

## Mise en ligne

Voir `LANCEMENT-SANS-PERTE.md` (GitHub → `tools/deployer.sh` dans la console SSH Infomaniak). Redirections : `redirects.csv`.
