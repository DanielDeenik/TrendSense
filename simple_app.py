#!/usr/bin/env python3
"""
Simple SustainaTrend Dashboard - Minimal Version for GitHub

This application provides a lightweight version of the SustainaTrend dashboard
using only the Python standard library and minimal external dependencies.
"""

import os
import json
import http.server
import socketserver
import datetime
import random
import threading
import logging
from urllib.parse import parse_qs, urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SustainaTrend")

# Default port (environment variable or 5000)
PORT = int(os.environ.get('PORT', 5000))

# Sample data generation functions
def generate_metrics_data():
    """Generate sample sustainability metrics data"""
    return {
        "metrics": [
            {
                "id": 1,
                "name": "Carbon Intensity",
                "category": "emissions",
                "value": round(random.uniform(15, 45), 2),
                "unit": "tCO₂e/M$",
                "timestamp": datetime.datetime.now().isoformat()
            },
            {
                "id": 2,
                "name": "ESG Score", 
                "category": "governance",
                "value": round(random.uniform(65, 95), 1),
                "unit": "points",
                "timestamp": datetime.datetime.now().isoformat()
            },
            {
                "id": 3,
                "name": "Renewable Energy", 
                "category": "energy",
                "value": round(random.uniform(35, 85), 1),
                "unit": "%",
                "timestamp": datetime.datetime.now().isoformat()
            },
            {
                "id": 4,
                "name": "Water Intensity", 
                "category": "water",
                "value": round(random.uniform(2.5, 8.5), 2),
                "unit": "kL/M$",
                "timestamp": datetime.datetime.now().isoformat()
            }
        ]
    }

def generate_emissions_data():
    """Generate sample emissions data for the chart"""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return {
        "labels": months,
        "datasets": [
            {
                "label": "Scope 1 & 2 Emissions",
                "data": [
                    round(random.uniform(30, 40), 1) for _ in range(12)
                ],
                "borderColor": "rgba(75, 192, 192, 1)",
                "backgroundColor": "rgba(75, 192, 192, 0.2)"
            },
            {
                "label": "Scope 3 Emissions",
                "data": [
                    round(random.uniform(60, 100), 1) for _ in range(12)
                ],
                "borderColor": "rgba(153, 102, 255, 1)",
                "backgroundColor": "rgba(153, 102, 255, 0.2)"
            }
        ]
    }

def generate_insights():
    """Generate AI-powered sustainability insights"""
    insights = [
        "Carbon intensity decreased by 12.5% compared to last quarter, indicating improved operational efficiency.",
        "Water usage trends show seasonal variations with peaks during summer months.",
        "ESG governance score has improved steadily over the past 6 months.",
        "Renewable energy adoption is accelerating, with a 15% increase in the last reporting period.",
        "Supply chain emissions (Scope 3) remain the largest contributor to overall carbon footprint."
    ]
    return {"insights": insights}

