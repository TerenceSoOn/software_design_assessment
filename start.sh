#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Function to check if a port is in use
check_port() {
    lsof -i :$1 > /dev/null 2>&1
    return $?
}

# Function to kill process on a specific port
kill_port() {
    local port=$1
    local pid=$(lsof -ti :$port)
    if [ ! -z "$pid" ]; then
        echo -e "${YELLOW}⚠️  Port $port is in use (PID: $pid). Killing process...${NC}"
        kill -9 $pid 2>/dev/null
        sleep 1
    fi
}

# Function to kill background processes on exit
cleanup() {
    echo -e "\n${YELLOW}🛑 Stopping servers...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    echo -e "${GREEN}✅ Servers stopped${NC}"
    exit
}

trap cleanup SIGINT SIGTERM

echo -e "${BLUE}╔════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     FlirtNet Startup Script       ║${NC}"
echo -e "${BLUE}╔════════════════════════════════════╗${NC}"
echo ""

# Check and clean ports
echo -e "${BLUE}🔍 Checking ports...${NC}"
check_port 8000 && kill_port 8000
check_port 5173 && kill_port 5173

# Start Backend
echo -e "${BLUE}🚀 Starting Backend...${NC}"
cd "$SCRIPT_DIR/codespace/backend"

if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found at codespace/backend/venv${NC}"
    echo -e "${YELLOW}Please create it first with: python3 -m venv venv${NC}"
    exit 1
fi

source venv/bin/activate
python3 -m app.main > "$SCRIPT_DIR/backend.log" 2>&1 &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 2

# Check if backend started successfully
if ! ps -p $BACKEND_PID > /dev/null; then
    echo -e "${RED}❌ Backend failed to start. Check backend.log for details.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"

# Start Frontend
echo -e "${BLUE}✨ Starting Frontend...${NC}"
cd "$SCRIPT_DIR/codespace/frontend"

if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}⚠️  node_modules not found. Running npm install...${NC}"
    npm install
fi

npm run dev -- --port 5173 > "$SCRIPT_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!

# Wait a bit for frontend to start
sleep 3

# Check if frontend started successfully
if ! ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${RED}❌ Frontend failed to start. Check frontend.log for details.${NC}"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"
echo ""
echo -e "${GREEN}╔════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   🎉 FlirtNet is now running! 🎉  ║${NC}"
echo -e "${GREEN}╔════════════════════════════════════╗${NC}"
echo ""
echo -e "${BLUE}📍 Backend:  ${NC}http://localhost:8000"
echo -e "${BLUE}📍 API Docs: ${NC}http://localhost:8000/docs"
echo -e "${BLUE}📍 Frontend: ${NC}http://localhost:5173"
echo ""
echo -e "${YELLOW}📝 Logs are being written to:${NC}"
echo -e "   • backend.log"
echo -e "   • frontend.log"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all servers${NC}"
echo ""

wait
