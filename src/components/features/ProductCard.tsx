import { useState } from 'react'
import { Product, ProductCardProps } from '../../types/product.types'
import StarRating from '../common/StarRating'
import Button from '../common/Button'

const ProductCard = ({
  product,
  onAddToCart,
  onQuickView,
  onFavorite,
  isFavorite = false,
  showQuickView = true,
  compact = false
}: ProductCardProps) => {
  const [isHovered, setIsHovered] = useState(false)
  const [isFavorited, setIsFavorited] = useState(isFavorite)
  const [isAdding, setIsAdding] = useState(false)

  const handleAddToCart = async (e: React.MouseEvent) => {
    e.stopPropagation()
    if (onAddToCart && !isAdding) {
      setIsAdding(true)
      await onAddToCart(product)
      // Simulate animation delay
      setTimeout(() => setIsAdding(false), 1000)
    }
  }

  const handleFavorite = (e: React.MouseEvent) => {
    e.stopPropagation()
    setIsFavorited(!isFavorited)
    if (onFavorite) {
      onFavorite(product)
    }
  }

  const handleQuickView = (e: React.MouseEvent) => {
    e.stopPropagation()
    if (onQuickView) {
      onQuickView(product)
    }
  }

  const calculateDiscount = () => {
    if (product.originalPrice && product.originalPrice > product.price) {
      return Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100)
    }
    return 0
  }

  const discount = calculateDiscount()
  const currency = product.currency || '$'

  const badgeColors = {
    sale: 'bg-red-500',
    new: 'bg-blue-500',
    trending: 'bg-purple-500',
    limited: 'bg-orange-500',
    bestseller: 'bg-green-500'
  }

  return (
    <article
      className={`group bg-white rounded-xl shadow-md hover:shadow-2xl transition-all duration-300 overflow-hidden ${
        compact ? 'max-w-xs' : 'max-w-sm'
      } transform hover:-translate-y-1`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      role="article"
      aria-label={`Product: ${product.title}`}
    >
      {/* Image Container */}
      <div className="relative aspect-square overflow-hidden bg-gray-100">
        {/* Product Image */}
        <img
          src={product.image}
          alt={product.title}
          className={`w-full h-full object-cover transition-transform duration-500 ${
            isHovered ? 'scale-110' : 'scale-100'
          }`}
          loading="lazy"
        />

        {/* Badges */}
        <div className="absolute top-3 left-3 flex flex-col gap-2">
          {product.badge && (
            <span
              className={`${badgeColors[product.badge.type]} text-white text-xs font-bold px-3 py-1 rounded-full shadow-md uppercase tracking-wide`}
            >
              {product.badge.text}
            </span>
          )}
          {discount > 0 && (
            <span className="bg-red-500 text-white text-xs font-bold px-3 py-1 rounded-full shadow-md">
              -{discount}%
            </span>
          )}
        </div>

        {/* Favorite Button */}
        <button
          onClick={handleFavorite}
          className="absolute top-3 right-3 p-2 bg-white rounded-full shadow-md hover:scale-110 transition-transform duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
          aria-label={isFavorited ? 'Remove from favorites' : 'Add to favorites'}
          aria-pressed={isFavorited}
        >
          <svg
            className={`w-5 h-5 transition-colors ${
              isFavorited ? 'text-red-500 fill-current' : 'text-gray-400'
            }`}
            fill={isFavorited ? 'currentColor' : 'none'}
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
            />
          </svg>
        </button>

        {/* Quick View Button - Appears on Hover */}
        {showQuickView && (
          <button
            onClick={handleQuickView}
            className={`absolute bottom-3 left-1/2 -translate-x-1/2 px-4 py-2 bg-white text-gray-800 rounded-lg shadow-md font-medium transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              isHovered ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'
            }`}
            aria-label={`Quick view ${product.title}`}
          >
            Quick View
          </button>
        )}

        {/* Out of Stock Overlay */}
        {product.inStock === false && (
          <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <span className="text-white text-lg font-bold bg-black bg-opacity-75 px-4 py-2 rounded-lg">
              Out of Stock
            </span>
          </div>
        )}
      </div>

      {/* Product Info */}
      <div className={`p-4 ${compact ? 'space-y-2' : 'space-y-3'}`}>
        {/* Category */}
        {product.category && (
          <p className="text-xs text-gray-500 uppercase tracking-wide font-semibold">
            {product.category}
          </p>
        )}

        {/* Title */}
        <h3 className={`font-bold text-gray-900 line-clamp-2 ${compact ? 'text-base' : 'text-lg'}`}>
          {product.title}
        </h3>

        {/* Description */}
        <p className={`text-gray-600 line-clamp-2 ${compact ? 'text-xs' : 'text-sm'}`}>
          {product.description}
        </p>

        {/* Rating */}
        <StarRating
          rating={product.rating.average}
          reviewCount={product.rating.count}
          size={compact ? 'sm' : 'md'}
        />

        {/* Colors */}
        {product.colors && product.colors.length > 0 && (
          <div className="flex items-center gap-2">
            <span className="text-xs text-gray-500">Colors:</span>
            <div className="flex gap-1">
              {product.colors.slice(0, 5).map((color, index) => (
                <div
                  key={index}
                  className="w-5 h-5 rounded-full border-2 border-gray-300 hover:scale-110 transition-transform cursor-pointer"
                  style={{ backgroundColor: color }}
                  title={color}
                  role="button"
                  aria-label={`Select color ${color}`}
                  tabIndex={0}
                />
              ))}
              {product.colors.length > 5 && (
                <span className="text-xs text-gray-500 flex items-center">
                  +{product.colors.length - 5}
                </span>
              )}
            </div>
          </div>
        )}

        {/* Price and Add to Cart */}
        <div className="flex items-center justify-between pt-2 border-t border-gray-200">
          <div className="flex flex-col">
            <div className="flex items-center gap-2">
              <span className={`font-bold text-gray-900 ${compact ? 'text-lg' : 'text-xl'}`}>
                {currency}{product.price.toFixed(2)}
              </span>
              {product.originalPrice && product.originalPrice > product.price && (
                <span className="text-sm text-gray-500 line-through">
                  {currency}{product.originalPrice.toFixed(2)}
                </span>
              )}
            </div>
            {discount > 0 && (
              <span className="text-xs text-red-600 font-semibold">
                Save {currency}{(product.originalPrice! - product.price).toFixed(2)}
              </span>
            )}
          </div>

          <Button
            onClick={handleAddToCart}
            variant="primary"
            className={`${
              compact ? 'px-3 py-2 text-sm' : 'px-4 py-2'
            } flex items-center gap-2 ${isAdding ? 'animate-pulse' : ''}`}
            disabled={product.inStock === false || isAdding}
            aria-label={`Add ${product.title} to cart`}
          >
            {isAdding ? (
              <>
                <svg
                  className="animate-spin h-4 w-4"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
                <span className="hidden sm:inline">Adding...</span>
              </>
            ) : (
              <>
                <svg
                  className="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
                  />
                </svg>
                <span className="hidden sm:inline">Add</span>
              </>
            )}
          </Button>
        </div>
      </div>
    </article>
  )
}

export default ProductCard
