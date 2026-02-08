import { useState, useEffect } from 'react'
import { Tag } from 'lucide-react'
import { fetchBrands } from '../utils/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts'

const BRAND_COLORS = {
  'Dermalogica': '#1f2937',
  "Paula's Choice": '#2d8fb0',
  'Murad': '#7c3aed',
  'SkinCeuticals': '#dc2626',
}

const Brands = () => {
  const [brands, setBrands] = useState([])
  const [loading, setLoading] = useState(true)
  const [sortBy, setSortBy] = useState('product_count')

  useEffect(() => {
    loadBrands()
  }, [])

  const loadBrands = async () => {
    try {
      const data = await fetchBrands()
      setBrands(data)
    } catch (error) {
      console.error('Error loading brands:', error)
    } finally {
      setLoading(false)
    }
  }

  const sortedBrands = [...brands].sort((a, b) => {
    if (sortBy === 'product_count') return b.product_count - a.product_count
    if (sortBy === 'avg_price') return b.avg_price - a.avg_price
    if (sortBy === 'name') return a.brand.localeCompare(b.brand)
    return 0
  })

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 dark:border-white"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Marques</h1>
          <p className="text-gray-500 dark:text-gray-400 mt-1">
            Analyse comparative des marques
          </p>
        </div>
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm focus:ring-2 focus:ring-gray-900 dark:focus:ring-white dark:bg-gray-800 dark:text-white"
        >
          <option value="product_count">Par nombre de produits</option>
          <option value="avg_price">Par prix moyen</option>
          <option value="name">Par nom</option>
        </select>
      </div>

      {/* Price Comparison Chart */}
      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-base font-semibold text-gray-900 dark:text-white mb-4">
          Comparaison des Prix
        </h3>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={sortedBrands.slice(0, 10)} barGap={4}>
            <CartesianGrid strokeDasharray="3 3" className="dark:opacity-20" />
            <XAxis dataKey="brand" angle={-45} textAnchor="end" height={120} className="text-xs" tick={{ fontSize: 11 }} />
            <YAxis className="text-xs" label={{ value: '€', angle: -90, position: 'insideLeft' }} />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(0, 0, 0, 0.85)',
                border: 'none',
                borderRadius: '8px',
                color: '#fff',
                fontSize: '13px',
              }}
            />
            <Legend wrapperStyle={{ fontSize: '12px' }} />
            <Bar dataKey="avg_price" fill="#374151" name="Prix moyen" radius={[4, 4, 0, 0]} />
            <Bar dataKey="min_price" fill="#10b981" name="Prix min" radius={[4, 4, 0, 0]} />
            <Bar dataKey="max_price" fill="#ef4444" name="Prix max" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Brands Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {sortedBrands.map((brand) => {
          const isDerma = brand.brand === 'Dermalogica'
          return (
            <div
              key={brand.brand}
              className={`rounded-xl p-5 transition-all hover:shadow-md ${
                isDerma
                  ? 'bg-gray-900 dark:bg-white text-white dark:text-gray-900 ring-2 ring-gray-900 dark:ring-white'
                  : 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700'
              }`}
            >
              <div className="flex items-center mb-4">
                <div className="w-3 h-3 rounded-full mr-2" style={{ backgroundColor: BRAND_COLORS[brand.brand] || '#6b7280' }}></div>
                <h3 className={`text-base font-bold ${isDerma ? '' : 'text-gray-900 dark:text-white'}`}>
                  {brand.brand}
                </h3>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className={`text-sm ${isDerma ? 'text-gray-400 dark:text-gray-500' : 'text-gray-500 dark:text-gray-400'}`}>Produits</span>
                  <span className={`text-sm font-semibold ${isDerma ? '' : 'text-gray-900 dark:text-white'}`}>
                    {brand.product_count}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className={`text-sm ${isDerma ? 'text-gray-400 dark:text-gray-500' : 'text-gray-500 dark:text-gray-400'}`}>Prix moyen</span>
                  <span className={`text-sm font-semibold ${isDerma ? '' : 'text-gray-900 dark:text-white'}`}>
                    {brand.avg_price}€
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className={`text-sm ${isDerma ? 'text-gray-400 dark:text-gray-500' : 'text-gray-500 dark:text-gray-400'}`}>Fourchette</span>
                  <span className={`text-sm font-semibold ${isDerma ? '' : 'text-gray-900 dark:text-white'}`}>
                    {brand.min_price}€ - {brand.max_price}€
                  </span>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default Brands
