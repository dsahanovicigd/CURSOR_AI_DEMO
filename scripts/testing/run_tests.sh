#!/bin/bash
# Script to run tests with coverage

echo "🧪 Running tests with coverage..."
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run tests with coverage
pytest \
    --cov=app \
    --cov-report=html \
    --cov-report=term-missing \
    --cov-report=xml \
    --cov-fail-under=90 \
    -v \
    tests/

echo ""
echo "✅ Test coverage report generated in htmlcov/index.html"
