# E-Commerce Checkout Process - Comprehensive Test Cases

## Overview

This document describes comprehensive test cases for an e-commerce checkout process, covering cart management, discount codes, payment processing, order confirmation, and email notifications.

**Test File**: `tests/test_ecommerce_checkout_unittest.py`

**Total Test Cases**: 80+ test scenarios

---

## Test Categories

### 1. Cart Management (20+ tests)
- Adding items to cart
- Updating quantities
- Removing items
- Clearing cart
- Cart calculations

### 2. Discount Code Application (15+ tests)
- Applying valid codes
- Percentage discounts
- Fixed amount discounts
- Minimum purchase requirements
- Maximum discount limits

### 3. Payment Processing (20+ tests)
- Valid payment processing
- Card validation
- Payment gateway integration
- Error handling
- Security validation

### 4. Order Confirmation (10+ tests)
- Order creation
- Order details
- Order status
- Order history

### 5. Email Notifications (5+ tests)
- Order confirmation emails
- Email content validation
- Error handling

### 6. Integration Tests (5+ tests)
- Complete checkout flow
- End-to-end scenarios

---

## Test Coverage Breakdown

### Cart Management

#### Positive Test Cases ✅
- Add single item to cart
- Add multiple different items
- Update item quantity
- Get cart contents
- Remove item from cart
- Clear entire cart

#### Negative Test Cases ❌
- Add item without authentication
- Add non-existent product
- Add out of stock product
- Add item with invalid quantity (zero/negative)
- Add quantity exceeding stock
- Update/remove non-existent cart item

#### Edge Cases 🔍
- Add same product multiple times (should increase quantity)
- Update quantity to zero (should remove item)
- Cart calculations with multiple items
- Large quantities
- Decimal quantities (if supported)

#### Security Test Cases 🔒
- Cart isolation between users
- SQL injection in product ID
- Authorization checks

---

### Discount Code Application

#### Positive Test Cases ✅
- Apply valid percentage discount
- Apply valid fixed amount discount
- Remove applied discount
- Replace existing discount

#### Negative Test Cases ❌
- Apply invalid/non-existent code
- Apply expired code
- Apply code below minimum purchase
- Apply discount to empty cart
- Apply without authentication

#### Edge Cases 🔍
- Discount exceeds maximum limit (should cap)
- Discount makes total zero/negative (should prevent)
- Replace existing discount code
- Multiple discount attempts

#### Security Test Cases 🔒
- SQL injection in discount code
- XSS in discount code
- Code validation

---

### Payment Processing

#### Positive Test Cases ✅
- Process payment with valid card
- Process payment with discount applied
- Payment creates order
- Payment includes shipping address

#### Negative Test Cases ❌
- Process payment with empty cart
- Invalid card number
- Expired card
- Invalid CVV
- Missing shipping address
- Payment gateway failure

#### Edge Cases 🔍
- Missing optional payment fields
- Special characters in cardholder name
- Different card types (Visa, Mastercard, Amex)
- Payment amount validation

#### Security Test Cases 🔒
- Payment data not stored in plaintext
- SQL injection in payment fields
- XSS in shipping address
- Luhn algorithm validation
- Payment amount tampering prevention
- PCI compliance (no full card storage)

---

### Order Confirmation

#### Positive Test Cases ✅
- Order confirmed after payment
- Order contains all cart items
- Order includes shipping address
- Order includes payment details
- Order preserves discount code

#### Negative Test Cases ❌
- Get order without authentication
- Get non-existent order
- Get another user's order (should be forbidden)

#### Edge Cases 🔍
- Order with discount applied
- Order with multiple items
- Order status transitions

---

### Email Notifications

#### Positive Test Cases ✅
- Send order confirmation email
- Email contains order details
- Email sent to correct recipient

#### Negative Test Cases ❌
- Order created even if email fails
- Email service unavailable

#### Security Test Cases 🔒
- Email doesn't contain payment details
- Email doesn't contain full card numbers
- Email doesn't contain CVV

---

## Test Data Examples

### Valid Cart Item

```json
{
  "product_id": 1,
  "quantity": 2
}
```

### Valid Discount Code

```json
{
  "code": "SAVE10",
  "discount_percent": 10,
  "min_purchase": 50.00,
  "max_discount": 25.00,
  "expires_at": "2025-12-31T23:59:59",
  "is_active": true
}
```

### Valid Payment Data

```json
{
  "card_number": "4111111111111111",
  "cardholder_name": "John Doe",
  "expiry_month": 12,
  "expiry_year": 2025,
  "cvv": "123",
  "billing_address": {
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip": "10001",
    "country": "US"
  }
}
```

### Valid Shipping Address

```json
{
  "full_name": "John Doe",
  "street": "456 Shipping Ave",
  "city": "Los Angeles",
  "state": "CA",
  "zip": "90001",
  "country": "US",
  "phone": "+1234567890"
}
```

---

## Expected API Endpoints

### Cart Endpoints

