"""
Routes package for SustainaTrend application.

This package contains all route definitions for the application.
"""

# Import route modules
from .graph_analytics import graph_analytics_bp

# Export blueprints
__all__ = [
    'graph_analytics_bp',
]
