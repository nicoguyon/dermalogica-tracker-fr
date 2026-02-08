# Guide d'utilisation - Cosmetique Scraper

## Installation

```bash
# Cloner ou télécharger le projet
cd cosmetique-scraper

# Installer avec le script automatique
bash setup.sh

# OU installation manuelle :
pip install -r requirements.txt
playwright install chromium
```

## Activer l'environnement virtuel

```bash
source venv/bin/activate
```

## Commandes CLI

### 1. Scraper des produits

#### Scraper Sephora
```bash
python cli.py scrape --source sephora
```

#### Scraper avec limite
```bash
python cli.py scrape --source sephora --limit 50
```

#### Scraper les nouveautés uniquement
```bash
python cli.py scrape --source nocibe --new-only
```

#### Scraper tous les sites
```bash
python cli.py scrape --all
```

#### Voir le navigateur (mode debug)
```bash
python cli.py scrape --source sephora --no-headless
```

### 2. Exporter les données

#### Export JSON
```bash
python cli.py export --format json --output mes_produits.json
```

#### Export CSV
```bash
python cli.py export --format csv --output mes_produits.csv
```

#### Export avec filtre par source
```bash
python cli.py export --format json --source sephora
```

#### Export des nouveautés uniquement
```bash
python cli.py export --format csv --new-only
```

### 3. Statistiques

#### Stats globales
```bash
python cli.py stats
```

#### Stats par source
```bash
python cli.py stats --source sephora
```

### 4. Nettoyage de la base

#### Supprimer les anciennes données
```bash
python cli.py clean --days 30
```

#### Vider complètement la base
```bash
python cli.py clean --all
```

## Exemples de workflows

### Workflow 1 : Scraping quotidien
```bash
# Scraper les nouveautés de tous les sites
python cli.py scrape --all --new-only

# Voir les stats
python cli.py stats

# Exporter en JSON
python cli.py export --format json --new-only
```

### Workflow 2 : Analyse comparative
```bash
# Scraper chaque site séparément
python cli.py scrape --source sephora --limit 100
python cli.py scrape --source nocibe --limit 100

# Exporter par source
python cli.py export --format csv --source sephora --output sephora.csv
python cli.py export --format csv --source nocibe --output nocibe.csv
```

### Workflow 3 : Surveillance marque
```bash
# Scraper tous les produits
python cli.py scrape --all

# Filtrer dans la base via Python
python -c "
from src.database import Database
db = Database()
products = db.get_products(brand='Dior')
print(f'{len(products)} produits Dior trouvés')
"
```

## Localisation des fichiers

```
~/cosmetique-scraper/
├── data/
│   └── products.db          # Base de données SQLite
├── exports/
│   ├── products_*.json      # Exports JSON
│   └── products_*.csv       # Exports CSV
└── logs/
    └── scraper_*.log        # Logs quotidiens
```

## Utilisation programmatique (Python)

```python
from src.scrapers import get_scraper
from src.database import Database
from src.exporters import JSONExporter

# Scraper
with get_scraper('sephora', headless=True) as scraper:
    products = scraper.scrape_products(limit=20)

# Sauvegarder en base
db = Database()
db.add_products(products)

# Exporter
JSONExporter.export(products, Path('mes_produits.json'))
```

## Troubleshooting

### Erreur Playwright
```bash
# Réinstaller Chromium
playwright install chromium --force
```

### Base de données corrompue
```bash
# Supprimer et recréer
rm ~/cosmetique-scraper/data/products.db
python cli.py scrape --source sephora --limit 10
```

### Timeout lors du scraping
- Augmenter le timeout dans `src/utils/config.py`
- Utiliser `--no-headless` pour voir ce qui bloque
- Vérifier votre connexion internet

## Performance

- **Scraping Sephora** : ~2-3 produits/seconde
- **Scraping Nocibé** : ~2-3 produits/seconde
- **Base de données** : SQLite (illimité, léger)
- **RAM** : ~200-300 MB par navigateur

## Bonnes pratiques

1. ✅ Utiliser `--limit` lors des tests
2. ✅ Exporter régulièrement les données
3. ✅ Nettoyer les anciennes données (`clean --days 30`)
4. ✅ Vérifier les logs en cas d'erreur
5. ❌ Ne pas scraper trop fréquemment (risque de blocage IP)

## Rate limiting

Le scraper intègre un délai de 1 seconde entre chaque requête pour éviter la détection.
Modifiable dans `src/utils/config.py` :

```python
SCRAPER_CONFIG = {
    "rate_limit_delay": 1,  # secondes
}
```
