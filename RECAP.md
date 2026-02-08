# Dermalogica Tracker - Intelligence Concurrentielle

**URL** : https://dermalogica-tracker-production.up.railway.app
**GitHub** : https://github.com/nicoguyon/dermalogica-tracker-fr

---

## Objectif

Dashboard d'intelligence concurrentielle pour **Dermalogica**, permettant de suivre les prix, analyser le positionnement et détecter les signaux concurrentiels face à 3 marques rivales.

## Marques suivies (153 produits)

| Marque | Produits | Prix moyen | Fourchette |
|--------|----------|------------|------------|
| **Dermalogica** | 30 | 95.73€ | 56€ - 179€ |
| Paula's Choice | 45 | 40.12€ | 21.6€ - 60€ |
| Murad | 40 | 61€ | 22€ - 99€ |
| SkinCeuticals | 38 | 87.63€ | 32€ - 185€ |

## Pages du dashboard

### 1. Dashboard (`/`)
Vue d'ensemble avec stats globales, graphiques par marque/site, table comparative. Lien rapide vers l'analyse comparative.

### 2. Produits (`/products`)
Grille de 153 produits avec images, filtres (marque, site, prix, recherche), tri multi-critères et pagination. Chaque carte est cliquable.

### 3. Détail Produit (`/product/:id`)
Fiche produit complète : image, prix actuel vs ancien prix, graphique d'historique de prix (LineChart), métadonnées, lien externe, et liste de produits similaires dans la même catégorie.

### 4. Marques (`/brands`)
Graphique comparatif des prix (moyen, min, max) par marque. Cartes par marque avec Dermalogica mis en avant.

### 5. Analyse Comparative (`/compare`)
- Cartes overview par marque
- Bar chart comparaison des prix
- Radar chart couverture par catégorie (Sérums, Hydratants, Nettoyants, Exfoliants, SPF, Yeux, Traitements)
- Table de positionnement : Dermalogica = "Référence", concurrents avec % de différence

### 6. Comparaison Produit vs Produit (`/product-compare`)
Sélection de 2 à 4 produits via recherche, puis comparaison côte à côte (prix, marque, catégorie, site, historique).

### 7. Alertes (`/alerts`)
58 alertes auto-générées réparties en 5 catégories :
- **Prix** (34) : concurrents moins chers en moyenne ou par produit
- **Gaps de gamme** (4) : catégories où 2+ concurrents existent mais pas Dermalogica
- **Promos concurrents** : détection des baisses de prix > 15%
- **Nouveaux produits** (20) : produits concurrents ajoutés récemment

Chaque alerte inclut une **recommandation d'action** concrète.

### 8. Promotions (`/promotions`)
Produits avec baisse de prix récente, filtrable par période.

### 9. Nouveautés (`/new`)
Derniers produits ajoutés, filtrable par période et marque.

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Frontend | React + Vite + Tailwind CSS |
| Graphiques | Recharts (BarChart, PieChart, RadarChart, LineChart) |
| Backend | Flask (Python) + Gunicorn |
| Base de données | SQLite |
| Déploiement | Railway (Docker) |
| Scraping initial | Playwright (Shopify JSON API pour Dermalogica/Murad) |

## Design

- Palette Dermalogica : noir (`#111827`), gris, blanc
- Police Inter
- Dermalogica toujours distingué visuellement (fond inversé, badge "Référence")
- Dark mode complet
- Responsive mobile avec menu hamburger
- Favicon SVG "d" personnalisé

## Insights clés

- Paula's Choice est **58% moins cher** que Dermalogica en moyenne
- Murad est **36% moins cher**
- SkinCeuticals est **similaire** (-8%)
- 4 gaps de gamme identifiés (moisturizers, cleansers, eye care, toners en naming anglais)
- Dermalogica est le plus cher du marché avec un positionnement premium assumé

## Évolutions possibles

- Scraper automatisé pour rafraîchir les prix quotidiennement
- Notifications email en cas de baisse de prix concurrent
- Export PDF des analyses
- Historique de prix plus long avec graphiques avancés
