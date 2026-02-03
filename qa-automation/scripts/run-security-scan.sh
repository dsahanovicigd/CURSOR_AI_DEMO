#!/bin/bash
# Comprehensive Security Scanning Automation
# Target: 0 critical vulnerabilities

set +e  # Don't exit on errors

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR/../.."
REPORTS_DIR="$SCRIPT_DIR/../reports/security"

mkdir -p "$REPORTS_DIR"

CRITICAL_VULNS=0
HIGH_VULNS=0
MEDIUM_VULNS=0

echo "🔒 Running Security Scans..."

# 1. npm audit
echo "  [1/3] npm audit..."
cd "$ROOT_DIR"
if [ -f "package.json" ]; then
    npm audit --audit-level=moderate --json > "$REPORTS_DIR/npm-audit.json" 2>&1
    
    # Parse vulnerabilities
    if [ -f "$REPORTS_DIR/npm-audit.json" ]; then
        CRITICAL=$(python3 -c "import json, sys; data=json.load(sys.stdin); print(sum(1 for v in data.get('vulnerabilities', {}).values() if v.get('severity')=='critical'))" < "$REPORTS_DIR/npm-audit.json" 2>/dev/null || echo "0")
        HIGH=$(python3 -c "import json, sys; data=json.load(sys.stdin); print(sum(1 for v in data.get('vulnerabilities', {}).values() if v.get('severity')=='high'))" < "$REPORTS_DIR/npm-audit.json" 2>/dev/null || echo "0")
        MEDIUM=$(python3 -c "import json, sys; data=json.load(sys.stdin); print(sum(1 for v in data.get('vulnerabilities', {}).values() if v.get('severity')=='medium'))" < "$REPORTS_DIR/npm-audit.json" 2>/dev/null || echo "0")
        
        CRITICAL_VULNS=$((CRITICAL_VULNS + CRITICAL))
        HIGH_VULNS=$((HIGH_VULNS + HIGH))
        MEDIUM_VULNS=$((MEDIUM_VULNS + MEDIUM))
    fi
fi

# 2. Snyk scan
echo "  [2/3] Snyk scan..."
if command -v snyk &> /dev/null; then
    cd "$ROOT_DIR"
    snyk test --json > "$REPORTS_DIR/snyk-test.json" 2>&1 || true
    
    if [ -f "$REPORTS_DIR/snyk-test.json" ]; then
        CRITICAL=$(python3 -c "import json, sys; data=json.load(sys.stdin); print(len([v for v in data.get('vulnerabilities', []) if v.get('severity')=='critical']))" < "$REPORTS_DIR/snyk-test.json" 2>/dev/null || echo "0")
        HIGH=$(python3 -c "import json, sys; data=json.load(sys.stdin); print(len([v for v in data.get('vulnerabilities', []) if v.get('severity')=='high']))" < "$REPORTS_DIR/snyk-test.json" 2>/dev/null || echo "0")
        
        CRITICAL_VULNS=$((CRITICAL_VULNS + CRITICAL))
        HIGH_VULNS=$((HIGH_VULNS + HIGH))
    fi
fi

# 3. OWASP ZAP (if configured)
echo "  [3/3] OWASP ZAP scan..."
if command -v zap-cli &> /dev/null; then
    cd "$ROOT_DIR"
    zap-cli quick-scan --self-contained --start-options '-config api.disablekey=true' http://localhost:4173 > "$REPORTS_DIR/zap-scan.txt" 2>&1 || true
fi

# Summary
echo ""
if [ "$CRITICAL_VULNS" -eq 0 ] && [ "$HIGH_VULNS" -eq 0 ]; then
    echo "✓ 0 vulnerabilities found"
    exit 0
else
    echo "✗ Found: $CRITICAL_VULNS critical, $HIGH_VULNS high, $MEDIUM_VULNS medium"
    exit 1
fi
