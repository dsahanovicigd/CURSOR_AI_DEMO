import { Product } from '../types/product.types'

export const sampleProducts: Product[] = [
  {
    id: '1',
    title: 'Wireless Noise-Cancelling Headphones',
    description: 'Premium over-ear headphones with active noise cancellation, 30-hour battery life, and studio-quality sound.',
    price: 249.99,
    originalPrice: 349.99,
    currency: '$',
    image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    rating: {
      average: 4.8,
      count: 2847
    },
    category: 'Electronics',
    inStock: true,
    badge: {
      text: 'Bestseller',
      type: 'bestseller'
    },
    colors: ['#000000', '#C0C0C0', '#1E3A8A', '#991B1B']
  },
  {
    id: '2',
    title: 'Smart Watch Pro Series 8',
    description: 'Advanced fitness tracking, heart rate monitoring, GPS, and water resistance. Compatible with iOS and Android.',
    price: 399.99,
    originalPrice: 499.99,
    currency: '$',
    image: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    rating: {
      average: 4.6,
      count: 1523
    },
    category: 'Wearables',
    inStock: true,
    badge: {
      text: 'New Arrival',
      type: 'new'
    },
    colors: ['#000000', '#FFFFFF', '#FF6B6B', '#4ECDC4']
  },
  {
    id: '3',
    title: 'Ultra-Light Running Shoes',
    description: 'Breathable mesh upper with responsive cushioning. Perfect for long-distance runs and everyday training.',
    price: 129.99,
    originalPrice: 179.99,
    currency: '$',
    image: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    rating: {
      average: 4.7,
      count: 892
    },
    category: 'Footwear',
    inStock: true,
    badge: {
      text: '30% Off',
      type: 'sale'
    },
    colors: ['#000000', '#FFFFFF', '#3B82F6', '#10B981', '#F59E0B'],
    sizes: ['7', '8', '9', '10', '11', '12']
  },
  {
    id: '4',
    title: 'Designer Leather Backpack',
    description: 'Handcrafted genuine leather backpack with laptop compartment, multiple pockets, and adjustable straps.',
    price: 189.99,
    currency: '$',
    image: 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    rating: {
      average: 4.9,
      count: 456
    },
    category: 'Accessories',
    inStock: true,
    badge: {
      text: 'Limited Edition',
      type: 'limited'
    },
    colors: ['#8B4513', '#000000', '#4B5563']
  },
  {
    id: '5',
    title: 'Minimalist Desk Lamp',
    description: 'Modern LED desk lamp with adjustable brightness, USB charging port, and touch controls. Energy efficient.',
    price: 59.99,
    originalPrice: 89.99,
    currency: '$',
    image: 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    rating: {
      average: 4.5,
      count: 678
    },
    category: 'Home & Office',
    inStock: true,
    colors: ['#FFFFFF', '#000000', '#6B7280']
  },
  {
    id: '6',
    title: 'Portable Bluetooth Speaker',
    description: 'Waterproof wireless speaker with 360° sound, 20-hour battery, and built-in microphone for calls.',
    price: 79.99,
    originalPrice: 119.99,
    currency: '$',
    image: 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    rating: {
      average: 4.4,
      count: 1234
    },
    category: 'Electronics',
    inStock: true,
    badge: {
      text: 'Trending',
      type: 'trending'
    },
    colors: ['#EF4444', '#3B82F6', '#10B981', '#F59E0B', '#8B5CF6']
  },
  {
    id: '7',
    title: 'Organic Cotton T-Shirt',
    description: 'Super soft, sustainable organic cotton tee. Classic fit with modern style. Available in multiple colors.',
    price: 29.99,
    originalPrice: 44.99,
    currency: '$',
    image: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    rating: {
      average: 4.3,
      count: 2103
    },
    category: 'Clothing',
    inStock: true,
    badge: {
      text: 'Sale',
      type: 'sale'
    },
    colors: ['#FFFFFF', '#000000', '#1F2937', '#3B82F6', '#10B981', '#F59E0B'],
    sizes: ['XS', 'S', 'M', 'L', 'XL', 'XXL']
  },
  {
    id: '8',
    title: 'Stainless Steel Water Bottle',
    description: 'Insulated water bottle keeps drinks cold for 24h or hot for 12h. BPA-free, leak-proof, and eco-friendly.',
    price: 34.99,
    currency: '$',
    image: 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    rating: {
      average: 4.7,
      count: 987
    },
    category: 'Home & Kitchen',
    inStock: true,
    colors: ['#000000', '#FFFFFF', '#3B82F6', '#EC4899', '#10B981']
  },
  {
    id: '9',
    title: 'Wireless Charging Pad',
    description: 'Fast wireless charging for all Qi-enabled devices. Sleek design with LED indicator and overcharge protection.',
    price: 39.99,
    originalPrice: 59.99,
    currency: '$',
    image: 'https://images.unsplash.com/photo-1591290619762-f61b7eabef1e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    rating: {
      average: 4.2,
      count: 543
    },
    category: 'Electronics',
    inStock: true,
    colors: ['#000000', '#FFFFFF']
  },
  {
    id: '10',
    title: 'Premium Yoga Mat',
    description: 'Non-slip, eco-friendly yoga mat with extra cushioning. Includes carrying strap. Perfect for all yoga styles.',
    price: 49.99,
    currency: '$',
    image: 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    rating: {
      average: 4.6,
      count: 765
    },
    category: 'Fitness',
    inStock: true,
    badge: {
      text: 'Bestseller',
      type: 'bestseller'
    },
    colors: ['#EC4899', '#3B82F6', '#10B981', '#8B5CF6', '#000000']
  },
  {
    id: '11',
    title: 'Professional Camera Lens',
    description: 'High-quality 50mm f/1.8 lens for stunning portraits and low-light photography. Compatible with major camera brands.',
    price: 449.99,
    currency: '$',
    image: 'https://images.unsplash.com/photo-1606980624069-5dbb4c19c383?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    rating: {
      average: 4.9,
      count: 234
    },
    category: 'Photography',
    inStock: false,
    badge: {
      text: 'Limited Stock',
      type: 'limited'
    }
  },
  {
    id: '12',
    title: 'Ergonomic Office Chair',
    description: 'Premium mesh office chair with lumbar support, adjustable armrests, and tilt mechanism. Maximum comfort.',
    price: 299.99,
    originalPrice: 449.99,
    currency: '$',
    image: 'https://images.unsplash.com/photo-1580480055273-228ff5388ef8?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
    rating: {
      average: 4.8,
      count: 432
    },
    category: 'Furniture',
    inStock: true,
    badge: {
      text: '35% Off',
      type: 'sale'
    },
    colors: ['#000000', '#6B7280']
  }
]

export const getProductsByCategory = (category: string) => 
  sampleProducts.filter(p => p.category === category)

export const getBestsellingProducts = () => 
  sampleProducts.filter(p => p.badge?.type === 'bestseller')

export const getSaleProducts = () => 
  sampleProducts.filter(p => p.originalPrice && p.originalPrice > p.price)

export const getInStockProducts = () => 
  sampleProducts.filter(p => p.inStock !== false)

export const getProductById = (id: string) => 
  sampleProducts.find(p => p.id === id)
