#!/bin/bash
# Standalone Lighthouse Runner
# Handles server startup and Lighthouse execution

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
REPORTS_DIR="$SCRIPT_DIR/../reports"

cd "$ROOT_DIR"

echo "🔍 Running Lighthouse Performance Tests"
echo ""

# Check if Lighthouse is available
LIGHTHOUSE_CMD=""
if command -v lighthouse &> /dev/null; then
    LIGHTHOUSE_CMD="lighthouse"
elif command -v npx &> /dev/null; then
    LIGHTHOUSE_CMD="npx lighthouse"
else
    echo "❌ Lighthouse not found. Install with: npm install -g lighthouse"
    echo "   Or use: npx lighthouse"
    exit 1
fi

# Check if server is already running
LIGHTHOUSE_URL=""
PREVIEW_PID=""

if curl -s http://localhost:4173 > /dev/null 2>&1; then
    LIGHTHOUSE_URL="http://localhost:4173"
    echo "✅ Using existing preview server on port 4173"
elif curl -s http://localhost:5173 > /dev/null 2>&1; then
    LIGHTHOUSE_URL="http://localhost:5173"
    echo "✅ Using existing dev server on port 5173"
else
    echo "📦 Building frontend..."
    if ! npm run build > /dev/null 2>&1; then
        echo "❌ Build failed"
        exit 1
    fi
    
    echo "🚀 Starting preview server..."
    
    # Try port 4173 first
    PREVIEW_PORT=4173
    if npm run preview -- --port $PREVIEW_PORT --host 127.0.0.1 > /tmp/preview-server.log 2>&1 &
    then
        PREVIEW_PID=$!
    else
        # Try alternative port
        PREVIEW_PORT=4174
        npm run preview -- --port $PREVIEW_PORT --host 127.0.0.1 > /tmp/preview-server.log 2>&1 &
        PREVIEW_PID=$!
    fi
    
    # Wait for server (max 30 seconds)
    echo "⏳ Waiting for server to start..."
    for i in {1..30}; do
        if curl -s "http://localhost:$PREVIEW_PORT" > /dev/null 2>&1; then
            LIGHTHOUSE_URL="http://localhost:$PREVIEW_PORT"
            echo "✅ Server ready on port $PREVIEW_PORT"
            break
        fi
        sleep 1
    done
    
    if [ -z "$LIGHTHOUSE_URL" ]; then
        echo "❌ Server failed to start"
        echo "   Check logs: cat /tmp/preview-server.log"
        [ -n "$PREVIEW_PID" ] && kill $PREVIEW_PID 2>/dev/null || true
        exit 1
    fi
fi

# Run Lighthouse
echo "🔍 Running Lighthouse on $LIGHTHOUSE_URL..."
mkdir -p "$REPORTS_DIR"

$LIGHTHOUSE_CMD "$LIGHTHOUSE_URL" \
    --output=json \
    --output-path="$REPORTS_DIR/lighthouse-results.json" \
    --chrome-flags="--headless --no-sandbox --disable-gpu --disable-dev-shm-usage" \
    --quiet 2>&1 | grep -v "LH:" || true

if [ -f "$REPORTS_DIR/lighthouse-results.json" ] && [ -s "$REPORTS_DIR/lighthouse-results.json" ]; then
    echo "✅ Lighthouse completed successfully"
    echo "   Results: $REPORTS_DIR/lighthouse-results.json"
    
    # Extract key metrics
    python3 -c "
import json
try:
    with open('$REPORTS_DIR/lighthouse-results.json') as f:
        data = json.load(f)
        categories = data.get('categories', {})
        print('\\n📊 Performance Scores:')
        print(f\"   Performance: {int(categories.get('performance', {}).get('score', 0) * 100)}/100\")
        print(f\"   Accessibility: {int(categories.get('accessibility', {}).get('score', 0) * 100)}/100\")
        print(f\"   Best Practices: {int(categories.get('best-practices', {}).get('score', 0) * 100)}/100\")
        print(f\"   SEO: {int(categories.get('seo', {}).get('score', 0) * 100)}/100\")
except Exception as e:
    print(f'   Could not parse results: {e}')
" 2>/dev/null || true
else
    echo "❌ Lighthouse results not generated"
    exit 1
fi

# Cleanup
if [ -n "$PREVIEW_PID" ]; then
    echo "🧹 Cleaning up preview server..."
    kill $PREVIEW_PID 2>/dev/null || true
    sleep 1
    kill -9 $PREVIEW_PID 2>/dev/null || true
fi

echo ""
echo "✅ Lighthouse test complete!"
