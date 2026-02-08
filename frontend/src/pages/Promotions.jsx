import { useState, useEffect } from 'react'
import { TrendingDown } from 'lucide-react'
import ProductCard from '../components/ProductCard'
import { fetchPromotions } from '../utils/api'

const Promotions = () => {
  const [promotions, setPromotions] = useState([])
  const [loading, setLoading] = useState(true)
  const [days, setDays] = useState(7)

  useEffect(() => {
    loadPromotions()
  }, [days])

  const loadPromotions = async () => {
    setLoading(true)
    try {
      const data = await fetchPromotions(days)
      setPromotions(data)
    } catch (error) {
      console.error('Error loading promotions:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Promotions</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Produits avec baisse de prix récente
          </p>
        </div>
        <select
          value={days}
          onChange={(e) => setDays(Number(e.target.value))}
          className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white"
        >
          <option value={7}>7 derniers jours</option>
          <option value={14}>14 derniers jours</option>
          <option value={30}>30 derniers jours</option>
        </select>
      </div>

      {/* Stats */}
      <div className="bg-gradient-to-r from-red-500 to-pink-500 rounded-lg shadow-md p-6 text-white">
        <div className="flex items-center mb-2">
          <TrendingDown className="h-8 w-8 mr-3" />
          <div>
            <h3 className="text-2xl font-bold">{promotions.length} promotions actives</h3>
            <p className="text-red-100">Économisez jusqu'à {promotions.length > 0 ? Math.abs(Math.min(...promotions.map(p => p.discount_percent))) : 0}%</p>
          </div>
        </div>
      </div>

      {/* Promotions Grid */}
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : promotions.length === 0 ? (
        <div className="text-center py-12">
          <TrendingDown className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500 dark:text-gray-400">Aucune promotion trouvée</p>
          <p className="text-sm text-gray-400 dark:text-gray-500 mt-2">
            Essayez d'augmenter la période de recherche
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {promotions.map((product) => (
            <ProductCard key={product.id} product={product} showDiscount={true} />
          ))}
        </div>
      )}
    </div>
  )
}

export default Promotions
