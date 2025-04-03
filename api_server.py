from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import json
import random
import datetime
from typing import List, Dict, Any, Optional

app = Flask(__name__)
CORS(app)

# In-memory storage for demo purposes
funds = []
companies = []
metrics = []
patterns = []
documents = []
stories = []

# ID counters
fund_id_counter = 1
company_id_counter = 1
metric_id_counter = 1
pattern_id_counter = 1
document_id_counter = 1
story_id_counter = 1

# Helper functions to get objects by ID
def get_fund_by_id(fund_id: int):
    return next((f for f in funds if f['id'] == fund_id), None)

def get_company_by_id(company_id: int):
    return next((c for c in companies if c['id'] == company_id), None)

def get_pattern_by_id(pattern_id: int):
    return next((p for p in patterns if p['id'] == pattern_id), None)

# Initialize with sample data
def init_sample_data():
    global fund_id_counter, company_id_counter, metric_id_counter, pattern_id_counter, document_id_counter, story_id_counter
    
    # Clear existing data
    funds.clear()
    companies.clear()
    metrics.clear()
    patterns.clear()
    documents.clear()
    stories.clear()
    
    # Create a fund
    fund = {
        'id': fund_id_counter,
        'name': 'Sustainability Ventures',
        'description': 'Venture capital fund focused on sustainability investments',
        'createdAt': datetime.datetime.now().isoformat(),
        'updatedAt': datetime.datetime.now().isoformat()
    }
    funds.append(fund)
    fund_id_counter += 1
    
    # Create companies
    company1 = {
        'id': company_id_counter,
        'fundId': fund['id'],
        'name': 'EcoTech Solutions',
        'sector': 'Clean Energy',
        'description': 'Renewable energy technology provider',
        'isPublic': True,
        'createdAt': datetime.datetime.now().isoformat(),
        'updatedAt': datetime.datetime.now().isoformat()
    }
    companies.append(company1)
    company_id_counter += 1
    
    company2 = {
        'id': company_id_counter,
        'fundId': fund['id'],
        'name': 'GreenWater',
        'sector': 'Water Management',
        'description': 'Advanced water conservation systems',
        'isPublic': False,
        'createdAt': datetime.datetime.now().isoformat(),
        'updatedAt': datetime.datetime.now().isoformat()
    }
    companies.append(company2)
    company_id_counter += 1
    
    # Create metrics
    metric1 = {
        'id': metric_id_counter,
        'companyId': company1['id'],
        'name': 'Carbon Intensity',
        'category': 'emissions',
        'value': 12.4,
        'unit': 'tCO2e/M$',
        'isAnonymized': False,
        'timestamp': datetime.datetime.now().isoformat()
    }
    metrics.append(metric1)
    metric_id_counter += 1
    
    metric2 = {
        'id': metric_id_counter,
        'companyId': company1['id'],
        'name': 'ESG Score',
        'category': 'governance',
        'value': 73.8,
        'unit': 'points',
        'isAnonymized': False,
        'timestamp': datetime.datetime.now().isoformat()
    }
    metrics.append(metric2)
    metric_id_counter += 1
    
    metric3 = {
        'id': metric_id_counter,
        'companyId': company1['id'],
        'name': 'Renewable Energy',
        'category': 'energy',
        'value': 38,
        'unit': '%',
        'isAnonymized': False,
        'timestamp': datetime.datetime.now().isoformat()
    }
    metrics.append(metric3)
    metric_id_counter += 1
    
    metric4 = {
        'id': metric_id_counter,
        'companyId': company2['id'],
        'name': 'Water Intensity',
        'category': 'water',
        'value': 2.3,
        'unit': 'kL/M$',
        'isAnonymized': False,
        'timestamp': datetime.datetime.now().isoformat()
    }
    metrics.append(metric4)
    metric_id_counter += 1
    
    # Create a pattern
    pattern = {
        'id': pattern_id_counter,
        'name': 'Renewable Energy Adoption Trend',
        'description': 'Companies investing in renewable energy show improved ESG scores',
        'category': 'energy',
        'detectionMethod': 'correlation-analysis',
        'confidence': 0.85,
        'dataPoints': [
            {'company': 'EcoTech Solutions', 'metric': 'Renewable Energy', 'value': 38},
            {'company': 'EcoTech Solutions', 'metric': 'ESG Score', 'value': 73.8}
        ],
        'aiExplanation': 'This pattern indicates a positive correlation between renewable energy adoption and ESG performance.',
        'createdAt': datetime.datetime.now().isoformat(),
        'updatedAt': datetime.datetime.now().isoformat()
    }
    patterns.append(pattern)
    pattern_id_counter += 1
    
    # Create a document
    document = {
        'id': document_id_counter,
        'companyId': company1['id'],
        'title': 'Sustainability Report 2024',
        'description': 'Annual sustainability disclosure with ESG metrics and targets',
        'fileUrl': '/uploads/sustainability-report-2024.pdf',
        'fileType': 'pdf',
        'contentVector': [],  # Would contain embedding vector in production
        'uploadedAt': datetime.datetime.now().isoformat()
    }
    documents.append(document)
    document_id_counter += 1
    
    # Create a story
    story = {
        'id': story_id_counter,
        'patternId': pattern['id'],
        'title': 'Renewable Energy Drives ESG Performance',
        'content': 'Companies that invest in renewable energy sources consistently show better ESG scores and lower carbon intensity. This analysis of EcoTech Solutions reveals a clear correlation between increased renewable energy adoption and higher ESG performance ratings. The data suggests that every 10% increase in renewable energy usage corresponds to approximately a 5-point improvement in overall ESG score. This trend is consistent with broader industry patterns where sustainability-focused operational changes deliver measurable governance benefits.',
        'visualizationType': 'line-chart',
        'visualizationData': {
            'labels': ['Q1', 'Q2', 'Q3', 'Q4'],
            'datasets': [
                {'label': 'Renewable Energy', 'data': [32, 35, 37, 38]},
                {'label': 'ESG Score', 'data': [68, 70, 72, 73.8]}
            ]
        },
        'createdAt': datetime.datetime.now().isoformat(),
        'updatedAt': datetime.datetime.now().isoformat()
    }
    stories.append(story)
    story_id_counter += 1

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'timestamp': datetime.datetime.now().isoformat()})

