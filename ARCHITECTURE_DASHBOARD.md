# 🏗️ Architecture du Dashboard

## Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT                              │
│                    (Navigateur Web)                          │
└─────────────────────────────────────────────────────────────┘
                            ↓ HTTP
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Pages                                                │  │
│  │  ├── Dashboard.jsx  (Stats + Graphiques)            │  │
│  │  ├── Products.jsx   (Liste + Filtres)               │  │
│  │  ├── Brands.jsx     (Comparaison marques)           │  │
│  │  ├── Promotions.jsx (Baisses de prix)               │  │
│  │  └── NewProducts.jsx (Nouveautés)                   │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Components                                           │  │
│  │  ├── Navbar.jsx     (Navigation)                     │  │
│  │  ├── StatCard.jsx   (Cartes stats)                   │  │
│  │  └── ProductCard.jsx (Cartes produits)               │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Utils                                                │  │
│  │  └── api.js         (Client HTTP Axios)              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  Stack: React 18 + Vite + TailwindCSS + Recharts           │
│  Port: 3000 (dev) | 80 (prod)                              │
└─────────────────────────────────────────────────────────────┘
                            ↓ REST API
┌─────────────────────────────────────────────────────────────┐
│                     BACKEND (Flask)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Endpoints                                        │  │
│  │  ├── GET /api/stats           (Stats globales)       │  │
│  │  ├── GET /api/brands          (Liste marques)        │  │
│  │  ├── GET /api/products        (Liste produits)       │  │
│  │  ├── GET /api/new-products    (Nouveautés)           │  │
│  │  ├── GET /api/promotions      (Promotions)           │  │
│  │  ├── GET /api/price-history   (Historique prix)      │  │
│  │  ├── GET /api/sites           (Liste sites)          │  │
│  │  └── GET /api/search          (Recherche)            │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Business Logic                                       │  │
│  │  ├── Requêtes SQL optimisées                        │  │
│  │  ├── Filtres et pagination                          │  │
│  │  ├── Calculs stats (moyennes, min/max)              │  │
│  │  └── Détection promotions                           │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  Stack: Flask 3.0 + Flask-CORS                             │
│  Port: 5000                                                 │
└─────────────────────────────────────────────────────────────┘
                            ↓ SQL
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE (SQLite)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Tables                                               │  │
│  │  ├── products      (Infos produits)                  │  │
│  │  ├── prices        (Historique prix)                 │  │
│  │  └── new_products  (Nouveautés détectées)            │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Indexes                                              │  │
│  │  ├── idx_products_site                               │  │
│  │  ├── idx_prices_product                              │  │
│  │  └── idx_new_products_detected                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  Fichier: database/cosmetique.db                            │
└─────────────────────────────────────────────────────────────┘
```

## Flux de données

### 1. Affichage de la page Dashboard

```
User ouvre /
    ↓
React Router → Dashboard.jsx
    ↓
useEffect() déclenche 3 appels API parallèles:
    ├── fetchStats()    → GET /api/stats
    ├── fetchBrands()   → GET /api/brands
    └── fetchSites()    → GET /api/sites
    ↓
Flask exécute requêtes SQL:
    ├── COUNT produits, marques, sites
    ├── AVG/MIN/MAX prix
    └── Nouveautés 7j, promotions
    ↓
Backend retourne JSON
    ↓
Frontend met à jour state
    ↓
React re-render avec données
    ↓
Recharts génère graphiques
```

### 2. Filtrage de produits

```
User modifie filtres (marque, prix, recherche)
    ↓
handleFilterChange() met à jour state
    ↓
useEffect() détecte changement filters
    ↓
loadProducts() appelé avec nouveaux params
    ↓
GET /api/products?brand=dermalogica&min_price=20&max_price=100
    ↓
Flask construit requête SQL dynamique:
    WHERE brand = ? AND price >= ? AND price <= ?
    ↓
Backend exécute query + pagination
    ↓
Retourne { products: [...], pagination: {...} }
    ↓
Frontend affiche grille + pagination
```

### 3. Détection de promotions

```
User ouvre /promotions
    ↓
