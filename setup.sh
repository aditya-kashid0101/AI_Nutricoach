#!/bin/bash
set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "== NutriCoach setup =="

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required. Install Docker Desktop first."
  exit 1
fi

if ! command -v python3.12 >/dev/null 2>&1; then
  echo "Python 3.12 is recommended and was not found as python3.12."
  echo "Install Python 3.12, then run this script again."
  exit 1
fi

cd "$ROOT_DIR/backend"
python3.12 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
docker compose up -d

cd "$ROOT_DIR/frontend"
npm install

echo ""
echo "Setup complete."
echo "Terminal 1:"
echo "  cd \"$ROOT_DIR/backend\" && source venv/bin/activate && python -m uvicorn app.main:app --reload"
echo ""
echo "Terminal 2:"
echo "  cd \"$ROOT_DIR/frontend\" && npm run dev"
