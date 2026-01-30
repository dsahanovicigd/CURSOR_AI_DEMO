import { useState } from 'react'
import { checkoutAPI, cartAPI } from '../../services/api'

interface CartItem {
  id: number;
  product_id: number;
  quantity: number;
  subtotal?: number;
  product?: {
    id: number;
    title: string;
    price: string | number;
    image?: string;
  };
}

interface Cart {
  id: number;
  items: CartItem[];
  total: number;
  subtotal?: number;
  item_count?: number;
  discount_code?: string;
  discount_amount?: number;
}

interface Order {
  id: number;
  order_number: string;
  total: number;
  status: string;
}

interface CheckoutModalProps {
  cart: Cart | null
  onClose: () => void
  onOrderComplete: () => void
  onCartUpdate?: () => void
}

const CheckoutModal = ({ cart, onClose, onOrderComplete, onCartUpdate }: CheckoutModalProps) => {
  const [step, setStep] = useState<'cart' | 'checkout' | 'success'>('cart')
  const [discountCode, setDiscountCode] = useState('')
  const [applyingDiscount, setApplyingDiscount] = useState(false)
  const [paymentData, setPaymentData] = useState({
    card_number: '',
    cardholder_name: '',
    expiry_month: '',
    expiry_year: '',
    cvv: '',
  })
  const [shippingAddress, setShippingAddress] = useState({
    full_name: '',
    street: '',
    city: '',
    state: '',
    zip: '',
    country: 'US',
    phone: '',
  })
  const [processing, setProcessing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [order, setOrder] = useState<Order | null>(null)
  const [removingItem, setRemovingItem] = useState<number | null>(null)
  
  // Safely get cart items with error handling
  let cartItems: CartItem[] = []
  let isEmpty = true
  
  try {
    cartItems = cart?.items || []
    isEmpty = !cart || !Array.isArray(cartItems) || cartItems.length === 0
    console.log('CheckoutModal rendered with cart:', cart)
    console.log('Cart items:', cartItems)
    console.log('Is empty:', isEmpty)
  } catch (err) {
    console.error('Error processing cart data:', err)
    cartItems = []
    isEmpty = true
  }

  const handleApplyDiscount = async () => {
    if (!discountCode.trim()) return
    
    setApplyingDiscount(true)
    setError(null)
    try {
      const response = await cartAPI.applyDiscount(discountCode.trim())
      // Update cart from response
      if (response.cart) {
        // Cart will be updated via parent component's loadCart
        // For now, we can update local state if needed
        console.log('Discount applied, updated cart:', response.cart)
      }
    } catch (err) {
      const error = err as Error;
      setError(error.message || 'Failed to apply discount code')
    } finally {
      setApplyingDiscount(false)
    }
  }

  const handleRemoveDiscount = async () => {
    try {
      const response = await cartAPI.removeDiscount()
      if (response.cart) {
        console.log('Discount removed, updated cart:', response.cart)
      }
    } catch (err) {
      const error = err as Error;
      console.error('Failed to remove discount:', err)
      setError(error.message || 'Failed to remove discount code')
    }
  }

  const handleRemoveItem = async (itemId: number) => {
    try {
      setRemovingItem(itemId)
      setError(null)
      console.log('Removing item from cart:', itemId)
      const response = await cartAPI.removeItem(itemId)
      console.log('Remove item response:', response)
      
      // Update cart from response - trigger parent reload
      if (response.cart) {
        // Dispatch custom event to notify parent component
        window.dispatchEvent(new CustomEvent('cartUpdated'))
        // Also call callback if provided
        if (onCartUpdate) {
          onCartUpdate()
        }
      }
    } catch (err) {
      const error = err as Error;
      console.error('Error removing item:', err)
      setError(error.message || 'Failed to remove item from cart')
    } finally {
      setRemovingItem(null)
    }
  }

  const handleCheckout = () => {
    setStep('checkout')
  }

  const handlePayment = async () => {
    // Validate form
    if (!paymentData.card_number || !paymentData.cardholder_name || 
        !paymentData.expiry_month || !paymentData.expiry_year || !paymentData.cvv) {
      setError('Please fill in all payment fields')
      return
    }

    if (!shippingAddress.full_name || !shippingAddress.street || 
        !shippingAddress.city || !shippingAddress.state || !shippingAddress.zip) {
      setError('Please fill in all shipping address fields')
      return
    }

    setProcessing(true)
    setError(null)

    try {
      const response = await checkoutAPI.processPayment(
        {
          ...paymentData,
          expiry_month: parseInt(paymentData.expiry_month),
          expiry_year: parseInt(paymentData.expiry_year),
        },
        shippingAddress
      )
      
      setOrder(response.order)
      setStep('success')
    } catch (err) {
      const error = err as Error;
      setError(error.message || 'Payment processing failed')
    } finally {
      setProcessing(false)
    }
  }

  // Error boundary - if cart is null or empty, show empty message
  if (!cart || isEmpty) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" onClick={onClose}>
        <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4" onClick={(e) => e.stopPropagation()}>
          <h2 className="text-2xl font-bold mb-4">Cart is Empty</h2>
          <p className="text-gray-600 mb-4">
            {!cart ? 'Cart data is loading...' : 'Add some products to your cart first!'}
          </p>
          <button
            onClick={onClose}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
          >
            Close
          </button>
        </div>
      </div>
    )
  }

  // Ensure cart exists before rendering
  if (!cart) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" onClick={onClose}>
        <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4" onClick={(e) => e.stopPropagation()}>
          <h2 className="text-2xl font-bold mb-4">Loading Cart...</h2>
          <p className="text-gray-600 mb-4">Please wait while we load your cart.</p>
          <button
            onClick={onClose}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
          >
            Close
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 p-4 flex justify-between items-center">
          <h2 className="text-2xl font-bold">
            {step === 'cart' && 'Shopping Cart'}
            {step === 'checkout' && 'Checkout'}
            {step === 'success' && 'Order Confirmed!'}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {step === 'cart' && (
            <>
              {/* Cart Items */}
              <div className="space-y-4 mb-6">
                {cartItems.length > 0 ? (
                  cartItems.map((item: CartItem, index: number) => {
                    try {
                      const itemId = item.id || item.product_id || `item-${index}`
                      const product = item.product || {}
                      const price = parseFloat(product.price || item.subtotal || 0)
                      const quantity = item.quantity || 1
                      const subtotal = parseFloat(item.subtotal || price * quantity)
                      
                      return (
                        <div key={itemId} className="flex items-center gap-4 border-b pb-4">
                          <img
                            src={product.image || 'https://via.placeholder.com/100'}
                            alt={product.title || 'Product'}
                            className="w-20 h-20 object-cover rounded"
                            onError={(e) => {
                              (e.target as HTMLImageElement).src = 'https://via.placeholder.com/100'
                            }}
                          />
                          <div className="flex-1">
                            <h3 className="font-semibold">{product.title || 'Product'}</h3>
                            <p className="text-gray-600 text-sm">
                              ${price.toFixed(2)} × {quantity}
                            </p>
                          </div>
                          <div className="flex items-center gap-4">
                            <div className="text-right">
                              <p className="font-bold">${subtotal.toFixed(2)}</p>
                            </div>
                            <button
                              onClick={() => handleRemoveItem(item.id)}
                              disabled={removingItem === item.id}
                              className="text-red-600 hover:text-red-700 disabled:opacity-50 p-2 rounded hover:bg-red-50 transition-colors"
                              title="Remove item from cart"
                              aria-label={`Remove ${product.title || 'item'} from cart`}
                            >
                              {removingItem === item.id ? (
                                <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                              ) : (
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                </svg>
                              )}
                            </button>
                          </div>
                        </div>
                      )
                    } catch (err) {
                      console.error('Error rendering cart item:', err, item)
                      return (
                        <div key={`error-${index}`} className="text-red-500 text-sm">
                          Error loading item
                        </div>
                      )
                    }
                  })
                ) : (
                  <div className="text-center py-8 text-gray-500">
                    <p>No items in cart</p>
                  </div>
                )}
              </div>

              {/* Discount Code */}
              <div className="mb-6">
                <div className="flex gap-2">
                  <input
                    type="text"
                    placeholder="Discount Code"
                    value={discountCode}
                    onChange={(e) => setDiscountCode(e.target.value)}
                    className="flex-1 px-4 py-2 border rounded-lg"
                  />
                  <button
                    onClick={handleApplyDiscount}
                    disabled={applyingDiscount || !discountCode.trim()}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                  >
                    {applyingDiscount ? 'Applying...' : 'Apply'}
                  </button>
                </div>
                {cart?.discount_code && (
                  <div className="mt-2 flex items-center gap-2">
                    <span className="text-green-600">Discount applied: {cart.discount_code}</span>
                    <button
                      onClick={handleRemoveDiscount}
                      className="text-red-600 hover:text-red-700 text-sm"
                    >
                      Remove
                    </button>
                  </div>
                )}
                {error && <p className="text-red-600 text-sm mt-2">{error}</p>}
              </div>

              {/* Totals */}
              <div className="border-t pt-4 mb-6">
                <div className="flex justify-between mb-2">
                  <span>Subtotal:</span>
                  <span>${(cart.subtotal || 0).toFixed(2)}</span>
                </div>
                {(cart.discount_amount || 0) > 0 && (
                  <div className="flex justify-between mb-2 text-green-600">
                    <span>Discount:</span>
                    <span>-${(cart.discount_amount || 0).toFixed(2)}</span>
                  </div>
                )}
                <div className="flex justify-between font-bold text-xl">
                  <span>Total:</span>
                  <span>${(cart.total || cart.subtotal || 0).toFixed(2)}</span>
                </div>
              </div>

              <button
                onClick={handleCheckout}
                className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 font-semibold"
              >
                Proceed to Checkout
              </button>
            </>
          )}

          {step === 'checkout' && (
            <>
              {/* Order Summary */}
              <div className="mb-6 p-4 bg-gray-50 rounded-lg">
                <h3 className="font-bold mb-2">Order Summary</h3>
                <div className="space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span>Subtotal:</span>
                    <span>${(cart.subtotal || 0).toFixed(2)}</span>
                  </div>
                  {(cart.discount_amount || 0) > 0 && (
                    <div className="flex justify-between text-green-600">
                      <span>Discount:</span>
                      <span>-${(cart.discount_amount || 0).toFixed(2)}</span>
                    </div>
                  )}
                  <div className="flex justify-between font-bold">
                    <span>Total:</span>
                    <span>${(cart.total || cart.subtotal || 0).toFixed(2)}</span>
                  </div>
                </div>
              </div>

              {/* Shipping Address */}
              <div className="mb-6">
                <h3 className="font-bold mb-4">Shipping Address</h3>
                <div className="grid grid-cols-2 gap-4">
                  <input
                    type="text"
                    placeholder="Full Name"
                    value={shippingAddress.full_name}
                    onChange={(e) => setShippingAddress({ ...shippingAddress, full_name: e.target.value })}
                    className="col-span-2 px-4 py-2 border rounded-lg"
                  />
                  <input
                    type="text"
                    placeholder="Street Address"
                    value={shippingAddress.street}
                    onChange={(e) => setShippingAddress({ ...shippingAddress, street: e.target.value })}
                    className="col-span-2 px-4 py-2 border rounded-lg"
                  />
                  <input
                    type="text"
                    placeholder="City"
                    value={shippingAddress.city}
                    onChange={(e) => setShippingAddress({ ...shippingAddress, city: e.target.value })}
                    className="px-4 py-2 border rounded-lg"
                  />
                  <input
                    type="text"
                    placeholder="State"
                    value={shippingAddress.state}
                    onChange={(e) => setShippingAddress({ ...shippingAddress, state: e.target.value })}
                    className="px-4 py-2 border rounded-lg"
                  />
                  <input
                    type="text"
                    placeholder="ZIP Code"
                    value={shippingAddress.zip}
                    onChange={(e) => setShippingAddress({ ...shippingAddress, zip: e.target.value })}
                    className="px-4 py-2 border rounded-lg"
                  />
                  <input
                    type="text"
                    placeholder="Phone (optional)"
                    value={shippingAddress.phone}
                    onChange={(e) => setShippingAddress({ ...shippingAddress, phone: e.target.value })}
                    className="px-4 py-2 border rounded-lg"
                  />
                </div>
              </div>

              {/* Payment Information */}
              <div className="mb-6">
                <h3 className="font-bold mb-4">Payment Information</h3>
                <div className="space-y-4">
                  <input
                    type="text"
                    placeholder="Card Number"
                    value={paymentData.card_number}
                    onChange={(e) => setPaymentData({ ...paymentData, card_number: e.target.value })}
                    className="w-full px-4 py-2 border rounded-lg"
                    maxLength={19}
                  />
                  <input
                    type="text"
                    placeholder="Cardholder Name"
                    value={paymentData.cardholder_name}
                    onChange={(e) => setPaymentData({ ...paymentData, cardholder_name: e.target.value })}
                    className="w-full px-4 py-2 border rounded-lg"
                  />
                  <div className="grid grid-cols-4 gap-4">
                    <input
                      type="text"
                      placeholder="MM"
                      value={paymentData.expiry_month}
                      onChange={(e) => setPaymentData({ ...paymentData, expiry_month: e.target.value })}
                      className="px-4 py-2 border rounded-lg"
                      maxLength={2}
                    />
                    <input
                      type="text"
                      placeholder="YYYY"
                      value={paymentData.expiry_year}
                      onChange={(e) => setPaymentData({ ...paymentData, expiry_year: e.target.value })}
                      className="px-4 py-2 border rounded-lg"
                      maxLength={4}
                    />
                    <input
                      type="text"
                      placeholder="CVV"
                      value={paymentData.cvv}
                      onChange={(e) => setPaymentData({ ...paymentData, cvv: e.target.value })}
                      className="col-span-2 px-4 py-2 border rounded-lg"
                      maxLength={4}
                    />
                  </div>
                </div>
              </div>

              {error && (
                <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">
                  {error}
                </div>
              )}

              <div className="flex gap-4">
                <button
                  onClick={() => setStep('cart')}
                  className="flex-1 px-4 py-2 border rounded-lg hover:bg-gray-50"
                  disabled={processing}
                >
                  Back to Cart
                </button>
                <button
                  onClick={handlePayment}
                  disabled={processing}
                  className="flex-1 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                  {processing ? 'Processing...' : 'Complete Order'}
                </button>
              </div>
            </>
          )}

          {step === 'success' && order && (
            <div className="text-center">
              <div className="text-6xl mb-4">✅</div>
              <h3 className="text-2xl font-bold mb-2">Order Confirmed!</h3>
              <p className="text-gray-600 mb-4">
                Your order number is: <strong>{order.order_number}</strong>
              </p>
              <p className="text-gray-600 mb-6">
                A confirmation email has been sent to your email address.
              </p>
              <button
                onClick={() => {
                  onOrderComplete()
                  onClose()
                }}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
              >
                Continue Shopping
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default CheckoutModal
