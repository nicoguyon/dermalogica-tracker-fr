import { useState, useEffect } from 'react'
import { Sparkles } from 'lucide-react'
import ProductCard from '../components/ProductCard'
import { fetchNewProducts, fetchBrands } from '../utils/api'

const NewProducts = () => {
  const [products, setProducts] = useState([])
  const [brands, setBrands] = useState([])
  const [loading, setLoading] = useState(true)
  const [days, setDays] = useState(7)
  const [selectedBrand, setSelectedBrand] = useState('')

  useEffect(() => {
    loadBrands()
  }, [])

  useEffect(() => {
    loadNewProducts()
  }, [days, selectedBrand])

  const loadBrands = async () => {
    try {
      const data = await fetchBrands()
      setBrands(data)
    } catch (error) {
      console.error('Error loading brands:', error)
    }
  }

  const loadNewProducts = async () => {
    setLoading(true)
    try {
      const data = await fetchNewProducts(days, selectedBrand || null)
      setProducts(data)
    } catch (error) {
      console.error('Error loading new products:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Nouveautés</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Derniers produits ajoutés à la base de données
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <select
          value={days}
          onChange={(e) => setDays(Number(e.target.value))}
          className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white"
        >
          <option value={7}>7 derniers jours</option>
          <option value={14}>14 derniers jours</option>
          <option value={30}>30 derniers jours</option>
          <option value={60}>60 derniers jours</option>
        </select>

        <select
          value={selectedBrand}
          onChange={(e) => setSelectedBrand(e.target.value)}
          className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white"
        >
          <option value="">Toutes les marques</option>
          {brands.map((brand) => (
            <option key={brand.brand} value={brand.brand}>
              {brand.brand}
            </option>
          ))}
        </select>
      </div>

      {/* Stats */}
      <div className="bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg shadow-md p-6 text-white">
        <div className="flex items-center">
          <Sparkles className="h-8 w-8 mr-3" />
          <div>
            <h3 className="text-2xl font-bold">{products.length} nouveaux produits</h3>
            <p className="text-green-100">
              {selectedBrand ? `De la marque ${selectedBrand}` : 'Toutes marques confondues'}
            </p>
          </div>
        </div>
      </div>

      {/* Products Grid */}
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : products.length === 0 ? (
        <div className="text-center py-12">
          <Sparkles className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500 dark:text-gray-400">Aucun nouveau produit trouvé</p>
          <p className="text-sm text-gray-400 dark:text-gray-500 mt-2">
            Essayez d'augmenter la période de recherche ou de changer de marque
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}
    </div>
  )
}

export default NewProducts
