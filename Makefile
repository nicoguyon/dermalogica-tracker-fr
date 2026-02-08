# Makefile pour Cosmetique Scraper

.PHONY: install test clean scrape-all export stats help

# Couleurs pour output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Afficher l'aide
	@echo "$(GREEN)Cosmetique Scraper - Commandes disponibles$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Installer les dépendances
	@echo "$(GREEN)Installation des dépendances...$(NC)"
	pip install -r requirements.txt
	playwright install chromium
	@echo "$(GREEN)✓ Installation terminée$(NC)"

test: ## Lancer les tests
	@echo "$(GREEN)Lancement des tests...$(NC)"
	python test_scraper.py

scrape-sephora: ## Scraper Sephora (20 produits)
	@echo "$(GREEN)Scraping Sephora...$(NC)"
	python cli.py scrape --source sephora --limit 20

scrape-nocibe: ## Scraper Nocibé (20 produits)
	@echo "$(GREEN)Scraping Nocibé...$(NC)"
	python cli.py scrape --source nocibe --limit 20

scrape-all: ## Scraper tous les sites
	@echo "$(GREEN)Scraping tous les sites...$(NC)"
	python cli.py scrape --all --limit 50

scrape-new: ## Scraper les nouveautés uniquement
	@echo "$(GREEN)Scraping nouveautés...$(NC)"
	python cli.py scrape --all --new-only --limit 30

export-json: ## Exporter en JSON
	@echo "$(GREEN)Export JSON...$(NC)"
	python cli.py export --format json

export-csv: ## Exporter en CSV
	@echo "$(GREEN)Export CSV...$(NC)"
	python cli.py export --format csv

stats: ## Afficher les statistiques
	@python cli.py stats

clean-old: ## Nettoyer les données de plus de 30 jours
	@echo "$(YELLOW)Nettoyage des anciennes données...$(NC)"
	python cli.py clean --days 30

clean-all: ## Vider toute la base de données
	@echo "$(RED)⚠ Suppression de toutes les données...$(NC)"
	python cli.py clean --all

clean-exports: ## Supprimer les exports
	@echo "$(YELLOW)Suppression des exports...$(NC)"
	rm -f ~/cosmetique-scraper/exports/*.json
	rm -f ~/cosmetique-scraper/exports/*.csv
	@echo "$(GREEN)✓ Exports supprimés$(NC)"

clean-logs: ## Supprimer les logs
	@echo "$(YELLOW)Suppression des logs...$(NC)"
	rm -f ~/cosmetique-scraper/logs/*.log
	@echo "$(GREEN)✓ Logs supprimés$(NC)"

format: ## Formater le code (black)
	@command -v black >/dev/null 2>&1 || { echo "$(RED)black non installé$(NC)"; exit 1; }
	black src/ cli.py test_scraper.py

lint: ## Vérifier le code (flake8)
	@command -v flake8 >/dev/null 2>&1 || { echo "$(RED)flake8 non installé$(NC)"; exit 1; }
	flake8 src/ cli.py --max-line-length=120

dev-install: ## Installation développement (avec outils dev)
	pip install -r requirements.txt
	pip install black flake8 pytest
	playwright install chromium

workflow-daily: ## Workflow quotidien : scrape + export + stats
	@echo "$(GREEN)🔄 Workflow quotidien$(NC)"
	@make scrape-new
	@make export-json
	@make stats
	@echo "$(GREEN)✓ Workflow terminé$(NC)"

workflow-full: ## Workflow complet : scrape tout + export + stats
	@echo "$(GREEN)🔄 Workflow complet$(NC)"
	@make scrape-all
	@make export-json
	@make export-csv
	@make stats
	@echo "$(GREEN)✓ Workflow terminé$(NC)"
