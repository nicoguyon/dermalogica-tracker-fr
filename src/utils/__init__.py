"""Utilitaires communs."""

from .logger import setup_logger
from .config import (
    BASE_DIR,
    DATA_DIR,
    EXPORTS_DIR,
    DATABASE_PATH,
    PLAYWRIGHT_CONFIG,
    SCRAPER_CONFIG,
    BASE_URLS,
    CATEGORIES,
)

__all__ = [
    "setup_logger",
    "BASE_DIR",
    "DATA_DIR",
    "EXPORTS_DIR",
    "DATABASE_PATH",
    "PLAYWRIGHT_CONFIG",
    "SCRAPER_CONFIG",
    "BASE_URLS",
    "CATEGORIES",
]
