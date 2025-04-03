#!/bin/bash

# Launch the standalone dashboard workflow in Replit
echo "Launching Standalone Regulatory AI Dashboard..."

# Set up port
export PORT=6000
export PYTHONPATH="/home/runner/workspace:/home/runner/workspace/frontend"

# Run the standalone dashboard
cd frontend
python standalone_dashboard.py