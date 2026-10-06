#!/bin/sh
# Render free plan: ek hi container mein API (andar, 8000) + Streamlit UI (public $PORT)
uvicorn app.main:app --host 127.0.0.1 --port 8000 &
exec streamlit run ui/streamlit_app.py \
  --server.port "${PORT:-8501}" --server.address 0.0.0.0 --server.headless true
