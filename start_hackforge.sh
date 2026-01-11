#!/bin/bash

# Hackforge Unified Startup Script
# Starts all components in the correct order

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              HACKFORGE PLATFORM STARTUP                   ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if machines are generated
check_and_generate_machines() {
    echo -e "${YELLOW}[0/5] Checking for generated machines...${NC}"

    if [ ! -d "$SCRIPT_DIR/core/generated_machines" ] || [ -z "$(ls -A "$SCRIPT_DIR/core/generated_machines" 2>/dev/null)" ]; then
        echo -e "${YELLOW}⚠️  No machines found${NC}"
        echo ""
        read -p "Generate vulnerable machines now? (y/n): " -n 1 -r
        echo

        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${BLUE}🎲 Generating vulnerable machines...${NC}"
            cd "$SCRIPT_DIR/core"

            if python3 generator.py; then
                echo -e "${GREEN}✓ Machines generated successfully${NC}"

                # Also run template engine if it exists
		if [ -f "$SCRIPT_DIR/core/template_engine.py" ]; then
    			echo -e "${BLUE}🔨 Converting configs to applications...${NC}"
    			cd "$SCRIPT_DIR/core"
    			python3 template_engine.py 
    			echo -e "${GREEN}✓ Templates processed${NC}"
		fi

                # Automatically start Docker machines after generation
                echo ""
                echo -e "${BLUE}🐳 Starting generated Docker machines...${NC}"
                sleep 2

                cd "$SCRIPT_DIR/core/generated_machines"
                if [ -f "docker-compose.yml" ]; then
                    docker-compose up -d --build
                    if [ $? -eq 0 ]; then
                        echo -e "${GREEN}✓ Docker machines built and started${NC}"

                        # Show machine URLs
                        echo ""
                        echo -e "${GREEN}Available Machines:${NC}"
                        machine_count=$(find . -maxdepth 1 -type d ! -name "." ! -name ".." | wc -l)
                        for i in $(seq 0 $((machine_count - 1))); do
                            port=$((8080 + i))
                            echo "  • Machine $((i + 1)): http://localhost:$port"
                        done
                    else
                        echo -e "${RED}❌ Failed to start Docker machines${NC}"
                        echo "You can try manually: cd core/generated_machines && docker-compose up -d --build"
                    fi
                else
                    echo -e "${RED}❌ No docker-compose.yml found${NC}"
                fi

                cd "$SCRIPT_DIR"
            else
                echo -e "${RED}❌ Machine generation failed${NC}"
                exit 1
            fi
        else
            echo -e "${YELLOW}Skipping machine generation${NC}"
            echo "You can generate machines later with: cd core && python3 generator.py"
        fi
    else
        machine_count=$(find "$SCRIPT_DIR/core/generated_machines" -maxdepth 1 -type d ! -name "." ! -name ".." ! -name "app" 2>/dev/null | wc -l)
        echo -e "${GREEN}✓ Found $machine_count generated machine(s)${NC}"

        # Check if machines are already running
        cd "$SCRIPT_DIR/core/generated_machines"
        if [ -f "docker-compose.yml" ]; then
            running_containers=$(docker-compose ps -q 2>/dev/null | wc -l)
            if [ "$running_containers" -eq 0 ]; then
                echo ""
                read -p "Start Docker machines? (y/n): " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    echo -e "${BLUE}🐳 Starting Docker machines...${NC}"
                    docker-compose up -d
                    echo -e "${GREEN}✓ Docker machines started${NC}"
                fi
            else
                echo -e "${GREEN}✓ Docker machines already running ($running_containers containers)${NC}"
            fi
        fi
        cd "$SCRIPT_DIR"
    fi
}

# Check if MongoDB is running
check_mongodb() {
    echo -e "\n${YELLOW}[1/5] Checking MongoDB...${NC}"

    if pgrep -x "mongod" > /dev/null; then
        echo -e "${GREEN}✓ MongoDB is running${NC}"
        return 0
    else
        echo -e "${YELLOW}MongoDB not running. Starting...${NC}"

        # Try to start MongoDB
        if command -v systemctl &> /dev/null; then
            sudo systemctl start mongod
            sleep 2
            echo -e "${GREEN}✓ MongoDB started${NC}"
        else
            echo -e "${RED}❌ Could not start MongoDB automatically${NC}"
            echo "Please start MongoDB manually or use Docker:"
            echo "  docker run -d -p 27017:27017 --name mongodb mongo:latest"
            exit 1
        fi
    fi
}

# Start API with Database
start_api() {
    echo -e "\n${YELLOW}[2/5] Starting API Server...${NC}"

    # Kill existing API process if running
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    pkill -9 -f "web.api.main_with_db" 2>/dev/null || true
    sleep 1

    # FIXED: Run from project root with correct module path
    cd "$SCRIPT_DIR"
    python3 -m web.api.main_with_db > "$SCRIPT_DIR/logs/api.log" 2>&1 &
    API_PID=$!

    echo $API_PID > "$SCRIPT_DIR/.api.pid"

    # Wait for API to start
    sleep 3

    if ps -p $API_PID > /dev/null; then
        echo -e "${GREEN}✓ API started (PID: $API_PID)${NC}"
        echo "  URL: http://localhost:8000"
        echo "  Docs: http://localhost:8000/docs"
    else
        echo -e "${RED}❌ API failed to start. Check logs/api.log${NC}"
        tail -20 "$SCRIPT_DIR/logs/api.log"
        exit 1
    fi
}

