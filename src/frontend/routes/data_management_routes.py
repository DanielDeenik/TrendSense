"""
Data Management Routes

This module provides Flask routes for the data management system.
"""

import os
import logging
import json
from typing import Dict, List, Any
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename

# Import data management components
from src.data_management import (
    get_rag_data_manager, get_ai_connector,
    get_data_source_connector, get_data_storage, get_data_retrieval
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
data_management_bp = Blueprint('data_management', __name__, url_prefix='/data-management')

# Initialize data management components
ai_connector = get_ai_connector()
rag_data_manager = get_rag_data_manager(ai_connector)
data_storage = get_data_storage()
data_retrieval = get_data_retrieval()

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'json', 'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    """Check if a file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@data_management_bp.route('/')
def index():
    """Render the data management dashboard."""
    try:
        # Get data sources
        data_sources = data_retrieval.get_data_for_display('data_sources')
        
        # Get recent data processing jobs
        processing_jobs = data_retrieval.get_data_for_display(
            'processing_jobs',
            sort=[('timestamp', -1)],
            limit=10
        )
        
        # Get collection stats
        collection_stats = []
        collections = ['companies', 'funds', 'projects', 'metrics', 'insights']
        
        for collection in collections:
            # Count documents in collection
            count = len(data_retrieval.get_data_for_display(collection))
            collection_stats.append({
                'name': collection,
                'count': count
            })
        
        return render_template(
            'data_management/dashboard.html',
            active_nav='data_management',
            data_sources=data_sources,
            processing_jobs=processing_jobs,
            collection_stats=collection_stats,
            ai_available=ai_connector.is_available()
        )
    
    except Exception as e:
        logger.error(f"Error rendering data management dashboard: {str(e)}")
        return render_template(
            'fin_errors/fin_500.html',
            active_nav='data_management',
            error_message=f"Error rendering data management dashboard: {str(e)}"
        )

@data_management_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    """Handle file uploads for data processing."""
    if request.method == 'POST':
        try:
            # Check if a file was uploaded
            if 'file' not in request.files:
                flash('No file part', 'error')
                return redirect(request.url)
            
            file = request.files['file']
            
            # Check if a file was selected
            if file.filename == '':
                flash('No file selected', 'error')
                return redirect(request.url)
            
            # Check if the file has an allowed extension
            if not allowed_file(file.filename):
                flash(f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}', 'error')
                return redirect(request.url)
            
            # Save the file
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(os.getcwd(), 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            
            # Get form data
            source_type = request.form.get('source_type', '').lower()
            collection_name = request.form.get('collection_name', '')
            enrich_with_rag = request.form.get('enrich_with_rag') == 'on'
            
            # Determine source type from file extension if not provided
            if not source_type:
                extension = filename.rsplit('.', 1)[1].lower()
                if extension in ['json']:
                    source_type = 'json'
                elif extension in ['csv']:
                    source_type = 'csv'
                elif extension in ['xlsx', 'xls']:
                    source_type = 'excel'
            
            # Process the file
            options = {
                'collection_name': collection_name,
                'enrich_with_rag': enrich_with_rag
            }
            
            result = rag_data_manager.process_data_source(source_type, file_path, options)
            
            # Store the processing job
            job_data = {
                'source_type': source_type,
                'source_path': file_path,
                'collection_name': collection_name,
                'enrich_with_rag': enrich_with_rag,
                'result': result
            }
            
            data_storage.store_data(job_data, 'processing_jobs')
            
            # Store the data source
            source_data = {
                'name': filename,
                'type': source_type,
                'path': file_path,
                'collection_name': collection_name,
                'processed': True,
                'record_count': result.get('records_processed', 0)
            }
            
            data_storage.store_data(source_data, 'data_sources')
            
            # Flash success message
            if result.get('success'):
                flash(f'Successfully processed {result.get("records_processed", 0)} records', 'success')
            else:
                flash(f'Error processing file: {result.get("error", "Unknown error")}', 'error')
            
            return redirect(url_for('data_management.index'))
        
        except Exception as e:
            logger.error(f"Error processing uploaded file: {str(e)}")
            flash(f'Error processing file: {str(e)}', 'error')
            return redirect(request.url)
    
    # GET request
    return render_template(
        'data_management/upload.html',
        active_nav='data_management',
        ai_available=ai_connector.is_available()
    )

@data_management_bp.route('/api', methods=['GET', 'POST'])
def api():
    """Handle API data processing."""
    if request.method == 'POST':
        try:
            # Get form data
            api_url = request.form.get('api_url', '')
            collection_name = request.form.get('collection_name', '')
            enrich_with_rag = request.form.get('enrich_with_rag') == 'on'
            
            # Process the API data
            options = {
                'collection_name': collection_name,
                'enrich_with_rag': enrich_with_rag,
                'method': request.form.get('method', 'GET'),
                'headers': json.loads(request.form.get('headers', '{}')),
                'params': json.loads(request.form.get('params', '{}')),
                'data': request.form.get('data', '')
            }
            
            result = rag_data_manager.process_data_source('api', api_url, options)
            
            # Store the processing job
            job_data = {
                'source_type': 'api',
                'source_path': api_url,
                'collection_name': collection_name,
                'enrich_with_rag': enrich_with_rag,
                'result': result
            }
            
            data_storage.store_data(job_data, 'processing_jobs')
            
            # Store the data source
            source_data = {
                'name': api_url,
                'type': 'api',
                'path': api_url,
                'collection_name': collection_name,
                'processed': True,
                'record_count': result.get('records_processed', 0)
            }
            
            data_storage.store_data(source_data, 'data_sources')
            
            # Flash success message
            if result.get('success'):
                flash(f'Successfully processed {result.get("records_processed", 0)} records', 'success')
            else:
                flash(f'Error processing API data: {result.get("error", "Unknown error")}', 'error')
            
            return redirect(url_for('data_management.index'))
        
        except Exception as e:
            logger.error(f"Error processing API data: {str(e)}")
            flash(f'Error processing API data: {str(e)}', 'error')
            return redirect(request.url)
    
    # GET request
    return render_template(
        'data_management/api.html',
        active_nav='data_management',
        ai_available=ai_connector.is_available()
    )

@data_management_bp.route('/view/<collection_name>')
def view_collection(collection_name):
    """View data in a collection."""
    try:
        # Get query parameters
        limit = int(request.args.get('limit', 50))
        skip = int(request.args.get('skip', 0))
        
        # Get data from collection
        data = data_retrieval.get_data_for_display(
            collection_name,
            limit=limit,
            skip=skip
        )
        
        # Count total documents
        total_count = len(data_retrieval.get_data_for_display(collection_name))
        
        return render_template(
            'data_management/view_collection.html',
            active_nav='data_management',
            collection_name=collection_name,
            data=data,
            total_count=total_count,
            limit=limit,
            skip=skip
        )
    
    except Exception as e:
        logger.error(f"Error viewing collection {collection_name}: {str(e)}")
        return render_template(
            'fin_errors/fin_500.html',
            active_nav='data_management',
            error_message=f"Error viewing collection {collection_name}: {str(e)}"
        )

@data_management_bp.route('/view/<collection_name>/<document_id>')
def view_document(collection_name, document_id):
    """View a document in a collection."""
    try:
        # Get document
        document = data_retrieval.get_data_by_id(collection_name, document_id)
        
        if not document:
            flash(f'Document not found: {document_id}', 'error')
            return redirect(url_for('data_management.view_collection', collection_name=collection_name))
        
        return render_template(
            'data_management/view_document.html',
            active_nav='data_management',
            collection_name=collection_name,
            document=document
        )
    
    except Exception as e:
        logger.error(f"Error viewing document {document_id} in collection {collection_name}: {str(e)}")
        return render_template(
            'fin_errors/fin_500.html',
            active_nav='data_management',
            error_message=f"Error viewing document {document_id} in collection {collection_name}: {str(e)}"
        )

@data_management_bp.route('/api/process', methods=['POST'])
def api_process():
    """API endpoint for processing data."""
    try:
        # Get JSON data
        data = request.json
        
        # Get parameters
        source_type = data.get('source_type', '').lower()
        source_path = data.get('source_path', '')
        collection_name = data.get('collection_name', '')
        options = data.get('options', {})
        
        # Add collection name to options
        options['collection_name'] = collection_name
        
        # Process the data
        result = rag_data_manager.process_data_source(source_type, source_path, options)
        
        # Store the processing job
        job_data = {
            'source_type': source_type,
            'source_path': source_path,
            'collection_name': collection_name,
            'options': options,
            'result': result
        }
        
        data_storage.store_data(job_data, 'processing_jobs')
        
        # Return result
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error processing data via API: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@data_management_bp.route('/api/collections/<collection_name>', methods=['GET'])
def api_get_collection(collection_name):
    """API endpoint for getting data from a collection."""
    try:
        # Get query parameters
        limit = int(request.args.get('limit', 50))
        skip = int(request.args.get('skip', 0))
        
        # Get data from collection
        data = data_retrieval.get_data_for_display(
            collection_name,
            limit=limit,
            skip=skip
        )
        
        # Return data
        return jsonify({
            'success': True,
            'data': data
        })
    
    except Exception as e:
        logger.error(f"Error getting data from collection {collection_name} via API: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@data_management_bp.route('/api/collections/<collection_name>/<document_id>', methods=['GET'])
def api_get_document(collection_name, document_id):
    """API endpoint for getting a document from a collection."""
    try:
        # Get document
        document = data_retrieval.get_data_by_id(collection_name, document_id)
        
        if not document:
            return jsonify({
                'success': False,
                'error': f'Document not found: {document_id}'
            }), 404
        
        # Return document
        return jsonify({
            'success': True,
            'data': document
        })
    
    except Exception as e:
        logger.error(f"Error getting document {document_id} from collection {collection_name} via API: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@data_management_bp.route('/api/chart/<collection_name>', methods=['GET'])
def api_get_chart_data(collection_name):
    """API endpoint for getting chart data from a collection."""
    try:
        # Get query parameters
        x_field = request.args.get('x_field')
        y_field = request.args.get('y_field')
        group_by = request.args.get('group_by')
        
        # Get chart data
        chart_data = data_retrieval.get_data_for_chart(
            collection_name,
            x_field=x_field,
            y_field=y_field,
            group_by=group_by
        )
        
        # Return chart data
        return jsonify({
            'success': True,
            'data': chart_data
        })
    
    except Exception as e:
        logger.error(f"Error getting chart data from collection {collection_name} via API: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
