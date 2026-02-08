"""Flask API for Dermalogica Competitive Tracker."""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import os
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import DB_PATH

# Serve frontend static files in production
FRONTEND_DIR = Path(__file__).parent.parent / 'frontend' / 'dist'

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path='')
CORS(app)


@app.route('/')
def serve_frontend():
    """Serve the React SPA."""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files, fallback to index.html for SPA routing."""
    file_path = Path(app.static_folder) / path
    if file_path.exists():
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')


def get_db_connection():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def dict_from_row(row):
    """Convert sqlite3.Row to dict."""
    return dict(zip(row.keys(), row))


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get global statistics."""
    conn = get_db_connection()

    # Total products
    total = conn.execute('SELECT COUNT(*) as count FROM products').fetchone()['count']

    # Total brands
    brands = conn.execute('SELECT COUNT(DISTINCT brand) as count FROM products WHERE brand IS NOT NULL').fetchone()['count']

    # Total sites
    sites = conn.execute('SELECT COUNT(DISTINCT site) as count FROM products').fetchone()['count']

    # New products (last 7 days)
    week_ago = (datetime.now() - timedelta(days=7)).isoformat()
    new_products = conn.execute(
        'SELECT COUNT(*) as count FROM products WHERE first_seen >= ?',
        (week_ago,)
    ).fetchone()['count']

    # Average price
    avg_price = conn.execute('''
        SELECT AVG(p.price) as avg_price
        FROM prices p
        INNER JOIN (
            SELECT product_id, MAX(timestamp) as max_ts
            FROM prices
            GROUP BY product_id
        ) latest ON p.product_id = latest.product_id AND p.timestamp = latest.max_ts
    ''').fetchone()['avg_price']

    # Price range
    price_range = conn.execute('''
        SELECT MIN(p.price) as min_price, MAX(p.price) as max_price
        FROM prices p
        INNER JOIN (
            SELECT product_id, MAX(timestamp) as max_ts
            FROM prices
            GROUP BY product_id
        ) latest ON p.product_id = latest.product_id AND p.timestamp = latest.max_ts
    ''').fetchone()

    # Products with promotions (price decreased)
    promotions = conn.execute('''
        SELECT COUNT(DISTINCT p1.product_id) as count
        FROM prices p1
        INNER JOIN (
            SELECT product_id, MAX(timestamp) as max_ts
            FROM prices
            GROUP BY product_id
        ) latest ON p1.product_id = latest.product_id AND p1.timestamp = latest.max_ts
        INNER JOIN (
            SELECT product_id, price as old_price
            FROM prices p2
            WHERE timestamp < datetime('now', '-7 days')
            GROUP BY product_id
            HAVING timestamp = MAX(timestamp)
        ) old ON p1.product_id = old.product_id
        WHERE p1.price < old.old_price
    ''').fetchone()['count']

    conn.close()

    return jsonify({
        'total_products': total,
        'total_brands': brands,
        'total_sites': sites,
        'new_products_week': new_products,
        'average_price': round(avg_price, 2) if avg_price else 0,
        'min_price': round(price_range['min_price'], 2) if price_range['min_price'] else 0,
        'max_price': round(price_range['max_price'], 2) if price_range['max_price'] else 0,
        'active_promotions': promotions
    })


@app.route('/api/brands', methods=['GET'])
def get_brands():
    """Get brand statistics."""
    conn = get_db_connection()

    query = '''
        SELECT
            pr.brand,
            COUNT(DISTINCT pr.id) as product_count,
            AVG(p.price) as avg_price,
            MIN(p.price) as min_price,
            MAX(p.price) as max_price,
            GROUP_CONCAT(DISTINCT pr.site) as sites
        FROM products pr
        LEFT JOIN (
            SELECT p1.product_id, p1.price
            FROM prices p1
            INNER JOIN (
                SELECT product_id, MAX(timestamp) as max_ts
                FROM prices
                GROUP BY product_id
            ) latest ON p1.product_id = latest.product_id AND p1.timestamp = latest.max_ts
        ) p ON pr.id = p.product_id
        WHERE pr.brand IS NOT NULL
        GROUP BY pr.brand
        ORDER BY product_count DESC
    '''

    brands = conn.execute(query).fetchall()
    conn.close()

    result = []
    for brand in brands:
        result.append({
            'brand': brand['brand'],
            'product_count': brand['product_count'],
            'avg_price': round(brand['avg_price'], 2) if brand['avg_price'] else 0,
            'min_price': round(brand['min_price'], 2) if brand['min_price'] else 0,
            'max_price': round(brand['max_price'], 2) if brand['max_price'] else 0,
            'sites': brand['sites'].split(',') if brand['sites'] else []
        })

    return jsonify(result)


