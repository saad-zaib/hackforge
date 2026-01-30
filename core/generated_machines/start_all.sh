#!/bin/bash
# Start all Hackforge machines

echo "🚀 Starting all machines..."
echo ""

echo "Starting 8ed8fa14892a2b42..."
cd 8ed8fa14892a2b42 && docker-compose up -d --build && cd ..

echo "Starting 5a1226e6f1bde475..."
cd 5a1226e6f1bde475 && docker-compose up -d --build && cd ..

echo "Starting 58e7e5331ef3b59d..."
cd 58e7e5331ef3b59d && docker-compose up -d --build && cd ..


echo ""
echo "✓ All machines started!"
echo ""
echo "Active machines:"
echo "  • http://localhost:8080 - 8ed8fa14892a2b42"
echo "  • http://localhost:8081 - 5a1226e6f1bde475"
echo "  • http://localhost:8082 - 58e7e5331ef3b59d"
