#!/bin/bash
# List all Hackforge machines

echo "📋 Hackforge Machines"
echo "===================="
echo ""

echo "212c1e002d67fe22"
echo "  Port: 8081"
echo "  Category: sqli"
echo "  URL: http://localhost:8081"
cd 212c1e002d67fe22 && echo -n "  Status: " && docker-compose ps --services --filter "status=running" | wc -l | awk '{if ($1 > 0) print "🟢 Running"; else print "⚫ Stopped"}' && cd ..
echo ""

