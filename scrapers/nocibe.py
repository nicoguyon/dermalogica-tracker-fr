"""Scraper pour Nocibé."""

import logging
import re
from typing import Dict, List, Optional
from urllib.parse import urljoin
from .base import BaseScraper

logger = logging.getLogger(__name__)


class NocibeScraper(BaseScraper):
    """Scraper pour Nocibe.fr"""

    def __init__(self):
        super().__init__(
            site_name='nocibe',
            base_url='https://www.nocibe.fr'
        )

    def scrape_products(self, category: str = 'nouveautes',
                       max_pages: int = 3) -> List[Dict]:
        """Scrape les produits d'une catégorie.

        Args:
            category: Catégorie à scraper
            max_pages: Nombre max de pages à scraper

        Returns:
            Liste de produits
        """
        products = []
        logger.info(f"Scraping Nocibé - catégorie: {category}")

        # URL de la catégorie
        category_url = f"{self.base_url}/{category}"

        for page in range(1, max_pages + 1):
            url = f"{category_url}?page={page}"
            logger.info(f"Scraping page {page}/{max_pages}: {url}")

            response = self._make_request(url)
            if not response:
                logger.warning(f"Échec page {page}")
                continue

            soup = self._parse_html(response.text)
            if not soup:
                continue

            # Trouver les produits (adapter les sélecteurs)
            product_items = soup.find_all('div', class_=re.compile(r'product-item|product-tile'))

            if not product_items:
                # Essayer un autre sélecteur
                product_items = soup.find_all('article', class_=re.compile(r'product'))

            if not product_items:
                logger.info(f"Aucun produit trouvé page {page}")
                break

            logger.info(f"Trouvé {len(product_items)} produits page {page}")

            for item in product_items:
                try:
                    product = self._parse_product_item(item)
                    if product:
                        products.append(product)
                except Exception as e:
                    logger.error(f"Erreur parsing produit: {e}")
                    continue

        logger.info(f"Total produits scrapés: {len(products)}")
        return products

    def _parse_product_item(self, item) -> Optional[Dict]:
        """Parse un élément produit de la liste.

        Args:
            item: Élément BeautifulSoup du produit

        Returns:
            Dictionnaire avec les données du produit
        """
        try:
            # Nom du produit
            name_elem = item.find(['h2', 'h3', 'span'], class_=re.compile(r'product-name|title'))
            if not name_elem:
                name_elem = item.find('a', title=True)
            if not name_elem:
                return None

            name = name_elem.get_text(strip=True) if hasattr(name_elem, 'get_text') else name_elem.get('title')

            # Marque
            brand_elem = item.find(['span', 'div'], class_=re.compile(r'brand|marque'))
            brand = brand_elem.get_text(strip=True) if brand_elem else None

            # URL
            link_elem = item.find('a', href=True)
            product_url = urljoin(self.base_url, link_elem['href']) if link_elem else None

            # ID produit
            product_id = item.get('data-product-id') or item.get('data-id')
            if not product_id and product_url:
                # Essayer d'extraire de l'URL
                match = re.search(r'[-_](\d+)\.html|/p/(\d+)', product_url)
                if match:
                    product_id = match.group(1) or match.group(2)

            # Image
            img_elem = item.find('img', src=True)
            image_url = img_elem.get('src') or img_elem.get('data-src') if img_elem else None
            if image_url and image_url.startswith('//'):
                image_url = 'https:' + image_url

            # Prix
            price = None
            price_elem = item.find(['span', 'div'], class_=re.compile(r'price|prix'))
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                match = re.search(r'(\d+[,.]?\d*)', price_text.replace(',', '.'))
                if match:
                    price = float(match.group(1))

            if not product_id:
                logger.warning(f"Pas d'ID pour: {name}")
                # Générer un ID basé sur le nom
                product_id = re.sub(r'[^a-z0-9]', '', name.lower())[:50]

            return {
                'product_id': str(product_id),
                'name': name,
                'brand': brand,
                'url': product_url,
                'image_url': image_url,
                'price': price,
                'category': 'nouveautes'
            }

        except Exception as e:
            logger.error(f"Erreur parsing produit: {e}")
            return None

    def scrape_product_details(self, product_url: str) -> Optional[Dict]:
        """Scrape les détails complets d'un produit.

        Args:
            product_url: URL du produit

        Returns:
            Dictionnaire avec tous les détails
        """
        response = self._make_request(product_url)
        if not response:
            return None

        soup = self._parse_html(response.text)
        if not soup:
            return None

        try:
            # Nom
            name_elem = soup.find(['h1', 'h2'], class_=re.compile(r'product-name|title'))
            name = name_elem.get_text(strip=True) if name_elem else None

            # Description
            desc_elem = soup.find(['div', 'p'], class_=re.compile(r'description'))
            description = desc_elem.get_text(strip=True) if desc_elem else None

            # Prix
            price = None
            price_elem = soup.find(['span', 'div'], class_=re.compile(r'price'))
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                match = re.search(r'(\d+[,.]?\d*)', price_text.replace(',', '.'))
                if match:
                    price = float(match.group(1))

            return {
                'name': name,
                'description': description,
                'price': price,
                'url': product_url
            }

        except Exception as e:
            logger.error(f"Erreur détails produit: {e}")
            return None
