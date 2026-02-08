import { ExternalLink, TrendingDown } from 'lucide-react'

const BRAND_COLORS = {
  'Dermalogica': 'bg-gray-900 text-white dark:bg-white dark:text-gray-900',
  "Paula's Choice": 'bg-accent-100 text-accent-800 dark:bg-accent-900/30 dark:text-accent-300',
  'Murad': 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300',
  'SkinCeuticals': 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300',
}

const ProductCard = ({ product, showDiscount = false }) => {
  const brandColor = BRAND_COLORS[product.brand] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden hover:shadow-lg transition-all group">
      <div className="relative aspect-square bg-gray-50 dark:bg-gray-700">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        ) : (
          <div className="flex items-center justify-center h-full text-gray-300 dark:text-gray-600">
            <Package className="h-12 w-12" />
          </div>
        )}
        {showDiscount && product.discount_percent && (
          <div className="absolute top-3 right-3 bg-red-500 text-white px-2.5 py-1 rounded-lg text-xs font-bold flex items-center shadow-lg">
            <TrendingDown className="h-3 w-3 mr-1" />
            {Math.abs(product.discount_percent)}%
          </div>
        )}
      </div>
      <div className="p-4">
        <div className="mb-2">
          <span className={`text-xs font-semibold px-2 py-0.5 rounded-md ${brandColor}`}>
            {product.brand}
          </span>
        </div>
        <h3 className="text-sm font-medium text-gray-900 dark:text-white mb-3 line-clamp-2 leading-snug">
          {product.name}
        </h3>
        <div className="flex items-center justify-between">
          <div>
            {product.current_price ? (
              <div className="flex items-baseline space-x-2">
                <span className="text-lg font-bold text-gray-900 dark:text-white">
                  {product.current_price}€
                </span>
                {showDiscount && product.old_price && (
                  <span className="text-sm text-gray-400 line-through">
                    {product.old_price}€
                  </span>
                )}
              </div>
            ) : (
              <span className="text-gray-400 text-sm">Prix N/A</span>
            )}
          </div>
          {product.url && (
            <a
              href={product.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              <ExternalLink className="h-4 w-4" />
            </a>
          )}
        </div>
      </div>
    </div>
  )
}

// Import Package for fallback icon
import { Package } from 'lucide-react'

export default ProductCard