# Fund routes
@app.route('/api/funds', methods=['GET'])
def get_funds():
    return jsonify(funds)

@app.route('/api/funds/<int:fund_id>', methods=['GET'])
def get_fund(fund_id):
    fund = get_fund_by_id(fund_id)
    if not fund:
        return jsonify({'error': 'Fund not found'}), 404
    return jsonify(fund)

@app.route('/api/funds', methods=['POST'])
def create_fund():
    global fund_id_counter
    data = request.get_json()
    
    fund = {
        'id': fund_id_counter,
        'name': data.get('name'),
        'description': data.get('description'),
        'createdAt': datetime.datetime.now().isoformat(),
        'updatedAt': datetime.datetime.now().isoformat()
    }
    
    funds.append(fund)
    fund_id_counter += 1
    
    return jsonify(fund), 201

# Company routes
@app.route('/api/companies', methods=['GET'])
def get_companies():
    fund_id = request.args.get('fundId')
    if fund_id:
        result = [c for c in companies if c['fundId'] == int(fund_id)]
        return jsonify(result)
    return jsonify(companies)

@app.route('/api/companies/<int:company_id>', methods=['GET'])
def get_company(company_id):
    company = get_company_by_id(company_id)
    if not company:
        return jsonify({'error': 'Company not found'}), 404
    return jsonify(company)

@app.route('/api/companies', methods=['POST'])
def create_company():
    global company_id_counter
    data = request.get_json()
    
    company = {
        'id': company_id_counter,
        'fundId': data.get('fundId'),
        'name': data.get('name'),
        'sector': data.get('sector'),
        'description': data.get('description'),
        'isPublic': data.get('isPublic', False),
        'createdAt': datetime.datetime.now().isoformat(),
        'updatedAt': datetime.datetime.now().isoformat()
    }
    
    companies.append(company)
    company_id_counter += 1
    
    return jsonify(company), 201

# Metrics routes
@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    company_id = request.args.get('companyId')
    if company_id:
        result = [m for m in metrics if m['companyId'] == int(company_id)]
        return jsonify(result)
    return jsonify(metrics)

@app.route('/api/metrics/<int:metric_id>', methods=['GET'])
def get_metric(metric_id):
    metric = next((m for m in metrics if m['id'] == metric_id), None)
    if not metric:
        return jsonify({'error': 'Metric not found'}), 404
    return jsonify(metric)

