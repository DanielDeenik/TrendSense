"""
Standalone script to run the Flask frontend
"""
import os
import sys
from flask import Flask, send_from_directory, jsonify, request

app = Flask(__name__, 
           static_folder='frontend/static',
           template_folder='frontend/templates')

@app.route('/')
def index():
    """Serve the index.html file"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/dashboard')
def dashboard():
    """Serve the dashboard page"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "API is running"})

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory(app.static_folder, path)

def run_flask(host='0.0.0.0', port=None):
    """Run the Flask frontend directly"""
    if port is None:
        port = int(os.environ.get('PORT', 5000))
        
    print(f"Starting Flask frontend on http://{host}:{port}")
    app.run(host=host, port=port, debug=True)

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the Flask application
    run_flask(port=port)