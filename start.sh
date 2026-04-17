#!/bin/bash

# Start both backend and frontend for Skin Cancer Analyzer

set -e

echo "Starting Skin Cancer Analyzer..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if ports are available
check_port() {
    if lsof -i:$1 > /dev/null 2>&1; then
        echo -e "${RED}Port $1 is already in use${NC}"
        return 1
    fi
    return 0
}

# Start backend
start_backend() {
    echo -e "${YELLOW}Starting backend on port 8000...${NC}"
    cd backend
    uvicorn app.main:app --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    echo -e "${GREEN}Backend started (PID: $BACKEND_PID)${NC}"
    cd ..
}

# Start frontend
start_frontend() {
    echo -e "${YELLOW}Starting frontend on port 3000...${NC}"
    cd frontend
    npm run dev &
    FRONTEND_PID=$!
    echo -e "${GREEN}Frontend started (PID: $FRONTEND_PID)${NC}"
    cd ..
}

# Main
echo ""
echo "========================================="
echo "  Skin Cancer Analyzer"
echo "  Backend: http://localhost:8000"
echo "  Frontend: http://localhost:3000"
echo "========================================="
echo ""

# Start services
start_backend
start_frontend

echo ""
echo -e "${GREEN}All services started!${NC}"
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "echo -e '\n${YELLOW}Stopping services...${NC}'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" SIGINT SIGTERM

wait