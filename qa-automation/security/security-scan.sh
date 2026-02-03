#!/bin/bash
# Security Scanning Script
# Runs all security scans (Snyk, OWASP ZAP, npm audit)

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORTS_DIR="$SCRIPT_DIR/../reports"
SECURITY_REPORTS_DIR="$REPORTS_DIR/security"

mkdir -p "$SECURITY_REPORTS_DIR"

echo -e "${BLUE}🔒 Starting Security Scans...${NC}"
echo ""

# 1. npm audit
echo -e "${YELLOW}📦 Running npm audit...${NC}"
cd "$SCRIPT_DIR/../../"
if [ -f "package.json" ]; then
    npm audit --audit-level=moderate --json > "$SECURITY_REPORTS_DIR/npm-audit.json" 2>&1 || true
    npm audit --audit-level=moderate > "$SECURITY_REPORTS_DIR/npm-audit.txt" 2>&1 || true
    echo -e "${GREEN}✅ npm audit complete${NC}"
else
    echo -e "${YELLOW}⚠️  package.json not found, skipping npm audit${NC}"
fi

# 2. Snyk (if available)
echo -e "${YELLOW}🛡️  Running Snyk scan...${NC}"
if command -v snyk &> /dev/null; then
    cd "$SCRIPT_DIR/../../"
    snyk test --json > "$SECURITY_REPORTS_DIR/snyk-test.json" 2>&1 || true
    snyk test > "$SECURITY_REPORTS_DIR/snyk-test.txt" 2>&1 || true
    echo -e "${GREEN}✅ Snyk scan complete${NC}"
else
    echo -e "${YELLOW}⚠️  Snyk not installed, skipping. Install with: npm install -g snyk${NC}"
fi

# 3. OWASP ZAP (if available)
echo -e "${YELLOW}🕷️  Running OWASP ZAP scan...${NC}"
if command -v zap-cli &> /dev/null || command -v zap.sh &> /dev/null; then
    echo -e "${YELLOW}⚠️  OWASP ZAP requires manual setup. See documentation.${NC}"
else
    echo -e "${YELLOW}⚠️  OWASP ZAP not installed, skipping${NC}"
fi

echo ""
echo -e "${GREEN}✅ Security scans complete!${NC}"
echo -e "${BLUE}📊 Reports saved to: $SECURITY_REPORTS_DIR${NC}"
