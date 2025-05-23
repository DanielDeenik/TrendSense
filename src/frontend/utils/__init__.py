"""
Utils module for SustainaTrend™

This module provides utility functions for the application.
"""

from typing import Dict, Any
from datetime import datetime
from flask import request, current_app, Blueprint
from .navigation_config import get_context_for_template, get_navigation_items

def get_context_for_template() -> Dict[str, Any]:
    """
    Get common context variables for templates.
    
    Returns:
        Dict[str, Any]: Common template context
    """
    return {
        'request': request,
        'current_route': request.endpoint.split('.')[0] if request.endpoint else None,
        'timestamp': datetime.now().isoformat(),
        'app_name': current_app.config.get('APP_NAME', 'SustainaTrend™'),
        'version': current_app.config.get('VERSION', '1.0.0'),
        'environment': current_app.config.get('ENVIRONMENT', 'development'),
        'debug': current_app.debug,
        'user': {
            'is_authenticated': True,  # TODO: Replace with actual auth check
            'name': 'Demo User',  # TODO: Replace with actual user data
            'role': 'admin'  # TODO: Replace with actual user role
        },
        'navigation': {
            'current_section': request.endpoint.split('.')[0] if request.endpoint else None,
            'sections': [
                {'name': 'Dashboard', 'url': '/', 'icon': 'home'},
                {'name': 'Analytics', 'url': '/analytics', 'icon': 'chart-bar'},
                {'name': 'Companies', 'url': '/companies', 'icon': 'building'},
                {'name': 'Trends', 'url': '/trends', 'icon': 'trending-up'},
                {'name': 'Settings', 'url': '/settings', 'icon': 'cog'}
            ]
        }
    }

# Create a blueprint for utility functions
utils_bp = Blueprint('utils', __name__)

# Register template filters
@utils_bp.app_template_filter('format_number')
def format_number(value):
    """
    Format a number with commas as thousands separators.
    
    Args:
        value: The number to format
        
    Returns:
        str: Formatted number
    """
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return value

@utils_bp.app_template_filter('format_date')
def format_date(value):
    """
    Format a date string.
    
    Args:
        value: The date string to format
        
    Returns:
        str: Formatted date
    """
    try:
        if isinstance(value, str):
            dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        else:
            dt = value
        return dt.strftime('%B %d, %Y')
    except (ValueError, TypeError):
        return value

@utils_bp.app_template_filter('format_currency')
def format_currency(value):
    """
    Format a number as currency.
    
    Args:
        value: The number to format
        
    Returns:
        str: Formatted currency
    """
    try:
        return f"${int(value):,}"
    except (ValueError, TypeError):
        return value
