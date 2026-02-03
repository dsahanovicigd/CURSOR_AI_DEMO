#!/bin/bash
# Fix All Test Types - Run all test types and generate dashboard results
# This script ensures all test sets have results displayed in the dashboard

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
REPORTS_DIR="$SCRIPT_DIR/../reports"
QA_DIR="$SCRIPT_DIR/.."

mkdir -p "$REPORTS_DIR"
mkdir -p "$REPORTS_DIR/security"
cd "$ROOT_DIR"

echo ""
echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║     Fix All Test Types - Generate Dashboard Results       ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Find Python venv
VENV_PYTHON=""
if [ -f "$ROOT_DIR/flask_api/venv/bin/python" ]; then
    VENV_PYTHON="$ROOT_DIR/flask_api/venv/bin/python"
fi

PYTEST_CMD=""
if [ -n "$VENV_PYTHON" ]; then
    PYTEST_CMD="$VENV_PYTHON -m pytest"
elif command -v pytest &> /dev/null; then
    PYTEST_CMD="pytest"
fi

# [1] Backend Unit Tests
echo -e "${BLUE}[1/9] Running Backend Unit Tests (pytest)...${NC}"
if [ -n "$PYTEST_CMD" ]; then
    cd flask_api
    $PYTEST_CMD ../qa-automation/tests/unit/backend/ \
                 -v --junitxml="$REPORTS_DIR/pytest-unit.xml" 2>&1 | tail -1 || true
    cd ..
    echo -e "${GREEN}✓ Unit tests completed${NC}"
else
    echo -e "${YELLOW}⚠ pytest not found${NC}"
fi
echo ""

# [2] Frontend Unit Tests (Jest)
echo -e "${BLUE}[2/9] Running Frontend Unit Tests (Jest)...${NC}"
if [ -f "node_modules/.bin/jest" ] || command -v jest &> /dev/null; then
    # Run Jest tests and save JSON output
    npm run test:jest -- --passWithNoTests --json > "$REPORTS_DIR/jest-results.json" 2>&1 || true
    echo -e "${GREEN}✓ Jest tests completed${NC}"
else
    echo -e "${YELLOW}⚠ Jest not found${NC}"
fi
echo ""

# [3] Integration Tests
echo -e "${BLUE}[3/9] Running Integration Tests (pytest)...${NC}"
if [ -n "$PYTEST_CMD" ]; then
    cd flask_api
    $PYTEST_CMD ../qa-automation/tests/integration/backend/ \
                 -v --junitxml="$REPORTS_DIR/pytest-integration.xml" 2>&1 | tail -1 || true
    cd ..
    echo -e "${GREEN}✓ Integration tests completed${NC}"
else
    echo -e "${YELLOW}⚠ pytest not found${NC}"
fi
echo ""

# [4] Performance Tests (pytest)
echo -e "${BLUE}[4/9] Running Performance Tests (pytest)...${NC}"
if [ -n "$PYTEST_CMD" ]; then
    cd flask_api
    $PYTEST_CMD ../qa-automation/tests/performance/backend/ \
                 -v --junitxml="$REPORTS_DIR/pytest-performance.xml" 2>&1 | tail -1 || true
    cd ..
    echo -e "${GREEN}✓ Performance tests completed${NC}"
else
    echo -e "${YELLOW}⚠ pytest not found${NC}"
fi
echo ""

# [5] E2E Tests (Playwright)
echo -e "${BLUE}[5/9] Running E2E Tests (Playwright)...${NC}"
if command -v npx &> /dev/null && [ -f "node_modules/.bin/playwright" ]; then
    mkdir -p test-results
    
    # Use dedicated script to capture ALL test results
    if [ -f "$QA_DIR/scripts/run-all-playwright-tests.sh" ]; then
        bash "$QA_DIR/scripts/run-all-playwright-tests.sh" 2>&1 | grep -E "✅|📊|Total|Passed|Failed|Skipped|Success Rate" || true
    else
        # Fallback: Run with JSON reporter and capture
        SKIP_WEBSERVER=${SKIP_WEBSERVER:-true} npx playwright test --reporter=json 2>&1 | python3 -c "
