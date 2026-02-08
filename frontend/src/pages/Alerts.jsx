import { useState, useEffect } from 'react'
import { Bell, AlertTriangle, TrendingDown, ShieldAlert, Package, ArrowRight } from 'lucide-react'
import { fetchBrands, fetchProducts, fetchPromotions } from '../utils/api'

const ALERT_TYPES = {
  price_cheaper: { icon: TrendingDown, color: 'red', label: 'Concurrent moins cher' },
  category_gap: { icon: ShieldAlert, color: 'amber', label: 'Gap de gamme' },
  competitor_promo: { icon: AlertTriangle, color: 'orange', label: 'Promo concurrent' },
  new_competitor_product: { icon: Package, color: 'blue', label: 'Nouveau produit concurrent' },
}

const Alerts = () => {
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    generateAlerts()
  }, [])

  const generateAlerts = async () => {
    try {
      const [brandsData, productsData, promosData] = await Promise.all([
        fetchBrands(),
        fetchProducts({ per_page: 300 }),
        fetchPromotions(30),
      ])

      const products = productsData.products || []
      const dermaProducts = products.filter(p => p.brand === 'Dermalogica')
      const competitorProducts = products.filter(p => p.brand !== 'Dermalogica')
      const dermaBrand = brandsData.find(b => b.brand === 'Dermalogica')
      const generatedAlerts = []

      // 1. Competitors with lower average price
      brandsData.forEach(brand => {
        if (brand.brand === 'Dermalogica' || !dermaBrand) return
        if (brand.avg_price < dermaBrand.avg_price * 0.85) {
          generatedAlerts.push({
            type: 'price_cheaper',
            severity: 'high',
            title: `${brand.brand} est ${Math.round((1 - brand.avg_price / dermaBrand.avg_price) * 100)}% moins cher en moyenne`,
            description: `Prix moyen ${brand.brand}: ${brand.avg_price}€ vs Dermalogica: ${dermaBrand.avg_price}€`,
            brand: brand.brand,
            data: { dermaAvg: dermaBrand.avg_price, competitorAvg: brand.avg_price },
          })
        }
      })

      // 2. Category gaps - categories where competitors have products but Dermalogica doesn't
      const dermaCategories = new Set(dermaProducts.map(p => (p.category || '').toLowerCase()))
      const competitorCategories = {}
      competitorProducts.forEach(p => {
        const cat = (p.category || '').toLowerCase()
        if (cat && !dermaCategories.has(cat)) {
          if (!competitorCategories[cat]) competitorCategories[cat] = new Set()
          competitorCategories[cat].add(p.brand)
        }
      })

      Object.entries(competitorCategories).forEach(([category, brands]) => {
        if (brands.size >= 2) {
          generatedAlerts.push({
            type: 'category_gap',
            severity: 'medium',
            title: `Gamme absente: ${category}`,
            description: `${brands.size} concurrent(s) présent(s): ${[...brands].join(', ')}`,
            brand: [...brands][0],
            data: { category, brands: [...brands] },
          })
        }
      })

      // 3. Competitor promotions
      promosData.forEach(promo => {
        if (promo.brand !== 'Dermalogica' && promo.discount_percent) {
          const discount = Math.abs(promo.discount_percent)
          if (discount >= 15) {
            generatedAlerts.push({
              type: 'competitor_promo',
              severity: discount >= 30 ? 'high' : 'medium',
              title: `${promo.brand}: -${discount.toFixed(0)}% sur ${promo.name}`,
              description: `De ${promo.old_price}€ à ${promo.current_price}€`,
              brand: promo.brand,
              data: { product: promo.name, discount },
            })
          }
        }
      })

      // 4. Products where competitors are cheaper than Dermalogica for similar categories
      const dermaCategoryPrices = {}
      dermaProducts.forEach(p => {
        const cat = (p.category || '').toLowerCase()
        if (cat && p.current_price) {
          if (!dermaCategoryPrices[cat]) dermaCategoryPrices[cat] = []
          dermaCategoryPrices[cat].push(p.current_price)
        }
      })

      Object.entries(dermaCategoryPrices).forEach(([cat, prices]) => {
        const dermaAvg = prices.reduce((a, b) => a + b, 0) / prices.length
        competitorProducts.forEach(p => {
          if ((p.category || '').toLowerCase() === cat && p.current_price && p.current_price < dermaAvg * 0.7) {
            generatedAlerts.push({
              type: 'price_cheaper',
              severity: 'medium',
              title: `${p.brand} - "${p.name}" à ${p.current_price}€`,
              description: `${Math.round((1 - p.current_price / dermaAvg) * 100)}% moins cher que la moyenne Dermalogica (${Math.round(dermaAvg)}€) dans la catégorie "${cat}"`,
              brand: p.brand,
              data: { productPrice: p.current_price, dermaAvg },
            })
          }
        })
      })

      // Sort by severity
      const severityOrder = { high: 0, medium: 1, low: 2 }
      generatedAlerts.sort((a, b) => (severityOrder[a.severity] || 2) - (severityOrder[b.severity] || 2))

      setAlerts(generatedAlerts)
    } catch (error) {
      console.error('Error generating alerts:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredAlerts = filter === 'all'
    ? alerts
    : alerts.filter(a => a.type === filter)

  const alertCounts = {
    all: alerts.length,
    price_cheaper: alerts.filter(a => a.type === 'price_cheaper').length,
    category_gap: alerts.filter(a => a.type === 'category_gap').length,
    competitor_promo: alerts.filter(a => a.type === 'competitor_promo').length,
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 dark:border-white"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Alertes</h1>
        <p className="text-gray-500 dark:text-gray-400 mt-1">
          Signaux concurrentiels et opportunités pour Dermalogica
        </p>
      </div>

      {/* Alert Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { key: 'all', label: 'Toutes', count: alertCounts.all, icon: Bell, bg: 'bg-gray-900 dark:bg-white', text: 'text-white dark:text-gray-900' },
          { key: 'price_cheaper', label: 'Prix', count: alertCounts.price_cheaper, icon: TrendingDown, bg: 'bg-red-50 dark:bg-red-900/20', text: 'text-red-700 dark:text-red-400' },
          { key: 'category_gap', label: 'Gaps', count: alertCounts.category_gap, icon: ShieldAlert, bg: 'bg-amber-50 dark:bg-amber-900/20', text: 'text-amber-700 dark:text-amber-400' },
          { key: 'competitor_promo', label: 'Promos', count: alertCounts.competitor_promo, icon: AlertTriangle, bg: 'bg-orange-50 dark:bg-orange-900/20', text: 'text-orange-700 dark:text-orange-400' },
        ].map(item => {
          const Icon = item.icon
          const isActive = filter === item.key
          return (
            <button
              key={item.key}
              onClick={() => setFilter(item.key)}
              className={`p-4 rounded-xl text-left transition-all ${
                isActive
                  ? `${item.bg} ${item.text} ring-2 ring-gray-900 dark:ring-white`
                  : 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400 hover:border-gray-400 dark:hover:border-gray-500'
              }`}
            >
              <div className="flex items-center justify-between">
                <Icon className="h-5 w-5" />
                <span className={`text-2xl font-bold ${isActive ? '' : 'text-gray-900 dark:text-white'}`}>{item.count}</span>
              </div>
              <p className="text-sm font-medium mt-2">{item.label}</p>
            </button>
          )
        })}
      </div>

      {/* Alerts List */}
      <div className="space-y-3">
        {filteredAlerts.length === 0 ? (
          <div className="text-center py-16 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
            <Bell className="h-12 w-12 text-gray-300 dark:text-gray-600 mx-auto mb-3" />
            <p className="text-gray-500 dark:text-gray-400">Aucune alerte dans cette catégorie</p>
          </div>
        ) : (
          filteredAlerts.map((alert, i) => {
            const config = ALERT_TYPES[alert.type] || ALERT_TYPES.price_cheaper
            const Icon = config.icon
            const severityColors = {
              high: 'border-l-red-500',
              medium: 'border-l-amber-500',
              low: 'border-l-blue-500',
            }

            return (
              <div
                key={i}
                className={`bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 border-l-4 ${severityColors[alert.severity]} p-5 transition-all hover:shadow-md`}
              >
                <div className="flex items-start gap-4">
                  <div className={`p-2 rounded-lg flex-shrink-0 ${
                    alert.severity === 'high' ? 'bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400' :
                    alert.severity === 'medium' ? 'bg-amber-50 dark:bg-amber-900/20 text-amber-600 dark:text-amber-400' :
                    'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400'
                  }`}>
                    <Icon className="h-5 w-5" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`text-xs font-medium uppercase tracking-wider ${
                        alert.severity === 'high' ? 'text-red-600 dark:text-red-400' :
                        alert.severity === 'medium' ? 'text-amber-600 dark:text-amber-400' :
                        'text-blue-600 dark:text-blue-400'
                      }`}>
                        {config.label}
                      </span>
                      <span className="text-xs text-gray-400">|</span>
                      <span className="text-xs text-gray-500 dark:text-gray-400">{alert.brand}</span>
                    </div>
                    <h4 className="text-sm font-semibold text-gray-900 dark:text-white">
                      {alert.title}
                    </h4>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                      {alert.description}
                    </p>
                  </div>
                  <div className={`px-2 py-1 rounded text-xs font-medium flex-shrink-0 ${
                    alert.severity === 'high' ? 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400' :
                    alert.severity === 'medium' ? 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400' :
                    'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400'
                  }`}>
                    {alert.severity === 'high' ? 'Critique' : alert.severity === 'medium' ? 'Important' : 'Info'}
                  </div>
                </div>
              </div>
            )
          })
        )}
      </div>
    </div>
  )
}

export default Alerts