@app.route('/api/products', methods=['GET'])
def get_products():
    """Get products with filters and pagination."""
    # Query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    brand = request.args.get('brand', None)
    site = request.args.get('site', None)
    min_price = request.args.get('min_price', None, type=float)
    max_price = request.args.get('max_price', None, type=float)
    search = request.args.get('search', None)
    sort_by = request.args.get('sort_by', 'last_updated')
    sort_order = request.args.get('sort_order', 'DESC')

    conn = get_db_connection()

    # Build query
    query = '''
        SELECT
            pr.id,
            pr.site,
            pr.product_id,
            pr.name,
            pr.brand,
            pr.category,
            pr.url,
            pr.image_url,
            pr.first_seen,
            pr.last_updated,
            p.price as current_price,
            p.currency
        FROM products pr
        LEFT JOIN (
            SELECT p1.product_id, p1.price, p1.currency
            FROM prices p1
            INNER JOIN (
                SELECT product_id, MAX(timestamp) as max_ts
                FROM prices
                GROUP BY product_id
            ) latest ON p1.product_id = latest.product_id AND p1.timestamp = latest.max_ts
        ) p ON pr.id = p.product_id
        WHERE 1=1
    '''

    params = []

    if brand:
        query += ' AND LOWER(pr.brand) = LOWER(?)'
        params.append(brand)

    if site:
        query += ' AND LOWER(pr.site) = LOWER(?)'
        params.append(site)

    if min_price is not None:
        query += ' AND p.price >= ?'
        params.append(min_price)

    if max_price is not None:
        query += ' AND p.price <= ?'
        params.append(max_price)

    if search:
        query += ' AND (LOWER(pr.name) LIKE LOWER(?) OR LOWER(pr.brand) LIKE LOWER(?))'
        search_term = f'%{search}%'
        params.extend([search_term, search_term])

    # Add sorting
    valid_sort_fields = ['name', 'brand', 'current_price', 'last_updated', 'first_seen']
    if sort_by in valid_sort_fields:
        query += f' ORDER BY {sort_by} {sort_order}'

    # Count total
    count_query = f'SELECT COUNT(*) as total FROM ({query})'
    total = conn.execute(count_query, params).fetchone()['total']

    # Add pagination
    offset = (page - 1) * per_page
    query += f' LIMIT ? OFFSET ?'
    params.extend([per_page, offset])

    products = conn.execute(query, params).fetchall()
    conn.close()

    result = [dict_from_row(row) for row in products]

    return jsonify({
        'products': result,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        }
    })


@app.route('/api/new-products', methods=['GET'])
def get_new_products():
    """Get new products."""
    days = request.args.get('days', 7, type=int)
    brand = request.args.get('brand', None)

    conn = get_db_connection()

    since = (datetime.now() - timedelta(days=days)).isoformat()

    query = '''
        SELECT
            pr.id,
            pr.site,
            pr.name,
            pr.brand,
            pr.category,
            pr.url,
            pr.image_url,
            pr.first_seen,
            p.price as current_price,
            p.currency
        FROM products pr
        LEFT JOIN (
            SELECT p1.product_id, p1.price, p1.currency
            FROM prices p1
            INNER JOIN (
                SELECT product_id, MAX(timestamp) as max_ts
                FROM prices
                GROUP BY product_id
            ) latest ON p1.product_id = latest.product_id AND p1.timestamp = latest.max_ts
        ) p ON pr.id = p.product_id
        WHERE pr.first_seen >= ?
    '''

    params = [since]

    if brand:
        query += ' AND LOWER(pr.brand) = LOWER(?)'
        params.append(brand)

    query += ' ORDER BY pr.first_seen DESC'

    products = conn.execute(query, params).fetchall()
    conn.close()

    return jsonify([dict_from_row(row) for row in products])


