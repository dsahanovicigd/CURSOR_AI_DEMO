#!/bin/bash
# Generate Playwright JSON results for dashboard
# This ensures results.json is created even if tests fail

set -e

echo "🎭 Generating Playwright JSON results..."

# Ensure test-results directory exists
mkdir -p test-results

# Run Playwright tests with explicit JSON reporter
# The config already has JSON reporter, but we ensure it outputs correctly
echo "Running Playwright tests with JSON reporter..."
npm run test -- --reporter=json --reporter-option output=test-results/results.json || {
    echo "⚠️  Tests completed (some may have failed)"
}

# Verify results.json was created
if [ -f "test-results/results.json" ]; then
    echo "✅ Playwright results generated: test-results/results.json"
    
    # Show summary
    if command -v python3 &> /dev/null; then
        python3 << 'PYEOF'
import json
from pathlib import Path

results_file = Path('test-results/results.json')
if results_file.exists():
    try:
        with open(results_file) as f:
            data = json.load(f)
            stats = data.get('stats', {})
            total = stats.get('expected', 0) + stats.get('unexpected', 0) + stats.get('skipped', 0)
            passed = stats.get('expected', 0)
            failed = stats.get('unexpected', 0)
            skipped = stats.get('skipped', 0)
            
            if total > 0:
                print(f"   Total: {total}, Passed: {passed}, Failed: {failed}, Skipped: {skipped}")
            else:
                # Try suites structure
                suites = data.get('suites', [])
                if suites:
                    print(f"   Found {len(suites)} test suites")
    except Exception as e:
        print(f"   Error reading results: {e}")
PYEOF
    fi
else
    echo "❌ Error: test-results/results.json was not generated"
    echo "   Check Playwright configuration and test execution"
    exit 1
fi
