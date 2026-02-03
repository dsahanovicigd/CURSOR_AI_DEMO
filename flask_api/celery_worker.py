#!/usr/bin/env python3
"""
Celery worker entry point

Usage:
    python celery_worker.py
    # Or use Celery CLI directly:
    celery -A celery_worker:celery worker --loglevel=info
"""
import sys
from app import create_app

# Create Flask app to initialize Celery with proper configuration
app = create_app()

# Get the configured Celery instance from the Flask app
celery = app.celery

if __name__ == '__main__':
    # Use Celery's command-line interface
    # Replace script name with 'celery' and add 'worker' command
    sys.argv = ['celery', 'worker'] + (sys.argv[1:] if len(sys.argv) > 1 else ['--loglevel=info'])
    celery.start()
