from flask import Blueprint, request, jsonify
from ..mcp_client.mcp_client import MCPClient
from ..models.portfolio import Portfolio
from ..models.mcp_connection import MCPConnection
from ..database import db
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
mcp_bp = Blueprint('mcp', __name__)

@mcp_bp.route('/api/mcp/fetch', methods=['POST'])
def fetch_mcp_spec():
    """
    Fetch and parse MCP specification from a given URL.
    """
    try:
        data = request.get_json()
        url = data.get('url')
        api_key = data.get('api_key')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
            
        # Initialize MCP client
        client = MCPClient()
        
        # Fetch MCP specification
        spec = client.fetch_mcp_spec(url, api_key)
        
        # Parse capabilities
        capabilities = client.parse_capabilities(spec)
        
        return jsonify(capabilities)
        
    except Exception as e:
        logger.error(f"Error fetching MCP specification: {str(e)}")
        return jsonify({'error': str(e)}), 500

@mcp_bp.route('/api/mcp/connect', methods=['POST'])
def connect_mcp_tool():
    """
    Connect an MCP tool to a portfolio.
    """
    try:
        data = request.get_json()
        url = data.get('url')
        api_key = data.get('api_key')
        portfolio_id = data.get('portfolio_id')
        
        if not all([url, portfolio_id]):
            return jsonify({'error': 'URL and portfolio ID are required'}), 400
            
        # Check if portfolio exists
        portfolio = Portfolio.query.get(portfolio_id)
        if not portfolio:
            return jsonify({'error': 'Portfolio not found'}), 404
            
        # Initialize MCP client
        client = MCPClient()
        
        # Fetch and validate MCP specification
        spec = client.fetch_mcp_spec(url, api_key)
        capabilities = client.parse_capabilities(spec)
        
        # Create MCP connection
        connection = MCPConnection(
            portfolio_id=portfolio_id,
            url=url,
            api_key=api_key,
            name=capabilities.get('name', 'Unknown Tool'),
            version=capabilities.get('version', 'Unknown'),
            capabilities=capabilities
        )
        
        # Save to database
        db.session.add(connection)
        db.session.commit()
        
        return jsonify({
            'message': 'MCP tool connected successfully',
            'connection_id': connection.id
        })
        
    except Exception as e:
        logger.error(f"Error connecting MCP tool: {str(e)}")
        return jsonify({'error': str(e)}), 500

@mcp_bp.route('/api/mcp/connections/<portfolio_id>', methods=['GET'])
def get_mcp_connections(portfolio_id):
    """
    Get all MCP connections for a portfolio.
    """
    try:
        # Check if portfolio exists
        portfolio = Portfolio.query.get(portfolio_id)
        if not portfolio:
            return jsonify({'error': 'Portfolio not found'}), 404
            
        # Get connections
        connections = MCPConnection.query.filter_by(portfolio_id=portfolio_id).all()
        
        return jsonify({
            'connections': [{
                'id': conn.id,
                'name': conn.name,
                'version': conn.version,
                'url': conn.url,
                'capabilities': conn.capabilities
            } for conn in connections]
        })
        
    except Exception as e:
        logger.error(f"Error getting MCP connections: {str(e)}")
        return jsonify({'error': str(e)}), 500

@mcp_bp.route('/api/mcp/connections/<connection_id>', methods=['DELETE'])
def delete_mcp_connection(connection_id):
    """
    Delete an MCP connection.
    """
    try:
        # Get connection
        connection = MCPConnection.query.get(connection_id)
        if not connection:
            return jsonify({'error': 'Connection not found'}), 404
            
        # Delete connection
        db.session.delete(connection)
        db.session.commit()
        
        return jsonify({'message': 'MCP connection deleted successfully'})
        
    except Exception as e:
        logger.error(f"Error deleting MCP connection: {str(e)}")
        return jsonify({'error': str(e)}), 500 