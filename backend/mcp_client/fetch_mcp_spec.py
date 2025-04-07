"""
Fetch MCP Specification
Module for fetching Model Context Protocol (MCP) specifications.
"""

import logging
import requests
from typing import Dict, Any, Optional
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_mcp_spec(base_url: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetch the MCP specification from a server
    
    Args:
        base_url: Base URL of the MCP server
        api_key: Optional API key for authentication
        
    Returns:
        Dict containing the MCP specification
    """
    try:
        # Ensure the base URL doesn't end with a slash
        base_url = base_url.rstrip('/')
        
        # Construct the URL for the MCP specification
        url = urljoin(base_url, '/.well-known/mcp.json')
        
        # Set up headers
        headers = {}
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'
        
        # Make the request
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse the response
        spec = response.json()
        
        logger.info(f"Successfully fetched MCP specification from {url}")
        return spec
    except Exception as e:
        logger.error(f"Error fetching MCP specification from {base_url}: {str(e)}")
        raise 