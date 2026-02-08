"""Export des données en CSV."""

import csv
import logging
from pathlib import Path
from typing import List, Dict
from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)


class CSVExporter:
    """Exporter CSV."""

    def __init__(self, output_dir: Path):
        """Initialise l'exporter.

        Args:
            output_dir: Répertoire de sortie
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_products(self, products: List[Dict],
                       filename: str = None) -> Path:
        """Export les produits en CSV.

        Args:
            products: Liste de produits
            filename: Nom du fichier (optionnel)

        Returns:
            Chemin du fichier créé
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'products_{timestamp}.csv'

        output_path = self.output_dir / filename

        try:
            # Utiliser pandas pour un export plus robuste
            df = pd.DataFrame(products)

            # Réorganiser les colonnes si elles existent
            columns_order = [
                'site', 'product_id', 'name', 'brand', 'category',
                'current_price', 'url', 'image_url', 'first_seen', 'last_updated'
            ]
            existing_columns = [col for col in columns_order if col in df.columns]
            other_columns = [col for col in df.columns if col not in columns_order]
            final_columns = existing_columns + other_columns

            df = df[final_columns]

            # Export
            df.to_csv(output_path, index=False, encoding='utf-8-sig')

            logger.info(f"Export CSV réussi: {output_path} ({len(products)} produits)")
            return output_path

        except Exception as e:
            logger.error(f"Erreur export CSV: {e}")
            raise

    def export_price_history(self, price_history: List[Dict],
                            filename: str = None) -> Path:
        """Export l'historique des prix en CSV.

        Args:
            price_history: Liste des prix avec timestamps
            filename: Nom du fichier (optionnel)

        Returns:
            Chemin du fichier créé
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'price_history_{timestamp}.csv'

        output_path = self.output_dir / filename

        try:
            df = pd.DataFrame(price_history)

            # Réorganiser les colonnes
            columns_order = [
                'product_id', 'product_name', 'price', 'currency', 'timestamp'
            ]
            existing_columns = [col for col in columns_order if col in df.columns]
            other_columns = [col for col in df.columns if col not in columns_order]
            final_columns = existing_columns + other_columns

            df = df[final_columns]

            df.to_csv(output_path, index=False, encoding='utf-8-sig')

            logger.info(f"Export historique CSV réussi: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Erreur export historique CSV: {e}")
            raise

    def export_new_products(self, new_products: List[Dict],
                           filename: str = None) -> Path:
        """Export les nouveautés en CSV.

        Args:
            new_products: Liste des nouveaux produits
            filename: Nom du fichier (optionnel)

        Returns:
            Chemin du fichier créé
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'new_products_{timestamp}.csv'

        output_path = self.output_dir / filename

        try:
            df = pd.DataFrame(new_products)

            # Réorganiser les colonnes
            columns_order = [
                'site', 'name', 'brand', 'current_price',
                'detected_at', 'url'
            ]
            existing_columns = [col for col in columns_order if col in df.columns]
            other_columns = [col for col in df.columns if col not in columns_order]
            final_columns = existing_columns + other_columns

            df = df[final_columns]

            df.to_csv(output_path, index=False, encoding='utf-8-sig')

            logger.info(f"Export nouveautés CSV réussi: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Erreur export nouveautés CSV: {e}")
            raise

    def export_comparison(self, comparison_report: Dict,
                         filename: str = None) -> Path:
        """Export le rapport de comparaison en CSV.

        Args:
            comparison_report: Rapport de comparaison entre marques
            filename: Nom du fichier (optionnel)

        Returns:
            Chemin du fichier créé
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'comparison_{timestamp}.csv'

        output_path = self.output_dir / filename

        try:
            # Créer un DataFrame depuis le ranking
            df = pd.DataFrame(comparison_report['ranking'])

            # Convertir la liste de sites en string
            if 'sites' in df.columns:
                df['sites'] = df['sites'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

            # Réorganiser les colonnes
            columns_order = [
                'brand', 'count', 'avg_price', 'min_price', 'max_price',
                'median_price', 'positioning', 'sites'
            ]
            existing_columns = [col for col in columns_order if col in df.columns]
            df = df[existing_columns]

            # Renommer pour plus de clarté
            df = df.rename(columns={
                'brand': 'Marque',
                'count': 'Nb_Produits',
                'avg_price': 'Prix_Moyen',
                'min_price': 'Prix_Min',
                'max_price': 'Prix_Max',
                'median_price': 'Prix_Median',
                'positioning': 'Positionnement',
                'sites': 'Sites'
            })

            df.to_csv(output_path, index=False, encoding='utf-8-sig')

            logger.info(f"Export comparaison CSV réussi: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Erreur export comparaison CSV: {e}")
            raise
