"""
Portfolio Company Schema
Defines the expected fields and validation rules for portfolio company data ingestion.
"""

from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime

class FinancialMetrics(BaseModel):
    """Financial metrics for a portfolio company"""
    revenue: Optional[float] = Field(None, description="Annual revenue in USD")
    ebitda: Optional[float] = Field(None, description="EBITDA in USD")
    growth_rate: Optional[float] = Field(None, description="Year-over-year growth rate")
    burn_rate: Optional[float] = Field(None, description="Monthly cash burn rate in USD")
    runway_months: Optional[int] = Field(None, description="Estimated runway in months")
    funding_rounds: Optional[List[Dict]] = Field(default_factory=list, description="List of funding rounds")
    valuation: Optional[float] = Field(None, description="Latest valuation in USD")
    
    @validator('growth_rate')
    def validate_growth_rate(cls, v):
        if v is not None and (v < -100 or v > 1000):
            raise ValueError("Growth rate must be between -100 and 1000 percent")
        return v

class SustainabilityMetrics(BaseModel):
    """Sustainability metrics for a portfolio company"""
    carbon_intensity: Optional[float] = Field(None, description="Carbon intensity in tCO2e/$M revenue")
    renewable_energy_pct: Optional[float] = Field(None, description="Percentage of energy from renewable sources")
    water_intensity: Optional[float] = Field(None, description="Water intensity in m3/$M revenue")
    waste_reduction_pct: Optional[float] = Field(None, description="Percentage of waste reduction")
    sdg_alignment: Optional[List[int]] = Field(default_factory=list, description="List of SDGs the company aligns with")
    esg_score: Optional[float] = Field(None, description="ESG score (0-100)")
    impact_score: Optional[float] = Field(None, description="Impact score (0-100)")
    
    @validator('esg_score', 'impact_score')
    def validate_score_range(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError("Score must be between 0 and 100")
        return v
    
    @validator('sdg_alignment')
    def validate_sdg_range(cls, v):
        if v:
            for sdg in v:
                if sdg < 1 or sdg > 17:
                    raise ValueError("SDG must be between 1 and 17")
        return v

class PortfolioCompany(BaseModel):
    """Portfolio company data model"""
    id: Optional[str] = Field(None, description="Unique identifier")
    name: str = Field(..., description="Company name")
    legal_name: Optional[str] = Field(None, description="Legal entity name")
    country: str = Field(..., description="Country of headquarters")
    region: Optional[str] = Field(None, description="Region")
    sector: str = Field(..., description="Primary sector")
    subsector: Optional[str] = Field(None, description="Subsector")
    description: Optional[str] = Field(None, description="Company description")
    website: Optional[str] = Field(None, description="Company website")
    founded_date: Optional[datetime] = Field(None, description="Company founding date")
    investment_date: Optional[datetime] = Field(None, description="Date of investment")
    exit_date: Optional[datetime] = Field(None, description="Date of exit if applicable")
    status: str = Field(..., description="Investment status (active, exited, written-off)")
    ownership_pct: Optional[float] = Field(None, description="Percentage ownership")
    financial_metrics: Optional[FinancialMetrics] = Field(None, description="Financial metrics")
    sustainability_metrics: Optional[SustainabilityMetrics] = Field(None, description="Sustainability metrics")
    team: Optional[List[Dict]] = Field(default_factory=list, description="Key team members")
    board_members: Optional[List[Dict]] = Field(default_factory=list, description="Board members")
    documents: Optional[List[Dict]] = Field(default_factory=list, description="Related documents")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    
    @validator('ownership_pct')
    def validate_ownership(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError("Ownership percentage must be between 0 and 100")
        return v
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ['active', 'exited', 'written-off', 'pending']
        if v not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
        return v 