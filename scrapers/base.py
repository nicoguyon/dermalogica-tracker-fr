"""Classe de base pour tous les scrapers."""

import time
import logging
import random
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

logger = logging.getLogger(__name__)


class BaseScraper:
    """Classe de base pour tous les scrapers."""

    def __init__(self, site_name: str, base_url: str,
                 request_delay: float = 2.0,
                 timeout: int = 10,
                 max_retries: int = 3):
        """Initialise le scraper.

        Args:
            site_name: Nom du site
            base_url: URL de base du site
            request_delay: Délai entre requêtes (secondes)
            timeout: Timeout des requêtes (secondes)
            max_retries: Nombre max de tentatives
        """
        self.site_name = site_name
        self.base_url = base_url
        self.request_delay = request_delay
        self.timeout = timeout
        self.max_retries = max_retries
        self.ua = UserAgent()
        self.session = requests.Session()

    def _get_headers(self) -> Dict:
        """Génère des headers avec User-Agent aléatoire.

        Returns:
            Dictionnaire de headers
        """
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    def _make_request(self, url: str, method: str = 'GET',
                     **kwargs) -> Optional[requests.Response]:
        """Effectue une requête HTTP avec retry et rate limiting.

        Args:
            url: URL à requêter
            method: Méthode HTTP
            **kwargs: Arguments supplémentaires pour requests

        Returns:
            Réponse HTTP ou None si échec
        """
        for attempt in range(self.max_retries):
            try:
                # Rate limiting
                time.sleep(self.request_delay + random.uniform(0, 0.5))

                # Requête
                response = self.session.request(
                    method=method,
                    url=url,
                    headers=self._get_headers(),
                    timeout=self.timeout,
                    **kwargs
                )

                response.raise_for_status()
                logger.debug(f"Requête réussie: {url}")
                return response

            except requests.exceptions.RequestException as e:
                logger.warning(
                    f"Erreur requête (tentative {attempt + 1}/{self.max_retries}): {e}"
                )
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Échec après {self.max_retries} tentatives: {url}")
                    return None

    def _parse_html(self, html: str) -> Optional[BeautifulSoup]:
        """Parse le HTML avec BeautifulSoup.

        Args:
            html: HTML à parser

        Returns:
            Objet BeautifulSoup ou None
        """
        try:
            return BeautifulSoup(html, 'lxml')
        except Exception as e:
            logger.error(f"Erreur parsing HTML: {e}")
            return None

    def _normalize_brand(self, brand: str) -> str:
        """Normalise le nom d'une marque pour la comparaison.

        Args:
            brand: Nom de la marque

        Returns:
            Nom normalisé (minuscules, sans accents)
        """
        if not brand:
            return ''
        return brand.lower().strip()

    def _match_brands(self, brand: str, target_brands: Optional[List[str]] = None) -> bool:
        """Vérifie si une marque correspond aux marques cibles.

        Args:
            brand: Nom de la marque du produit
            target_brands: Liste des marques à filtrer (None = toutes)

        Returns:
            True si la marque correspond, False sinon
        """
        if not target_brands:
            return True  # Pas de filtre = accepter tous

        if not brand:
            return False

        from config import BRAND_ALIASES

        brand_normalized = self._normalize_brand(brand)

        # Vérifier les correspondances avec les alias
        for target in target_brands:
            target_normalized = self._normalize_brand(target)
            aliases = BRAND_ALIASES.get(target_normalized, [target_normalized])

            for alias in aliases:
                if self._normalize_brand(alias) in brand_normalized or brand_normalized in self._normalize_brand(alias):
                    return True

        return False

    def scrape_products(self, **kwargs) -> List[Dict]:
        """Scrape les produits. À implémenter dans les sous-classes.

        Returns:
            Liste de produits
        """
        raise NotImplementedError("À implémenter dans les sous-classes")

    def scrape_product_details(self, product_url: str) -> Optional[Dict]:
        """Scrape les détails d'un produit. À implémenter dans les sous-classes.

        Args:
            product_url: URL du produit

        Returns:
            Dictionnaire avec les détails du produit
        """
        raise NotImplementedError("À implémenter dans les sous-classes")

    def close(self):
        """Ferme la session."""
        self.session.close()
        logger.info(f"Session fermée pour {self.site_name}")
