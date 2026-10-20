#!/usr/bin/env bash

# BookWise AI — Fast One-Click Local Launcher (macOS M-series & Linux)
set -e

echo "=========================================================="
echo "   BOOKWISE AI — INTELLIGENT BOOK RECOMMENDATION SYSTEM   "
echo "   B.Tech CSE (AIML) NTCC Project Local Launcher          "
echo "=========================================================="

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# 1. Check Python Virtual Environment
if [ ! -d "backend/venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv backend/venv
    source backend/venv/bin/activate
    pip install --upgrade pip
    pip install -r backend/requirements.txt
else
    source backend/venv/bin/activate
fi

# 2. Ensure datasets and seed database if necessary
if [ ! -f "datasets/books.csv" ]; then
    echo "Generating authentic curated book dataset..."
    python scripts/seed_dataset.py
fi

# 3. Check frontend dependencies
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing frontend dependencies..."
    cd frontend && npm install && cd ..
fi

echo ""
echo "🚀 Starting Flask Backend on http://127.0.0.1:5000..."
python backend/run.py &
BACKEND_PID=$!

echo "🚀 Starting Vite React Frontend on http://localhost:5173..."
cd frontend
npm run dev -- --host 127.0.0.1 &
FRONTEND_PID=$!
cd ..

cleanup() {
    echo ""
    echo "Shutting down BookWise AI..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    exit 0
}

trap cleanup INT TERM

echo ""
echo "=========================================================="
echo "BookWise AI is running!"
echo "➡️  Frontend: http://localhost:5173"
echo "➡️  Backend:  http://127.0.0.1:5000"
echo "Press Ctrl+C to stop both servers."
echo "=========================================================="

wait
