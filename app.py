"""
LensIQ™ Intelligence Platform

A comprehensive platform for sustainability trend analysis and investment intelligence.
"""

import os
import sys
import logging
from flask import Flask, render_template, jsonify

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for more detailed logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Set Flask's logger to DEBUG as well
logging.getLogger('flask').setLevel(logging.DEBUG)
logging.getLogger('werkzeug').setLevel(logging.DEBUG)

# Import blueprints with error handling
try:
    from src.frontend.routes.api import api_bp
except ImportError:
    # Create a minimal API blueprint if import fails
    from flask import Blueprint, jsonify
    api_bp = Blueprint('api', __name__)

    @api_bp.route('/health')
    def health_check():
        return jsonify({'status': 'ok', 'message': 'Fallback API'})

try:
    from src.frontend.routes.strategy_direct_flask import bp as strategy_bp
except ImportError:
    from flask import Blueprint
    strategy_bp = Blueprint('strategy', __name__)

try:
    from src.frontend.routes.data_management_routes import data_management_bp
except ImportError:
    from flask import Blueprint
    data_management_bp = Blueprint('data_management', __name__)

try:
    from src.frontend.routes.lookthrough_routes import lookthrough_bp
except ImportError:
    from flask import Blueprint
    lookthrough_bp = Blueprint('lookthrough', __name__)

try:
    from src.frontend.routes.graph_analytics import graph_analytics_bp
except ImportError:
    from flask import Blueprint
    graph_analytics_bp = Blueprint('graph_analytics', __name__)

try:
    from src.frontend.routes.vc_lens import vc_lens_bp
except ImportError:
    from flask import Blueprint
    vc_lens_bp = Blueprint('vc_lens', __name__)

try:
    from src.frontend.routes.lensiq import lensiq_bp
except ImportError:
    from flask import Blueprint
    lensiq_bp = Blueprint('lensiq', __name__)

try:
    from src.frontend.routes.trendradar import trendradar_bp
except ImportError:
    from flask import Blueprint
    trendradar_bp = Blueprint('trendradar', __name__)

try:
    from src.frontend.routes.lifecycle import lifecycle_bp
except ImportError:
    from flask import Blueprint
    lifecycle_bp = Blueprint('lifecycle', __name__)

try:
    from src.frontend.routes.copilot import copilot_bp
except ImportError:
    from flask import Blueprint
    copilot_bp = Blueprint('copilot', __name__)

# Import context processors with error handling
try:
    from src.frontend.utils.context_processors import navigation_processor
except ImportError:
    # Create a minimal navigation processor if import fails
    def navigation_processor():
        return {
            'navigation': [
                {'name': 'Home', 'url': '/', 'icon': 'fas fa-home'},
                {'name': 'VC Lens', 'url': '/vc-lens/', 'icon': 'fas fa-chart-line'},
                {'name': 'LensIQ', 'url': '/lensiq/', 'icon': 'fas fa-brain'},
                {'name': 'TrendRadar', 'url': '/trendradar/', 'icon': 'fas fa-radar'},
                {'name': 'Strategy', 'url': '/strategy/', 'icon': 'fas fa-chess'},
                {'name': 'Data Management', 'url': '/data-management/', 'icon': 'fas fa-database'},
                {'name': 'Lookthrough', 'url': '/lookthrough/', 'icon': 'fas fa-search'},
                {'name': 'Graph Analytics', 'url': '/graph-analytics/', 'icon': 'fas fa-project-diagram'},
                {'name': 'Lifecycle', 'url': '/lifecycle/', 'icon': 'fas fa-recycle'},
                {'name': 'Copilot', 'url': '/copilot/', 'icon': 'fas fa-robot'}
            ]
        }

def create_app():
    """Create and configure the Flask application."""
    # Get the absolute path to the templates and static directories
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src', 'frontend', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src', 'frontend', 'static'))

    logger.info(f"Template directory: {template_dir}")
    logger.info(f"Static directory: {static_dir}")

    # Initialize Flask app with custom template and static folders
    app = Flask(__name__,
                template_folder=template_dir,
                static_folder=static_dir)

    # Configure app
    app.secret_key = os.getenv('SECRET_KEY', 'lensiq-secret-key')
    app.config['DEBUG'] = os.getenv('DEBUG', 'True').lower() == 'true'

    return app

# Initialize Flask app
app = create_app()

# Register context processor
app.context_processor(navigation_processor)

# Main routes
@app.route('/')
def index():
    """Home page."""
    try:
        logger.info("Rendering home page")
        # The navigation_processor is already registered as a context processor,
        # so we don't need to pass it explicitly to the template
        return render_template('fin_home.html', active_nav='home')
    except Exception as e:
        logger.error(f"Error rendering home page: {str(e)}")
        try:
            # Try to use the simple error page that doesn't depend on navigation
            return render_template('fin_errors/fin_error_simple.html',
                                  error_code=500,
                                  error_message=f"Error loading home page: {str(e)}"), 500
        except Exception as inner_e:
            logger.error(f"Error rendering error page: {str(inner_e)}")
            # Last resort fallback
            return f"<h1>Error 500</h1><p>Application error: {str(e)}</p><p>Error page error: {str(inner_e)}</p>", 500

