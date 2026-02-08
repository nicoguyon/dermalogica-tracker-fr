"""Scraper pour Nocibé."""

from typing import List, Optional
import re

from .base import BaseScraper
from ..database import Product
from ..utils import setup_logger, BASE_URLS

logger = setup_logger("nocibe_scraper")


class NocibeScraper(BaseScraper):
    """Scraper spécialisé pour Nocibé."""

    def __init__(self, headless: bool = True):
        super().__init__(headless)
        self.base_url = BASE_URLS['nocibe']
        self.source = "nocibe"

    def scrape_products(self, limit: Optional[int] = None, new_only: bool = False) -> List[Product]:
        """Scrape les produits Nocibé.

        Args:
            limit: Nombre maximum de produits
            new_only: Nouveautés uniquement

        Returns:
            Liste de produits
        """
        if new_only:
            url = f"{self.base_url}/nouveautes"
        else:
            url = f"{self.base_url}/maquillage"  # Catégorie par défaut

        logger.info(f"Scraping Nocibé : {url}")

        try:
            self.page.goto(url, wait_until='domcontentloaded')

            # Accepter les cookies
            try:
                cookie_btn = self.page.locator('button:has-text("Accepter")')
                if cookie_btn.is_visible(timeout=2000):
                    cookie_btn.click()
            except:
                pass

            # Attendre le chargement des produits
            self.page.wait_for_selector('.product-item', timeout=10000)

            # Scroll pour charger plus
            self._scroll_page(3)

            # Récupérer les produits
            product_elements = self.page.locator('.product-item').all()
            logger.info(f"Trouvé {len(product_elements)} produits sur la page")

            count = 0
            for element in product_elements:
                if limit and count >= limit:
                    break

                product = self._extract_product_data(element)
                if product:
                    self.products.append(product)
                    count += 1

                self._rate_limit()

            logger.info(f"✓ {len(self.products)} produits scrapés depuis Nocibé")

        except Exception as e:
            logger.error(f"Erreur lors du scraping Nocibé : {e}")

        return self.products

    def _scroll_page(self, times: int = 3):
        """Scroll la page pour charger plus de produits."""
        for _ in range(times):
            self.page.evaluate("window.scrollBy(0, window.innerHeight)")
            self.page.wait_for_timeout(1000)

    def _extract_product_data(self, element) -> Optional[Product]:
        """Extrait les données d'un produit Nocibé.

        Args:
            element: Élément Playwright

        Returns:
            Instance de Product ou None
        """
        try:
            # Nom
            name_elem = element.locator('.product-name, .product-title')
            name = name_elem.inner_text().strip() if name_elem.count() > 0 else ""

            if not name:
                return None

            # Marque
            brand_elem = element.locator('.product-brand, .brand-name')
            brand = brand_elem.inner_text().strip() if brand_elem.count() > 0 else "Inconnu"

            # Prix
            price_elem = element.locator('.price, .product-price')
            price_text = price_elem.inner_text().strip() if price_elem.count() > 0 else "0"

            price_match = re.search(r'(\d+[,.]?\d*)', price_text.replace(',', '.'))
            price = float(price_match.group(1)) if price_match else 0.0

            # URL
            link_elem = element.locator('a').first
            url = link_elem.get_attribute('href') if link_elem.count() > 0 else ""
            if url and not url.startswith('http'):
                url = f"{self.base_url}{url}"

            # Image
            img_elem = element.locator('img').first
            image_url = img_elem.get_attribute('src') if img_elem.count() > 0 else ""

            # Product ID
            product_id = self._extract_product_id(url)

            # Badge nouveau
            is_new = element.locator('text=Nouveau').count() > 0

            product = Product(
                source=self.source,
                product_id=product_id,
                name=name,
                brand=brand,
                price=price,
                currency="EUR",
                url=url,
                image_url=image_url,
                is_new=is_new,
                metadata={
                    "raw_price": price_text
                }
            )

            logger.debug(f"Produit extrait : {brand} - {name[:30]}... ({price}€)")
            return product

        except Exception as e:
            logger.warning(f"Erreur lors de l'extraction d'un produit : {e}")
            return None

    def _extract_product_id(self, url: str) -> str:
        """Extrait l'ID du produit depuis l'URL."""
        match = re.search(r'\/(\d+)\.', url)
        if match:
            return match.group(1)

        return url.split('/')[-1][:50]
