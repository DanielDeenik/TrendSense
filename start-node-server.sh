#!/bin/bash
# Script to run the SustainaTrend Node.js server

echo "Starting SustainaTrend Dashboard (Node.js)..."
echo "---------------------------------------------"

# Run the Node.js server
if command -v node &> /dev/null
then
    node server.js
else
    echo "Node.js not found. Please install Node.js to run this server."
    exit 1
fi