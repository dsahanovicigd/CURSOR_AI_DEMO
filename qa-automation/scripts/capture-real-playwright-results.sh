#!/bin/bash
# Capture REAL Playwright test results from actual test run
# This script runs Playwright and captures the actual JSON output with real pass/fail counts

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
RESULTS_DIR="$ROOT_DIR/test-results"

mkdir -p "$RESULTS_DIR"
cd "$ROOT_DIR"

echo "🎭 Capturing REAL Playwright test results..."
echo ""

# Run Playwright with JSON reporter - this will output JSON to stdout
# We need to capture this and save it properly
echo "Running Playwright tests (this may take a while)..."
echo ""

# Run with JSON reporter and capture output
PLAYWRIGHT_OUTPUT=$(SKIP_WEBSERVER=${SKIP_WEBSERVER:-true} npx playwright test --reporter=json 2>&1)

# Extract JSON from output
python3 << 'PYTHON_SCRIPT'
import json
import sys

content = sys.stdin.read()

# Find JSON object start
json_start = content.find('{')
if json_start < 0:
    print("❌ No JSON found in Playwright output", file=sys.stderr)
    sys.exit(1)

# Extract JSON by finding matching braces
json_str = content[json_start:]
brace_count = 0
json_end = -1

for i, char in enumerate(json_str):
    if char == '{':
        brace_count += 1
    elif char == '}':
        brace_count -= 1
        if brace_count == 0:
            json_end = i + 1
            break

if json_end < 0:
    print("❌ Could not find complete JSON object", file=sys.stderr)
    sys.exit(1)

# Extract and parse JSON
json_content = json_str[:json_end]

try:
    data = json.loads(json_content)
    
    # Save to file
    output_file = 'test-results/results.json'
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Print summary
    stats = data.get('stats', {})
    total = stats.get('total', 0)
    passed = stats.get('expected', 0)
    failed = stats.get('unexpected', 0)
    skipped = stats.get('skipped', 0)
    flaky = stats.get('flaky', 0)
    
    print(f"✅ Saved REAL Playwright results to {output_file}")
    print(f"")
    print(f"📊 REAL Test Results:")
    print(f"   Total Tests: {total}")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   ⏭️  Skipped: {skipped}")
    if flaky > 0:
        print(f"   🔄 Flaky: {flaky}")
    
    if total > 0:
        success_rate = (passed / total) * 100
        print(f"   Success Rate: {success_rate:.1f}%")
    
    # Validate results make sense
    if total > 100 and failed == 0 and skipped == 0:
        print(f"")
        print(f"⚠️  WARNING: 100% pass rate with {total} tests seems unlikely")
        print(f"   This might indicate an issue with test execution or result capture")
    
except json.JSONDecodeError as e:
    print(f"❌ Invalid JSON: {e}", file=sys.stderr)
    sys.exit(1)
PYTHON_SCRIPT <<< "$PLAYWRIGHT_OUTPUT"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Real Playwright test results captured"
    echo "   Run: python qa-automation/reports/generate_dashboard.py to update dashboard"
else
    echo "❌ Failed to capture Playwright results"
    exit 1
fi
