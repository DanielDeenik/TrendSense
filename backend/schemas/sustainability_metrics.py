"""
Sustainability Metrics Schema
Defines the expected fields and validation rules for sustainability data ingestion.
"""

from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime

class CarbonEmissions(BaseModel):
    """Carbon emissions data"""
    scope1_emissions: Optional[float] = Field(None, description="Scope 1 emissions in tCO2e")
    scope2_emissions: Optional[float] = Field(None, description="Scope 2 emissions in tCO2e")
    scope3_emissions: Optional[float] = Field(None, description="Scope 3 emissions in tCO2e")
    total_emissions: Optional[float] = Field(None, description="Total emissions in tCO2e")
    emission_intensity: Optional[float] = Field(None, description="Emission intensity in tCO2e/$M revenue")
    reduction_target: Optional[float] = Field(None, description="Emission reduction target in percentage")
    reduction_achieved: Optional[float] = Field(None, description="Emission reduction achieved in percentage")
    carbon_offsets: Optional[float] = Field(None, description="Carbon offsets in tCO2e")
    net_emissions: Optional[float] = Field(None, description="Net emissions after offsets in tCO2e")
    reporting_period: Optional[datetime] = Field(None, description="Reporting period end date")
    
    @validator('reduction_target', 'reduction_achieved')
    def validate_percentage(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError("Percentage must be between 0 and 100")
        return v

class EnergyMetrics(BaseModel):
    """Energy consumption and renewable energy data"""
    total_energy_consumption: Optional[float] = Field(None, description="Total energy consumption in MWh")
    renewable_energy_consumption: Optional[float] = Field(None, description="Renewable energy consumption in MWh")
    renewable_energy_percentage: Optional[float] = Field(None, description="Percentage of energy from renewable sources")
    energy_intensity: Optional[float] = Field(None, description="Energy intensity in MWh/$M revenue")
    energy_efficiency_improvement: Optional[float] = Field(None, description="Energy efficiency improvement in percentage")
    reporting_period: Optional[datetime] = Field(None, description="Reporting period end date")
    
    @validator('renewable_energy_percentage', 'energy_efficiency_improvement')
    def validate_percentage(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError("Percentage must be between 0 and 100")
        return v

class WaterMetrics(BaseModel):
    """Water consumption and management data"""
    total_water_withdrawal: Optional[float] = Field(None, description="Total water withdrawal in m3")
    water_consumption: Optional[float] = Field(None, description="Water consumption in m3")
    water_intensity: Optional[float] = Field(None, description="Water intensity in m3/$M revenue")
    water_recycling_rate: Optional[float] = Field(None, description="Water recycling rate in percentage")
    water_stress_area: Optional[bool] = Field(None, description="Whether the company operates in a water-stressed area")
    reporting_period: Optional[datetime] = Field(None, description="Reporting period end date")
    
    @validator('water_recycling_rate')
    def validate_percentage(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError("Percentage must be between 0 and 100")
        return v

class WasteMetrics(BaseModel):
    """Waste generation and management data"""
    total_waste_generated: Optional[float] = Field(None, description="Total waste generated in tonnes")
    hazardous_waste: Optional[float] = Field(None, description="Hazardous waste in tonnes")
    waste_recycling_rate: Optional[float] = Field(None, description="Waste recycling rate in percentage")
    waste_to_landfill: Optional[float] = Field(None, description="Waste sent to landfill in tonnes")
    circular_economy_score: Optional[float] = Field(None, description="Circular economy score (0-100)")
    reporting_period: Optional[datetime] = Field(None, description="Reporting period end date")
    
    @validator('waste_recycling_rate', 'circular_economy_score')
    def validate_percentage(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError("Percentage must be between 0 and 100")
        return v

class SDGAlignment(BaseModel):
    """Sustainable Development Goals alignment data"""
    sdg_goals: List[int] = Field(..., description="List of SDGs the company aligns with")
    primary_sdg: Optional[int] = Field(None, description="Primary SDG focus")
    sdg_contribution_score: Optional[float] = Field(None, description="SDG contribution score (0-100)")
    sdg_impact_metrics: Optional[Dict[str, float]] = Field(None, description="Impact metrics for each SDG")
    
    @validator('sdg_goals', 'primary_sdg')
    def validate_sdg_range(cls, v):
        if isinstance(v, list):
            for sdg in v:
                if sdg < 1 or sdg > 17:
                    raise ValueError("SDG must be between 1 and 17")
        elif v is not None and (v < 1 or v > 17):
            raise ValueError("SDG must be between 1 and 17")
        return v
    
    @validator('sdg_contribution_score')
    def validate_score_range(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError("Score must be between 0 and 100")
        return v

class SustainabilityMetrics(BaseModel):
    """Comprehensive sustainability metrics data model"""
    company_id: str = Field(..., description="Company identifier")
    reporting_period: datetime = Field(..., description="Reporting period end date")
    carbon_emissions: Optional[CarbonEmissions] = Field(None, description="Carbon emissions data")
    energy_metrics: Optional[EnergyMetrics] = Field(None, description="Energy metrics data")
    water_metrics: Optional[WaterMetrics] = Field(None, description="Water metrics data")
    waste_metrics: Optional[WasteMetrics] = Field(None, description="Waste metrics data")
    sdg_alignment: Optional[SDGAlignment] = Field(None, description="SDG alignment data")
    esg_score: Optional[float] = Field(None, description="Overall ESG score (0-100)")
    impact_score: Optional[float] = Field(None, description="Impact score (0-100)")
    verification_status: Optional[str] = Field(None, description="Verification status of the data")
    verification_body: Optional[str] = Field(None, description="Body that verified the data")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    
    @validator('esg_score', 'impact_score')
    def validate_score_range(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError("Score must be between 0 and 100")
        return v
    
    @validator('verification_status')
    def validate_verification_status(cls, v):
        if v is not None:
            valid_statuses = ['verified', 'self-reported', 'pending', 'not-verified']
            if v not in valid_statuses:
                raise ValueError(f"Verification status must be one of {valid_statuses}")
        return v 