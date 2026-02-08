#!/usr/bin/env python3
"""Interface CLI pour Cosmetique Scraper."""

import sys
import logging
from pathlib import Path
import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Import des modules
from config import DB_PATH, EXPORT_DIR, LOGS_DIR, LOG_FORMAT, LOG_LEVEL, TARGET_BRANDS
from database import Database
from scrapers import (
    SephoraScraper, NocibeScraper, MarionnaudScraper,
    LookfantasticScraper, FeeluniqueScraper
)
from exporters import JSONExporter, CSVExporter
from src.analyzer import ProductAnalyzer

console = Console()

# Configuration du logging
LOGS_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOGS_DIR / 'scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def get_scraper(site_name: str):
    """Retourne le scraper approprié."""
    scrapers = {
        'sephora': SephoraScraper,
        'nocibe': NocibeScraper,
        'marionnaud': MarionnaudScraper,
        'lookfantastic': LookfantasticScraper,
        'feelunique': FeeluniqueScraper
    }
    return scrapers.get(site_name)()


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """🛍️  Cosmetique Scraper - Scraping de produits cosmétiques."""
    pass


@cli.command()
@click.option('--site', type=click.Choice(['sephora', 'nocibe', 'marionnaud', 'lookfantastic', 'feelunique', 'all']),
              default='all', help='Site à scraper')
@click.option('--category', default='nouveautes', help='Catégorie à scraper')
@click.option('--max-pages', default=3, type=int, help='Nombre max de pages')
@click.option('--brands', help='Marques à filtrer (séparées par virgules)')
def scrape(site, category, max_pages, brands):
    """Scraper les produits depuis un ou plusieurs sites."""
    db = Database(DB_PATH)
    sites = ['sephora', 'nocibe', 'marionnaud', 'lookfantastic', 'feelunique'] if site == 'all' else [site]

    # Parser les marques
    brand_list = None
    if brands:
        brand_list = [b.strip() for b in brands.split(',')]
        console.print(f"[dim]Filtrage marques: {', '.join(brand_list)}[/dim]")

    console.print(f"\n[bold cyan]🔍 Scraping en cours...[/bold cyan]")
    console.print(f"Catégorie: {category} | Max pages: {max_pages}\n")

    total_products = 0

    for site_name in sites:
        try:
            console.print(f"[yellow]⏳ {site_name.upper()}...[/yellow]")

            scraper = get_scraper(site_name)
            products = scraper.scrape_products(category=category, max_pages=max_pages, brands=brand_list)

            # Sauvegarder en DB
            for product_data in products:
                product_id = db.add_product(site_name, product_data)
                if product_data.get('price'):
                    db.add_price(product_id, product_data['price'])

            total_products += len(products)
            console.print(f"[green]✓ {site_name.upper()}: {len(products)} produits[/green]")

            scraper.close()

        except Exception as e:
            console.print(f"[red]❌ Erreur {site_name}: {e}[/red]")
            logger.error(f"Erreur scraping {site_name}: {e}", exc_info=True)

    console.print(f"\n[bold green]✓ Total: {total_products} produits scrapés[/bold green]\n")


@cli.command()
@click.option('--format', 'fmt', type=click.Choice(['json', 'csv', 'both']),
              default='json', help='Format d\'export')
@click.option('--site', type=click.Choice(['sephora', 'nocibe', 'marionnaud', 'lookfantastic', 'feelunique']),
              help='Filtrer par site')
