#!/bin/bash

echo "==============================================================="
echo "Starting Refactored Dashboard on port 3000..."
echo "==============================================================="

# Kill any existing process running on port 3000
if lsof -i:3000 > /dev/null 2>&1; then
  echo "Killing existing process on port 3000..."
  lsof -i:3000 | grep LISTEN | awk '{print $2}' | xargs kill -9
  sleep 2
fi

# Navigate to frontend directory
cd frontend

# Set environment variables
export PORT=3000
export FLASK_ENV=development
export DEBUG=true
export HOST=0.0.0.0
export REPLIT_ENVIRONMENT=true
export WERKZEUG_RUN_MAIN=true

# Unset any existing Werkzeug FD to avoid restart issues
unset WERKZEUG_SERVER_FD

# Check if Pinecone API key is available, if not, set a warning flag
if [ -z "$PINECONE_API_KEY" ]; then
  echo "Warning: PINECONE_API_KEY environment variable not set!"
  echo "RAG functionality will not be available."
fi

echo "Starting Python app: $(pwd)/refactored_app.py"
echo "With PORT=$PORT"

# Start the application with nohup to allow it to run in the background
nohup python refactored_app.py > ../refactored_dashboard.log 2>&1 &

# Wait for server to start
echo "Waiting for server to start up..."
sleep 5

# Check if server is running
if curl -s http://localhost:3000/ > /dev/null; then
  echo "Server started successfully! Available at http://localhost:3000/"
  echo "Log file is at ../refactored_dashboard.log"
  echo "Dashboard should be accessible at http://localhost:3000/regulatory/dashboard"
else
  echo "Server failed to start properly. Check logs at ../refactored_dashboard.log"
  # Show last few lines of log
  echo "Last 10 lines of log:"
  tail -n 10 ../refactored_dashboard.log
fi