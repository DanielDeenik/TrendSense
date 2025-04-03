#!/bin/bash

# Test theme preference in the URL parameter
echo "Testing theme preference with URL parameter..."
curl -s "http://localhost:5000/monetization?theme=light" | grep -A3 "<html" 

echo ""
echo "Testing default theme (should be dark-mode)..."
curl -s "http://localhost:5000/monetization" | grep -A3 "<html"