#!/bin/bash
# Start 58e7e5331ef3b59d
echo "🚀 Starting 58e7e5331ef3b59d..."
docker-compose up -d --build

echo "✓ Machine running at: http://localhost:8082"
echo "✓ Container: hackforge_58e7e5331ef3b59d"
echo ""
echo "View logs: docker-compose logs -f"
echo "Stop: docker-compose down"
