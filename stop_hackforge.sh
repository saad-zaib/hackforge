#!/bin/bash

# Stop all Hackforge services

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║           STOPPING HACKFORGE SERVICES                     ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Stop API
if [ -f ".api.pid" ]; then
    API_PID=$(cat .api.pid)
    if ps -p $API_PID > /dev/null; then
        echo "Stopping API (PID: $API_PID)..."
        kill $API_PID
        echo "✓ API stopped"
    fi
    rm .api.pid
fi

# Alternative: kill by process name
pkill -f "main_with_db.py" 2>/dev/null && echo "✓ API stopped" || true

# Stop Frontend
if [ -f ".frontend.pid" ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null; then
        echo "Stopping Frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        echo "✓ Frontend stopped"
    fi
    rm .frontend.pid
fi

# Alternative: kill by process name
pkill -f "react-scripts start" 2>/dev/null && echo "✓ Frontend stopped" || true

# Stop Docker machines
if [ -d "core/generated_machines" ]; then
    echo "Stopping Docker machines..."
    cd core/generated_machines
    docker-compose down 2>/dev/null && echo "✓ Docker machines stopped" || true
    cd "$SCRIPT_DIR"
fi

echo ""
echo "✓ All services stopped"
echo ""
