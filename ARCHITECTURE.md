# Architecture - Cosmetique Scraper

## Vue d'ensemble

Outil de scraping modulaire pour extraire les données de produits cosmétiques depuis Sephora, Nocibé et Marionnaud.

## Structure du projet

```
cosmetique-scraper/
├── src/
│   ├── __init__.py
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── base.py              # Classe abstraite de base
│   │   ├── sephora.py           # Scraper Sephora
│   │   ├── nocibe.py            # Scraper Nocibé
│   │   └── marionnaud.py        # Scraper Marionnaud
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db.py                # Gestion SQLite
│   │   └── models.py            # Modèles de données
│   ├── exporters/
│   │   ├── __init__.py
│   │   ├── json_exporter.py     # Export JSON
│   │   └── csv_exporter.py      # Export CSV
│   └── utils/
│       ├── __init__.py
│       ├── logger.py            # Configuration logging
│       └── config.py            # Configuration globale
├── cli.py                        # Interface CLI
├── requirements.txt
├── README.md
└── .gitignore
```

## Architecture des composants

### 1. Scrapers (src/scrapers/)

**BaseScraper (base.py)**
- Classe abstraite définissant l'interface commune
- Méthodes obligatoires : `scrape_products()`, `scrape_product_details()`
- Gestion Playwright commune
- Rate limiting intégré

**Scrapers spécifiques**
- Implémentent BaseScraper
- Logique de sélection CSS/XPath adaptée à chaque site
- Gestion des pagination
- Extraction des prix, nouveautés, détails produit

### 2. Database (src/database/)

**Modèle de données (models.py)**
```python
Product:
  - id (UUID)
  - source (str: sephora|nocibe|marionnaud)
  - product_id (str: ID du site)
  - name (str)
  - brand (str)
  - price (float)
  - currency (str)
  - url (str)
  - image_url (str)
  - category (str)
  - is_new (bool)
  - scraped_at (datetime)
  - metadata (JSON)
```

**Database Manager (db.py)**
- Connexion SQLite
- CRUD operations
- Requêtes avancées (filtres, recherche)
- Migration schema

### 3. Exporters (src/exporters/)

**JSONExporter**
- Export en JSON structuré
- Groupement par source
- Pretty print

**CSVExporter**
- Export CSV plat
- Headers configurables
- Gestion encodage UTF-8

### 4. Utils (src/utils/)

**Logger**
- Logs fichier + console
- Niveaux configurables
- Rotation automatique

**Config**
- Paramètres globaux
- Chemins de fichiers
- Settings Playwright

### 5. CLI (cli.py)

**Commandes principales**
```bash
# Scraper un site
python cli.py scrape --source sephora --category skincare

# Scraper tous les sites
python cli.py scrape --all

# Scraper les nouveautés uniquement
python cli.py scrape --source nocibe --new-only

# Export
python cli.py export --format json --output products.json
python cli.py export --format csv --output products.csv

# Statistiques
python cli.py stats

# Nettoyage base de données
python cli.py clean --days 30
```

## Flux de données

1. **CLI** → Parse arguments
2. **Scraper** → Démarre Playwright
3. **Scraper** → Navigue et extrait données
4. **Database** → Stocke produits
5. **Exporter** → Génère fichiers sortie

## Gestion des erreurs

- Retry automatique (3 tentatives)
- Logs détaillés des erreurs
- Continuation même si un site échoue
- Timeout configurable

## Performance

- Scraping asynchrone avec Playwright
- Mise en cache des pages
- Rate limiting (délai entre requêtes)
- Connexion DB en pool

## Évolutivité

- Ajout facile de nouveaux sites (hériter de BaseScraper)
- Nouveaux formats d'export (hériter de BaseExporter)
- Configuration extensible
- Tests unitaires par composant
