# LUX-TAXI Genève — Maison de Chauffeurs Privés

Site web officiel haute performance de **LUX-TAXI Genève** (Genève & Alpes Suisses).

## Architecture Technique

- **Frontend** : HTML5 sémantique, Tailwind CSS, CSS Custom Prestige (`vitesse-prestige.css`)
- **Multilingue (i18n)** : Moteur réactif sans rechargement (`assets/js/i18n.js`), 4 langues : Français (FR), Anglais (EN), Allemand (DE), Italien (IT)
- **Conversion** :
  - **B2C Particuliers** : Réservation WhatsApp instantanée avec message pré-rempli et géolocalisé
  - **Formulaire unique** : `pages/contact.html` → `api/contact.php` → `info@lux-taxi.com` (particuliers et entreprises)
- **Hébergement** : Infomaniak (Apache, PHP 8 pour `api/contact.php`)

## Structure des Pages

- `index.html` : Accueil, simulateur de réservation, grille bento des services, avis vérifiés et aperçu des stations alpines
- `pages/services.html` : Gamme de prestations VIP (Aéroport GVA, Chauffeur Privé à l'Heure, Navettes Ski, Corporate & Salons)
- `pages/flotte.html` : Showroom des véhicules d'exception (Mercedes Classe S, Classe V VIP, Maybach First Class, EQS SUV, Range Rover)
- `pages/destinations.html` : Bento interactif des transferts alpestres et résidences genevoises
- `pages/contact.html` : Formulaire unique de demande de devis (pré-rempli depuis les autres pages)
- `404.html` : Page d'erreur

## Déploiement

Fichiers déposés à la racine du site sur l'hébergement Infomaniak de lux-taxi.com (`.htaccess` inclus).
