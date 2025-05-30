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
        # Import navigation items from navigation_config.py for consistency
        from .navigation_config import NAVIGATION_ITEMS

        # Format navigation items for templates
        navigation_items = []
        for item in NAVIGATION_ITEMS:
            nav_item = {
                'name': item['name'],
                'url': item['url'],
                'icon': f"fas fa-{item['icon']}",
                'description': item.get('description', ''),
                'roles': item.get('roles', [])
            }
            navigation_items.append(nav_item)

        # Create categories for the sidebar
        categories = [
            {
                'id': 'main',
                'name': 'Main Navigation'
            },
            {
                'id': 'analytics',
                'name': 'Analytics'
            },
            {
                'id': 'management',
                'name': 'Management'
            },
            {
                'id': 'tools',
                'name': 'Tools'
            }
        ]

        # Assign categories to items
        for item in navigation_items:
            if item['name'] in ['Home', 'VC Lens', 'TrendSense', 'TrendRadar']:
                item['category'] = 'main'
            elif item['name'] in ['Graph Analytics', 'Lookthrough', 'Lifecycle']:
                item['category'] = 'analytics'
            elif item['name'] in ['Data Management', 'Strategy']:
                item['category'] = 'management'
            else:
                item['category'] = 'tools'

        return {
            'navigation': {
                'items': navigation_items,
                'categories': categories,
                'structure': {
                    'main': {'items': [i for i in navigation_items if i.get('category') == 'main']},
                    'analytics': {'items': [i for i in navigation_items if i.get('category') == 'analytics']},
                    'management': {'items': [i for i in navigation_items if i.get('category') == 'management']},
                    'tools': {'items': [i for i in navigation_items if i.get('category') == 'tools']}
                }
            },
            'app_name': 'TrendSense',
            'app_version': '1.0.0'
        }

    except Exception as e:
        logger.error(f"Error in navigation processor: {str(e)}")
        return {
            'navigation': {
                'items': [],
                'categories': [],
                'structure': {}
            },
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
