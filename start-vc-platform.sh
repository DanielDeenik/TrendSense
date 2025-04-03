#!/bin/bash

# TrendSense™ VC/PE Platform Startup Script

# Set text color variables
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========== TrendSense™ VC/PE Platform ==========${NC}"
echo -e "${BLUE}Optimized for Venture Capital and Private Equity workflows${NC}"
echo -e "${BLUE}=================================================${NC}"

# Make scripts executable
chmod +x ./scripts/*.sh ./scripts/*.py

# Run setup check if available
if [ -f "./scripts/setup_check.py" ]; then
    echo -e "${BLUE}Running environment setup check...${NC}"
    python ./scripts/setup_check.py
fi

# Determine which startup method to use based on available files
if [ -f "server/index.ts" ]; then
    # Node.js/TypeScript implementation
    echo -e "${GREEN}Starting Node.js application...${NC}"
    exec npx ts-node server/index.ts
elif [ -f "frontend/app.py" ]; then
    # Python Flask application
    echo -e "${GREEN}Starting Python Flask application...${NC}"
    python frontend/app.py
elif [ -f "frontend/refactored_app.py" ]; then
    # Refactored Python application
    echo -e "${GREEN}Starting refactored Python application...${NC}"
    python frontend/refactored_app.py
elif [ -f "backend/main.py" ]; then
    # FastAPI backend
    echo -e "${GREEN}Starting FastAPI backend...${NC}"
    python -m uvicorn backend.main:app --host 0.0.0.0 --port 3000 &
    
    # Wait for backend to start
    sleep 2
    
    # Start Flask frontend
    echo -e "${GREEN}Starting Flask frontend...${NC}"
    python -m flask --app frontend.app run --host 0.0.0.0 --port 8000
else
    echo -e "${RED}Could not find a suitable application entry point.${NC}"
    echo -e "${YELLOW}Please create one of the following files:${NC}"
    echo -e "${YELLOW}  - server/index.ts (Node.js/TypeScript)${NC}"
    echo -e "${YELLOW}  - frontend/app.py (Python Flask)${NC}"
    echo -e "${YELLOW}  - frontend/refactored_app.py (Refactored Python)${NC}"
    echo -e "${YELLOW}  - backend/main.py (FastAPI backend)${NC}"
    exit 1
fi