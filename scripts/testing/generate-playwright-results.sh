#!/bin/bash
# Generate Playwright JSON results for dashboard

set -e

echo "🎭 Generating Playwright test results..."

# Ensure test-results directory exists
mkdir -p test-results

# Run Playwright tests with JSON reporter
# The config already has JSON reporter, but we'll ensure it outputs correctly
npm run test -- --reporter=json --reporter-option output=test-results/results.json

echo "✅ Playwright results generated: test-results/results.json"
