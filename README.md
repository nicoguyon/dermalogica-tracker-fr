# 🧴 Cosmetique Scraper - Focus Dermalogica

Outil professionnel de scraping et d'analyse comparative pour les produits cosmétiques, spécialisé dans **Dermalogica** et ses concurrents directs.

## 🎯 Marques cibles

- **Dermalogica** (cible principale)
- SkinCeuticals
- Drunk Elephant
- Paula's Choice
- The Ordinary
- Murad
- Dr. Dennis Gross
- Clinique

## ✨ Fonctionnalités

- 🔍 **Scraping multi-sites** : Sephora, Nocibé, Marionnaud, Lookfantastic, Feelunique
- 🏷️ **Filtrage par marque** : Focus sur Dermalogica et concurrents
- 📊 **Analyse comparative** : Comparaison de prix entre marques
- 💰 **Positionnement prix** : Analyse premium/moyen/accessible
- 🆕 **Détection de nouveautés** : Par marque et par site
- 💾 **Base de données SQLite** : Historique des prix automatique
- 📦 **Exports enrichis** : JSON et CSV avec données comparatives
- 🛡️ **Anti-détection** : User-Agent rotation, rate limiting
- 🎨 **Interface CLI riche** : Commandes intuitives avec Rich

## 🚀 Installation

```bash
# Cloner le projet
cd ~/cosmetique-scraper

# Installer les dépendances
pip install -r requirements.txt
```

## 📖 Utilisation

### 1. Scraper des produits

```bash
# Scraper tous les sites (toutes les marques)
python3 cli.py scrape

# Scraper avec filtre par marque
python3 cli.py scrape --brands dermalogica,skinceuticals
python3 cli.py scrape --brands "drunk elephant,the ordinary"

# Scraper un site spécifique avec filtre marque
python3 cli.py scrape --site sephora --brands dermalogica
python3 cli.py scrape --site lookfantastic --brands "paula's choice"

# Options avancées
python3 cli.py scrape --site all --brands dermalogica --max-pages 5
```

### 2. Comparer les marques

```bash
# Comparer les marques par défaut (toutes les marques cibles)
python3 cli.py compare

# Comparer des marques spécifiques
python3 cli.py compare --brands dermalogica,skinceuticals
python3 cli.py compare --brands "drunk elephant,the ordinary,murad"

# Comparer toutes les marques en DB
python3 cli.py compare --brands all
```

**Affiche :**
- Nombre de produits par marque
- Prix moyen, min, max
- Positionnement prix (premium/moyen/accessible)
- Sites où la marque est disponible

### 3. Voir les nouveautés par marque

```bash
# Nouveautés des 7 derniers jours (toutes marques)
python3 cli.py novelties

# Nouveautés pour des marques spécifiques
python3 cli.py novelties --brands dermalogica
python3 cli.py novelties --brands "skinceuticals,drunk elephant"

# Nouveautés des 30 derniers jours
python3 cli.py novelties --days 30 --brands dermalogica
```

### 4. Exporter les données

```bash
# Export standard JSON
python3 cli.py export --format json

# Export enrichi avec analyse comparative
python3 cli.py export --format both --enhanced

# Export avec filtre
python3 cli.py export --format csv --site sephora --limit 100
```

**L'export enrichi ajoute :**
- Prix moyen de la marque
- Positionnement prix
- Écart vs prix moyen de la marque
- Concurrents directs (même fourchette de prix)

### 5. Statistiques

```bash
# Statistiques globales
python3 cli.py stats
```

### 6. Historique des prix

```bash
# Voir l'historique d'un produit (par ID)
python3 cli.py history 42
```

## 📁 Structure du projet

```
cosmetique-scraper/
├── cli.py                  # Interface CLI
├── config.py              # Configuration (marques cibles, sites)
├── requirements.txt       # Dépendances Python
├── database/
│   ├── __init__.py
│   └── models.py         # Gestion SQLite
├── scrapers/
│   ├── __init__.py
│   ├── base.py          # Scraper de base (avec filtrage marque)
│   ├── sephora.py       # Scraper Sephora
│   ├── nocibe.py        # Scraper Nocibé
│   ├── marionnaud.py    # Scraper Marionnaud
│   ├── lookfantastic.py # Scraper Lookfantastic
│   └── feelunique.py    # Scraper Feelunique
├── src/
│   └── analyzer.py      # Module d'analyse comparative
├── exporters/
│   ├── __init__.py
│   ├── json_exporter.py # Export JSON (+ comparaison)
│   └── csv_exporter.py  # Export CSV (+ comparaison)
├── database/
│   └── cosmetique.db    # Base SQLite (auto-créée)
├── exports/             # Fichiers exportés (auto-créé)
└── logs/               # Logs (auto-créé)
```

## 🗄️ Base de données

La base SQLite contient :

- **products** : Tous les produits scrapés
  - ID, site, product_id, name, brand, category, url, image_url
  - first_seen, last_updated

- **prices** : Historique des prix
  - product_id, price, currency, timestamp

- **new_products** : Nouveautés détectées
  - product_id, detected_at

## 📊 Format des données

### Produit enrichi (JSON)

