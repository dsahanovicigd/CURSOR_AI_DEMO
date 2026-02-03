# Development Scripts

Scripts for managing development environment and services.

## Scripts

- **start-all-services.sh** - Start all application services (frontend, backend, Redis, Celery)
- **stop-all-services.sh** - Stop all application services
- **investigate_redis.sh** - Investigate Redis connection and activity

## Usage

```bash
# Start all services
./scripts/development/start-all-services.sh

# Stop all services
./scripts/development/stop-all-services.sh

# Investigate Redis
./scripts/development/investigate_redis.sh
```
