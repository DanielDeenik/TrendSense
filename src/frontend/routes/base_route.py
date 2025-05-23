"""
Base Route Class for SustainaTrend™

This module provides a base class for all route handlers in the application.
It includes common functionality and utilities that can be reused across different routes.
"""

import json
import logging
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Dict, Optional, Union, List

from flask import Blueprint, render_template, request, jsonify, current_app, Response
from werkzeug.exceptions import HTTPException

class BaseRoute:
    """Base class for all route handlers."""
    
    def __init__(self, name: str):
        """
        Initialize the base route.
        
        Args:
            name: The name of the route
        """
        self.name = name
        self.blueprint = Blueprint(name, __name__)
        self.logger = logging.getLogger(f"frontend.routes.{name}")
        
    def render_template(self, template: str, **kwargs) -> str:
        """
        Render a template with common context.
        
        Args:
            template: The template to render
            **kwargs: Additional context variables
            
        Returns:
            The rendered template
        """
        try:
            # Add common context variables
            context = {
                'current_route': self.name,
                'request': request,
                'now': datetime.now,
                **kwargs
            }
            return render_template(template, **context)
        except Exception as e:
            self.logger.error(f"Error rendering template {template}: {str(e)}")
            return self.json_response({'error': 'Template rendering failed'}, 500)
    
    def json_response(self, data: Any, status: int = 200) -> Response:
        """
        Create a JSON response.
        
        Args:
            data: The data to return
            status: HTTP status code
            
        Returns:
            Flask response object
        """
        return jsonify(data), status
    
    def handle_errors(self, f: Callable) -> Callable:
        """
        Decorator to handle errors in route handlers.
        
        Args:
            f: The function to decorate
            
        Returns:
            Decorated function
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except HTTPException as e:
                self.logger.error(f"HTTP error in {f.__name__}: {str(e)}")
                return self.json_response({'error': str(e)}, e.code)
            except Exception as e:
                self.logger.error(f"Error in {f.__name__}: {str(e)}")
                return self.json_response({'error': 'Internal server error'}, 500)
        return decorated_function
    
    def validate_required_fields(self, data: Dict, required_fields: list) -> Optional[str]:
        """
        Validate that all required fields are present in the data.
        
        Args:
            data: The data to validate
            required_fields: List of required field names
            
        Returns:
            Error message if validation fails, None otherwise
        """
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return f"Missing required fields: {', '.join(missing_fields)}"
        return None
    
    def cache_with_ttl(self, ttl: int = None) -> Callable:
        """
        Decorator for caching function results with a time-to-live.
        
        Args:
            ttl: Time-to-live in seconds
            
        Returns:
            A decorator function
        """
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Simple implementation - in a real app, use a proper caching system
                return f(*args, **kwargs)
            return decorated_function
        return decorator
