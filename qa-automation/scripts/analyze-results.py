#!/usr/bin/env python3
"""
QA Results Analyzer
Analyzes test results and generates insights
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
REPORTS_DIR = SCRIPT_DIR.parent / "reports"
ROOT_DIR = SCRIPT_DIR.parent.parent

def load_json_file(filepath):
    """Load JSON file safely"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def analyze_test_results():
    """Analyze test results from various sources"""
    results = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "coverage": {}
        },
        "by_category": {
            "unit": {"passed": 0, "failed": 0, "total": 0},
            "integration": {"passed": 0, "failed": 0, "total": 0},
            "e2e": {"passed": 0, "failed": 0, "total": 0},
            "performance": {"passed": 0, "failed": 0, "total": 0}
        },
        "trends": [],
        "issues": []
    }
    
    # Analyze Jest results (if exists)
    jest_coverage = ROOT_DIR / "coverage" / "coverage-summary.json"
    if jest_coverage.exists():
        coverage_data = load_json_file(jest_coverage)
        if coverage_data:
            results["summary"]["coverage"]["frontend"] = {
                "lines": coverage_data.get("total", {}).get("lines", {}).get("pct", 0),
                "statements": coverage_data.get("total", {}).get("statements", {}).get("pct", 0),
                "functions": coverage_data.get("total", {}).get("functions", {}).get("pct", 0),
                "branches": coverage_data.get("total", {}).get("branches", {}).get("pct", 0)
            }
    
    # Analyze pytest results
    pytest_xml = ROOT_DIR / "test-results" / "results.xml"
    if pytest_xml.exists():
        try:
            import xml.etree.ElementTree as ET
            tree = ET.parse(pytest_xml)
            root = tree.getroot()
            
            total = int(root.get('tests', 0))
            failures = int(root.get('failures', 0))
            errors = int(root.get('errors', 0))
            skipped = int(root.get('skipped', 0))
            
            results["summary"]["total_tests"] += total
            results["summary"]["failed"] += failures + errors
            results["summary"]["skipped"] += skipped
            results["summary"]["passed"] += total - failures - errors - skipped
            
            results["by_category"]["unit"]["total"] += total
            results["by_category"]["unit"]["passed"] += total - failures - errors - skipped
            results["by_category"]["unit"]["failed"] += failures + errors
        except Exception as e:
            results["issues"].append(f"Error parsing pytest XML: {e}")
    
    # Analyze Playwright results
    playwright_json = ROOT_DIR / "test-results" / "results.json"
    if playwright_json.exists():
        playwright_data = load_json_file(playwright_json)
        if playwright_data:
            suites = playwright_data.get("suites", [])
            for suite in suites:
                specs = suite.get("specs", [])
                for spec in specs:
                    tests = spec.get("tests", [])
                    for test in tests:
                        results["by_category"]["e2e"]["total"] += 1
                        if test.get("results", [{}])[0].get("status") == "passed":
                            results["by_category"]["e2e"]["passed"] += 1
                        else:
                            results["by_category"]["e2e"]["failed"] += 1
    
    # Analyze dashboard data
    dashboard_data = REPORTS_DIR / "dashboard-data.json"
    if dashboard_data.exists():
        dashboard = load_json_file(dashboard_data)
        if dashboard:
            # Extract insights from dashboard
            if dashboard.get("backend_tests", {}).get("success_rate", 0) < 0.9:
                results["issues"].append("Backend test success rate below 90%")
            
            if dashboard.get("frontend_tests", {}).get("success_rate", 0) < 0.9:
                results["issues"].append("Frontend test success rate below 90%")
            
            pylint_score = dashboard.get("code_quality", {}).get("pylint_score", 0)
            if pylint_score < 8.0:
                results["issues"].append(f"Pylint score below target: {pylint_score}/10")
    
    # Calculate success rates
    for category in results["by_category"]:
        total = results["by_category"][category]["total"]
        if total > 0:
            passed = results["by_category"][category]["passed"]
            results["by_category"][category]["success_rate"] = round(passed / total * 100, 2)
    
    return results

def generate_insights(results):
    """Generate insights from analysis"""
    insights = []
    
    # Overall health
    total = results["summary"]["total_tests"]
    if total > 0:
        success_rate = (results["summary"]["passed"] / total) * 100
        if success_rate >= 95:
            insights.append("✅ Excellent test success rate")
        elif success_rate >= 80:
            insights.append("⚠️  Good test success rate, room for improvement")
        else:
            insights.append("❌ Test success rate needs attention")
    
    # Coverage insights
    coverage = results["summary"].get("coverage", {})
    if coverage.get("frontend", {}).get("lines", 0) < 70:
        insights.append("⚠️  Frontend coverage below 70% target")
    
    # Category insights
    for category, data in results["by_category"].items():
        if data["total"] > 0:
            rate = data.get("success_rate", 0)
            if rate < 80:
                insights.append(f"⚠️  {category.title()} tests: {rate}% success rate")
    
    return insights

def main():
    """Main analysis function"""
    print("🔍 Analyzing QA Results...")
    
    results = analyze_test_results()
    insights = generate_insights(results)
    
    # Save analysis results
    output_file = REPORTS_DIR / "analysis-results.json"
    with open(output_file, 'w') as f:
        json.dump({
            "analysis": results,
            "insights": insights
        }, f, indent=2)
    
    print("\n📊 Analysis Summary:")
    print(f"  Total Tests: {results['summary']['total_tests']}")
    print(f"  Passed: {results['summary']['passed']}")
    print(f"  Failed: {results['summary']['failed']}")
    print(f"  Skipped: {results['summary']['skipped']}")
    
    print("\n💡 Insights:")
    for insight in insights:
        print(f"  {insight}")
    
    print(f"\n✅ Analysis saved to: {output_file}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
