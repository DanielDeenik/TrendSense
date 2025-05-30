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

# Define navigation items - aligned with registered blueprints in app.py
NAVIGATION_ITEMS = [
    {
        "name": "Home",
        "url": "/",
        "icon": "home",
        "roles": ["admin", "user", "vc"],
        "description": "TrendSense Dashboard"
    },
    {
        "name": "VC Lens",
        "url": "/vc-lens",
        "icon": "chart-line",
        "roles": ["admin", "user", "vc"],
        "description": "Private Equity Analytics"
    },
    {
        "name": "TrendSense",
        "url": "/trendsense",
        "icon": "brain",
        "roles": ["admin", "user", "vc"],
        "description": "AI-Powered Trend Analysis"
    },
    {
        "name": "TrendRadar",
        "url": "/trendradar",
        "icon": "radar",
        "roles": ["admin", "user", "vc"],
        "description": "Real-time Trend Monitoring"
    },
    {
        "name": "Strategy",
        "url": "/strategy",
        "icon": "chess",
        "roles": ["admin", "user", "vc"],
        "description": "Strategic Planning Hub"
    },
    {
        "name": "Data Management",
        "url": "/data-management",
        "icon": "database",
        "roles": ["admin", "user"],
        "description": "Data Storage & Retrieval"
    },
    {
        "name": "Lookthrough",
        "url": "/lookthrough",
        "icon": "search",
        "roles": ["admin", "user", "vc"],
        "description": "Portfolio Analysis"
    },
    {
        "name": "Graph Analytics",
        "url": "/graph-analytics",
        "icon": "project-diagram",
        "roles": ["admin", "user", "vc"],
        "description": "Network Analysis"
    },
    {
        "name": "Lifecycle",
        "url": "/lifecycle",
        "icon": "recycle",
        "roles": ["admin", "user", "vc"],
        "description": "Investment Lifecycle"
    },
    {
        "name": "Copilot",
        "url": "/copilot",
        "icon": "robot",
        "roles": ["admin", "user", "vc"],
        "description": "AI Assistant"
    },
    {
        "name": "API",
        "url": "/api",
        "icon": "code",
        "roles": ["admin"],
        "description": "API Documentation"
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
