"""
Trendsense Integration Routes

This module provides routes for integrating with the Trendsense API
for enhanced sustainability analysis.
"""

from flask import Blueprint, request, jsonify, render_template, current_app
import os
import json
import logging
from werkzeug.utils import secure_filename
from datetime import datetime
from ..document_processor import DocumentProcessor
from ..trendsense_client import TrendsenseClient

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
trendsense_bp = Blueprint('trendsense', __name__)

# Initialize clients
trendsense_client = TrendsenseClient()
document_processor = DocumentProcessor()

# Helper function to get allowed file extensions
def allowed_file(filename, allowed_extensions=None):
    if allowed_extensions is None:
        allowed_extensions = {'txt', 'pdf', 'doc', 'docx', 'csv', 'xlsx', 'xls'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Document Analysis Routes
@trendsense_bp.route('/api/trendsense/analyze', methods=['POST'])
def analyze_with_trendsense():
    """
    Send data to Trendsense for advanced sustainability analysis
    
    Expected JSON payload:
    {
        "document_data": {...},
        "document_text": "...",
        "metadata": {...}
    }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
            
        # Extract data from request
        document_data = data.get('document_data', {})
        document_text = data.get('document_text', '')
        metadata = data.get('metadata', {})
        
        # Send to Trendsense
        result = trendsense_client.submit_document_analysis(
            document_data,
            document_text,
            metadata
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in analyze_with_trendsense: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@trendsense_bp.route('/api/trendsense/upload', methods=['POST'])
def upload_document():
    """
    Upload and analyze a document with Trendsense
    
    Expected form data:
    - file: The document file
    - document_type: Type of document (e.g., 'sustainability_report', 'esg_disclosure')
    - metadata: Optional JSON string with additional metadata
    """
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400
            
        file = request.files['file']
        
        # Check if file has a name
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
            
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'File type not allowed'
            }), 400
            
        # Get document type
        document_type = request.form.get('document_type', 'sustainability_report')
        
        # Get metadata
        metadata = {}
        if 'metadata' in request.form:
            try:
                metadata = json.loads(request.form['metadata'])
            except json.JSONDecodeError:
                logger.warning(f"Invalid metadata JSON: {request.form['metadata']}")
        
        # Save file
        filename = secure_filename(file.filename)
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Process document
        result = document_processor.process_document(file_path, document_type, metadata)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in upload_document: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Company Analysis Routes
@trendsense_bp.route('/api/trendsense/company', methods=['POST'])
def analyze_company():
    """
    Get sustainability analysis for a company
    
    Expected JSON payload:
    {
        "company_name": "...",
        "sector": "...",
        "metrics": {...}
    }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
            
        # Get sustainability score
        result = trendsense_client.get_sustainability_score(data)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in analyze_company: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Industry Benchmark Routes
@trendsense_bp.route('/api/trendsense/benchmarks', methods=['POST'])
def get_benchmarks():
    """
    Get industry benchmarks for sustainability metrics
    
    Expected JSON payload:
    {
        "sector": "...",
        "metrics": ["carbon_emissions", "water_usage", ...]
    }
    """
    try:
        data = request.json
        
        if not data or 'sector' not in data:
            return jsonify({
                'success': False,
                'error': 'Sector is required'
            }), 400
            
        # Get benchmarks
        sector = data['sector']
        metrics = data.get('metrics')
        
        result = trendsense_client.get_industry_benchmarks(sector, metrics)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in get_benchmarks: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Trend Analysis Routes
@trendsense_bp.route('/api/trendsense/trends/<sector>', methods=['GET'])
def get_trends(sector):
    """
    Get trend analysis for a sector
    
    Query parameters:
    - timeframe: Analysis timeframe (e.g., "1m", "3m", "6m", "1y")
    """
    try:
        # Get timeframe from query parameters
        timeframe = request.args.get('timeframe', '1y')
        
        # Get trend analysis
        result = trendsense_client.get_trend_analysis(sector, timeframe)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in get_trends: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Webhook Routes
@trendsense_bp.route('/api/trendsense/webhook', methods=['POST'])
def trendsense_webhook():
    """
    Receive callback data from Trendsense analysis
    
    Expected JSON payload:
    {
        "analysis_id": "...",
        "status": "...",
        "results": {...}
    }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
            
        # Log webhook data
        logger.info(f"Received Trendsense webhook: {json.dumps(data)}")
        
        # Process webhook data (implement your logic here)
        # For example, update a database record, trigger a notification, etc.
        
        return jsonify({
            'success': True,
            'message': 'Webhook processed successfully'
        })
        
    except Exception as e:
        logger.error(f"Error in trendsense_webhook: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# UI Routes
@trendsense_bp.route('/trendsense')
def trendsense_dashboard():
    """Render the Trendsense dashboard page"""
    return render_template('trendsense/dashboard.html')

@trendsense_bp.route('/trendsense/upload')
def trendsense_upload():
    """Render the document upload page"""
    return render_template('trendsense/upload.html')

@trendsense_bp.route('/trendsense/company/<company_id>')
def company_analysis(company_id):
    """Render the company analysis page"""
    return render_template('trendsense/company_analysis.html', company_id=company_id)

@trendsense_bp.route('/trendsense/benchmarks/<sector>')
def industry_benchmarks(sector):
    """Render the industry benchmarks page"""
    return render_template('trendsense/benchmarks.html', sector=sector)

@trendsense_bp.route('/trendsense/trends/<sector>')
def trend_analysis(sector):
    """Render the trend analysis page"""
    return render_template('trendsense/trends.html', sector=sector) 