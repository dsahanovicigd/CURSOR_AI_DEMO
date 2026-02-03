#!/bin/bash

# Flask API Startup Script
# Ensures port 5001 is used to avoid macOS AirPlay Receiver conflict

cd "$(dirname "$0")"

# Stop any existing Flask processes first
echo "🧹 Cleaning up any existing Flask processes..."
pkill -f "python.*run.py" 2>/dev/null
sleep 1

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found. Run ./setup.sh first."
    exit 1
fi

# Force port 5001 (override any .env settings)
export FLASK_PORT=5001
export FLASK_ENV=development

# Check if port is still in use
if lsof -i :5001 > /dev/null 2>&1; then
    echo "⚠️  Port 5001 is still in use. Trying to free it..."
    lsof -ti :5001 | xargs kill -9 2>/dev/null
    sleep 2
fi

echo "🚀 Starting Flask API on port 5001..."
echo "📚 Swagger UI: http://localhost:5001/api/docs"
echo "💚 Health Check: http://localhost:5001/api/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python run.py