# API health check
@app.route('/api/health')
def health_check():
    """API health check."""
    return jsonify({
        'status': 'ok',
        'version': '1.0.0',
        'environment': os.getenv('FLASK_ENV', 'development')
    })

# Debug route for navigation
@app.route('/debug/navigation')
def debug_navigation():
    """Debug route for navigation."""
    try:
        # Get navigation data
        nav_data = navigation_processor()

        # Return as JSON
        return jsonify({
            'status': 'ok',
            'navigation': nav_data['navigation']
        })
    except Exception as e:
        logger.error(f"Error in debug navigation: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

# Register blueprints with standardized URL prefixes (no trailing slashes)
blueprints_to_register = [
    (api_bp, '/api', 'API'),
    (strategy_bp, '/strategy', 'Strategy'),
    (data_management_bp, '/data-management', 'Data Management'),
    (lookthrough_bp, '/lookthrough', 'Lookthrough'),
    (graph_analytics_bp, '/graph-analytics', 'Graph Analytics'),
    (vc_lens_bp, '/vc-lens', 'VC Lens'),
    (lensiq_bp, '/lensiq', 'LensIQ'),
    (trendradar_bp, '/trendradar', 'TrendRadar'),
    (lifecycle_bp, '/lifecycle', 'Lifecycle'),
    (copilot_bp, '/copilot', 'Copilot')
]

for blueprint, url_prefix, name in blueprints_to_register:
    try:
        # Check if blueprint already has a url_prefix defined
        if hasattr(blueprint, 'url_prefix') and blueprint.url_prefix:
            app.register_blueprint(blueprint)
            logger.info(f"Registered {name} blueprint with existing prefix: {blueprint.url_prefix}")
        else:
            app.register_blueprint(blueprint, url_prefix=url_prefix)
            logger.info(f"Registered {name} blueprint with prefix: {url_prefix}")
    except Exception as e:
        logger.error(f"Failed to register {name} blueprint: {e}")
        # Create a minimal fallback blueprint
        from flask import Blueprint, jsonify
        fallback_bp = Blueprint(f'fallback_{blueprint.name}', __name__)

        @fallback_bp.route('/')
        def fallback_index():
            return jsonify({'status': 'fallback', 'message': f'{name} module not available'})

        try:
            app.register_blueprint(fallback_bp, url_prefix=url_prefix)
            logger.info(f"Registered fallback {name} blueprint")
        except Exception as fallback_error:
            logger.error(f"Failed to register fallback {name} blueprint: {fallback_error}")

# Log registered blueprints
logger.info("Registered blueprints:")
for blueprint in app.blueprints:
    logger.info(f"- {blueprint}: {app.blueprints[blueprint].url_prefix}")

# Error handlers
@app.errorhandler(404)
def page_not_found(_):
    """404 error handler."""
    try:
        # The navigation_processor is already registered as a context processor,
        # so we don't need to pass it explicitly to the template
        return render_template(
            'fin_errors/fin_404.html',
            error_message="Page not found"
        ), 404
    except Exception as e:
        app.logger.error(f"Error in 404 handler: {str(e)}")
        # Fallback to a simple error page if navigation processor fails
        try:
            return render_template(
                'fin_errors/fin_error_simple.html',
                error_code=404,
                error_message="Page not found"
            ), 404
        except Exception as inner_e:
            app.logger.error(f"Error rendering simple error page: {str(inner_e)}")
            # Last resort fallback
            return "<h1>Error 404</h1><p>Page not found</p>", 404

@app.errorhandler(500)
def server_error(error):
    """500 error handler."""
    try:
        # The navigation_processor is already registered as a context processor,
        # so we don't need to pass it explicitly to the template
        return render_template(
            'fin_errors/fin_500.html',
            error_message=str(error)
        ), 500
    except Exception as e:
        app.logger.error(f"Error in 500 handler: {str(e)}")
        # Fallback to a simple error page if navigation processor fails
        try:
            return render_template(
                'fin_errors/fin_error_simple.html',
                error_code=500,
                error_message=f"Internal server error: {str(error)}"
            ), 500
        except Exception as inner_e:
            app.logger.error(f"Error rendering simple error page: {str(inner_e)}")
            # Last resort fallback
            return f"<h1>Error 500</h1><p>Internal server error: {str(error)}</p>", 500

def create_app(config=None):
    """Create and configure the Flask application."""
    if config:
        app.config.update(config)

    # Set testing mode if environment variable is set
    if os.environ.get('TESTING') == 'True':
        app.config['TESTING'] = True

    return app

if __name__ == '__main__':
    # Initialize database if needed
    try:
        from src.database.adapters import get_database_adapter
        from src.database.init_all_data import init_all_data

        db_adapter = get_database_adapter()
        if db_adapter.connect():
            logger.info("Connected to database")

            # Initialize all data
            init_all_data()
            logger.info("Initialized all data")
        else:
            logger.warning("Failed to connect to database")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")

    # Run the application
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5050))  # Changed default port to 5050
    debug = os.getenv('DEBUG', 'True').lower() == 'true'

    logger.info(f"Starting LensIQ on {host}:{port} (debug={debug})")
    app.run(host=host, port=port, debug=debug)
