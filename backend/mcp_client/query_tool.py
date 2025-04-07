"""
Query Tool
Module for querying tools on Model Context Protocol (MCP) servers.
"""

import logging
import requests
from typing import Dict, Any, Optional
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def query_tool(
    base_url: str,
    tool_id: str,
    method: str = 'GET',
    params: Optional[Dict[str, Any]] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Query a tool on an MCP server
    
    Args:
        base_url: Base URL of the MCP server
        tool_id: ID of the tool to query
        method: HTTP method to use (GET, POST, etc.)
        params: Parameters to pass to the tool
        api_key: Optional API key for authentication
        
    Returns:
        Dict containing the tool response
    """
    try:
        # Ensure the base URL doesn't end with a slash
        base_url = base_url.rstrip('/')
        
        # Set up headers
        headers = {}
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'
        
        # Construct the URL for the tool
        url = urljoin(base_url, f'/{tool_id}')
        
        # Make the request
        if method.upper() == 'GET':
            response = requests.get(url, params=params, headers=headers)
        elif method.upper() == 'POST':
            response = requests.post(url, json=params, headers=headers)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        
        # Parse the response
        result = response.json()
        
        logger.info(f"Successfully queried tool {tool_id} on {base_url}")
        return result
    except Exception as e:
        logger.error(f"Error querying tool {tool_id} on {base_url}: {str(e)}")
        raise 