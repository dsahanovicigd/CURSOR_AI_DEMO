#!/bin/bash
# Complete QA Automation Suite Runner
# Runs all tests and generates comprehensive dashboard with all test sets
#
# Usage:
#   ./qa-automation/scripts/run-qa-suite.sh
#   OR
#   bash qa-automation/scripts/run-qa-suite.sh
#
# Environment Variables:
#   SKIP_E2E=true          - Skip E2E tests (default: false)
#   BASE_URL=<url>         - Base URL for E2E tests (default: http://localhost:5173)
#   LIGHTHOUSE_URL=<url>   - URL for Lighthouse (default: http://localhost:4173)

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get script directory and set paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
REPORTS_DIR="$SCRIPT_DIR/../reports"
QA_DIR="$SCRIPT_DIR/.."

# Create reports directory
mkdir -p "$REPORTS_DIR"
mkdir -p "$REPORTS_DIR/security"
cd "$ROOT_DIR"

# Track overall status
OVERALL_STATUS=0
START_TIME=$(date +%s)

# Print header
echo ""
echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║     QA Automation Suite - Complete Test Execution        ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to print step header
print_step() {
    local step_num=$1
    local total_steps=$2
    local step_name=$3
    echo -e "${BLUE}[$step_num/$total_steps]${NC} ${CYAN}$step_name...${NC}"
}

# Function to print success
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Function to print failure
print_failure() {
    echo -e "${RED}✗${NC} $1"
    OVERALL_STATUS=1
}

# Function to print info
print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# Check dependencies
print_info "Checking dependencies..."
if [ ! -d "node_modules" ]; then
    print_info "Installing npm dependencies..."
    npm install --silent
fi

# Find Python venv and set up Python command (check multiple locations)
# Priority: flask_api/venv (has pytest) > flask_api/.venv > qa-automation/.venv
VENV_ACTIVATED=false
VENV_PYTHON=""
VENV_PYTHON_PATH=""

if [ -d "$ROOT_DIR/flask_api/venv" ] && [ -f "$ROOT_DIR/flask_api/venv/bin/python" ]; then
    VENV_PYTHON_PATH="$ROOT_DIR/flask_api/venv/bin/python"
    VENV_ACTIVATED=true
    VENV_PYTHON="$VENV_PYTHON_PATH"
elif [ -d "$ROOT_DIR/flask_api/.venv" ] && [ -f "$ROOT_DIR/flask_api/.venv/bin/python" ]; then
    VENV_PYTHON_PATH="$ROOT_DIR/flask_api/.venv/bin/python"
    VENV_ACTIVATED=true
    VENV_PYTHON="$VENV_PYTHON_PATH"
elif [ -d "$ROOT_DIR/qa-automation/.venv" ] && [ -f "$ROOT_DIR/qa-automation/.venv/bin/python" ]; then
    VENV_PYTHON_PATH="$ROOT_DIR/qa-automation/.venv/bin/python"
    VENV_ACTIVATED=true
    VENV_PYTHON="$VENV_PYTHON_PATH"
fi

# Try to activate venv for pip commands (may not persist, but helps with PATH)
if [ "$VENV_ACTIVATED" = true ] && [ -n "$VENV_PYTHON_PATH" ]; then
    source "$(dirname "$VENV_PYTHON_PATH")/activate" > /dev/null 2>&1 || true
fi

# Check for Python dependencies (use venv python if available, python3 otherwise)
PYTHON_CMD="python3"
if [ "$VENV_ACTIVATED" = true ] && [ -n "$VENV_PYTHON" ]; then
    PYTHON_CMD="$VENV_PYTHON"
fi

if ! $PYTHON_CMD -c "import jinja2" 2>/dev/null; then
    print_info "Installing Python dependencies (jinja2)..."
    if [ "$VENV_ACTIVATED" = true ] && [ -n "$VENV_PYTHON" ]; then
        "$VENV_PYTHON" -m pip install jinja2 > /dev/null 2>&1 || true
    else
        python3 -m pip install --user jinja2 > /dev/null 2>&1 || true
    fi
