#!/bin/bash

# Direct GitHub push script for TrendSense with token authentication

# GitHub repository details
GITHUB_USERNAME="DanDeenik"
REPO_NAME="TrendSense"
TOKEN="ghp_4yXqQdbKQj9YDG9XcZw5WN3NaZmWNS"
GITHUB_REPO="https://$TOKEN@github.com/$GITHUB_USERNAME/$REPO_NAME.git"

echo "Setting up Git configuration..."
git config --global user.name "$GITHUB_USERNAME"
git config --global user.email "dan@example.com"

# Check if .git directory exists
if [ ! -d ".git" ]; then
  echo "Initializing Git repository..."
  git init
fi

echo "Adding all files to Git..."
git add .

echo "Committing changes..."
git commit -m "Initial commit of TrendSense platform"

# Add remote repository if it doesn't exist
if ! git remote | grep -q "origin"; then
  echo "Adding GitHub remote repository..."
  git remote add origin "$GITHUB_REPO"
else
  echo "Updating GitHub remote repository..."
  git remote set-url origin "$GITHUB_REPO"
fi

echo "Pushing to GitHub..."
git push -u origin main || git push -u origin master

echo "Successfully pushed TrendSense to GitHub!"
