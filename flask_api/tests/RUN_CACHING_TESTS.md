# Running Caching Tests

## Quick Start

To run caching tests **without coverage warnings**, use the dedicated config file:

```bash
cd flask_api
source venv/bin/activate
pytest -c tests/pytest_caching.ini tests/test_post_caching.py tests/test_cache_invalidation.py tests/test_database_indexes.py tests/test_post_routes_coverage.py
```

## Why the Coverage Warning?

The main `pytest.ini` checks coverage for the **entire app** (`--cov=app`) and requires 90% coverage. When running only caching tests, the overall app coverage is ~51%, which triggers the warning.

## Solutions

### Option 1: Use Dedicated Config (Recommended)
Use the caching-specific config that only checks coverage for caching modules:

```bash
pytest -c tests/pytest_caching.ini tests/test_post_*.py tests/test_cache_*.py tests/test_database_*.py
```

**Coverage checked:**
- `app/cache_utils.py`: 73% ✅
- `app/posts/routes.py`: 78% ✅
- **Total**: 76% ✅ (exceeds 70% threshold)

### Option 2: Override Coverage Settings
Run tests with explicit coverage settings:

```bash
pytest tests/test_post_caching.py tests/test_cache_invalidation.py tests/test_database_indexes.py tests/test_post_routes_coverage.py \
  --cov=app.cache_utils \
  --cov=app.posts.routes \
  --cov-report=term \
  --cov-fail-under=70 \
  -v
```

### Option 3: Run Without Coverage Check
If you just want to verify tests pass:

```bash
pytest tests/test_post_caching.py tests/test_cache_invalidation.py tests/test_database_indexes.py tests/test_post_routes_coverage.py -v --no-cov
```

## Test Results

With the caching config:
```
✅ 48 tests passed
✅ Coverage: 76% (cache_utils: 73%, posts/routes: 78%)
✅ No coverage warnings
```

## All Test Commands

```bash
# Run all caching tests (recommended)
pytest -c tests/pytest_caching.ini tests/test_post_*.py tests/test_cache_*.py tests/test_database_*.py

# Run specific test file
pytest -c tests/pytest_caching.ini tests/test_post_caching.py -v

# Run with HTML coverage report
pytest -c tests/pytest_caching.ini tests/test_post_*.py tests/test_cache_*.py --cov-report=html
# Open: htmlcov/index.html

# Run without coverage (fastest)
pytest tests/test_post_*.py tests/test_cache_*.py -v --no-cov
```
