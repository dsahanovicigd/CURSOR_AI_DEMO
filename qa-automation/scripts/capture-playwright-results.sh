#!/bin/bash
# Capture Playwright JSON Results
# Extracts JSON output from Playwright and saves to test-results/results.json

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
RESULTS_DIR="$ROOT_DIR/test-results"

mkdir -p "$RESULTS_DIR"
cd "$ROOT_DIR"

echo "📊 Capturing Playwright test results..."

# Run Playwright with JSON reporter and capture full output
PLAYWRIGHT_OUTPUT=$(npx playwright test --reporter=json 2>&1)

# Extract JSON from output using Python (more reliable)
python3 << 'PYTHON_SCRIPT'
import json
import sys

# Read all input
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
    
    print(f"✅ Saved Playwright results to {output_file}")
    print(f"   Total: {total}")
    print(f"   Passed: {passed}")
    print(f"   Failed: {failed}")
    print(f"   Skipped: {skipped}")
    
except json.JSONDecodeError as e:
    print(f"❌ Invalid JSON: {e}", file=sys.stderr)
    sys.exit(1)
PYTHON_SCRIPT <<< "$PLAYWRIGHT_OUTPUT"

if [ $? -eq 0 ]; then
    echo "✅ Playwright results captured successfully"
else
    echo "❌ Failed to capture Playwright results"
    exit 1
fi
