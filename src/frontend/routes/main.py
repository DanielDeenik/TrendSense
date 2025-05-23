"""
Main routes for SustainaTrend™
"""

import logging
from flask import Blueprint, render_template, redirect, url_for
from .base_route import BaseRoute
from ..utils.navigation_config import get_context_for_template

logger = logging.getLogger(__name__)

class MainRoute(BaseRoute):
    """Main route handler."""
    
    def __init__(self):
        """Initialize the main route."""
        super().__init__(name='main')
        self.blueprint = Blueprint('main', __name__)
        self.template = 'index.html'
        self.register_routes()
    
    def register_routes(self):
        """Register all routes for the main blueprint."""
        
        @self.blueprint.route('/')
        @self.handle_errors
        def index():
            """Render the main index page."""
            context = get_context_for_template('index')
            return self.render_template(self.template, **context)
        
        @self.blueprint.route('/dashboard')
        @self.handle_errors
        def dashboard():
            """Redirect to dashboard page."""
            return redirect(url_for('dashboard.index'))
        
        @self.blueprint.route('/copilot')
        @self.handle_errors
        def copilot():
            """Render the AI copilot interface."""
            context = get_context_for_template('copilot')
            return self.render_template('copilot.html', **context)
        
        @self.blueprint.route('/vc-dashboard')
        @self.handle_errors
        def vc_dashboard():
            """Redirect to VC dashboard."""
            return redirect(url_for('vc_dashboard.index'))
        
        @self.blueprint.route('/about')
        @self.handle_errors
        def about():
            """Render the about page."""
            try:
                return self.render_template('about.html')
            except Exception as e:
                logger.error(f"Error rendering about page: {str(e)}")
                return self.render_template('error.html', message="An error occurred while loading the page"), 500
        
        @self.blueprint.route('/contact')
        @self.handle_errors
        def contact():
            """Render the contact page."""
            try:
                return self.render_template('contact.html')
            except Exception as e:
                logger.error(f"Error rendering contact page: {str(e)}")
                return self.render_template('error.html', message="An error occurred while loading the page"), 500
        
        @self.blueprint.route('/navigation')
        @self.handle_errors
        def navigation():
            """Render the navigation demo page."""
            context = get_context_for_template('navigation')
            return self.render_template('navigation.html', **context)

# Create instance
main_route = MainRoute()
bp = main_route.blueprint
