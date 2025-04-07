"""
Consolidated SustainaTrend Dashboard Application
This application combines the features of all previous Flask applications into a single, well-structured application.
"""
import os
import json
import logging
import random
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, send_from_directory, request, flash, redirect, url_for
from dotenv import load_dotenv
from pymongo import MongoClient
from mongodb_config import MONGODB_URI
from vc_pe.routes import vc_pe_bp
from werkzeug.utils import secure_filename
from vc_pe.data_manager import DataManager
import pandas as pd

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Initialize MongoDB client
try:
    client = MongoClient(MONGODB_URI)
    db = client.get_database()
    logger.info("Successfully connected to MongoDB")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    client = None
    db = None

# Initialize Flask app
app = Flask(__name__, 
            template_folder='frontend/templates',
            static_folder='frontend/static')
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'sustainatrend-platform-secret-key-2025')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
app.config['MONGODB_URI'] = MONGODB_URI  # Use the URI from mongodb_config.py

# Register VC/PE blueprint
app.register_blueprint(vc_pe_bp, url_prefix='/vc-pe')

# Register VC routes blueprint
from backend.routes.vc_routes import vc_bp
app.register_blueprint(vc_bp, url_prefix='/vc')

# Register Trendsense routes blueprint
from backend.routes.trendsense_routes import trendsense_bp
app.register_blueprint(trendsense_bp, url_prefix='/trendsense')

# Initialize SQLAlchemy database
from backend.database import init_db
init_db(app)

# Initialize DataManager
data_manager = DataManager(app.config['MONGODB_URI'])

# Sample data generators with MongoDB integration
def generate_metrics_data():
    """Generate sustainability metrics data from MongoDB"""
    if db is None:
        return {
            'carbon_intensity': {
                'value': round(random.uniform(10, 15), 1),
                'change': round(random.uniform(-20, -10), 1),
                'trend': 'negative'
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
                'trend': 'negative'
            }
        }
    
    try:
        metrics = db.metrics.find_one({}, sort=[('timestamp', -1)])
        if metrics:
            return metrics['data']
        return generate_metrics_data()  # Fallback to sample data
    except Exception as e:
        logger.error(f"Error fetching metrics data: {str(e)}")
        return generate_metrics_data()  # Fallback to sample data

def generate_emissions_data():
    """Generate emissions data from MongoDB"""
    if db is None:
        dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]
        dates.reverse()
        return {
            'labels': dates,
            'datasets': [
                {
                    'label': 'Scope 1',
                    'data': [round(random.uniform(100, 200), 1) for _ in range(30)],
                    'borderColor': '#dc3545',
                    'tension': 0.1
                },
                {
                    'label': 'Scope 2',
                    'data': [round(random.uniform(50, 150), 1) for _ in range(30)],
                    'borderColor': '#198754',
                    'tension': 0.1
                },
                {
                    'label': 'Scope 3',
                    'data': [round(random.uniform(200, 400), 1) for _ in range(30)],
                    'borderColor': '#0d6efd',
                    'tension': 0.1
                }
            ]
        }
    
    try:
        emissions = db.emissions.find_one({}, sort=[('timestamp', -1)])
        if emissions:
            return emissions['data']
        return generate_emissions_data()  # Fallback to sample data
    except Exception as e:
        logger.error(f"Error fetching emissions data: {str(e)}")
        return generate_emissions_data()  # Fallback to sample data

