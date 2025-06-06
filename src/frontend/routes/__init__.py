"""
Routes package for LensIQ application.

This package contains all route definitions for the streamlined application.
"""

# Import main route modules
try:
    from .lensiq import lensiq_bp
except ImportError:
    lensiq_bp = None

try:
    from .strategy_direct_flask import bp as strategy_bp
except ImportError:
    strategy_bp = None

try:
    from .trendradar import trendradar_bp
except ImportError:
    trendradar_bp = None

try:
    from .api import api_bp
except ImportError:
    api_bp = None

# Export main blueprints
__all__ = [
    'lensiq_bp',
    'strategy_bp',
    'trendradar_bp',
    'api_bp'
]
