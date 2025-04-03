#!/bin/bash

# Standalone Document Upload Runner
# This script provides a direct way to run the standalone document upload module
# without the overhead of the full application.

echo "Starting Standalone Document Upload on port 7000..."

# Kill any process using port 7000 (if any)
fuser -k 7000/tcp 2>/dev/null || true

# Create uploads directory if it doesn't exist
mkdir -p frontend/uploads

# Set environment variables
export DEBUG=true
export FLASK_ENV=development
export HOST=0.0.0.0
export PORT=7000
export REPLIT_ENVIRONMENT=true
export ENABLE_REPLIT_AUTH=false

# Make sure we're not using WERKZEUG environment variables that could cause issues
unset WERKZEUG_SERVER_FD
unset WERKZEUG_RUN_MAIN

# Run the standalone upload script
cd frontend && python standalone_upload.py