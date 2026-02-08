# 🚀 DÉMARREZ ICI

Bienvenue dans **Cosmetique Scraper** !

---

## ⚡ Installation (2 minutes)

```bash
cd ~/cosmetique-scraper
bash setup.sh
source venv/bin/activate
```

---

## 🎯 Première utilisation (30 secondes)

```bash
# Test rapide (5 produits)
python cli.py scrape --source sephora --limit 5

# Voir les résultats
python cli.py stats

# Exporter
python cli.py export --format json
```

---

## 📖 Documentation

Choisissez selon votre besoin :

| Si vous voulez... | Consultez... |
|-------------------|--------------|
| ⚡ Démarrer immédiatement | **QUICKREF.md** (1 page) |
| 📖 Comprendre toutes les fonctionnalités | **USAGE.md** (guide complet) |
| 🏗️ Comprendre l'architecture | **ARCHITECTURE.md** |
| 🛠️ Ajouter un nouveau site | **CONTRIBUTING.md** |
| 🎨 Voir une démo visuelle | **DEMO.txt** |
| 📊 Vue d'ensemble du projet | **INDEX.md** |

---

## 🔥 Commandes les plus utilisées

```bash
# Scraping
python cli.py scrape --source sephora --limit 20
python cli.py scrape --all
python cli.py scrape --source nocibe --new-only

# Export
python cli.py export --format json
python cli.py export --format csv

# Stats
python cli.py stats

# Nettoyage
python cli.py clean --days 30
```

---

## 🎨 Interface interactive

Préférez un menu interactif ?

```bash
bash quickstart.sh
```

---

## 🛠️ Makefile (raccourcis)

```bash
make scrape-sephora   # Scraper Sephora
make scrape-all       # Scraper tous
make stats            # Statistiques
make workflow-daily   # Workflow complet
```

---

## 📂 Fichiers importants

```
~/cosmetique-scraper/
├── README.md              ← Documentation principale
├── QUICKREF.md            ← Référence ultra-rapide
├── cli.py                 ← Interface CLI
├── setup.sh               ← Installation
├── test_scraper.py        ← Tests
└── src/                   ← Code source
    ├── scrapers/          ← Scrapers par site
    ├── database/          ← Gestion base de données
    └── exporters/         ← Export JSON/CSV
```

---

## ❓ Besoin d'aide ?

1. **Erreur Playwright** → `playwright install chromium --force`
2. **Tests** → `python test_scraper.py`
3. **Debug** → `python cli.py scrape --source sephora --no-headless --limit 5`
4. **Logs** → `~/cosmetique-scraper/logs/scraper_*.log`

---

## 🎉 C'est parti !

```bash
# Votre première commande
python cli.py scrape --source sephora --limit 10
```

---

**Bonne utilisation ! 🧴✨**
