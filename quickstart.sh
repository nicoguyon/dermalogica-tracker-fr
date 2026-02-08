#!/bin/bash
# Script de démarrage rapide

echo "🚀 Démarrage rapide - Cosmetique Scraper"
echo "========================================"
echo ""

# Vérifier si déjà installé
if [ ! -d "venv" ]; then
    echo "❌ Installation non détectée"
    echo "Lancer d'abord : bash setup.sh"
    exit 1
fi

# Activer venv
source venv/bin/activate

echo "Que voulez-vous faire ?"
echo ""
echo "1) Scraper Sephora (20 produits)"
echo "2) Scraper Nocibé (20 produits)"
echo "3) Scraper tous les sites (50 produits)"
echo "4) Scraper nouveautés uniquement"
echo "5) Voir les statistiques"
echo "6) Exporter en JSON"
echo "7) Exporter en CSV"
echo "8) Quitter"
echo ""

read -p "Votre choix (1-8) : " choice

case $choice in
    1)
        echo ""
        python cli.py scrape --source sephora --limit 20
        ;;
    2)
        echo ""
        python cli.py scrape --source nocibe --limit 20
        ;;
    3)
        echo ""
        python cli.py scrape --all --limit 50
        ;;
    4)
        echo ""
        python cli.py scrape --all --new-only --limit 30
        ;;
    5)
        echo ""
        python cli.py stats
        ;;
    6)
        echo ""
        python cli.py export --format json
        ;;
    7)
        echo ""
        python cli.py export --format csv
        ;;
    8)
        echo "👋 À bientôt !"
        exit 0
        ;;
    *)
        echo "❌ Choix invalide"
        exit 1
        ;;
esac

echo ""
echo "✅ Terminé !"
