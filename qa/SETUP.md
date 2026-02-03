# QA Automation Setup Guide

## Prerequisites Installation

### 1. Install Node.js Dependencies

```bash
npm install
```

This will install:
- Jest and testing libraries
- Playwright
- ESLint
- Lighthouse
- All other dev dependencies

### 2. Install Python Dependencies

**For QA Scripts (Recommended - Virtual Environment):**
```bash
# Create virtual environment for QA scripts
python3 -m venv qa/.venv
source qa/.venv/bin/activate  # On Windows: qa\.venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install jinja2 markdown pylint pylint-json2html pylint-flask
```

**Alternative - User Installation (if virtual env not preferred):**
```bash
pip3 install --user jinja2 markdown pylint pylint-json2html pylint-flask
```

**For Flask API:**
```bash
cd flask_api
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install pylint pylint-json2html pylint-flask
```

**Note:** The QA runner script (`run-qa-local.sh`) will automatically create and use a virtual environment in `qa/.venv` if dependencies are not found.

### 3. Install k6 (Optional, for load testing)

**macOS:**
```bash
brew install k6
```

**Linux:**
```bash
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6
```

**Windows:**
Download from https://k6.io/docs/getting-started/installation/

## Common Issues & Solutions

### Issue: Jest not found
**Solution:**
```bash
npm install --save-dev jest jest-environment-jsdom ts-jest @testing-library/jest-dom @testing-library/react @testing-library/user-event @types/jest identity-obj-proxy
```

### Issue: Pylint not found
**Solution:**
```bash
pip3 install pylint pylint-json2html pylint-flask
```

### Issue: jinja2 not found
**Solution:**
```bash
pip3 install jinja2 markdown
```

### Issue: pytest not found
**Solution:**
```bash
cd flask_api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Port 5173 already in use (Playwright)
**Solution:**
```bash
# Find and kill process on port 5173
lsof -ti:5173 | xargs kill -9

# Or set reuseExistingServer in playwright.config.ts
```

### Issue: ESLint errors (TypeScript `any` types)
**Solution:**
Replace `any` with proper TypeScript types:
- Use specific interfaces/types
- Use `unknown` for truly unknown types
- Use generics where appropriate

## Quick Setup Script

Run this to set up everything:

```bash
# Install Node dependencies
npm install

# Install Python dependencies
pip3 install jinja2 markdown pylint pylint-json2html pylint-flask

# Install Playwright browsers
npx playwright install --with-deps

# Verify installations
npm run test:jest -- --version
pylint --version
pytest --version
```

## Running QA Checks

### Run All Checks
```bash
./qa/scripts/run-qa-local.sh
```

### Run Individual Checks
```bash
# Code quality
npm run lint
cd flask_api && pylint app

# Tests
npm run test:jest
npm run test

# Security
npm audit

# Performance
npm run qa:performance
k6 run qa/k6-load-test.js
```

## Next Steps

1. Fix ESLint errors (replace `any` types)
2. Write Jest unit tests for React components
3. Ensure Flask API virtual environment is activated for pytest
4. Review and fix security vulnerabilities
5. Generate dashboard: `npm run qa:dashboard`
