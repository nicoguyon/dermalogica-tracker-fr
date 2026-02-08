import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, ExternalLink, TrendingDown, TrendingUp, Minus, Package } from 'lucide-react'
import { fetchPriceHistory, fetchProducts } from '../utils/api'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts'

const BRAND_COLORS = {
  'Dermalogica': { bg: 'bg-gray-900 text-white dark:bg-white dark:text-gray-900', accent: '#1f2937' },
  "Paula's Choice": { bg: 'bg-sky-100 text-sky-800 dark:bg-sky-900/30 dark:text-sky-300', accent: '#2d8fb0' },
  'Murad': { bg: 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300', accent: '#7c3aed' },
  'SkinCeuticals': { bg: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300', accent: '#dc2626' },
}

const ProductDetail = () => {
  const { id } = useParams()
  const [product, setProduct] = useState(null)
  const [history, setHistory] = useState([])
  const [similar, setSimilar] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadProduct()
  }, [id])

  const loadProduct = async () => {
    setLoading(true)
    try {
      const data = await fetchPriceHistory(id)
      setProduct(data.product)
      setHistory(data.history)

      // Load similar products from same category
      if (data.product.category) {
        const allProducts = await fetchProducts({ per_page: 300 })
        const cat = (data.product.category || '').toLowerCase()
        const similarProducts = (allProducts.products || []).filter(
          p => p.id !== data.product.id && (p.category || '').toLowerCase() === cat
        ).slice(0, 8)
        setSimilar(similarProducts)
      }
    } catch (error) {
      console.error('Error loading product:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="h-8 w-48 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="aspect-square bg-gray-200 dark:bg-gray-700 rounded-xl animate-pulse" />
          <div className="space-y-4">
            <div className="h-6 w-24 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />
            <div className="h-10 w-3/4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />
            <div className="h-16 w-32 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />
          </div>
        </div>
      </div>
    )
  }

  if (!product) {
    return (
      <div className="text-center py-16">
        <Package className="h-16 w-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Produit introuvable</h2>
        <Link to="/products" className="text-sm text-gray-500 hover:text-gray-900 dark:hover:text-white mt-2 inline-block">
          Retour aux produits
        </Link>
      </div>
    )
  }

  const brandStyle = BRAND_COLORS[product.brand] || { bg: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300', accent: '#6b7280' }

  // Format history for chart
  const chartData = history.map(h => ({
    date: new Date(h.timestamp).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short' }),
    prix: h.price,
    fullDate: new Date(h.timestamp).toLocaleDateString('fr-FR', { day: '2-digit', month: 'long', year: 'numeric' }),
  })).sort((a, b) => new Date(a.fullDate) - new Date(b.fullDate))

  const currentPrice = history.length > 0 ? history[history.length - 1].price : null
  const oldPrice = history.length > 1 ? history[0].price : null
  const priceChange = currentPrice && oldPrice ? ((currentPrice - oldPrice) / oldPrice * 100) : 0
  const avgPrice = history.length > 0 ? history.reduce((sum, h) => sum + h.price, 0) / history.length : 0

  return (
    <div className="space-y-8">
      {/* Breadcrumb */}
      <Link to="/products" className="inline-flex items-center text-sm text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors">
        <ArrowLeft className="h-4 w-4 mr-1.5" />
        Retour aux produits
      </Link>

      {/* Product Hero */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Image */}
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
          {product.image_url ? (
            <img
              src={product.image_url}
              alt={product.name}
              className="w-full h-full object-cover aspect-square"
            />
          ) : (
            <div className="flex items-center justify-center aspect-square bg-gray-50 dark:bg-gray-700">
              <Package className="h-24 w-24 text-gray-300 dark:text-gray-600" />
            </div>
          )}
        </div>

        {/* Info */}
        <div className="space-y-6">
          <div>
            <span className={`inline-block text-xs font-semibold px-2.5 py-1 rounded-md mb-3 ${brandStyle.bg}`}>
              {product.brand}
            </span>
            <h1 className="text-2xl lg:text-3xl font-bold text-gray-900 dark:text-white leading-tight">
              {product.name}
            </h1>
            {product.category && (
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">{product.category}</p>
            )}
          </div>

          {/* Price */}
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-end gap-4">
              <span className="text-4xl font-bold text-gray-900 dark:text-white">
                {currentPrice ? `${currentPrice}€` : 'N/A'}
              </span>
              {priceChange !== 0 && (
                <div className={`flex items-center text-sm font-medium px-2.5 py-1 rounded-full ${
                  priceChange < 0 ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' : 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                }`}>
                  {priceChange < 0 ? <TrendingDown className="h-3.5 w-3.5 mr-1" /> : <TrendingUp className="h-3.5 w-3.5 mr-1" />}
                  {priceChange > 0 ? '+' : ''}{priceChange.toFixed(1)}%
                </div>
              )}
            </div>
            {oldPrice && oldPrice !== currentPrice && (
              <p className="text-sm text-gray-400 mt-1">
                Ancien prix : <span className="line-through">{oldPrice}€</span>
              </p>
            )}
            <div className="grid grid-cols-2 gap-4 mt-4 pt-4 border-t border-gray-100 dark:border-gray-700">
              <div>
                <p className="text-xs text-gray-500 dark:text-gray-400">Prix moyen</p>
                <p className="text-sm font-semibold text-gray-900 dark:text-white">{avgPrice.toFixed(2)}€</p>
              </div>
              <div>
                <p className="text-xs text-gray-500 dark:text-gray-400">Enregistrements</p>
                <p className="text-sm font-semibold text-gray-900 dark:text-white">{history.length}</p>
              </div>
            </div>
          </div>

          {/* Meta */}
          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-gray-500 dark:text-gray-400">Site</span>
              <span className="font-medium text-gray-900 dark:text-white">{product.site}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-500 dark:text-gray-400">Ajouté le</span>
              <span className="font-medium text-gray-900 dark:text-white">
                {new Date(product.first_seen).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })}
              </span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-500 dark:text-gray-400">Dernière MAJ</span>
              <span className="font-medium text-gray-900 dark:text-white">
                {new Date(product.last_updated).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })}
              </span>
            </div>
          </div>

          {/* Actions */}
          {product.url && (
            <a
              href={product.url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center px-6 py-3 bg-gray-900 dark:bg-white text-white dark:text-gray-900 rounded-lg text-sm font-medium hover:bg-gray-800 dark:hover:bg-gray-100 transition-colors"
            >
              Voir sur {product.site}
              <ExternalLink className="h-4 w-4 ml-2" />
            </a>
          )}
        </div>
      </div>

      {/* Price History Chart */}
      {chartData.length > 1 && (
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Historique des Prix
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" className="dark:opacity-20" />
              <XAxis dataKey="date" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} domain={['auto', 'auto']} label={{ value: '€', angle: -90, position: 'insideLeft' }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(0, 0, 0, 0.85)',
                  border: 'none',
                  borderRadius: '8px',
                  color: '#fff',
                  fontSize: '13px',
                }}
                formatter={(value) => [`${value}€`, 'Prix']}
              />
              <ReferenceLine y={avgPrice} stroke="#9ca3af" strokeDasharray="3 3" label={{ value: `Moy: ${avgPrice.toFixed(0)}€`, position: 'right', fontSize: 11, fill: '#9ca3af' }} />
              <Line
                type="monotone"
                dataKey="prix"
                stroke={brandStyle.accent}
                strokeWidth={2.5}
                dot={{ fill: brandStyle.accent, r: 4 }}
                activeDot={{ r: 6, strokeWidth: 2, stroke: '#fff' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Similar Products */}
      {similar.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Produits similaires ({product.category})
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
            {similar.map(p => {
              const pBrand = BRAND_COLORS[p.brand] || { bg: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300' }
              const isDerma = p.brand === 'Dermalogica'
              return (
                <Link
                  key={p.id}
                  to={`/product/${p.id}`}
                  className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden hover:shadow-lg transition-all group"
                >
                  <div className="relative aspect-square bg-gray-50 dark:bg-gray-700">
                    {p.image_url ? (
                      <img src={p.image_url} alt={p.name} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
                    ) : (
                      <div className="flex items-center justify-center h-full text-gray-300 dark:text-gray-600">
                        <Package className="h-8 w-8" />
                      </div>
                    )}
                  </div>
                  <div className="p-3">
                    <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${pBrand.bg}`}>
                      {p.brand}
                    </span>
                    <h4 className="text-xs font-medium text-gray-900 dark:text-white mt-1.5 line-clamp-2 leading-snug">
                      {p.name}
                    </h4>
                    <p className="text-sm font-bold text-gray-900 dark:text-white mt-2">
                      {p.current_price ? `${p.current_price}€` : 'N/A'}
                    </p>
                  </div>
                </Link>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}

export default ProductDetail
