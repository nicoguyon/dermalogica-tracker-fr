# Référence Rapide - Cosmetique Scraper

## Installation (1 commande)

```bash
cd ~/cosmetique-scraper && bash setup.sh
```

## Commandes essentielles

```bash
# Activer l'environnement
source venv/bin/activate

# Scraper un site
python cli.py scrape --source sephora --limit 20

# Scraper tous les sites
python cli.py scrape --all

# Exporter
python cli.py export --format json

# Statistiques
python cli.py stats
```

## Makefile (encore plus rapide)

```bash
make install          # Installer
make scrape-sephora   # Scraper Sephora
make scrape-all       # Scraper tous
make export-json      # Export JSON
make stats            # Stats
make workflow-daily   # Workflow quotidien
```

## Script interactif

```bash
bash quickstart.sh
```

## Structure des dossiers

```
~/cosmetique-scraper/
├── data/products.db           # Base SQLite
├── exports/*.json             # Exports JSON
├── exports/*.csv              # Exports CSV
└── logs/scraper_*.log         # Logs
```

## Utilisation Python

```python
from src.scrapers import get_scraper
from src.database import Database

# Scraper
with get_scraper('sephora') as scraper:
    products = scraper.scrape_products(limit=10)

# Sauvegarder
db = Database()
db.add_products(products)

# Stats
print(db.get_stats())
```

## Options CLI

| Option | Description |
|--------|-------------|
| `--source` | Site à scraper (sephora, nocibe) |
| `--all` | Tous les sites |
| `--limit` | Nombre max de produits |
| `--new-only` | Nouveautés uniquement |
| `--no-headless` | Voir le navigateur |
| `--format` | Format export (json, csv) |
| `--output` | Fichier de sortie |

## Troubleshooting rapide

```bash
# Réinstaller Playwright
playwright install chromium --force

# Voir le navigateur (debug)
python cli.py scrape --source sephora --no-headless --limit 5

# Vider la base
python cli.py clean --all

# Tests
python test_scraper.py
```

## Support

- Documentation : `README.md`
- Usage détaillé : `USAGE.md`
- Architecture : `ARCHITECTURE.md`
- Contribuer : `CONTRIBUTING.md`
- Exemples : `examples/basic_usage.py`
