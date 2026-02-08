import { useState, useEffect } from 'react'
import { Search, Filter } from 'lucide-react'
import ProductCard from '../components/ProductCard'
import { fetchProducts, fetchBrands, fetchSites } from '../utils/api'

const Products = () => {
  const [products, setProducts] = useState([])
  const [brands, setBrands] = useState([])
  const [sites, setSites] = useState([])
  const [loading, setLoading] = useState(true)
  const [pagination, setPagination] = useState({ page: 1, per_page: 20, total: 0, pages: 0 })

  // Filters
  const [filters, setFilters] = useState({
    brand: '',
    site: '',
    min_price: '',
    max_price: '',
    search: '',
    sort_by: 'last_updated',
    sort_order: 'DESC',
  })

  useEffect(() => {
    loadBrandsAndSites()
  }, [])

  useEffect(() => {
    loadProducts()
  }, [filters, pagination.page])

  const loadBrandsAndSites = async () => {
    try {
      const [brandsData, sitesData] = await Promise.all([fetchBrands(), fetchSites()])
      setBrands(brandsData)
      setSites(sitesData)
    } catch (error) {
      console.error('Error loading filters data:', error)
    }
  }

  const loadProducts = async () => {
    setLoading(true)
    try {
      const params = {
        page: pagination.page,
        per_page: pagination.per_page,
        ...filters,
      }
      // Remove empty filters
      Object.keys(params).forEach((key) => {
        if (params[key] === '') delete params[key]
      })

      const data = await fetchProducts(params)
      setProducts(data.products)
      setPagination(data.pagination)
    } catch (error) {
      console.error('Error loading products:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (key, value) => {
    setFilters({ ...filters, [key]: value })
    setPagination({ ...pagination, page: 1 })
  }

  const handlePageChange = (newPage) => {
    setPagination({ ...pagination, page: newPage })
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Produits</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Explorez tous les produits de votre base de données
        </p>
      </div>

      {/* Filters */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <div className="flex items-center mb-4">
          <Filter className="h-5 w-5 text-gray-600 dark:text-gray-400 mr-2" />
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Filtres</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Search */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Recherche
            </label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Nom ou marque..."
                value={filters.search}
                onChange={(e) => handleFilterChange('search', e.target.value)}
                className="pl-10 w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white"
              />
            </div>
          </div>

          {/* Brand */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Marque
            </label>
            <select
              value={filters.brand}
              onChange={(e) => handleFilterChange('brand', e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white"
            >
              <option value="">Toutes les marques</option>
              {brands.map((brand) => (
                <option key={brand.brand} value={brand.brand}>
                  {brand.brand} ({brand.product_count})
                </option>
              ))}
            </select>
          </div>

          {/* Site */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Site
            </label>
            <select
              value={filters.site}
              onChange={(e) => handleFilterChange('site', e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white"
            >
              <option value="">Tous les sites</option>
              {sites.map((site) => (
                <option key={site.site} value={site.site}>
                  {site.site} ({site.product_count})
                </option>
              ))}
            </select>
          </div>

          {/* Sort */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Trier par
            </label>
            <select
              value={filters.sort_by}
              onChange={(e) => handleFilterChange('sort_by', e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white"
            >
              <option value="last_updated">Dernière mise à jour</option>
              <option value="name">Nom</option>
              <option value="brand">Marque</option>
              <option value="current_price">Prix</option>
              <option value="first_seen">Date d'ajout</option>
            </select>
          </div>

          {/* Price Range */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Prix min
            </label>
            <input
              type="number"
              placeholder="0"
              value={filters.min_price}
              onChange={(e) => handleFilterChange('min_price', e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Prix max
            </label>
            <input
              type="number"
              placeholder="999"
              value={filters.max_price}
              onChange={(e) => handleFilterChange('max_price', e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white"
            />
          </div>
        </div>
      </div>

      {/* Results count */}
      <div className="text-sm text-gray-600 dark:text-gray-400">
        {pagination.total} produit{pagination.total > 1 ? 's' : ''} trouvé{pagination.total > 1 ? 's' : ''}
      </div>

      {/* Products Grid */}
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : products.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 dark:text-gray-400">Aucun produit trouvé</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>

          {/* Pagination */}
          {pagination.pages > 1 && (
            <div className="flex justify-center items-center space-x-2 mt-8">
              <button
                onClick={() => handlePageChange(pagination.page - 1)}
                disabled={pagination.page === 1}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 dark:hover:bg-gray-700 dark:text-white"
              >
                Précédent
              </button>

              <div className="flex space-x-1">
                {[...Array(pagination.pages)].map((_, i) => {
                  const page = i + 1
                  if (
                    page === 1 ||
                    page === pagination.pages ||
                    (page >= pagination.page - 1 && page <= pagination.page + 1)
                  ) {
                    return (
                      <button
                        key={page}
                        onClick={() => handlePageChange(page)}
                        className={`px-4 py-2 rounded-lg ${
                          page === pagination.page
                            ? 'bg-primary-600 text-white'
                            : 'border border-gray-300 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700 dark:text-white'
                        }`}
                      >
                        {page}
                      </button>
                    )
                  } else if (page === pagination.page - 2 || page === pagination.page + 2) {
                    return <span key={page} className="px-2 dark:text-white">...</span>
                  }
                  return null
                })}
              </div>

              <button
                onClick={() => handlePageChange(pagination.page + 1)}
                disabled={pagination.page === pagination.pages}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 dark:hover:bg-gray-700 dark:text-white"
              >
                Suivant
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default Products
