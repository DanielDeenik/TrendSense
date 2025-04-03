#!/bin/bash

# Simple script to check if we got truncated output
echo "Checking if push was successful..."

# Create a temp directory 
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR" || exit 1

# Try to clone the repo (will fail if it wasn't pushed successfully)
git clone https://github.com/DanielDeenik/TrendSense.git

# Check the result
if [ -d "TrendSense" ]; then
  echo "SUCCESS: Repository was successfully pushed to GitHub!"
  ls -la TrendSense | head -n 10
else
  echo "FAILURE: Repository was not successfully pushed to GitHub."
fi

# Clean up
cd .. && rm -rf "$TEMP_DIR"