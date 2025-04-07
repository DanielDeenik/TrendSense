from datetime import datetime
from ..database import db

class VCFirm(db.Model):
    """
    Model for storing VC firm information.
    """
    __tablename__ = 'vc_firms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    website = db.Column(db.String(255), nullable=True)
    founded_year = db.Column(db.Integer, nullable=True)
    headquarters = db.Column(db.String(100), nullable=True)
    fund_size = db.Column(db.String(50), nullable=True)
    investment_focus = db.Column(db.String(255), nullable=True)
    
    # Sustainability Focus
    sustainability_focus = db.Column(db.Text, nullable=True)
    impact_goals = db.Column(db.JSON, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    portfolios = db.relationship('Portfolio', backref='vc_firm', lazy=True)
    theses = db.relationship('InvestmentThesis', backref='vc_firm', lazy=True)
    
    def __init__(self, name, description=None, website=None, founded_year=None, 
                 headquarters=None, fund_size=None, investment_focus=None,
                 sustainability_focus=None, impact_goals=None):
        self.name = name
        self.description = description
        self.website = website
        self.founded_year = founded_year
        self.headquarters = headquarters
        self.fund_size = fund_size
        self.investment_focus = investment_focus
        self.sustainability_focus = sustainability_focus
        self.impact_goals = impact_goals
    
    def to_dict(self):
        """
        Convert the model to a dictionary.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'website': self.website,
            'founded_year': self.founded_year,
            'headquarters': self.headquarters,
            'fund_size': self.fund_size,
            'investment_focus': self.investment_focus,
            'sustainability_focus': self.sustainability_focus,
            'impact_goals': self.impact_goals,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<VCFirm {self.name}>'


class InvestmentThesis(db.Model):
    """
    Model for storing VC investment theses.
    """
    __tablename__ = 'investment_theses'
    
    id = db.Column(db.Integer, primary_key=True)
    vc_firm_id = db.Column(db.Integer, db.ForeignKey('vc_firms.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    focus_areas = db.Column(db.JSON, nullable=True)  # List of focus areas
    investment_criteria = db.Column(db.JSON, nullable=True)  # Structured criteria
    sustainability_priorities = db.Column(db.JSON, nullable=True)  # Sustainability priorities
    regulatory_considerations = db.Column(db.JSON, nullable=True)  # Regulatory considerations
    
    # Keywords and phrases for matching
    keywords = db.Column(db.JSON, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, vc_firm_id, title, description=None, focus_areas=None, 
                 investment_criteria=None, sustainability_priorities=None,
                 regulatory_considerations=None, keywords=None):
        self.vc_firm_id = vc_firm_id
        self.title = title
        self.description = description
        self.focus_areas = focus_areas
        self.investment_criteria = investment_criteria
        self.sustainability_priorities = sustainability_priorities
        self.regulatory_considerations = regulatory_considerations
        self.keywords = keywords
    
    def to_dict(self):
        """
        Convert the model to a dictionary.
        """
        return {
            'id': self.id,
            'vc_firm_id': self.vc_firm_id,
            'title': self.title,
            'description': self.description,
            'focus_areas': self.focus_areas,
            'investment_criteria': self.investment_criteria,
            'sustainability_priorities': self.sustainability_priorities,
            'regulatory_considerations': self.regulatory_considerations,
            'keywords': self.keywords,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<InvestmentThesis {self.title}>'


class Portfolio(db.Model):
    """
    Model for storing VC portfolios.
    """
    __tablename__ = 'portfolios'
    
    id = db.Column(db.Integer, primary_key=True)
    vc_firm_id = db.Column(db.Integer, db.ForeignKey('vc_firms.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    fund_name = db.Column(db.String(100), nullable=True)
    vintage_year = db.Column(db.Integer, nullable=True)
    investment_thesis_id = db.Column(db.Integer, db.ForeignKey('investment_theses.id'), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    investment_thesis = db.relationship('InvestmentThesis', backref='portfolios', lazy=True)
    
    def __init__(self, vc_firm_id, name, description=None, fund_name=None, 
                 vintage_year=None, investment_thesis_id=None):
        self.vc_firm_id = vc_firm_id
        self.name = name
        self.description = description
        self.fund_name = fund_name
        self.vintage_year = vintage_year
        self.investment_thesis_id = investment_thesis_id
    
    def to_dict(self):
        """
        Convert the model to a dictionary.
        """
        return {
            'id': self.id,
            'vc_firm_id': self.vc_firm_id,
            'name': self.name,
            'description': self.description,
            'fund_name': self.fund_name,
            'vintage_year': self.vintage_year,
            'investment_thesis_id': self.investment_thesis_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Portfolio {self.name}>' 