@click.option('--limit', type=int, help='Limiter le nombre de produits')
@click.option('--enhanced', is_flag=True, help='Export enrichi avec analyse comparative')
def export(fmt, site, limit, enhanced):
    """Exporter les produits de la base de données."""
    db = Database(DB_PATH)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    console.print(f"\n[bold cyan]📦 Export en cours...[/bold cyan]\n")

    # Récupérer les produits
    products = db.get_products(site=site, limit=limit)

    if not products:
        console.print("[yellow]⚠️  Aucun produit à exporter[/yellow]")
        return

    console.print(f"Produits à exporter: {len(products)}")

    # Enrichir si demandé
    if enhanced:
        console.print("[dim]Enrichissement avec analyse comparative...[/dim]")
        analyzer = ProductAnalyzer(products)
        products = analyzer.export_enhanced_products()
        console.print("[green]✓ Données enrichies[/green]")

    # Export
    try:
        if fmt in ['json', 'both']:
            json_exporter = JSONExporter(EXPORT_DIR)
            json_path = json_exporter.export_products(products)
            console.print(f"[green]✓ JSON: {json_path}[/green]")

        if fmt in ['csv', 'both']:
            csv_exporter = CSVExporter(EXPORT_DIR)
            csv_path = csv_exporter.export_products(products)
            console.print(f"[green]✓ CSV: {csv_path}[/green]")

        # Export rapport comparatif si enhanced
        if enhanced:
            analyzer = ProductAnalyzer(products)
            comparison = analyzer.generate_comparison_report()

            if fmt in ['json', 'both']:
                comp_json_path = json_exporter.export_comparison(comparison)
                console.print(f"[green]✓ Comparaison JSON: {comp_json_path}[/green]")

            if fmt in ['csv', 'both']:
                comp_csv_path = csv_exporter.export_comparison(comparison)
                console.print(f"[green]✓ Comparaison CSV: {comp_csv_path}[/green]")

        console.print()

    except Exception as e:
        console.print(f"[red]❌ Erreur export: {e}[/red]")
        logger.error(f"Erreur export: {e}", exc_info=True)


@cli.command()
@click.option('--site', type=click.Choice(['sephora', 'nocibe', 'marionnaud']),
              help='Filtrer par site')
@click.option('--days', type=int, default=7, help='Jours de nouveautés')
def new(site, days):
    """Afficher les nouveautés récentes."""
    db = Database(DB_PATH)

    console.print(f"\n[bold cyan]🆕 Nouveautés ({days} derniers jours)[/bold cyan]\n")

    new_products = db.get_new_products(days=days)

    if site:
        new_products = [p for p in new_products if p['site'] == site]

    if not new_products:
        console.print("[yellow]⚠️  Aucune nouveauté[/yellow]")
        return

    # Table
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Site", style="cyan", width=12)
    table.add_column("Marque", style="magenta", width=15)
    table.add_column("Produit", style="white", width=40)
    table.add_column("Prix", style="green", justify="right")
    table.add_column("Détecté", style="dim", width=12)

    for product in new_products[:20]:  # Limiter à 20
        table.add_row(
            product['site'],
            product.get('brand') or 'N/A',
            product['name'][:40],
            f"{product.get('current_price', 0):.2f} €" if product.get('current_price') else 'N/A',
            product['detected_at'][:10]
        )

    console.print(table)
    console.print(f"\n[dim]Total: {len(new_products)} nouveautés[/dim]\n")


@cli.command()
def stats():
    """Afficher les statistiques de la base de données."""
    db = Database(DB_PATH)

    console.print("\n[bold cyan]📊 Statistiques[/bold cyan]\n")

    stats = db.get_stats()

    # Table générale
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Métrique", style="cyan", width=30)
    table.add_column("Valeur", style="green", justify="right")

    table.add_row("Total produits", str(stats['total_products']))
    table.add_row("Nouveautés (7j)", str(stats['new_last_week']))
    table.add_row("Prix enregistrés", str(stats['total_prices']))

    console.print(table)

    # Table par site
    if stats['products_by_site']:
        console.print()
        site_table = Table(show_header=True, header_style="bold cyan")
        site_table.add_column("Site", style="cyan")
        site_table.add_column("Produits", style="green", justify="right")

        for site, count in stats['products_by_site'].items():
            site_table.add_row(site.upper(), str(count))

        console.print(site_table)

    console.print()


