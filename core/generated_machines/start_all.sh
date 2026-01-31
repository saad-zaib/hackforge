#!/bin/bash
# Start all Hackforge machines

echo "🚀 Starting all machines..."
echo ""

echo "Starting 212c1e002d67fe22..."
cd 212c1e002d67fe22 && docker-compose up -d --build && cd ..


echo ""
echo "✓ All machines started!"
echo ""
echo "Active machines:"
echo "  • http://localhost:8081 - 212c1e002d67fe22"