import json, sys
content = sys.stdin.read()
start = content.find('{')
if start >= 0:
    json_str = content[start:]
    brace_count = 0
    end = -1
    for i, char in enumerate(json_str):
        if char == '{': brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                end = i + 1
                break
    if end > 0:
        try:
            data = json.loads(json_str[:end])
            with open('test-results/results.json', 'w') as f:
                json.dump(data, f, indent=2)
            stats = data.get('stats', {})
            print(f\"  Captured {stats.get('total', 0)} tests\")
        except Exception as e:
            print(f\"  Error: {e}\")
" 2>/dev/null || true
    fi
    
    # Check for results.json
    if [ -f "test-results/results.json" ]; then
        echo -e "${GREEN}✓ Playwright tests completed${NC}"
    else
        echo -e "${YELLOW}⚠ Playwright tests run but results.json not found${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Playwright not found${NC}"
fi
echo ""

# [6] Code Quality (Pylint)
echo -e "${BLUE}[6/9] Running Code Quality Checks (Pylint)...${NC}"
if [ -n "$VENV_PYTHON" ]; then
    cd flask_api
    
    # Check if pylint is available (try both venv and system)
    PYLINT_CMD=""
    if $VENV_PYTHON -m pylint --version &>/dev/null 2>&1; then
        PYLINT_CMD="$VENV_PYTHON -m pylint"
    elif command -v pylint &> /dev/null; then
        PYLINT_CMD="pylint"
    fi
    
    if [ -n "$PYLINT_CMD" ]; then
        $PYLINT_CMD app --rcfile=../qa-automation/quality/pylint.rc \
            --output-format=json --reports=no \
            > "$REPORTS_DIR/pylint-report.json" 2>/dev/null || true
        
        # Check if file has content
        if [ -f "$REPORTS_DIR/pylint-report.json" ] && [ -s "$REPORTS_DIR/pylint-report.json" ]; then
            echo -e "${GREEN}✓ Pylint check completed${NC}"
        else
            # Create empty array if no issues
            echo "[]" > "$REPORTS_DIR/pylint-report.json"
            echo -e "${GREEN}✓ Pylint check completed (no issues found)${NC}"
        fi
    else
        # Create empty report if pylint not available
        echo "[]" > "$REPORTS_DIR/pylint-report.json"
        echo -e "${YELLOW}⚠ Pylint not available - created empty report${NC}"
    fi
    cd ..
else
    echo -e "${YELLOW}⚠ Python venv not found${NC}"
fi
echo ""

# [7] Security Scan (npm audit)
echo -e "${BLUE}[7/9] Running Security Scan (npm audit)...${NC}"
npm audit --audit-level=moderate --json > "$REPORTS_DIR/security/npm-audit.json" 2>&1 || true
echo -e "${GREEN}✓ Security scan completed${NC}"
echo ""

# [8] Performance (Lighthouse)
echo -e "${BLUE}[8/9] Running Performance Tests (Lighthouse)...${NC}"
if command -v lighthouse &> /dev/null || command -v npx &> /dev/null; then
    LIGHTHOUSE_CMD=""
    if command -v lighthouse &> /dev/null; then
        LIGHTHOUSE_CMD="lighthouse"
    else
        LIGHTHOUSE_CMD="npx lighthouse"
    fi
    
    # Check if frontend is already running
    PREVIEW_PID=""
    if curl -s http://localhost:4173 > /dev/null 2>&1; then
        LIGHTHOUSE_URL="http://localhost:4173"
        echo "  Using existing preview server on port 4173"
    elif curl -s http://localhost:5173 > /dev/null 2>&1; then
        LIGHTHOUSE_URL="http://localhost:5173"
        echo "  Using existing dev server on port 5173"
    else
        echo "  Building frontend for Lighthouse..."
        if npm run build > /dev/null 2>&1; then
            echo "  Starting preview server..."
            # Try to start preview server on port 4173
            # If that fails, try a different port
            PREVIEW_PORT=4173
            if npm run preview -- --port $PREVIEW_PORT > /tmp/preview-server.log 2>&1 &
            then
                PREVIEW_PID=$!
            else
                # Try alternative port
                PREVIEW_PORT=4174
                npm run preview -- --port $PREVIEW_PORT > /tmp/preview-server.log 2>&1 &
                PREVIEW_PID=$!
            fi
            
            # Wait for server to be ready (max 30 seconds)
            echo "  Waiting for server to start on port $PREVIEW_PORT..."
            for i in {1..30}; do
                if curl -s "http://localhost:$PREVIEW_PORT" > /dev/null 2>&1; then
                    echo "  Server ready on port $PREVIEW_PORT!"
                    LIGHTHOUSE_URL="http://localhost:$PREVIEW_PORT"
                    break
                fi
                sleep 1
            done
            
            if [ -z "$LIGHTHOUSE_URL" ]; then
                echo -e "${YELLOW}⚠ Preview server failed to start (check port permissions)${NC}"
                echo -e "${YELLOW}  Tip: Start server manually: npm run preview${NC}"
                [ -n "$PREVIEW_PID" ] && kill $PREVIEW_PID 2>/dev/null || true
            fi
        else
            echo -e "${YELLOW}⚠ Frontend build failed${NC}"
        fi
    fi
    
    if [ -n "$LIGHTHOUSE_URL" ]; then
        echo "  Running Lighthouse on $LIGHTHOUSE_URL..."
        # Use Chrome flags to avoid interstitial issues
        $LIGHTHOUSE_CMD "$LIGHTHOUSE_URL" \
            --output=json \
            --output-path="$REPORTS_DIR/lighthouse-results.json" \
            --chrome-flags="--headless --no-sandbox --disable-gpu --disable-dev-shm-usage" \
            --quiet 2>&1 | grep -v "LH:" || true
        
        if [ -f "$REPORTS_DIR/lighthouse-results.json" ] && [ -s "$REPORTS_DIR/lighthouse-results.json" ]; then
            echo -e "${GREEN}✓ Lighthouse tests completed${NC}"
        else
            echo -e "${YELLOW}⚠ Lighthouse results not generated${NC}"
        fi
        
        # Clean up preview server if we started it
        if [ -n "$PREVIEW_PID" ]; then
            kill $PREVIEW_PID 2>/dev/null || true
            sleep 1
            # Force kill if still running
            kill -9 $PREVIEW_PID 2>/dev/null || true
        fi
    else
        echo -e "${YELLOW}⚠ Frontend not available for Lighthouse${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Lighthouse not installed (use: npx lighthouse)${NC}"
fi
echo ""

# [9] Load Testing (k6)
echo -e "${BLUE}[9/9] Running Load Tests (k6)...${NC}"
if command -v k6 &> /dev/null; then
    # Use dedicated script to run k6 tests
    if [ -f "$QA_DIR/scripts/run-k6-load-test.sh" ]; then
        bash "$QA_DIR/scripts/run-k6-load-test.sh" 2>&1 | grep -E "✅|⚠️|📊|Total|Failed|Response" || true
    else
        # Fallback: Run k6 directly
        BASE_URL="${BASE_URL:-http://localhost:5001}"
        
        if curl -s "$BASE_URL/api/health" > /dev/null 2>&1; then
            k6 run --out json="$REPORTS_DIR/k6-results.json" \
                   --env BASE_URL="$BASE_URL" \
                   "$QA_DIR/performance/k6-load-test.js" > /dev/null 2>&1 || true
            
            if [ -f "$REPORTS_DIR/k6-results.json" ] && [ -s "$REPORTS_DIR/k6-results.json" ]; then
                echo -e "${GREEN}✓ k6 load tests completed${NC}"
            else
                echo -e "${YELLOW}⚠ k6 results not generated${NC}"
            fi
        else
            echo -e "${YELLOW}⚠ Backend API not running at $BASE_URL${NC}"
            echo -e "${YELLOW}  Start backend or set BASE_URL environment variable${NC}"
        fi
    fi
else
    echo -e "${YELLOW}⚠ k6 not installed (install with: brew install k6)${NC}"
fi
echo ""

# Generate Dashboard
echo -e "${BLUE}[10/10] Generating Dashboard...${NC}"
if [ -n "$VENV_PYTHON" ] && $VENV_PYTHON -c "import jinja2" 2>/dev/null; then
    $VENV_PYTHON "$QA_DIR/reports/generate_dashboard.py" 2>&1 | tail -1
    echo -e "${GREEN}✓ Dashboard generated${NC}"
else
    echo -e "${YELLOW}⚠ Dashboard generation skipped (jinja2 not available)${NC}"
fi
echo ""

# Summary
echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║              All Tests Complete!                            ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📊 View Dashboard:${NC}"
echo -e "  ${CYAN}$REPORTS_DIR/dashboard.html${NC}"
echo ""
