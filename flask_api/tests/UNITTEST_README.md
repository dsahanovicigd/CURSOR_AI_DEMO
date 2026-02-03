# User Profile Management - Unittest Test Suite

## Overview

This test suite provides comprehensive unittest-based tests for user profile management features. The tests are organized using Python's `unittest` framework with proper setup/teardown methods, mock data generation, and categorized test classes.

## File Structure

```
tests/
├── test_user_profile_unittest.py  # Main unittest test file
├── test_helpers.py                # Helper utilities and mock data generators
├── conftest.py                    # Pytest fixtures (for pytest tests)
└── UNITTEST_README.md            # This file
```

## Key Features

- ✅ **Unittest Framework**: Uses Python's built-in unittest framework
- ✅ **Proper Fixtures**: setUp and tearDown methods for each test
- ✅ **Mock Data**: Comprehensive mock data generation utilities
- ✅ **Organized Categories**: Tests grouped by feature and test type
- ✅ **Security Focus**: Dedicated security test classes
- ✅ **Integration Tests**: End-to-end workflow testing

## Test Organization

### Test Categories

1. **Positive Tests** - Valid inputs and successful operations
2. **Negative Tests** - Invalid inputs and error handling
3. **Edge Cases** - Boundary conditions and unusual scenarios
4. **Security Tests** - Authorization, authentication, and security vulnerabilities

### Test Classes

#### User Registration
- `TestUserRegistrationPositive` - Successful registration scenarios
- `TestUserRegistrationNegative` - Registration failures
- `TestUserRegistrationEdgeCases` - Edge cases
- `TestUserRegistrationSecurity` - Security tests

#### Profile Updates
- `TestProfileUpdatesPositive` - Successful updates
- `TestProfileUpdatesNegative` - Update failures
- `TestProfileUpdatesEdgeCases` - Edge cases
- `TestProfileUpdatesSecurity` - Security tests

#### Password Changes
- `TestPasswordChangesPositive` - Successful password changes
- `TestPasswordChangesNegative` - Password change failures
- `TestPasswordChangesSecurity` - Security tests

#### Account Deletion
- `TestAccountDeletionPositive` - Successful deletions
- `TestAccountDeletionNegative` - Deletion failures
- `TestAccountDeletionSecurity` - Security tests

#### Integration
- `TestUserProfileIntegration` - End-to-end workflows

## Running Tests

### Run All Tests

```bash
cd flask_api
source venv/bin/activate
python -m unittest tests.test_user_profile_unittest -v
```

### Run Specific Test Class

```bash
# Run only registration tests
python -m unittest tests.test_user_profile_unittest.TestUserRegistrationPositive -v

# Run only security tests
python -m unittest tests.test_user_profile_unittest.TestUserRegistrationSecurity -v
```

### Run Specific Test Method

```bash
python -m unittest tests.test_user_profile_unittest.TestUserRegistrationPositive.test_register_user_with_minimal_fields -v
```

### Run with Test Suite

```bash
python tests/test_user_profile_unittest.py
```

### Run with Coverage

```bash
coverage run -m unittest tests.test_user_profile_unittest
coverage report
coverage html  # Generate HTML report
```

## Test Structure

### Base Test Case

All test classes inherit from `BaseTestCase` which provides:

- **setUp()**: Creates Flask app, test client, database, and test users
- **tearDown()**: Cleans up database and app context
- **Helper Methods**: User creation, authentication headers, etc.

```python
class BaseTestCase(unittest.TestCase):
    def setUp(self):
        # Initialize app, database, test users
        pass
    
    def tearDown(self):
        # Clean up database
        pass
```

### Example Test Method

```python
def test_register_user_with_minimal_fields(self):
    """Test: Register user with only required fields
    Expected: User created successfully with default role 'customer'
    """
    data = {
        'username': 'newuser123',
        'email': 'newuser@example.com',
        'password': 'SecurePass123'
    }
    response = self.client.post('/api/auth/register', json=data)
    
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json['username'], 'newuser123')
    self.assertNotIn('password', response.json)
```

## Mock Data Generation

### Using MockDataGenerator

```python
from tests.test_helpers import MockDataGenerator

# Generate user registration data
user_data = MockDataGenerator.generate_user_data(
    username='testuser',
    email='test@example.com'
)

# Generate invalid data for negative tests
invalid_data_list = MockDataGenerator.generate_invalid_user_data()

# Generate edge case data
edge_cases = MockDataGenerator.generate_edge_case_data()

# Generate security test data
security_data = MockDataGenerator.generate_security_test_data()
```

### Using TestUserFactory

```python
from tests.test_helpers import TestUserFactory

# Create test users
customer = TestUserFactory.create_customer(db_session)
admin = TestUserFactory.create_admin(db_session)
agent = TestUserFactory.create_agent(db_session)

# Create multiple users
users = TestUserFactory.create_multiple_users(db_session, count=10)
```

## Helper Utilities

### AssertionHelpers

```python
from tests.test_helpers import AssertionHelpers

# Assert user response structure
AssertionHelpers.assert_user_response_structure(response.json)

# Assert error response
AssertionHelpers.assert_error_response(
    response, 
    expected_status=400,
    error_keywords=['username', 'already exists']
)

# Assert password security
AssertionHelpers.assert_password_security(user, 'password123')
```

## Test Data Examples

### Valid Test Data

