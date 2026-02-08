#!/bin/bash

# Script de démarrage rapide du dashboard Dermalogica Tracker

echo "🚀 Démarrage du Dashboard Dermalogica Tracker..."
echo ""

# Vérifier si on est dans le bon dossier
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Erreur: docker-compose.yml non trouvé"
    echo "Veuillez lancer ce script depuis la racine du projet cosmetique-scraper"
    exit 1
fi

# Demander le mode de démarrage
echo "Choisissez le mode de démarrage:"
echo "1) Docker (production - recommandé)"
echo "2) Développement local (backend + frontend séparés)"
read -p "Votre choix (1 ou 2): " choice

if [ "$choice" == "1" ]; then
    echo ""
    echo "🐳 Démarrage avec Docker..."

    # Vérifier si Docker est installé
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker n'est pas installé. Installez Docker Desktop puis relancez ce script."
        exit 1
    fi

    # Vérifier si Docker est lancé
    if ! docker info &> /dev/null; then
        echo "❌ Docker n'est pas lancé. Démarrez Docker Desktop puis relancez ce script."
        exit 1
    fi

    # Build et lancement
    echo "📦 Build des images Docker..."
    docker-compose down 2>/dev/null
    docker-compose up --build -d

    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Dashboard démarré avec succès!"
        echo ""
        echo "🌐 Frontend: http://localhost"
        echo "🔌 Backend API: http://localhost:5000"
        echo ""
        echo "📋 Commandes utiles:"
        echo "  - Voir les logs: docker-compose logs -f"
        echo "  - Arrêter: docker-compose down"
        echo "  - Rebuild: docker-compose up --build -d"
    else
        echo "❌ Erreur lors du démarrage Docker"
        exit 1
    fi

elif [ "$choice" == "2" ]; then
    echo ""
    echo "💻 Démarrage en mode développement..."

    # Vérifier Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 n'est pas installé"
        exit 1
    fi

    # Vérifier Node
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js n'est pas installé"
        exit 1
    fi

    # Backend
    echo ""
    echo "🐍 Installation des dépendances backend..."
    cd backend
    pip install -q -r requirements.txt

    echo "🚀 Démarrage du backend (port 5000)..."
    python app.py &
    BACKEND_PID=$!
    cd ..

    # Frontend
    echo ""
    echo "📦 Installation des dépendances frontend..."
    cd frontend

    if [ ! -d "node_modules" ]; then
        npm install
    fi

    echo "🚀 Démarrage du frontend (port 3000)..."
    npm run dev &
    FRONTEND_PID=$!
    cd ..

    echo ""
    echo "✅ Dashboard démarré en mode développement!"
    echo ""
    echo "🌐 Frontend: http://localhost:3000"
    echo "🔌 Backend API: http://localhost:5000"
    echo ""
    echo "⚠️  Appuyez sur Ctrl+C pour arrêter"

    # Attendre l'interruption
    trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
    wait

else
    echo "❌ Choix invalide"
    exit 1
fi
