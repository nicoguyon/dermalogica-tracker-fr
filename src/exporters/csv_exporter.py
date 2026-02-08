"""Export des données en format CSV."""

import csv
from pathlib import Path
from typing import List
from datetime import datetime

from ..database import Product
from ..utils import setup_logger, EXPORTS_DIR

logger = setup_logger("csv_exporter")


class CSVExporter:
    """Exporte les produits en format CSV."""

    HEADERS = [
        "id",
        "source",
        "product_id",
        "name",
        "brand",
        "price",
        "currency",
        "url",
        "image_url",
        "category",
        "is_new",
        "scraped_at",
    ]

    @staticmethod
    def export(products: List[Product], output_path: Path = None) -> Path:
        """Exporte les produits en CSV.

        Args:
            products: Liste de produits
            output_path: Chemin de sortie (optionnel)

        Returns:
            Chemin du fichier généré
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = EXPORTS_DIR / f"products_{timestamp}.csv"

        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=CSVExporter.HEADERS)
            writer.writeheader()

            for product in products:
                row = {
                    "id": product.id,
                    "source": product.source,
                    "product_id": product.product_id,
                    "name": product.name,
                    "brand": product.brand,
                    "price": product.price,
                    "currency": product.currency,
                    "url": product.url,
                    "image_url": product.image_url,
                    "category": product.category,
                    "is_new": "Oui" if product.is_new else "Non",
                    "scraped_at": product.scraped_at,
                }
                writer.writerow(row)

        logger.info(f"✓ Export CSV réussi : {output_path} ({len(products)} produits)")
        return output_path
