#!/usr/bin/env python3
"""Script de test rapide pour vérifier le scraper."""

from src.scrapers import get_scraper
from src.database import Database
from rich.console import Console

console = Console()


def test_sephora():
    """Test du scraper Sephora."""
    console.print("\n[cyan]🧪 Test Sephora[/cyan]")

    try:
        with get_scraper('sephora', headless=True) as scraper:
            products = scraper.scrape_products(limit=5)

            if products:
                console.print(f"[green]✓ {len(products)} produits scrapés[/green]")

                # Afficher le premier produit
                p = products[0]
                console.print(f"\n[bold]Premier produit :[/bold]")
                console.print(f"  Marque: {p.brand}")
                console.print(f"  Nom: {p.name[:50]}...")
                console.print(f"  Prix: {p.price}€")
                console.print(f"  URL: {p.url[:60]}...")
                console.print(f"  Nouveau: {'Oui' if p.is_new else 'Non'}")

                return True
            else:
                console.print("[red]❌ Aucun produit trouvé[/red]")
                return False

    except Exception as e:
        console.print(f"[red]❌ Erreur : {e}[/red]")
        return False


def test_nocibe():
    """Test du scraper Nocibé."""
    console.print("\n[cyan]🧪 Test Nocibé[/cyan]")

    try:
        with get_scraper('nocibe', headless=True) as scraper:
            products = scraper.scrape_products(limit=5)

            if products:
                console.print(f"[green]✓ {len(products)} produits scrapés[/green]")
                return True
            else:
                console.print("[yellow]⚠ Aucun produit trouvé[/yellow]")
                return False

    except Exception as e:
        console.print(f"[red]❌ Erreur : {e}[/red]")
        return False


def test_database():
    """Test de la base de données."""
    console.print("\n[cyan]🧪 Test Database[/cyan]")

    try:
        db = Database()

        # Stats
        stats = db.get_stats()
        console.print(f"[green]✓ Base de données OK[/green]")
        console.print(f"  Total produits: {stats['total_products']}")

        return True

    except Exception as e:
        console.print(f"[red]❌ Erreur : {e}[/red]")
        return False


if __name__ == '__main__':
    console.print("[bold]🧴 Test Cosmetique Scraper[/bold]")
    console.print("=" * 50)

    results = []

    # Tests
    results.append(("Database", test_database()))
    results.append(("Sephora", test_sephora()))
    results.append(("Nocibé", test_nocibe()))

    # Résumé
    console.print("\n" + "=" * 50)
    console.print("[bold]📊 Résumé des tests[/bold]\n")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "[green]✓[/green]" if result else "[red]❌[/red]"
        console.print(f"  {status} {name}")

    console.print(f"\n[bold]{passed}/{total} tests réussis[/bold]")

    if passed == total:
        console.print("\n[bold green]🎉 Tous les tests sont passés ![/bold green]")
    else:
        console.print("\n[bold yellow]⚠ Certains tests ont échoué[/bold yellow]")
