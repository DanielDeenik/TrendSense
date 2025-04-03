#!/bin/bash
#
# Replit-specific starter script for Sustainability Intelligence Platform
# This script starts both the backend API and frontend interface
# with proper configuration for Replit hosting environment

set -e

# Print colored messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
  echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
  echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
  echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

# Install required dependencies
log_info "Installing required dependencies..."
pip install fastapi uvicorn flask python-dotenv redis httpx gunicorn psutil

# Prepare environment
log_info "Setting up environment for Replit..."

# Use Replit's PORT environment variable for the frontend
export FRONTEND_PORT=${PORT:-5000}
# Use a fixed port for the backend
export BACKEND_PORT=8080
export HOST="0.0.0.0"

log_info "Frontend will run on port $FRONTEND_PORT (Replit assigned port)"
log_info "Backend API will run on port $BACKEND_PORT"

# Set the backend URL for the frontend to use
# This is critical for proper API communication
export BACKEND_URL="http://$HOST:$BACKEND_PORT"
log_info "Frontend will connect to backend at: $BACKEND_URL"

# Make port_manager.py available to both services
if [ ! -f frontend/port_manager.py ]; then
  log_info "Copying port_manager.py to frontend directory..."
  cp port_manager.py frontend/ 2>/dev/null || cp backend/port_manager.py frontend/ 2>/dev/null || true
fi

if [ ! -f backend/port_manager.py ]; then
  log_info "Copying port_manager.py to backend directory..."
  cp port_manager.py backend/ 2>/dev/null || cp frontend/port_manager.py backend/ 2>/dev/null || true
fi

# Start backend API in the background
log_info "Starting backend API service..."
cd backend

# Free up the backend port if needed
python3 port_manager.py --port $BACKEND_PORT --host $HOST --free > /dev/null 2>&1 || true

# Start the backend server
# Removed reload=True to avoid port binding issues
log_info "Starting storytelling_api.py on port $BACKEND_PORT..."
python3 storytelling_api.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
log_info "Waiting for backend API to initialize..."
sleep 5

# Check if backend is responding
if curl -s "http://127.0.0.1:$BACKEND_PORT/health" > /dev/null; then
  log_success "Backend API started successfully"
else
  log_warning "Backend API might not be fully initialized yet, but continuing"
fi

# Start frontend
log_info "Starting frontend service on port $FRONTEND_PORT..."
cd frontend

# Free up the frontend port if needed
python3 port_manager.py --port $FRONTEND_PORT --host $HOST --free > /dev/null 2>&1 || true

# Start the frontend application
log_info "Starting direct_app.py on port $FRONTEND_PORT..."
python3 direct_app.py &
FRONTEND_PID=$!

# Keep script running
log_success "Sustainability Intelligence Platform is starting up!"
log_info "You can access the platform at your Replit URL"
log_info "Backend API: http://$HOST:$BACKEND_PORT"
log_info "Frontend UI: http://$HOST:$FRONTEND_PORT"
log_info "Press Ctrl+C to stop all services"

# Set up signal handlers for clean shutdown
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true" SIGINT SIGTERM

# Wait for frontend process to keep the script running
wait $FRONTEND_PID