@cli.command()
@click.option('--brands', help='Marques à comparer (séparées par virgules, "all" pour toutes)')
def compare(brands):
    """Comparer les prix et stats entre marques."""
    db = Database(DB_PATH)

    console.print("\n[bold cyan]🔍 Analyse comparative des marques[/bold cyan]\n")

    # Récupérer tous les produits
    products = db.get_products()

    if not products:
        console.print("[yellow]⚠️  Aucun produit à analyser[/yellow]")
        return

    # Parser les marques
    brand_list = None
    if brands and brands.lower() != 'all':
        brand_list = [b.strip() for b in brands.split(',')]
    else:
        brand_list = TARGET_BRANDS

    # Analyse
    analyzer = ProductAnalyzer(products)
    report = analyzer.generate_comparison_report(brand_list)

    # Table de comparaison
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Marque", style="cyan", width=20)
    table.add_column("Produits", style="white", justify="right")
    table.add_column("Prix Moyen", style="green", justify="right")
    table.add_column("Min", style="dim", justify="right")
    table.add_column("Max", style="dim", justify="right")
    table.add_column("Position", style="magenta")
    table.add_column("Sites", style="dim", width=15)

    for item in report['ranking']:
        table.add_row(
            item['brand'].title(),
            str(item['count']),
            f"{item['avg_price']:.2f} €",
            f"{item['min_price']:.2f} €",
            f"{item['max_price']:.2f} €",
            item['positioning'].upper(),
            ', '.join(s[:3].upper() for s in item['sites'][:3])
        )

    console.print(table)
    console.print(f"\n[dim]Total: {report['total_products']} produits | {report['total_brands']} marques[/dim]\n")


@cli.command()
@click.option('--days', type=int, default=7, help='Jours de nouveautés')
@click.option('--brands', help='Filtrer par marques (séparées par virgules)')
def novelties(days, brands):
    """Afficher les nouveautés par marque."""
    db = Database(DB_PATH)

    console.print(f"\n[bold cyan]🆕 Nouveautés par marque ({days} derniers jours)[/bold cyan]\n")

    # Récupérer tous les produits
    products = db.get_products()

    if not products:
        console.print("[yellow]⚠️  Aucun produit[/yellow]")
        return

    # Parser les marques
    brand_list = None
    if brands:
        brand_list = [b.strip() for b in brands.split(',')]

    # Analyse
    analyzer = ProductAnalyzer(products)
    novelties_by_brand = analyzer.get_novelties_by_brand(days=days)

    # Filtrer par marques si demandé
    if brand_list:
        novelties_by_brand = {
            b: p for b, p in novelties_by_brand.items()
            if any(bl.lower() in b.lower() for bl in brand_list)
        }

    if not novelties_by_brand:
        console.print("[yellow]⚠️  Aucune nouveauté trouvée[/yellow]")
        return

    # Afficher par marque
    total_novelties = 0
    for brand, products_list in sorted(novelties_by_brand.items()):
        if not products_list:
            continue

        console.print(f"\n[bold magenta]• {brand.upper()}[/bold magenta] [dim]({len(products_list)} nouveautés)[/dim]")

        table = Table(show_header=True, header_style="bold cyan", show_lines=False)
        table.add_column("Produit", style="white", width=40)
        table.add_column("Prix", style="green", justify="right")
        table.add_column("Site", style="cyan", width=10)
        table.add_column("Détecté", style="dim", width=12)

        for product in products_list[:10]:  # Limiter à 10 par marque
            table.add_row(
                product['name'][:40],
                f"{product.get('current_price', 0):.2f} €" if product.get('current_price') else 'N/A',
                product['site'][:10].upper(),
                product.get('detected_at', '')[:10]
            )

        console.print(table)
        total_novelties += len(products_list)

    console.print(f"\n[dim]Total: {total_novelties} nouveautés sur {len(novelties_by_brand)} marques[/dim]\n")


@cli.command()
@click.argument('product_id', type=int)
def history(product_id):
    """Afficher l'historique des prix d'un produit."""
    db = Database(DB_PATH)

    console.print(f"\n[bold cyan]📈 Historique prix (ID: {product_id})[/bold cyan]\n")

    history = db.get_price_history(product_id)

    if not history:
        console.print("[yellow]⚠️  Aucun historique[/yellow]")
        return

    # Table
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Date", style="cyan", width=20)
    table.add_column("Prix", style="green", justify="right")
    table.add_column("Devise", style="dim")

    for record in history:
        table.add_row(
            record['timestamp'][:19],
            f"{record['price']:.2f}",
            record['currency']
        )

    console.print(table)
    console.print()


if __name__ == '__main__':
    cli()
