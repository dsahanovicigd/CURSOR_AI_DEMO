export interface Product {
  id: string
  title: string
  description: string
  price: number
  originalPrice?: number // For showing discounts
  currency?: string
  image: string
  rating: ProductRating
  category?: string
  inStock?: boolean
  badge?: ProductBadge
  colors?: string[]
  sizes?: string[]
}

export interface ProductRating {
  average: number // 0-5
  count: number // Number of reviews
}

export interface ProductBadge {
  text: string
  type: 'sale' | 'new' | 'trending' | 'limited' | 'bestseller'
}

export interface ProductCardProps {
  product: Product
  onAddToCart?: (product: Product) => void
  onQuickView?: (product: Product) => void
  onFavorite?: (product: Product) => void
  isFavorite?: boolean
  showQuickView?: boolean
  compact?: boolean
}
