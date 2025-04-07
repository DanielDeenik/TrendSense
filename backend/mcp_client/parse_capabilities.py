"""
Parse Capabilities
Module for parsing capabilities from Model Context Protocol (MCP) specifications.
"""

import logging
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_capabilities(spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse capabilities from an MCP specification
    
    Args:
        spec: MCP specification
        
    Returns:
        Dict containing the parsed capabilities
    """
    try:
        capabilities = {
            'name': spec.get('name', ''),
            'description': spec.get('description', ''),
            'version': spec.get('version', ''),
            'endpoints': []
        }
        
        for endpoint in spec.get('endpoints', []):
            capabilities['endpoints'].append({
                'path': endpoint.get('path', ''),
                'method': endpoint.get('method', 'GET'),
                'description': endpoint.get('description', ''),
                'parameters': endpoint.get('parameters', []),
                'responses': endpoint.get('responses', {})
            })
        
        logger.info(f"Successfully parsed capabilities from {spec.get('name', 'Unknown')}")
        return capabilities
    except Exception as e:
        logger.error(f"Error parsing capabilities: {str(e)}")
        raise 