#!/bin/sh
# Render free plan: FastAPI serves both the API and the web UI on $PORT
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
