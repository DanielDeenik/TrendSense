#!/usr/bin/env python3
"""
Ultra Simple SustainaTrend Dashboard - Using Only Standard Library
"""
import os
import json
import random
import http.server
import socketserver
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs

# Sample data for our dashboard
def generate_metrics_data():
    """Generate sample sustainability metrics data"""
    return {
        'carbon_intensity': {
            'value': round(random.uniform(10, 15), 1),
            'change': round(random.uniform(-20, -10), 1),
            'trend': 'negative'  # Lower is better for carbon intensity
        },
        'esg_score': {
            'value': round(random.uniform(70, 80), 1),
            'change': round(random.uniform(1, 5), 1),
            'trend': 'positive'
        },
        'renewable_energy': {
            'value': round(random.uniform(30, 45)),
            'change': round(random.uniform(5, 10)),
            'trend': 'positive'
        },
        'water_intensity': {
            'value': round(random.uniform(2, 3), 1),
            'change': round(random.uniform(-15, -8), 1),
            'trend': 'negative'  # Lower is better for water intensity
        }
    }

def generate_emissions_data():
    """Generate sample emissions data for the chart"""
    today = datetime.now()
    months = [(today - timedelta(days=30*i)).strftime('%b') for i in range(6)]
    months.reverse()
    
    # Generate a decreasing trend for carbon emissions
    values = []
    start_value = random.uniform(15, 20)
    for i in range(6):
        value = max(start_value - random.uniform(1, 3) * i, 5)
        values.append(round(value, 1))
    
    return {
        'labels': months,
        'data': values
    }

def generate_insights():
    """Generate AI-powered sustainability insights"""
    insights = [
        {
            'title': 'Emissions Trend Analysis',
            'content': 'Your emissions reduction is outpacing industry benchmarks by 6.2%. Key contributors: Renewable energy adoption and facility upgrades.'
        },
        {
            'title': 'Regulatory Readiness',
            'content': 'CSRD preparation is at 75% completion, with data collection systems fully implemented. Focus areas: scope 3 emissions and biodiversity impacts.'
        },
        {
            'title': 'Water Risk Alert',
            'content': 'Three manufacturing facilities are in high water stress regions. Consider implementing advanced water recycling technologies.'
        }
    ]
    return insights

class SustainaTrendHandler(http.server.SimpleHTTPRequestHandler):
    """Handler for SustainaTrend Dashboard requests"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='frontend', **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        url_parts = urlparse(self.path)
        path = url_parts.path
        
        if path == '/' or path == '/dashboard':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Send the dashboard HTML
            with open('frontend/templates/dashboard.html', 'rb') as f:
                self.wfile.write(f.read())
                
        elif path == '/api/metrics':
            self.send_json_response(generate_metrics_data())
            
        elif path == '/api/emissions':
            self.send_json_response(generate_emissions_data())
            
        elif path == '/api/insights':
            self.send_json_response(generate_insights())
            
        elif path == '/health':
            self.send_json_response({"status": "ok", "time": datetime.now().isoformat()})
            
        else:
            # Try to serve static files
            try:
                super().do_GET()
            except Exception as e:
                self.send_error(404, f"File not found: {self.path}")
    
    def send_json_response(self, data):
        """Send a JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def log_message(self, format, *args):
        """Override to add timestamp to log messages"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {self.address_string()} - {format % args}")

def main():
    """Run the server"""
    # Use PORT environment variable if available (for Replit compatibility)
    port = int(os.environ.get('PORT', 8080))
    
    print(f"Starting SustainaTrend Dashboard on port {port}...")
    
    try:
        with socketserver.TCPServer(("0.0.0.0", port), SustainaTrendHandler) as httpd:
            print(f"Server running at http://0.0.0.0:{port}/")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == '__main__':
    main()