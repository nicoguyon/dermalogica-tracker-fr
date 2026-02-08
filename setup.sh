#!/bin/bash
# Script d'installation et configuration

echo "🧴 Configuration de Cosmetique Scraper"
echo "======================================"

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trouvé"
    exit 1
fi

echo "✓ Python 3 trouvé"

# Créer environnement virtuel
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer
source venv/bin/activate

# Installer dépendances
echo "📥 Installation des dépendances..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Installer Playwright browsers
echo "🌐 Installation de Chromium pour Playwright..."
playwright install chromium

# Rendre CLI exécutable
chmod +x cli.py

echo ""
echo "✅ Installation terminée !"
echo ""
echo "Pour utiliser l'outil :"
echo "  source venv/bin/activate"
echo "  python cli.py --help"
echo ""
echo "Exemple de commande :"
echo "  python cli.py scrape --source sephora --limit 20"