@app.route('/api/metrics', methods=['POST'])
def create_metric():
    global metric_id_counter
    data = request.get_json()
    
    metric = {
        'id': metric_id_counter,
        'companyId': data.get('companyId'),
        'name': data.get('name'),
        'category': data.get('category'),
        'value': data.get('value'),
        'unit': data.get('unit'),
        'isAnonymized': data.get('isAnonymized', False),
        'timestamp': datetime.datetime.now().isoformat()
    }
    
    metrics.append(metric)
    metric_id_counter += 1
    
    return jsonify(metric), 201

# Pattern routes
@app.route('/api/patterns', methods=['GET'])
def get_patterns():
    return jsonify(patterns)

@app.route('/api/patterns/<int:pattern_id>', methods=['GET'])
def get_pattern(pattern_id):
    pattern = get_pattern_by_id(pattern_id)
    if not pattern:
        return jsonify({'error': 'Pattern not found'}), 404
    return jsonify(pattern)

@app.route('/api/patterns', methods=['POST'])
def create_pattern():
    global pattern_id_counter
    data = request.get_json()
    
    pattern = {
        'id': pattern_id_counter,
        'name': data.get('name'),
        'description': data.get('description'),
        'category': data.get('category'),
        'detectionMethod': data.get('detectionMethod'),
        'confidence': data.get('confidence'),
        'dataPoints': data.get('dataPoints', []),
        'aiExplanation': data.get('aiExplanation'),
        'createdAt': datetime.datetime.now().isoformat(),
        'updatedAt': datetime.datetime.now().isoformat()
    }
    
    patterns.append(pattern)
    pattern_id_counter += 1
    
    return jsonify(pattern), 201

# Document routes
@app.route('/api/documents', methods=['GET'])
def get_documents():
    company_id = request.args.get('companyId')
    if company_id:
        result = [d for d in documents if d['companyId'] == int(company_id)]
        return jsonify(result)
    return jsonify(documents)

@app.route('/api/documents/<int:document_id>', methods=['GET'])
def get_document(document_id):
    document = next((d for d in documents if d['id'] == document_id), None)
    if not document:
        return jsonify({'error': 'Document not found'}), 404
    return jsonify(document)

@app.route('/api/documents', methods=['POST'])
def create_document():
    global document_id_counter
    data = request.get_json()
    
    document = {
        'id': document_id_counter,
        'companyId': data.get('companyId'),
        'title': data.get('title'),
        'description': data.get('description'),
        'fileUrl': data.get('fileUrl'),
        'fileType': data.get('fileType'),
        'contentVector': data.get('contentVector', []),
        'uploadedAt': datetime.datetime.now().isoformat()
    }
    
    documents.append(document)
    document_id_counter += 1
    
    return jsonify(document), 201

# Story routes
@app.route('/api/stories', methods=['GET'])
def get_stories():
    pattern_id = request.args.get('patternId')
    if pattern_id:
        result = [s for s in stories if s['patternId'] == int(pattern_id)]
        return jsonify(result)
    return jsonify(stories)

@app.route('/api/stories/<int:story_id>', methods=['GET'])
def get_story(story_id):
    story = next((s for s in stories if s['id'] == story_id), None)
    if not story:
        return jsonify({'error': 'Story not found'}), 404
    return jsonify(story)

@app.route('/api/stories', methods=['POST'])
def create_story():
    global story_id_counter
    data = request.get_json()
    
    story = {
        'id': story_id_counter,
        'patternId': data.get('patternId'),
        'title': data.get('title'),
        'content': data.get('content'),
        'visualizationType': data.get('visualizationType', 'line-chart'),
        'visualizationData': data.get('visualizationData'),
        'createdAt': datetime.datetime.now().isoformat(),
        'updatedAt': datetime.datetime.now().isoformat()
    }
    
    stories.append(story)
    story_id_counter += 1
    
    return jsonify(story), 201

# AI-related routes
@app.route('/api/ai/explain-pattern', methods=['POST'])
def explain_pattern():
    data = request.get_json()
    pattern_id = data.get('patternId')
    data_points = data.get('dataPoints', [])
    
    # This would integrate with Google Gemini API in production
    # For now, return a placeholder explanation
    explanation = f"This sustainability pattern shows a correlation between {len(data_points) if data_points else 'several'} factors. The data suggests an emerging trend that could impact future sustainability outcomes."
    
    return jsonify({'explanation': explanation})

# Serve frontend assets (for production)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path == '':
        return send_from_directory('frontend', 'index.html')
    else:
        try:
            return send_from_directory('frontend', path)
        except Exception:
            return send_from_directory('frontend', 'index.html')

if __name__ == '__main__':
    init_sample_data()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)