class SustainaTrendHandler(http.server.SimpleHTTPRequestHandler):
    """Handler for SustainaTrend Dashboard requests"""
    
    def __init__(self, *args, **kwargs):
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == "/" or path == "/index.html":
            self.send_dashboard()
        elif path == "/api/metrics":
            self.send_json_response(generate_metrics_data())
        elif path == "/api/emissions":
            self.send_json_response(generate_emissions_data())
        elif path == "/api/insights":
            self.send_json_response(generate_insights())
        elif path == "/api/health":
            self.send_json_response({"status": "healthy", "timestamp": datetime.datetime.now().isoformat()})
        else:
            self.send_error(404, "File not found")
    
    def send_json_response(self, data):
        """Send a JSON response"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def send_dashboard(self):
        """Send the dashboard HTML"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SustainaTrend™ Dashboard</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                body {{ background-color: #f5f7f9; }}
                .dashboard-card {{
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    transition: transform 0.3s;
                    overflow: hidden;
                }}
                .dashboard-card:hover {{ transform: translateY(-5px); }}
                .metric-value {{ font-size: 2.5rem; font-weight: 700; }}
                .metric-unit {{ font-size: 0.9rem; color: #6c757d; }}
                .navbar-brand {{ font-weight: 700; }}
                .highlight {{ background-color: #e8f4f8; padding: 2px 5px; border-radius: 3px; }}
                .metric-card-emissions {{ border-top: 4px solid #dc3545; }}
                .metric-card-governance {{ border-top: 4px solid #198754; }}
                .metric-card-energy {{ border-top: 4px solid #0d6efd; }}
                .metric-card-water {{ border-top: 4px solid #6f42c1; }}
            </style>
        </head>
        <body>
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                <div class="container">
                    <a class="navbar-brand" href="/">
                        SustainaTrend™ Dashboard
                    </a>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarNav">
                        <ul class="navbar-nav ms-auto">
                            <li class="nav-item">
                                <a class="nav-link active" href="/">Dashboard</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="/companies">Companies</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="/patterns">Patterns</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="/documents">Documents</a>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>

            <div class="container mt-4">
                <div class="row mb-4">
                    <div class="col">
                        <h1>Sustainability Overview</h1>
                        <p class="text-muted">Portfolio-wide sustainability metrics and trends</p>
                    </div>
                    <div class="col-auto">
                        <div class="btn-group" role="group">
                            <button type="button" class="btn btn-outline-primary">This Month</button>
                            <button type="button" class="btn btn-outline-primary">Quarter</button>
                            <button type="button" class="btn btn-primary">Year</button>
                        </div>
                    </div>
                </div>

                <div class="row" id="metrics-container">
                    <div class="col-md-6 col-lg-3 mb-4">
                        <div class="card dashboard-card metric-card-emissions h-100">
                            <div class="card-body">
                                <h5 class="card-title text-muted">Carbon Intensity</h5>
                                <div class="d-flex align-items-baseline mt-3">
                                    <div class="metric-value" id="carbon-value">--</div>
                                    <div class="metric-unit ms-2" id="carbon-unit">tCO₂e/M$</div>
                                </div>
                                <div class="mt-3 text-success" id="carbon-trend">
                                    <i class="bi bi-arrow-down"></i> Loading...
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 col-lg-3 mb-4">
                        <div class="card dashboard-card metric-card-governance h-100">
                            <div class="card-body">
                                <h5 class="card-title text-muted">ESG Score</h5>
                                <div class="d-flex align-items-baseline mt-3">
                                    <div class="metric-value" id="esg-value">--</div>
                                    <div class="metric-unit ms-2" id="esg-unit">points</div>
                                </div>
                                <div class="mt-3 text-success" id="esg-trend">
                                    <i class="bi bi-arrow-up"></i> Loading...
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 col-lg-3 mb-4">
                        <div class="card dashboard-card metric-card-energy h-100">
                            <div class="card-body">
                                <h5 class="card-title text-muted">Renewable Energy</h5>
                                <div class="d-flex align-items-baseline mt-3">
                                    <div class="metric-value" id="renewable-value">--</div>
                                    <div class="metric-unit ms-2" id="renewable-unit">%</div>
                                </div>
                                <div class="mt-3 text-success" id="renewable-trend">
                                    <i class="bi bi-arrow-up"></i> Loading...
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 col-lg-3 mb-4">
                        <div class="card dashboard-card metric-card-water h-100">
                            <div class="card-body">
                                <h5 class="card-title text-muted">Water Intensity</h5>
                                <div class="d-flex align-items-baseline mt-3">
                                    <div class="metric-value" id="water-value">--</div>
                                    <div class="metric-unit ms-2" id="water-unit">kL/M$</div>
                                </div>
                                <div class="mt-3 text-success" id="water-trend">
                                    <i class="bi bi-arrow-down"></i> Loading...
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="row mb-4">
                    <div class="col-lg-8">
                        <div class="card dashboard-card h-100">
                            <div class="card-body">
                                <h5 class="card-title">Emissions Trend</h5>
                                <div class="chart-container" style="position: relative; height:300px;">
                                    <canvas id="emissionsChart"></canvas>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-4">
                        <div class="card dashboard-card h-100">
                            <div class="card-body">
                                <h5 class="card-title">AI Insights</h5>
                                <ul class="list-group list-group-flush" id="insights-list">
                                    <li class="list-group-item bg-transparent">Loading insights...</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <footer class="bg-light py-4 mt-5">
                <div class="container">
                    <div class="row">
                        <div class="col-md-6">
                            <p>© 2025 SustainaTrend™. All rights reserved.</p>
                        </div>
                        <div class="col-md-6 text-md-end">
                            <p>Version 1.0.0 | <a href="#" class="text-decoration-none">GitHub</a></p>
                        </div>
                    </div>
                </div>
            </footer>

            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
            <script>
                // Fetch metrics data
                fetch('/api/metrics')
                    .then(response => response.json())
                    .then(data => {
                        const metrics = data.metrics;
                        
                        // Update Carbon Intensity
                        const carbonMetric = metrics.find(m => m.name === "Carbon Intensity");
                        if (carbonMetric) {
                            document.getElementById('carbon-value').textContent = carbonMetric.value;
                            document.getElementById('carbon-unit').textContent = carbonMetric.unit;
                            document.getElementById('carbon-trend').innerHTML = 
                                `<i class="bi bi-arrow-down"></i> 12.5% vs last quarter`;
                        }
                        
                        // Update ESG Score
                        const esgMetric = metrics.find(m => m.name === "ESG Score");
                        if (esgMetric) {
                            document.getElementById('esg-value').textContent = esgMetric.value;
                            document.getElementById('esg-unit').textContent = esgMetric.unit;
                            document.getElementById('esg-trend').innerHTML = 
                                `<i class="bi bi-arrow-up"></i> 7.2% vs last quarter`;
                        }
                        
                        // Update Renewable Energy
                        const renewableMetric = metrics.find(m => m.name === "Renewable Energy");
                        if (renewableMetric) {
                            document.getElementById('renewable-value').textContent = renewableMetric.value;
                            document.getElementById('renewable-unit').textContent = renewableMetric.unit;
                            document.getElementById('renewable-trend').innerHTML = 
                                `<i class="bi bi-arrow-up"></i> 15.0% vs last quarter`;
                        }
                        
                        // Update Water Intensity
                        const waterMetric = metrics.find(m => m.name === "Water Intensity");
                        if (waterMetric) {
                            document.getElementById('water-value').textContent = waterMetric.value;
                            document.getElementById('water-unit').textContent = waterMetric.unit;
                            document.getElementById('water-trend').innerHTML = 
                                `<i class="bi bi-arrow-down"></i> 5.3% vs last quarter`;
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching metrics:', error);
                    });
                
                // Fetch emissions chart data
                fetch('/api/emissions')
                    .then(response => response.json())
                    .then(data => {
                        const ctx = document.getElementById('emissionsChart').getContext('2d');
                        new Chart(ctx, {
                            type: 'line',
                            data: {
                                labels: data.labels,
                                datasets: data.datasets
                            },
                            options: {
                                responsive: true,
                                maintainAspectRatio: false,
                                scales: {
                                    y: {
                                        beginAtZero: true,
                                        title: {
                                            display: true,
                                            text: 'tCO₂e'
                                        }
                                    }
                                }
                            }
                        });
                    })
                    .catch(error => {
                        console.error('Error fetching emissions data:', error);
                    });
                
                // Fetch insights data
                fetch('/api/insights')
                    .then(response => response.json())
                    .then(data => {
                        const insightsList = document.getElementById('insights-list');
                        insightsList.innerHTML = '';
                        
                        data.insights.forEach(insight => {
                            const li = document.createElement('li');
                            li.className = 'list-group-item bg-transparent';
                            li.innerHTML = insight;
                            insightsList.appendChild(li);
                        });
                    })
                    .catch(error => {
                        console.error('Error fetching insights:', error);
                    });
            </script>
        </body>
        </html>
        """
        
        self.wfile.write(html.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to add timestamp to log messages"""
        logger.info("%s - %s" % (self.address_string(), format % args))

def main():
    """Run the server"""
    try:
        logger.info(f"Starting SustainaTrend Dashboard on port {PORT}")
        server = socketserver.TCPServer(("0.0.0.0", PORT), SustainaTrendHandler)
        logger.info(f"Server running at http://0.0.0.0:{PORT}")
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")

if __name__ == "__main__":
    main()