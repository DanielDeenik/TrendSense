#!/bin/bash

# Script to export code to a zip file for easy downloading
# This avoids GitHub authentication issues

# Create a timestamp for the filename
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
EXPORT_NAME="TrendSense_export_${TIMESTAMP}.zip"

# Create a temporary directory for organizing files
TEMP_DIR="temp_export"
mkdir -p "$TEMP_DIR"

# Copy relevant files to the temp directory
echo "Copying files to temporary directory..."
cp -r backend client server shared examples frontend scripts test_files "$TEMP_DIR"
cp *.py *.js *.sh *.md *.json "$TEMP_DIR" 2>/dev/null || true

# Create the zip file
echo "Creating zip file $EXPORT_NAME..."
zip -r "$EXPORT_NAME" "$TEMP_DIR"

# Clean up
rm -rf "$TEMP_DIR"

echo "Export completed: $EXPORT_NAME"
echo "Download this file from the Replit Files panel, then extract and push from your local machine."