@app.route('/api/promotions', methods=['GET'])
def get_promotions():
    """Get products with price decreases (promotions)."""
    days = request.args.get('days', 7, type=int)

    conn = get_db_connection()

    query = '''
        SELECT
            pr.id,
            pr.site,
            pr.name,
            pr.brand,
            pr.category,
            pr.url,
            pr.image_url,
            p1.price as current_price,
            old.old_price,
            ROUND(((p1.price - old.old_price) / old.old_price) * 100, 2) as discount_percent,
            p1.currency
        FROM products pr
        INNER JOIN (
            SELECT px.product_id, px.price, px.currency
            FROM prices px
            INNER JOIN (
                SELECT product_id, MAX(timestamp) as max_ts
                FROM prices
                GROUP BY product_id
            ) latest ON px.product_id = latest.product_id AND px.timestamp = latest.max_ts
        ) p1 ON pr.id = p1.product_id
        INNER JOIN (
            SELECT product_id, price as old_price
            FROM prices p2
            WHERE timestamp < datetime('now', '-' || ? || ' days')
            GROUP BY product_id
            HAVING timestamp = MAX(timestamp)
        ) old ON p1.product_id = old.product_id
        WHERE p1.price < old.old_price
        ORDER BY discount_percent ASC
    '''

    promotions = conn.execute(query, (days,)).fetchall()
    conn.close()

    return jsonify([dict_from_row(row) for row in promotions])


@app.route('/api/price-history/<int:product_id>', methods=['GET'])
def get_price_history(product_id):
    """Get price history for a product."""
    conn = get_db_connection()

    # Get product info
    product = conn.execute(
        'SELECT * FROM products WHERE id = ?',
        (product_id,)
    ).fetchone()

    if not product:
        conn.close()
        return jsonify({'error': 'Product not found'}), 404

    # Get price history
    history = conn.execute(
        '''SELECT price, currency, timestamp
           FROM prices
           WHERE product_id = ?
           ORDER BY timestamp ASC''',
        (product_id,)
    ).fetchall()

    conn.close()

    return jsonify({
        'product': dict_from_row(product),
        'history': [dict_from_row(row) for row in history]
    })


@app.route('/api/sites', methods=['GET'])
def get_sites():
    """Get list of sites with product counts."""
    conn = get_db_connection()

    query = '''
        SELECT
            site,
            COUNT(*) as product_count,
            COUNT(DISTINCT brand) as brand_count
        FROM products
        GROUP BY site
        ORDER BY product_count DESC
    '''

    sites = conn.execute(query).fetchall()
    conn.close()

    return jsonify([dict_from_row(row) for row in sites])


@app.route('/api/search', methods=['GET'])
def search():
    """Search products by name or brand."""
    query = request.args.get('q', '')
    limit = request.args.get('limit', 10, type=int)

    if not query:
        return jsonify([])

    conn = get_db_connection()

    sql = '''
        SELECT
            pr.id,
            pr.name,
            pr.brand,
            pr.site,
            pr.image_url,
            p.price as current_price
        FROM products pr
        LEFT JOIN (
            SELECT p1.product_id, p1.price
            FROM prices p1
            INNER JOIN (
                SELECT product_id, MAX(timestamp) as max_ts
                FROM prices
                GROUP BY product_id
            ) latest ON p1.product_id = latest.product_id AND p1.timestamp = latest.max_ts
        ) p ON pr.id = p.product_id
        WHERE LOWER(pr.name) LIKE LOWER(?) OR LOWER(pr.brand) LIKE LOWER(?)
        LIMIT ?
    '''

    search_term = f'%{query}%'
    results = conn.execute(sql, (search_term, search_term, limit)).fetchall()
    conn.close()

    return jsonify([dict_from_row(row) for row in results])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
