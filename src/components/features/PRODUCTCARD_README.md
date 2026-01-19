# ProductCard Component

A comprehensive, accessible product card component for e-commerce applications.

## Features

### 🎨 Visual Design
- **Smooth Animations**: Image zoom on hover, smooth transitions
- **Product Badges**: Sale, New, Bestseller, Trending, Limited Edition
- **Discount Display**: Automatic percentage and savings calculation
- **Color Swatches**: Visual color variant selection
- **Responsive Images**: Optimized aspect ratio with lazy loading
- **Modern UI**: Clean, professional design with Tailwind CSS

### ⚡ Interactive Features
- **Add to Cart**: Button with loading animation and feedback
- **Favorite/Wishlist**: Heart icon toggle with state management
- **Quick View**: Hover-activated quick view button
- **Out of Stock**: Visual overlay for unavailable products
- **Star Rating**: Visual rating display with review count
- **Price Comparison**: Shows original price with strikethrough

### ♿ Accessibility
- **Semantic HTML**: Proper `<article>` structure
- **ARIA Labels**: Descriptive labels for all interactive elements
- **Keyboard Navigation**: Full keyboard support
- **Screen Reader**: Proper announcements and descriptions
- **Focus Indicators**: Clear visual focus states
- **Alt Text**: Descriptive image alternative text

## Usage

### Basic Usage

```tsx
import { ProductCard } from './components'
import { Product } from './types/product.types'

const product: Product = {
  id: '1',
  title: 'Wireless Headphones',
  description: 'Premium noise-cancelling headphones',
  price: 249.99,
  originalPrice: 349.99,
  image: 'https://example.com/image.jpg',
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
  colors: ['#000000', '#C0C0C0', '#1E3A8A']
}

function App() {
  const handleAddToCart = async (product: Product) => {
    console.log('Adding to cart:', product)
    // Add your cart logic here
  }

  return (
    <ProductCard
      product={product}
      onAddToCart={handleAddToCart}
    />
  )
}
```

### With All Features

```tsx
<ProductCard
  product={product}
  onAddToCart={(product) => console.log('Add to cart:', product)}
  onQuickView={(product) => console.log('Quick view:', product)}
  onFavorite={(product) => console.log('Toggle favorite:', product)}
  isFavorite={false}
  showQuickView={true}
  compact={false}
/>
```

### Compact Mode

```tsx
<ProductCard
  product={product}
  onAddToCart={handleAddToCart}
  compact={true}
/>
```

## Type Definitions

### Product Interface

```typescript
interface Product {
  id: string                    // Unique product identifier
  title: string                 // Product name
  description: string           // Product description
  price: number                 // Current price
  originalPrice?: number        // Original price (for discounts)
  currency?: string             // Currency symbol (default: '$')
  image: string                 // Product image URL
  rating: ProductRating         // Rating information
  category?: string             // Product category
  inStock?: boolean             // Stock status (default: true)
  badge?: ProductBadge          // Optional badge
  colors?: string[]             // Available colors (hex codes)
  sizes?: string[]              // Available sizes
}
```

### ProductRating Interface

```typescript
interface ProductRating {
  average: number   // Average rating (0-5)
  count: number     // Number of reviews
}
```

### ProductBadge Interface

```typescript
interface ProductBadge {
  text: string                                          // Badge text
  type: 'sale' | 'new' | 'trending' | 'limited' | 'bestseller'  // Badge type
}
```

### ProductCardProps Interface

```typescript
interface ProductCardProps {
  product: Product                    // Product data
  onAddToCart?: (product: Product) => void       // Add to cart callback
  onQuickView?: (product: Product) => void       // Quick view callback
  onFavorite?: (product: Product) => void        // Favorite toggle callback
  isFavorite?: boolean                // Is product favorited
  showQuickView?: boolean             // Show quick view button (default: true)
  compact?: boolean                   // Compact mode (default: false)
}
```

## Component Structure

### Main Components

#### ProductCard
- Main container with hover effects
- Manages internal state (hover, favorite, loading)
- Handles all user interactions

#### StarRating
- Displays star rating with half-star support
- Shows review count
- Supports multiple sizes (sm, md, lg)
- Fully accessible

## Styling