Promotions.jsx → fetchPromotions(days=7)
    ↓
GET /api/promotions?days=7
    ↓
Flask exécute requête complexe:
    - Récupère prix actuel
    - Compare avec prix d'il y a 7j
    - Calcule % réduction
    - Filtre price < old_price
    ↓
Retourne produits triés par % réduction
    ↓
Frontend affiche avec badge -X%
```

## Architecture Docker

```
docker-compose.yml
    ↓
    ├── Service: backend
    │   ├── Build: backend/Dockerfile
    │   ├── Port: 5000:5000
    │   ├── Volume: ./database (read-only)
    │   └── Env: FLASK_ENV=production
    │
    └── Service: frontend
        ├── Build: frontend/Dockerfile
        │   ├── Stage 1: Build React (node:20-alpine)
        │   └── Stage 2: Serve static (nginx:alpine)
        ├── Port: 80:80
        ├── Depends: backend
        └── Nginx reverse proxy: /api → backend:5000
```

## Patterns de conception

### Frontend

- **Component Pattern** : Composants réutilisables (StatCard, ProductCard)
- **Custom Hooks** : useState, useEffect pour state management
- **API Client Pattern** : Module api.js centralisé pour toutes les requêtes
- **Route-based Code Splitting** : React Router pour navigation SPA
- **Utility-First CSS** : TailwindCSS pour styling rapide

### Backend

- **RESTful API** : Endpoints standards (GET /resource)
- **Repository Pattern** : Séparation logique DB / business logic
- **Pagination Pattern** : Limit/Offset pour grandes datasets
- **Query Builder Pattern** : Construction dynamique requêtes SQL
- **Error Handling** : Try/catch + codes HTTP appropriés

## Sécurité

### Frontend
- ✅ Variables d'env pour URLs API (pas de hardcode)
- ✅ Sanitization des inputs utilisateur
- ✅ HTTPS en production (via Nginx)

### Backend
- ✅ CORS configuré (whitelist origins)
- ✅ Requêtes SQL paramétrées (protection injection)
- ✅ Validation des inputs (types, ranges)
- ✅ Rate limiting (à ajouter en production)

### Database
- ✅ Read-only volume en Docker
- ✅ Indexes pour performance
- ✅ Foreign keys pour intégrité

## Performance

### Frontend
- ⚡ Vite build ultra-rapide (< 10s)
- ⚡ Code splitting automatique par route
- ⚡ Lazy loading images
- ⚡ Debounce sur recherche
- ⚡ Mise en cache localStorage (dark mode)

### Backend
- ⚡ Indexes SQL sur colonnes fréquentes
- ⚡ Pagination pour limiter data transfert
- ⚡ Requêtes optimisées (JOINs, subqueries)
- ⚡ Connection pooling SQLite

### Infrastructure
- ⚡ Nginx pour serving static files
- ⚡ Gzip compression
- ⚡ Docker multi-stage builds (image légère)

## Scalabilité

### Actuelle (SQLite + Flask simple)
- ✅ Support ~ 100K produits
- ✅ ~ 10-50 requêtes/sec
- ✅ Parfait pour usage personnel/équipe

### Pour scale (si nécessaire)
- 📈 Remplacer SQLite par PostgreSQL
- 📈 Ajouter Redis pour cache
- 📈 Gunicorn + multiple workers
- 📈 Load balancer (Nginx)
- 📈 CDN pour assets frontend

## Monitoring & Logs

### Développement
- Console.log frontend (React DevTools)
- Flask logs stdout
- Docker logs: `docker-compose logs -f`

### Production (à ajouter)
- Sentry pour error tracking
- Prometheus + Grafana pour métriques
- ELK Stack pour logs centralisés

## Maintenance

### Mises à jour dépendances
```bash
# Frontend
cd frontend
npm update
npm audit fix

# Backend
cd backend
pip install --upgrade -r requirements.txt
```

### Backup database
```bash
cp database/cosmetique.db database/backup-$(date +%Y%m%d).db
```

### Monitoring espace disque
```bash
du -sh database/
```

---

**Architecture évolutive et maintenable** ✨
