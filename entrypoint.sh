#!/bin/sh

set -x

echo "Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug --use-colors  2>&1
