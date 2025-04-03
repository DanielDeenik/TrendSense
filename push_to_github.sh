#!/bin/bash

# Script for pushing to GitHub
# Usage: bash push_to_github.sh username token

if [ $# -ne 2 ]; then
  echo "Usage: bash push_to_github.sh <username> <token>"
  exit 1
fi

USERNAME="$1"
TOKEN="$2"

# Configure git if needed
git config --global user.name "$USERNAME"
git config --global user.email "$USERNAME@users.noreply.github.com"

# Create a temp directory for the operation
TEMP_DIR=$(mktemp -d)
echo "Created temporary directory: $TEMP_DIR"

# Clone existing repo structure to temp directory
echo "Copying project files to temporary directory..."
cp -r server shared client backend package.json package-lock.json README.md ARCHITECTURE.md VC_PE_ENGINE.md AI-DRIVEN-ARCHITECTURE.md "$TEMP_DIR/" 2>/dev/null

# Navigate to temp directory
cd "$TEMP_DIR" || { echo "Failed to change to temporary directory"; exit 1; }

# Initialize git and commit files
echo "Initializing git repository..."
git init
git add .
git commit -m "Initial commit from Replit"

# Add remote with credentials embedded in URL
echo "Adding remote repository..."
git remote add origin "https://$USERNAME:$TOKEN@github.com/DanielDeenik/TrendSense.git"

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main --force

echo "Push operation completed."