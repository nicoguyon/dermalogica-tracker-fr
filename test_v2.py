#!/usr/bin/env python3
"""Tests de validation pour Cosmetique Scraper V2."""

import sys
from pathlib import Path

# Ajouter le répertoire au path
sys.path.insert(0, str(Path(__file__).parent))

from config import TARGET_BRANDS, BRAND_ALIASES, SITES
from scrapers import (
    SephoraScraper, NocibeScraper, MarionnaudScraper,
    LookfantasticScraper, FeeluniqueScraper
)
from src.analyzer import ProductAnalyzer
from exporters import JSONExporter, CSVExporter


def test_configuration():
    """Test de la configuration."""
    print("\n🔧 Test Configuration")
    print("-" * 50)

    # Test marques cibles
    assert len(TARGET_BRANDS) == 8, "Doit avoir 8 marques cibles"
    assert 'dermalogica' in TARGET_BRANDS, "Dermalogica doit être dans les cibles"
    print(f"✓ {len(TARGET_BRANDS)} marques cibles configurées")

    # Test aliases
    assert len(BRAND_ALIASES) >= 8, "Doit avoir au moins 8 alias configurés"
    assert 'dermalogica' in BRAND_ALIASES, "Dermalogica doit avoir des alias"
    print(f"✓ {len(BRAND_ALIASES)} marques avec aliases")

    # Test sites
    assert len(SITES) == 5, "Doit avoir 5 sites configurés"
    assert 'lookfantastic' in SITES, "Lookfantastic doit être configuré"
    assert 'feelunique' in SITES, "Feelunique doit être configuré"
    print(f"✓ {len(SITES)} sites configurés")

    print("\n✅ Configuration : OK\n")


def test_scrapers():
    """Test des scrapers."""
    print("\n🔍 Test Scrapers")
    print("-" * 50)

    scrapers = [
        ('Sephora', SephoraScraper),
        ('Nocibé', NocibeScraper),
        ('Marionnaud', MarionnaudScraper),
        ('Lookfantastic', LookfantasticScraper),
        ('Feelunique', FeeluniqueScraper)
    ]

    for name, ScraperClass in scrapers:
        scraper = ScraperClass()
        assert scraper.site_name is not None, f"{name} doit avoir un site_name"
        assert scraper.base_url is not None, f"{name} doit avoir un base_url"

        # Test de la méthode de matching
        assert hasattr(scraper, '_match_brands'), f"{name} doit avoir _match_brands"

        print(f"✓ {name:15s} : {scraper.base_url}")
        scraper.close()

    print("\n✅ Scrapers : OK\n")


def test_brand_matching():
    """Test du matching de marques."""
    print("\n🏷️  Test Matching Marques")
    print("-" * 50)

    from scrapers.base import BaseScraper

    # Créer un scraper de test
    scraper = BaseScraper(site_name='test', base_url='https://test.com')

    # Test matching exact
    assert scraper._match_brands('Dermalogica', ['dermalogica']), "Match exact Dermalogica"
    assert scraper._match_brands('DERMALOGICA', ['dermalogica']), "Match case insensitive"

    # Test matching avec alias
    assert scraper._match_brands('Drunk Elephant', ['drunk elephant']), "Match Drunk Elephant"
    assert scraper._match_brands('SkinCeuticals', ['skinceuticals']), "Match SkinCeuticals"

    # Test pas de match
    assert not scraper._match_brands('Random Brand', ['dermalogica']), "Pas de match pour Random Brand"

    # Test sans filtre (doit accepter tout)
    assert scraper._match_brands('Any Brand', None), "Sans filtre = accepte tout"

    print("✓ Match exact")
    print("✓ Match case insensitive")
    print("✓ Match avec alias")
    print("✓ Pas de match pour marque inconnue")
    print("✓ Sans filtre accepte tout")

    print("\n✅ Matching : OK\n")


