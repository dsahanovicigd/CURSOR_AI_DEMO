#!/usr/bin/env python3
"""
Parse actual Playwright test results from test-results directories
Counts actual passed/failed tests from result.json files
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def count_tests_from_directories(test_results_dir):
    """Count actual tests from test-results directories"""
    test_results_path = Path(test_results_dir)
    
    if not test_results_path.exists():
        return None
    
    stats = {
        'total': 0,
        'passed': 0,
        'failed': 0,
        'skipped': 0,
        'flaky': 0
    }
    
    # Find all result.json files
    result_files = list(test_results_path.glob('**/result.json'))
    
    # Also check for test result directories (not retry directories)
    test_dirs = [d for d in test_results_path.iterdir() 
                 if d.is_dir() and not d.name.startswith('.') and 'retry' not in d.name]
    
    print(f"Found {len(result_files)} result.json files")
    print(f"Found {len(test_dirs)} test directories")
    
    # Count from result.json files
    for result_file in result_files:
        try:
            with open(result_file) as f:
                data = json.load(f)
                status = data.get('status', 'unknown')
                if status == 'passed':
                    stats['passed'] += 1
                elif status == 'failed':
                    stats['failed'] += 1
                elif status == 'skipped':
                    stats['skipped'] += 1
                stats['total'] += 1
        except Exception as e:
            continue
    
    # If we didn't get good counts from result.json, try to estimate from directory names
    if stats['total'] == 0 and len(test_dirs) > 0:
        # Each directory might represent a test run
        # This is a fallback - better to use actual JSON results
        print(f"Warning: Could not parse result.json files, using directory count as estimate")
        stats['total'] = len(test_dirs)
    
    return stats

def main():
    """Main entry point"""
    test_results_dir = Path(__file__).parent.parent.parent / "test-results"
    
    print("🔍 Parsing actual Playwright test results...")
    print(f"   Looking in: {test_results_dir}")
    print()
    
    stats = count_tests_from_directories(test_results_dir)
    
    if not stats or stats['total'] == 0:
        print("❌ No test results found")
        print("   Run Playwright tests first: npx playwright test")
        return 1
    
    print(f"📊 Actual Test Results:")
    print(f"   Total: {stats['total']}")
    print(f"   Passed: {stats['passed']}")
    print(f"   Failed: {stats['failed']}")
    print(f"   Skipped: {stats['skipped']}")
    
    if stats['total'] > 0:
        success_rate = (stats['passed'] / stats['total']) * 100
        print(f"   Success Rate: {success_rate:.1f}%")
    
    # Create results.json in Playwright format
    results = {
        "stats": {
            "startTime": datetime.now().isoformat() + "Z",
            "duration": 0,
            "total": stats['total'],
            "expected": stats['passed'],
            "unexpected": stats['failed'],
            "skipped": stats['skipped'],
            "flaky": stats['flaky']
        },
        "suites": []
    }
    
    output_file = test_results_dir / "results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print()
    print(f"✅ Created {output_file}")
    print(f"   Run: python qa-automation/reports/generate_dashboard.py to update dashboard")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
