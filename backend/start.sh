#!/bin/sh
set -e  # Exit immediately if a command exits with a non-zero status

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI server..."
fastapi run --workers 4 app/main.py