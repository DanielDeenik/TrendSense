#!/bin/bash

# Direct GitHub push script with minimal dependencies
# Sets HOME to ensure proper git configuration

# Temp home directory for git config
export HOME="/tmp/git_home"
mkdir -p "$HOME"

# Take token as input
echo "Enter your GitHub token:"
read -s TOKEN

# Set git config in the temp home
git config --global user.name "DanielDeenik"
git config --global user.email "user@example.com"

# Create temp directory for clean push
TEMP_DIR=$(mktemp -d)
echo "Created temporary directory: $TEMP_DIR"

# Copy important files
echo "Copying project files..."
cp -r server shared client backend package.json package-lock.json README.md ARCHITECTURE.md VC_PE_ENGINE.md AI-DRIVEN-ARCHITECTURE.md .gitignore "$TEMP_DIR/"

# Initialize and push
cd "$TEMP_DIR" || exit 1
git init
git add .
git commit -m "Direct push from Replit $(date +%Y-%m-%d_%H-%M-%S)"

# Add remote with token
git remote add origin "https://DanielDeenik:${TOKEN}@github.com/DanielDeenik/TrendSense.git"

# Push (try both main and master branches)
echo "Pushing to GitHub..."
git push -u origin main --force || git push -u origin master --force

echo "Push completed. Check your GitHub repository."