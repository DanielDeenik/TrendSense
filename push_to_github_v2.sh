#!/bin/bash

# Script to push to GitHub using credentials provided as arguments
# Usage: ./push_to_github_v2.sh <username> <token>

# Check if both username and token are provided
if [ $# -ne 2 ]; then
    echo "Usage: ./push_to_github_v2.sh <username> <token>"
    exit 1
fi

USERNAME=$1
TOKEN=$2

# Configure Git to use the token
git config --local credential.helper "store --file=.git/credentials"
echo "https://$USERNAME:$TOKEN@github.com" > .git/credentials

# Push to GitHub
echo "Pushing to GitHub..."
git push origin main

# Remove credentials
rm .git/credentials
git config --local --unset credential.helper

echo "Push completed and credentials removed."