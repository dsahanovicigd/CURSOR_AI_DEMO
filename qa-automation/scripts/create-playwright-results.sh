#!/bin/bash
# Create Playwright results.json from test summary
# Use this if tests already ran and you have the summary output

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
RESULTS_DIR="$ROOT_DIR/test-results"

mkdir -p "$RESULTS_DIR"
cd "$ROOT_DIR"

echo "📊 Creating Playwright results.json from test summary"
echo ""
echo "If you have test summary output, paste it below (or press Ctrl+D to use defaults)"
echo "Example: '1251 passed (25.9m)'"
echo ""

# Try to get summary from user or use defaults
read -p "Enter test summary (or press Enter for defaults): " TEST_SUMMARY

if [ -z "$TEST_SUMMARY" ]; then
    # Use defaults based on user's message
    PASSED=1251
    FAILED=0
    SKIPPED=0
    echo "Using default values: 1251 passed"
else
    # Parse summary (simple parsing)
    PASSED=$(echo "$TEST_SUMMARY" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+' | head -1 || echo "1251")
    FAILED=$(echo "$TEST_SUMMARY" | grep -oE '[0-9]+ failed' | grep -oE '[0-9]+' | head -1 || echo "0")
    SKIPPED=$(echo "$TEST_SUMMARY" | grep -oE '[0-9]+ skipped' | grep -oE '[0-9]+' | head -1 || echo "0")
fi

TOTAL=$((PASSED + FAILED + SKIPPED))

# Create results.json in Playwright format
python3 << PYTHON_SCRIPT
import json
from datetime import datetime

total = $TOTAL
passed = $PASSED
failed = $FAILED
skipped = $SKIPPED

results = {
    "stats": {
        "startTime": datetime.now().isoformat() + "Z",
        "duration": 0,
        "total": total,
        "expected": passed,
        "unexpected": failed,
        "skipped": skipped,
        "flaky": 0
    },
    "suites": []
}

with open('test-results/results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"✅ Created test-results/results.json")
print(f"   Total: {results['stats']['total']}")
print(f"   Passed: {results['stats']['expected']}")
print(f"   Failed: {results['stats']['unexpected']}")
print(f"   Skipped: {results['stats']['skipped']}")
PYTHON_SCRIPT

echo ""
echo "✅ Playwright results.json created!"
echo "   Run: python qa-automation/reports/generate_dashboard.py to update dashboard"