```
POST   /api/cart/items              - Add item to cart
GET    /api/cart                    - Get cart contents
PUT    /api/cart/items/{item_id}    - Update cart item
DELETE /api/cart/items/{item_id}    - Remove cart item
DELETE /api/cart                    - Clear cart
POST   /api/cart/apply-discount     - Apply discount code
DELETE /api/cart/discount           - Remove discount code
```

### Checkout Endpoints

```
POST   /api/checkout/process-payment - Process payment and create order
GET    /api/orders                  - Get user's orders
GET    /api/orders/{order_id}       - Get order details
```

---

## Security Requirements

### Payment Data Security

1. **Never store full card numbers** - Only store last 4 digits
2. **Never store CVV** - CVV should never be stored
3. **Use payment gateway** - Process payments through secure gateway (Stripe, PayPal, etc.)
4. **PCI Compliance** - Follow PCI DSS requirements
5. **Encryption** - Encrypt sensitive data in transit (HTTPS)
6. **Tokenization** - Use payment tokens instead of card data

### Input Validation

1. **Card Number Validation** - Use Luhn algorithm
2. **CVV Validation** - 3 digits (4 for Amex)
3. **Expiry Validation** - Check expiry date
4. **Amount Validation** - Prevent tampering
5. **SQL Injection Prevention** - Parameterized queries
6. **XSS Prevention** - Sanitize user input

### Authorization

1. **Cart Isolation** - Users can only access their own cart
2. **Order Access** - Users can only view their own orders
3. **Authentication Required** - All checkout operations require auth

---

## Test Execution

### Run All E-Commerce Tests

```bash
cd flask_api
source venv/bin/activate
python -m unittest tests.test_ecommerce_checkout_unittest -v
```

### Run Specific Test Category

```bash
# Run only cart management tests
python -m unittest tests.test_ecommerce_checkout_unittest.TestCartManagementPositive -v

# Run only payment processing tests
python -m unittest tests.test_ecommerce_checkout_unittest.TestPaymentProcessingPositive -v
```

### Run with Coverage

```bash
coverage run -m unittest tests.test_ecommerce_checkout_unittest
coverage report
coverage html
```

---

## Implementation Notes

### Required Models

These tests assume the following models exist:

1. **Product** - Product catalog
2. **Cart** - Shopping cart
3. **CartItem** - Items in cart
4. **DiscountCode** - Discount codes
5. **Order** - Order records
6. **OrderItem** - Order line items
7. **Payment** - Payment transactions

### Required Services

1. **PaymentService** - Payment gateway integration
2. **EmailService** - Email notification service
3. **InventoryService** - Stock management

### Mock Services

Tests use `unittest.mock` to mock:
- Payment gateway responses
- Email service calls
- External API calls

---

## Test Scenarios Summary

### Complete Checkout Flow

1. **Add Items to Cart**
   - User adds products to cart
   - Cart calculates subtotal

2. **Apply Discount Code**
   - User applies valid discount code
   - Cart recalculates with discount

3. **Enter Shipping Address**
   - User provides shipping information
   - Address validated

4. **Process Payment**
   - User enters payment details
   - Payment validated (Luhn, expiry, CVV)
   - Payment processed through gateway

5. **Order Confirmation**
   - Order created with all details
   - Order status set to "confirmed"
   - Stock levels updated

6. **Email Notification**
   - Confirmation email sent
   - Email contains order details
   - Cart cleared

---

## Error Handling

### Payment Failures

- **Insufficient Funds** - Return 402 Payment Required
- **Invalid Card** - Return 400 Bad Request
- **Gateway Error** - Return 500 Internal Server Error
- **Network Error** - Retry logic or return error

### Cart Errors

- **Empty Cart** - Return 400 Bad Request
- **Out of Stock** - Return 400 Bad Request
- **Invalid Quantity** - Return 400 Bad Request

### Discount Errors

- **Invalid Code** - Return 400 Bad Request
- **Expired Code** - Return 400 Bad Request
- **Minimum Not Met** - Return 400 Bad Request

---

## Best Practices

1. **Test Isolation** - Each test is independent
2. **Mock External Services** - Don't call real payment gateways
3. **Use Test Cards** - Use test card numbers (4111...)
4. **Validate Security** - Always test security scenarios
5. **Edge Cases** - Test boundary conditions
6. **Error Handling** - Test all error scenarios

---

## Future Enhancements

- [ ] Add tests for refund processing
- [ ] Add tests for order cancellation
- [ ] Add tests for shipping tracking
- [ ] Add tests for order status updates
- [ ] Add tests for inventory management
- [ ] Add tests for multiple payment methods
- [ ] Add tests for subscription/recurring payments
- [ ] Add performance/load tests

---

## References

- **Test File**: `tests/test_ecommerce_checkout_unittest.py`
- **Helper Utilities**: `tests/ecommerce_test_helpers.py`
- **Payment Standards**: PCI DSS Compliance
- **Card Validation**: Luhn Algorithm
