# QA Automation System - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

```bash
# Frontend
npm install

# Backend
cd flask_api
pip install -r requirements.txt
pip install pylint pylint-json2html pylint-flask radon jinja2 markdown
cd ..
```

### Step 2: Run Complete QA Suite

```bash
./qa-automation/scripts/master-qa-runner.sh
```

### Step 3: View Results

```bash
# Open dashboard in browser
open qa-automation/reports/dashboard.html

# View recommendations
cat qa-automation/reports/recommendations.md
```

## 📊 What Gets Tested

1. **Unit Tests** - Frontend (Jest) + Backend (pytest)
2. **Integration Tests** - API endpoints and workflows
3. **E2E Tests** - Full user flows (Playwright with POM)
4. **Code Quality** - ESLint + Pylint + Complexity
5. **Security** - npm audit + Snyk + OWASP ZAP
6. **Performance** - k6 load tests + Lighthouse

## 🎯 Quality Targets

- ✅ Test Coverage: **80%+**
- ✅ Code Complexity: **<10**
- ✅ Security Vulnerabilities: **0 critical**
- ✅ Response Time: **<500ms**
- ✅ Error Rate: **<1%**

## 📝 Common Commands

```bash
# Run all QA checks
./qa-automation/scripts/master-qa-runner.sh

# Run only tests
npm run test

# Run only code quality
npm run lint

# Run only security
./qa-automation/scripts/run-security-scan.sh

# Run only performance
./qa-automation/scripts/run-performance-tests.sh

# Generate dashboard
python3 qa-automation/reports/generate-report.py
```

## 🔍 Page Object Model Usage

```typescript
import { LoginPage, DashboardPage } from './pages';

test('login flow', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.login('user@example.com', 'password');
  
  const dashboard = new DashboardPage(page);
  await dashboard.verifyDashboardLoaded();
});
```

## 📚 Full Documentation

See `QA_SYSTEM_DOCUMENTATION.md` for complete details.