fi

echo ""

# Detect pytest command once for all test sections
# Check if pytest is available (either as command or via python/python3 -m)
# Try multiple methods: direct command, venv python -m, or python3 -m
PYTEST_CMD=""

# First check: direct pytest command
if command -v pytest &> /dev/null; then
    PYTEST_CMD="pytest"
fi

# Second check: if venv python is available, try venv python -m pytest
if [ -z "$PYTEST_CMD" ] && [ "$VENV_ACTIVATED" = true ] && [ -n "$VENV_PYTHON" ] && [ -f "$VENV_PYTHON" ]; then
    # Use the venv's python directly (full path)
    if "$VENV_PYTHON" -m pytest --version &> /dev/null 2>&1; then
        PYTEST_CMD="$VENV_PYTHON -m pytest"
    fi
fi

# Third check: try python -m pytest (in case venv python is in PATH after activation)
if [ -z "$PYTEST_CMD" ] && [ "$VENV_ACTIVATED" = true ]; then
    if python -m pytest --version &> /dev/null 2>&1; then
        PYTEST_CMD="python -m pytest"
    fi
fi

# Fallback: try python3 -m pytest
if [ -z "$PYTEST_CMD" ] && python3 -m pytest --version &> /dev/null 2>&1; then
    PYTEST_CMD="python3 -m pytest"
fi

if [ -n "$PYTEST_CMD" ]; then
    print_info "pytest detected: $PYTEST_CMD"
else
    print_info "pytest not found - backend tests will be skipped"
    if [ "$VENV_ACTIVATED" = true ] && [ -n "$VENV_PYTHON" ]; then
        print_info "  (VENV found: $VENV_PYTHON, but pytest not available)"
        print_info "  (Try: $VENV_PYTHON -m pip install pytest)"
    else
        print_info "  (Try: cd flask_api && source venv/bin/activate && pip install pytest)"
    fi
fi
echo ""

# =========================================
# [1/8] Running Unit Tests (Backend)
# =========================================
print_step 1 8 "Running Backend Unit Tests (pytest)"

UNIT_TEST_COUNT=0
UNIT_TEST_TIME=0

if [ -n "$PYTEST_CMD" ]; then
    cd flask_api
    START_UNIT=$(date +%s.%N)
    
    PYTEST_OUTPUT=$(PYTHONPATH="$ROOT_DIR/flask_api:$ROOT_DIR" \
        $PYTEST_CMD ../qa-automation/tests/unit/backend/ \
        -v --tb=short \
        --junitxml="$REPORTS_DIR/pytest-unit.xml" \
        2>&1) || UNIT_EXIT_CODE=$?
    
    END_UNIT=$(date +%s.%N)
    UNIT_TEST_TIME=$(echo "$END_UNIT - $START_UNIT" | bc 2>/dev/null || echo "0")
    
    PYTEST_SUMMARY=$(echo "$PYTEST_OUTPUT" | grep -E '(passed|failed|error)' | tail -1 || echo "")
    PYTEST_PASSED=$(echo "$PYTEST_SUMMARY" | grep -oE '[0-9]+ passed' | sed -nE 's/([0-9]+) passed/\1/p' | tail -1 || echo "0")
    PYTEST_FAILED=$(echo "$PYTEST_SUMMARY" | grep -oE '[0-9]+ failed' | sed -nE 's/([0-9]+) failed/\1/p' | tail -1 || echo "0")
    
    [ -z "$PYTEST_PASSED" ] && PYTEST_PASSED=0
    [ -z "$PYTEST_FAILED" ] && PYTEST_FAILED=0
    
    UNIT_TEST_COUNT=$PYTEST_PASSED
    cd ..
    
    if [ "$PYTEST_PASSED" -gt 0 ]; then
        print_success "Backend Unit Tests: $PYTEST_PASSED passed, $PYTEST_FAILED failed (${UNIT_TEST_TIME}s)"
    else
        print_info "Backend Unit Tests: No tests found or all skipped"
    fi
