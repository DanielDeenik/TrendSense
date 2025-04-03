#!/bin/bash
set -e

echo "Starting Sustainability Dashboard with reliable port handling..."

# Check if psutil is installed, install if needed
python3 -c "import psutil" 2>/dev/null || pip install psutil

# Copy port_manager.py to the correct location if it's not there
if [ ! -f frontend/port_manager.py ]; then
  cp port_manager.py frontend/ 2>/dev/null || true
fi

# Run our reliable starter script
cd frontend
python3 port_manager.py --flask direct_app.py

# This script should not exit normally as the Python script keeps running
echo "Flask application has stopped."