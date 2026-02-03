# Test Failures Fixed

## Summary
Fixed multiple test failures identified in the e-commerce test suite. The main issues were:

1. **Expired card expiry years** - Tests were using `expiry_year: 2025` but we're in 2026, so cards were expired
2. **Discount code validation bug** - Using `db.func.now()` in Python comparison instead of `datetime.utcnow()`
3. **Product field name mismatch** - Tests checking `in_stock` but Product model returns `inStock` (camelCase)
4. **Missing discount code** - Test expected `SAVE20` discount code but it wasn't created in test setup
5. **Cart response key mismatch** - Tests expected `'discount'` key but cart returns `'discount_code'` and `'discount_amount'`

## Fixes Applied

### 1. Fixed Expired Card Years (`test_ecommerce_routes_coverage.py`)
**Problem**: Tests were hardcoding `expiry_year: 2025`, which is expired in 2026.

**Solution**: Updated all payment tests to use dynamic future year:
```python
future_year = datetime.now().year + 1
```

**Files Changed**:
- `tests/test_ecommerce_routes_coverage.py` - Updated 5 instances
- `tests/test_ecommerce_checkout_unittest.py` - Updated `_create_mock_payment_data()` default parameter

### 2. Fixed Discount Code Expiry Validation (`app/cart/routes.py`)
**Problem**: Line 176 was using `discount_code.expires_at < db.func.now()` which doesn't work in Python comparisons.

**Solution**: Changed to use `datetime.utcnow()`:
```python
# Before:
if discount_code.expires_at and discount_code.expires_at < db.func.now():

# After:
if discount_code.expires_at and discount_code.expires_at < datetime.utcnow():
```

**Files Changed**:
- `app/cart/routes.py` - Added `from datetime import datetime` import and fixed comparison

### 3. Fixed Product In-Stock Filter Test (`test_ecommerce_routes_coverage.py`)
**Problem**: Test was checking `p.get('in_stock', False)` but Product model's `to_dict()` returns `inStock` (camelCase).

**Solution**: Updated test to check correct field name:
```python
# Before:
self.assertTrue(all(p.get('in_stock', False) for p in response.json['products']))

# After:
products = response.json['products']
if products:
    self.assertTrue(all(p.get('inStock', False) for p in products))
```

**Files Changed**:
- `tests/test_ecommerce_routes_coverage.py::TestProductsRoutes::test_get_products_in_stock_only`

### 4. Fixed Discount Code Response Key (`test_ecommerce_checkout_unittest.py`)
**Problem**: Test expected `'discount'` key but cart returns `'discount_code'` and `'discount_amount'`.

**Solution**: Updated test assertion:
```python
# Before:
self.assertIn('discount', cart)

# After:
self.assertIn('discount_code', cart)
self.assertIn('discount_amount', cart)
```

**Files Changed**:
- `tests/test_ecommerce_checkout_unittest.py::TestDiscountCodePositive::test_apply_valid_discount_code`

### 5. Added Missing SAVE20 Discount Code (`test_ecommerce_checkout_unittest.py`)
**Problem**: Test `test_replace_existing_discount_code` expected `SAVE20` discount code but it wasn't created in test setup.

**Solution**: Added SAVE20 discount code creation in `_create_discount_codes_in_db()`:
```python
# Create SAVE20 discount code for test_replace_existing_discount_code
save20 = DiscountCode(
    code='SAVE20',
    discount_type='percentage',
    discount_percent=Decimal('20.00'),
    min_purchase=Decimal('0.00'),
    is_active=True
)
db.session.add(save20)
```

**Files Changed**:
- `tests/test_ecommerce_checkout_unittest.py::BaseEcommerceTestCase::_create_discount_codes_in_db()`

## Test Results

After fixes, the following tests now pass:
- ✅ `test_get_products_in_stock_only`
- ✅ `test_apply_expired_discount_code`
- ✅ `test_process_payment_valid`

## Remaining Issues

There are still other failing tests that need investigation:
- Payment processing tests that mock `app.services.payment_service.process_payment` (but actual implementation uses `process_payment_mock` directly)
- Email notification tests that mock `app.services.email_service.send_email` (but email service may not be implemented)
- Order confirmation tests that may have similar mocking issues

## Next Steps

1. Review remaining failing tests to identify similar patterns
2. Fix payment service mocking to match actual implementation
3. Fix email service mocking or implement actual email service
4. Run full test suite to verify all fixes
5. Increase test coverage to 80% as requested
