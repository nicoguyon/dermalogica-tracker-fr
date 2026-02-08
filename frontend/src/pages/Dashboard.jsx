import { useState, useEffect } from 'react'
import { Package, Tag, TrendingDown, Sparkles, DollarSign, TrendingUp, ArrowRight } from 'lucide-react'
import { Link } from 'react-router-dom'
import StatCard from '../components/StatCard'
import { fetchStats, fetchBrands, fetchSites } from '../utils/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const BRAND_COLORS = {
  'Dermalogica': '#1f2937',
  "Paula's Choice": '#2d8fb0',
  'Murad': '#7c3aed',
  'SkinCeuticals': '#dc2626',
}

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
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 dark:border-white"></div>
      </div>
    )
  }

  const COLORS = Object.values(BRAND_COLORS)

  const mainBrands = brands.filter(b =>
    ['Dermalogica', "Paula's Choice", 'Murad', 'SkinCeuticals'].includes(b.brand)
  )

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
          <p className="text-gray-500 dark:text-gray-400 mt-1">
            Intelligence concurrentielle Dermalogica
          </p>
        </div>
        <Link
          to="/compare"
          className="hidden sm:inline-flex items-center px-4 py-2 bg-gray-900 dark:bg-white text-white dark:text-gray-900 rounded-lg text-sm font-medium hover:bg-gray-800 dark:hover:bg-gray-100 transition-colors"
        >
          Analyse comparative
          <ArrowRight className="h-4 w-4 ml-2" />
        </Link>
      </div>

      {/* Stats Grid */}
      {stats && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard
            title="Total Produits"
            value={stats.total_products}
            icon={Package}
            color="dark"
          />
          <StatCard
            title="Marques suivies"
            value={stats.total_brands}
            icon={Tag}
            color="accent"
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

      {/* Price Overview */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Prix Moyen</h3>
              <DollarSign className="h-4 w-4 text-gray-400" />
            </div>
            <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.average_price}€</p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Prix Min</h3>
              <TrendingDown className="h-4 w-4 text-green-500" />
            </div>
            <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.min_price}€</p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Prix Max</h3>
              <TrendingUp className="h-4 w-4 text-red-500" />
            </div>
            <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.max_price}€</p>
          </div>
        </div>
      )}

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Brands Chart */}
        {mainBrands.length > 0 && (
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
            <h3 className="text-base font-semibold text-gray-900 dark:text-white mb-4">
              Produits par Marque
            </h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={mainBrands}>
                <CartesianGrid strokeDasharray="3 3" className="dark:opacity-20" />
                <XAxis dataKey="brand" className="text-xs" tick={{ fontSize: 11 }} />
                <YAxis className="text-xs" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(0, 0, 0, 0.85)',
                    border: 'none',
                    borderRadius: '8px',
                    color: '#fff',
                    fontSize: '13px',
                  }}
                />
                <Bar dataKey="product_count" radius={[6, 6, 0, 0]}>
                  {mainBrands.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={BRAND_COLORS[entry.brand] || '#6b7280'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Sites Chart */}
        {sites.length > 0 && (
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
            <h3 className="text-base font-semibold text-gray-900 dark:text-white mb-4">
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
                  strokeWidth={2}
                >
                  {sites.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(0, 0, 0, 0.85)',
                    border: 'none',
                    borderRadius: '8px',
                    color: '#fff',
                    fontSize: '13px',
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Top Brands Table */}
      {mainBrands.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-base font-semibold text-gray-900 dark:text-white">
              Vue d'ensemble des Marques
            </h3>
            <Link to="/compare" className="text-sm text-gray-500 hover:text-gray-900 dark:hover:text-white transition-colors flex items-center">
              Analyse complète <ArrowRight className="h-3 w-3 ml-1" />
            </Link>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead>
                <tr className="border-b border-gray-200 dark:border-gray-700">
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Marque</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Produits</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Prix Moyen</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Fourchette</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                {mainBrands.map((brand) => (
                  <tr key={brand.brand} className={`hover:bg-gray-50 dark:hover:bg-gray-700/50 ${brand.brand === 'Dermalogica' ? 'bg-gray-50 dark:bg-gray-700/30' : ''}`}>
                    <td className="px-4 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full" style={{ backgroundColor: BRAND_COLORS[brand.brand] }}></div>
                        <span className={`text-sm font-medium ${brand.brand === 'Dermalogica' ? 'text-gray-900 dark:text-white font-semibold' : 'text-gray-700 dark:text-gray-300'}`}>
                          {brand.brand}
                        </span>
                      </div>
                    </td>
                    <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-700 dark:text-gray-300">
                      {brand.product_count}
                    </td>
                    <td className="px-4 py-4 whitespace-nowrap text-sm font-semibold text-gray-900 dark:text-white">
                      {brand.avg_price}€
                    </td>
                    <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      {brand.min_price}€ - {brand.max_price}€
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
