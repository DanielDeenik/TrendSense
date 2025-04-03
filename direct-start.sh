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
pkill -f "port 5000" || true
pkill -f "port 5001" || true
pkill -f "port 8000" || true
pkill -f "redis-server" || true

# Short pause to ensure all processes are terminated
sleep 2

# Make scripts executable
chmod +x frontend/start.sh
chmod +x backend/run_api.py
chmod +x frontend/direct_app.py
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

# Start Redis server for Flask caching
echo "Starting Redis server..."
redis-server --daemonize yes --maxmemory 128mb --maxmemory-policy allkeys-lru

# Start FastAPI backend in background (no timeout)
echo "Starting FastAPI backend on port 8000..."
cd backend
python run_api.py > ../logs/fastapi.log 2>&1 &
FASTAPI_PID=$!
cd ..

# Wait for FastAPI to be ready
echo "Waiting for FastAPI backend to be ready..."
MAX_RETRIES=15
RETRY_COUNT=0
while ! curl -s http://localhost:8000/health > /dev/null; do
    if ! ps -p $FASTAPI_PID > /dev/null; then
        echo "ERROR: FastAPI process died. Check logs/fastapi.log for details"
        exit 1
    fi
    
    RETRY_COUNT=$((RETRY_COUNT+1))
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "ERROR: Could not connect to FastAPI after $MAX_RETRIES attempts"
        echo "Showing FastAPI logs:"
        cat logs/fastapi.log
        exit 1
    fi
    
    echo "Waiting for FastAPI backend to be ready (attempt $RETRY_COUNT/$MAX_RETRIES)..."
    sleep 2
done

echo "FastAPI backend is ready!"

# Test API health
echo "Testing API health..."
curl -s http://localhost:8000/health

# Test metrics endpoint
echo -e "\nTesting metrics endpoint..."
curl -s http://localhost:8000/api/metrics | head -30

# Start Flask frontend
echo -e "\nStarting Flask frontend on port 5001..."
cd frontend
# Set the backend URL environment variable
export BACKEND_URL="http://localhost:8000"

# Start Flask directly
python direct_app.py > ../logs/flask.log 2>&1 &
FLASK_PID=$!
cd ..

# Wait for Flask to be ready
echo "Waiting for Flask frontend to be ready..."
MAX_RETRIES=10
RETRY_COUNT=0
while ! curl -s http://localhost:5001 > /dev/null; do
    if ! ps -p $FLASK_PID > /dev/null; then
        echo "ERROR: Flask process died. Check logs/flask.log for details"
        exit 1
    fi
    
    RETRY_COUNT=$((RETRY_COUNT+1))
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "ERROR: Could not connect to Flask after $MAX_RETRIES attempts"
        echo "Showing Flask logs:"
        cat logs/flask.log
        exit 1
    fi
    
    echo "Waiting for Flask frontend to be ready (attempt $RETRY_COUNT/$MAX_RETRIES)..."
    sleep 2
done

echo "Flask frontend is ready!"

echo "Services started successfully!"
echo "- FastAPI backend: http://localhost:8000"
echo "- Flask frontend: http://localhost:5001"
echo "- Dashboard: http://localhost:5001/dashboard"

echo "Process IDs:"
echo "- FastAPI: $FASTAPI_PID"
echo "- Flask: $FLASK_PID"

# Print a message and wait for both processes
echo "Press Ctrl+C to stop all services"
wait $FASTAPI_PID $FLASK_PID
