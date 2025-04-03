"""
Simple standalone regulatory dashboard for SustainaTrend™ platform
This lightweight Flask application provides a direct regulatory dashboard interface
"""
import os
import json
import logging
from flask import Flask, render_template, jsonify, send_from_directory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, 
           template_folder="frontend/templates",
           static_folder="frontend/static")

# Get port with fallback to 6000
port = int(os.environ.get('PORT', 6000))

# Sample data for dashboard
stats = {
    'documents_count': 12,
    'document_growth': '24%',
    'frameworks_count': 7,
    'recent_framework': 'EU CSRD',
    'avg_compliance': '78%',
    'analysis_count': 48,
    'analysis_growth': '18%'
}

recent_documents = [
    {
        'title': 'Company XYZ Sustainability Report 2025',
        'date': 'Mar 24, 2025',
        'framework': 'EU CSRD',
        'score': 92,
        'status': 'Compliant',
        'preview': 'This sustainability report outlines our commitment to environmental stewardship and social responsibility...'
    },
    {
        'title': 'Environmental Impact Statement Q1',
        'date': 'Mar 18, 2025',
        'framework': 'GRI',
        'score': 78,
        'status': 'Needs Review',
        'preview': 'We have made significant progress in reducing our carbon footprint through innovative technologies...'
    },
    {
        'title': 'Climate Risk Disclosure',
        'date': 'Mar 10, 2025',
        'framework': 'TCFD',
        'score': 65,
        'status': 'Incomplete',
        'preview': 'This document presents our comprehensive analysis of climate-related risks and their potential impacts...'
    }
]

recent_activity = [
    {
        'action': 'Document Uploaded',
        'details': 'Sustainability Report 2025',
        'time': '2 hours ago',
        'user': 'John D.'
    },
    {
        'action': 'Analysis Completed',
        'details': 'Climate Risk Disclosure',
        'time': '4 hours ago',
        'user': 'System'
    },
    {
        'action': 'Framework Added',
        'details': 'Added ISSB framework support',
        'time': '1 day ago',
        'user': 'Admin'
    }
]

@app.route('/')
def dashboard():
    """Render the simplified dashboard page"""
    logger.info("Dashboard accessed")
    
    # Create navigation context
    navigation = {
        'main_dashboard': 'http://localhost:5000/',
        'strategy_hub': 'http://localhost:5000/strategy-hub',
        'regulatory_dashboard': 'http://localhost:6000/',
        'document_upload': 'http://localhost:5000/regulatory-ai-refactored/upload',
        'standalone': True
    }
    
    # API status
    api_status = {
        'fastapi': {'status': 'online', 'url': 'http://localhost:8080'},
        'flask': {'status': 'online', 'url': 'http://localhost:5000'},
        'standalone_dashboard': {'status': 'online', 'url': f'http://localhost:{port}'}
    }
    
    return render_template(
        'regulatory/simple_dashboard.html',
        active_nav='regulatory-ai-refactored',
        page_title="Regulatory AI Dashboard (Simplified)",
        stats=stats,
        recent_documents=recent_documents,
        recent_activity=recent_activity,
        api_status=api_status,
        theme='dark',
        navigation=navigation
    )

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files"""
    logger.info(f"Serving static file: {path}")
    return send_from_directory(os.path.join(os.getcwd(), 'frontend/static'), path)

@app.route('/api/frameworks')
def api_frameworks():
    """API endpoint for supported frameworks"""
    frameworks = [
        {"id": "CSRD", "name": "EU Corporate Sustainability Reporting Directive", "count": 5},
        {"id": "TCFD", "name": "Task Force on Climate-related Financial Disclosures", "count": 3},
        {"id": "GRI", "name": "Global Reporting Initiative", "count": 4},
        {"id": "SASB", "name": "Sustainability Accounting Standards Board", "count": 2},
        {"id": "SFDR", "name": "Sustainable Finance Disclosure Regulation", "count": 1},
        {"id": "SDG", "name": "UN Sustainable Development Goals", "count": 3},
        {"id": "CDP", "name": "Carbon Disclosure Project", "count": 2}
    ]
    return jsonify(frameworks)

@app.route('/api/compliance-data')
def api_compliance_data():
    """API endpoint for compliance data"""
    compliance_data = {
        "labels": ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"],
        "datasets": [
            {
                "label": "EU CSRD",
                "data": [65, 68, 70, 72, 75, 78]
            },
            {
                "label": "TCFD",
                "data": [55, 59, 65, 70, 73, 76]
            },
            {
                "label": "GRI",
                "data": [60, 62, 65, 68, 70, 74]
            }
        ]
    }
    return jsonify(compliance_data)

@app.route('/api/analysis-data')
def api_analysis_data():
    """API endpoint for analysis data"""
    analysis_data = {
        "labels": ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"],
        "datasets": [
            {
                "label": "Gap Analyses",
                "data": [8, 12, 15, 18, 22, 28]
            },
            {
                "label": "RAG Queries",
                "data": [15, 18, 22, 30, 35, 42]
            }
        ]
    }
    return jsonify(analysis_data)

if __name__ == '__main__':
    logger.info(f"Starting simplified dashboard on port {port}")
    logger.info(f"Template folder: {app.template_folder}")
    logger.info(f"Static folder: {app.static_folder}")
    app.run(host='0.0.0.0', port=port, debug=True)