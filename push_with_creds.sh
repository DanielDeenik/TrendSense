#!/bin/bash
# Debug script to verify if we can access secret values
echo "Checking if username is accessible: ${GITHUB_USERNAME:-NOT_FOUND}"
echo "Checking if token is accessible (masked): ${GITHUB_TRENDSENSE_TOKEN:0:4}...${GITHUB_TRENDSENSE_TOKEN: -4}"

# Print environment variables for debugging
echo "All environment variables starting with GITHUB_:"
env | grep GITHUB_

# Try pushing with direct URL construction
GITHUB_USER="${GITHUB_USERNAME}"
GITHUB_TOKEN="${GITHUB_TRENDSENSE_TOKEN}"
REPO_URL="https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/DanielDeenik/TrendSense.git"

echo "Attempting to push to: https://${GITHUB_USER}:****@github.com/DanielDeenik/TrendSense.git"
git push "$REPO_URL" main