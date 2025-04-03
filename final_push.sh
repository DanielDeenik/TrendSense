#!/bin/bash

# Final push attempt with complete error handling
# This script creates a completely fresh git repo and pushes all files

# Set HOME for git
export HOME="/tmp/git_home"
mkdir -p "$HOME"

# Get token
echo "Enter your GitHub token:"
read -s TOKEN

# Configure git
git config --global user.name "DanielDeenik"
git config --global user.email "user@example.com"

# Create a fresh temp directory
TEMP_DIR=$(mktemp -d)
echo "Working in: $TEMP_DIR"

# Copy ALL project files - be more thorough
echo "Copying ALL project files..."
cp -r server/ shared/ client/ backend/ "$TEMP_DIR/"
cp package.json package-lock.json README.md ARCHITECTURE.md VC_PE_ENGINE.md AI-DRIVEN-ARCHITECTURE.md "$TEMP_DIR/"

# Add other important files
cp -r .gitignore "$TEMP_DIR/" 2>/dev/null
cp -r .github "$TEMP_DIR/" 2>/dev/null

# Create a comprehensive .gitignore if it doesn't exist
if [ ! -f "$TEMP_DIR/.gitignore" ]; then
  echo "Creating .gitignore..."
  cat > "$TEMP_DIR/.gitignore" << EOF
# Node.js
node_modules/
npm-debug.log
yarn-error.log
yarn-debug.log
.pnpm-debug.log
.npm

# Python
__pycache__/
*.py[cod]
*$py.class
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Build files
/build
/dist

# Logs
logs
*.log
EOF
fi

# Navigate to temp directory
cd "$TEMP_DIR" || { echo "Failed to change to temporary directory"; exit 1; }

# Initialize git repo
echo "Initializing git repository..."
git init
git add .
git status

# Commit all files
echo "Committing files..."
git commit -m "Complete project push from Replit $(date +%Y-%m-%d_%H-%M-%S)"

# Add remote with credentials embedded in URL
echo "Adding remote repository..."
git remote add origin "https://DanielDeenik:$TOKEN@github.com/DanielDeenik/TrendSense.git"

# Push to GitHub (try both main and master)
echo "Pushing to GitHub..."
git push -u origin main --force || git push -u origin master --force

echo "Push operation completed. Check your GitHub repository."