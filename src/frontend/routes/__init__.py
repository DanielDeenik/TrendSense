"""
Routes package for LensIQ Narrative Builder.

This package contains core route definitions for the narrative builder functionality.
"""

# Import core route modules
try:
    from .lensiq import lensiq_bp
except ImportError:
    lensiq_bp = None

try:
    from .narrative_builder_routes import narrative_builder_bp
except ImportError:
    narrative_builder_bp = None

try:
    from .api import api_bp
except ImportError:
    api_bp = None

# Export core blueprints
__all__ = [
    'lensiq_bp',
    'narrative_builder_bp',
    'api_bp'
]
