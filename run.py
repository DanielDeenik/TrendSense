#!/usr/bin/env python3
"""
Main development server runner for SustainaTrend Platform.
This script starts the Flask development server with proper configuration.
"""

import os
import sys
from app import app

if __name__ == '__main__':
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Get port from environment or default to 5000
        port = int(os.getenv('FLASK_PORT', 5000))
        debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
        
        print(f"Starting server on port {port}...")
        print(f"Debug mode: {debug}")
        
        # Start the Flask development server
        app.run(
            host='127.0.0.1',  # Only allow local connections
            port=port,
            debug=debug
        )
    except Exception as e:
        print(f"Error starting server: {str(e)}", file=sys.stderr)
        sys.exit(1) 