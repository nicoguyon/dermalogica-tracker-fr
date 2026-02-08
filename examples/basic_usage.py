#!/usr/bin/env python3
"""Exemple d'utilisation basique de Cosmetique Scraper."""

import sys
from pathlib import Path

# Ajouter le dossier parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scrapers import get_scraper
from src.database import Database
from src.exporters import JSONExporter, CSVExporter


def example_1_basic_scraping():
    """Exemple 1 : Scraping basique de Sephora."""
    print("=== Exemple 1 : Scraping Sephora ===\n")

    with get_scraper('sephora', headless=True) as scraper:
        products = scraper.scrape_products(limit=10)

        print(f"✓ {len(products)} produits scrapés\n")

        # Afficher quelques produits
        for product in products[:3]:
            print(f"  • {product.brand} - {product.name[:40]}... ({product.price}€)")


def example_2_save_to_database():
    """Exemple 2 : Sauvegarder en base de données."""
    print("\n=== Exemple 2 : Sauvegarder en base ===\n")

    # Scraper
    with get_scraper('sephora', headless=True) as scraper:
        products = scraper.scrape_products(limit=5)

    # Sauvegarder
    db = Database()
    count = db.add_products(products)

    print(f"✓ {count} produits ajoutés à la base")

    # Récupérer et afficher
    all_products = db.get_products(source='sephora')
    print(f"✓ Total Sephora en base : {len(all_products)}")


def example_3_export_data():
    """Exemple 3 : Exporter les données."""
    print("\n=== Exemple 3 : Export ===\n")

    db = Database()
    products = db.get_products(limit=10)

    if products:
        # Export JSON
        json_path = JSONExporter.export(products, Path('example_export.json'))
        print(f"✓ Export JSON : {json_path}")

        # Export CSV
        csv_path = CSVExporter.export(products, Path('example_export.csv'))
        print(f"✓ Export CSV : {csv_path}")


def example_4_filter_by_brand():
    """Exemple 4 : Filtrer par marque."""
    print("\n=== Exemple 4 : Filtrer par marque ===\n")

    db = Database()

    # Rechercher une marque
    brand_name = "Dior"
    products = db.get_products(brand=brand_name)

    print(f"✓ {len(products)} produits trouvés pour '{brand_name}'")

    for product in products[:5]:
        print(f"  • {product.name[:50]}... - {product.price}€")


def example_5_statistics():
    """Exemple 5 : Statistiques."""
    print("\n=== Exemple 5 : Statistiques ===\n")

    db = Database()
    stats = db.get_stats()

    print(f"Total produits : {stats['total_products']}")
    print(f"Nouveautés : {stats['new_products']}")
    print(f"Prix moyen : {stats['average_price']:.2f}€")
    print(f"\nPar source :")
    for source, count in stats['by_source'].items():
        print(f"  • {source}: {count}")


def example_6_scrape_new_only():
    """Exemple 6 : Scraper uniquement les nouveautés."""
    print("\n=== Exemple 6 : Nouveautés uniquement ===\n")

    with get_scraper('nocibe', headless=True) as scraper:
        products = scraper.scrape_products(limit=10, new_only=True)

        new_products = [p for p in products if p.is_new]
        print(f"✓ {len(new_products)} nouveautés trouvées")

        for product in new_products[:3]:
            print(f"  🆕 {product.brand} - {product.name[:40]}...")


if __name__ == '__main__':
    print("🧴 Exemples d'utilisation - Cosmetique Scraper\n")
    print("=" * 50)

    try:
        # Décommenter les exemples à tester

        # example_1_basic_scraping()
        # example_2_save_to_database()
        # example_3_export_data()
        # example_4_filter_by_brand()
        example_5_statistics()
        # example_6_scrape_new_only()

        print("\n" + "=" * 50)
        print("✓ Exemples terminés")

    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
