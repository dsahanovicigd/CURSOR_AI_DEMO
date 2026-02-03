#!/bin/bash
# Sanity Check Script - Runs a few tests from each test set
# Quick verification that dashboard displays results correctly

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
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
echo -e "${CYAN}║        QA Sanity Check - Few Tests from Each Set          ║${NC}"
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

# [1] Backend Unit Tests - Run 2-3 tests
echo -e "${BLUE}[1/7] Running Backend Unit Tests (2 tests)...${NC}"
if [ -n "$PYTEST_CMD" ]; then
    cd flask_api
    $PYTEST_CMD ../qa-automation/tests/unit/backend/test_auth.py::TestAuthentication::test_register_user \
                 ../qa-automation/tests/unit/backend/test_auth.py::TestAuthentication::test_login_success \
                 -v --junitxml="$REPORTS_DIR/pytest-unit.xml" 2>&1 | grep -E "passed|failed" | tail -1 || true
    cd ..
    echo -e "${GREEN}✓ Unit tests completed${NC}"
else
    echo -e "${YELLOW}⚠ pytest not found${NC}"
fi
echo ""

# [2] Frontend Unit Tests (Jest)
echo -e "${BLUE}[2/7] Running Frontend Unit Tests (Jest)...${NC}"
if [ -f "node_modules/.bin/jest" ] || command -v jest &> /dev/null; then
    npm run test:jest -- --passWithNoTests --silent --json > "$REPORTS_DIR/jest-results.json" 2>&1 || true
    echo -e "${GREEN}✓ Jest tests completed${NC}"
else
    echo -e "${YELLOW}⚠ Jest not found${NC}"
fi
echo ""

# [3] Integration Tests - Run 2-3 tests
echo -e "${BLUE}[3/7] Running Integration Tests (2 tests)...${NC}"
if [ -n "$PYTEST_CMD" ]; then
    cd flask_api
    $PYTEST_CMD ../qa-automation/tests/integration/backend/test_comprehensive_api_suite.py \
                 -k "test_get_users or test_create_user" \
                 -v --junitxml="$REPORTS_DIR/pytest-integration.xml" 2>&1 | grep -E "passed|failed" | tail -1 || true
    cd ..
    echo -e "${GREEN}✓ Integration tests completed${NC}"
else
    echo -e "${YELLOW}⚠ pytest not found${NC}"
fi
echo ""

# [4] Performance Tests - Run 1-2 tests
echo -e "${BLUE}[4/7] Running Performance Tests (2 tests)...${NC}"
if [ -n "$PYTEST_CMD" ]; then
    cd flask_api
    $PYTEST_CMD ../qa-automation/tests/performance/backend/test_performance.py \
                 -k "test_api_response_time or test_database_query_performance" \
                 -v --junitxml="$REPORTS_DIR/pytest-performance.xml" 2>&1 | grep -E "passed|failed" | tail -1 || true
    cd ..
    echo -e "${GREEN}✓ Performance tests completed${NC}"
else
    echo -e "${YELLOW}⚠ pytest not found${NC}"
fi
echo ""

# [5] Code Quality (Pylint) - Check one file
echo -e "${BLUE}[5/7] Running Code Quality Checks (Pylint)...${NC}"
if command -v pylint &> /dev/null; then
    cd flask_api
    pylint app/auth.py --rcfile=../qa-automation/quality/pylint.rc \
        --output-format=json --reports=no \
        > "$REPORTS_DIR/pylint-report.json" 2>/dev/null || true
    cd ..
    echo -e "${GREEN}✓ Pylint check completed${NC}"
else
    echo -e "${YELLOW}⚠ Pylint not found${NC}"
fi
echo ""

# [6] Security Scan
echo -e "${BLUE}[6/7] Running Security Scan (npm audit)...${NC}"
npm audit --audit-level=moderate --json > "$REPORTS_DIR/security/npm-audit.json" 2>&1 || true
echo -e "${GREEN}✓ Security scan completed${NC}"
echo ""

# [7] Generate Dashboard
echo -e "${BLUE}[7/7] Generating Dashboard...${NC}"
if [ -n "$VENV_PYTHON" ] && $VENV_PYTHON -c "import jinja2" 2>/dev/null; then
    $VENV_PYTHON "$QA_DIR/reports/generate_dashboard.py" 2>&1 | tail -1
    echo -e "${GREEN}✓ Dashboard generated${NC}"
else
    echo -e "${YELLOW}⚠ Dashboard generation skipped (jinja2 not available)${NC}"
fi
echo ""

# Summary
echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║              Sanity Check Complete!                       ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📊 View Dashboard:${NC}"
echo -e "  ${CYAN}$REPORTS_DIR/dashboard.html${NC}"
echo ""