def test_analyzer():
    """Test du module d'analyse."""
    print("\n📊 Test Analyzer")
    print("-" * 50)

    # Créer des données de test
    test_products = [
        {
            'id': 1,
            'brand': 'Dermalogica',
            'name': 'Daily Microfoliant',
            'current_price': 59.00,
            'site': 'sephora',
            'detected_at': '2026-02-08 10:00:00'
        },
        {
            'id': 2,
            'brand': 'Dermalogica',
            'name': 'Special Cleansing Gel',
            'current_price': 49.00,
            'site': 'nocibe',
            'detected_at': '2026-02-08 10:00:00'
        },
        {
            'id': 3,
            'brand': 'SkinCeuticals',
            'name': 'C E Ferulic',
            'current_price': 165.00,
            'site': 'sephora',
            'detected_at': '2026-02-08 10:00:00'
        }
    ]

    analyzer = ProductAnalyzer(test_products)

    # Test stats par marque
    stats = analyzer.get_brand_stats('dermalogica')
    assert stats['count'] == 2, "Doit avoir 2 produits Dermalogica"
    assert stats['avg_price'] == 54.0, "Prix moyen Dermalogica doit être 54.0"
    print(f"✓ Stats Dermalogica : {stats['count']} produits, {stats['avg_price']}€ moyen")

    # Test comparaison
    comparison = analyzer.compare_brands(['dermalogica', 'skinceuticals'])
    assert 'dermalogica' in comparison, "Dermalogica doit être dans la comparaison"
    assert 'skinceuticals' in comparison, "SkinCeuticals doit être dans la comparaison"
    print(f"✓ Comparaison : {len(comparison)} marques comparées")

    # Test positionnement
    positioning = analyzer.get_price_positioning('dermalogica')
    assert positioning in ['premium', 'moyen', 'accessible'], "Positionnement doit être valide"
    print(f"✓ Positionnement Dermalogica : {positioning}")

    # Test export enrichi
    enriched = analyzer.export_enhanced_products()
    assert len(enriched) == len(test_products), "Même nombre de produits enrichis"
    assert 'brand_avg_price' in enriched[0], "Doit avoir brand_avg_price"
    assert 'brand_positioning' in enriched[0], "Doit avoir brand_positioning"
    print(f"✓ Export enrichi : {len(enriched)} produits avec données comparatives")

    print("\n✅ Analyzer : OK\n")


def test_exporters():
    """Test des exporters."""
    print("\n📦 Test Exporters")
    print("-" * 50)

    # Créer répertoire temp
    from tempfile import mkdtemp
    temp_dir = Path(mkdtemp())

    test_data = [
        {'id': 1, 'name': 'Test Product', 'brand': 'Dermalogica', 'price': 59.00}
    ]

    # Test JSON Exporter
    json_exporter = JSONExporter(temp_dir)
    json_path = json_exporter.export_products(test_data, filename='test_products.json')
    assert json_path.exists(), "Fichier JSON doit exister"
    print(f"✓ JSON Export : {json_path.name}")

    # Test CSV Exporter
    csv_exporter = CSVExporter(temp_dir)
    csv_path = csv_exporter.export_products(test_data, filename='test_products.csv')
    assert csv_path.exists(), "Fichier CSV doit exister"
    print(f"✓ CSV Export : {csv_path.name}")

    # Test export comparaison
    comparison_data = {
        'brands': {'dermalogica': {'count': 10, 'avg_price': 55.0}},
        'ranking': [{'brand': 'dermalogica', 'count': 10, 'avg_price': 55.0}],
        'total_products': 10,
        'total_brands': 1
    }

    comp_json = json_exporter.export_comparison(comparison_data, filename='test_comparison.json')
    assert comp_json.exists(), "Comparaison JSON doit exister"
    print(f"✓ Comparaison JSON : {comp_json.name}")

    comp_csv = csv_exporter.export_comparison(comparison_data, filename='test_comparison.csv')
    assert comp_csv.exists(), "Comparaison CSV doit exister"
    print(f"✓ Comparaison CSV : {comp_csv.name}")

    # Nettoyage
    import shutil
    shutil.rmtree(temp_dir)

    print("\n✅ Exporters : OK\n")


def main():
    """Lance tous les tests."""
    print("=" * 50)
    print("🧪 TESTS COSMETIQUE SCRAPER V2")
    print("=" * 50)

    try:
        test_configuration()
        test_scrapers()
        test_brand_matching()
        test_analyzer()
        test_exporters()

        print("=" * 50)
        print("✅ TOUS LES TESTS RÉUSSIS")
        print("=" * 50)
        print("\n✨ Le projet est prêt à utiliser !\n")

        return 0

    except AssertionError as e:
        print(f"\n❌ ÉCHEC : {e}\n")
        return 1
    except Exception as e:
        print(f"\n❌ ERREUR : {e}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
