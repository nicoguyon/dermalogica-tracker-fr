# 🚀 Démarrage Rapide - Dashboard

Guide ultra-rapide pour lancer le dashboard en 2 minutes.

## ⚡ Méthode Express (Recommandée)

### Avec Docker (le plus simple)

```bash
# À la racine du projet
./start-dashboard.sh
# Choisir l'option 1 (Docker)
```

Ou manuellement :
```bash
docker-compose up -d
```

**C'est tout !** 🎉

- Dashboard : http://localhost
- API : http://localhost:5000

### Sans Docker (développement)

```bash
# Terminal 1 - Backend
cd backend
pip install -r requirements.txt
python app.py

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

- Dashboard : http://localhost:3000
- API : http://localhost:5000

## 📊 Première utilisation

Si votre base de données est vide :

```bash
# Scraper quelques produits pour tester
python3 cli.py scrape --brands dermalogica --max-pages 2
```

Puis rafraîchir le dashboard.

## 🎯 Pages disponibles

- **/** - Dashboard principal avec stats et graphiques
- **/products** - Liste de tous les produits avec filtres
- **/brands** - Analyse comparative des marques
- **/promotions** - Produits en promotion
- **/new** - Nouveautés récentes

## 🛠️ Commandes Utiles

### Docker
```bash
# Arrêter
docker-compose down

# Voir les logs
docker-compose logs -f

# Rebuild
docker-compose up --build -d
```

### Développement
```bash
# Backend (Flask)
cd backend
python app.py

# Frontend (Vite)
cd frontend
npm run dev

# Build production frontend
npm run build
```

## 🐛 Problèmes ?

### "Aucune donnée affichée"
→ Lancer le scraper pour peupler la base

### "Cannot connect to backend"
→ Vérifier que le backend tourne sur le port 5000

### "Docker error"
→ Vérifier que Docker Desktop est lancé

### "Module not found"
```bash
# Backend
cd backend && pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

## 📖 Documentation complète

Voir [DASHBOARD_README.md](./DASHBOARD_README.md) pour la documentation complète.

## 🎨 Aperçu des fonctionnalités

- ✅ Stats en temps réel
- ✅ Graphiques interactifs
- ✅ Filtres avancés
- ✅ Dark mode
- ✅ Responsive design
- ✅ Comparaison de prix
- ✅ Détection promotions
- ✅ Tracking nouveautés

---

**Enjoy! 🎉**
