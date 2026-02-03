#!/bin/bash

# Master Script to Stop All Services
# Stops Frontend, Backend API, Redis (optional), and Celery Worker

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$ROOT_DIR"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   Stopping All Services${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to kill process by PID file
kill_by_pid_file() {
    local pid_file=$1
    local service_name=$2
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p "$pid" > /dev/null 2>&1; then
            echo -e "${YELLOW}Stopping $service_name (PID: $pid)...${NC}"
            kill "$pid" 2>/dev/null || kill -9 "$pid" 2>/dev/null || true
            rm -f "$pid_file"
            echo -e "${GREEN}✓ $service_name stopped${NC}"
        else
            echo -e "${YELLOW}⚠ $service_name not running (stale PID file)${NC}"
            rm -f "$pid_file"
        fi
    fi
}

# Function to kill processes by name pattern
kill_by_pattern() {
    local pattern=$1
    local service_name=$2
    
    local pids=$(pgrep -f "$pattern" 2>/dev/null || true)
    if [ -n "$pids" ]; then
        echo -e "${YELLOW}Stopping $service_name...${NC}"
        echo "$pids" | xargs kill 2>/dev/null || echo "$pids" | xargs kill -9 2>/dev/null || true
        echo -e "${GREEN}✓ $service_name stopped${NC}"
    else
        echo -e "${YELLOW}⚠ $service_name not running${NC}"
    fi
}

# 1. Stop Frontend
echo -e "${BLUE}[1/4] Stopping Frontend...${NC}"
kill_by_pid_file "$ROOT_DIR/frontend.pid" "Frontend"
kill_by_pattern "vite" "Frontend (by pattern)"
echo ""

# 2. Stop Backend API
echo -e "${BLUE}[2/4] Stopping Backend API...${NC}"
kill_by_pid_file "$ROOT_DIR/backend.pid" "Backend API"
kill_by_pattern "python.*run.py" "Backend API (by pattern)"
echo ""

# 3. Stop Celery Worker
echo -e "${BLUE}[3/4] Stopping Celery Worker...${NC}"
kill_by_pid_file "$ROOT_DIR/celery.pid" "Celery Worker"
kill_by_pattern "celery.*worker" "Celery Worker (by pattern)"
echo ""

# 4. Stop Redis (optional - ask user)
echo -e "${BLUE}[4/4] Redis Status...${NC}"
if command -v redis-cli >/dev/null 2>&1; then
    if redis-cli ping >/dev/null 2>&1; then
        read -p "Stop Redis? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            if command -v brew >/dev/null 2>&1; then
                brew services stop redis 2>/dev/null || true
                echo -e "${GREEN}✓ Redis stopped${NC}"
            elif command -v docker >/dev/null 2>&1; then
                docker stop redis 2>/dev/null || true
                echo -e "${GREEN}✓ Redis container stopped${NC}"
            else
                kill_by_pattern "redis-server" "Redis"
            fi
        else
            echo -e "${YELLOW}⚠ Redis left running${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ Redis not running${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Redis CLI not found${NC}"
fi
echo ""

# Clean up log files (optional)
read -p "Remove log files? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f "$ROOT_DIR/backend.log" "$ROOT_DIR/frontend.log" "$ROOT_DIR/celery.log"
    echo -e "${GREEN}✓ Log files removed${NC}"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}   All Services Stopped!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
