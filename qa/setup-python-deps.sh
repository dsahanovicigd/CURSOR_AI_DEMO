#!/bin/bash
# Setup Python dependencies for QA automation scripts
# This script creates a virtual environment and installs required packages

set -e

echo "🐍 Setting up Python dependencies for QA automation..."

# Create virtual environment if it doesn't exist
if [ ! -d "qa/.venv" ]; then
    echo "Creating virtual environment in qa/.venv..."
    python3 -m venv qa/.venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source qa/.venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
echo "Installing Python packages..."
pip install jinja2 markdown pylint pylint-json2html pylint-flask

echo ""
echo "✅ Python dependencies installed successfully!"
echo ""
echo "To use the virtual environment manually:"
echo "  source qa/.venv/bin/activate"
echo ""
echo "The QA runner script will automatically use this virtual environment."
