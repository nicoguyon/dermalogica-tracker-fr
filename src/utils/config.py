"""Configuration globale de l'application."""

from pathlib import Path
from typing import Dict, Any

# Chemins
BASE_DIR = Path.home() / "cosmetique-scraper"
DATA_DIR = BASE_DIR / "data"
EXPORTS_DIR = BASE_DIR / "exports"
LOGS_DIR = BASE_DIR / "logs"

# Créer les dossiers nécessaires
for directory in [DATA_DIR, EXPORTS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Base de données
DATABASE_PATH = DATA_DIR / "products.db"

# Configuration Playwright
PLAYWRIGHT_CONFIG: Dict[str, Any] = {
    "headless": True,
    "slow_mo": 100,  # Délai en ms entre actions (éviter détection bot)
    "timeout": 30000,  # 30 secondes
}

# Configuration scraping
SCRAPER_CONFIG: Dict[str, Any] = {
    "max_retries": 3,
    "retry_delay": 2,  # secondes
    "rate_limit_delay": 1,  # secondes entre chaque requête
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
}

# URLs de base
BASE_URLS = {
    "sephora": "https://www.sephora.fr",
    "nocibe": "https://www.nocibe.fr",
    "marionnaud": "https://www.marionnaud.fr",
}

# Catégories à scraper
CATEGORIES = [
    "soins-visage",
    "maquillage",
    "parfum",
    "soins-corps",
    "soins-cheveux",
]
