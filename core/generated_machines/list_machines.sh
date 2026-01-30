#!/bin/bash
# List all Hackforge machines

echo "📋 Hackforge Machines"
echo "===================="
echo ""

echo "8ed8fa14892a2b42"
echo "  Port: 8080"
echo "  Category: sqli"
echo "  URL: http://localhost:8080"
cd 8ed8fa14892a2b42 && echo -n "  Status: " && docker-compose ps --services --filter "status=running" | wc -l | awk '{if ($1 > 0) print "🟢 Running"; else print "⚫ Stopped"}' && cd ..
echo ""

echo "5a1226e6f1bde475"
echo "  Port: 8081"
echo "  Category: xss"
echo "  URL: http://localhost:8081"
cd 5a1226e6f1bde475 && echo -n "  Status: " && docker-compose ps --services --filter "status=running" | wc -l | awk '{if ($1 > 0) print "🟢 Running"; else print "⚫ Stopped"}' && cd ..
echo ""

echo "58e7e5331ef3b59d"
echo "  Port: 8082"
echo "  Category: cmdi"
echo "  URL: http://localhost:8082"
cd 58e7e5331ef3b59d && echo -n "  Status: " && docker-compose ps --services --filter "status=running" | wc -l | awk '{if ($1 > 0) print "🟢 Running"; else print "⚫ Stopped"}' && cd ..
echo ""

