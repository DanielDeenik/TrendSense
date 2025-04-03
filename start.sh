#!/bin/bash

# SustainaTrend startup script

echo "Starting SustainaTrend platform..."

# Check if database is available
echo "Checking database connection..."
python check_db.py

# Start the application with a simplified approach
python simple_app.py