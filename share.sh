#!/usr/bin/env bash

# BookWise AI — Public Website Launcher for College Faculty Evaluation
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "=========================================================="
echo "   BOOKWISE AI — PUBLIC COLLEGE FACULTY DEMO LAUNCHER     "
echo "=========================================================="

# 1. Activate Python virtualenv
source backend/venv/bin/activate

# 2. Build production frontend if not built
if [ ! -d "frontend/dist" ]; then
    echo "Building production React frontend..."
    cd frontend && npm run build && cd ..
fi

# 3. Check if Flask is already running
if ! curl -s http://127.0.0.1:5000/api/health > /dev/null 2>&1; then
    echo "Starting Flask backend (unified with frontend SPA)..."
    python backend/run.py &
    BACKEND_PID=$!
    sleep 2
else
    echo "Flask server already running on port 5000."
fi

# 4. Launch Cloudflare Tunnel
echo ""
echo "🚀 Creating secure, public HTTPS website URL via Cloudflare..."
cloudflared tunnel --url http://127.0.0.1:5000
