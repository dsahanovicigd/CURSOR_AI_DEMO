#!/bin/bash
# Run ALL Playwright E2E tests and capture complete results
# This ensures all 1900+ tests are captured, not just a summary

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
RESULTS_DIR="$ROOT_DIR/test-results"

mkdir -p "$RESULTS_DIR"
cd "$ROOT_DIR"

echo "🎭 Running ALL Playwright E2E Tests..."
echo ""

# Check if server is needed
if [ "$SKIP_WEBSERVER" != "true" ]; then
    # Check if dev server is running
    if ! curl -s http://localhost:5173 > /dev/null 2>&1; then
        echo "⚠️  Dev server not running. Starting with SKIP_WEBSERVER=true"
        export SKIP_WEBSERVER=true
    fi
fi

# Run Playwright with JSON reporter and capture full output
echo "Running tests (this may take a while for 1900+ tests)..."
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
    
    # Count actual tests from suites
    suites = data.get('suites', [])
    def count_tests_from_suites(suite_list):
        count = 0
        for suite in suite_list:
            tests = suite.get('tests', [])
            count += len(tests)
            child_suites = suite.get('suites', [])
            count += count_tests_from_suites(child_suites)
        return count
    
    actual_test_count = count_tests_from_suites(suites)
    
    print(f"✅ Saved Playwright results to {output_file}")
    print(f"")
    print(f"📊 Test Summary:")
    print(f"   Total Tests: {total}")
    if actual_test_count > 0:
        print(f"   Tests in Suites: {actual_test_count}")
    print(f"   Passed: {passed}")
    print(f"   Failed: {failed}")
    print(f"   Skipped: {skipped}")
    if flaky > 0:
        print(f"   Flaky: {flaky}")
    print(f"   Success Rate: {(passed/total*100) if total > 0 else 0:.1f}%")
    
except json.JSONDecodeError as e:
    print(f"❌ Invalid JSON: {e}", file=sys.stderr)
    sys.exit(1)
PYTHON_SCRIPT <<< "$PLAYWRIGHT_OUTPUT"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All Playwright test results captured successfully"
    echo "   Run: python qa-automation/reports/generate_dashboard.py to update dashboard"
else
    echo "❌ Failed to capture Playwright results"
    exit 1
fi
