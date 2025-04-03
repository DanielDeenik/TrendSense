#!/bin/bash
#
# Complete Sustainability Platform Starter
# This script reliably starts both backend and frontend components
# with proper port management and process coordination
#

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

# Install required dependencies if needed
install_deps() {
  log_info "Checking for required dependencies..."

  # Install psutil if needed for port management
  python3 -c "import psutil" 2>/dev/null || pip install psutil

  # Install other dependencies if needed
  python3 -c "import fastapi" 2>/dev/null || pip install fastapi uvicorn
  python3 -c "import flask" 2>/dev/null || pip install flask

  log_success "All dependencies are installed"
}

# Prepare database and ensure it's running
setup_database() {
  log_info "Ensuring database is properly configured..."

  # Check if DB exists and is accessible
  if python3 -c "import os; import psycopg2; conn = psycopg2.connect(os.environ['DATABASE_URL']); conn.close()" 2>/dev/null; then
    log_success "Database connection established"
  else
    log_warning "Database connection issue detected - attempting to create/setup tables"

    # Try to create the tables if they don't exist
    cd backend
    python3 test_db_connection.py
    cd ..

    if [ $? -eq 0 ]; then
      log_success "Database tables created successfully"
    else
      log_error "Failed to create database tables. Continuing anyway..."
    fi
  fi
}

# Make sure the port manager is available
ensure_port_manager() {
  if [ ! -f frontend/port_manager.py ]; then
    log_info "Installing port manager..."
    cp port_manager.py frontend/ 2>/dev/null || \
    cp backend/port_manager.py frontend/ 2>/dev/null || \
    echo "Unable to find port_manager.py, please ensure it exists"
  fi

  if [ ! -f backend/port_manager.py ]; then
    log_info "Installing port manager for backend..."
    cp port_manager.py backend/ 2>/dev/null || \
    cp frontend/port_manager.py backend/ 2>/dev/null || \
    echo "Unable to find port_manager.py, please ensure it exists"
  fi
}

# Start the backend API server
start_backend() {
  log_info "Starting FastAPI backend server on port 8080..."

  # Use port manager to ensure port 8000 is free
  cd backend

  # Set explicit host to 0.0.0.0 for Replit compatibility
  export HOST="0.0.0.0"
  export PORT=8080

  # Free the port and start API
  python3 port_manager.py --port 8080 --host 0.0.0.0 --free
  python3 port_manager.py --port 8080 --host 0.0.0.0 --run "python3 storytelling_api.py" &
  BACKEND_PID=$!
  cd ..

  # Wait for backend to start
  log_info "Waiting for backend to start..."
  for i in {1..30}; do
    if curl -s http://127.0.0.1:8080/health >/dev/null; then
      log_success "Backend started successfully"
      return 0
    fi
    sleep 1
  done

  log_error "Failed to start backend server"
  return 1
}

# Start the frontend dashboard
start_frontend() {
  log_info "Starting Frontend on port 5000..."

  # Use port manager to free port 5000
  cd frontend
  python3 port_manager.py --port 5000 --host 0.0.0.0 --free

  # Set the backend URL
  export BACKEND_URL="http://127.0.0.1:8080"

  # Start the frontend
  python3 port_manager.py --port 5000 --host 0.0.0.0 --flask direct_app.py &
  FRONTEND_PID=$!
  cd ..

  # Wait for frontend to start
  log_info "Waiting for frontend to start..."
  for i in {1..30}; do
    if curl -s http://127.0.0.1:5000 >/dev/null; then
      log_success "Frontend started successfully"
      break
    fi
    sleep 1
  done
}

# Install signal handlers for clean shutdown
cleanup() {
  log_info "Stopping services..."
  kill $FRONTEND_PID 2>/dev/null || true
  kill $BACKEND_PID 2>/dev/null || true
  wait
  log_success "All services stopped"
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Main execution
main() {
  log_info "Starting Sustainability Intelligence Platform..."

  # Setup steps
  install_deps
  setup_database
  ensure_port_manager

  # Start services
  start_backend
  start_frontend

  log_success "Sustainability Intelligence Platform is now running!"
  log_info "API: http://127.0.0.1:8080"
  log_info "Frontend: http://127.0.0.1:5000"
  log_info "Press Ctrl+C to stop all services"

  # Keep script running to maintain services
  wait $FRONTEND_PID
}

# Run the main function
main