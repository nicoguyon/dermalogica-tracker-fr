"""Scraper pour Feelunique."""

import logging
from typing import Dict, List, Optional
from urllib.parse import urljoin
from .base import BaseScraper
from config import SITES

logger = logging.getLogger(__name__)


class FeeluniqueScraper(BaseScraper):
    """Scraper pour le site Feelunique.com/fr."""

    def __init__(self):
        """Initialise le scraper Feelunique."""
        site_config = SITES['feelunique']
        super().__init__(
            site_name='feelunique',
            base_url=site_config['base_url']
        )

    def scrape_products(self, category: str = 'nouveautes',
                       max_pages: int = 3,
                       brands: Optional[List[str]] = None) -> List[Dict]:
        """Scrape les produits de Feelunique.

        Args:
            category: Catégorie à scraper
            max_pages: Nombre max de pages
            brands: Liste de marques à filtrer (optionnel)

        Returns:
            Liste de produits
        """
        products = []

        # Construction URL selon catégorie
        if category == 'nouveautes':
            base_url = f"{self.base_url}/nouveautes"
        else:
            base_url = f"{self.base_url}/{category}"

        for page in range(1, max_pages + 1):
            try:
                url = f"{base_url}?page={page}"
                logger.info(f"Scraping Feelunique page {page}: {url}")

                response = self._make_request(url)
                if not response:
                    continue

                soup = self._parse_html(response.text)
                if not soup:
                    continue

                # Sélecteurs pour Feelunique
                product_cards = soup.select('div.product-item, article.product-card')

                if not product_cards:
                    logger.warning(f"Aucun produit trouvé page {page}")
                    break

                for card in product_cards:
                    try:
                        product = self._extract_product_data(card)
                        if product and self._match_brands(product.get('brand', ''), brands):
                            products.append(product)
                    except Exception as e:
                        logger.error(f"Erreur extraction produit: {e}", exc_info=True)
                        continue

                logger.info(f"Page {page}: {len(product_cards)} produits trouvés")

            except Exception as e:
                logger.error(f"Erreur page {page}: {e}", exc_info=True)
                continue

        logger.info(f"Total Feelunique: {len(products)} produits")
        return products

    def _extract_product_data(self, card) -> Optional[Dict]:
        """Extrait les données d'un produit depuis une card.

        Args:
            card: Element BeautifulSoup de la card produit

        Returns:
            Dictionnaire de données produit
        """
        try:
            # Nom du produit
            name_elem = card.select_one('h3.product-name, h2.product-title, a.product-link')
            name = name_elem.text.strip() if name_elem else None

            # Marque
            brand_elem = card.select_one('span.product-brand, div.brand-name')
            brand = brand_elem.text.strip() if brand_elem else None

            # Prix
            price = None
            price_elem = card.select_one('span.price, span.product-price')
            if price_elem:
                price_text = price_elem.text.strip()
                price = self._parse_price(price_text)

            # URL
            link_elem = card.select_one('a.product-link, a[href*="/products/"]')
            url = None
            if link_elem and link_elem.get('href'):
                href = link_elem['href']
                url = urljoin(self.base_url, href) if not href.startswith('http') else href

            # Image
            img_elem = card.select_one('img.product-image, img[itemprop="image"]')
            image_url = None
            if img_elem:
                image_url = img_elem.get('src') or img_elem.get('data-src')

            # ID produit (extrait de l'URL)
            product_id = None
            if url:
                product_id = url.rstrip('/').split('/')[-1].split('?')[0]

            if not all([name, url]):
                logger.warning("Produit incomplet, ignoré")
                return None

            return {
                'product_id': product_id,
                'name': name,
                'brand': brand,
                'price': price,
                'url': url,
                'image_url': image_url,
                'category': 'nouveautes'
            }

        except Exception as e:
            logger.error(f"Erreur extraction données: {e}", exc_info=True)
            return None

    def _parse_price(self, price_text: str) -> Optional[float]:
        """Parse le texte de prix pour extraire le montant.

        Args:
            price_text: Texte du prix (ex: "29,99 €")

        Returns:
            Prix en float ou None
        """
        try:
            # Nettoyer le texte (supprimer €, £, espaces)
            price_clean = price_text.replace('€', '').replace('£', '').replace(',', '.').strip()
            return float(price_clean)
        except (ValueError, AttributeError):
            return None

    def scrape_product_details(self, product_url: str) -> Optional[Dict]:
        """Scrape les détails d'un produit spécifique.

        Args:
            product_url: URL du produit

        Returns:
            Dictionnaire avec détails du produit
        """
        try:
            logger.info(f"Scraping détails: {product_url}")
            response = self._make_request(product_url)

            if not response:
                return None

            soup = self._parse_html(response.text)
            if not soup:
                return None

            # Extraction détails
            details = {}

            # Description
            desc_elem = soup.select_one('div.product-description, div[itemprop="description"]')
            if desc_elem:
                details['description'] = desc_elem.text.strip()

            # Ingrédients
            ingredients_elem = soup.select_one('div.ingredients, div.product-ingredients')
            if ingredients_elem:
                details['ingredients'] = ingredients_elem.text.strip()

            return details

        except Exception as e:
            logger.error(f"Erreur scraping détails: {e}", exc_info=True)
            return None
