#!/bin/bash
set -e

echo "Starting FastAPI Storytelling API with reliable port handling..."

# Check if psutil is installed, install if needed
python3 -c "import psutil" 2>/dev/null || pip install psutil

# Copy port_manager.py to the correct location if it's not there
if [ ! -f backend/port_manager.py ]; then
  cp frontend/port_manager.py backend/ 2>/dev/null || cp port_manager.py backend/ 2>/dev/null || true
fi

# Change to the backend directory
cd backend

# Set explicit host to 0.0.0.0 for Replit compatibility
export HOST="0.0.0.0"
export PORT=8080

# Use our port manager to run the API on port 8080 reliably
# Add additional timeout for server startup
python3 port_manager.py --port 8080 --host 0.0.0.0 --free

echo "Starting storytelling API directly for better reliability..."
python3 storytelling_api.py &

# Wait for API to start and verify it's running
PID=$!
echo "API started with PID: $PID"

# Give the server time to start up
echo "Waiting for API to initialize..."
sleep 5

# Check if the API is responding
RETRY_COUNT=0
MAX_RETRIES=5

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  if curl -s http://localhost:8080/health > /dev/null; then
    echo "API is running and responding to health checks"
    break
  else
    echo "API not responding yet, waiting... (attempt $((RETRY_COUNT+1))/$MAX_RETRIES)"
    RETRY_COUNT=$((RETRY_COUNT+1))
    sleep 2
  fi
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
  echo "WARNING: API did not respond to health checks, but continuing anyway"
else
  # Show the health response
  echo "API health check response:"
  curl -s http://localhost:8080/health
fi

echo "API server is now running. Press Ctrl+C to stop."

# Keep script running
wait $PID

# This script should not exit normally as the Python script keeps running
echo "FastAPI application has stopped."