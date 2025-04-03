#!/bin/bash

# Start the complete SustainaTrend platform with Regulatory AI components
echo "Starting SustainaTrend Complete Platform..."

# 1. Start the main application on port 5000
echo "Starting main dashboard on port 5000..."
cd frontend && PORT=5000 python app.py > /tmp/main_app.log 2>&1 &
MAIN_PID=$!
echo "Main application started with PID: $MAIN_PID"

# 2. Start the standalone Regulatory AI Dashboard on port 6000
echo "Starting Regulatory AI Dashboard on port 6000..."
cd frontend && PORT=6000 python standalone_dashboard.py > /tmp/regulatory_dashboard.log 2>&1 &
REG_PID=$!
echo "Regulatory AI Dashboard started with PID: $REG_PID"

echo ""
echo "SustainaTrend Platform started successfully!"
echo "Main Dashboard: http://localhost:5000/"
echo "Regulatory AI Dashboard: http://localhost:6000/"
echo ""
echo "Use the following links to access the dashboards directly:"
echo "- Main Dashboard: http://localhost:5000/strategy-hub"
echo "- Regulatory AI Dashboard: http://localhost:6000/"
echo ""
echo "To stop the platform, run: kill $MAIN_PID $REG_PID"

# Keep the script running to hold the terminal
wait