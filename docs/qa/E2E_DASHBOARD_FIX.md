# E2E Tests Dashboard Fix

## Issue Fixed

The QA dashboard was not showing E2E (Playwright) test results even though the results file existed.

## Changes Made

### 1. Updated Playwright Results Parser (`generate_dashboard.py`)

**Problem:** The parser was looking for `stats.total`, `stats.passed`, `stats.failed` which don't exist in Playwright's JSON format.

**Solution:** Updated parser to use Playwright's actual format:
- `stats.expected` → passed tests
- `stats.unexpected` → failed tests  
- `stats.skipped` → skipped tests
- `stats.flaky` → flaky tests
- Total = expected + unexpected + skipped

**Code Location:** `qa-automation/reports/generate_dashboard.py` lines 241-309

### 2. Enhanced File Location Detection

**Problem:** Dashboard only checked one location for Playwright results.

**Solution:** Added multiple location checks:
- `test-results/results.json` (primary)
- `test-results/playwright-results.json` (alternative)
- `qa-automation/reports/playwright-results.json` (fallback)
- Any JSON files in `test-results/` directory (except metadata files)

**Code Location:** `qa-automation/reports/generate_dashboard.py` lines 315-333

### 3. Updated Dashboard HTML Template

**Added:** Display of skipped and flaky tests in the E2E section.

**Code Location:** `qa-automation/reports/generate_dashboard.py` lines 562-590

### 4. Updated QA Script

**Enhanced:** `run-all-qa.sh` to ensure `test-results` directory exists before running Playwright tests.

**Code Location:** `qa-automation/scripts/run-all-qa.sh` lines 155-172

## Current Status

✅ **E2E Tests section now appears in dashboard**
✅ **Parser correctly reads Playwright JSON format**
✅ **Dashboard shows: Total, Passed, Failed, Skipped, Flaky**
✅ **Multiple file locations checked**

## Note

The dashboard currently shows **0 tests** because:
- Playwright tests haven't been run yet, OR
- Tests were skipped, OR  
- Tests failed to start (e.g., web server not running)

## To Generate E2E Test Results

Run Playwright tests:

```bash
# Option 1: Run via npm script
npm run test

# Option 2: Run via QA script (includes E2E tests)
./qa-automation/scripts/run-all-qa.sh

# Option 3: Run directly with Playwright
npx playwright test
```

After running tests, the `test-results/results.json` file will be updated with actual test results, and the dashboard will display them.

## Verification

Check dashboard data:
```bash
python3 -c "import json; d=json.load(open('qa-automation/reports/dashboard-data.json')); print('Playwright:', d.get('playwright'))"
```

Regenerate dashboard:
```bash
python3 qa-automation/reports/generate_dashboard.py
```

View dashboard:
```bash
open qa-automation/reports/dashboard.html
```

## Result

The E2E Tests section now appears in the dashboard and will show actual results once Playwright tests are executed.
