import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Search, X, Plus, Package, ExternalLink, ArrowLeft } from 'lucide-react'
import { searchProducts, fetchPriceHistory } from '../utils/api'

const BRAND_COLORS = {
  'Dermalogica': { bg: 'bg-gray-900 text-white dark:bg-white dark:text-gray-900', accent: '#1f2937' },
  "Paula's Choice": { bg: 'bg-sky-100 text-sky-800 dark:bg-sky-900/30 dark:text-sky-300', accent: '#2d8fb0' },
  'Murad': { bg: 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300', accent: '#7c3aed' },
  'SkinCeuticals': { bg: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300', accent: '#dc2626' },
}

const ProductCompare = () => {
  const [selectedProducts, setSelectedProducts] = useState([])
  const [productDetails, setProductDetails] = useState({})
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [searching, setSearching] = useState(false)
  const [showSearch, setShowSearch] = useState(false)

  useEffect(() => {
    if (searchQuery.length >= 2) {
      const timeout = setTimeout(() => doSearch(), 300)
      return () => clearTimeout(timeout)
    } else {
      setSearchResults([])
    }
  }, [searchQuery])

  const doSearch = async () => {
    setSearching(true)
    try {
      const results = await searchProducts(searchQuery)
      setSearchResults(results.filter(r => !selectedProducts.includes(r.id)))
    } catch (error) {
      console.error('Search error:', error)
    } finally {
      setSearching(false)
    }
  }

  const addProduct = async (product) => {
    if (selectedProducts.length >= 4) return
    setSelectedProducts(prev => [...prev, product.id])
    setSearchQuery('')
    setSearchResults([])
    setShowSearch(false)

    try {
      const data = await fetchPriceHistory(product.id)
      setProductDetails(prev => ({ ...prev, [product.id]: { ...data.product, history: data.history, current_price: product.current_price } }))
    } catch (error) {
      console.error('Error loading product detail:', error)
    }
  }

  const removeProduct = (id) => {
    setSelectedProducts(prev => prev.filter(p => p !== id))
    setProductDetails(prev => {
      const next = { ...prev }
      delete next[id]
      return next
    })
  }

  const products = selectedProducts.map(id => productDetails[id]).filter(Boolean)
  const cheapest = products.length > 0 ? Math.min(...products.filter(p => p.current_price).map(p => p.current_price)) : 0
  const mostExpensive = products.length > 0 ? Math.max(...products.filter(p => p.current_price).map(p => p.current_price)) : 0

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <Link to="/compare" className="inline-flex items-center text-sm text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors mb-2">
            <ArrowLeft className="h-4 w-4 mr-1" />
            Analyse comparative
          </Link>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Comparer des Produits</h1>
          <p className="text-gray-500 dark:text-gray-400 mt-1">
            Sélectionnez 2 à 4 produits pour les comparer
          </p>
        </div>
      </div>

      {/* Product Selector */}
      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-5">
        <div className="flex items-center gap-3 flex-wrap">
          {/* Selected product chips */}
          {products.map(p => {
            const brand = BRAND_COLORS[p.brand] || { bg: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300' }
            return (
              <div key={p.id} className="flex items-center gap-2 bg-gray-100 dark:bg-gray-700 rounded-lg px-3 py-2">
                {p.image_url && (
                  <img src={p.image_url} alt="" className="w-8 h-8 rounded object-cover" />
                )}
                <div>
                  <p className="text-xs font-medium text-gray-900 dark:text-white line-clamp-1">{p.name}</p>
                  <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${brand.bg}`}>{p.brand}</span>
                </div>
                <button onClick={() => removeProduct(p.id)} className="text-gray-400 hover:text-red-500 transition-colors">
                  <X className="h-4 w-4" />
                </button>
              </div>
            )
          })}

          {/* Add button */}
          {selectedProducts.length < 4 && (
            <div className="relative">
              <button
                onClick={() => setShowSearch(!showSearch)}
                className="flex items-center gap-2 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg px-4 py-2.5 text-sm text-gray-500 dark:text-gray-400 hover:border-gray-400 dark:hover:border-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
              >
                <Plus className="h-4 w-4" />
                Ajouter un produit
              </button>

              {showSearch && (
                <div className="absolute top-full left-0 mt-2 w-80 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-xl z-50">
                  <div className="p-3">
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
                      <input
                        type="text"
                        placeholder="Rechercher un produit..."
                        value={searchQuery}
                        onChange={e => setSearchQuery(e.target.value)}
                        autoFocus
                        className="w-full pl-9 pr-4 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm focus:ring-2 focus:ring-gray-900 dark:focus:ring-white dark:bg-gray-700 dark:text-white"
                      />
                    </div>
                  </div>
                  <div className="max-h-64 overflow-y-auto border-t border-gray-100 dark:border-gray-700">
                    {searching ? (
                      <div className="p-4 text-center text-sm text-gray-400">Recherche...</div>
                    ) : searchResults.length === 0 && searchQuery.length >= 2 ? (
                      <div className="p-4 text-center text-sm text-gray-400">Aucun résultat</div>
                    ) : (
                      searchResults.map(r => (
                        <button
                          key={r.id}
                          onClick={() => addProduct(r)}
                          className="w-full flex items-center gap-3 px-3 py-2.5 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-left"
                        >
                          {r.image_url ? (
                            <img src={r.image_url} alt="" className="w-10 h-10 rounded object-cover flex-shrink-0" />
                          ) : (
                            <div className="w-10 h-10 bg-gray-100 dark:bg-gray-600 rounded flex items-center justify-center flex-shrink-0">
                              <Package className="h-5 w-5 text-gray-400" />
                            </div>
                          )}
                          <div className="min-w-0">
                            <p className="text-sm font-medium text-gray-900 dark:text-white truncate">{r.name}</p>
                            <p className="text-xs text-gray-500 dark:text-gray-400">{r.brand} - {r.current_price ? `${r.current_price}€` : 'N/A'}</p>
                          </div>
                        </button>
                      ))
                    )}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Comparison Table */}
      {products.length >= 2 ? (
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
          {/* Product images row */}
          <div className="grid" style={{ gridTemplateColumns: `200px repeat(${products.length}, 1fr)` }}>
            <div className="p-4 border-b border-r border-gray-100 dark:border-gray-700"></div>
            {products.map(p => {
              const brand = BRAND_COLORS[p.brand] || { bg: 'bg-gray-100 text-gray-800' }
              return (
                <div key={p.id} className="p-4 border-b border-r border-gray-100 dark:border-gray-700 last:border-r-0 text-center">
                  <div className="mx-auto w-24 h-24 rounded-lg overflow-hidden mb-3 bg-gray-50 dark:bg-gray-700">
                    {p.image_url ? (
                      <img src={p.image_url} alt={p.name} className="w-full h-full object-cover" />
                    ) : (
                      <div className="flex items-center justify-center h-full"><Package className="h-8 w-8 text-gray-300" /></div>
                    )}
                  </div>
                  <span className={`inline-block text-[10px] font-semibold px-2 py-0.5 rounded ${brand.bg} mb-1`}>{p.brand}</span>
                  <Link to={`/product/${p.id}`} className="block text-xs font-medium text-gray-900 dark:text-white line-clamp-2 hover:underline">{p.name}</Link>
                </div>
              )
            })}
          </div>

          {/* Comparison rows */}
          {[
            { label: 'Prix', render: p => {
              const isMin = p.current_price === cheapest
              const isMax = p.current_price === mostExpensive
              return (
                <div className="flex items-center gap-2">
                  <span className={`text-lg font-bold ${isMin ? 'text-green-600 dark:text-green-400' : isMax ? 'text-red-600 dark:text-red-400' : 'text-gray-900 dark:text-white'}`}>
                    {p.current_price ? `${p.current_price}€` : 'N/A'}
                  </span>
                  {isMin && products.length > 1 && <span className="text-[10px] font-medium bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 px-1.5 py-0.5 rounded">Le - cher</span>}
                  {isMax && products.length > 1 && <span className="text-[10px] font-medium bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 px-1.5 py-0.5 rounded">Le + cher</span>}
                </div>
              )
            }},
            { label: 'Marque', render: p => <span className="text-sm text-gray-700 dark:text-gray-300">{p.brand}</span> },
            { label: 'Catégorie', render: p => <span className="text-sm text-gray-700 dark:text-gray-300">{p.category || 'N/A'}</span> },
            { label: 'Site', render: p => <span className="text-sm text-gray-700 dark:text-gray-300">{p.site}</span> },
            { label: 'Historique prix', render: p => <span className="text-sm text-gray-700 dark:text-gray-300">{p.history?.length || 0} enregistrement(s)</span> },
            { label: 'Lien', render: p => p.url ? (
              <a href={p.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center text-xs text-gray-500 hover:text-gray-900 dark:hover:text-white transition-colors">
                Voir <ExternalLink className="h-3 w-3 ml-1" />
              </a>
            ) : <span className="text-xs text-gray-400">N/A</span> },
          ].map((row, i) => (
            <div key={i} className="grid" style={{ gridTemplateColumns: `200px repeat(${products.length}, 1fr)` }}>
              <div className="px-4 py-3 border-b border-r border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/30">
                <span className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">{row.label}</span>
              </div>
              {products.map(p => (
                <div key={p.id} className="px-4 py-3 border-b border-r border-gray-100 dark:border-gray-700 last:border-r-0">
                  {row.render(p)}
                </div>
              ))}
            </div>
          ))}
        </div>
      ) : products.length === 1 ? (
        <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
          <Plus className="h-12 w-12 text-gray-300 dark:text-gray-600 mx-auto mb-3" />
          <p className="text-gray-500 dark:text-gray-400">Ajoutez au moins un autre produit pour comparer</p>
        </div>
      ) : (
        <div className="text-center py-16 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
          <Search className="h-12 w-12 text-gray-300 dark:text-gray-600 mx-auto mb-3" />
          <p className="text-gray-500 dark:text-gray-400">Recherchez et sélectionnez des produits à comparer</p>
          <p className="text-xs text-gray-400 mt-1">Comparez jusqu'à 4 produits côte à côte</p>
        </div>
      )}
    </div>
  )
}

export default ProductCompare
