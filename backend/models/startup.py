from datetime import datetime
from ..database import db

class Startup(db.Model):
    """
    Model for storing startup information with sustainability assessment data.
    """
    __tablename__ = 'startups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    sector = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    founded_year = db.Column(db.Integer, nullable=True)
    funding_stage = db.Column(db.String(50), nullable=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=True)
    
    # LCA Data
    lca_data = db.Column(db.JSON, nullable=True)
    carbon_intensity_per_unit = db.Column(db.Float, nullable=True)
    water_intensity_per_unit = db.Column(db.Float, nullable=True)
    energy_intensity_per_unit = db.Column(db.Float, nullable=True)
    circularity_index = db.Column(db.Float, nullable=True)
    
    # Assessment Metrics
    product_viability_score = db.Column(db.Float, nullable=True)
    operational_maturity_score = db.Column(db.Float, nullable=True)
    governance_risk_score = db.Column(db.Float, nullable=True)
    strategic_fit_score = db.Column(db.Float, nullable=True)
    market_signal_score = db.Column(db.Float, nullable=True)
    overall_readiness_score = db.Column(db.Float, nullable=True)
    
    # Materiality Assessment
    materiality_matrix = db.Column(db.JSON, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    portfolio = db.relationship('Portfolio', backref=db.backref('startups', lazy=True))
    documents = db.relationship('StartupDocument', backref='startup', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, name, description=None, sector=None, country=None, founded_year=None, 
                 funding_stage=None, portfolio_id=None):
        self.name = name
        self.description = description
        self.sector = sector
        self.country = country
        self.founded_year = founded_year
        self.funding_stage = funding_stage
        self.portfolio_id = portfolio_id
    
    def to_dict(self):
        """
        Convert the model to a dictionary.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'sector': self.sector,
            'country': self.country,
            'founded_year': self.founded_year,
            'funding_stage': self.funding_stage,
            'portfolio_id': self.portfolio_id,
            'lca_data': self.lca_data,
            'carbon_intensity_per_unit': self.carbon_intensity_per_unit,
            'water_intensity_per_unit': self.water_intensity_per_unit,
            'energy_intensity_per_unit': self.energy_intensity_per_unit,
            'circularity_index': self.circularity_index,
            'product_viability_score': self.product_viability_score,
            'operational_maturity_score': self.operational_maturity_score,
            'governance_risk_score': self.governance_risk_score,
            'strategic_fit_score': self.strategic_fit_score,
            'market_signal_score': self.market_signal_score,
            'overall_readiness_score': self.overall_readiness_score,
            'materiality_matrix': self.materiality_matrix,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Startup {self.name}>'


class StartupDocument(db.Model):
    """
    Model for storing documents related to startups (LCA reports, pitch decks, etc.).
    """
    __tablename__ = 'startup_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    startup_id = db.Column(db.Integer, db.ForeignKey('startups.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)  # 'lca', 'pitch', 'financial', etc.
    file_path = db.Column(db.String(500), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, nullable=True)  # in bytes
    content_summary = db.Column(db.Text, nullable=True)
    extracted_data = db.Column(db.JSON, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, startup_id, document_type, file_path, file_name, file_size=None, 
                 content_summary=None, extracted_data=None):
        self.startup_id = startup_id
        self.document_type = document_type
        self.file_path = file_path
        self.file_name = file_name
        self.file_size = file_size
        self.content_summary = content_summary
        self.extracted_data = extracted_data
    
    def to_dict(self):
        """
        Convert the model to a dictionary.
        """
        return {
            'id': self.id,
            'startup_id': self.startup_id,
            'document_type': self.document_type,
            'file_path': self.file_path,
            'file_name': self.file_name,
            'file_size': self.file_size,
            'content_summary': self.content_summary,
            'extracted_data': self.extracted_data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<StartupDocument {self.file_name} ({self.document_type})>' 