"""
Simple Flask app for SustainaTrend Dashboard
"""
import os
import json
import random
from flask import Flask, render_template, jsonify, send_from_directory
from datetime import datetime, timedelta

app = Flask(__name__, 
            template_folder='frontend/templates',
            static_folder='frontend/static')

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

@app.route('/')
@app.route('/dashboard')
def dashboard():
    """Render the dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/metrics')
def metrics_data():
    """API endpoint for metrics data"""
    return jsonify(generate_metrics_data())

@app.route('/api/emissions')
def emissions_data():
    """API endpoint for emissions chart data"""
    return jsonify(generate_emissions_data())

@app.route('/api/insights')
def insights_data():
    """API endpoint for sustainability insights"""
    return jsonify(generate_insights())

@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "ok", "time": datetime.now().isoformat()})

if __name__ == '__main__':
    # Use PORT environment variable if available (for Replit compatibility)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)