# Start Frontend
start_frontend() {
    echo -e "\n${YELLOW}[3/5] Starting React Frontend...${NC}"

    # Kill existing frontend processes thoroughly
    echo "Cleaning up any existing frontend processes..."

    # Kill by port (most reliable)
    lsof -ti:3000 | xargs kill -9 2>/dev/null || true

    # Kill by process name
    pkill -9 -f "react-scripts start" 2>/dev/null || true
    pkill -9 -f "node.*frontend" 2>/dev/null || true

    # Wait for ports to be released
    sleep 2

    if [ ! -d "$SCRIPT_DIR/web/frontend/node_modules" ]; then
        echo -e "${YELLOW}Installing frontend dependencies...${NC}"
        cd "$SCRIPT_DIR/web/frontend"
        npm install > "$SCRIPT_DIR/logs/npm-install.log" 2>&1
    fi

    cd "$SCRIPT_DIR/web/frontend"

    # Start frontend in background
    BROWSER=none npm start > "$SCRIPT_DIR/logs/frontend.log" 2>&1 &
    FRONTEND_PID=$!

    echo $FRONTEND_PID > "$SCRIPT_DIR/.frontend.pid"

    # Wait for frontend to start
    echo "Waiting for frontend to compile..."
    sleep 10

    if ps -p $FRONTEND_PID > /dev/null; then
        echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
        echo "  URL: http://localhost:3000"
    else
        echo -e "${RED}❌ Frontend failed to start. Check logs/frontend.log${NC}"
        tail -20 "$SCRIPT_DIR/logs/frontend.log"
        exit 1
    fi
}

# Show Docker status
show_docker_status() {
    echo -e "\n${YELLOW}[4/5] Docker Machines Status...${NC}"

    if [ -d "$SCRIPT_DIR/core/generated_machines" ] && [ -f "$SCRIPT_DIR/core/generated_machines/docker-compose.yml" ]; then
        cd "$SCRIPT_DIR/core/generated_machines"

        running=$(docker-compose ps -q 2>/dev/null | wc -l)

        if [ "$running" -gt 0 ]; then
            echo -e "${GREEN}✓ $running Docker machine(s) running${NC}"
            echo ""
            docker-compose ps
        else
            echo -e "${YELLOW}⚠️  No Docker machines running${NC}"
            echo "Start them with: cd core/generated_machines && docker-compose up -d"
        fi

        cd "$SCRIPT_DIR"
    else
        echo -e "${YELLOW}⚠️  No machines available${NC}"
    fi
}

# Final summary
show_summary() {
    echo -e "\n${YELLOW}[5/5] System Summary${NC}"

    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║              HACKFORGE IS NOW RUNNING!                    ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    echo -e "${GREEN}🌐 Web Services:${NC}"
    echo "  • Frontend:  http://localhost:3000"
    echo "  • API:       http://localhost:8000"
    echo "  • API Docs:  http://localhost:8000/docs"
    echo "  • MongoDB:   mongodb://localhost:27017"
    echo ""

    # Show vulnerable machines
    if [ -d "$SCRIPT_DIR/core/generated_machines" ]; then
        cd "$SCRIPT_DIR/core/generated_machines"
        machine_dirs=$(find . -maxdepth 1 -type d ! -name "." ! -name ".." ! -name "app" 2>/dev/null)
        machine_count=$(echo "$machine_dirs" | grep -v "^$" | wc -l)

        if [ "$machine_count" -gt 0 ]; then
            echo -e "${GREEN}🎯 Vulnerable Machines:${NC}"
            i=0
            for dir in $machine_dirs; do
                if [ ! -z "$dir" ] && [ "$dir" != "." ]; then
                    port=$((8080 + i))
                    machine_id=$(basename "$dir")

                    # Check if container is running
                    if docker-compose ps -q "$machine_id" 2>/dev/null | grep -q .; then
                        echo -e "  • Machine $((i + 1)) [${GREEN}RUNNING${NC}]: http://localhost:$port"
                    else
                        echo -e "  • Machine $((i + 1)) [${RED}STOPPED${NC}]: http://localhost:$port"
                    fi

                    i=$((i + 1))
                fi
            done
        fi
        cd "$SCRIPT_DIR"
    fi

    echo ""
    echo -e "${YELLOW}📋 Logs:${NC}"
    echo "  • API:       tail -f logs/api.log"
    echo "  • Frontend:  tail -f logs/frontend.log"
    echo "  • Docker:    cd core/generated_machines && docker-compose logs -f"
    echo ""
    echo -e "${YELLOW}🛠️  Management:${NC}"
    echo "  • Stop all:      ./stop_hackforge.sh"
    echo "  • Restart:       ./stop_hackforge.sh && ./start_hackforge.sh"
    echo "  • Docker up:     cd core/generated_machines && docker-compose up -d"
    echo "  • Docker down:   cd core/generated_machines && docker-compose down"
    echo "  • Docker logs:   cd core/generated_machines && docker-compose logs -f"
    echo ""
    echo -e "${BLUE}💡 Tip: If API fails to start, check the logs and ensure MongoDB is running${NC}"
    echo ""
}

# Create logs directory
mkdir -p "$SCRIPT_DIR/logs"

# Main startup sequence
main() {
    check_and_generate_machines
    check_mongodb
    start_api
    start_frontend
    show_docker_status
    show_summary
}

# Trap Ctrl+C
trap 'echo -e "\n${YELLOW}Use ./stop_hackforge.sh to stop all services${NC}"; exit 0' INT

main
