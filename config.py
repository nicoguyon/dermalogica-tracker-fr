"""Configuration globale du scraper."""

import os
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "database" / "cosmetique.db"
LOGS_DIR = BASE_DIR / "logs"
EXPORT_DIR = BASE_DIR / "exports"

# Rate limiting (secondes entre requêtes)
REQUEST_DELAY = 2
REQUEST_TIMEOUT = 10

# User-Agent rotation
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
]

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 5

# Marques cibles (focus Dermalogica + concurrents)
TARGET_BRANDS = [
    'dermalogica',
    'skinceuticals',
    'drunk elephant',
    "paula's choice",
    'the ordinary',
    'murad',
    'dr. dennis gross',
    'clinique'
]

# Mapping des variations de noms de marques
BRAND_ALIASES = {
    'dermalogica': ['dermalogica'],
    'skinceuticals': ['skinceuticals', 'skin ceuticals'],
    'drunk elephant': ['drunk elephant', 'drunkelephant'],
    "paula's choice": ["paula's choice", 'paulas choice', 'paula choice'],
    'the ordinary': ['the ordinary', 'ordinary'],
    'murad': ['murad'],
    'dr. dennis gross': ['dr. dennis gross', 'dr dennis gross', 'dennis gross'],
    'clinique': ['clinique']
}

# Sites configuration
SITES = {
    'sephora': {
        'base_url': 'https://www.sephora.fr',
        'enabled': True
    },
    'nocibe': {
        'base_url': 'https://www.nocibe.fr',
        'enabled': True
    },
    'marionnaud': {
        'base_url': 'https://www.marionnaud.fr',
        'enabled': True
    },
    'lookfantastic': {
        'base_url': 'https://www.lookfantastic.fr',
        'enabled': True
    },
    'feelunique': {
        'base_url': 'https://www.feelunique.com/fr',
        'enabled': True
    }
}

# Logging
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'
