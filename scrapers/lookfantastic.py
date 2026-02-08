"""Scraper pour Lookfantastic."""

import logging
from typing import Dict, List, Optional
from urllib.parse import urljoin
from .base import BaseScraper
from config import SITES

logger = logging.getLogger(__name__)


class LookfantasticScraper(BaseScraper):
    """Scraper pour le site Lookfantastic.fr."""

    def __init__(self):
        """Initialise le scraper Lookfantastic."""
        site_config = SITES['lookfantastic']
        super().__init__(
            site_name='lookfantastic',
            base_url=site_config['base_url']
        )

    def scrape_products(self, category: str = 'nouveautes',
                       max_pages: int = 3,
                       brands: Optional[List[str]] = None) -> List[Dict]:
        """Scrape les produits de Lookfantastic.

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
                logger.info(f"Scraping Lookfantastic page {page}: {url}")

                response = self._make_request(url)
                if not response:
                    continue

                soup = self._parse_html(response.text)
                if not soup:
                    continue

                # Sélecteurs pour Lookfantastic
                product_cards = soup.select('li.productListProducts_product')

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

        logger.info(f"Total Lookfantastic: {len(products)} produits")
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
            name_elem = card.select_one('h3.productBlock_productName')
            name = name_elem.text.strip() if name_elem else None

            # Marque
            brand_elem = card.select_one('span.productBlock_brandName')
            brand = brand_elem.text.strip() if brand_elem else None

            # Prix
            price = None
            price_elem = card.select_one('span.productBlock_priceValue')
            if price_elem:
                price_text = price_elem.text.strip()
                price = self._parse_price(price_text)

            # URL
            link_elem = card.select_one('a.productBlock_link')
            url = urljoin(self.base_url, link_elem['href']) if link_elem else None

            # Image
            img_elem = card.select_one('img.productBlock_image')
            image_url = img_elem.get('src') or img_elem.get('data-src') if img_elem else None

            # ID produit (extrait de l'URL)
            product_id = None
            if url:
                product_id = url.rstrip('/').split('/')[-1].split('.')[0]

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
            price_clean = price_text.replace('€', '').replace(',', '.').strip()
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
            desc_elem = soup.select_one('div.productDescription_description')
            if desc_elem:
                details['description'] = desc_elem.text.strip()

            # Ingrédients
            ingredients_elem = soup.select_one('div.productIngredients')
            if ingredients_elem:
                details['ingredients'] = ingredients_elem.text.strip()

            return details

        except Exception as e:
            logger.error(f"Erreur scraping détails: {e}", exc_info=True)
            return None
