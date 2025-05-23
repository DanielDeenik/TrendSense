"""
Context processors for TrendSense application.

These functions provide data that is available to all templates.
"""

import logging

# Configure logging
logger = logging.getLogger(__name__)

def navigation_processor():
    """
    Provide navigation data to all templates.
    
    Returns:
        dict: Dictionary containing navigation data
    """
    try:
        navigation_items = [
            {
                'name': 'Home',
                'url': '/',
                'icon': 'fas fa-home',
                'description': 'TrendSense Dashboard'
            },
            {
                'name': 'VC Lens',
                'url': '/vc-lens/',
                'icon': 'fas fa-chart-line',
                'description': 'Private Equity Analytics'
            },
            {
                'name': 'TrendSense',
                'url': '/trendsense/',
                'icon': 'fas fa-brain',
                'description': 'AI-Powered Trend Analysis'
            },
            {
                'name': 'TrendRadar',
                'url': '/trendradar/',
                'icon': 'fas fa-radar',
                'description': 'Real-time Trend Monitoring'
            },
            {
                'name': 'Strategy',
                'url': '/strategy/',
                'icon': 'fas fa-chess',
                'description': 'Strategic Planning Hub'
            },
            {
                'name': 'Data Management',
                'url': '/data-management/',
                'icon': 'fas fa-database',
                'description': 'Data Storage & Retrieval'
            },
            {
                'name': 'Lookthrough',
                'url': '/lookthrough/',
                'icon': 'fas fa-search',
                'description': 'Portfolio Analysis'
            },
            {
                'name': 'Graph Analytics',
                'url': '/graph-analytics/',
                'icon': 'fas fa-project-diagram',
                'description': 'Network Analysis'
            },
            {
                'name': 'Lifecycle',
                'url': '/lifecycle/',
                'icon': 'fas fa-recycle',
                'description': 'Investment Lifecycle'
            },
            {
                'name': 'Copilot',
                'url': '/copilot/',
                'icon': 'fas fa-robot',
                'description': 'AI Assistant'
            }
        ]
        
        return {
            'navigation': navigation_items,
            'app_name': 'TrendSense',
            'app_version': '1.0.0'
        }
        
    except Exception as e:
        logger.error(f"Error in navigation processor: {str(e)}")
        return {
            'navigation': [],
            'app_name': 'TrendSense',
            'app_version': '1.0.0'
        }

def user_processor():
    """
    Provide user data to all templates.
    
    Returns:
        dict: Dictionary containing user data
    """
    try:
        # In a real application, this would get user data from session/database
        return {
            'user': {
                'name': 'Demo User',
                'role': 'Analyst',
                'authenticated': True
            }
        }
    except Exception as e:
        logger.error(f"Error in user processor: {str(e)}")
        return {
            'user': {
                'name': 'Guest',
                'role': 'Visitor',
                'authenticated': False
            }
        }

def theme_processor():
    """
    Provide theme data to all templates.
    
    Returns:
        dict: Dictionary containing theme data
    """
    try:
        return {
            'theme': {
                'name': 'dark',
                'primary_color': '#1a1a1a',
                'secondary_color': '#2d2d2d',
                'accent_color': '#007bff',
                'text_color': '#ffffff'
            }
        }
    except Exception as e:
        logger.error(f"Error in theme processor: {str(e)}")
        return {
            'theme': {
                'name': 'light',
                'primary_color': '#ffffff',
                'secondary_color': '#f8f9fa',
                'accent_color': '#007bff',
                'text_color': '#000000'
            }
        }

def debug_processor():
    """
    Provide debug information to templates (only in debug mode).
    
    Returns:
        dict: Dictionary containing debug data
    """
    try:
        import os
        debug_mode = os.environ.get('FLASK_ENV') == 'development'
        
        if debug_mode:
            return {
                'debug': {
                    'enabled': True,
                    'environment': os.environ.get('FLASK_ENV', 'production'),
                    'database_adapter': os.environ.get('DATABASE_ADAPTER', 'unknown')
                }
            }
        else:
            return {'debug': {'enabled': False}}
            
    except Exception as e:
        logger.error(f"Error in debug processor: {str(e)}")
        return {'debug': {'enabled': False}}

# Main context processor function that combines all processors
def get_global_context():
    """
    Get all global context data for templates.
    
    Returns:
        dict: Combined context data from all processors
    """
    try:
        context = {}
        
        # Combine all context processors
        context.update(navigation_processor())
        context.update(user_processor())
        context.update(theme_processor())
        context.update(debug_processor())
        
        return context
        
    except Exception as e:
        logger.error(f"Error getting global context: {str(e)}")
        return {
            'navigation': [],
            'app_name': 'TrendSense',
            'app_version': '1.0.0',
            'user': {'name': 'Guest', 'authenticated': False},
            'theme': {'name': 'light'},
            'debug': {'enabled': False}
        }
