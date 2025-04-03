#!/bin/bash

# Direct GitHub push script for TrendSense

# GitHub repository details
GITHUB_USERNAME="DanDeenik"
REPO_NAME="TrendSense"
GITHUB_REPO="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

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
  echo "GitHub remote repository already exists."
fi

echo "Pushing to GitHub..."
echo "Please enter your GitHub personal access token when prompted."
git push -u origin main || git push -u origin master

echo "Successfully pushed TrendSense to GitHub!"
