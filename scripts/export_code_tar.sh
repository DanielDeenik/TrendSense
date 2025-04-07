#!/bin/bash

# Create a timestamped tarball for download and manual pushing
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ARCHIVE_NAME="TrendSense_export_${TIMESTAMP}.tar.gz"

echo "Creating archive $ARCHIVE_NAME..."

# Check which files and directories exist before adding them to the list
echo "Checking for important files and directories..."

# Start with an empty file
> files_to_archive.txt

# Add directories if they exist
for dir in server shared client backend; do
  if [ -d "./$dir" ]; then
    echo "./$dir" >> files_to_archive.txt
    echo "Added directory: $dir"
  fi
done

# Add files if they exist
for file in package.json package-lock.json README.md ARCHITECTURE.md VC_PE_ENGINE.md AI-DRIVEN-ARCHITECTURE.md .gitignore; do
  if [ -f "./$file" ]; then
    echo "./$file" >> files_to_archive.txt
    echo "Added file: $file"
  fi
done

# Create the tarball
tar -czf "$ARCHIVE_NAME" -T files_to_archive.txt

echo "Archive created: $ARCHIVE_NAME"
echo
echo "INSTRUCTIONS:"
echo "1. Download the archive file from the Files pane"
echo "2. Extract it on your local machine: tar -xzf $ARCHIVE_NAME"
echo "3. Navigate to the extracted directory: cd TrendSense"
echo "4. Initialize a new git repo: git init"
echo "5. Add all files: git add ."
echo "6. Commit: git commit -m 'Initial commit from Replit export'"
echo "7. Add remote: git remote add origin https://github.com/DanielDeenik/TrendSense.git"
echo "8. Push to GitHub: git push -u origin main"
echo
echo "These steps will let you push the code directly from your machine without authentication issues."

# Clean up
rm files_to_archive.txt