# Guide de contribution

## Ajouter un nouveau scraper

### 1. Créer le fichier scraper

Créer `src/scrapers/nouveau_site.py` :

```python
from typing import List, Optional
import re

from .base import BaseScraper
from ..database import Product
from ..utils import setup_logger, BASE_URLS

logger = setup_logger("nouveau_site_scraper")


class NouveauSiteScraper(BaseScraper):
    """Scraper pour NouveauSite."""

    def __init__(self, headless: bool = True):
        super().__init__(headless)
        self.base_url = BASE_URLS['nouveau_site']
        self.source = "nouveau_site"

    def scrape_products(self, limit: Optional[int] = None, new_only: bool = False) -> List[Product]:
        """Scrape les produits."""
        url = f"{self.base_url}/produits"
        logger.info(f"Scraping {self.source} : {url}")

        try:
            self.page.goto(url, wait_until='domcontentloaded')

            # Attendre les produits
            self.page.wait_for_selector('.product-card', timeout=10000)

            # Récupérer les éléments
            product_elements = self.page.locator('.product-card').all()

            count = 0
            for element in product_elements:
                if limit and count >= limit:
                    break

                product = self._extract_product_data(element)
                if product:
                    self.products.append(product)
                    count += 1

                self._rate_limit()

            logger.info(f"✓ {len(self.products)} produits scrapés")

        except Exception as e:
            logger.error(f"Erreur scraping : {e}")

        return self.products

    def _extract_product_data(self, element) -> Optional[Product]:
        """Extrait les données d'un produit."""
        try:
            # ADAPTER SELON LA STRUCTURE HTML DU SITE

            # Nom
            name_elem = element.locator('.product-name')
            name = name_elem.inner_text().strip()

            # Marque
            brand_elem = element.locator('.product-brand')
            brand = brand_elem.inner_text().strip()

            # Prix
            price_elem = element.locator('.price')
            price_text = price_elem.inner_text().strip()
            price_match = re.search(r'(\d+[,.]?\d*)', price_text.replace(',', '.'))
            price = float(price_match.group(1)) if price_match else 0.0

            # URL
            link = element.locator('a').first.get_attribute('href')
            url = f"{self.base_url}{link}" if not link.startswith('http') else link

            # Image
            img = element.locator('img').first.get_attribute('src')

            # ID
            product_id = self._extract_product_id(url)

            return Product(
                source=self.source,
                product_id=product_id,
                name=name,
                brand=brand,
                price=price,
                url=url,
                image_url=img,
            )

        except Exception as e:
            logger.warning(f"Erreur extraction : {e}")
            return None

    def _extract_product_id(self, url: str) -> str:
        """Extrait l'ID depuis l'URL."""
        # Adapter selon le format d'URL
        return url.split('/')[-1][:50]
```

### 2. Ajouter l'URL de base

Dans `src/utils/config.py`, ajouter :

```python
BASE_URLS = {
    "sephora": "https://www.sephora.fr",
    "nocibe": "https://www.nocibe.fr",
    "marionnaud": "https://www.marionnaud.fr",
    "nouveau_site": "https://www.nouveau-site.fr",  # AJOUTER ICI
}
```

### 3. Enregistrer le scraper

Dans `src/scrapers/__init__.py`, ajouter :

```python
from .nouveau_site import NouveauSiteScraper

SCRAPERS = {
    "sephora": SephoraScraper,
    "nocibe": NocibeScraper,
    "marionnaud": MarionnaudScraper,
    "nouveau_site": NouveauSiteScraper,  # AJOUTER ICI
}
```

### 4. Tester

```bash
python cli.py scrape --source nouveau_site --limit 5 --no-headless
```

## Méthode pour trouver les sélecteurs CSS

1. Ouvrir le site dans Chrome/Firefox
2. F12 → Inspecter un produit
3. Clic droit sur l'élément → Copy → Copy selector
4. Tester dans la console : `document.querySelector('votre-selecteur')`

## Bonnes pratiques

### Gestion des cookies
```python
try:
    cookie_btn = self.page.locator('button:has-text("Accepter")')
    if cookie_btn.is_visible(timeout=2000):
        cookie_btn.click()
except:
    pass
```

### Scroll infini
```python
def _scroll_page(self, times: int = 3):
    for _ in range(times):
        self.page.evaluate("window.scrollBy(0, window.innerHeight)")
        self.page.wait_for_timeout(1000)
```

### Pagination
```python
def _next_page(self) -> bool:
    """Aller à la page suivante."""
    try:
        next_btn = self.page.locator('.pagination .next')
        if next_btn.is_visible():
            next_btn.click()
            self.page.wait_for_timeout(2000)
            return True
    except:
        pass
    return False
```

### Retry sur erreur
```python
product = self._retry_on_failure(self._extract_product_data, element)
```

## Debugging

### Mode visuel
```bash
python cli.py scrape --source nouveau_site --no-headless
```

### Logs détaillés
Modifier dans le scraper :
```python
logger = setup_logger("nouveau_site_scraper", level=logging.DEBUG)
```

### Breakpoint Playwright
```python
self.page.pause()  # Ouvre l'inspecteur Playwright
```

## Tests

Créer `tests/test_nouveau_site.py` :

```python
from src.scrapers import get_scraper

def test_nouveau_site_scraper():
    with get_scraper('nouveau_site', headless=True) as scraper:
        products = scraper.scrape_products(limit=5)
        assert len(products) > 0
        assert products[0].source == "nouveau_site"
```

## Pull Request

1. Fork le projet
2. Créer une branche : `git checkout -b scraper-nouveau-site`
3. Commit : `git commit -m "Add nouveau_site scraper"`
4. Push : `git push origin scraper-nouveau-site`
5. Ouvrir une PR

## Checklist

- [ ] Scraper créé dans `src/scrapers/`
- [ ] URL ajoutée dans `config.py`
- [ ] Scraper enregistré dans `__init__.py`
- [ ] Testé avec `--limit 5 --no-headless`
- [ ] Testé avec `--new-only`
- [ ] Rate limiting respecté
- [ ] Logs informatifs
- [ ] Gestion des erreurs
- [ ] Documentation mise à jour
