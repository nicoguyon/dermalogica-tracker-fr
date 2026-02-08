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
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Promotions</h1>
          <p className="text-gray-500 dark:text-gray-400 mt-1">
            Produits avec baisse de prix récente
          </p>
        </div>
        <select
          value={days}
          onChange={(e) => setDays(Number(e.target.value))}
          className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm focus:ring-2 focus:ring-gray-900 dark:focus:ring-white dark:bg-gray-800 dark:text-white"
        >
          <option value={7}>7 derniers jours</option>
          <option value={14}>14 derniers jours</option>
          <option value={30}>30 derniers jours</option>
        </select>
      </div>

      {/* Stats banner */}
      <div className="bg-gray-900 dark:bg-white rounded-xl p-6">
        <div className="flex items-center">
          <TrendingDown className="h-8 w-8 mr-3 text-white dark:text-gray-900" />
          <div>
            <h3 className="text-2xl font-bold text-white dark:text-gray-900">{promotions.length} promotions actives</h3>
            <p className="text-gray-400 dark:text-gray-500 text-sm">
              {promotions.length > 0 ? `Jusqu'à ${Math.abs(Math.min(...promotions.map(p => p.discount_percent)))}% de réduction` : 'Aucune promotion en cours'}
            </p>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 dark:border-white"></div>
        </div>
      ) : promotions.length === 0 ? (
        <div className="text-center py-16 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
          <TrendingDown className="h-12 w-12 text-gray-300 dark:text-gray-600 mx-auto mb-3" />
          <p className="text-gray-500 dark:text-gray-400">Aucune promotion trouvée</p>
          <p className="text-sm text-gray-400 mt-1">Essayez d'augmenter la période</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {promotions.map((product) => (
            <ProductCard key={product.id} product={product} showDiscount={true} />
          ))}
        </div>
      )}
    </div>
  )
}

export default Promotions
