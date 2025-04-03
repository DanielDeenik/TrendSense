#!/bin/bash
# Improved startup script for the Sustainability Intelligence Platform
# with better error handling and more robust service startup

echo "Starting Sustainability Intelligence Platform..."
echo "Time: $(date)"

# Create logs directory
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

sleep 2  # Give processes time to terminate

# Make sure scripts are executable
chmod +x backend/seed_database.py
chmod +x backend/simple_api.py
chmod +x frontend/simple_app.py

# Find an available Python installation
echo "Looking for Python..."
PYTHON_CMD=""

# Check for different Python versions
for cmd in python3.11 python3.10 python3.9 python3.8 python3 python; do
    if command -v $cmd &> /dev/null; then
        PYTHON_CMD=$cmd
        echo "Found Python: $PYTHON_CMD"
        $PYTHON_CMD --version
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "ERROR: Python not found. Please install Python 3.x"
    exit 1
fi

# Check Python dependencies
echo "Installing required packages..."
$PYTHON_CMD -m pip install -q flask fastapi uvicorn psycopg2-binary requests python-dotenv flask-caching || echo "Warning: Package installation failed, but we'll try to continue anyway"

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
$PYTHON_CMD seed_database.py || { 
    echo "Error: Database seeding failed"
    exit 1
}
cd ..

# Start FastAPI backend (using simplified version)
echo "Starting FastAPI backend on port 8000..."
cd backend
$PYTHON_CMD simple_api.py > ../logs/fastapi.log 2>&1 &
FASTAPI_PID=$!
cd ..

# Check if FastAPI process is running
if ! ps -p $FASTAPI_PID > /dev/null; then
    echo "Error: FastAPI failed to start. Check logs/fastapi.log for details."
    exit 1
fi

# Give FastAPI time to start
echo "Waiting for FastAPI backend to start..."
MAX_RETRIES=15
for i in $(seq 1 $MAX_RETRIES); do
    if curl -s http://localhost:8000/health > /dev/null; then
        break
    fi

    # Check if process is still running
    if ! ps -p $FASTAPI_PID > /dev/null; then
        echo "Error: FastAPI process stopped unexpectedly. Check logs/fastapi.log for details."
        cat logs/fastapi.log
        exit 1
    fi

    echo "Waiting for FastAPI backend (attempt $i/$MAX_RETRIES)..."
    sleep 2

    if [ $i -eq $MAX_RETRIES ]; then
        echo "Error: FastAPI failed to become ready after $MAX_RETRIES attempts"
        exit 1
    fi
done

# Start Flask frontend (using simplified version)
echo "Starting Flask frontend on port 5001..."
cd frontend
# Set the backend URL environment variable
export BACKEND_URL="http://localhost:8000"
$PYTHON_CMD simple_app.py > ../logs/flask.log 2>&1 &
FLASK_PID=$!
cd ..

# Check if Flask process is running
if ! ps -p $FLASK_PID > /dev/null; then
    echo "Error: Flask failed to start. Check logs/flask.log for details."
    exit 1
fi

# Wait for Flask to be ready
echo "Waiting for Flask frontend to start..."
MAX_RETRIES=15
for i in $(seq 1 $MAX_RETRIES); do
    if curl -s http://localhost:5001 > /dev/null; then
        break
    fi

    # Check if process is still running
    if ! ps -p $FLASK_PID > /dev/null; then
        echo "Error: Flask process stopped unexpectedly. Check logs/flask.log for details."
        cat logs/flask.log
        exit 1
    fi

    echo "Waiting for Flask frontend (attempt $i/$MAX_RETRIES)..."
    sleep 2

    if [ $i -eq $MAX_RETRIES ]; then
        echo "Error: Flask failed to become ready after $MAX_RETRIES attempts"
        exit 1
    fi
done

# Verify FastAPI is working
echo "Checking FastAPI health..."
curl -s http://localhost:8000/health

# Verify FastAPI metrics
echo -e "\nChecking FastAPI metrics (sample)..."
curl -s http://localhost:8000/api/metrics | head -n 1

# Verify Flask is working
echo -e "\nChecking Flask frontend..."
if curl -s http://localhost:5001 > /dev/null; then
    echo "Flask frontend is accessible"
else
    echo "Warning: Flask frontend is not accessible"
fi

echo "Services started with PIDs:"
echo "- FastAPI: $FASTAPI_PID"
echo "- Flask: $FLASK_PID"

echo -e "\nAccess the web interface at: http://localhost:5001"
echo "Access the dashboard at: http://localhost:5001/dashboard"
echo "Access the API at: http://localhost:8000/api/metrics"

echo "Press Ctrl+C to stop all services"

# Wait for both processes
wait $FASTAPI_PID $FLASK_PID