import { ExternalLink, TrendingDown } from 'lucide-react'

const ProductCard = ({ product, showDiscount = false }) => {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-all">
      <div className="relative aspect-square bg-gray-100 dark:bg-gray-700">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400">
            No image
          </div>
        )}
        {showDiscount && product.discount_percent && (
          <div className="absolute top-2 right-2 bg-red-500 text-white px-2 py-1 rounded-full text-xs font-bold flex items-center">
            <TrendingDown className="h-3 w-3 mr-1" />
            {Math.abs(product.discount_percent)}%
          </div>
        )}
      </div>
      <div className="p-4">
        <div className="mb-2">
          <span className="text-xs font-semibold text-primary-600 dark:text-primary-400 uppercase">
            {product.brand}
          </span>
        </div>
        <h3 className="text-sm font-medium text-gray-900 dark:text-white mb-2 line-clamp-2">
          {product.name}
        </h3>
        <div className="flex items-center justify-between">
          <div>
            {product.current_price ? (
              <div className="flex items-baseline space-x-2">
                <span className="text-xl font-bold text-gray-900 dark:text-white">
                  {product.current_price}€
                </span>
                {showDiscount && product.old_price && (
                  <span className="text-sm text-gray-500 line-through">
                    {product.old_price}€
                  </span>
                )}
              </div>
            ) : (
              <span className="text-gray-500 dark:text-gray-400 text-sm">Prix N/A</span>
            )}
          </div>
          {product.url && (
            <a
              href={product.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300"
            >
              <ExternalLink className="h-5 w-5" />
            </a>
          )}
        </div>
        <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
          <span className="capitalize">{product.site}</span>
        </div>
      </div>
    </div>
  )
}

export default ProductCard
