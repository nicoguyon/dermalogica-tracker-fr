import { useState, useEffect } from 'react'
import { Tag } from 'lucide-react'
import { fetchBrands } from '../utils/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

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
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Marques</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Analyse comparative des marques
        </p>
      </div>

      {/* Sort */}
      <div className="flex justify-end">
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white"
        >
          <option value="product_count">Trier par nombre de produits</option>
          <option value="avg_price">Trier par prix moyen</option>
          <option value="name">Trier par nom</option>
        </select>
      </div>

      {/* Price Comparison Chart */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Comparaison des Prix Moyens
        </h3>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={sortedBrands.slice(0, 10)}>
            <CartesianGrid strokeDasharray="3 3" className="dark:opacity-20" />
            <XAxis
              dataKey="brand"
              angle={-45}
              textAnchor="end"
              height={120}
              className="text-xs dark:text-gray-400"
            />
            <YAxis className="text-xs dark:text-gray-400" label={{ value: 'Prix (€)', angle: -90, position: 'insideLeft' }} />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                border: 'none',
                borderRadius: '8px',
                color: '#fff',
              }}
            />
            <Legend />
            <Bar dataKey="avg_price" fill="#0ea5e9" name="Prix moyen" radius={[8, 8, 0, 0]} />
            <Bar dataKey="min_price" fill="#10b981" name="Prix min" radius={[8, 8, 0, 0]} />
            <Bar dataKey="max_price" fill="#ef4444" name="Prix max" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Brands Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {sortedBrands.map((brand) => (
          <div
            key={brand.brand}
            className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 hover:shadow-xl transition-all"
          >
            <div className="flex items-center mb-4">
              <Tag className="h-6 w-6 text-primary-600 dark:text-primary-400 mr-2" />
              <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                {brand.brand}
              </h3>
            </div>

            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600 dark:text-gray-400">Produits</span>
                <span className="text-sm font-semibold text-gray-900 dark:text-white">
                  {brand.product_count}
                </span>
              </div>

              <div className="flex justify-between">
                <span className="text-sm text-gray-600 dark:text-gray-400">Prix moyen</span>
                <span className="text-sm font-semibold text-gray-900 dark:text-white">
                  {brand.avg_price}€
                </span>
              </div>

              <div className="flex justify-between">
                <span className="text-sm text-gray-600 dark:text-gray-400">Fourchette</span>
                <span className="text-sm font-semibold text-gray-900 dark:text-white">
                  {brand.min_price}€ - {brand.max_price}€
                </span>
              </div>

              <div>
                <span className="text-sm text-gray-600 dark:text-gray-400 block mb-2">Sites</span>
                <div className="flex flex-wrap gap-1">
                  {brand.sites.map((site) => (
                    <span
                      key={site}
                      className="px-2 py-1 text-xs font-medium bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 rounded-full"
                    >
                      {site}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Brands
