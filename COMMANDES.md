# 📋 Commandes Rapides - Cosmetique Scraper V2

## 🎯 Commandes principales

### Scraper par marque
```bash
# Une marque
python3 cli.py scrape --brands dermalogica

# Plusieurs marques
python3 cli.py scrape --brands "dermalogica,skinceuticals"

# Toutes les marques sur tous les sites
python3 cli.py scrape

# Site spécifique + marque
python3 cli.py scrape --site lookfantastic --brands dermalogica

# Avec options
python3 cli.py scrape --site sephora --brands dermalogica --max-pages 5
```

### Comparer les marques
```bash
# Comparer marques par défaut (8 marques cibles)
python3 cli.py compare

# Comparer marques spécifiques
python3 cli.py compare --brands "dermalogica,skinceuticals"

# Comparer toutes les marques en DB
python3 cli.py compare --brands all
```

### Voir les nouveautés
```bash
# Nouveautés de la semaine (toutes marques)
python3 cli.py novelties

# Nouveautés d'une marque
python3 cli.py novelties --brands dermalogica

# Nouveautés du mois
python3 cli.py novelties --days 30 --brands dermalogica

# Plusieurs marques
python3 cli.py novelties --brands "dermalogica,drunk elephant" --days 14
```

### Exporter
```bash
# Export standard JSON
python3 cli.py export --format json

# Export enrichi (recommandé)
python3 cli.py export --format both --enhanced

# Export avec filtre
python3 cli.py export --format csv --site sephora --limit 100
```

### Statistiques
```bash
python3 cli.py stats
```

### Historique prix
```bash
python3 cli.py history 42  # ID du produit
```

---

## 🚀 Workflows complets

### Workflow 1 : Veille Dermalogica hebdomadaire
```bash
# 1. Scraper
python3 cli.py scrape --brands dermalogica --max-pages 5

# 2. Nouveautés
python3 cli.py novelties --brands dermalogica --days 7

# 3. Export enrichi
python3 cli.py export --format both --enhanced
```

### Workflow 2 : Analyse concurrentielle complète
```bash
# 1. Scraper concurrents
python3 cli.py scrape --brands "dermalogica,skinceuticals,drunk elephant" --max-pages 3

# 2. Comparer
python3 cli.py compare --brands "dermalogica,skinceuticals,drunk elephant"

# 3. Export comparatif
python3 cli.py export --format both --enhanced
```

### Workflow 3 : Focus site (ex: Lookfantastic)
```bash
# Scraper + export
python3 cli.py scrape --site lookfantastic --brands dermalogica
python3 cli.py export --format csv --site lookfantastic
```

### Workflow 4 : Veille nouveautés toutes marques
```bash
# Scraper toutes marques cibles
python3 cli.py scrape --max-pages 3

# Voir nouveautés par marque
python3 cli.py novelties --days 14

# Comparer
python3 cli.py compare
```

---

## 🎓 Options par commande

### `scrape`
| Option | Valeurs | Exemple |
|--------|---------|---------|
| `--site` | sephora, nocibe, marionnaud, lookfantastic, feelunique, all | `--site sephora` |
| `--brands` | Liste séparée par virgules | `--brands dermalogica` |
| `--category` | nouveautes, soins, ... | `--category nouveautes` |
| `--max-pages` | Nombre | `--max-pages 5` |

### `compare`
| Option | Valeurs | Exemple |
|--------|---------|---------|
| `--brands` | Liste séparée par virgules ou "all" | `--brands dermalogica,skinceuticals` |

### `novelties`
| Option | Valeurs | Exemple |
|--------|---------|---------|
| `--brands` | Liste séparée par virgules | `--brands dermalogica` |
| `--days` | Nombre de jours | `--days 30` |

### `export`
| Option | Valeurs | Exemple |
|--------|---------|---------|
| `--format` | json, csv, both | `--format both` |
| `--enhanced` | Flag (activer) | `--enhanced` |
| `--site` | sephora, nocibe, ... | `--site sephora` |
| `--limit` | Nombre | `--limit 100` |

---

## 🔍 Sites disponibles

| Nom | Code | URL |
|-----|------|-----|
| Sephora | `sephora` | https://www.sephora.fr |
| Nocibé | `nocibe` | https://www.nocibe.fr |
| Marionnaud | `marionnaud` | https://www.marionnaud.fr |
| Lookfantastic | `lookfantastic` | https://www.lookfantastic.fr |
| Feelunique | `feelunique` | https://www.feelunique.com/fr |

---

## 🏷️ Marques disponibles

| Nom | Code |
|-----|------|
| **Dermalogica** ⭐ | `dermalogica` |
| SkinCeuticals | `skinceuticals` |
| Drunk Elephant | `drunk elephant` |
| Paula's Choice | `paula's choice` |
| The Ordinary | `the ordinary` |
| Murad | `murad` |
| Dr. Dennis Gross | `dr. dennis gross` |
| Clinique | `clinique` |

---

## 🆘 Aide

```bash
# Aide générale
python3 cli.py --help

# Aide commande spécifique
python3 cli.py scrape --help
python3 cli.py compare --help
python3 cli.py novelties --help
python3 cli.py export --help
```

---

## 🧪 Tests

```bash
# Valider l'installation
python3 test_v2.py

# Vérifier les imports
python3 -c "from scrapers import *; print('✓ OK')"
```

---

## 💡 Tips

### Plusieurs marques
Toujours mettre entre guillemets si noms avec espaces :
```bash
python3 cli.py scrape --brands "drunk elephant,paula's choice"
```

### Export enrichi
Toujours utiliser `--enhanced` pour avoir :
- Prix moyen de la marque
- Positionnement prix
- Concurrents directs
- Rapport de comparaison

### One-liner complet
```bash
python3 cli.py scrape && python3 cli.py compare && python3 cli.py export --enhanced --format both
```

---

## 📊 Fichiers générés

### Après scraping
- Base de données : `database/cosmetique.db`
- Logs : `logs/scraper.log`

### Après export
- Produits : `exports/products_XXXXXX.json` / `.csv`
- Comparaison : `exports/comparison_XXXXXX.json` / `.csv` (si --enhanced)

---

**🚀 Prêt à utiliser !**

Pour démarrer rapidement : `python3 cli.py compare`
