import { useState, useEffect } from 'react'
import { ProductCard } from '../components'
import { Product } from '../types/product.types'
import { productsAPI, cartAPI, authAPI } from '../services/api'
import CheckoutModal from '../components/checkout/CheckoutModal'

type FilterType = 'all' | 'sale' | 'bestseller' | 'new' | 'instock'
type SortType = 'featured' | 'price-low' | 'price-high' | 'rating'

const ProductShowcase = () => {
  const [products, setProducts] = useState<Product[]>([])
  const [filter, setFilter] = useState<FilterType>('all')
  const [sort, setSort] = useState<SortType>('featured')
  const [favorites, setFavorites] = useState<Set<string>>(new Set())
  const [cartCount, setCartCount] = useState(0)
  interface Cart {
    id: number;
    items: Array<{ id: number; product_id: number; quantity: number; product?: Product }>;
    total: number;
    item_count?: number;
    discount_code?: string;
    discount_amount?: number;
  }
  const [cart, setCart] = useState<Cart | null>(null)
  const [showCheckout, setShowCheckout] = useState(false)
  const [, setLoading] = useState(true)
  const [, setError] = useState<string | null>(null)

  // Load products and cart on mount
  useEffect(() => {
    loadProducts()
    // Auto-login with test account if not authenticated
    const autoLogin = async () => {
      if (!authAPI.isAuthenticated()) {
        try {
          console.log('Auto-login attempt on page load...')
          await authAPI.login('testcustomer', 'customerpassword123')
          console.log('Auto-login successful on page load')
        } catch (err) {
          const error = err as Error;
          console.log('Auto-login failed on page load:', error.message)
          // If login fails, try to register a guest user
          try {
            const guestUsername = `guest_${Math.random().toString(36).substring(7)}`
            console.log('Attempting guest registration on page load...', guestUsername)
            await authAPI.register({
              username: guestUsername,
              email: `${guestUsername}@example.com`,
              password: 'guest123'
            })
            console.log('Guest registration successful on page load')
          } catch (registerErr) {
            const error = registerErr as Error;
            console.log('Auto-login/register failed on page load:', error.message)
            // Continue without auth - user can still browse products
          }
        }
      }
      // Load cart after authentication attempt
      loadCart()
    }
    autoLogin()

    // Listen for cart update events from CheckoutModal
    const handleCartUpdate = () => {
      console.log('Cart update event received, reloading cart...')
      loadCart()
    }
    window.addEventListener('cartUpdated', handleCartUpdate)

    return () => {
      window.removeEventListener('cartUpdated', handleCartUpdate)
    }
  }, [])

  const loadProducts = async () => {
    try {
      setLoading(true)
      const response = await productsAPI.getAll({ per_page: 100 })
      // Transform API products to match frontend Product type
      interface ApiProduct {
        id: number;
        title: string;
        description?: string;
        price: string | number;
        originalPrice?: string | number;
        currency?: string;
        image?: string;
        rating: { average: string | number; count: number };
        category?: string;
        inStock?: boolean;
        badge?: { type: string; text: string };
        colors?: string[];
        sizes?: string[];
      }
      const transformedProducts = response.products.map((p: ApiProduct) => ({
        id: p.id.toString(),
        title: p.title,
        description: p.description || '',
        price: parseFloat(p.price),
        originalPrice: p.originalPrice ? parseFloat(p.originalPrice) : undefined,
        currency: p.currency || '$',
        image: p.image || 'https://via.placeholder.com/400',
        rating: {
          average: parseFloat(p.rating.average),
          count: p.rating.count
        },
        category: p.category,
        inStock: p.inStock,
        badge: p.badge,
        colors: p.colors || [],
        sizes: p.sizes || []
      }))
      setProducts(transformedProducts)
      setError(null)
    } catch (err) {
      const error = err as Error;
      console.error('Failed to load products:', err)
      const errorMsg = error.message || 'Failed to load products'
      setError(errorMsg)
      // Fallback to sample products if API fails
      const { sampleProducts } = await import('../data/sampleProducts')
      setProducts(sampleProducts)
    } finally {
      setLoading(false)
    }
  }

  const loadCart = async () => {
    try {
      const response = await cartAPI.get()
      console.log('Cart loaded:', response.cart)
      if (response.cart) {
        setCart(response.cart)
        const itemCount = response.cart.item_count || response.cart.items?.length || 0
        setCartCount(itemCount)
        console.log('Cart count updated to:', itemCount)
      }
    } catch (err) {
      const error = err as Error & { status?: number };
      console.error('Failed to load cart:', err)
      // If not authenticated (401), try to auto-login
      if (error.status === 401 || (error.message && error.message.includes('401'))) {
        try {
          await authAPI.login('testcustomer', 'customerpassword123')
          // Retry loading cart
          const retryResponse = await cartAPI.get()
          if (retryResponse.cart) {
            setCart(retryResponse.cart)
            const itemCount = retryResponse.cart.item_count || retryResponse.cart.items?.length || 0
            setCartCount(itemCount)
          }
        } catch (loginErr) {
          // Silently fail - cart will be empty
          console.log('Cart not available without authentication')
        }
      } else {
        setError(error.message)
      }
    }
  }

  const handleAddToCart = async (product: Product) => {
    try {
      console.log('Adding product to cart:', product.id)
      const response = await cartAPI.addItem(parseInt(product.id), 1)
      console.log('Add to cart response:', response)
      
      // Update cart immediately from response
      if (response.cart) {
        setCart(response.cart)
        setCartCount(response.cart.item_count || response.cart.items?.length || 0)
        console.log('Cart updated from response, count:', response.cart.item_count || response.cart.items?.length || 0)
      }
      
      // Also reload cart to ensure sync
      await loadCart()
      console.log('Product added to cart successfully, final count:', cartCount)
    } catch (err) {
      const error = err as Error & { status?: number; isNetworkError?: boolean; originalError?: string };
      console.error('Add to cart error:', err)
      console.error('Error details:', {
        message: error.message,
        status: error.status,
        isNetworkError: error.isNetworkError,
        originalError: error.originalError
      })
      
      // Handle network errors
      if (error.isNetworkError || error.status === 0 || error.message?.includes('Failed to fetch')) {
        alert(`Unable to connect to the Flask API server.\n\nPlease ensure:\n1. Flask server is running on http://localhost:5001\n2. Check browser console for CORS errors\n3. Verify API_BASE_URL in src/services/api.ts\n\nError: ${error.message || error.originalError || 'Network error'}`)
        return
      }
      
      // If not authenticated (401), try to auto-login/register
      if (error.status === 401 || (error.message && (error.message.includes('401') || error.message.includes('Authorization') || error.message.includes('Unauthorized')))) {
        try {
          // First try to login with a default test account
          console.log('Attempting auto-login...')
          await authAPI.login('testcustomer', 'customerpassword123')
          console.log('Auto-login successful, retrying add to cart')
          // Retry adding to cart after login
          const retryResponse = await cartAPI.addItem(parseInt(product.id), 1)
          if (retryResponse.cart) {
            setCart(retryResponse.cart)
            setCartCount(retryResponse.cart.item_count || retryResponse.cart.items?.length || 0)
          }
          await loadCart()
        } catch (loginErr) {
          console.error('Auto-login failed:', loginErr)
          // If login fails, try to register a new guest user
          try {
            const guestUsername = `guest_${Math.random().toString(36).substring(7)}`
            console.log('Attempting guest registration...', guestUsername)
            await authAPI.register({
              username: guestUsername,
              email: `${guestUsername}@example.com`,
              password: 'guest123'
            })
            console.log('Guest registration successful, retrying add to cart')
            // Retry adding to cart after registration
            const retryResponse = await cartAPI.addItem(parseInt(product.id), 1)
            if (retryResponse.cart) {
              setCart(retryResponse.cart)
              setCartCount(retryResponse.cart.item_count || retryResponse.cart.items?.length || 0)
            }
            await loadCart()
          } catch (registerErr) {
            const registerError = registerErr as Error & { status?: number; isNetworkError?: boolean; originalError?: string };
            console.error('Auto-registration failed:', registerErr)
            // Show detailed error for debugging
            const errorMsg = registerError.message || 'Unknown error'
            if (registerError.isNetworkError || registerError.status === 0) {
              alert(`Unable to connect to the Flask API server.\n\nPlease ensure:\n1. Flask server is running on http://localhost:5001\n2. Check browser console for CORS errors\n\nError: ${registerError.message || registerError.originalError || 'Network error'}`)
            } else {
              alert(`Unable to add item to cart: ${errorMsg}\n\nPlease check the browser console for more details.`)
            }
          }
        }
      } else {
        alert(`Failed to add item to cart: ${error.message || 'Unknown error'}\n\nStatus: ${error.status || 'N/A'}`)
      }
    }
  }

  const handleQuickView = (product: Product) => {
    alert(`Quick View: ${product.title}\n\n${product.description}\n\nPrice: $${product.price}`)
  }

  const handleFavorite = (product: Product) => {
    setFavorites(prev => {
      const newFavorites = new Set(prev)
      if (newFavorites.has(product.id)) {
        newFavorites.delete(product.id)
      } else {
        newFavorites.add(product.id)
      }
      return newFavorites
    })
  }

  const getFilteredProducts = () => {
    let filtered = [...products]

    // Apply filter
    switch (filter) {
      case 'sale':
        filtered = filtered.filter(p => p.originalPrice && p.originalPrice > p.price)
        break
      case 'bestseller':
        filtered = filtered.filter(p => p.badge?.type === 'bestseller')
        break
      case 'new':
        filtered = filtered.filter(p => p.badge?.type === 'new')
        break
      case 'instock':
        filtered = filtered.filter(p => p.inStock !== false)
        break
    }

    // Apply sort
    switch (sort) {
      case 'price-low':
        filtered.sort((a, b) => a.price - b.price)
        break
      case 'price-high':
        filtered.sort((a, b) => b.price - a.price)
        break
      case 'rating':
        filtered.sort((a, b) => b.rating.average - a.rating.average)
        break
    }

    return filtered
  }

  const filteredProducts = getFilteredProducts()

  const filterButtons: { type: FilterType; label: string; icon: string }[] = [
    { type: 'all', label: 'All Products', icon: '🛍️' },
    { type: 'sale', label: 'On Sale', icon: '🏷️' },
    { type: 'bestseller', label: 'Bestsellers', icon: '⭐' },
    { type: 'new', label: 'New Arrivals', icon: '✨' },
    { type: 'instock', label: 'In Stock', icon: '✅' }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-md border-b border-gray-200 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">🛒</span>
              </div>
              <h1 className="text-2xl font-bold text-gray-800">Product Showcase</h1>
            </div>
            
            {/* Cart Counter */}
            <div className="relative">
              <button 
                onClick={() => {
                  console.log('Cart button clicked, cartCount:', cartCount, 'cart:', cart)
                  if (cartCount > 0 || (cart && cart.items && cart.items.length > 0)) {
                    setShowCheckout(true)
                  } else {
                    // Try to load cart first
                    loadCart().then(() => {
                      if (cartCount > 0 || (cart && cart.items && cart.items.length > 0)) {
                        setShowCheckout(true)
                      } else {
                        alert('Your cart is empty. Add some products first!')
                      }
                    })
                  }
                }}
                className={`p-2 rounded-lg transition-colors ${
                  cartCount > 0 || (cart && cart.items && cart.items.length > 0)
                    ? 'bg-blue-600 text-white hover:bg-blue-700'
                    : 'bg-gray-400 text-white cursor-not-allowed'
                }`}
                title={cartCount > 0 ? `View cart (${cartCount} items)` : 'Cart is empty'}
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                {(cartCount > 0 || (cart && cart.items && cart.items.length > 0)) && (
                  <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
                    {cartCount || (cart?.items?.length || 0)}
                  </span>
                )}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-12">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Discover Amazing Products
          </h2>
          <p className="text-lg md:text-xl text-blue-100 mb-6">
            Shop our curated collection of premium products with exclusive deals
          </p>
          <div className="flex flex-wrap justify-center gap-2">
            <span className="bg-white text-blue-600 px-4 py-2 rounded-full text-sm font-semibold">
              Free Shipping Over $50
            </span>
            <span className="bg-white text-purple-600 px-4 py-2 rounded-full text-sm font-semibold">
              30-Day Returns
            </span>
            <span className="bg-white text-green-600 px-4 py-2 rounded-full text-sm font-semibold">
              Secure Checkout
            </span>
          </div>
        </div>
      </div>

      {/* Filters and Sort */}
      <div className="container mx-auto px-4 py-8">
        <div className="bg-white rounded-xl shadow-md p-6 mb-8">
          {/* Filter Buttons */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-3">Filter By:</h3>
            <div className="flex flex-wrap gap-2">
              {filterButtons.map(({ type, label, icon }) => (
                <button
                  key={type}
                  onClick={() => setFilter(type)}
                  className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                    filter === type
                      ? 'bg-blue-600 text-white shadow-lg scale-105'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  <span className="flex items-center gap-2">
                    <span>{icon}</span>
                    <span>{label}</span>
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Sort Options */}
          <div className="flex flex-wrap items-center gap-4">
            <label className="text-sm font-semibold text-gray-700">Sort By:</label>
            <select
              value={sort}
              onChange={(e) => setSort(e.target.value as SortType)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="featured">Featured</option>
              <option value="price-low">Price: Low to High</option>
              <option value="price-high">Price: High to Low</option>
              <option value="rating">Highest Rated</option>
            </select>
            
            <span className="text-sm text-gray-600 ml-auto">
              Showing {filteredProducts.length} of {products.length} products
            </span>
          </div>
        </div>

        {/* Products Grid */}
        {filteredProducts.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredProducts.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                onAddToCart={handleAddToCart}
                onQuickView={handleQuickView}
                onFavorite={handleFavorite}
                isFavorite={favorites.has(product.id)}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-16 bg-white rounded-xl shadow-md">
            <div className="text-6xl mb-4">🔍</div>
            <h3 className="text-2xl font-semibold text-gray-700 mb-2">
              No products found
            </h3>
            <p className="text-gray-500 mb-4">
              Try adjusting your filters
            </p>
            <button
              onClick={() => setFilter('all')}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Show All Products
            </button>
          </div>
        )}
      </div>

      {/* Features Section */}
      <div className="container mx-auto px-4 py-12">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
            ✨ ProductCard Component Features
          </h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="space-y-3">
              <h3 className="font-semibold text-gray-800 text-lg flex items-center gap-2">
                <span className="text-2xl">🎨</span>
                <span>Visual Design</span>
              </h3>
              <ul className="space-y-2 text-gray-600 text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Smooth hover effects with image zoom</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Product badges (Sale, New, Bestseller)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Discount percentage display</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Color variant swatches</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Responsive card layout</span>
                </li>
              </ul>
            </div>
            
            <div className="space-y-3">
              <h3 className="font-semibold text-gray-800 text-lg flex items-center gap-2">
                <span className="text-2xl">⚡</span>
                <span>Interactive Features</span>
              </h3>
              <ul className="space-y-2 text-gray-600 text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Add to cart with loading animation</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Favorite/wishlist toggle</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Quick view button on hover</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Out of stock state handling</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Star rating with review count</span>
                </li>
              </ul>
            </div>
            
            <div className="space-y-3">
              <h3 className="font-semibold text-gray-800 text-lg flex items-center gap-2">
                <span className="text-2xl">♿</span>
                <span>Accessibility</span>
              </h3>
              <ul className="space-y-2 text-gray-600 text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Semantic HTML structure</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>ARIA labels on all buttons</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Keyboard navigation support</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Screen reader descriptions</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>Focus indicators</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-gray-600">
            <p className="mb-2">
              Built with React, TypeScript, Vite, and Tailwind CSS
            </p>
            <p className="text-sm text-gray-500">
              Try adding products to cart, filtering, sorting, and favoriting items!
            </p>
          </div>
        </div>
      </footer>

      {/* Checkout Modal */}
      {showCheckout && (
        <CheckoutModal
          cart={cart || null}
          onClose={async () => {
            console.log('Closing checkout modal')
            setShowCheckout(false)
            try {
              await loadCart() // Refresh cart when closing
            } catch (err) {
              console.error('Error loading cart on close:', err)
            }
          }}
          onOrderComplete={async () => {
            console.log('Order completed')
            setShowCheckout(false)
            setCartCount(0)
            setCart(null)
            try {
              await loadCart() // Refresh cart after order
            } catch (err) {
              console.error('Error loading cart after order:', err)
            }
          }}
          onCartUpdate={async () => {
            console.log('Cart updated from modal')
            try {
              await loadCart() // Refresh cart when item is removed
            } catch (err) {
              console.error('Error loading cart after update:', err)
            }
          }}
        />
      )}
    </div>
  )
}

export default ProductShowcase
