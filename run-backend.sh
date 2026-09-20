#!/bin/bash
set -e
cd "$(dirname "$0")/backend"
source venv/bin/activate
docker compose up -d
python -m uvicorn app.main:app --reload
