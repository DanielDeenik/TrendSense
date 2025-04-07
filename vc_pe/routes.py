"""
VC/PE Route Configuration for SustainaTrend™
This module defines the route structure for VC/PE specific features.
"""

from flask import Blueprint, render_template, jsonify
from .data import generate_portfolio_metrics, generate_company_benchmarks, generate_sustainability_insights

# Create blueprint for VC/PE routes
vc_pe_bp = Blueprint('vc_pe', __name__, 
                    template_folder='templates',
                    static_folder='static')

# Core VC/PE Pages
@vc_pe_bp.route('/dashboard')
def vc_pe_dashboard():
    """Main VC/PE sustainability dashboard"""
    return render_template('vc_pe/dashboard.html')

@vc_pe_bp.route('/portfolio')
def portfolio_analysis():
    """Portfolio company sustainability analysis"""
    return render_template('vc_pe/portfolio.html',
                         metrics=generate_portfolio_metrics(),
                         insights=generate_sustainability_insights())

@vc_pe_bp.route('/pipeline')
def investment_pipeline():
    """Sustainability-focused deal pipeline"""
    return render_template('vc_pe/pipeline.html')

# API Endpoints
@vc_pe_bp.route('/api/metrics')
def vc_pe_metrics():
    """Get VC/PE specific sustainability metrics"""
    return jsonify(generate_portfolio_metrics())

@vc_pe_bp.route('/api/companies')
def vc_pe_companies():
    """Get portfolio company sustainability data"""
    return jsonify(generate_company_benchmarks())

@vc_pe_bp.route('/api/insights')
def vc_pe_insights():
    """Get VC/PE specific sustainability insights"""
    return jsonify(generate_sustainability_insights())

# Specialized Tools
@vc_pe_bp.route('/pdf-analyzer')
def vc_pe_pdf_analyzer():
    """VC/PE specific document analysis tool"""
    return render_template('vc_pe/pdf_analyzer.html')

@vc_pe_bp.route('/co-pilot')
def vc_pe_copilot():
    """VC/PE specific AI assistant"""
    return render_template('vc_pe/copilot.html')

# Debug Routes
@vc_pe_bp.route('/debug/vc-pe')
def debug_vc_pe():
    """Debug route for VC/PE features"""
    return jsonify({
        "status": "ok",
        "routes": [
            "/dashboard",
            "/portfolio",
            "/pipeline",
            "/api/metrics",
            "/api/companies",
            "/api/insights"
        ]
    }) 