def generate_insights():
    """Generate AI-powered sustainability insights from MongoDB"""
    if db is None:
        return [
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
    
    try:
        insights = db.insights.find_one({}, sort=[('timestamp', -1)])
        if insights:
            return insights['data']
        return generate_insights()  # Fallback to sample data
    except Exception as e:
        logger.error(f"Error fetching insights data: {str(e)}")
        return generate_insights()  # Fallback to sample data

def generate_regulatory_data():
    """Generate regulatory compliance data from MongoDB"""
    if db is None:
        return {
            'stats': {
                'documents_count': 12,
                'document_growth': '24%',
                'frameworks_count': 7,
                'recent_framework': 'EU CSRD',
                'avg_compliance': '78%',
                'analysis_count': 48,
                'analysis_growth': '18%'
            },
            'frameworks': [
                {"id": "CSRD", "name": "EU Corporate Sustainability Reporting Directive", "count": 5},
                {"id": "TCFD", "name": "Task Force on Climate-related Financial Disclosures", "count": 3},
                {"id": "GRI", "name": "Global Reporting Initiative", "count": 4},
                {"id": "SASB", "name": "Sustainability Accounting Standards Board", "count": 2},
                {"id": "SFDR", "name": "Sustainable Finance Disclosure Regulation", "count": 1},
                {"id": "SDG", "name": "UN Sustainable Development Goals", "count": 3},
                {"id": "CDP", "name": "Carbon Disclosure Project", "count": 2}
            ],
            'compliance_data': {
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
        }
    
    try:
        regulatory = db.regulatory.find_one({}, sort=[('timestamp', -1)])
        if regulatory:
            return regulatory['data']
        return generate_regulatory_data()  # Fallback to sample data
    except Exception as e:
        logger.error(f"Error fetching regulatory data: {str(e)}")
        return generate_regulatory_data()  # Fallback to sample data

# Routes
@app.route('/')
@app.route('/dashboard')
def dashboard():
    """Render the main dashboard page"""
    return render_template('dashboard.html')

@app.route('/regulatory')
def regulatory_dashboard():
    """Render the regulatory dashboard page"""
    # Create navigation context
    navigation = {
        'main_dashboard': 'http://localhost:3000/',
        'strategy_hub': 'http://localhost:3000/strategy-hub',
        'regulatory_dashboard': 'http://localhost:3000/regulatory',
        'document_upload': 'http://localhost:3000/regulatory/upload',
        'standalone': False
    }
    
    # API status
    api_status = {
        'fastapi': {'status': 'online', 'url': 'http://localhost:3000'},
        'flask': {'status': 'online', 'url': 'http://localhost:3000'}
    }
    
    return render_template(
        'regulatory/simple_dashboard.html',
        active_nav='regulatory',
        page_title="Regulatory AI Dashboard",
        stats=generate_regulatory_data()['stats'],
        recent_documents=[],
        recent_activity=[],
        api_status=api_status,
        theme='dark',
        navigation=navigation
    )

# API Endpoints
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

@app.route('/api/regulatory')
def regulatory_data():
    """API endpoint for regulatory data"""
    return jsonify(generate_regulatory_data())

@app.route('/api/frameworks')
def api_frameworks():
    """API endpoint for supported frameworks"""
    return jsonify(generate_regulatory_data()['frameworks'])

@app.route('/api/compliance-data')
def api_compliance_data():
    """API endpoint for compliance data"""
    return jsonify(generate_regulatory_data()['compliance_data'])

@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    mongodb_status = "connected" if client is not None else "disconnected"
    return jsonify({
        "status": "ok",
        "time": datetime.now().isoformat(),
        "version": "1.0.0",
        "mongodb": mongodb_status
    })

# Enhanced Routes for Data-Driven Insights
@app.route('/insights/esg-performance')
def esg_performance():
    """ESG Performance Analytics Page"""
    metrics = generate_metrics_data()
    return render_template(
        'insights/esg_performance.html',
        active_page='esg-performance',
        metrics=metrics
    )

@app.route('/insights/carbon-footprint')
def carbon_footprint():
    """Carbon Footprint Analysis Page"""
    emissions = generate_emissions_data()
    return render_template(
        'insights/carbon_footprint.html',
        active_page='carbon-footprint',
        emissions=emissions
    )

@app.route('/insights/regulatory-compliance')
def regulatory_compliance():
    """Regulatory Compliance Dashboard"""
    regulatory = generate_regulatory_data()
    return render_template(
        'insights/regulatory_compliance.html',
        active_page='regulatory-compliance',
        regulatory=regulatory
    )

@app.route('/portfolio/companies')
def portfolio_companies():
    """Portfolio Companies Overview"""
    return render_template(
        'portfolio/companies.html',
        active_page='companies'
    )

@app.route('/portfolio/benchmarks')
def portfolio_benchmarks():
    """Industry Benchmarks and Comparisons"""
    return render_template(
        'portfolio/benchmarks.html',
        active_page='benchmarks'
    )

@app.route('/portfolio/trends')
def portfolio_trends():
    """Portfolio Trends and Analysis"""
    return render_template(
        'portfolio/trends.html',
        active_page='trends'
    )

@app.route('/analytics/predictions')
def analytics_predictions():
    """AI-Powered Predictions"""
    return render_template(
        'analytics/predictions.html',
        active_page='predictions'
    )

@app.route('/analytics/risk-assessment')
def analytics_risk():
    """Risk Assessment Dashboard"""
    return render_template(
        'analytics/risk_assessment.html',
        active_page='risk-assessment'
    )

@app.route('/analytics/recommendations')
def analytics_recommendations():
    """AI-Generated Recommendations"""
    return render_template(
        'analytics/recommendations.html',
        active_page='recommendations'
    )

@app.route('/reports/custom')
def reports_custom():
    """Custom Report Builder"""
    return render_template(
        'reports/custom.html',
        active_page='custom-reports'
    )

@app.route('/reports/scheduled')
def reports_scheduled():
    """Scheduled Reports Management"""
    return render_template(
        'reports/scheduled.html',
        active_page='scheduled-reports'
    )

@app.route('/reports/exports')
def reports_exports():
    """Data Export Interface"""
    return render_template(
        'reports/exports.html',
        active_page='exports'
    )

# Enhanced API Endpoints for Data-Driven Insights
@app.route('/api/portfolio/companies')
def api_portfolio_companies():
    """API endpoint for portfolio companies data"""
    # Sample data - replace with actual database query
    return jsonify({
        'companies': [
            {
                'id': 1,
                'name': 'EcoTech Solutions',
                'sector': 'Clean Energy',
                'esg_score': 85,
                'carbon_footprint': 120,
                'sustainability_rating': 'A',
                'risk_level': 'Low',
                'trend': 'positive'
            },
            {
                'id': 2,
                'name': 'GreenBuild Construction',
                'sector': 'Construction',
                'esg_score': 78,
                'carbon_footprint': 450,
                'sustainability_rating': 'B+',
                'risk_level': 'Medium',
                'trend': 'stable'
            }
        ]
    })

@app.route('/api/portfolio/benchmarks')
def api_portfolio_benchmarks():
    """API endpoint for industry benchmarks"""
    # Sample data - replace with actual database query
    return jsonify({
        'benchmarks': {
            'industry_averages': {
                'esg_score': 72,
                'carbon_footprint': 580,
                'water_usage': 850,
                'renewable_energy': 35
            },
            'top_performers': {
                'esg_score': 89,
                'carbon_footprint': 180,
                'water_usage': 420,
                'renewable_energy': 78
            }
        }
    })

@app.route('/api/analytics/predictions')
def api_analytics_predictions():
    """API endpoint for AI-powered predictions"""
    # Sample data - replace with actual ML predictions
    return jsonify({
        'predictions': {
            'esg_trends': [
                {
                    'metric': 'Carbon Emissions',
                    'current': 580,
                    'prediction_3m': 520,
                    'prediction_6m': 480,
                    'confidence': 0.85
                },
                {
                    'metric': 'Water Usage',
                    'current': 850,
                    'prediction_3m': 800,
                    'prediction_6m': 750,
                    'confidence': 0.82
                }
            ],
            'risk_factors': [
                {
                    'factor': 'Regulatory Changes',
                    'probability': 0.75,
                    'impact': 'High',
                    'timeline': '6-12 months'
                },
                {
                    'factor': 'Resource Scarcity',
                    'probability': 0.60,
                    'impact': 'Medium',
                    'timeline': '12-24 months'
                }
            ]
        }
    })

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv', 'xlsx', 'xls'}

def preview_file(file_path):
    """Generate preview data for uploaded file"""
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        return {
            'companies_count': len(df['company'].unique()) if 'company' in df.columns else 0,
            'data_points': len(df),
            'date_range': f"{df['date'].min()} - {df['date'].max()}" if 'date' in df.columns else 'N/A',
            'headers': df.columns.tolist(),
            'sample_rows': df.head(5).values.tolist()
        }
    except Exception as e:
        app.logger.error(f"Error generating preview: {str(e)}")
        return None

@app.route('/import')
def import_data():
    """Render data import template"""
    # Get recent imports from MongoDB
    recent_imports = []
    try:
        esg_imports = data_manager.db.esg_data.find().sort('import_date', -1).limit(5)
        carbon_imports = data_manager.db.carbon_data.find().sort('import_date', -1).limit(5)
        
        for imp in esg_imports:
            recent_imports.append({
                'import_date': imp['import_date'].strftime('%Y-%m-%d %H:%M'),
                'type': 'ESG Data',
                'file_name': os.path.basename(imp['source_file']),
                'status': 'Completed',
                'actions': [
                    {'label': 'View', 'url': url_for('view_import', import_id=str(imp['_id']))},
                    {'label': 'Delete', 'url': url_for('delete_import', import_id=str(imp['_id']))}
                ]
            })
        
        for imp in carbon_imports:
            recent_imports.append({
                'import_date': imp['import_date'].strftime('%Y-%m-%d %H:%M'),
                'type': 'Carbon Data',
                'file_name': os.path.basename(imp['source_file']),
                'status': 'Completed',
                'actions': [
                    {'label': 'View', 'url': url_for('view_import', import_id=str(imp['_id']))},
                    {'label': 'Delete', 'url': url_for('delete_import', import_id=str(imp['_id']))}
                ]
            })
        
        recent_imports.sort(key=lambda x: x['import_date'], reverse=True)
    except Exception as e:
        app.logger.error(f"Error fetching recent imports: {str(e)}")
        recent_imports = []

    return render_template('data_import.html', recent_imports=recent_imports)

@app.route('/import/esg', methods=['POST'])
def import_esg_data():
    """Handle ESG data file upload and import"""
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('import_data'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('import_data'))
    
    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload CSV or Excel files.', 'error')
        return redirect(url_for('import_data'))
    
    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        logger.info(f"Saving file to: {file_path}")
        file.save(file_path)
        
        # Generate preview data
        logger.info(f"Generating preview for file: {file_path}")
        preview_data = preview_file(file_path)
        
        # Import data
        logger.info(f"Importing ESG data from: {file_path}")
        result = data_manager.import_esg_data(file_path)
        logger.info(f"Import result: {result}")
        
        if result['success']:
            flash('ESG data imported successfully', 'success')
            return render_template('data_import.html', 
                                preview_data=preview_data,
                                recent_imports=result.get('metrics', []))
        else:
            flash(f"Import failed: {result['message']}", 'error')
            return redirect(url_for('import_data'))
            
    except Exception as e:
        app.logger.error(f"Error importing ESG data: {str(e)}")
        flash(f"Error importing ESG data: {str(e)}", 'error')
        return redirect(url_for('import_data'))

@app.route('/import/carbon', methods=['POST'])
def import_carbon_data():
    """Handle carbon data file upload and import"""
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('import_data'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('import_data'))
    
    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload CSV or Excel files.', 'error')
        return redirect(url_for('import_data'))
    
    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        logger.info(f"Saving file to: {file_path}")
        file.save(file_path)
        
        # Generate preview data
        logger.info(f"Generating preview for file: {file_path}")
        preview_data = preview_file(file_path)
        
        # Import data
        logger.info(f"Importing carbon data from: {file_path}")
        result = data_manager.import_carbon_data(file_path)
        logger.info(f"Import result: {result}")
        
        if result['success']:
            flash('Carbon data imported successfully', 'success')
            return render_template('data_import.html', 
                                preview_data=preview_data,
                                recent_imports=result.get('emissions', []))
        else:
            flash(f"Import failed: {result['message']}", 'error')
            return redirect(url_for('import_data'))
            
    except Exception as e:
        app.logger.error(f"Error importing carbon data: {str(e)}")
        flash(f"Error importing carbon data: {str(e)}", 'error')
        return redirect(url_for('import_data'))

@app.route('/import/<import_id>')
def view_import(import_id):
    """View details of a specific import"""
    try:
        # Try to find in ESG data first
        import_data = data_manager.db.esg_data.find_one({'_id': import_id})
        if not import_data:
            # Try carbon data if not found in ESG
            import_data = data_manager.db.carbon_data.find_one({'_id': import_id})
        
        if not import_data:
            flash('Import not found', 'error')
            return redirect(url_for('import_data'))
        
        preview_data = preview_file(import_data['source_file'])
        return render_template('data_import.html', preview_data=preview_data)
        
    except Exception as e:
        app.logger.error(f"Error viewing import: {str(e)}")
        flash(f"Error viewing import: {str(e)}", 'error')
        return redirect(url_for('import_data'))

@app.route('/import/<import_id>/delete')
def delete_import(import_id):
    """Delete a specific import"""
    try:
        # Try to delete from ESG data first
        result = data_manager.db.esg_data.delete_one({'_id': import_id})
        if result.deleted_count == 0:
            # Try carbon data if not found in ESG
            result = data_manager.db.carbon_data.delete_one({'_id': import_id})
        
        if result.deleted_count > 0:
            flash('Import deleted successfully', 'success')
        else:
            flash('Import not found', 'error')
            
    except Exception as e:
        app.logger.error(f"Error deleting import: {str(e)}")
        flash(f"Error deleting import: {str(e)}", 'error')
    
    return redirect(url_for('import_data'))

if __name__ == '__main__':
    # Use the configuration from run.py
    app.run()