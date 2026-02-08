import { useState, useEffect } from 'react'
import { GitCompare, ArrowUpRight, ArrowDownRight, Minus } from 'lucide-react'
import { fetchBrands, fetchProducts } from '../utils/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts'

const BRAND_COLORS = {
  'Dermalogica': '#1f2937',
  "Paula's Choice": '#2d8fb0',
  'Murad': '#7c3aed',
  'SkinCeuticals': '#dc2626',
}

const CATEGORIES_MAP = {
  'Sérums': ['Sérums', 'Serums', 'Vitamin C Serums', 'Anti-Aging Serums', 'Hydrating Serums', 'Acne Serums', 'Brightening', 'Boosters'],
  'Hydratants': ['Hydratants', 'Hydratants & SPF', 'Moisturizers', 'Anti-Aging Creams'],
  'Nettoyants': ['Nettoyants', 'Démaquillants & Nettoyants', 'Cleansers'],
  'Exfoliants': ['Exfoliants', 'Exfoliators'],
  'SPF / Solaire': ['Protection solaire', 'Suncare', 'Sunscreens', 'Hydratants & SPF'],
  'Yeux': ['Contour des yeux', 'Eye Care'],
  'Traitements': ['Traitements', 'Treatments', 'Retinol', 'Sensitive Skin'],
}

