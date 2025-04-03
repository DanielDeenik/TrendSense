#!/bin/bash
set -e

echo "Starting Sustainability Dashboard..."

# Find any process using port 5000 and terminate it gracefully
PORT=5000
PID=$(lsof -i:$PORT -t 2>/dev/null || echo "")

if [ -n "$PID" ]; then
  echo "Port $PORT is in use by process $PID, terminating..."
  kill -15 $PID 2>/dev/null || true
  # Give it a moment to terminate
  sleep 2
  # Force kill if still running
  if ps -p $PID > /dev/null 2>&1; then
    echo "Process still running, force terminating..."
    kill -9 $PID 2>/dev/null || true
    sleep 1
  fi
  echo "Port $PORT has been freed"
fi

# Start the Flask frontend application
cd frontend
echo "Starting Flask application on port $PORT..."
python app.py
