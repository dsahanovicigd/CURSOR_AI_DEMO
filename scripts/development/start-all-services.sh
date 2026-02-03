#!/bin/bash

# Master Script to Start All Services
# Starts Frontend, Backend API, Redis (optional), and Celery Worker (optional)

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$ROOT_DIR"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   Starting All Services${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is in use
port_in_use() {
    lsof -i :"$1" >/dev/null 2>&1
}

# Function to wait for a service to be ready
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=0
    
    echo -e "${YELLOW}Waiting for $service_name to be ready...${NC}"
    while [ $attempt -lt $max_attempts ]; do
        if curl -s "$url" >/dev/null 2>&1; then
            echo -e "${GREEN}✓ $service_name is ready!${NC}"
            return 0
        fi
        attempt=$((attempt + 1))
        sleep 1
    done
    echo -e "${RED}✗ $service_name failed to start${NC}"
    return 1
}

# 1. Check Redis (Optional)
echo -e "${BLUE}[1/4] Checking Redis...${NC}"
if command_exists redis-cli; then
    if redis-cli ping >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Redis is already running${NC}"
    else
        echo -e "${YELLOW}⚠ Redis is not running. Starting Redis...${NC}"
        if command_exists brew; then
            brew services start redis 2>/dev/null || redis-server &
        elif command_exists docker; then
            docker run -d -p 6379:6379 --name redis redis 2>/dev/null || echo "Redis container may already exist"
        else
            echo -e "${YELLOW}⚠ Please start Redis manually: redis-server${NC}"
        fi
        sleep 2
    fi
else
    echo -e "${YELLOW}⚠ Redis not found. Skipping (optional service)${NC}"
fi
echo ""

# 2. Start Flask Backend API
echo -e "${BLUE}[2/4] Starting Flask Backend API...${NC}"
if port_in_use 5001; then
    echo -e "${YELLOW}⚠ Port 5001 is already in use${NC}"
    read -p "Kill existing process? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        lsof -ti :5001 | xargs kill -9 2>/dev/null || true
        sleep 2
    else
        echo -e "${YELLOW}⚠ Skipping backend startup${NC}"
        SKIP_BACKEND=true
    fi
fi

if [ "$SKIP_BACKEND" != "true" ]; then
    cd flask_api
    
    if [ ! -d "venv" ]; then
        echo -e "${RED}✗ Virtual environment not found. Run ./setup.sh first${NC}"
        exit 1
    fi
    
    # Start backend in background
    echo -e "${GREEN}Starting Flask API on port 5001...${NC}"
    source venv/bin/activate
    export FLASK_PORT=5001
    export FLASK_ENV=development
    python run.py > "$ROOT_DIR/backend.log" 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > "$ROOT_DIR/backend.pid"
    
    cd "$ROOT_DIR"
    
    # Wait for backend to be ready
    sleep 3
    if wait_for_service "http://localhost:5001/api/health" "Backend API"; then
        echo -e "${GREEN}✓ Backend API: http://localhost:5001/api${NC}"
        echo -e "${GREEN}✓ Swagger UI: http://localhost:5001/api/docs${NC}"
    fi
fi
echo ""

# 3. Start Celery Worker (Optional)
echo -e "${BLUE}[3/4] Starting Celery Worker (Optional)...${NC}"
if command_exists celery && redis-cli ping >/dev/null 2>&1; then
    cd flask_api
    source venv/bin/activate
    celery -A app.celery_app.celery worker --loglevel=info > "$ROOT_DIR/celery.log" 2>&1 &
    CELERY_PID=$!
    echo $CELERY_PID > "$ROOT_DIR/celery.pid"
    cd "$ROOT_DIR"
    echo -e "${GREEN}✓ Celery worker started (PID: $CELERY_PID)${NC}"
else
    echo -e "${YELLOW}⚠ Skipping Celery worker (Redis not available or Celery not installed)${NC}"
fi
echo ""

# 4. Start Frontend
echo -e "${BLUE}[4/4] Starting Frontend...${NC}"
if port_in_use 5173; then
    echo -e "${YELLOW}⚠ Port 5173 is already in use${NC}"
    read -p "Kill existing process? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        lsof -ti :5173 | xargs kill -9 2>/dev/null || true
        sleep 2
    else
        echo -e "${YELLOW}⚠ Skipping frontend startup${NC}"
        SKIP_FRONTEND=true
    fi
fi

if [ "$SKIP_FRONTEND" != "true" ]; then
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}⚠ node_modules not found. Installing dependencies...${NC}"
        npm install
    fi
    
    echo -e "${GREEN}Starting Frontend on port 5173...${NC}"
    npm run dev > "$ROOT_DIR/frontend.log" 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > "$ROOT_DIR/frontend.pid"
    
    # Wait for frontend to be ready
    sleep 3
    if wait_for_service "http://localhost:5173" "Frontend"; then
        echo -e "${GREEN}✓ Frontend: http://localhost:5173${NC}"
    fi
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}   All Services Started!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${BLUE}Service URLs:${NC}"
echo -e "  Frontend:    ${GREEN}http://localhost:5173${NC}"
echo -e "  Backend API: ${GREEN}http://localhost:5001/api${NC}"
echo -e "  Swagger UI:  ${GREEN}http://localhost:5001/api/docs${NC}"
echo -e "  Health:      ${GREEN}http://localhost:5001/api/health${NC}"
echo ""
echo -e "${YELLOW}Logs:${NC}"
echo -e "  Backend:  tail -f $ROOT_DIR/backend.log"
echo -e "  Frontend: tail -f $ROOT_DIR/frontend.log"
echo -e "  Celery:   tail -f $ROOT_DIR/celery.log"
echo ""
echo -e "${BLUE}Run QA Tests (including E2E):${NC}"
echo -e "  ${GREEN}npm run qa${NC}                    # Run all QA tests (E2E enabled)"
echo -e "  ${GREEN}SKIP_E2E=true npm run qa${NC}     # Skip E2E tests"
echo ""
echo -e "${YELLOW}To stop all services:${NC}"
echo -e "  ./scripts/development/stop-all-services.sh"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop this script (services will continue running)${NC}"
echo ""

# Keep script running and handle Ctrl+C
trap 'echo ""; echo -e "${YELLOW}Services are still running in background${NC}"; echo -e "Run ./scripts/development/stop-all-services.sh to stop them${NC}"; exit 0' INT

# Wait for user interrupt
wait
