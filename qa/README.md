# QA Automation System

Complete Quality Assurance automation system for the full-stack application with automated testing, code quality checks, security scanning, performance monitoring, and AI-generated recommendations.

## 🎯 Features

### ✅ Automated Test Execution
- **Jest** - Frontend unit tests
- **Playwright** - Frontend E2E tests
- **pytest** - Backend unit and integration tests

### 🔍 Code Quality Checks
- **ESLint** - JavaScript/TypeScript linting
- **Pylint** - Python code quality analysis

### 🔒 Security Scanning
- **Snyk** - Dependency vulnerability scanning
- **OWASP ZAP** - Dynamic security testing

### ⚡ Performance Monitoring
- **Lighthouse** - Web performance, accessibility, SEO analysis
- **k6** - Load and stress testing

### 📊 Quality Reporting
- **Dashboard** - HTML dashboard with all metrics
- **AI Recommendations** - Automated improvement suggestions

## 🚀 Quick Start

### Prerequisites

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
cd flask_api
pip install -r requirements.txt
pip install pylint pylint-json2html pylint-flask jinja2
cd ..

# Install k6 (macOS)
brew install k6

# Install k6 (Linux)
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6
```

### Run QA Locally

**First Time Setup:**
```bash
# Set up Python dependencies (creates virtual environment)
./qa/setup-python-deps.sh
```

**Run QA Checks:**
```bash
# Run all QA checks (will auto-setup Python deps if needed)
./qa/scripts/run-qa-local.sh

# Or run individual checks
npm run qa:lint      # ESLint
npm run qa:test      # Jest + Playwright
npm run qa:security  # npm audit
npm run qa:performance  # Lighthouse
npm run qa:dashboard   # Generate dashboard
```

### Run Individual Tools

#### Frontend Tests (Jest)
```bash
npm run test:jest
npm run test:jest:watch
npm run test:jest:coverage
```

#### Backend Code Quality (Pylint)
```bash
cd flask_api
pylint app --output-format=json --reports=yes
```

#### Security Scanning
```bash
# Snyk (requires SNYK_TOKEN)
npx snyk test

# npm audit
npm audit --audit-level=moderate
```

#### Performance Testing
```bash
# Lighthouse
npm run build
npm run preview &
npm run qa:performance

# k6 Load Testing
k6 run qa/k6-load-test.js
```

## 📁 Project Structure

```
qa/
├── README.md                 # This file
├── k6-load-test.js          # k6 load test script
├── .zap/
│   └── rules.tsv            # OWASP ZAP rules
└── scripts/
    ├── generate_dashboard.py      # Dashboard generator
    ├── generate_recommendations.py  # AI recommendations
    └── run-qa-local.sh            # Local QA runner

qa-reports/                  # Generated reports (gitignored)
├── dashboard.html           # Quality dashboard
├── dashboard-data.json      # Dashboard data
├── recommendations.json     # Recommendations (JSON)
└── recommendations.md       # Recommendations (Markdown)
```

## 🔧 Configuration Files

- `jest.config.js` - Jest configuration
- `.pylintrc` - Pylint configuration
- `.lighthouserc.js` - Lighthouse CI configuration
- `.eslintrc.cjs` - ESLint configuration (existing)

## 📊 GitHub Actions Workflow

The QA automation runs automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Daily schedule (2 AM UTC)
- Manual trigger via workflow_dispatch

### Workflow Jobs

1. **Code Quality**
   - ESLint (Frontend)
   - Pylint (Backend)

2. **Test Execution**
   - Jest (Frontend unit tests)
   - Playwright (Frontend E2E tests)
   - pytest (Backend tests)

3. **Security Scanning**
   - Snyk (Dependencies)
   - OWASP ZAP (Dynamic scanning)

4. **Performance Monitoring**
   - Lighthouse (Web performance)
   - k6 (Load testing)

5. **Reporting**
   - Quality dashboard generation
   - AI recommendations
   - PR comments (on pull requests)

## 📈 Quality Metrics

### Test Coverage Targets
- **Frontend**: 70%+ (Jest)
- **Backend**: 80%+ (pytest)

### Code Quality Targets
- **Pylint Score**: 8.0+/10
- **ESLint**: 0 errors, minimal warnings

### Performance Targets
- **Lighthouse Performance**: 80+
- **Lighthouse Accessibility**: 90+
- **k6 P95 Response Time**: <2000ms
- **k6 Error Rate**: <1%

### Security Targets
- **Snyk High Vulnerabilities**: 0
- **OWASP ZAP**: No high/critical issues

## 🤖 AI Recommendations

The system automatically generates recommendations based on:
- Test coverage gaps
- Code quality issues
- Security vulnerabilities
- Performance bottlenecks
- Accessibility issues

Recommendations are prioritized as:
- 🔴 **High Priority** - Critical issues requiring immediate attention
- 🟡 **Medium Priority** - Important improvements
- 🟢 **Low Priority** - Nice-to-have enhancements

## 🔐 Required Secrets

For full functionality, add these GitHub Secrets:

- `SNYK_TOKEN` - Snyk API token (for security scanning)
- `SLACK_WEBHOOK_URL` - Slack webhook (for notifications)
- `VITE_API_URL` - Frontend API URL (for builds)

## 📝 Writing Tests

### Frontend Unit Tests (Jest)

```typescript
// src/components/__tests__/Button.test.tsx
import { render, screen } from '@testing-library/react';
import { Button } from '../Button';

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });
});
```

### Backend Tests (pytest)

```python
# flask_api/tests/test_example.py
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        yield client

def test_example(client):
    response = client.get('/api/health')
    assert response.status_code == 200
```

## 🐛 Troubleshooting

### Jest tests not running
- Ensure `jest.config.js` exists
- Check that test files match the pattern `*.test.{ts,tsx}` or `*.spec.{ts,tsx}`
- Verify `setupTests.ts` exists in `src/`

### Pylint not finding modules
- Check `.pylintrc` init-hook includes Flask API path
- Ensure you're running from project root

### k6 tests failing
- Ensure backend API is running
- Check `BASE_URL` environment variable
- Verify API endpoints are accessible

### Dashboard not generating
- Ensure all QA reports exist in `qa-reports/`
- Check Python dependencies: `pip install jinja2`
- Verify scripts have execute permissions

## 📚 Resources

- [Jest Documentation](https://jestjs.io/)
- [Playwright Documentation](https://playwright.dev/)
- [pytest Documentation](https://docs.pytest.org/)
- [Pylint Documentation](https://pylint.pycqa.org/)
- [Lighthouse Documentation](https://developers.google.com/web/tools/lighthouse)
- [k6 Documentation](https://k6.io/docs/)
- [Snyk Documentation](https://docs.snyk.io/)
- [OWASP ZAP Documentation](https://www.zaproxy.org/docs/)

## 🎉 Success Metrics

Track your QA improvements:
- Test coverage trends
- Code quality scores
- Security vulnerability reduction
- Performance improvements
- Time to fix issues

## 🤝 Contributing

When adding new features:
1. Write tests (Jest for frontend, pytest for backend)
2. Run QA locally before pushing
3. Ensure all checks pass
4. Review AI recommendations
5. Update documentation if needed
