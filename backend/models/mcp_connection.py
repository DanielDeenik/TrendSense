from ..database import db
from datetime import datetime
import json

class MCPConnection(db.Model):
    """
    Model for storing MCP tool connections.
    """
    __tablename__ = 'mcp_connections'
    
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    api_key = db.Column(db.String(500), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(50), nullable=False)
    capabilities = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    portfolio = db.relationship('Portfolio', backref=db.backref('mcp_connections', lazy=True))
    
    def __init__(self, portfolio_id, url, api_key, name, version, capabilities):
        self.portfolio_id = portfolio_id
        self.url = url
        self.api_key = api_key
        self.name = name
        self.version = version
        self.capabilities = capabilities
        
    def to_dict(self):
        """
        Convert the model to a dictionary.
        """
        return {
            'id': self.id,
            'portfolio_id': self.portfolio_id,
            'url': self.url,
            'name': self.name,
            'version': self.version,
            'capabilities': self.capabilities,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
    def __repr__(self):
        return f'<MCPConnection {self.name} (v{self.version})>' 