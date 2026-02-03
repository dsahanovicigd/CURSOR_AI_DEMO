# Test Suite Structure

## Overview

The test suite is organized into focused test files for better maintainability and clarity.

## Test Structure

```
tests/
├── conftest.py          # Shared fixtures and configuration
├── test_auth.py         # Authentication and authorization tests
├── test_tasks.py        # Task CRUD operation tests
├── test_validation.py   # Input validation tests
└── test_performance.py  # Performance, caching, and background task tests
```

## Test Files

### `conftest.py`
**Purpose:** Shared fixtures and pytest configuration

**Fixtures:**
- `app` - Flask application instance
- `client` - Test client
- `db_session` - Database session
- `test_user` - Test customer user
- `test_admin` - Test admin user
- `test_agent` - Test agent user
- `test_project` - Test project
- `test_task` - Test task
- `multiple_tasks` - Multiple test tasks
- `auth_headers` - Authentication headers for test user
- `admin_headers` - Authentication headers for admin user

### `test_auth.py`
**Purpose:** Authentication and authorization tests

**Test Classes:**
- `TestAuthentication` - Login, registration, token management
- `TestAuthorization` - Access control, role-based permissions

**Coverage:**
- User registration
- Login/logout
- Token refresh
- Protected endpoint access
- Role-based access control
- Admin-only endpoints

### `test_tasks.py`
**Purpose:** Task CRUD operations

**Test Classes:**
- `TestTaskCRUD` - Create, read, update, delete operations
- `TestTaskAccessControl` - Access permissions
- `TestTaskPagination` - Pagination functionality
- `TestTaskFilters` - Filtering by status, priority, project
- `TestTaskAssignment` - Task assignment functionality

**Coverage:**
- Task creation
- Task retrieval (single and list)
- Task updates
- Task deletion
- Task completion
- Access control
- Pagination
- Filtering

### `test_validation.py`
**Purpose:** Input validation tests

**Test Classes:**
- `TestTaskValidation` - Task field validation
- `TestUserValidation` - User field validation
- `TestProjectValidation` - Project field validation
- `TestPaginationValidation` - Pagination parameter validation
- `TestFilterValidation` - Filter parameter validation
- `TestDateValidation` - Date field validation
- `TestAccessValidation` - Access validation

**Coverage:**
- Required fields
- Field formats (email, dates, etc.)
- Enum values (status, priority, etc.)
- Field length limits
- Invalid data handling
- Access validation

### `test_performance.py`
**Purpose:** Performance, caching, and background tasks

**Test Classes:**
- `TestCachingPerformance` - Cache performance tests
- `TestDatabasePerformance` - Database query performance
- `TestPaginationPerformance` - Pagination performance
- `TestConcurrentRequests` - Concurrent request handling
- `TestCacheHitRate` - Cache effectiveness
- `TestBackgroundTaskPerformance` - Background task performance
- `TestMemoryUsage` - Memory usage tests

**Coverage:**
- Cache hit/miss rates
- Query performance with indexes
- Pagination performance
- Concurrent request handling
- Background task execution
- Cache invalidation
- Memory usage

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_auth.py
pytest tests/test_tasks.py
pytest tests/test_validation.py
pytest tests/test_performance.py
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html
```

### Run Specific Test Class
```bash
pytest tests/test_tasks.py::TestTaskCRUD
```

### Run Specific Test
```bash
pytest tests/test_tasks.py::TestTaskCRUD::test_create_task
```

### Run with Verbose Output
```bash
pytest -v
```

### Run Tests in Parallel
```bash
pytest -n auto  # Requires pytest-xdist
```

## Test Coverage

Target: **90%+ coverage**

Current coverage can be viewed by running:
```bash
pytest --cov=app --cov-report=html
```

Then open `htmlcov/index.html` in your browser.

## Test Fixtures Usage

### Example: Using test_user fixture
```python
def test_something(client, test_user):
    # test_user is automatically created
    response = client.get(f'/api/users/{test_user.id}')
    assert response.status_code == 200
```

### Example: Using auth_headers fixture
```python
def test_protected_endpoint(client, auth_headers):
    # auth_headers contains valid JWT token
    response = client.get('/api/tasks', headers=auth_headers)
    assert response.status_code == 200
```

### Example: Using multiple fixtures
```python
def test_task_in_project(client, auth_headers, test_project):
    response = client.post('/api/tasks',
        headers=auth_headers,
        json={
            'title': 'Task',
            'project_id': test_project.id
        }
    )
    assert response.status_code == 201
```

## Best Practices

1. **Use fixtures** - Don't create test data manually, use fixtures
2. **Isolated tests** - Each test should be independent
3. **Clear test names** - Test names should describe what they test
4. **Arrange-Act-Assert** - Follow AAA pattern
5. **Test edge cases** - Test both success and failure scenarios
6. **Mock external services** - Mock external APIs, databases in unit tests
7. **Clean up** - Fixtures handle cleanup automatically

## Continuous Integration

Tests are designed to run in CI/CD pipelines:
- Fast execution (< 30 seconds)
- No external dependencies required (uses in-memory DB)
- Deterministic results
- High coverage

## Troubleshooting

### Tests failing with database errors
- Ensure test database is properly isolated
- Check that fixtures are cleaning up properly

### Tests failing with import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that app is in Python path

### Cache-related test failures
- Cache is cleared between tests automatically
- If issues persist, check cache configuration in `conftest.py`
