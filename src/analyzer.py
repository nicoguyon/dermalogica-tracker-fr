"""Module d'analyse comparative des produits et marques."""

import logging
from typing import Dict, List, Optional
from collections import defaultdict
from statistics import mean, median
from config import TARGET_BRANDS, BRAND_ALIASES

logger = logging.getLogger(__name__)


class ProductAnalyzer:
    """Analyse comparative des produits cosmétiques."""

    def __init__(self, products: List[Dict]):
        """Initialise l'analyseur avec une liste de produits.

        Args:
            products: Liste de produits à analyser
        """
        self.products = products
        self.brands_data = self._group_by_brand()

    def _normalize_brand(self, brand: str) -> str:
        """Normalise le nom d'une marque.

        Args:
            brand: Nom de la marque

        Returns:
            Nom normalisé
        """
        if not brand:
            return 'unknown'

        brand_lower = brand.lower().strip()

        # Chercher dans les alias
        for canonical, aliases in BRAND_ALIASES.items():
            for alias in aliases:
                if alias.lower() in brand_lower or brand_lower in alias.lower():
                    return canonical

        return brand_lower

    def _group_by_brand(self) -> Dict[str, List[Dict]]:
        """Groupe les produits par marque.

        Returns:
            Dictionnaire {marque: [produits]}
        """
        grouped = defaultdict(list)

        for product in self.products:
            brand = self._normalize_brand(product.get('brand', ''))
            grouped[brand].append(product)

        return dict(grouped)

    def get_brand_stats(self, brand: str = None) -> Dict:
        """Calcule les statistiques pour une marque.

        Args:
            brand: Nom de la marque (None = toutes)

        Returns:
            Dictionnaire de statistiques
        """
        if brand:
            brand_normalized = self._normalize_brand(brand)
            products = self.brands_data.get(brand_normalized, [])
        else:
            products = self.products

        if not products:
            return {
                'count': 0,
                'avg_price': 0,
                'min_price': 0,
                'max_price': 0,
                'median_price': 0
            }

        prices = [p['current_price'] for p in products if p.get('current_price')]

        return {
            'count': len(products),
            'avg_price': round(mean(prices), 2) if prices else 0,
            'min_price': round(min(prices), 2) if prices else 0,
            'max_price': round(max(prices), 2) if prices else 0,
            'median_price': round(median(prices), 2) if prices else 0,
            'sites': list(set(p['site'] for p in products))
        }

    def compare_brands(self, brands: Optional[List[str]] = None) -> Dict[str, Dict]:
        """Compare les statistiques entre plusieurs marques.

        Args:
            brands: Liste de marques à comparer (None = TARGET_BRANDS)

        Returns:
            Dictionnaire {marque: stats}
        """
        if not brands:
            brands = TARGET_BRANDS

        comparison = {}

        for brand in brands:
            brand_normalized = self._normalize_brand(brand)
            comparison[brand] = self.get_brand_stats(brand_normalized)

        return comparison

    def find_price_competitors(self, product: Dict, price_tolerance: float = 5.0) -> List[Dict]:
        """Trouve les produits concurrents dans une fourchette de prix.

        Args:
            product: Produit de référence
            price_tolerance: Tolérance de prix en €

        Returns:
            Liste de produits concurrents
        """
        if not product.get('current_price'):
            return []

        ref_price = product['current_price']
        ref_brand = self._normalize_brand(product.get('brand', ''))

        competitors = []

        for p in self.products:
            if not p.get('current_price'):
                continue

            # Même marque = ignorer
            if self._normalize_brand(p.get('brand', '')) == ref_brand:
                continue

            # Dans la fourchette de prix
            price_diff = abs(p['current_price'] - ref_price)
            if price_diff <= price_tolerance:
                competitors.append({
                    **p,
                    'price_diff': round(price_diff, 2),
                    'price_diff_percent': round((price_diff / ref_price) * 100, 1)
                })

        # Trier par différence de prix
        competitors.sort(key=lambda x: x['price_diff'])

        return competitors

    def get_price_positioning(self, brand: str) -> str:
        """Détermine le positionnement prix d'une marque.

        Args:
            brand: Nom de la marque

        Returns:
            Catégorie de prix: 'premium', 'moyen', 'accessible'
        """
        stats = self.get_brand_stats(brand)
        avg_price = stats.get('avg_price', 0)

        if avg_price == 0:
            return 'unknown'

        # Calculer la moyenne globale
        all_prices = [p['current_price'] for p in self.products if p.get('current_price')]
        global_avg = mean(all_prices) if all_prices else 0

        if avg_price > global_avg * 1.5:
            return 'premium'
        elif avg_price > global_avg * 0.8:
            return 'moyen'
        else:
            return 'accessible'

    def find_best_deals_by_brand(self, brand: str, limit: int = 5) -> List[Dict]:
        """Trouve les meilleurs prix pour une marque.

        Args:
            brand: Nom de la marque
            limit: Nombre de résultats

        Returns:
            Liste de produits avec meilleurs prix
        """
        brand_normalized = self._normalize_brand(brand)
        products = self.brands_data.get(brand_normalized, [])

        # Filtrer produits avec prix
        products_with_price = [p for p in products if p.get('current_price')]

        # Trier par prix croissant
        products_with_price.sort(key=lambda x: x['current_price'])

        return products_with_price[:limit]

    def get_novelties_by_brand(self, days: int = 7) -> Dict[str, List[Dict]]:
        """Groupe les nouveautés par marque.

        Args:
            days: Nombre de jours pour la nouveauté

        Returns:
            Dictionnaire {marque: [nouveautés]}
        """
        from datetime import datetime, timedelta

        cutoff_date = datetime.now() - timedelta(days=days)
        novelties = defaultdict(list)

        for product in self.products:
            detected_at = product.get('detected_at')
            if not detected_at:
                continue

            try:
                detected_date = datetime.fromisoformat(detected_at.replace('Z', '+00:00'))
                if detected_date >= cutoff_date:
                    brand = self._normalize_brand(product.get('brand', ''))
                    novelties[brand].append(product)
            except (ValueError, TypeError):
                continue

        return dict(novelties)

    def generate_comparison_report(self, brands: Optional[List[str]] = None) -> Dict:
        """Génère un rapport de comparaison complet.

        Args:
            brands: Liste de marques à comparer

        Returns:
            Rapport complet
        """
        comparison = self.compare_brands(brands)

        # Ajouter positionnement prix
        for brand, stats in comparison.items():
            stats['positioning'] = self.get_price_positioning(brand)

        # Classement par prix moyen
        ranked = sorted(
            comparison.items(),
            key=lambda x: x[1]['avg_price'],
            reverse=True
        )

        return {
            'brands': comparison,
            'ranking': [{'brand': b, **stats} for b, stats in ranked],
            'total_products': len(self.products),
            'total_brands': len(comparison)
        }

    def export_enhanced_products(self) -> List[Dict]:
        """Exporte les produits avec données d'analyse enrichies.

        Returns:
            Liste de produits enrichis
        """
        enhanced = []

        for product in self.products:
            # Copier le produit original
            enhanced_product = product.copy()

            # Ajouter stats de la marque
            brand = self._normalize_brand(product.get('brand', ''))
            brand_stats = self.get_brand_stats(brand)

            enhanced_product['brand_avg_price'] = brand_stats['avg_price']
            enhanced_product['brand_positioning'] = self.get_price_positioning(brand)

            # Calculer écart au prix moyen de la marque
            if product.get('current_price') and brand_stats['avg_price'] > 0:
                price_diff = product['current_price'] - brand_stats['avg_price']
                enhanced_product['price_vs_brand_avg'] = round(price_diff, 2)
                enhanced_product['price_vs_brand_avg_percent'] = round(
                    (price_diff / brand_stats['avg_price']) * 100, 1
                )

            # Trouver concurrents directs
            competitors = self.find_price_competitors(product, price_tolerance=5.0)
            if competitors:
                enhanced_product['competitors_count'] = len(competitors)
                enhanced_product['cheapest_competitor'] = competitors[0]['name'] if competitors else None
                enhanced_product['cheapest_competitor_price'] = competitors[0]['current_price'] if competitors else None

            enhanced.append(enhanced_product)

        return enhanced
