"""Export des données en format JSON."""

import json
from pathlib import Path
from typing import List
from datetime import datetime

from ..database import Product
from ..utils import setup_logger, EXPORTS_DIR

logger = setup_logger("json_exporter")


class JSONExporter:
    """Exporte les produits en format JSON."""

    @staticmethod
    def export(products: List[Product], output_path: Path = None) -> Path:
        """Exporte les produits en JSON.

        Args:
            products: Liste de produits
            output_path: Chemin de sortie (optionnel)

        Returns:
            Chemin du fichier généré
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = EXPORTS_DIR / f"products_{timestamp}.json"

        # Grouper par source
        grouped = {}
        for product in products:
            source = product.source
            if source not in grouped:
                grouped[source] = []

            # Convertir en dict
            data = product.to_dict()
            # Reconvertir metadata en dict pour JSON
            if isinstance(data['metadata'], str):
                data['metadata'] = json.loads(data['metadata'])

            grouped[source].append(data)

        # Structure finale
        output_data = {
            "export_date": datetime.now().isoformat(),
            "total_products": len(products),
            "sources": list(grouped.keys()),
            "products": grouped,
            "stats": {
                source: len(prods) for source, prods in grouped.items()
            }
        }

        # Écrire le fichier
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        logger.info(f"✓ Export JSON réussi : {output_path} ({len(products)} produits)")
        return output_path
