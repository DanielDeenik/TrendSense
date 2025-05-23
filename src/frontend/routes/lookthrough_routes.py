"""
Look Through Engine Routes

This module provides routes for the Look Through Engine, which propagates metrics through
the Fund → Company → Project structure.
"""

import logging
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash

# Import Look Through Engine components
from src.lookthrough.entity_traversal import EntityTraversal
from src.lookthrough.metrics_propagator import MetricsProgagator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
lookthrough_bp = Blueprint('lookthrough', __name__, url_prefix='/lookthrough')

# Initialize components
entity_traversal = EntityTraversal()
metrics_propagator = MetricsProgagator()

@lookthrough_bp.route('/')
def index():
    """Look Through Engine dashboard."""
    try:
        # Ensure database connection
        if not entity_traversal.db_adapter.is_connected():
            entity_traversal.db_adapter.connect()

        # Initialize collections if they don't exist
        entity_traversal.db_adapter.initialize_collections(['funds', 'companies', 'projects'])

        # Get funds
        funds = entity_traversal.db_adapter.find('funds')

        # Get entity counts
        fund_count = len(funds)
        company_count = len(entity_traversal.db_adapter.find('companies'))
        project_count = len(entity_traversal.db_adapter.find('projects'))

        return render_template(
            'lookthrough/dashboard.html',
            active_nav='lookthrough',
            funds=funds,
            fund_count=fund_count,
            company_count=company_count,
            project_count=project_count
        )

    except Exception as e:
        logger.error(f"Error rendering Look Through Engine dashboard: {str(e)}")
        return render_template(
            'fin_errors/fin_500.html',
            active_nav='lookthrough',
            error_message=f"Error rendering Look Through Engine dashboard: {str(e)}"
        )

@lookthrough_bp.route('/fund/<fund_id>')
def view_fund(fund_id):
    """View a fund's hierarchy."""
    try:
        # Get fund hierarchy
        hierarchy = entity_traversal.get_fund_hierarchy(fund_id)

        if not hierarchy.get('success', False):
            flash(f"Error retrieving fund hierarchy: {hierarchy.get('error', 'Unknown error')}", 'error')
            return redirect(url_for('lookthrough.index'))

        return render_template(
            'lookthrough/fund_view.html',
            active_nav='lookthrough',
            fund=hierarchy.get('fund'),
            companies=hierarchy.get('companies', []),
            projects=hierarchy.get('projects', [])
        )

    except Exception as e:
        logger.error(f"Error viewing fund hierarchy: {str(e)}")
        return render_template(
            'fin_errors/fin_500.html',
            active_nav='lookthrough',
            error_message=f"Error viewing fund hierarchy: {str(e)}"
        )

@lookthrough_bp.route('/company/<company_id>')
def view_company(company_id):
    """View a company's hierarchy."""
    try:
        # Get company hierarchy
        hierarchy = entity_traversal.get_company_hierarchy(company_id)

        if not hierarchy.get('success', False):
            flash(f"Error retrieving company hierarchy: {hierarchy.get('error', 'Unknown error')}", 'error')
            return redirect(url_for('lookthrough.index'))

        return render_template(
            'lookthrough/company_view.html',
            active_nav='lookthrough',
            company=hierarchy.get('company'),
            projects=hierarchy.get('projects', []),
            funds=hierarchy.get('funds', [])
        )

    except Exception as e:
        logger.error(f"Error viewing company hierarchy: {str(e)}")
        return render_template(
            'fin_errors/fin_500.html',
            active_nav='lookthrough',
            error_message=f"Error viewing company hierarchy: {str(e)}"
        )

@lookthrough_bp.route('/project/<project_id>')
def view_project(project_id):
    """View a project's hierarchy."""
    try:
        # Get project hierarchy
        hierarchy = entity_traversal.get_project_hierarchy(project_id)

        if not hierarchy.get('success', False):
            flash(f"Error retrieving project hierarchy: {hierarchy.get('error', 'Unknown error')}", 'error')
            return redirect(url_for('lookthrough.index'))

        return render_template(
            'lookthrough/project_view.html',
            active_nav='lookthrough',
            project=hierarchy.get('project'),
            company=hierarchy.get('company'),
            funds=hierarchy.get('funds', [])
        )

    except Exception as e:
        logger.error(f"Error viewing project hierarchy: {str(e)}")
        return render_template(
            'fin_errors/fin_500.html',
            active_nav='lookthrough',
            error_message=f"Error viewing project hierarchy: {str(e)}"
        )

