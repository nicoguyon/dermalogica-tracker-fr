"""Modèles et gestion de la base de données SQLite."""

import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import json

logger = logging.getLogger(__name__)


class Database:
    """Gestion de la base de données SQLite."""

    def __init__(self, db_path: Path):
        """Initialise la connexion à la base de données.

        Args:
            db_path: Chemin vers le fichier SQLite
        """
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Crée les tables si elles n'existent pas."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Table produits
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    site TEXT NOT NULL,
                    product_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    brand TEXT,
                    category TEXT,
                    url TEXT,
                    image_url TEXT,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(site, product_id)
                )
            """)

            # Table prix (historique)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    price REAL NOT NULL,
                    currency TEXT DEFAULT 'EUR',
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            """)

            # Table nouveautés
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS new_products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            """)

            # Index pour optimiser les requêtes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_products_site
                ON products(site)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_prices_product
                ON prices(product_id, timestamp)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_new_products_detected
                ON new_products(detected_at)
            """)

            conn.commit()
            logger.info(f"Base de données initialisée: {self.db_path}")

    def add_product(self, site: str, product_data: Dict) -> int:
        """Ajoute ou met à jour un produit.

        Args:
            site: Nom du site (sephora, nocibe, marionnaud)
            product_data: Dictionnaire avec les données du produit

        Returns:
            ID du produit dans la base
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Vérifier si le produit existe
            cursor.execute("""
                SELECT id FROM products
                WHERE site = ? AND product_id = ?
            """, (site, product_data['product_id']))

            result = cursor.fetchone()

            if result:
                # Mise à jour
                product_id = result[0]
                cursor.execute("""
                    UPDATE products
                    SET name = ?, brand = ?, category = ?,
                        url = ?, image_url = ?, last_updated = ?
                    WHERE id = ?
                """, (
                    product_data['name'],
                    product_data.get('brand'),
                    product_data.get('category'),
                    product_data.get('url'),
                    product_data.get('image_url'),
                    datetime.now(),
                    product_id
                ))
            else:
                # Insertion
                cursor.execute("""
                    INSERT INTO products
                    (site, product_id, name, brand, category, url, image_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    site,
                    product_data['product_id'],
                    product_data['name'],
                    product_data.get('brand'),
                    product_data.get('category'),
                    product_data.get('url'),
                    product_data.get('image_url')
                ))
                product_id = cursor.lastrowid

                # Marquer comme nouveauté
                cursor.execute("""
                    INSERT INTO new_products (product_id)
                    VALUES (?)
                """, (product_id,))

            conn.commit()
            return product_id

    def add_price(self, product_id: int, price: float, currency: str = 'EUR'):
        """Ajoute un prix au historique.

        Args:
            product_id: ID du produit
            price: Prix
            currency: Devise
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO prices (product_id, price, currency)
                VALUES (?, ?, ?)
            """, (product_id, price, currency))
            conn.commit()

    def get_products(self, site: Optional[str] = None,
                     limit: Optional[int] = None) -> List[Dict]:
        """Récupère les produits.

        Args:
            site: Filtrer par site (optionnel)
            limit: Nombre max de résultats (optionnel)

        Returns:
            Liste de dictionnaires avec les produits
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = """
                SELECT p.*,
                       (SELECT price FROM prices
                        WHERE product_id = p.id
                        ORDER BY timestamp DESC LIMIT 1) as current_price
                FROM products p
            """
            params = []

            if site:
                query += " WHERE p.site = ?"
                params.append(site)

            query += " ORDER BY p.last_updated DESC"

            if limit:
                query += f" LIMIT {limit}"

            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_price_history(self, product_id: int) -> List[Dict]:
        """Récupère l'historique des prix d'un produit.

        Args:
            product_id: ID du produit

        Returns:
            Liste des prix avec timestamps
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT price, currency, timestamp
                FROM prices
                WHERE product_id = ?
                ORDER BY timestamp DESC
            """, (product_id,))

            return [dict(row) for row in cursor.fetchall()]

    def get_new_products(self, days: int = 7) -> List[Dict]:
        """Récupère les nouveautés récentes.

        Args:
            days: Nombre de jours (défaut: 7)

        Returns:
            Liste des nouveaux produits
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT p.*, np.detected_at,
                       (SELECT price FROM prices
                        WHERE product_id = p.id
                        ORDER BY timestamp DESC LIMIT 1) as current_price
                FROM products p
                JOIN new_products np ON p.id = np.product_id
                WHERE datetime(np.detected_at) > datetime('now', '-' || ? || ' days')
                ORDER BY np.detected_at DESC
            """, (days,))

            return [dict(row) for row in cursor.fetchall()]

    def get_stats(self) -> Dict:
        """Récupère les statistiques de la base.

        Returns:
            Dictionnaire avec les stats
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Total produits par site
            cursor.execute("""
                SELECT site, COUNT(*) as count
                FROM products
                GROUP BY site
            """)
            products_by_site = dict(cursor.fetchall())

            # Total produits
            cursor.execute("SELECT COUNT(*) FROM products")
            total_products = cursor.fetchone()[0]

            # Nouveautés 7 derniers jours
            cursor.execute("""
                SELECT COUNT(*) FROM new_products
                WHERE datetime(detected_at) > datetime('now', '-7 days')
            """)
            new_last_week = cursor.fetchone()[0]

            # Total prix enregistrés
            cursor.execute("SELECT COUNT(*) FROM prices")
            total_prices = cursor.fetchone()[0]

            return {
                'total_products': total_products,
                'products_by_site': products_by_site,
                'new_last_week': new_last_week,
                'total_prices': total_prices
            }
