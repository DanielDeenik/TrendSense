"""
Simple standalone application for SustainaTrend Dashboard
"""
import os
import sys
import json
import logging
from flask import Flask, render_template, jsonify, request, redirect, url_for, abort

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask
app = Flask(__name__, 
            template_folder='frontend/templates',
            static_folder='frontend/static')
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'sustainatrend-platform-secret-key-2025')

@app.route('/')
def index():
    """Serve the index/dashboard page"""
    return render_template('dashboard.html')

@app.route('/dashboard')
def dashboard():
    """Serve the dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/dashboard-data')
def dashboard_data():
    """Get data for the dashboard"""
    try:
        # For demonstration, we'll return static data
        return jsonify({
            "carbon_intensity": {"value": 12.4, "change": -15.3},
            "esg_score": {"value": 73.8, "change": 2.5},
            "renewable_energy": {"value": 38, "change": 8},
            "water_intensity": {"value": 2.3, "change": -12.2}
        })
    except Exception as e:
        logger.error(f"Error fetching dashboard data: {str(e)}")
        return jsonify({
            "error": str(e)
        }), 500

@app.route('/api/insights')
def insights():
    """Get sustainability insights for the dashboard"""
    try:
        # Return static insights
        return jsonify({
            "emissions_trend": {
                "title": "Emissions Trend Analysis",
                "content": "Your emissions reduction is outpacing industry benchmarks by 6.2%. Key contributors: Renewable energy adoption and facility upgrades."
            },
            "regulatory_readiness": {
                "title": "Regulatory Readiness",
                "content": "CSRD preparation is at 75% completion, with data collection systems fully implemented. Focus areas: scope 3 emissions and biodiversity impacts."
            },
            "water_risk": {
                "title": "Water Risk Alert",
                "content": "Three manufacturing facilities are in high water stress regions. Consider implementing advanced water recycling technologies."
            }
        })
    except Exception as e:
        logger.error(f"Error fetching insights: {str(e)}")
        return jsonify({
            "error": str(e)
        }), 500

@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        "status": "ok",
        "version": "1.0.0"
    })

if __name__ == "__main__":
    # Use the PORT environment variable provided by Replit, or default to 5000
    port = int(os.environ.get("PORT", 5000))
    
    logger.info(f"Starting Flask server on port {port}")
    
    # Start the Flask app with the correct host and port
    app.run(host="0.0.0.0", port=port, debug=True)