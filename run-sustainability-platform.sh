#!/bin/bash
# Run script for Sustainability Intelligence Platform with Storytelling capabilities
# This script starts both the FastAPI backend and Flask frontend

# Set environment variables
export FLASK_ENV=development
export FLASK_DEBUG=1
export STORYTELLING_API_URL=http://localhost:8080

echo "Starting Sustainability Intelligence Platform with Storytelling capabilities..."

# Start the FastAPI storytelling backend
echo "Starting FastAPI Storytelling backend on port 8080..."
python run-storytelling-api.py &
FASTAPI_PID=$!

# Wait for FastAPI to start
sleep 3
echo "FastAPI backend started with PID: $FASTAPI_PID"

# Start the Flask frontend
echo "Starting Flask frontend on port 5000..."
cd frontend && python direct_app.py &
FLASK_PID=$!

echo "Flask frontend started with PID: $FLASK_PID"
echo "Sustainability Intelligence Platform is now running!"
echo "Flask frontend: http://localhost:5000"
echo "FastAPI backend: http://localhost:8080"
echo "API documentation: http://localhost:8080/docs"

# Function to handle script termination
function cleanup {
  echo "Shutting down services..."
  kill $FASTAPI_PID $FLASK_PID
  echo "Services stopped."
}

# Register the cleanup function for script termination
trap cleanup EXIT

# Keep the script running
echo "Press Ctrl+C to stop all services"
wait