```json
{
  "id": 1,
  "site": "sephora",
  "product_id": "P12345",
  "name": "Daily Microfoliant",
  "brand": "Dermalogica",
  "category": "nouveautes",
  "url": "https://www.sephora.fr/...",
  "image_url": "https://...",
  "current_price": 59.00,
  "brand_avg_price": 62.50,
  "brand_positioning": "premium",
  "price_vs_brand_avg": -3.50,
  "price_vs_brand_avg_percent": -5.6,
  "competitors_count": 3,
  "cheapest_competitor": "SkinCeuticals Micro Polish",
  "cheapest_competitor_price": 58.00,
  "first_seen": "2026-02-08 10:00:00",
  "last_updated": "2026-02-08 10:00:00"
}
```

### Export comparaison (CSV)

| Marque | Nb_Produits | Prix_Moyen | Prix_Min | Prix_Max | Prix_Median | Positionnement | Sites |
|--------|------------|------------|----------|----------|-------------|----------------|-------|
| Dermalogica | 24 | 62.50 | 29.00 | 119.00 | 59.00 | premium | SEP, NOC, MAR |
| SkinCeuticals | 18 | 89.00 | 45.00 | 165.00 | 85.00 | premium | SEP, LOO |

## 🛡️ Fonctionnalités anti-détection

- ✅ User-Agent aléatoire (rotation)
- ✅ Rate limiting (2s entre requêtes)
- ✅ Exponential backoff sur échec
- ✅ Timeout configurables
- ✅ Retry automatique (3 tentatives)

## 🎯 Commandes disponibles

| Commande | Description |
|----------|-------------|
| `scrape` | Scraper des produits (avec filtre marque) |
| `compare` | Comparer prix et stats entre marques |
| `novelties` | Nouveautés par marque |
| `export` | Exporter les données (mode enrichi disponible) |
| `new` | Afficher les nouveautés globales |
| `stats` | Statistiques de la base |
| `history` | Historique prix d'un produit |
| `--help` | Aide pour chaque commande |

## ⚙️ Configuration

Éditer `config.py` :

```python
# Marques cibles
TARGET_BRANDS = [
    'dermalogica',
    'skinceuticals',
    'drunk elephant',
    # ...
]

# Rate limiting
REQUEST_DELAY = 2  # Secondes entre requêtes
REQUEST_TIMEOUT = 10  # Timeout requête

# Retry
MAX_RETRIES = 3
RETRY_DELAY = 5
```

## 📝 Logging

Les logs sont sauvegardés dans `logs/scraper.log` avec :
- Niveau : INFO par défaut
- Format : timestamp - module - niveau - message
- Rotation automatique

## 🔧 Développement

### Ajouter un nouveau site

1. Créer `scrapers/nouveau_site.py`
2. Hériter de `BaseScraper`
3. Implémenter `scrape_products()` avec support du paramètre `brands`
4. Ajouter dans `config.py` SITES
5. Importer dans `scrapers/__init__.py`

### Structure d'un scraper

```python
from .base import BaseScraper
from typing import Optional, List, Dict

class NouveauSiteScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            site_name='nouveau_site',
            base_url='https://...'
        )

    def scrape_products(self, category: str = 'nouveautes',
                       max_pages: int = 3,
                       brands: Optional[List[str]] = None) -> List[Dict]:
        # Utiliser self._match_brands() pour filtrer
        pass
```

## 📦 Dépendances

- `requests` : Requêtes HTTP
- `beautifulsoup4` : Parsing HTML
- `lxml` : Parser rapide
- `fake-useragent` : User-Agent aléatoires
- `pandas` : Manipulation données (CSV)
- `click` : Interface CLI
- `rich` : Interface colorée

## 💡 Exemples d'utilisation

### Cas 1 : Veille Dermalogica

```bash
# 1. Scraper Dermalogica sur tous les sites
python3 cli.py scrape --brands dermalogica --max-pages 5

# 2. Voir les nouveautés Dermalogica
python3 cli.py novelties --brands dermalogica --days 30

# 3. Export enrichi
python3 cli.py export --format both --enhanced
```

### Cas 2 : Analyse concurrentielle

```bash
# 1. Scraper toutes les marques concurrentes
python3 cli.py scrape --brands "dermalogica,skinceuticals,drunk elephant" --max-pages 3

# 2. Comparer les marques
python3 cli.py compare --brands "dermalogica,skinceuticals,drunk elephant"

# 3. Export comparaison
python3 cli.py export --format csv --enhanced
```

### Cas 3 : Focus Lookfantastic

```bash
# Scraper uniquement Lookfantastic pour marques premium
python3 cli.py scrape --site lookfantastic --brands "dermalogica,skinceuticals,dr. dennis gross"
```

## 🐛 Troubleshooting

### Erreur de connexion
- Vérifier la connexion internet
- Augmenter `REQUEST_TIMEOUT` dans config.py

### Aucun produit trouvé
- Les sites ont peut-être changé leur structure HTML
- Vérifier les logs dans `logs/scraper.log`
- Adapter les sélecteurs CSS dans le scraper

### Trop de requêtes (429)
- Augmenter `REQUEST_DELAY` dans config.py
- Réduire `max_pages` lors du scraping

### Marques non détectées
- Vérifier les alias dans `BRAND_ALIASES` dans config.py
- Ajouter des variations de noms de marques

## 📜 Licence

MIT License - Libre d'utilisation

## 👨‍💻 Auteur

Créé avec ❤️ par Claude Sonnet 4.5

---

**Note** : Ce projet est à usage éducatif et de veille concurrentielle. Respectez les conditions d'utilisation des sites scrapés.
