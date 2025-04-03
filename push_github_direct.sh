#!/bin/bash

# Script to push to GitHub using inline credentials
# Usage: ./push_github_direct.sh <username> <token>

if [ $# -ne 2 ]; then
    echo "Usage: ./push_github_direct.sh <username> <token>"
    exit 1
fi

USERNAME=$1
TOKEN=$2

# The direct URL format with credentials
REPO_URL="https://$USERNAME:$TOKEN@github.com/DanielDeenik/TrendSense.git"

echo "Attempting to push directly to GitHub..."
git push "$REPO_URL" main

echo "Push attempt completed."