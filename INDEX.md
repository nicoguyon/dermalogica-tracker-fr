# 🧴 Cosmetique Scraper

## Outil de scraping professionnel de produits cosmétiques

> Scraping modulaire et automatisé des prix et nouveautés cosmétiques depuis Sephora, Nocibé et Marionnaud.

---

## 📋 Vue d'ensemble

**Cosmetique Scraper** est un outil Python complet pour extraire, stocker et exporter les données de produits cosmétiques depuis les principaux sites français.

### ✨ Fonctionnalités principales

- 🔍 **Scraping automatisé** - Extraction intelligente avec Playwright
- 💾 **Base de données** - Stockage SQLite avec indexation
- 📤 **Exports multiples** - JSON et CSV
- 📊 **Statistiques** - Analyse des données scrapées
- 🎨 **Interface CLI** - Commandes intuitives avec Rich
- 🔧 **Architecture modulaire** - Facilement extensible
- ⚙️ **Configuration avancée** - Rate limiting, retry, logs
- 🚀 **Scripts d'installation** - Setup en 1 commande

### 🏪 Sites supportés

| Site | Status | Fonctionnalités |
|------|--------|-----------------|
| Sephora | ✅ Complet | Prix, nouveautés, détails |
| Nocibé | ✅ Complet | Prix, nouveautés, détails |
| Marionnaud | 🚧 En dev | À implémenter |

---

## 🚀 Démarrage rapide

### Installation (1 minute)

```bash
cd ~/cosmetique-scraper
bash setup.sh
source venv/bin/activate
```

### Première utilisation (30 secondes)

```bash
# Scraper 10 produits Sephora
python cli.py scrape --source sephora --limit 10

# Voir les statistiques
python cli.py stats

# Exporter en JSON
python cli.py export --format json
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | Documentation principale |
| [QUICKREF.md](QUICKREF.md) | ⚡ Référence ultra-rapide |
| [USAGE.md](USAGE.md) | Guide complet d'utilisation |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Architecture technique |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Ajouter un nouveau scraper |
| [CHANGELOG.md](CHANGELOG.md) | Historique des versions |
| [PROJECT_STRUCTURE.txt](PROJECT_STRUCTURE.txt) | Arborescence du projet |

---

## 💻 Exemples d'utilisation

### CLI - Scraping

```bash
# Scraper un site spécifique
python cli.py scrape --source sephora --limit 50

# Scraper tous les sites
python cli.py scrape --all

# Nouveautés uniquement
python cli.py scrape --source nocibe --new-only

# Mode debug (voir le navigateur)
python cli.py scrape --source sephora --no-headless --limit 5
```

### CLI - Export & Stats

```bash
# Export JSON
python cli.py export --format json --output produits.json

# Export CSV d'une source
python cli.py export --format csv --source sephora

# Statistiques globales
python cli.py stats

# Stats par source
python cli.py stats --source nocibe
```

### Makefile - Workflows

```bash
make install          # Installer
make scrape-sephora   # Scraper Sephora
make scrape-all       # Scraper tous les sites
make workflow-daily   # Workflow quotidien complet
make stats            # Statistiques
```

### Python - Utilisation programmatique

```python
from src.scrapers import get_scraper
from src.database import Database
from src.exporters import JSONExporter

# Scraper
with get_scraper('sephora', headless=True) as scraper:
    products = scraper.scrape_products(limit=20)

# Sauvegarder
db = Database()
db.add_products(products)

# Exporter
JSONExporter.export(products, 'output.json')
```

---

## 🏗️ Architecture

### Structure modulaire

```
src/
├── scrapers/       # Scrapers par site (extensible)
├── database/       # Gestion SQLite
├── exporters/      # Export JSON/CSV
└── utils/          # Config, logs, helpers
```

### Flux de données

```
Playwright → Scraper → Product → Database → Exporter → JSON/CSV
```

### Points forts

- ✅ **Abstraction** - Classe `BaseScraper` pour tous les scrapers
- ✅ **Robustesse** - Retry automatique, rate limiting, logs
- ✅ **Performance** - SQLite avec index, scraping optimisé
- ✅ **Maintenance** - Code documenté, architecture claire
- ✅ **Extensibilité** - Ajout facile de nouveaux sites

---

## 📊 Statistiques du projet

| Métrique | Valeur |
|----------|--------|
| Lignes de code | ~1,268 |
| Fichiers Python | 15 |
| Scrapers actifs | 2 (Sephora, Nocibé) |
| Formats d'export | 2 (JSON, CSV) |
| Commandes CLI | 4 principales |
| Commandes Make | 15+ |
| Documentation | 7 fichiers |

---

## 🎯 Cas d'usage

### 1. Veille concurrentielle
Suivre les prix et nouveautés de la concurrence en temps réel.

### 2. Analyse de marché
Identifier les tendances, marques populaires, gammes de prix.

### 3. Alertes prix
Détecter les promotions et baisses de prix (roadmap).

### 4. Catalogue produits
Constituer une base de données produits à jour.

### 5. Étude consommateur
Analyser l'offre disponible par catégorie/marque.

---

## 🛠️ Technologies

| Technologie | Usage |
|-------------|-------|
| Python 3.10+ | Langage principal |
| Playwright | Scraping web |
| SQLite | Base de données |
| Click | Interface CLI |
| Rich | Output formaté |

---

## 📈 Roadmap

### Version 1.1
- [ ] Scraper Marionnaud complet
- [ ] Support des catégories
- [ ] Filtres avancés

### Version 1.2
- [ ] Historique des prix
- [ ] Alertes de prix
- [ ] Export Excel

### Version 2.0
- [ ] API REST
- [ ] Dashboard web
- [ ] Scraping parallèle
- [ ] Notifications email/Telegram

---

## 🤝 Contribution

Les contributions sont bienvenues ! Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour :
- Ajouter un nouveau site
- Améliorer un scraper existant
- Proposer de nouvelles fonctionnalités

---

## 📝 Licence

MIT License - Libre d'utilisation et modification.

---

## 👤 Auteur

Créé avec Claude Code (Anthropic) - Février 2026

---

## 📞 Support

- 📖 Documentation complète dans le projet
- 🐛 Issues : Créer un ticket GitHub (si projet public)
- 💬 Questions : Consulter USAGE.md et QUICKREF.md

---

**🌟 N'hésitez pas à personnaliser et étendre cet outil selon vos besoins !**
