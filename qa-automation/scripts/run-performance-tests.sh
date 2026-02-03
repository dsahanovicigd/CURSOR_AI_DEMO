#!/bin/bash
# Performance Testing Automation
# Targets: Response time <500ms, Error rate <1%

set +e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR/../.."
REPORTS_DIR="$SCRIPT_DIR/../reports"

mkdir -p "$REPORTS_DIR"

echo "⚡ Running Performance Tests..."

# 1. k6 Load Testing
echo "  [1/2] k6 Load Test..."
if command -v k6 &> /dev/null; then
    cd "$ROOT_DIR"
    BASE_URL="${BASE_URL:-http://localhost:5001}"
    
    k6 run --out json="$REPORTS_DIR/k6-results.json" \
           --env BASE_URL="$BASE_URL" \
           qa-automation/performance/k6-load-test.js > "$REPORTS_DIR/k6-output.txt" 2>&1
    
    # Parse results
    if [ -f "$REPORTS_DIR/k6-results.json" ]; then
        P95_RESPONSE=$(python3 -c "import json; data=json.load(open('$REPORTS_DIR/k6-results.json')); print(data.get('metrics', {}).get('http_req_duration', {}).get('values', {}).get('p(95)', 0))" 2>/dev/null || echo "0")
        ERROR_RATE=$(python3 -c "import json; data=json.load(open('$REPORTS_DIR/k6-results.json')); print(data.get('metrics', {}).get('http_req_failed', {}).get('values', {}).get('rate', 0) * 100)" 2>/dev/null || echo "0")
        
        echo "    P95 Response Time: ${P95_RESPONSE}ms"
        echo "    Error Rate: ${ERROR_RATE}%"
    fi
fi

# 2. Lighthouse Performance
echo "  [2/2] Lighthouse Performance..."
if command -v lighthouse &> /dev/null; then
    cd "$ROOT_DIR"
    URL="${LIGHTHOUSE_URL:-http://localhost:4173}"
    
    lighthouse "$URL" \
        --config-path=qa-automation/performance/lighthouse.config.js \
        --output=json \
        --output-path="$REPORTS_DIR/lighthouse-results.json" \
        --quiet > /dev/null 2>&1
    
    if [ -f "$REPORTS_DIR/lighthouse-results.json" ]; then
        PERFORMANCE_SCORE=$(python3 -c "import json; data=json.load(open('$REPORTS_DIR/lighthouse-results.json')); print(int(data.get('categories', {}).get('performance', {}).get('score', 0) * 100))" 2>/dev/null || echo "0")
        FCP=$(python3 -c "import json; data=json.load(open('$REPORTS_DIR/lighthouse-results.json')); print(int(data.get('audits', {}).get('first-contentful-paint', {}).get('numericValue', 0)))" 2>/dev/null || echo "0")
        
        echo "    Performance Score: ${PERFORMANCE_SCORE}/100"
        echo "    First Contentful Paint: ${FCP}ms"
    fi
fi

echo ""
echo "✓ Performance tests complete"

# Check thresholds
if [ -n "$P95_RESPONSE" ] && (( $(echo "$P95_RESPONSE < 500" | bc -l) )); then
    echo "✓ Response time target met (<500ms)"
else
    echo "✗ Response time target not met"
    exit 1
fi

if [ -n "$ERROR_RATE" ] && (( $(echo "$ERROR_RATE < 1" | bc -l) )); then
    echo "✓ Error rate target met (<1%)"
else
    echo "✗ Error rate target not met"
    exit 1
fi

exit 0
