#!/bin/bash

# Run the standalone Regulatory AI Dashboard
export PORT=6000
export DEBUG=true
export WERKZEUG_DEBUG_PIN=off
export PYTHONUNBUFFERED=1
export PYTHONPATH=$(pwd)

echo "Starting Standalone Regulatory AI Dashboard on port 6000..."
cd frontend && PORT=6000 python standalone_dashboard.py