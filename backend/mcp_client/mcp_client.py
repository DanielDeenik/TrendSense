"""
MCP Client
Main class for interacting with Model Context Protocol (MCP) servers.
"""

import json
import logging
import requests
from typing import Dict, Any, List, Optional, Union
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPClient:
    """Client for interacting with MCP servers"""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize the MCP client
        
        Args:
            base_url: Base URL of the MCP server
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.spec = None
        self.capabilities = None
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}'
            })
    
    def fetch_spec(self) -> Dict[str, Any]:
        """
        Fetch the MCP specification from the server
        
        Returns:
            Dict containing the MCP specification
        """
        try:
            url = urljoin(self.base_url, '/.well-known/mcp.json')
            response = self.session.get(url)
            response.raise_for_status()
            
            self.spec = response.json()
            return self.spec
        except Exception as e:
            logger.error(f"Error fetching MCP spec: {str(e)}")
            raise
    
    def parse_capabilities(self) -> Dict[str, Any]:
        """
        Parse the capabilities from the MCP specification
        
        Returns:
            Dict containing the parsed capabilities
        """
        if not self.spec:
            self.fetch_spec()
        
        try:
            capabilities = {
                'name': self.spec.get('name', ''),
                'description': self.spec.get('description', ''),
                'version': self.spec.get('version', ''),
                'endpoints': []
            }
            
            for endpoint in self.spec.get('endpoints', []):
                capabilities['endpoints'].append({
                    'path': endpoint.get('path', ''),
                    'method': endpoint.get('method', 'GET'),
                    'description': endpoint.get('description', ''),
                    'parameters': endpoint.get('parameters', []),
                    'responses': endpoint.get('responses', {})
                })
            
            self.capabilities = capabilities
            return capabilities
        except Exception as e:
            logger.error(f"Error parsing capabilities: {str(e)}")
            raise
    
    def query_tool(self, tool_id: str, method: str = 'GET', params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Query a tool on the MCP server
        
        Args:
            tool_id: ID of the tool to query
            method: HTTP method to use (GET, POST, etc.)
            params: Parameters to pass to the tool
            
        Returns:
            Dict containing the tool response
        """
        if not self.capabilities:
            self.parse_capabilities()
        
        try:
            # Find the endpoint for the tool
            endpoint = None
            for ep in self.capabilities['endpoints']:
                if ep['path'].endswith(f'/{tool_id}'):
                    endpoint = ep
                    break
            
            if not endpoint:
                raise ValueError(f"Tool {tool_id} not found in MCP specification")
            
            # Construct the URL
            url = urljoin(self.base_url, endpoint['path'])
            
            # Make the request
            if method.upper() == 'GET':
                response = self.session.get(url, params=params)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=params)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            logger.error(f"Error querying tool {tool_id}: {str(e)}")
            raise
    
    def get_tool_prompt(self, tool_id: str) -> str:
        """
        Generate a prompt for using a tool
        
        Args:
            tool_id: ID of the tool
            
        Returns:
            String containing the prompt
        """
        if not self.capabilities:
            self.parse_capabilities()
        
        try:
            # Find the endpoint for the tool
            endpoint = None
            for ep in self.capabilities['endpoints']:
                if ep['path'].endswith(f'/{tool_id}'):
                    endpoint = ep
                    break
            
            if not endpoint:
                raise ValueError(f"Tool {tool_id} not found in MCP specification")
            
            # Generate the prompt
            prompt = f"Tool: {endpoint['description']}\n"
            prompt += f"Method: {endpoint['method']}\n"
            
            if endpoint.get('parameters'):
                prompt += "Parameters:\n"
                for param in endpoint['parameters']:
                    prompt += f"  - {param.get('name')}: {param.get('description')}\n"
            
            if endpoint.get('responses'):
                prompt += "Responses:\n"
                for status, response in endpoint['responses'].items():
                    prompt += f"  - {status}: {response.get('description')}\n"
            
            return prompt
        except Exception as e:
            logger.error(f"Error generating prompt for tool {tool_id}: {str(e)}")
            raise 