"""Export des données en JSON."""

import json
import logging
from pathlib import Path
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class JSONExporter:
    """Exporter JSON."""

    def __init__(self, output_dir: Path):
        """Initialise l'exporter.

        Args:
            output_dir: Répertoire de sortie
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_products(self, products: List[Dict],
                       filename: str = None) -> Path:
        """Export les produits en JSON.

        Args:
            products: Liste de produits
            filename: Nom du fichier (optionnel)

        Returns:
            Chemin du fichier créé
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'products_{timestamp}.json'

        output_path = self.output_dir / filename

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(products, f, ensure_ascii=False, indent=2)

            logger.info(f"Export JSON réussi: {output_path} ({len(products)} produits)")
            return output_path

        except Exception as e:
            logger.error(f"Erreur export JSON: {e}")
            raise

    def export_price_history(self, price_history: Dict[str, List[Dict]],
                            filename: str = None) -> Path:
        """Export l'historique des prix en JSON.

        Args:
            price_history: Historique par produit
            filename: Nom du fichier (optionnel)

        Returns:
            Chemin du fichier créé
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'price_history_{timestamp}.json'

        output_path = self.output_dir / filename

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(price_history, f, ensure_ascii=False, indent=2)

            logger.info(f"Export historique JSON réussi: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Erreur export historique JSON: {e}")
            raise

    def export_stats(self, stats: Dict, filename: str = None) -> Path:
        """Export les statistiques en JSON.

        Args:
            stats: Statistiques
            filename: Nom du fichier (optionnel)

        Returns:
            Chemin du fichier créé
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'stats_{timestamp}.json'

        output_path = self.output_dir / filename

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)

            logger.info(f"Export stats JSON réussi: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Erreur export stats JSON: {e}")
            raise

    def export_comparison(self, comparison_report: Dict, filename: str = None) -> Path:
        """Export le rapport de comparaison en JSON.

        Args:
            comparison_report: Rapport de comparaison entre marques
            filename: Nom du fichier (optionnel)

        Returns:
            Chemin du fichier créé
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'comparison_{timestamp}.json'

        output_path = self.output_dir / filename

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(comparison_report, f, ensure_ascii=False, indent=2)

            logger.info(f"Export comparaison JSON réussi: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Erreur export comparaison JSON: {e}")
            raise
