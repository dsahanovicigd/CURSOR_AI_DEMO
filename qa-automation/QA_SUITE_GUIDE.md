# QA Automation Suite - Quick Start Guide

## 🚀 One Command to Run Everything

Run the complete QA automation suite with a single command:

```bash
npm run qa
```

Or directly:

```bash
bash qa-automation/scripts/run-qa-suite.sh
```

## 📊 What Gets Tested

The suite runs **8 comprehensive test categories**:

1. **Backend Unit Tests** (pytest)
   - All unit tests in `qa-automation/tests/unit/backend/`
   - Generates: `qa-automation/reports/pytest-unit.xml`

2. **Frontend Unit Tests** (Jest)
   - All Jest tests in the project
   - Generates: `qa-automation/reports/jest-results.json`

3. **Integration Tests** (pytest)
   - All integration tests in `qa-automation/tests/integration/backend/`
   - Generates: `qa-automation/reports/pytest-integration.xml`

4. **E2E Tests** (Playwright)
   - All E2E tests in `qa-automation/tests/e2e/frontend/`
   - Test sets included:
     - ✅ Accessibility Tests
     - ✅ Authentication Tests
     - ✅ Navigation Tests
     - ✅ Task Management Tests
     - ✅ Product Search Tests
     - ✅ Registration Tests
     - ✅ Responsive Design Tests
     - ✅ Error Handling Tests
   - Generates: `test-results/results.json`, `playwright-report/index.html`

5. **Code Quality Checks**
   - ESLint (Frontend)
   - Pylint (Backend)
   - Generates: `qa-automation/reports/pylint-report.json`

6. **Security Scans**
   - npm audit
   - Snyk (if available)
   - Generates: `qa-automation/reports/security/npm-audit.json`

7. **Performance Tests**
   - Backend performance tests (pytest)
   - k6 load testing (if available)
   - Lighthouse (if available)
   - Generates: `qa-automation/reports/k6-results.json`, `lighthouse-results.json`

8. **Quality Dashboard Generation**
   - Aggregates all test results into a single HTML dashboard
   - Generates: `qa-automation/reports/dashboard.html`

## 📈 Dashboard Features

The generated dashboard (`qa-automation/reports/dashboard.html`) displays:

- **Test Results Summary**
  - Total tests run
  - Passed/Failed counts
  - Success rates
  - Execution times

- **Code Quality Metrics**
  - Pylint score (0-10)
  - Error/Warning counts
  - ESLint results

- **Security Status**
  - Vulnerability counts by severity
  - npm audit results
  - Snyk scan results

- **Performance Metrics**
  - Lighthouse scores (Performance, Accessibility, Best Practices, SEO)
  - k6 load test results (response times, failure rates)

- **All Test Sets Indicated**
  - Clear breakdown of all test categories
  - Visual indicators for pass/fail status
  - Color-coded success rates

## 🎯 Usage Examples

### Basic Usage

```bash
# Run complete suite
npm run qa

# Or use the script directly
bash qa-automation/scripts/run-qa-suite.sh
```

### Skip E2E Tests (Faster)

```bash
SKIP_E2E=true npm run qa
```

### Custom URLs for Performance Tests

```bash
BASE_URL=http://localhost:5001 LIGHTHOUSE_URL=http://localhost:4173 npm run qa
```

### View Dashboard After Running

```bash
# Open dashboard in browser
open qa-automation/reports/dashboard.html

# Or on Linux
xdg-open qa-automation/reports/dashboard.html

# Or on Windows
start qa-automation/reports/dashboard.html
```

### View Playwright Report

```bash
npm run test:report
```

## 📁 Generated Reports

After running the suite, you'll find:

```
qa-automation/reports/
├── dashboard.html              # Main dashboard (open this!)
├── dashboard-data.json          # Dashboard data (JSON)
├── recommendations.md           # Quality recommendations
├── recommendations.json         # Recommendations data
├── jest-results.json           # Frontend unit test results
├── pytest-unit.xml             # Backend unit test results
├── pytest-integration.xml      # Integration test results
├── pylint-report.json          # Code quality results
├── k6-results.json             # Load test results
├── lighthouse-results.json     # Performance audit results
└── security/
    ├── npm-audit.json          # npm security audit
    └── snyk-test.json          # Snyk scan results (if available)

test-results/
├── results.json                # Playwright E2E test results
└── results.xml                 # Playwright JUnit results

playwright-report/
└── index.html                  # Playwright HTML report
```

## 🔧 Requirements

### Required
- Node.js and npm
- Python 3
- pytest (for backend tests)
- Playwright (installed via npm)

### Optional (for full suite)
- pylint (for code quality)
- k6 (for load testing)
- lighthouse (for performance audits)
- snyk (for security scanning)

### Install Python Dependencies

```bash
npm run qa:install-deps
```

Or manually:

```bash
python3 -m pip install --user jinja2
```

## 🎨 Dashboard Preview

The dashboard includes:

- **Color-coded status indicators**
  - 🟢 Green: Passing/Good
  - 🟡 Yellow: Warning/Needs attention
  - 🔴 Red: Failing/Critical

- **Test Set Breakdown**
  - All test categories clearly labeled
  - Individual test counts
  - Success rates with visual indicators

- **Comprehensive Metrics**
  - Test execution times
  - Code quality scores
  - Security vulnerability counts
  - Performance benchmarks

## 💡 Tips

1. **First Run**: May take longer as dependencies are installed
2. **CI/CD**: Set `CI=true` for CI-specific behavior
3. **Local Dev**: Dashboard auto-opens if `open` command is available
4. **Troubleshooting**: Check individual report files if dashboard shows missing data
5. **Performance**: Use `SKIP_E2E=true` for faster runs during development

## 🐛 Troubleshooting

### Dashboard shows "No results available"

- Ensure all test categories ran successfully
- Check that report files exist in `qa-automation/reports/`
- Verify jinja2 is installed: `python3 -c "import jinja2"`

### E2E tests fail

- Ensure dev server is running or Playwright can start it
- Check `playwright.config.ts` for correct base URL
- Verify test-results directory is writable

### Missing test results

- Check that test files exist in expected directories
- Verify pytest/playwright/jest are installed
- Review script output for error messages

## 📝 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SKIP_E2E` | `false` | Skip E2E tests for faster runs |
| `BASE_URL` | `http://localhost:5001` | Base URL for k6 load tests |
| `LIGHTHOUSE_URL` | `http://localhost:4173` | URL for Lighthouse audit |
| `CI` | `false` | CI mode (affects Playwright retries) |

## 🎯 Quick Reference

```bash
# Run everything
npm run qa

# Skip E2E tests
SKIP_E2E=true npm run qa

# View dashboard
open qa-automation/reports/dashboard.html

# View Playwright report
npm run test:report

# Install dependencies
npm run qa:install-deps

# Generate dashboard only (after tests run)
npm run qa:dashboard
```

---

**Happy Testing! 🚀**
