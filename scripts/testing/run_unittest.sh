#!/bin/bash
# Test runner script for unittest test suite

set -e

echo "=========================================="
echo "User Profile Management - Unittest Suite"
echo "=========================================="
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run tests with different verbosity levels
VERBOSITY=${1:-2}

echo "Running unittest tests..."
echo "Verbosity level: $VERBOSITY"
echo ""

# Run the test suite
python -m unittest tests.test_user_profile_unittest -v

echo ""
echo "=========================================="
echo "Test execution completed"
echo "=========================================="

# Optional: Run with coverage if coverage is installed
if command -v coverage &> /dev/null; then
    echo ""
    echo "Running with coverage..."
    coverage run -m unittest tests.test_user_profile_unittest
    coverage report
    echo ""
    echo "Coverage HTML report generated in htmlcov/"
    coverage html
fi
