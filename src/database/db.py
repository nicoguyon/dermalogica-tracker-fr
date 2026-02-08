"""Gestionnaire de base de données SQLite."""

import sqlite3
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from .models import Product
from ..utils import DATABASE_PATH, setup_logger

logger = setup_logger("database")


class Database:
    """Gestionnaire de la base de données SQLite."""

    def __init__(self, db_path: Path = DATABASE_PATH):
        """Initialise la connexion à la base de données.

        Args:
            db_path: Chemin vers le fichier SQLite
        """
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Crée les tables si elles n'existent pas."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id TEXT PRIMARY KEY,
                    source TEXT NOT NULL,
                    product_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    brand TEXT NOT NULL,
                    price REAL NOT NULL,
                    currency TEXT DEFAULT 'EUR',
                    url TEXT,
                    image_url TEXT,
                    category TEXT,
                    is_new INTEGER DEFAULT 0,
                    scraped_at TEXT NOT NULL,
                    metadata TEXT,
                    UNIQUE(source, product_id)
                )
            """)

            # Index pour améliorer les performances
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_source ON products(source)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_brand ON products(brand)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_scraped_at ON products(scraped_at)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_is_new ON products(is_new)")

            conn.commit()

        logger.info(f"Base de données initialisée : {self.db_path}")

    def add_product(self, product: Product) -> bool:
        """Ajoute un produit à la base de données.

        Args:
            product: Instance de Product à ajouter

        Returns:
            True si ajouté, False si déjà existant
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                data = product.to_dict()

                cursor.execute("""
                    INSERT OR REPLACE INTO products
                    (id, source, product_id, name, brand, price, currency,
                     url, image_url, category, is_new, scraped_at, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    data['id'], data['source'], data['product_id'],
                    data['name'], data['brand'], data['price'], data['currency'],
                    data['url'], data['image_url'], data['category'],
                    1 if data['is_new'] else 0, data['scraped_at'], data['metadata']
                ))

                conn.commit()
                logger.debug(f"Produit ajouté : {product.brand} - {product.name[:30]}")
                return True

        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du produit : {e}")
            return False

    def add_products(self, products: List[Product]) -> int:
        """Ajoute plusieurs produits en batch.

        Args:
            products: Liste de produits

        Returns:
            Nombre de produits ajoutés
        """
        count = 0
        for product in products:
            if self.add_product(product):
                count += 1

        logger.info(f"{count}/{len(products)} produits ajoutés à la base")
        return count

    def get_products(
        self,
        source: Optional[str] = None,
        brand: Optional[str] = None,
        new_only: bool = False,
        limit: Optional[int] = None
    ) -> List[Product]:
        """Récupère les produits avec filtres.

        Args:
            source: Filtrer par source (sephora, nocibe, marionnaud)
            brand: Filtrer par marque
            new_only: Uniquement les nouveautés
            limit: Limite de résultats

        Returns:
            Liste de produits
        """
        query = "SELECT * FROM products WHERE 1=1"
        params = []

        if source:
            query += " AND source = ?"
            params.append(source)

        if brand:
            query += " AND brand LIKE ?"
            params.append(f"%{brand}%")

        if new_only:
            query += " AND is_new = 1"

        query += " ORDER BY scraped_at DESC"

        if limit:
            query += f" LIMIT {limit}"

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

        products = []
        for row in rows:
            data = dict(row)
            data['is_new'] = bool(data['is_new'])
            products.append(Product.from_dict(data))

        return products

    def get_stats(self, source: Optional[str] = None) -> Dict[str, Any]:
        """Récupère les statistiques de la base.

        Args:
            source: Statistiques pour une source spécifique

        Returns:
            Dictionnaire avec les statistiques
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            where_clause = f"WHERE source = '{source}'" if source else ""

            # Total produits
            cursor.execute(f"SELECT COUNT(*) FROM products {where_clause}")
            total = cursor.fetchone()[0]

            # Nouveautés
            cursor.execute(f"SELECT COUNT(*) FROM products {where_clause} {'AND' if source else 'WHERE'} is_new = 1")
            new_products = cursor.fetchone()[0]

            # Par source
            cursor.execute(f"SELECT source, COUNT(*) FROM products {where_clause} GROUP BY source")
            by_source = dict(cursor.fetchall())

            # Par marque (top 10)
            cursor.execute(f"""
                SELECT brand, COUNT(*) as count
                FROM products {where_clause}
                GROUP BY brand
                ORDER BY count DESC
                LIMIT 10
            """)
            top_brands = dict(cursor.fetchall())

            # Prix moyen
            cursor.execute(f"SELECT AVG(price) FROM products {where_clause}")
            avg_price = cursor.fetchone()[0] or 0

            # Dernier scraping
            cursor.execute(f"SELECT MAX(scraped_at) FROM products {where_clause}")
            last_scraped = cursor.fetchone()[0]

        return {
            "total_products": total,
            "new_products": new_products,
            "by_source": by_source,
            "top_brands": top_brands,
            "average_price": round(avg_price, 2),
            "last_scraped": last_scraped,
        }

    def clean_old_data(self, days: int = 30) -> int:
        """Supprime les données de plus de X jours.

        Args:
            days: Nombre de jours à conserver

        Returns:
            Nombre de produits supprimés
        """
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE scraped_at < ?", (cutoff_date,))
            deleted = cursor.rowcount
            conn.commit()

        logger.info(f"{deleted} produits supprimés (> {days} jours)")
        return deleted

    def clear_all(self) -> int:
        """Supprime toutes les données.

        Returns:
            Nombre de produits supprimés
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM products")
            count = cursor.fetchone()[0]
            cursor.execute("DELETE FROM products")
            conn.commit()

        logger.info(f"Base de données vidée : {count} produits supprimés")
        return count
