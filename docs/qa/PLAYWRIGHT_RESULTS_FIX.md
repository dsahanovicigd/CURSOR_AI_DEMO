# Playwright E2E Test Results Fix

## Issue

E2E test results are not showing in the QA dashboard because `test-results/results.json` is missing.

## Root Cause

Playwright tests are configured to generate JSON reports in `playwright.config.ts`, but the `results.json` file is not being generated when tests run. This can happen if:

1. Tests haven't been run since the config was updated
2. The JSON reporter isn't working correctly
3. Tests are run without the JSON reporter flag

## Solution

### Option 1: Run Tests with JSON Reporter (Recommended)

```bash
npm run test -- --reporter=json --reporter-option output=test-results/results.json
```

Or use the helper script:
```bash
./scripts/testing/generate-playwright-results.sh
```

### Option 2: Update QA Scripts

The QA scripts have been updated to ensure JSON reports are generated:
- `qa-automation/scripts/run-all-qa.sh` now explicitly sets JSON reporter output
- Verifies that `results.json` is created after test run

### Option 3: Verify Playwright Config

Ensure `playwright.config.ts` has JSON reporter configured:

```typescript
reporter: [
  ['html'],
  ['json', { outputFile: 'test-results/results.json' }],
  ['junit', { outputFile: 'test-results/results.xml' }]
]
```

## Dashboard Updates

The dashboard generator has been updated to:

1. **Check multiple locations** for Playwright results:
   - `test-results/results.json`
   - `test-results/playwright-results.json`
   - `qa-automation/reports/playwright-results.json`
   - `playwright-report/results.json`

2. **Show helpful message** when results are missing:
   - Displays instructions on how to generate results
   - Shows the command to run

3. **Improved parsing**:
   - Better handling of different Playwright JSON formats
   - Handles suites structure correctly
   - Counts skipped tests properly

## Verification

After running tests, verify the results file exists:

```bash
ls -lh test-results/results.json
```

Then regenerate the dashboard:

```bash
python3 qa-automation/reports/generate_dashboard.py
```

## Expected Result

After running Playwright tests with JSON reporter, the dashboard should show:

```
E2E Tests (Playwright)
- Total Tests: X
- Passed: Y
- Failed: Z
- Success Rate: XX%
```

## Troubleshooting

If results still don't appear:

1. **Check file exists**: `ls test-results/results.json`
2. **Check file format**: `head test-results/results.json | python3 -m json.tool`
3. **Check dashboard logs**: Look for warnings in dashboard generation output
4. **Run tests manually**: `npm run test -- --reporter=json`
5. **Check Playwright version**: Ensure compatible version is installed

## Related Files

- `playwright.config.ts` - Playwright configuration
- `qa-automation/reports/generate_dashboard.py` - Dashboard generator
- `qa-automation/scripts/run-all-qa.sh` - QA runner script
- `scripts/testing/generate-playwright-results.sh` - Helper script