@lookthrough_bp.route('/propagate', methods=['POST'])
def propagate_metrics():
    """Propagate metrics through the Fund → Company → Project structure."""
    try:
        # Get fund ID from form
        fund_id = request.form.get('fund_id')

        # Propagate metrics
        result = metrics_propagator.propagate_metrics(fund_id)

        if result.get('success', False):
            flash(f"Successfully propagated metrics for {result.get('funds_processed', 0)} funds", 'success')
        else:
            flash(f"Error propagating metrics: {result.get('error', 'Unknown error')}", 'error')

        # Redirect to the appropriate page
        if fund_id:
            return redirect(url_for('lookthrough.view_fund', fund_id=fund_id))
        else:
            return redirect(url_for('lookthrough.index'))

    except Exception as e:
        logger.error(f"Error propagating metrics: {str(e)}")
        flash(f"Error propagating metrics: {str(e)}", 'error')
        return redirect(url_for('lookthrough.index'))

@lookthrough_bp.route('/api/funds')
def api_get_funds():
    """API endpoint for getting all funds."""
    try:
        # Get funds
        funds = entity_traversal.db_adapter.find('funds')

        # Format funds
        formatted_funds = [
            {
                "fund_id": fund.get("_id"),
                "fund_name": fund.get("name", "Unknown Fund"),
                "aum": fund.get("aum", 0),
                "currency": fund.get("currency", "USD"),
                "company_count": len(fund.get("portfolio_companies", [])),
                "metrics": fund.get("sustainability_metrics", {})
            }
            for fund in funds
        ]

        return jsonify({
            "success": True,
            "funds": formatted_funds,
            "count": len(formatted_funds)
        })

    except Exception as e:
        logger.error(f"Error getting funds: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@lookthrough_bp.route('/api/companies')
def api_get_companies():
    """API endpoint for getting all companies."""
    try:
        # Get filter parameters
        sector = request.args.get('sector')

        # Get companies
        result = entity_traversal.get_all_companies(sector)

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error getting companies: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@lookthrough_bp.route('/api/projects')
def api_get_projects():
    """API endpoint for getting all projects."""
    try:
        # Get filter parameters
        status = request.args.get('status')

        # Get projects
        result = entity_traversal.get_all_projects(status)

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error getting projects: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@lookthrough_bp.route('/api/fund/<fund_id>')
def api_get_fund(fund_id):
    """API endpoint for getting a fund's hierarchy."""
    try:
        # Get fund hierarchy
        hierarchy = entity_traversal.get_fund_hierarchy(fund_id)

        return jsonify(hierarchy)

    except Exception as e:
        logger.error(f"Error getting fund hierarchy: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@lookthrough_bp.route('/api/company/<company_id>')
def api_get_company(company_id):
    """API endpoint for getting a company's hierarchy."""
    try:
        # Get company hierarchy
        hierarchy = entity_traversal.get_company_hierarchy(company_id)

        return jsonify(hierarchy)

    except Exception as e:
        logger.error(f"Error getting company hierarchy: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@lookthrough_bp.route('/api/project/<project_id>')
def api_get_project(project_id):
    """API endpoint for getting a project's hierarchy."""
    try:
        # Get project hierarchy
        hierarchy = entity_traversal.get_project_hierarchy(project_id)

        return jsonify(hierarchy)

    except Exception as e:
        logger.error(f"Error getting project hierarchy: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@lookthrough_bp.route('/api/propagate', methods=['POST'])
def api_propagate_metrics():
    """API endpoint for propagating metrics."""
    try:
        # Get fund ID from JSON data
        data = request.json or {}
        fund_id = data.get('fund_id')

        # Propagate metrics
        result = metrics_propagator.propagate_metrics(fund_id)

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error propagating metrics: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
