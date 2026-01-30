#!/bin/bash
# Stop all Hackforge machines

echo "🛑 Stopping all machines..."
echo ""

echo "Stopping 8ed8fa14892a2b42..."
cd 8ed8fa14892a2b42 && docker-compose down && cd ..

echo "Stopping 5a1226e6f1bde475..."
cd 5a1226e6f1bde475 && docker-compose down && cd ..

echo "Stopping 58e7e5331ef3b59d..."
cd 58e7e5331ef3b59d && docker-compose down && cd ..


echo ""
echo "✓ All machines stopped!"
