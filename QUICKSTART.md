# 🚀 Guide de Démarrage Rapide

## Installation (1 min)

```bash
cd ~/cosmetique-scraper
pip install -r requirements.txt
```

## Premier Scraping (2 min)

```bash
# Scraper Sephora (3 pages de nouveautés)
python3 cli.py scrape --site sephora

# Voir les résultats
python3 cli.py stats
```

## Export des Données (30 sec)

```bash
# Export JSON
python3 cli.py export --format json

# Export CSV
python3 cli.py export --format csv
```

Les fichiers sont dans `exports/`

## Commandes Utiles

```bash
# Scraper tous les sites
python3 cli.py scrape

# Nouveautés des 7 derniers jours
python3 cli.py new

# Stats par site
python3 cli.py stats

# Historique prix d'un produit
python3 cli.py history 1

# Aide complète
python3 cli.py --help
```

## Structure des Dossiers

- `database/cosmetique.db` - Base SQLite
- `exports/` - Fichiers exportés
- `logs/scraper.log` - Logs

## Prochaines Étapes

1. ✅ Scraper régulièrement pour suivre les prix
2. ✅ Exporter et analyser les données
3. ✅ Détecter les nouveautés
4. ✅ Suivre l'historique des prix

## Support

Voir `README.md` pour la documentation complète.
