from datetime import datetime
from ..database import db

class LCAData(db.Model):
    """
    Model for storing Life Cycle Assessment (LCA) data.
    """
    __tablename__ = 'lca_data'
    
    id = db.Column(db.Integer, primary_key=True)
    startup_id = db.Column(db.Integer, db.ForeignKey('startups.id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=True)
    functional_unit = db.Column(db.String(100), nullable=True)
    system_boundary = db.Column(db.String(255), nullable=True)
    
    # LCA Stages
    raw_materials = db.Column(db.JSON, nullable=True)  # Raw materials extraction and processing
    manufacturing = db.Column(db.JSON, nullable=True)  # Manufacturing and assembly
    distribution = db.Column(db.JSON, nullable=True)  # Distribution and transportation
    use_phase = db.Column(db.JSON, nullable=True)  # Use phase
    end_of_life = db.Column(db.JSON, nullable=True)  # End-of-life and disposal
    
    # Environmental Impacts
    global_warming_potential = db.Column(db.Float, nullable=True)  # kg CO2e
    water_consumption = db.Column(db.Float, nullable=True)  # m3
    energy_consumption = db.Column(db.Float, nullable=True)  # MJ
    resource_depletion = db.Column(db.Float, nullable=True)  # kg Sb-eq
    eutrophication = db.Column(db.Float, nullable=True)  # kg PO4-eq
    
    # Circularity Metrics
    recyclability = db.Column(db.Float, nullable=True)  # 0-1 scale
    reusability = db.Column(db.Float, nullable=True)  # 0-1 scale
    biodegradability = db.Column(db.Float, nullable=True)  # 0-1 scale
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    startup = db.relationship('Startup', backref=db.backref('lca_assessments', lazy=True))
    
    def __init__(self, startup_id, product_name=None, functional_unit=None, system_boundary=None,
                 raw_materials=None, manufacturing=None, distribution=None, use_phase=None, 
                 end_of_life=None, global_warming_potential=None, water_consumption=None,
                 energy_consumption=None, resource_depletion=None, eutrophication=None,
                 recyclability=None, reusability=None, biodegradability=None):
        self.startup_id = startup_id
        self.product_name = product_name
        self.functional_unit = functional_unit
        self.system_boundary = system_boundary
        self.raw_materials = raw_materials
        self.manufacturing = manufacturing
        self.distribution = distribution
        self.use_phase = use_phase
        self.end_of_life = end_of_life
        self.global_warming_potential = global_warming_potential
        self.water_consumption = water_consumption
        self.energy_consumption = energy_consumption
        self.resource_depletion = resource_depletion
        self.eutrophication = eutrophication
        self.recyclability = recyclability
        self.reusability = reusability
        self.biodegradability = biodegradability
    
    def to_dict(self):
        """
        Convert the model to a dictionary.
        """
        return {
            'id': self.id,
            'startup_id': self.startup_id,
            'product_name': self.product_name,
            'functional_unit': self.functional_unit,
            'system_boundary': self.system_boundary,
            'raw_materials': self.raw_materials,
            'manufacturing': self.manufacturing,
            'distribution': self.distribution,
            'use_phase': self.use_phase,
            'end_of_life': self.end_of_life,
            'global_warming_potential': self.global_warming_potential,
            'water_consumption': self.water_consumption,
            'energy_consumption': self.energy_consumption,
            'resource_depletion': self.resource_depletion,
            'eutrophication': self.eutrophication,
            'recyclability': self.recyclability,
            'reusability': self.reusability,
            'biodegradability': self.biodegradability,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<LCAData {self.product_name} for Startup {self.startup_id}>'


class StartupAssessment(db.Model):
    """
    Model for storing startup assessment results.
    """
    __tablename__ = 'startup_assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    startup_id = db.Column(db.Integer, db.ForeignKey('startups.id'), nullable=False)
    vc_firm_id = db.Column(db.Integer, db.ForeignKey('vc_firms.id'), nullable=True)
    investment_thesis_id = db.Column(db.Integer, db.ForeignKey('investment_theses.id'), nullable=True)
    
    # Assessment Scores
    product_viability_score = db.Column(db.Float, nullable=True)
    operational_maturity_score = db.Column(db.Float, nullable=True)
    governance_risk_score = db.Column(db.Float, nullable=True)
    strategic_fit_score = db.Column(db.Float, nullable=True)
    market_signal_score = db.Column(db.Float, nullable=True)
    overall_readiness_score = db.Column(db.Float, nullable=True)
    
    # Detailed Assessment
    product_viability_details = db.Column(db.JSON, nullable=True)
    operational_maturity_details = db.Column(db.JSON, nullable=True)
    governance_risk_details = db.Column(db.JSON, nullable=True)
    strategic_fit_details = db.Column(db.JSON, nullable=True)
    market_signal_details = db.Column(db.JSON, nullable=True)
    
    # AI-Generated Insights
    ai_insights = db.Column(db.Text, nullable=True)
    improvement_recommendations = db.Column(db.JSON, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    startup = db.relationship('Startup', backref=db.backref('assessments', lazy=True))
    vc_firm = db.relationship('VCFirm', backref=db.backref('assessments', lazy=True))
    investment_thesis = db.relationship('InvestmentThesis', backref=db.backref('assessments', lazy=True))
    
    def __init__(self, startup_id, vc_firm_id=None, investment_thesis_id=None,
                 product_viability_score=None, operational_maturity_score=None,
                 governance_risk_score=None, strategic_fit_score=None,
                 market_signal_score=None, overall_readiness_score=None,
                 product_viability_details=None, operational_maturity_details=None,
                 governance_risk_details=None, strategic_fit_details=None,
                 market_signal_details=None, ai_insights=None,
                 improvement_recommendations=None):
        self.startup_id = startup_id
        self.vc_firm_id = vc_firm_id
        self.investment_thesis_id = investment_thesis_id
        self.product_viability_score = product_viability_score
        self.operational_maturity_score = operational_maturity_score
        self.governance_risk_score = governance_risk_score
        self.strategic_fit_score = strategic_fit_score
        self.market_signal_score = market_signal_score
        self.overall_readiness_score = overall_readiness_score
        self.product_viability_details = product_viability_details
        self.operational_maturity_details = operational_maturity_details
        self.governance_risk_details = governance_risk_details
        self.strategic_fit_details = strategic_fit_details
        self.market_signal_details = market_signal_details
        self.ai_insights = ai_insights
        self.improvement_recommendations = improvement_recommendations
    
    def to_dict(self):
        """
        Convert the model to a dictionary.
        """
        return {
            'id': self.id,
            'startup_id': self.startup_id,
            'vc_firm_id': self.vc_firm_id,
            'investment_thesis_id': self.investment_thesis_id,
            'product_viability_score': self.product_viability_score,
            'operational_maturity_score': self.operational_maturity_score,
            'governance_risk_score': self.governance_risk_score,
            'strategic_fit_score': self.strategic_fit_score,
            'market_signal_score': self.market_signal_score,
            'overall_readiness_score': self.overall_readiness_score,
            'product_viability_details': self.product_viability_details,
            'operational_maturity_details': self.operational_maturity_details,
            'governance_risk_details': self.governance_risk_details,
            'strategic_fit_details': self.strategic_fit_details,
            'market_signal_details': self.market_signal_details,
            'ai_insights': self.ai_insights,
            'improvement_recommendations': self.improvement_recommendations,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<StartupAssessment for Startup {self.startup_id}>'


class MaterialityMatrix(db.Model):
    """
    Model for storing materiality matrices for startups.
    """
    __tablename__ = 'materiality_matrices'
    
    id = db.Column(db.Integer, primary_key=True)
    startup_id = db.Column(db.Integer, db.ForeignKey('startups.id'), nullable=False)
    sector = db.Column(db.String(100), nullable=True)
    geography = db.Column(db.String(100), nullable=True)
    company_size = db.Column(db.String(50), nullable=True)
    
    # Materiality Matrix Data
    matrix_data = db.Column(db.JSON, nullable=False)  # Structured matrix data
    regulatory_exposure = db.Column(db.JSON, nullable=True)  # Regulatory exposure data
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    startup = db.relationship('Startup', backref=db.backref('materiality_matrices', lazy=True))
    
    def __init__(self, startup_id, matrix_data, sector=None, geography=None, 
                 company_size=None, regulatory_exposure=None):
        self.startup_id = startup_id
        self.matrix_data = matrix_data
        self.sector = sector
        self.geography = geography
        self.company_size = company_size
        self.regulatory_exposure = regulatory_exposure
    
    def to_dict(self):
        """
        Convert the model to a dictionary.
        """
        return {
            'id': self.id,
            'startup_id': self.startup_id,
            'sector': self.sector,
            'geography': self.geography,
            'company_size': self.company_size,
            'matrix_data': self.matrix_data,
            'regulatory_exposure': self.regulatory_exposure,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<MaterialityMatrix for Startup {self.startup_id}>' 