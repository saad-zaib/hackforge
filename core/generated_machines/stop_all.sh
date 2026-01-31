#!/bin/bash
# Stop all Hackforge machines

echo "🛑 Stopping all machines..."
echo ""

echo "Stopping 212c1e002d67fe22..."
cd 212c1e002d67fe22 && docker-compose down && cd ..


echo ""
echo "✓ All machines stopped!"