```python
valid_user_data = {
    'username': 'testuser123',
    'email': 'test@example.com',
    'password': 'SecurePass123',
    'first_name': 'John',
    'last_name': 'Doe',
    'role': 'customer'
}
```

### Invalid Test Data

```python
invalid_cases = [
    {'username': 'ab', 'email': 'test@example.com', 'password': 'SecurePass123'},  # Username too short
    {'username': 'testuser', 'email': 'notanemail', 'password': 'SecurePass123'},  # Invalid email
    {'username': 'testuser', 'email': 'test@example.com', 'password': 'short'}  # Password too short
]
```

### Edge Case Data

```python
edge_cases = {
    'unicode': {'first_name': 'José', 'last_name': 'Müller'},
    'special_chars': {'first_name': "O'Brien", 'last_name': 'van der Berg'},
    'max_length': {'username': 'a' * 80, 'password': 'A' * 1000}
}
```

## Common Assertions

### Status Code Assertions

```python
self.assertEqual(response.status_code, 201)  # Created
self.assertEqual(response.status_code, 200)  # OK
self.assertEqual(response.status_code, 204)  # No Content
self.assertEqual(response.status_code, 400)  # Bad Request
self.assertEqual(response.status_code, 401)  # Unauthorized
self.assertEqual(response.status_code, 403)  # Forbidden
self.assertEqual(response.status_code, 404)  # Not Found
```

### Response Data Assertions

```python
# Check field exists
self.assertIn('username', response.json)

# Check field value
self.assertEqual(response.json['username'], 'expected_value')

# Check field not present
self.assertNotIn('password', response.json)

# Check boolean
self.assertTrue(response.json['is_active'])

# Check list
self.assertEqual(len(response.json['expertise_areas']), 3)
```

### Database Assertions

```python
# Check user exists
user = User.query.get(user_id)
self.assertIsNotNone(user)

# Check user deleted
deleted_user = User.query.get(user_id)
self.assertIsNone(deleted_user)

# Check password
self.assertTrue(user.check_password('password123'))
```

## Test Execution Output

### Verbose Output

```
test_register_user_with_minimal_fields (tests.test_user_profile_unittest.TestUserRegistrationPositive) ... ok
test_register_user_with_all_fields (tests.test_user_profile_unittest.TestUserRegistrationPositive) ... ok
test_register_user_as_agent (tests.test_user_profile_unittest.TestUserRegistrationPositive) ... ok
...

----------------------------------------------------------------------
Ran 100+ tests in 15.234s

OK
```

### With Failures

```
test_register_user_duplicate_username (tests.test_user_profile_unittest.TestUserRegistrationNegative) ... FAIL

======================================================================
FAIL: test_register_user_duplicate_username
----------------------------------------------------------------------
Traceback (most recent call last):
  File "tests/test_user_profile_unittest.py", line 245, in test_register_user_duplicate_username
    self.assertEqual(response.status_code, 400)
AssertionError: 201 != 400

----------------------------------------------------------------------
```

## Best Practices

### 1. Test Isolation

Each test should be independent and not rely on other tests:

```python
def setUp(self):
    # Create fresh test data for each test
    self.test_user = self._create_test_user()
```

### 2. Clear Test Names

Test names should clearly describe what they test:

```python
def test_register_user_with_duplicate_email_returns_400(self):
    """Test: Register with existing email returns 400"""
    pass
```

### 3. Arrange-Act-Assert Pattern

```python
def test_example(self):
    # Arrange - Set up test data
    data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'SecurePass123'}
    
    # Act - Perform action
    response = self.client.post('/api/auth/register', json=data)
    
    # Assert - Verify results
    self.assertEqual(response.status_code, 201)
```

### 4. Use Helper Methods

```python
def _create_user(self, **kwargs):
    """Helper to create test user"""
    user = User(**kwargs)
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user
```

### 5. Clean Up Resources

```python
def tearDown(self):
    """Always clean up after tests"""
    db.session.remove()
    db.drop_all()
```

## Comparison: Unittest vs Pytest

| Feature | Unittest | Pytest |
|---------|----------|--------|
| Framework | Built-in | External |
| Fixtures | setUp/tearDown | @pytest.fixture |
| Assertions | self.assertEqual() | assert statement |
| Test Discovery | unittest discovery | Automatic |
| Parametrization | Manual | @pytest.mark.parametrize |
| Plugins | Limited | Extensive |

## Troubleshooting

### Import Errors

```bash
# Ensure you're in the correct directory
cd flask_api

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Database Errors

```python
# Ensure database is created in setUp
def setUp(self):
    db.create_all()

# Ensure database is cleaned in tearDown
def tearDown(self):
    db.drop_all()
```

### Authentication Errors

```python
# Ensure headers are set correctly
headers = {'Authorization': f'Bearer {token}'}

# Verify token is valid
login_response = self.client.post('/api/auth/login', json=credentials)
self.assertEqual(login_response.status_code, 200)
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Unittest Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          cd flask_api
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd flask_api
          python -m unittest tests.test_user_profile_unittest -v
```

## Test Coverage Goals

- **Line Coverage**: > 90%
- **Branch Coverage**: > 85%
- **Function Coverage**: 100%

## Additional Resources

- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [Flask Testing Guide](https://flask.palletsprojects.com/en/2.0.x/testing/)
- [Test Helpers Documentation](test_helpers.py)

## Support

For questions or issues:
1. Check test file comments
2. Review helper utilities
3. Check existing test examples
4. Review API documentation
