#!/bin/bash
set -e

echo "Starting Flask frontend..."
cd frontend

# Set backend URL
export BACKEND_URL="http://localhost:8080"
echo "Using BACKEND_URL: $BACKEND_URL"

# Use PORT from environment or default to 5000
export PORT=${PORT:-5000}
echo "Using PORT: $PORT"

# Check if psutil is installed, install if needed
python3 -c "import psutil" 2>/dev/null || pip install psutil

# Make sure port_manager.py is available
if [ ! -f port_manager.py ]; then
  cp ../port_manager.py ./ 2>/dev/null || echo "Warning: port_manager.py not found"
fi

# Use our port manager to run Flask reliably
python3 port_manager.py --port $PORT --host 0.0.0.0 --flask direct_app.py