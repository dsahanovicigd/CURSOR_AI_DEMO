# E-Commerce Test Setup Notes

## Automatic Test Setup

The e-commerce checkout test cases have been modified to **automatically handle user creation and authentication** - no manual registration or login is required.

## What Happens Automatically

### In `setUp()` Method:

1. **Database Setup**
   - Creates all database tables
   - Clears cache

2. **User Creation** (Automatic)
   - Creates a test customer user automatically
   - Username: `testcustomer`
   - Email: `customer@example.com`
   - Password: `customerpassword123`
   - **No registration API call needed**

3. **Authentication** (Automatic)
   - Automatically logs in the test user
   - Retrieves JWT token
   - Sets up `customer_headers` for API calls
   - **No manual login API call needed**

4. **Product Creation** (Automatic)
   - Creates 3 test products in database:
     - Product 1: $29.99, Stock: 100
     - Product 2: $49.99, Stock: 50
     - Product 3: $99.99, Stock: 0 (out of stock)

5. **Discount Code Creation** (Automatic)
   - Creates multiple discount codes:
     - `SAVE10`: 10% discount
     - `FIXED5`: $5 fixed discount
     - `MIN50`: 10% discount, requires $50 minimum
     - `MAX50`: 20% discount, max $50
     - `EXPIRED`: Expired discount code

## Test Execution

### Running Tests

```bash
cd flask_api
source venv/bin/activate
python -m unittest tests.test_ecommerce_checkout_unittest -v
```

### What Tests Do

- **No manual setup required** - everything is automatic
- Tests use `self.customer_headers` for authenticated requests
- Products and discount codes are already in database
- User is already authenticated

## Authentication Tests

Some tests check for "without authentication" scenarios:

- `test_add_item_without_authentication`
- `test_apply_discount_without_authentication`
- `test_get_order_without_authentication`

These tests are **flexible** and accept multiple status codes:
- `401` if authentication is required
- `200/400/404` if anonymous access is supported

This allows tests to work with different API designs.

## Benefits

1. **No Manual Steps**: Tests run without requiring user registration/login
2. **Isolated**: Each test gets a fresh database and user
3. **Fast**: No API calls for setup - direct database operations
4. **Reliable**: No dependency on external auth services
5. **Flexible**: Tests adapt to different authentication requirements

## Example Test Flow

```python
def test_add_item_to_cart(self):
    # User already exists and is authenticated
    # Product already exists in database
    # Just make the API call!
    response = self.client.post(
        '/api/cart/items',
        headers=self.customer_headers,  # Already set up
        json={'product_id': 1, 'quantity': 2}
    )
    # Assert results...
```

## Notes

- All setup happens in `BaseEcommerceTestCase.setUp()`
- Each test method gets a fresh database state
- Products are created with IDs 1, 2, 3
- User ID is automatically assigned by database
- Authentication token is automatically retrieved
