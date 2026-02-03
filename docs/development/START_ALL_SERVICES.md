# How to Run All Services

Complete guide to start all services for the full-stack application.

## Services Overview

1. **Frontend** - React + Vite (Port 5173)
2. **Backend API** - Flask REST API (Port 5001)
3. **Redis** - Caching & Task Queue (Port 6379) - Optional but recommended
4. **Celery Worker** - Background Tasks - Optional

---

## Quick Start (All Services)

### Option 1: Using the Master Script (Recommended)

```bash
# Make script executable (first time only)
chmod +x start-all-services.sh

# Run all services
./start-all-services.sh
```

This will start all services in separate terminal windows/tabs.

### Option 2: Manual Start (Step by Step)

---

## Step-by-Step Guide

### 1. Start Redis (Optional but Recommended)

**macOS:**
```bash
# Install Redis (if not installed)
brew install redis

# Start Redis service
brew services start redis

# Or run manually
redis-server
```

**Linux (Ubuntu/Debian):**
```bash
# Install Redis (if not installed)
sudo apt-get install redis-server

# Start Redis service
sudo systemctl start redis

# Or run manually
redis-server
```

**Docker:**
```bash
docker run -d -p 6379:6379 --name redis redis
```

**Verify Redis is running:**
```bash
redis-cli ping
# Should return: PONG
```

---

### 2. Start Flask Backend API

**Terminal 1:**
```bash
cd flask_api

# Using startup script (recommended)
./start.sh

# Or manually:
source venv/bin/activate
python run.py
```

**Expected Output:**
```
🚀 Starting Flask API on port 5001...
📚 Swagger UI: http://localhost:5001/api/docs
💚 Health Check: http://localhost:5001/api/health
```

**Verify API is running:**
- Open browser: http://localhost:5001/api/health
- Should return: `{"status": "healthy"}`
- Swagger UI: http://localhost:5001/api/docs

---

### 3. Start Celery Worker (Optional - for Background Tasks)

**Terminal 2:**
```bash
cd flask_api
source venv/bin/activate

# Start Celery worker
celery -A app.celery_app.celery worker --loglevel=info

# Or using the worker script
python celery_worker.py
```

**Note:** Celery requires Redis to be running.

---

### 4. Start Frontend (React + Vite)

**Terminal 3:**
```bash
# From project root
npm install  # First time only

# Start development server
npm run dev
```

**Expected Output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**Verify Frontend is running:**
- Open browser: http://localhost:5173
- Should see the application interface

---

## Service URLs Summary

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:5173 | React application |
| **Backend API** | http://localhost:5001/api | Flask REST API |
| **API Docs** | http://localhost:5001/api/docs | Swagger UI |
| **Health Check** | http://localhost:5001/api/health | API status |
| **Redis** | localhost:6379 | Cache & task queue |

---

## Running Services in Background

### Using `screen` (Linux/macOS)

```bash
# Install screen (if needed)
# macOS: brew install screen
# Linux: sudo apt-get install screen

# Start screen session
screen -S flask-api
cd flask_api && ./start.sh
# Press Ctrl+A then D to detach

# Start another screen for frontend
screen -S frontend
npm run dev
# Press Ctrl+A then D to detach

# List sessions
screen -ls

# Reattach to session
screen -r flask-api
```

### Using `tmux` (Linux/macOS)

```bash
# Install tmux (if needed)
# macOS: brew install tmux
# Linux: sudo apt-get install tmux

# Start tmux session
tmux new -s services

# Split panes (Ctrl+B then %)
# Run Flask API in one pane
cd flask_api && ./start.sh

# Split again (Ctrl+B then ")
# Run frontend in another pane
npm run dev

# Detach: Ctrl+B then D
# Reattach: tmux attach -t services
```

---

## Stop All Services

### Stop Frontend
- Press `Ctrl+C` in the terminal running `npm run dev`

### Stop Backend API
- Press `Ctrl+C` in the terminal running Flask
- Or: `cd flask_api && ./stop.sh` (if available)

### Stop Celery Worker
- Press `Ctrl+C` in the terminal running Celery

### Stop Redis
```bash
# macOS
brew services stop redis

# Linux
sudo systemctl stop redis

# Docker
docker stop redis
```

---

## Troubleshooting

### Port Already in Use

**Port 5001 (Backend):**
```bash
# Find process using port 5001
lsof -i :5001

# Kill process
kill -9 <PID>
```

**Port 5173 (Frontend):**
```bash
# Find process using port 5173
lsof -i :5173

# Kill process
kill -9 <PID>
```

**Port 6379 (Redis):**
```bash
# Find process using port 6379
lsof -i :6379

# Kill process
kill -9 <PID>
```

### Backend Won't Start

1. **Check virtual environment:**
   ```bash
   cd flask_api
   source venv/bin/activate
   which python  # Should show venv path
   ```

2. **Check dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Check database:**
   ```bash
   flask db upgrade
   ```

### Frontend Can't Connect to Backend

1. **Verify backend is running:**
   ```bash
   curl http://localhost:5001/api/health
   ```

2. **Check CORS configuration:**
   - Backend `.env` should have: `CORS_ORIGINS=http://localhost:5173`
   - Restart backend after changing `.env`

3. **Check browser console:**
   - Open DevTools (F12)
   - Look for CORS errors or network errors

### Redis Connection Issues

1. **Verify Redis is running:**
   ```bash
   redis-cli ping
   ```

2. **Check Redis URL in backend `.env`:**
   ```
   REDIS_URL=redis://localhost:6379/0
   ```

---

## Development Workflow

### Typical Development Session

1. **Start Redis** (if using caching/background tasks)
   ```bash
   brew services start redis  # macOS
   ```

2. **Start Backend API**
   ```bash
   cd flask_api && ./start.sh
   ```

3. **Start Frontend**
   ```bash
   npm run dev
   ```

4. **Start Celery Worker** (if using background tasks)
   ```bash
   cd flask_api
   source venv/bin/activate
   celery -A app.celery_app.celery worker --loglevel=info
   ```

### Hot Reload

- **Frontend:** Vite automatically reloads on file changes
- **Backend:** Flask debug mode reloads on Python file changes
- **Celery:** Restart worker after code changes

---

## Production Deployment

For production, use:

- **Frontend:** `npm run build` → Serve static files with Nginx
- **Backend:** Gunicorn or uWSGI with Nginx reverse proxy
- **Redis:** Production Redis server
- **Celery:** Systemd service or supervisor

See individual service README files for production deployment details.

---

## Quick Reference Commands

```bash
# Start all services (manual)
redis-server &                    # Redis (background)
cd flask_api && ./start.sh &      # Backend (background)
npm run dev                       # Frontend (foreground)

# Check if services are running
curl http://localhost:5001/api/health    # Backend
curl http://localhost:5173               # Frontend
redis-cli ping                            # Redis

# Stop all services
pkill -f "python.*run.py"         # Stop Flask
pkill -f "vite"                   # Stop Frontend
brew services stop redis          # Stop Redis (macOS)
```
