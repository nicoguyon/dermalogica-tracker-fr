"""Configuration du système de logging."""

import logging
import sys
from pathlib import Path
from datetime import datetime

def setup_logger(name: str = "cosmetique_scraper", level: int = logging.INFO):
    """Configure et retourne un logger.

    Args:
        name: Nom du logger
        level: Niveau de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Logger configuré
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Éviter de dupliquer les handlers
    if logger.handlers:
        return logger

    # Format des logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler fichier
    log_dir = Path.home() / "cosmetique-scraper" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"scraper_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