const Compare = () => {
  const [brands, setBrands] = useState([])
  const [allProducts, setAllProducts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [brandsData, productsData] = await Promise.all([
        fetchBrands(),
        fetchProducts({ per_page: 300 }),
      ])
      setBrands(brandsData)
      setAllProducts(productsData.products || [])
    } catch (error) {
      console.error('Error loading comparison data:', error)
    } finally {
      setLoading(false)
    }
  }

  const mainBrands = brands.filter(b =>
    ['Dermalogica', "Paula's Choice", 'Murad', 'SkinCeuticals'].includes(b.brand)
  )

  // Price comparison data
  const priceData = mainBrands.map(b => ({
    brand: b.brand,
    'Prix moyen': b.avg_price,
    'Prix min': b.min_price,
    'Prix max': b.max_price,
  }))

  // Category coverage
  const getCategoryCount = (brand, categories) => {
    return allProducts.filter(p =>
      p.brand === brand && categories.some(cat =>
        (p.category || '').toLowerCase().includes(cat.toLowerCase())
      )
    ).length
  }

  const radarData = Object.entries(CATEGORIES_MAP).map(([label, categories]) => {
    const entry = { category: label }
    mainBrands.forEach(b => {
      entry[b.brand] = getCategoryCount(b.brand, categories)
    })
    return entry
  })

  // Dermalogica positioning
  const derma = mainBrands.find(b => b.brand === 'Dermalogica')
  const competitors = mainBrands.filter(b => b.brand !== 'Dermalogica')

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 dark:border-white"></div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Analyse Comparative</h1>
        <p className="text-gray-500 dark:text-gray-400 mt-1">
          Positionnement de Dermalogica face à ses concurrents
        </p>
      </div>

      {/* Brand Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {mainBrands.map(brand => {
          const isDerma = brand.brand === 'Dermalogica'
          return (
            <div key={brand.brand} className={`rounded-xl p-5 transition-all ${
              isDerma
                ? 'bg-gray-900 dark:bg-white text-white dark:text-gray-900 ring-2 ring-gray-900 dark:ring-white'
                : 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700'
            }`}>
              <div className="flex items-center justify-between mb-3">
                <h3 className={`text-sm font-semibold uppercase tracking-wider ${isDerma ? 'text-gray-300 dark:text-gray-600' : 'text-gray-500 dark:text-gray-400'}`}>
                  {brand.brand}
                </h3>
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: BRAND_COLORS[brand.brand] }}></div>
              </div>
              <p className={`text-3xl font-bold ${isDerma ? '' : 'text-gray-900 dark:text-white'}`}>
                {brand.product_count}
              </p>
              <p className={`text-sm ${isDerma ? 'text-gray-400 dark:text-gray-500' : 'text-gray-500 dark:text-gray-400'}`}>
                produits suivis
              </p>
              <div className={`mt-3 pt-3 border-t ${isDerma ? 'border-gray-700 dark:border-gray-300' : 'border-gray-100 dark:border-gray-700'}`}>
                <div className="flex justify-between text-sm">
                  <span className={isDerma ? 'text-gray-400 dark:text-gray-500' : 'text-gray-500 dark:text-gray-400'}>Prix moyen</span>
                  <span className={`font-semibold ${isDerma ? '' : 'text-gray-900 dark:text-white'}`}>{brand.avg_price}€</span>
                </div>
                <div className="flex justify-between text-sm mt-1">
                  <span className={isDerma ? 'text-gray-400 dark:text-gray-500' : 'text-gray-500 dark:text-gray-400'}>Fourchette</span>
                  <span className={`font-semibold ${isDerma ? '' : 'text-gray-900 dark:text-white'}`}>{brand.min_price}€ - {brand.max_price}€</span>
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Price Comparison */}
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Comparaison des Prix
          </h3>
          <ResponsiveContainer width="100%" height={350}>
            <BarChart data={priceData} barGap={4}>
              <CartesianGrid strokeDasharray="3 3" className="dark:opacity-20" />
              <XAxis dataKey="brand" className="text-xs" tick={{ fontSize: 11 }} />
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
              <Bar dataKey="Prix moyen" fill="#374151" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Prix min" fill="#10b981" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Prix max" fill="#ef4444" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Category Coverage Radar */}
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Couverture par Catégorie
          </h3>
          <ResponsiveContainer width="100%" height={350}>
            <RadarChart data={radarData}>
              <PolarGrid strokeDasharray="3 3" />
              <PolarAngleAxis dataKey="category" tick={{ fontSize: 11 }} />
              <PolarRadiusAxis tick={{ fontSize: 10 }} />
              {mainBrands.map(b => (
                <Radar
                  key={b.brand}
                  name={b.brand}
                  dataKey={b.brand}
                  stroke={BRAND_COLORS[b.brand]}
                  fill={BRAND_COLORS[b.brand]}
                  fillOpacity={b.brand === 'Dermalogica' ? 0.3 : 0.1}
                  strokeWidth={b.brand === 'Dermalogica' ? 2 : 1}
                />
              ))}
              <Legend wrapperStyle={{ fontSize: '12px' }} />
              <Tooltip />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Competitive Positioning Table */}
      {derma && (
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Positionnement vs Concurrents
          </h3>
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead>
                <tr className="border-b border-gray-200 dark:border-gray-700">
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Indicateur</th>
                  <th className="px-4 py-3 text-center text-xs font-semibold uppercase tracking-wider bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-white">Dermalogica</th>
                  {competitors.map(c => (
                    <th key={c.brand} className="px-4 py-3 text-center text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">{c.brand}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                <tr>
                  <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">Nombre de produits</td>
                  <td className="px-4 py-3 text-center font-semibold text-gray-900 dark:text-white bg-gray-50 dark:bg-gray-700/50">{derma.product_count}</td>
                  {competitors.map(c => (
                    <td key={c.brand} className="px-4 py-3 text-center text-sm text-gray-700 dark:text-gray-300">{c.product_count}</td>
                  ))}
                </tr>
                <tr>
                  <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">Prix moyen</td>
                  <td className="px-4 py-3 text-center font-semibold text-gray-900 dark:text-white bg-gray-50 dark:bg-gray-700/50">{derma.avg_price}€</td>
                  {competitors.map(c => {
                    const diff = c.avg_price - derma.avg_price
                    return (
                      <td key={c.brand} className="px-4 py-3 text-center text-sm">
                        <span className="text-gray-700 dark:text-gray-300">{c.avg_price}€</span>
                        <span className={`ml-2 text-xs font-medium ${diff > 0 ? 'text-green-600' : diff < 0 ? 'text-red-600' : 'text-gray-500'}`}>
                          {diff > 0 ? '+' : ''}{diff.toFixed(0)}€
                        </span>
                      </td>
                    )
                  })}
                </tr>
                <tr>
                  <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">Prix minimum</td>
                  <td className="px-4 py-3 text-center font-semibold text-gray-900 dark:text-white bg-gray-50 dark:bg-gray-700/50">{derma.min_price}€</td>
                  {competitors.map(c => (
                    <td key={c.brand} className="px-4 py-3 text-center text-sm text-gray-700 dark:text-gray-300">{c.min_price}€</td>
                  ))}
                </tr>
                <tr>
                  <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">Prix maximum</td>
                  <td className="px-4 py-3 text-center font-semibold text-gray-900 dark:text-white bg-gray-50 dark:bg-gray-700/50">{derma.max_price}€</td>
                  {competitors.map(c => (
                    <td key={c.brand} className="px-4 py-3 text-center text-sm text-gray-700 dark:text-gray-300">{c.max_price}€</td>
                  ))}
                </tr>
                <tr>
                  <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">Positionnement prix</td>
                  <td className="px-4 py-3 text-center bg-gray-50 dark:bg-gray-700/50">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-900 dark:bg-white text-white dark:text-gray-900">
                      Référence
                    </span>
                  </td>
                  {competitors.map(c => {
                    const diff = ((c.avg_price - derma.avg_price) / derma.avg_price * 100)
                    let label, color
                    if (diff > 10) { label = 'Plus cher'; color = 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300' }
                    else if (diff < -10) { label = 'Moins cher'; color = 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300' }
                    else { label = 'Similaire'; color = 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300' }
                    return (
                      <td key={c.brand} className="px-4 py-3 text-center">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${color}`}>
                          {diff > 0 ? <ArrowUpRight className="h-3 w-3 mr-1" /> : diff < 0 ? <ArrowDownRight className="h-3 w-3 mr-1" /> : <Minus className="h-3 w-3 mr-1" />}
                          {label} ({diff > 0 ? '+' : ''}{diff.toFixed(0)}%)
                        </span>
                      </td>
                    )
                  })}
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}

export default Compare
