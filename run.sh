#!/bin/bash

# Display environment info
echo "Environment information:"
echo "-----------------------"
echo "User: $(whoami)"
echo "Current directory: $(pwd)"
echo "PATH: $PATH"
echo "Available binaries:"
find /bin /usr/bin -type f -executable -name "python*" 2>/dev/null || echo "No Python found"
find /bin /usr/bin -type f -executable -name "node*" 2>/dev/null || echo "No Node.js found"
echo "-----------------------"

# Try to run the server with any available method
echo "Attempting to run the server..."

# Method 1: Try direct Python
python basic_server.py || python3 basic_server.py || echo "Failed to run with direct Python"

# Method 2: Try environment
REPLIT_PYTHON=$(find /nix/store -name python3 -type f -executable 2>/dev/null | head -1)
if [ -n "$REPLIT_PYTHON" ]; then
    echo "Found Python at $REPLIT_PYTHON. Trying to run..."
    $REPLIT_PYTHON basic_server.py || echo "Failed to run with environment Python"
fi

# Method 3: Fall back to a simple server message
echo "Fallback: Simple file-based communication..."
echo "<!DOCTYPE html>
<html>
<head>
    <title>SustainaTrend Fallback</title>
</head>
<body>
    <h1>SustainaTrend Dashboard</h1>
    <p>Our server cannot be started in this environment.</p>
    <p>Please try one of these alternatives:</p>
    <ul>
        <li>View the static dashboard template at <a href='frontend/templates/dashboard.html'>frontend/templates/dashboard.html</a></li>
        <li>Run 'python basic_server.py' from the command line</li>
    </ul>
</body>
</html>" > fallback.html

echo "Created fallback.html file. Please open this file to view instructions."