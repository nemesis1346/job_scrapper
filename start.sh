#!/bin/bash

# Web3 Job Seeker Startup Script
# This script starts both the backend and frontend servers

echo "🚀 Starting Web3 Job Seeker..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"

if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8+${NC}"
    exit 1
fi

if ! command_exists node; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 16+${NC}"
    exit 1
fi

if ! command_exists npm; then
    echo -e "${RED}❌ npm is not installed. Please install npm${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Function to start backend
start_backend() {
    echo -e "${BLUE}🐍 Starting Python backend...${NC}"
    cd backend
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    echo -e "${YELLOW}📦 Installing Python dependencies...${NC}"
    pip install -r requirements.txt
    
    # Start backend server
    echo -e "${GREEN}🚀 Starting backend server on http://localhost:8000${NC}"
    python run.py &
    BACKEND_PID=$!
    
    cd ..
}

# Function to start frontend
start_frontend() {
    echo -e "${BLUE}⚛️  Starting React frontend...${NC}"
    cd frontend
    
    # Install dependencies
    echo -e "${YELLOW}📦 Installing Node.js dependencies...${NC}"
    npm install
    
    # Start frontend server
    echo -e "${GREEN}🚀 Starting frontend server on http://localhost:3000${NC}"
    npm start &
    FRONTEND_PID=$!
    
    cd ..
}

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down servers...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo -e "${GREEN}✅ Backend server stopped${NC}"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo -e "${GREEN}✅ Frontend server stopped${NC}"
    fi
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start servers
start_backend
sleep 3  # Give backend time to start

start_frontend
sleep 3  # Give frontend time to start

# Wait for servers to be ready
echo -e "${BLUE}⏳ Waiting for servers to be ready...${NC}"
sleep 5

# Check if servers are running
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅ Backend is running at http://localhost:8000${NC}"
    echo -e "${GREEN}📚 API Documentation: http://localhost:8000/docs${NC}"
else
    echo -e "${RED}❌ Backend failed to start${NC}"
fi

if curl -s http://localhost:3000 > /dev/null; then
    echo -e "${GREEN}✅ Frontend is running at http://localhost:3000${NC}"
else
    echo -e "${RED}❌ Frontend failed to start${NC}"
fi

echo -e "\n${GREEN}🎉 Web3 Job Seeker is ready!${NC}"
echo -e "${BLUE}📱 Frontend: http://localhost:3000${NC}"
echo -e "${BLUE}🔧 Backend API: http://localhost:8000${NC}"
echo -e "${BLUE}📚 API Docs: http://localhost:8000/docs${NC}"
echo -e "\n${YELLOW}Press Ctrl+C to stop all servers${NC}"

# Keep script running
wait
