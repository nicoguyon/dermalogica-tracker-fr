"""Scrapers pour les différents sites."""

from .base import BaseScraper
from .sephora import SephoraScraper
from .nocibe import NocibeScraper
from .marionnaud import MarionnaudScraper

__all__ = [
    "BaseScraper",
    "SephoraScraper",
    "NocibeScraper",
    "MarionnaudScraper",
]

# Factory pour obtenir le bon scraper
SCRAPERS = {
    "sephora": SephoraScraper,
    "nocibe": NocibeScraper,
    "marionnaud": MarionnaudScraper,
}


def get_scraper(source: str, headless: bool = True) -> BaseScraper:
    """Factory pour obtenir le scraper approprié.

    Args:
        source: Source du scraper (sephora, nocibe, marionnaud)
        headless: Mode headless

    Returns:
        Instance du scraper

    Raises:
        ValueError: Si la source est invalide
    """
    scraper_class = SCRAPERS.get(source.lower())
    if not scraper_class:
        raise ValueError(f"Source invalide : {source}. Sources disponibles : {list(SCRAPERS.keys())}")

    return scraper_class(headless=headless)
