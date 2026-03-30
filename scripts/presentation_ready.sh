#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

need_help() {
  echo
  echo "=== ACTION NEEDED FROM YOU ==="
  echo "$1"
  echo "============================="
}

echo "[1/6] Python package registry reachability"
if python -m pip index versions fastapi >/dev/null 2>&1; then
  echo "PyPI reachable"
else
  need_help "PyPI is blocked. Please provide outbound pip access (or configure PIP_INDEX_URL / proxy), then rerun ./scripts/presentation_ready.sh"
  exit 2
fi

echo "[2/6] Backend venv + deps"
python -m venv backend/.venv
source backend/.venv/bin/activate
pip install -q --upgrade pip
pip install -q -r backend/requirements.txt

echo "[3/6] Backend compile check"
python -m compileall backend/app >/dev/null

echo "[4/6] npm registry reachability"
if npm view react version >/dev/null 2>&1; then
  echo "npm registry reachable"
else
  need_help "npm registry is blocked. Please provide npm access or set npm config registry to your approved mirror, then rerun ./scripts/presentation_ready.sh"
  exit 3
fi

echo "[5/6] Frontend deps"
cd frontend
npm install


echo "[6/6] Presentation-ready environment complete"
echo "Run backend: source backend/.venv/bin/activate && uvicorn app.main:app --reload --port 8000 --app-dir backend"
echo "Run frontend: cd frontend && npm run dev"
