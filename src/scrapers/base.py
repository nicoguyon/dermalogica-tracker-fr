"""Classe de base abstraite pour tous les scrapers."""

from abc import ABC, abstractmethod
from typing import List, Optional
import time
from playwright.sync_api import sync_playwright, Browser, Page

from ..database import Product
from ..utils import setup_logger, PLAYWRIGHT_CONFIG, SCRAPER_CONFIG

logger = setup_logger("scrapers")


class BaseScraper(ABC):
    """Classe abstraite de base pour tous les scrapers."""

    def __init__(self, headless: bool = True):
        """Initialise le scraper.

        Args:
            headless: Exécuter en mode headless
        """
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.products: List[Product] = []

    def __enter__(self):
        """Context manager entry."""
        self._setup_browser()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self._cleanup()

    def _setup_browser(self):
        """Configure et démarre le navigateur Playwright."""
        logger.info("Démarrage du navigateur...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=PLAYWRIGHT_CONFIG['slow_mo']
        )

        context = self.browser.new_context(
            user_agent=SCRAPER_CONFIG['user_agent'],
            viewport={'width': 1920, 'height': 1080}
        )

        self.page = context.new_page()
        self.page.set_default_timeout(PLAYWRIGHT_CONFIG['timeout'])

        logger.info("Navigateur prêt")

    def _cleanup(self):
        """Nettoie les ressources."""
        if self.browser:
            self.browser.close()
        if hasattr(self, 'playwright'):
            self.playwright.stop()
        logger.info("Navigateur fermé")

    def _rate_limit(self):
        """Applique un délai entre les requêtes."""
        time.sleep(SCRAPER_CONFIG['rate_limit_delay'])

    def _retry_on_failure(self, func, *args, **kwargs):
        """Réessaye une fonction en cas d'échec.

        Args:
            func: Fonction à exécuter
            *args, **kwargs: Arguments de la fonction

        Returns:
            Résultat de la fonction ou None
        """
        max_retries = SCRAPER_CONFIG['max_retries']
        retry_delay = SCRAPER_CONFIG['retry_delay']

        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.warning(f"Tentative {attempt + 1}/{max_retries} échouée : {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    logger.error(f"Échec après {max_retries} tentatives")
                    return None

    @abstractmethod
    def scrape_products(self, limit: Optional[int] = None, new_only: bool = False) -> List[Product]:
        """Scrape les produits du site.

        Args:
            limit: Nombre maximum de produits à scraper
            new_only: Scraper uniquement les nouveautés

        Returns:
            Liste de produits scrapés
        """
        pass

    @abstractmethod
    def _extract_product_data(self, element) -> Optional[Product]:
        """Extrait les données d'un élément produit.

        Args:
            element: Élément DOM du produit

        Returns:
            Instance de Product ou None
        """
        pass

    def get_products(self) -> List[Product]:
        """Retourne la liste des produits scrapés.

        Returns:
            Liste de produits
        """
        return self.products
