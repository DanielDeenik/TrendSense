#!/bin/bash

# Direct GitHub push script for TrendSense
# This script uses a direct git command with embedded token for pushing

# Configuration
REPO_URL="https://github.com/DanielDeenik/TrendSense.git"
BRANCH="main"
USERNAME="DanielDeenik"

# Prompt for token
echo "Enter your GitHub personal access token (it won't be shown on screen):"
read -s TOKEN

# Configure Git
git config --global user.email "user@example.com"
git config --global user.name "$USERNAME"

# Make sure we're in the git root directory
cd "$(git rev-parse --show-toplevel)" || exit 1

# Add all files
git add .

# Commit changes
echo "Committing changes..."
git commit -m "Update from Replit $(date +%Y-%m-%d_%H-%M-%S)"

# Push to GitHub with token
echo "Pushing to GitHub..."
git push "https://$USERNAME:$TOKEN@github.com/DanielDeenik/TrendSense.git" $BRANCH

echo "Done!"