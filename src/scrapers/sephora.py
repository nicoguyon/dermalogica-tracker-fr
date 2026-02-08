"""Scraper pour Sephora France."""

from typing import List, Optional
import re

from .base import BaseScraper
from ..database import Product
from ..utils import setup_logger, BASE_URLS

logger = setup_logger("sephora_scraper")


class SephoraScraper(BaseScraper):
    """Scraper spécialisé pour Sephora France."""

    def __init__(self, headless: bool = True):
        super().__init__(headless)
        self.base_url = BASE_URLS['sephora']
        self.source = "sephora"

    def scrape_products(self, limit: Optional[int] = None, new_only: bool = False) -> List[Product]:
        """Scrape les produits Sephora.

        Args:
            limit: Nombre maximum de produits
            new_only: Nouveautés uniquement

        Returns:
            Liste de produits
        """
        if new_only:
            url = f"{self.base_url}/nouveautes/"
        else:
            url = f"{self.base_url}/recherche?q=*"  # Tous les produits

        logger.info(f"Scraping Sephora : {url}")

        try:
            self.page.goto(url, wait_until='domcontentloaded')
            self.page.wait_for_selector('[data-comp="ProductTile"]', timeout=10000)

            # Accepter les cookies si nécessaire
            try:
                cookie_btn = self.page.locator('button:has-text("Accepter")')
                if cookie_btn.is_visible(timeout=2000):
                    cookie_btn.click()
            except:
                pass

            # Scroll pour charger plus de produits
            self._scroll_page(3)

            # Récupérer tous les produits
            product_elements = self.page.locator('[data-comp="ProductTile"]').all()
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

            logger.info(f"✓ {len(self.products)} produits scrapés depuis Sephora")

        except Exception as e:
            logger.error(f"Erreur lors du scraping Sephora : {e}")

        return self.products

    def _scroll_page(self, times: int = 3):
        """Scroll la page pour charger plus de produits."""
        for _ in range(times):
            self.page.evaluate("window.scrollBy(0, window.innerHeight)")
            self.page.wait_for_timeout(1000)

    def _extract_product_data(self, element) -> Optional[Product]:
        """Extrait les données d'un produit Sephora.

        Args:
            element: Élément Playwright

        Returns:
            Instance de Product ou None
        """
        try:
            # Nom du produit
            name_elem = element.locator('[data-comp="ProductName"]')
            name = name_elem.inner_text().strip() if name_elem.count() > 0 else ""

            if not name:
                return None

            # Marque
            brand_elem = element.locator('[data-comp="BrandName"]')
            brand = brand_elem.inner_text().strip() if brand_elem.count() > 0 else "Inconnu"

            # Prix
            price_elem = element.locator('[data-comp="Price"]')
            price_text = price_elem.inner_text().strip() if price_elem.count() > 0 else "0"

            # Extraire le prix numérique (ex: "12,99 €" -> 12.99)
            price_match = re.search(r'(\d+[,.]?\d*)', price_text.replace(',', '.'))
            price = float(price_match.group(1)) if price_match else 0.0

            # URL du produit
            link_elem = element.locator('a').first
            url = link_elem.get_attribute('href') if link_elem.count() > 0 else ""
            if url and not url.startswith('http'):
                url = f"{self.base_url}{url}"

            # Image
            img_elem = element.locator('img').first
            image_url = img_elem.get_attribute('src') if img_elem.count() > 0 else ""

            # Product ID depuis l'URL
            product_id = self._extract_product_id(url)

            # Badge "Nouveau"
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
        """Extrait l'ID du produit depuis l'URL.

        Args:
            url: URL du produit

        Returns:
            Product ID ou URL hashée
        """
        # Sephora URL format: /p/product-name-P123456
        match = re.search(r'P(\d+)', url)
        if match:
            return f"P{match.group(1)}"

        # Fallback: utiliser l'URL complète
        return url.split('/')[-1][:50]
