# 🚀 Quick Start - Focus Dermalogica

Guide de démarrage rapide pour analyser Dermalogica et ses concurrents.

## Installation rapide

```bash
cd ~/cosmetique-scraper
pip install -r requirements.txt
```

## Scénario 1 : Veille Dermalogica 🎯

**Objectif** : Suivre tous les produits Dermalogica disponibles

```bash
# 1. Scraper Dermalogica sur tous les sites (5 pages par site)
python3 cli.py scrape --brands dermalogica --max-pages 5

# 2. Voir les nouveautés du mois
python3 cli.py novelties --brands dermalogica --days 30

# 3. Export complet avec analyse
python3 cli.py export --format both --enhanced
```

**Résultat** :
- `exports/products_XXXXXX.json` : Tous les produits Dermalogica
- `exports/comparison_XXXXXX.json` : Rapport d'analyse
- `exports/products_XXXXXX.csv` : Version Excel

---

## Scénario 2 : Analyse concurrentielle 📊

**Objectif** : Comparer Dermalogica vs concurrents premium

```bash
# 1. Scraper marques premium
python3 cli.py scrape --brands "dermalogica,skinceuticals,dr. dennis gross" --max-pages 3

# 2. Comparer les prix
python3 cli.py compare --brands "dermalogica,skinceuticals,dr. dennis gross"

# 3. Export comparatif
python3 cli.py export --format csv --enhanced
```

**Résultat** :
- Tableau comparatif des prix moyens
- Positionnement de chaque marque
- Sites où chaque marque est disponible

---

## Scénario 3 : Focus Lookfantastic 🛒

**Objectif** : Analyser uniquement sur Lookfantastic

```bash
# Scraper toutes les marques sur Lookfantastic
python3 cli.py scrape --site lookfantastic --brands "dermalogica,skinceuticals,murad,drunk elephant"

# Voir les stats
python3 cli.py stats
```

---

## Scénario 4 : Détection de nouveautés 🆕

**Objectif** : Voir toutes les nouveautés de toutes les marques

```bash
# Scraper toutes les marques cibles
python3 cli.py scrape --max-pages 3

# Voir nouveautés par marque
python3 cli.py novelties --days 14

# Filtrer une marque spécifique
python3 cli.py novelties --brands "drunk elephant" --days 30
```

---

## Scénario 5 : Export hebdomadaire 📅

**Objectif** : Créer un rapport hebdomadaire complet

```bash
# 1. Scraper toutes les marques cibles sur tous les sites
python3 cli.py scrape --max-pages 3

# 2. Comparaison globale
python3 cli.py compare --brands all

# 3. Export enrichi
python3 cli.py export --format both --enhanced

# 4. Nouveautés de la semaine
python3 cli.py novelties --days 7
```

---

## Commandes essentielles

| Commande | Description |
|----------|-------------|
| `python3 cli.py scrape --brands dermalogica` | Scraper uniquement Dermalogica |
| `python3 cli.py compare` | Comparer toutes les marques cibles |
| `python3 cli.py novelties --days 30` | Nouveautés du mois |
| `python3 cli.py export --enhanced` | Export avec analyse |
| `python3 cli.py stats` | Stats globales |

---

## Options utiles

### Filtrer par site
```bash
--site sephora              # Uniquement Sephora
--site lookfantastic        # Uniquement Lookfantastic
--site all                  # Tous les sites (défaut)
```

### Filtrer par marques
```bash
--brands dermalogica                              # Une marque
--brands "dermalogica,skinceuticals"             # Plusieurs marques
--brands all                                      # Toutes les marques en DB
```

### Autres options
```bash
--max-pages 5               # Nombre de pages à scraper
--days 30                   # Période pour nouveautés
--format both               # Export JSON + CSV
--enhanced                  # Export enrichi avec analyse
--limit 100                 # Limiter le nombre de résultats
```

---

## Marques disponibles

- **dermalogica** (cible principale)
- **skinceuticals**
- **drunk elephant**
- **paula's choice**
- **the ordinary**
- **murad**
- **dr. dennis gross**
- **clinique**

---

## Tips

### 1. Scraping intelligent
```bash
# Scraper uniquement les marques premium
python3 cli.py scrape --brands "dermalogica,skinceuticals,dr. dennis gross"

# Scraper uniquement les marques accessibles
python3 cli.py scrape --brands "the ordinary,paula's choice"
```

### 2. Analyse rapide
```bash
# Voir rapidement le positionnement de Dermalogica
python3 cli.py compare --brands dermalogica

# Comparer avec un concurrent spécifique
python3 cli.py compare --brands "dermalogica,skinceuticals"
```

### 3. Export ciblé
```bash
# Export uniquement Sephora pour Dermalogica
python3 cli.py scrape --site sephora --brands dermalogica
python3 cli.py export --format csv --site sephora
```

---

## Fichiers générés

```
exports/
├── products_20260208_103045.json        # Données brutes
├── products_20260208_103045.csv         # Version Excel
├── comparison_20260208_103045.json      # Rapport comparatif
└── comparison_20260208_103045.csv       # Rapport Excel
```

---

## Aide

```bash
# Aide générale
python3 cli.py --help

# Aide pour une commande spécifique
python3 cli.py scrape --help
python3 cli.py compare --help
python3 cli.py novelties --help
```

---

**🎯 Pro Tip** : Pour une veille complète hebdomadaire, lancez simplement :

```bash
python3 cli.py scrape && python3 cli.py compare && python3 cli.py export --enhanced --format both
```

Vous aurez tous les exports nécessaires en un seul coup !