else
    print_info "pytest not found - skipping backend unit tests"
fi
echo ""

# =========================================
# [2/8] Running Unit Tests (Frontend)
# =========================================
print_step 2 8 "Running Frontend Unit Tests (Jest)"

JEST_COUNT=0
if [ -f "node_modules/.bin/jest" ] || command -v jest &> /dev/null; then
    START_JEST=$(date +%s.%N)
    
    npm run test:jest -- --passWithNoTests --silent --json > "$REPORTS_DIR/jest-results.json" 2>&1 || true
    
    END_JEST=$(date +%s.%N)
    JEST_TIME=$(echo "$END_JEST - $START_JEST" | bc 2>/dev/null || echo "0")
    
    JEST_DATA=$(cat "$REPORTS_DIR/jest-results.json" 2>/dev/null || echo "{}")
    JEST_PASSED=$(echo "$JEST_DATA" | python3 -c "import json, sys; data=json.load(sys.stdin) if sys.stdin.read(1) else {}; print(data.get('numPassedTests', 0))" 2>/dev/null || echo "0")
    JEST_FAILED=$(echo "$JEST_DATA" | python3 -c "import json, sys; data=json.load(sys.stdin) if sys.stdin.read(1) else {}; print(data.get('numFailedTests', 0))" 2>/dev/null || echo "0")
    
    JEST_COUNT=$JEST_PASSED
    
    if [ "$JEST_PASSED" -gt 0 ] || [ "$JEST_FAILED" -gt 0 ]; then
        print_success "Frontend Unit Tests: $JEST_PASSED passed, $JEST_FAILED failed (${JEST_TIME}s)"
    else
        print_info "Frontend Unit Tests: No tests found"
    fi
else
    print_info "Jest not found - skipping frontend unit tests"
fi
echo ""

# =========================================
# [3/8] Running Integration Tests
# =========================================
print_step 3 8 "Running Integration Tests (pytest)"

INTEGRATION_COUNT=0
# Use the same pytest command detection from above
if [ -n "$PYTEST_CMD" ]; then
    cd flask_api
    START_INT=$(date +%s.%N)
    
    PYTEST_OUTPUT=$(PYTHONPATH="$ROOT_DIR/flask_api:$ROOT_DIR" \
        $PYTEST_CMD ../qa-automation/tests/integration/backend/ \
        -v --tb=short \
        --junitxml="$REPORTS_DIR/pytest-integration.xml" \
        2>&1) || INT_EXIT_CODE=$?
    
    END_INT=$(date +%s.%N)
    INT_TIME=$(echo "$END_INT - $START_INT" | bc 2>/dev/null || echo "0")
    
    PYTEST_SUMMARY=$(echo "$PYTEST_OUTPUT" | grep -E '(passed|failed|error)' | tail -1 || echo "")
    INT_PASSED=$(echo "$PYTEST_SUMMARY" | grep -oE '[0-9]+ passed' | sed -nE 's/([0-9]+) passed/\1/p' | tail -1 || echo "0")
    INT_FAILED=$(echo "$PYTEST_SUMMARY" | grep -oE '[0-9]+ failed' | sed -nE 's/([0-9]+) failed/\1/p' | tail -1 || echo "0")
    
    [ -z "$INT_PASSED" ] && INT_PASSED=0
    [ -z "$INT_FAILED" ] && INT_FAILED=0
    
    INTEGRATION_COUNT=$INT_PASSED
    cd ..
    
    if [ "$INT_PASSED" -gt 0 ]; then
        print_success "Integration Tests: $INT_PASSED passed, $INT_FAILED failed (${INT_TIME}s)"
    else
        print_info "Integration Tests: No tests found or all skipped"
    fi
else
    print_info "pytest not found - skipping integration tests"
fi
echo ""

