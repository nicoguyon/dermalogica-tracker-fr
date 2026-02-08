import { useState, useEffect } from 'react'
import { Package, Tag, TrendingUp, Sparkles, DollarSign, ShoppingBag, Globe, TrendingDown } from 'lucide-react'
import StatCard from '../components/StatCard'
import { fetchStats, fetchBrands, fetchSites } from '../utils/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const Dashboard = () => {
  const [stats, setStats] = useState(null)
  const [brands, setBrands] = useState([])
  const [sites, setSites] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [statsData, brandsData, sitesData] = await Promise.all([
        fetchStats(),
        fetchBrands(),
        fetchSites(),
      ])
      setStats(statsData)
      setBrands(brandsData)
      setSites(sitesData)
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const COLORS = ['#0ea5e9', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#ef4444']

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Vue d'ensemble de votre tracker de produits cosmétiques
        </p>
      </div>

      {/* Stats Grid */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard
            title="Total Produits"
            value={stats.total_products}
            icon={Package}
            color="primary"
          />
          <StatCard
            title="Marques"
            value={stats.total_brands}
            icon={Tag}
            color="purple"
          />
          <StatCard
            title="Nouveautés (7j)"
            value={stats.new_products_week}
            icon={Sparkles}
            color="green"
          />
          <StatCard
            title="Promotions actives"
            value={stats.active_promotions}
            icon={TrendingDown}
            color="orange"
          />
        </div>
      )}

      {/* Price Stats */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Prix Moyen</h3>
              <DollarSign className="h-5 w-5 text-primary-600 dark:text-primary-400" />
            </div>
            <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.average_price}€</p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Prix Min</h3>
              <TrendingDown className="h-5 w-5 text-green-600 dark:text-green-400" />
            </div>
            <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.min_price}€</p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Prix Max</h3>
              <TrendingUp className="h-5 w-5 text-red-600 dark:text-red-400" />
            </div>
            <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.max_price}€</p>
          </div>
        </div>
      )}

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Brands Chart */}
        {brands.length > 0 && (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Produits par Marque
            </h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={brands.slice(0, 8)}>
                <CartesianGrid strokeDasharray="3 3" className="dark:opacity-20" />
                <XAxis
                  dataKey="brand"
                  angle={-45}
                  textAnchor="end"
                  height={100}
                  className="text-xs dark:text-gray-400"
                />
                <YAxis className="text-xs dark:text-gray-400" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    border: 'none',
                    borderRadius: '8px',
                    color: '#fff',
                  }}
                />
                <Bar dataKey="product_count" fill="#0ea5e9" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Sites Chart */}
        {sites.length > 0 && (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Répartition par Site
            </h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={sites}
                  dataKey="product_count"
                  nameKey="site"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label={(entry) => entry.site}
                >
                  {sites.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    border: 'none',
                    borderRadius: '8px',
                    color: '#fff',
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Top Brands Table */}
      {brands.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Top Marques
          </h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead>
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Marque
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Produits
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Prix Moyen
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Fourchette
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Sites
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                {brands.slice(0, 10).map((brand) => (
                  <tr key={brand.brand} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm font-medium text-gray-900 dark:text-white">
                        {brand.brand}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-700 dark:text-gray-300">
                        {brand.product_count}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm font-semibold text-gray-900 dark:text-white">
                        {brand.avg_price}€
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-700 dark:text-gray-300">
                        {brand.min_price}€ - {brand.max_price}€
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
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
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}

export default Dashboard
