# 🚀 START HERE - Cosmetique Scraper V2

## 🎯 Vous voulez faire quoi ?

### 1️⃣ Suivre Dermalogica
```bash
python3 cli.py scrape --brands dermalogica --max-pages 5
python3 cli.py novelties --brands dermalogica --days 30
python3 cli.py export --format both --enhanced
```
📁 Résultat : Tous les produits Dermalogica + nouveautés + rapport Excel

---

### 2️⃣ Comparer Dermalogica vs concurrents
```bash
python3 cli.py scrape --brands "dermalogica,skinceuticals,drunk elephant"
python3 cli.py compare --brands "dermalogica,skinceuticals,drunk elephant"
```
📊 Résultat : Tableau comparatif des prix et positionnement

---

### 3️⃣ Voir toutes les nouveautés
```bash
python3 cli.py scrape
python3 cli.py novelties --days 7
```
🆕 Résultat : Nouveautés de la semaine par marque

---

### 4️⃣ Analyser Lookfantastic
```bash
python3 cli.py scrape --site lookfantastic --brands dermalogica
python3 cli.py export --format csv --site lookfantastic
```
🛒 Résultat : Tous les produits Dermalogica sur Lookfantastic

---

### 5️⃣ Rapport complet hebdomadaire
```bash
python3 cli.py scrape --max-pages 3
python3 cli.py compare --brands all
python3 cli.py export --format both --enhanced
python3 cli.py novelties --days 7
```
📋 Résultat : Rapport complet avec tous les exports

---

## 📖 Documentation

| Je veux... | Fichier à lire |
|-----------|----------------|
| **Démarrer rapidement** | `QUICKSTART_DERMALOGICA.md` |
| **Voir toutes les commandes** | `COMMANDES.md` |
| **Documentation complète** | `README.md` |
| **Voir les changements V2** | `CHANGELOG_V2.md` |
| **Vérifier le status** | `STATUS.md` |

---

## 🧪 Tester l'installation

```bash
python3 test_v2.py
```
✅ Doit afficher "TOUS LES TESTS RÉUSSIS"

---

## 🆘 Aide

```bash
python3 cli.py --help              # Liste des commandes
python3 cli.py scrape --help       # Options scraping
python3 cli.py compare --help      # Options comparaison
```

---

## 🎯 Marques disponibles

- **dermalogica** ⭐ (cible principale)
- skinceuticals
- drunk elephant
- paula's choice
- the ordinary
- murad
- dr. dennis gross
- clinique

---

## 🌐 Sites disponibles

- Sephora
- Nocibé
- Marionnaud
- **Lookfantastic** (nouveau)
- **Feelunique** (nouveau)

---

## 💡 Commande la plus utile

```bash
python3 cli.py compare
```
→ Compare instantanément toutes les marques cibles

---

**🚀 C'est tout ! Vous êtes prêt.**

*Besoin d'aide ? Lisez `QUICKSTART_DERMALOGICA.md` pour 5 scénarios détaillés.*
