"""
Error Handler module for SustainaTrend™

This module provides centralized error handling functionality.
"""

import logging
from typing import Dict, Any, Optional, Tuple, Callable
from functools import wraps
from flask import jsonify, render_template, current_app, Blueprint

logger = logging.getLogger(__name__)

class ErrorResponse:
    """Class for standardizing error responses."""
    
    def __init__(self, message: str, status_code: int, details: Optional[Dict[str, Any]] = None):
        """Initialize an error response."""
        self.message = message
        self.status_code = status_code
        self.details = details or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error response to dictionary."""
        return {
            "error": True,
            "message": self.message,
            "status_code": self.status_code,
            "details": self.details
        }

def handle_error(error: Exception) -> Tuple[Dict[str, Any], int]:
    """Handle any exception and return appropriate response."""
    logger.error(f"Error occurred: {str(error)}", exc_info=True)
    
    if hasattr(error, "code"):
        status_code = error.code
    else:
        status_code = 500
    
    error_response = ErrorResponse(
        message=str(error),
        status_code=status_code
    )
    
    return error_response.to_dict(), status_code

def api_error_handler(f):
    """Decorator for handling API endpoint errors."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            response, status_code = handle_error(e)
            return jsonify(response), status_code
    return decorated_function

def view_error_handler(f):
    """Decorator for handling view endpoint errors."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in view: {str(e)}", exc_info=True)
            return render_template(
                "error.html",
                error_message=str(e),
                error_code=getattr(e, "code", 500)
            ), getattr(e, "code", 500)
    return decorated_function

def init_error_handlers(app):
    """Initialize error handlers for the application."""
    
    @app.errorhandler(400)
    def bad_request_error(error):
        """Handle bad request errors."""
        return handle_error(error)
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        """Handle unauthorized errors."""
        return handle_error(error)
    
    @app.errorhandler(403)
    def forbidden_error(error):
        """Handle forbidden errors."""
        return handle_error(error)
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle not found errors."""
        return handle_error(error)
    
    @app.errorhandler(405)
    def method_not_allowed_error(error):
        """Handle method not allowed errors."""
        return handle_error(error)
    
    @app.errorhandler(429)
    def too_many_requests_error(error):
        """Handle too many requests errors."""
        return handle_error(error)
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle internal server errors."""
        return handle_error(error)
    
    @app.errorhandler(Exception)
    def unhandled_exception(error):
        """Handle any unhandled exceptions."""
        return handle_error(error)

def handle_errors(blueprint: Blueprint) -> Callable:
    """
    Register error handlers for a blueprint.
    
    Args:
        blueprint: The Flask blueprint to register error handlers for
        
    Returns:
        Callable: Function to register error handlers
    """
    def register_error_handlers():
        """Register error handlers for the blueprint."""
        
        @blueprint.errorhandler(400)
        def bad_request_error(error):
            """Handle bad request errors."""
            return handle_error(error)
        
        @blueprint.errorhandler(401)
        def unauthorized_error(error):
            """Handle unauthorized errors."""
            return handle_error(error)
        
        @blueprint.errorhandler(403)
        def forbidden_error(error):
            """Handle forbidden errors."""
            return handle_error(error)
        
        @blueprint.errorhandler(404)
        def not_found_error(error):
            """Handle not found errors."""
            return handle_error(error)
        
        @blueprint.errorhandler(405)
        def method_not_allowed_error(error):
            """Handle method not allowed errors."""
            return handle_error(error)
        
        @blueprint.errorhandler(429)
        def too_many_requests_error(error):
            """Handle too many requests errors."""
            return handle_error(error)
        
        @blueprint.errorhandler(500)
        def internal_server_error(error):
            """Handle internal server errors."""
            return handle_error(error)
        
        @blueprint.errorhandler(Exception)
        def unhandled_exception(error):
            """Handle any unhandled exceptions."""
            return handle_error(error)
    
    return register_error_handlers

class APIError(Exception):
    """Base class for API errors."""
    
    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None):
        """Initialize an API error."""
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}

class ValidationError(APIError):
    """Error raised when request validation fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        """Initialize a validation error."""
        super().__init__(message, status_code=400, details=details)

class AuthenticationError(APIError):
    """Error raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed"):
        """Initialize an authentication error."""
        super().__init__(message, status_code=401)

class AuthorizationError(APIError):
    """Error raised when authorization fails."""
    
    def __init__(self, message: str = "Not authorized"):
        """Initialize an authorization error."""
        super().__init__(message, status_code=403)

class NotFoundError(APIError):
    """Error raised when a resource is not found."""
    
    def __init__(self, message: str = "Resource not found"):
        """Initialize a not found error."""
        super().__init__(message, status_code=404)

class RateLimitError(APIError):
    """Error raised when rate limit is exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        """Initialize a rate limit error."""
        super().__init__(message, status_code=429) 