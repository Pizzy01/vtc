# Charte Graphique & Design System — VITESSE PRESTIGE (VTC & Chauffeur Privé Haut de Gamme)

Bienvenue dans la charte graphique et le Design System officiel de **VITESSE PRESTIGE**. Ce guide rassemble l'ensemble des règles visuelles, typographiques, chromatiques et composants d'interface conçus pour positionner l'entreprise au sommet du transport privé de luxe.

---

## 1. Positionnement & Identité de Marque

* **Positionnement** : Chauffeur privé d'élite, transferts aéroport (Genève, Paris, Côte d'Azur, Alpes) et mise à disposition VIP.
* **Piliers de Marque** :
  1. **Précision Suisse & Ponctualité Absolue** (Prix fixes, suivi des vols en temps réel).
  2. **Esthétique Stealth & Ultra-Luxe** (Véhicules Maybach, Classe S, AMG, Classe V Van VIP).
  3. **Technologie & Fluidité 24/7** (Réservation immédiate, contact WhatsApp direct, expérience digitale réactive).

---

## 2. Palette Chromatique & Tokens CSS

La palette chromatique est inspirée des plus grands constructeurs automobiles de luxe (Rolls-Royce, Mercedes-Maybach, Range Rover) combinée avec l'ambiance nuit & stealth tech.

### Couleurs Principales (Palette Sombre Stealth)

| Nom du Token | Valeur Hex / RGBA | Usage & Application |
| :--- | :--- | :--- |
| `--color-obsidian` | `#0A0A0C` | Arrière-plan principal (Profondeur absolue) |
| `--color-carbon` | `#121216` | Fond des cartes UI et sections surélevées |
| `--color-charcoal` | `#1A1A22` | Fond des champs d'entrée, modales et survol |
| `--color-gold-base` | `#C5A059` | Couleur d'accentuation prestige et icônes |
| `--color-gold-bright` | `#E8C94A` | Accentuation lumineuse et survol d'action |
| `--color-gold-glow` | `rgba(197, 160, 89, 0.25)` | Halo lumineux et bordures actives |
| `--color-emerald` | `#10B981` | Indicateur de disponibilité 24/7 et suivi de vol |
| `--color-text-primary` | `#FFFFFF` | Titres et textes prioritaires |
| `--color-text-secondary` | `#A1A1AA` | Sous-titres, descriptions et métadonnées |
| `--color-text-muted` | `#71717A` | Labels secondaires et mentions légales |

### Dégradés Signature (Signature Gradients)

```css
/* Dégradé Bouton Principal Or Luxe */
--gradient-gold-cta: linear-gradient(135deg, #C5A059 0%, #E8C94A 100%);

/* Dégradé Fond Carte Glassmorphism Or */
--gradient-glass-gold: linear-gradient(180deg, rgba(197, 160, 89, 0.08) 0%, rgba(10, 10, 12, 0.6) 100%);

/* Dégradé Fond Carte Sombre */
--gradient-surface-dark: linear-gradient(180deg, #16161E 0%, #101014 100%);
```

---

## 3. Système Typographique

Le système typographique associe l'élégance moderne de **Plus Jakarta Sans**, la lisibilité universelle d'**Inter**, et la précision technique monospacée de **JetBrains Mono**.

### Hiérarchie des Polices

1. **Titres Majeurs (Display / Headings)** : `Plus Jakarta Sans` ou `Inter` (Font-weight: 800 Extrabold, Letter-spacing: `0.18em` / `tracking-luxury`, Majuscules).
2. **Métriques & Données Techniques** : `JetBrains Mono` (Prix en CHF/EUR, numéros de vol, temps de trajet, capacité passagers/valises).
3. **Corps de Texte & Interfaces** : `Inter` (Font-weight: 400, 500, 600).

```css
/* Configuration Tailwind recommandée */
fontFamily: {
  sans: ['Inter', 'sans-serif'],
  display: ['Plus Jakarta Sans', 'sans-serif'],
  mono: ['JetBrains Mono', 'monospace']
}
```

---

## 4. Effets Visuels & Border Styling

### Glassmorphism & Elevation
```css
/* Effet Verre Dépoli Sombre */
.glass-panel {
  background: rgba(18, 18, 22, 0.75);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

/* Effet Verre Dépoli Or */
.glass-gold-panel {
  background: rgba(197, 160, 89, 0.06);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(197, 160, 89, 0.25);
  box-shadow: 0 0 25px rgba(197, 160, 89, 0.08);
}

/* Halo Or Interactif au Survol */
.gold-glow-hover {
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}
.gold-glow-hover:hover {
  border-color: rgba(197, 160, 89, 0.6);
  box-shadow: 0 0 30px rgba(197, 160, 89, 0.2);
  transform: translateY(-2px);
}
```

---

## 5. Composants UI Majeurs

### 1. Annonce Top Bar (Style Range Rover)
* Hauteur : `36px`
* Fond : `#0F141A` avec bordure inférieure `#1F2937`
* Contenu : Badge vert emeraude clignotant + texte en majuscules avec espacement `tracking-luxury`.

### 2. Widget de Réservation Instantanée
* Intégré directement dans la Hero Section.
* Champs :
  * Type de transfert (Aéroport, Point à Point, Mise à disposition, Longue distance)
  * Adresse de prise en charge (avec autocomplétion)
  * Destination
  * Catégorie de véhicule (Mercedes Classe E, Classe S, Maybach, Classe V, Sprinter)
  * Date & Heure (format mono)
* Bouton d'action CTA Or vibrant avec prix garanti en CHF/EUR.

### 3. Cartes Flotte Automobiles (Inspirées de `carder`)
Chaque carte de véhicule comprend :
* Image haute résolution recadrée avec ombre subtile.
* Badge de catégorie (`AFFAIRE`, `VIP FIRST CLASS`, `VAN EXECUTIVE`).
* Badges de capacités en typographie mono : `<i data-lucide="users"></i> 3 Pax`, `<i data-lucide="briefcase"></i> 3 Valises`.
* Liste d'équipements à bord (Wi-Fi 5G, Eaux minérales, Bouteille de champagne sur demande).
* Bouton "Réserver ce véhicule" ou "Consulter le tarif".

### 4. Barre Sticky Inférieure (Mobile & Desktop)
* Fixée au bas de l'écran avec fond verre dépoli.
* Comprend 2 boutons d'action rapide :
  * **Bouton WhatsApp** (Vert émeraude / Blanc) avec lien immédiat vers `https://wa.me/...`
  * **Bouton Réservation** (Dégradé Or) pour ouvrir le widget ou valider la course.

---

## 6. Déclinaisons des Fichiers dans le Projet

* **Page d'Accueil & VTC Principal** : [index.html](file:///Users/mind4peace/Desktop/vtc/index.html)
* **Démo Vitesse Prestige High-Tech** : [vitesse.html](file:///Users/mind4peace/Desktop/vtc/vitesse.html)
* **CSS Centralisé** : [assets/css/vitesse-prestige.css](file:///Users/mind4peace/Desktop/vtc/assets/css/vitesse-prestige.css)