All styling uses Tailwind CSS utility classes:

### Color Schemes
- **Sale Badge**: Red (`bg-red-500`)
- **New Badge**: Blue (`bg-blue-500`)
- **Trending Badge**: Purple (`bg-purple-500`)
- **Limited Badge**: Orange (`bg-orange-500`)
- **Bestseller Badge**: Green (`bg-green-500`)

### Animations
- **Hover Scale**: Card lifts up on hover
- **Image Zoom**: Image scales 110% on hover
- **Button Transitions**: Smooth color and scale changes
- **Loading Spinner**: Rotating animation during add to cart

### Responsive Design
- **Mobile**: Single column, full-width buttons
- **Tablet**: 2 columns, optimized spacing
- **Desktop**: 3-4 columns, full features visible

## Features in Detail

### 1. Discount Calculation
Automatically calculates and displays:
- Discount percentage badge
- Original price (strikethrough)
- Amount saved

```tsx
// Shows "-30%" badge and "Save $100.00"
originalPrice: 349.99
price: 249.99
```

### 2. Stock Status
Visual feedback for out-of-stock items:
- Semi-transparent overlay
- "Out of Stock" label
- Disabled add to cart button

```tsx
inStock: false
```

### 3. Color Variants
Display up to 5 colors with overflow indicator:
- Circular color swatches
- Hover scale effect
- "+N more" indicator

```tsx
colors: ['#000000', '#FFFFFF', '#FF0000', '#00FF00', '#0000FF', '#FFFF00']
// Shows first 5 + "+1" indicator
```

### 4. Quick View
Hover-activated button:
- Appears from bottom on hover
- Smooth slide-up animation
- Centered positioning

### 5. Favorite Toggle
Heart icon with state:
- Hollow when not favorited
- Filled red when favorited
- Scale animation on click

### 6. Add to Cart Animation
Loading state feedback:
- Spinning loader icon
- "Adding..." text
- Disabled during operation
- 1-second animation

## Accessibility Features

### ARIA Attributes
```tsx
role="article"
aria-label="Product: Wireless Headphones"
aria-pressed={isFavorited}
```

### Keyboard Navigation
- Tab through all interactive elements
- Enter/Space to activate buttons
- Focus indicators on all buttons

### Screen Reader Support
```tsx
<span className="sr-only">Add to favorites</span>
aria-label="Rating: 4.8 out of 5 stars, 2847 reviews"
```

## Best Practices

### Image Optimization
- Use optimized images (WebP format recommended)
- Lazy loading enabled by default
- Aspect ratio maintained (square)
- Recommended size: 800x800px

### Performance
- Async add to cart operations
- Debounced hover effects
- Optimized re-renders with proper state management

### Error Handling
```tsx
const handleAddToCart = async (product: Product) => {
  try {
    await addToCartAPI(product)
    showSuccessMessage()
  } catch (error) {
    showErrorMessage()
  }
}
```

## Examples

### E-commerce Store
```tsx
<div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
  {products.map(product => (
    <ProductCard
      key={product.id}
      product={product}
      onAddToCart={handleAddToCart}
      isFavorite={favorites.includes(product.id)}
    />
  ))}
</div>
```

### Product Listing with Filters
```tsx
const filteredProducts = products.filter(p => 
  p.category === selectedCategory && p.inStock
)

<div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
  {filteredProducts.map(product => (
    <ProductCard
      key={product.id}
      product={product}
      onAddToCart={handleAddToCart}
      compact={true}
    />
  ))}
</div>
```

## Customization

### Change Badge Colors
Modify the `badgeColors` object in the component:

```tsx
const badgeColors = {
  sale: 'bg-pink-500',
  new: 'bg-teal-500',
  // ... etc
}
```

### Adjust Hover Effects
Change the scale and transition values:

```tsx
className="transform hover:-translate-y-2 transition-all duration-500"
```

### Custom Currency
```tsx
product={{
  ...productData,
  currency: '€'
}}
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome)

## Dependencies

- React 18+
- TypeScript
- Tailwind CSS
- StarRating component
- Button component

## Related Components

- **StarRating**: Rating display component
- **Button**: Reusable button component
- **ProductShowcase**: Demo page with filters and sorting