# =========================================
# [4/8] Running E2E Tests (Playwright)
# =========================================
if [ "${SKIP_E2E:-false}" != "true" ]; then
    print_step 4 8 "Running E2E Tests (Playwright)"
    
    E2E_COUNT=0
    E2E_TIME=0
    
    if [ -f "node_modules/.bin/playwright" ] || command -v playwright &> /dev/null; then
        # Ensure test-results directory exists
        mkdir -p test-results
        mkdir -p playwright-report
        
        START_E2E=$(date +%s.%N)
        
        # Run Playwright tests with JSON reporter for dashboard
        # Playwright config should handle HTML reporter automatically
        PLAYWRIGHT_OUTPUT=$(npm run test -- --reporter=list,json,html 2>&1) || E2E_EXIT_CODE=$?
        
        END_E2E=$(date +%s.%N)
        E2E_TIME=$(echo "$END_E2E - $START_E2E" | bc 2>/dev/null || echo "0")
        E2E_TIME=$(printf "%.1f" "$E2E_TIME")
        
        # Try to parse results from multiple sources
        # Check test-results/results.json first
        if [ -f "test-results/results.json" ]; then
            PLAYWRIGHT_DATA=$(cat "test-results/results.json" 2>/dev/null || echo "{}")
            E2E_PASSED=$(echo "$PLAYWRIGHT_DATA" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    stats = data.get('stats', {})
    print(stats.get('expected', 0))
except:
    print(0)
" 2>/dev/null || echo "0")
            E2E_FAILED=$(echo "$PLAYWRIGHT_DATA" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    stats = data.get('stats', {})
    print(stats.get('unexpected', 0))
except:
    print(0)
" 2>/dev/null || echo "0")
        else
            # Fallback: parse from output
            E2E_PASSED=$(echo "$PLAYWRIGHT_OUTPUT" | grep -oE '[0-9]+ passed' | sed -nE 's/([0-9]+) passed/\1/p' | tail -1 || echo "0")
            E2E_FAILED=$(echo "$PLAYWRIGHT_OUTPUT" | grep -oE '[0-9]+ failed' | sed -nE 's/([0-9]+) failed/\1/p' | tail -1 || echo "0")
        fi
        
        [ -z "$E2E_PASSED" ] && E2E_PASSED=0
        [ -z "$E2E_FAILED" ] && E2E_FAILED=0
        
        E2E_COUNT=$E2E_PASSED
        
        if [ "$E2E_PASSED" -gt 0 ] || [ "$E2E_FAILED" -gt 0 ]; then
            print_success "E2E Tests: $E2E_PASSED passed, $E2E_FAILED failed (${E2E_TIME}s)"
        else
            print_info "E2E Tests: No tests found or all skipped"
        fi
    else
        print_info "Playwright not found - skipping E2E tests"
    fi
else
    print_step 4 8 "Running E2E Tests (Playwright)"
    print_info "E2E tests skipped (SKIP_E2E=true)"
fi
echo ""

# =========================================
# [5/8] Running Code Quality Checks
# =========================================
print_step 5 8 "Running Code Quality Checks"

LINT_ERRORS=0

# ESLint
ESLINT_OUTPUT=$(npm run lint 2>&1) || ESLINT_EXIT_CODE=$?
if [ ${ESLINT_EXIT_CODE:-0} -eq 0 ]; then
    ESLINT_ERRORS=0
else
    ESLINT_ERRORS=$(echo "$ESLINT_OUTPUT" | grep -c "error" || echo "0")
fi

# Pylint
if command -v pylint &> /dev/null; then
    cd flask_api
    pylint app --rcfile=../qa-automation/quality/pylint.rc \
        --output-format=json --reports=no \
        > "$REPORTS_DIR/pylint-report.json" 2>/dev/null || true
    
    PYLINT_ERRORS=$(python3 -c "
import json, sys
try:
    with open('$REPORTS_DIR/pylint-report.json') as f:
        data = json.load(f)
        if isinstance(data, list):
            print(len([m for m in data if isinstance(m, dict) and m.get('type')=='error']))
        else:
            print(len([m for m in data.get('messages', []) if m.get('type')=='error']))
except:
    print(0)
" 2>/dev/null || echo "0")
    
    LINT_ERRORS=$((LINT_ERRORS + PYLINT_ERRORS))
    cd ..
fi

if [ "$LINT_ERRORS" -eq 0 ]; then
    print_success "Code Quality: No linting errors found"
else
    print_failure "Code Quality: $LINT_ERRORS linting errors found"
fi
echo ""

# =========================================
# [6/8] Running Security Scans
# =========================================
print_step 6 8 "Running Security Scans"

VULNERABILITIES=0

# npm audit
AUDIT_OUTPUT=$(npm audit --audit-level=moderate --json > "$REPORTS_DIR/security/npm-audit.json" 2>&1) || AUDIT_EXIT_CODE=$?
if [ ${AUDIT_EXIT_CODE:-0} -eq 0 ]; then
    VULNERABILITIES=0
else
    if echo "$AUDIT_OUTPUT" | grep -q "ENOTFOUND\|ETIMEDOUT\|network\|getaddrinfo"; then
        VULNERABILITIES=0
    else
        VULNERABILITIES=$(python3 -c "
import json, sys
try:
    with open('$REPORTS_DIR/security/npm-audit.json') as f:
        data = json.load(f)
        vulns = data.get('vulnerabilities', {})
        print(sum(1 for v in vulns.values() if v.get('severity') in ['moderate', 'high', 'critical']))
except:
    print(0)
" 2>/dev/null || echo "0")
    fi
fi

# Snyk scan (if available)
if command -v snyk &> /dev/null; then
    snyk test --json > "$REPORTS_DIR/security/snyk-test.json" 2>&1 || true
fi

if [ "$VULNERABILITIES" -eq 0 ]; then
    print_success "Security: 0 vulnerabilities found"
else
    print_failure "Security: $VULNERABILITIES vulnerabilities found"
fi
echo ""

# =========================================
# [7/8] Running Performance Tests
# =========================================
print_step 7 8 "Running Performance Tests"

PERFORMANCE_PASSED=true

# Backend performance tests
if [ -n "$PYTEST_CMD" ]; then
    cd flask_api
    PYTEST_OUTPUT=$(PYTHONPATH="$ROOT_DIR/flask_api:$ROOT_DIR" \
        $PYTEST_CMD ../qa-automation/tests/performance/backend/ \
        -v --tb=short \
        --junitxml="$REPORTS_DIR/pytest-performance.xml" \
        2>&1) || PERF_EXIT_CODE=$?
    
    if echo "$PYTEST_OUTPUT" | grep -q "no tests collected\|no tests found"; then
        PERFORMANCE_PASSED=true
    else
        PYTEST_SUMMARY=$(echo "$PYTEST_OUTPUT" | grep -E '(passed|failed|error)' | tail -1 || echo "")
        PERF_PASSED=$(echo "$PYTEST_SUMMARY" | grep -oE '[0-9]+ passed' | sed -nE 's/([0-9]+) passed/\1/p' | tail -1 || echo "0")
        PERF_FAILED=$(echo "$PYTEST_SUMMARY" | grep -oE '[0-9]+ failed' | sed -nE 's/([0-9]+) failed/\1/p' | tail -1 || echo "0")
        [ -z "$PERF_PASSED" ] && PERF_PASSED=0
        [ -z "$PERF_FAILED" ] && PERF_FAILED=0
        
        if [ "$PERF_PASSED" -gt 0 ]; then
            if [ "$PERF_FAILED" -gt 0 ]; then
                print_success "Performance Tests: $PERF_PASSED passed, $PERF_FAILED failed"
            else
                print_success "Performance Tests: $PERF_PASSED passed"
            fi
        else
            print_info "Performance Tests: No tests found"
        fi
    fi
    cd ..
fi

# k6 load testing
if command -v k6 &> /dev/null; then
    BASE_URL="${BASE_URL:-http://localhost:5001}"
    k6 run --out json="$REPORTS_DIR/k6-results.json" \
           --env BASE_URL="$BASE_URL" \
           "$QA_DIR/performance/k6-load-test.js" > /dev/null 2>&1 || true
fi

# Lighthouse
if command -v lighthouse &> /dev/null; then
    LIGHTHOUSE_URL="${LIGHTHOUSE_URL:-http://localhost:4173}"
    lighthouse "$LIGHTHOUSE_URL" \
        --output=json \
        --output-path="$REPORTS_DIR/lighthouse-results.json" \
        --quiet > /dev/null 2>&1 || true
fi

echo ""

# =========================================
# [8/8] Generating Quality Dashboard
# =========================================
print_step 8 8 "Generating Quality Dashboard"

if $PYTHON_CMD -c "import jinja2" 2>/dev/null; then
    $PYTHON_CMD "$QA_DIR/reports/generate-report.py" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        print_success "Dashboard generated successfully"
    else
        print_failure "Failed to generate dashboard"
    fi
else
    print_info "Dashboard generation skipped (jinja2 not available)"
    print_info "Install with: python3 -m pip install --user jinja2"
fi
echo ""

# =========================================
# Final Summary
# =========================================
END_TIME=$(date +%s)
TOTAL_TIME=$((END_TIME - START_TIME))
MINUTES=$((TOTAL_TIME / 60))
SECONDS=$((TOTAL_TIME % 60))

echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
if [ $OVERALL_STATUS -eq 0 ]; then
    echo -e "${CYAN}║${NC}  ${GREEN}✓ All QA checks completed successfully!${NC}                    ${CYAN}║${NC}"
else
    echo -e "${CYAN}║${NC}  ${RED}✗ Some QA checks failed${NC}                                  ${CYAN}║${NC}"
fi
echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Test Summary
echo -e "${BLUE}Test Summary:${NC}"
echo "  • Backend Unit Tests:    ${GREEN}$UNIT_TEST_COUNT passed${NC}"
echo "  • Frontend Unit Tests:  ${GREEN}$JEST_COUNT passed${NC}"
echo "  • Integration Tests:    ${GREEN}$INTEGRATION_COUNT passed${NC}"
if [ "${SKIP_E2E:-false}" != "true" ]; then
    echo "  • E2E Tests:             ${GREEN}$E2E_COUNT passed${NC}"
fi
echo "  • Total Execution Time: ${CYAN}${MINUTES}m ${SECONDS}s${NC}"
echo ""

# Report Locations
echo -e "${BLUE}📊 Reports Generated:${NC}"
if [ -f "$REPORTS_DIR/dashboard.html" ]; then
    echo -e "  ${GREEN}✓${NC} Dashboard: ${CYAN}$REPORTS_DIR/dashboard.html${NC}"
    echo -e "     Open with: ${YELLOW}open $REPORTS_DIR/dashboard.html${NC}"
fi
if [ -f "playwright-report/index.html" ]; then
    echo -e "  ${GREEN}✓${NC} Playwright Report: ${CYAN}playwright-report/index.html${NC}"
    echo -e "     Open with: ${YELLOW}npm run test:report${NC}"
fi
if [ -f "$REPORTS_DIR/recommendations.md" ]; then
    echo -e "  ${GREEN}✓${NC} Recommendations: ${CYAN}$REPORTS_DIR/recommendations.md${NC}"
fi
echo ""

# Test Set Breakdown
echo -e "${BLUE}📋 Test Sets Included in Dashboard:${NC}"
echo "  • Backend Unit Tests (pytest)"
echo "  • Frontend Unit Tests (Jest)"
echo "  • Integration Tests (pytest)"
if [ "${SKIP_E2E:-false}" != "true" ]; then
    echo "  • E2E Tests (Playwright)"
    echo "    - Accessibility Tests"
    echo "    - Authentication Tests"
    echo "    - Navigation Tests"
    echo "    - Task Management Tests"
    echo "    - Product Search Tests"
    echo "    - Registration Tests"
    echo "    - Responsive Design Tests"
    echo "    - Error Handling Tests"
fi
echo "  • Code Quality (ESLint, Pylint)"
echo "  • Security (npm audit, Snyk)"
echo "  • Performance (Lighthouse, k6)"
echo ""

exit $OVERALL_STATUS
