#!/bin/bash
set -e

echo "Starting Sustainability Intelligence Platform..."

# Create logs directory if it doesn't exist
mkdir -p logs

# Kill any existing processes
echo "Stopping any existing services..."
pkill -f "python" || true
pkill -f "flask" || true
pkill -f "uvicorn" || true
pkill -f "redis-server" || true
pkill -f "port 5000" || true
pkill -f "port 8000" || true

# Short pause to ensure all processes are terminated
sleep 2

# Make scripts executable
chmod +x frontend/start.sh
chmod +x backend/start.sh
chmod +x backend/seed_database.py

# Display database connection info (without sensitive values)
echo "Database configuration:"
echo "- DATABASE_URL exists: $(if [ -n "$DATABASE_URL" ]; then echo "yes"; else echo "no"; fi)"
echo "- PGDATABASE exists: $(if [ -n "$PGDATABASE" ]; then echo "yes"; else echo "no"; fi)"
echo "- PGUSER exists: $(if [ -n "$PGUSER" ]; then echo "yes"; else echo "no"; fi)"
echo "- PGHOST exists: $(if [ -n "$PGHOST" ]; then echo "yes"; else echo "no"; fi)"
echo "- PGPORT exists: $(if [ -n "$PGPORT" ]; then echo "yes"; else echo "no"; fi)"

# Seed the database with sample metrics
echo "Seeding database with sample metrics..."
cd backend
python seed_database.py || echo "Warning: Database seeding failed, but continuing startup"
cd ..

# Start FastAPI backend directly (without background)
echo "Starting FastAPI backend on port 8000..."
cd backend

# Start the FastAPI backend with a timeout
timeout 10s python -c "
import uvicorn
uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='info')
" &
FASTAPI_PID=$!

# Wait for FastAPI to be ready
echo "Waiting for FastAPI backend to be ready..."
sleep 5  # Give FastAPI time to start up

# Check if FastAPI backend is running
if ! ps -p $FASTAPI_PID > /dev/null; then
    echo "FastAPI backend failed to start. Starting it again with better error visibility..."
    # Start again with different approach
    python main.py &
    FASTAPI_PID=$!
    sleep 5  # Give it time to start
fi

cd ..

# Start Flask frontend
echo "Starting Flask frontend on port 5000..."
cd frontend

# Set the backend URL environment variable
export BACKEND_URL="http://localhost:8000"

# Start Flask directly with debugging info
python app.py &
FLASK_PID=$!

cd ..

echo "Services started. Checking status..."

# Check service status
echo "FastAPI PID: $FASTAPI_PID, Flask PID: $FLASK_PID"

# Keep script running and monitor processes
echo "Services are running. Press Ctrl+C to stop."
echo "Access the web interface at: http://localhost:5000"
echo "Access the API at: http://localhost:8000/api/metrics"

# Wait for both services
wait $FASTAPI_PID $FLASK_PID

echo "Sustainability Intelligence Platform startup completed."