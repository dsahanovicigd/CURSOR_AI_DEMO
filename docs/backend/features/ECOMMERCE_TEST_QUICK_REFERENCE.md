# E-Commerce Checkout Tests - Quick Reference

## Quick Start

```bash
# Run all e-commerce tests
python -m unittest tests.test_ecommerce_checkout_unittest -v

# Run specific category
python -m unittest tests.test_ecommerce_checkout_unittest.TestCartManagementPositive -v

# Run with coverage
coverage run -m unittest tests.test_ecommerce_checkout_unittest
coverage report
```

## Test Statistics

- **Total Test Cases**: 80+
- **Test Classes**: 15
- **Categories**: Cart, Discount, Payment, Order, Email, Integration

## Test Class Overview

| Class | Purpose | Test Count |
|-------|---------|------------|
| `TestCartManagementPositive` | Successful cart operations | 6 |
| `TestCartManagementNegative` | Cart error handling | 7 |
| `TestCartManagementEdgeCases` | Cart edge cases | 3 |
| `TestCartManagementSecurity` | Cart security | 2 |
| `TestDiscountCodePositive` | Successful discount application | 4 |
| `TestDiscountCodeNegative` | Discount error handling | 5 |
| `TestDiscountCodeEdgeCases` | Discount edge cases | 3 |
| `TestDiscountCodeSecurity` | Discount security | 2 |
| `TestPaymentProcessingPositive` | Successful payments | 3 |
| `TestPaymentProcessingNegative` | Payment errors | 6 |
| `TestPaymentProcessingEdgeCases` | Payment edge cases | 2 |
| `TestPaymentProcessingSecurity` | Payment security | 5 |
| `TestOrderConfirmationPositive` | Order creation | 4 |
| `TestOrderConfirmationNegative` | Order errors | 3 |
| `TestOrderConfirmationEdgeCases` | Order edge cases | 1 |
| `TestEmailNotificationsPositive` | Email sending | 2 |
| `TestEmailNotificationsNegative` | Email errors | 1 |
| `TestEmailNotificationsSecurity` | Email security | 1 |
| `TestCheckoutIntegration` | End-to-end flows | 2 |

## Key Test Scenarios

### Cart Management
- ✅ Add/update/remove items
- ❌ Invalid products, quantities
- 🔍 Duplicate products, zero quantities
- 🔒 User isolation, SQL injection

### Discount Codes
- ✅ Apply valid codes
- ❌ Invalid/expired codes
- 🔍 Max discount limits
- 🔒 Code validation, XSS prevention

### Payment Processing
- ✅ Valid payments
- ❌ Invalid cards, expired cards
- 🔍 Edge cases
- 🔒 PCI compliance, data security

### Order Confirmation
- ✅ Order creation
- ❌ Unauthorized access
- 🔍 Discount preservation

### Email Notifications
- ✅ Confirmation emails
- ❌ Email failures
- 🔒 No sensitive data in emails

## Common Commands

```bash
# Run all tests
python -m unittest tests.test_ecommerce_checkout_unittest

# Run specific test class
python -m unittest tests.test_ecommerce_checkout_unittest.TestCartManagementPositive

# Run specific test method
python -m unittest tests.test_ecommerce_checkout_unittest.TestCartManagementPositive.test_add_item_to_cart

# Run with verbose output
python -m unittest tests.test_ecommerce_checkout_unittest -v

# Run with coverage
coverage run -m unittest tests.test_ecommerce_checkout_unittest
coverage html
```

## Expected API Endpoints

```
POST   /api/cart/items
GET    /api/cart
PUT    /api/cart/items/{id}
DELETE /api/cart/items/{id}
DELETE /api/cart
POST   /api/cart/apply-discount
DELETE /api/cart/discount
POST   /api/checkout/process-payment
GET    /api/orders
GET    /api/orders/{id}
```

## Mock Data Usage

```python
from tests.ecommerce_test_helpers import EcommerceMockDataGenerator

# Generate test data
product = EcommerceMockDataGenerator.generate_product_data()
cart_item = EcommerceMockDataGenerator.generate_cart_item_data(product_id=1)
discount = EcommerceMockDataGenerator.generate_discount_code_data()
payment = EcommerceMockDataGenerator.generate_payment_data()
shipping = EcommerceMockDataGenerator.generate_shipping_address()
```

## Security Checklist

- [x] Payment data not stored
- [x] SQL injection prevention
- [x] XSS prevention
- [x] Card validation (Luhn)
- [x] Amount tampering prevention
- [x] User isolation
- [x] Authentication required

## Test Data Examples

### Valid Test Card Numbers (Luhn-compliant)
- Visa: `4111111111111111`
- Mastercard: `5555555555554444`
- Amex: `378282246310005`

### Invalid Test Cases
- Empty cart checkout
- Out of stock products
- Expired discount codes
- Invalid card numbers
- Missing required fields
