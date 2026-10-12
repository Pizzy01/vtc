# LUX-TAXI Genève — Maison de Chauffeurs Privés

Site web officiel haute performance de **LUX-TAXI Genève** (Genève & Alpes Suisses).

## Architecture Technique

- **Frontend** : HTML5 sémantique, Tailwind CSS, CSS Custom Prestige (`vitesse-prestige.css`)
- **Multilingue (i18n)** : Moteur réactif sans rechargement (`assets/js/i18n.js`), 4 langues : Français (FR), Anglais (EN), Allemand (DE), Italien (IT)
- **Conversion** :
  - **B2C Particuliers** : Réservation WhatsApp instantanée avec message pré-rempli et géolocalisé
  - **B2B Entreprises** : Funnel e-mail corporate vers `info@lux-taxi.com`
- **Hébergement Recommandé** : Netlify / Vercel (déploiement automatique continu via GitHub)

## Structure des Pages

- `index.html` : Accueil, simulateur de réservation, grille bento des services, avis vérifiés et aperçu des stations alpines
- `pages/services.html` : Gamme de prestations VIP (Aéroport GVA, Chauffeur Privé à l'Heure, Navettes Ski, Corporate & Salons)
- `pages/flotte.html` : Showroom des véhicules d'exception (Mercedes Classe S, Classe V VIP, Maybach First Class, EQS SUV, Range Rover)
- `pages/destinations.html` : Bento interactif des transferts alpestres et résidences genevoises
- `pages/reservation.html` : Moteur de commande privée avec pré-sélection d'itinéraire

## Déploiement

Ce dépôt est prêt pour un déploiement direct en 1 clic sur Vercel ou Netlify, avec liaison DNS personnalisée sur Infomaniak.
