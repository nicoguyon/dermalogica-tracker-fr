"""Module de scrapers pour différents sites de cosmétique."""

from .sephora import SephoraScraper
from .nocibe import NocibeScraper
from .marionnaud import MarionnaudScraper
from .lookfantastic import LookfantasticScraper
from .feelunique import FeeluniqueScraper

__all__ = [
    'SephoraScraper',
    'NocibeScraper',
    'MarionnaudScraper',
    'LookfantasticScraper',
    'FeeluniqueScraper'
]
