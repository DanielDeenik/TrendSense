#!/bin/bash

# Direct GitHub push script for TrendSense
# This script uses direct credentials to push to GitHub

# GitHub repository details
GITHUB_USERNAME="DanDeenik"
REPO_NAME="TrendSense"
GITHUB_REPO="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# Function to handle errors
handle_error() {
  echo "ERROR: $1"
  exit 1
}

echo "Setting up Git configuration..."
git config --global user.name "$GITHUB_USERNAME" || handle_error "Failed to set Git user name"
git config --global user.email "dan@example.com" || handle_error "Failed to set Git user email"

# Check if .git directory exists
if [ ! -d ".git" ]; then
  echo "Initializing Git repository..."
  git init || handle_error "Failed to initialize Git repository"
fi

echo "Adding all files to Git..."
git add . || handle_error "Failed to add files to Git"

echo "Committing changes..."
git commit -m "Initial commit of TrendSense platform" || handle_error "Failed to commit changes"

# Add remote repository if it doesn't exist
if ! git remote | grep -q "origin"; then
  echo "Adding GitHub remote repository..."
  git remote add origin "$GITHUB_REPO" || handle_error "Failed to add remote repository"
else
  echo "GitHub remote repository already exists."
fi

echo "Pushing to GitHub..."
echo "Please enter your GitHub personal access token when prompted."
git push -u origin main || git push -u origin master || handle_error "Failed to push to GitHub"

echo "Successfully pushed TrendSense to GitHub!"