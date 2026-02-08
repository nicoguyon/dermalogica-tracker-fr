"""Configuration globale du tracker concurrentiel."""

import os
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "database" / "cosmetique.db"
LOGS_DIR = BASE_DIR / "logs"
EXPORT_DIR = BASE_DIR / "exports"

# Rate limiting (secondes entre requêtes)
REQUEST_DELAY = 2
REQUEST_TIMEOUT = 30

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 5

# Dermalogica + 3 marques concurrentes
TARGET_BRANDS = [
    'dermalogica',
    "paula's choice",
    'murad',
    'skinceuticals',
]

# Sites (Dermalogica + concurrents)
SITES = {
    'dermalogica': {
        'base_url': 'https://www.dermalogica.fr',
        'catalog_url': 'https://www.dermalogica.fr/collections/products/products.json?limit=250',
        'brand': 'Dermalogica',
        'currency': 'EUR',
        'method': 'shopify_json',
        'enabled': True
    },
    'paulaschoice': {
        'base_url': 'https://www.paulaschoice.fr',
        'catalog_url': 'https://www.paulaschoice.fr/fr/nos-soins',
        'brand': "Paula's Choice",
        'currency': 'EUR',
        'method': 'playwright_html',
        'enabled': True
    },
    'murad': {
        'base_url': 'https://www.murad.com',
        'catalog_url': 'https://www.murad.com/collections/all/products.json?limit=250',
        'brand': 'Murad',
        'currency': 'USD',
        'method': 'shopify_json',
        'enabled': True
    },
    'skinceuticals': {
        'base_url': 'https://www.skinceuticals.com',
        'catalog_url': 'https://www.skinceuticals.com/skin-care',
        'brand': 'SkinCeuticals',
        'currency': 'USD',
        'method': 'playwright_html',
        'enabled': True
    }
}

# Logging
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'
