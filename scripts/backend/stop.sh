#!/bin/bash

# Stop Flask API Script

echo "🛑 Stopping Flask API processes..."

# Kill any Flask processes
pkill -f "python.*run.py" 2>/dev/null
pkill -f "flask run" 2>/dev/null

sleep 1

# Check if any are still running
if pgrep -f "python.*run.py" > /dev/null; then
    echo "⚠️  Some processes still running. Force killing..."
    pkill -9 -f "python.*run.py"
fi

echo "✅ Flask API stopped"
