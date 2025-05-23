"""
Navigation configuration for SustainaTrend™

This module provides navigation configuration for the application.
"""

from typing import Dict, List, Any
from datetime import datetime
from .data_providers import (
    get_metrics,
    get_trends,
    get_stories,
    get_portfolio_companies,
    get_market_trends,
    get_sustainability_scores,
    get_properties,
    get_market_data,
    get_benchmarks,
    get_monetization_strategies
)
from .strategy_simulation import get_strategy_frameworks

# Define navigation items
NAVIGATION_ITEMS = [
    {
        "name": "Dashboard",
        "url": "/",
        "icon": "dashboard",
        "roles": ["admin", "user", "vc"]
    },
    {
        "name": "Analytics",
        "url": "/analytics",
        "icon": "analytics",
        "roles": ["admin", "user", "vc"]
    },
    {
        "name": "Trends",
        "url": "/trends",
        "icon": "trending_up",
        "roles": ["admin", "user", "vc"]
    },
    {
        "name": "Graph",
        "url": "/graph",
        "icon": "share",
        "roles": ["admin", "user", "vc"]
    },
    {
        "name": "Companies",
        "url": "/companies",
        "icon": "business",
        "roles": ["admin", "user", "vc"]
    },
    {
        "name": "Models",
        "url": "/models",
        "icon": "model_training",
        "roles": ["admin", "user"]
    },
    {
        "name": "Insights",
        "url": "/insights",
        "icon": "lightbulb",
        "roles": ["admin", "user", "vc"]
    },
    {
        "name": "Profile",
        "url": "/profile",
        "icon": "person",
        "roles": ["admin", "user", "vc"]
    },
    {
        "name": "Settings",
        "url": "/settings",
        "icon": "settings",
        "roles": ["admin", "user", "vc"]
    },
    {
        "name": "Strategy",
        "url": "/strategy",
        "icon": "strategy",
        "roles": ["user", "admin"]
    },
    {
        "name": "Real Estate",
        "url": "/real-estate",
        "icon": "home",
        "roles": ["user", "admin"]
    }
]

def get_navigation_items(roles: List[str] = None) -> List[Dict[str, Any]]:
    """
    Get navigation items for a specific role.

    Args:
        role: User role

    Returns:
        list: Navigation items for the role
    """
    if not roles:
        return NAVIGATION_ITEMS

    return [item for item in NAVIGATION_ITEMS if any(role in item.get("roles", []) for role in roles)]

def get_context_for_template(template_name: str = None) -> Dict[str, Any]:
    """
    Get context data for a specific template.

    Args:
        template_name (str, optional): Name of the template. Defaults to None.

    Returns:
        dict: Context data for the template
    """
    context = {
        'app_name': 'SustainaTrend™',
        'version': '1.0.0',
        'year': datetime.now().year,
        'theme': 'light',  # Default theme
        'user': {
            'name': 'Demo User',
            'role': 'admin'
        }
    }

    # Add template-specific context
    if template_name == 'dashboard':
        context.update({
            'metrics': get_metrics(),
            'trends': get_trends(),
            'stories': get_stories()
        })
    elif template_name == 'vc_dashboard':
        context.update({
            'portfolio_companies': get_portfolio_companies(),
            'market_trends': get_market_trends(),
            'sustainability_scores': get_sustainability_scores()
        })
    elif template_name == 'realestate':
        context.update({
            'properties': get_properties(),
            'market_data': get_market_data(),
            'benchmarks': get_benchmarks()
        })
    elif template_name == 'analytics':
        context.update({
            'metrics': get_metrics(),
            'monetization_strategies': get_monetization_strategies()
        })
    elif template_name == 'strategy':
        context.update({
            'frameworks': get_strategy_frameworks(),
            'current_metrics': get_metrics()
        })
    elif template_name == 'graph' or template_name == 'graph_network' or template_name == 'graph_relationships':
        context.update({
            'page_title': 'Sustainability Graph',
            'active_nav': 'graph'
        })

    return context

def get_analytics_metrics():
    """
    Get analytics-specific metrics.

    Returns:
        dict: Analytics metrics
    """
    metrics = get_metrics()
    return {
        'total_investments': 1250000000,  # $1.25B
        'roi': 18.5,
        'esg_impact': 82.5,
        'risk_score': 65.2
    }
