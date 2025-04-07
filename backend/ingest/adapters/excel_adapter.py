"""
Excel Adapter
Normalizes data from Excel format to TrendSense schema.
"""

import logging
import pandas as pd
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from ...schemas.portfolio_company import PortfolioCompany, FinancialMetrics, SustainabilityMetrics
from ...schemas.sustainability_metrics import SustainabilityMetrics as SustainabilityMetricsSchema

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExcelAdapter:
    """Adapter for normalizing Excel data to TrendSense schema"""
    
    def __init__(self):
        self.supported_formats = ['xlsx', 'xls']
    
    def can_handle(self, file_path: str) -> bool:
        """Check if this adapter can handle the given file"""
        file_extension = file_path.split('.')[-1].lower()
        return file_extension in self.supported_formats
    
    def read_file(self, file_path: str) -> Dict[str, pd.DataFrame]:
        """Read and parse the Excel file"""
        try:
            # Read all sheets into a dictionary of DataFrames
            excel_file = pd.ExcelFile(file_path)
            return {sheet_name: pd.read_excel(excel_file, sheet_name=sheet_name) 
                   for sheet_name in excel_file.sheet_names}
        except Exception as e:
            logger.error(f"Error reading Excel file: {str(e)}")
            raise
    
    def normalize_portfolio_companies(self, df: pd.DataFrame) -> List[PortfolioCompany]:
        """Normalize Excel portfolio company data to TrendSense schema"""
        normalized_companies = []
        
        for _, row in df.iterrows():
            try:
                # Extract financial metrics
                financial_metrics = None
                if all(col in row for col in ['revenue', 'ebitda', 'growth_rate']):
                    financial_metrics = FinancialMetrics(
                        revenue=row.get('revenue'),
                        ebitda=row.get('ebitda'),
                        growth_rate=row.get('growth_rate'),
                        burn_rate=row.get('burn_rate'),
                        runway_months=row.get('runway_months'),
                        funding_rounds=row.get('funding_rounds', []),
                        valuation=row.get('valuation')
                    )
                
                # Extract sustainability metrics
                sustainability_metrics = None
                if all(col in row for col in ['carbon_intensity', 'renewable_energy_pct']):
                    sustainability_metrics = SustainabilityMetrics(
                        carbon_intensity=row.get('carbon_intensity'),
                        renewable_energy_pct=row.get('renewable_energy_pct'),
                        water_intensity=row.get('water_intensity'),
                        waste_reduction_pct=row.get('waste_reduction_pct'),
                        sdg_alignment=row.get('sdg_alignment', []),
                        esg_score=row.get('esg_score'),
                        impact_score=row.get('impact_score')
                    )
                
                # Create normalized company
                company = PortfolioCompany(
                    id=row.get('id'),
                    name=row.get('name'),
                    legal_name=row.get('legal_name'),
                    country=row.get('country', 'Unknown'),
                    region=row.get('region'),
                    sector=row.get('sector', 'Unknown'),
                    subsector=row.get('subsector'),
                    description=row.get('description'),
                    website=row.get('website'),
                    founded_date=row.get('founded_date'),
                    investment_date=row.get('investment_date'),
                    exit_date=row.get('exit_date'),
                    status=row.get('status', 'active'),
                    ownership_pct=row.get('ownership_pct'),
                    financial_metrics=financial_metrics,
                    sustainability_metrics=sustainability_metrics,
                    team=row.get('team', []),
                    board_members=row.get('board_members', []),
                    documents=row.get('documents', [])
                )
                
                normalized_companies.append(company)
                
            except Exception as e:
                logger.error(f"Error normalizing company data: {str(e)}")
                continue
        
        return normalized_companies
    
    def normalize_sustainability_metrics(self, df: pd.DataFrame) -> List[SustainabilityMetricsSchema]:
        """Normalize Excel sustainability metrics to TrendSense schema"""
        normalized_metrics = []
        
        for _, row in df.iterrows():
            try:
                # Extract carbon emissions
                carbon_emissions = None
                if all(col in row for col in ['scope1_emissions', 'scope2_emissions', 'scope3_emissions']):
                    carbon_emissions = {
                        'scope1_emissions': row.get('scope1_emissions'),
                        'scope2_emissions': row.get('scope2_emissions'),
                        'scope3_emissions': row.get('scope3_emissions'),
                        'total_emissions': row.get('total_emissions'),
                        'emission_intensity': row.get('emission_intensity'),
                        'reduction_target': row.get('reduction_target'),
                        'reduction_achieved': row.get('reduction_achieved'),
                        'carbon_offsets': row.get('carbon_offsets'),
                        'net_emissions': row.get('net_emissions')
                    }
                
                # Extract energy metrics
                energy_metrics = None
                if all(col in row for col in ['total_energy_consumption', 'renewable_energy_consumption']):
                    energy_metrics = {
                        'total_energy_consumption': row.get('total_energy_consumption'),
                        'renewable_energy_consumption': row.get('renewable_energy_consumption'),
                        'energy_intensity': row.get('energy_intensity'),
                        'efficiency_improvements': row.get('efficiency_improvements')
                    }
                
                # Extract water metrics
                water_metrics = None
                if all(col in row for col in ['water_withdrawal', 'water_consumption']):
                    water_metrics = {
                        'water_withdrawal': row.get('water_withdrawal'),
                        'water_consumption': row.get('water_consumption'),
                        'water_intensity': row.get('water_intensity'),
                        'recycling_rate': row.get('recycling_rate'),
                        'water_stressed_area': row.get('water_stressed_area', False)
                    }
                
                # Extract waste metrics
                waste_metrics = None
                if all(col in row for col in ['total_waste', 'hazardous_waste']):
                    waste_metrics = {
                        'total_waste': row.get('total_waste'),
                        'hazardous_waste': row.get('hazardous_waste'),
                        'recycling_rate': row.get('recycling_rate'),
                        'circular_economy_score': row.get('circular_economy_score')
                    }
                
                # Extract SDG alignment
                sdg_alignment = None
                if 'sdg_alignment' in row:
                    sdg_alignment = {
                        'sdgs': row.get('sdgs', []),
                        'primary_sdg': row.get('primary_sdg'),
                        'contribution_score': row.get('contribution_score'),
                        'impact_metrics': row.get('impact_metrics', {})
                    }
                
                # Create normalized metrics
                metrics = SustainabilityMetricsSchema(
                    company_id=row.get('company_id'),
                    reporting_period=row.get('reporting_period'),
                    carbon_emissions=carbon_emissions,
                    energy_metrics=energy_metrics,
                    water_metrics=water_metrics,
                    waste_metrics=waste_metrics,
                    sdg_alignment=sdg_alignment,
                    esg_score=row.get('esg_score'),
                    verification_status=row.get('verification_status', 'unverified'),
                    verification_date=row.get('verification_date'),
                    last_updated=row.get('last_updated', datetime.now())
                )
                
                normalized_metrics.append(metrics)
                
            except Exception as e:
                logger.error(f"Error normalizing sustainability metrics: {str(e)}")
                continue
        
        return normalized_metrics
    
    def process(self, file_path: str) -> Dict[str, Any]:
        """Process the Excel file and return normalized data"""
        try:
            sheets = self.read_file(file_path)
            
            # Process each sheet based on its name or content
            result = {}
            
            for sheet_name, df in sheets.items():
                if 'portfolio' in sheet_name.lower() or 'companies' in sheet_name.lower():
                    normalized_data = self.normalize_portfolio_companies(df)
                    result['portfolio_companies'] = [company.dict() for company in normalized_data]
                elif 'sustainability' in sheet_name.lower() or 'esg' in sheet_name.lower():
                    normalized_data = self.normalize_sustainability_metrics(df)
                    result['sustainability_metrics'] = [metrics.dict() for metrics in normalized_data]
            
            if not result:
                raise ValueError("No recognized data sheets found in Excel file")
            
            return result
                
        except Exception as e:
            logger.error(f"Error processing Excel file: {str(e)}")
            raise 