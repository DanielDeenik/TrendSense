"""
LemonEdge Adapter
Normalizes data from LemonEdge format to TrendSense schema.
"""

import json
import logging
import pandas as pd
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from ...schemas.portfolio_company import PortfolioCompany, FinancialMetrics, SustainabilityMetrics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LemonEdgeAdapter:
    """Adapter for normalizing LemonEdge data to TrendSense schema"""
    
    def __init__(self):
        self.supported_formats = ['json', 'csv', 'xlsx']
    
    def can_handle(self, file_path: str) -> bool:
        """Check if this adapter can handle the given file"""
        file_extension = file_path.split('.')[-1].lower()
        return file_extension in self.supported_formats
    
    def read_file(self, file_path: str) -> Dict[str, Any]:
        """Read and parse the LemonEdge file"""
        file_extension = file_path.split('.')[-1].lower()
        
        try:
            if file_extension == 'json':
                with open(file_path, 'r') as f:
                    return json.load(f)
            elif file_extension == 'csv':
                return pd.read_csv(file_path).to_dict(orient='records')
            elif file_extension == 'xlsx':
                return pd.read_excel(file_path).to_dict(orient='records')
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
        except Exception as e:
            logger.error(f"Error reading LemonEdge file: {str(e)}")
            raise
    
    def normalize_portfolio_companies(self, data: Union[Dict, List[Dict]]) -> List[PortfolioCompany]:
        """Normalize LemonEdge portfolio company data to TrendSense schema"""
        if isinstance(data, dict):
            data = [data]
        
        normalized_companies = []
        
        for company_data in data:
            try:
                # Extract financial metrics
                financial_metrics = None
                if 'financials' in company_data:
                    financials = company_data['financials']
                    financial_metrics = FinancialMetrics(
                        revenue=financials.get('revenue'),
                        ebitda=financials.get('ebitda'),
                        growth_rate=financials.get('growth_rate'),
                        burn_rate=financials.get('burn_rate'),
                        runway_months=financials.get('runway_months'),
                        funding_rounds=financials.get('funding_rounds', []),
                        valuation=financials.get('valuation')
                    )
                
                # Extract sustainability metrics
                sustainability_metrics = None
                if 'sustainability' in company_data:
                    sustainability = company_data['sustainability']
                    sustainability_metrics = SustainabilityMetrics(
                        carbon_intensity=sustainability.get('carbon_intensity'),
                        renewable_energy_pct=sustainability.get('renewable_energy_pct'),
                        water_intensity=sustainability.get('water_intensity'),
                        waste_reduction_pct=sustainability.get('waste_reduction_pct'),
                        sdg_alignment=sustainability.get('sdg_alignment', []),
                        esg_score=sustainability.get('esg_score'),
                        impact_score=sustainability.get('impact_score')
                    )
                
                # Create normalized company
                company = PortfolioCompany(
                    id=company_data.get('id'),
                    name=company_data.get('name'),
                    legal_name=company_data.get('legal_name'),
                    country=company_data.get('country', 'Unknown'),
                    region=company_data.get('region'),
                    sector=company_data.get('sector', 'Unknown'),
                    subsector=company_data.get('subsector'),
                    description=company_data.get('description'),
                    website=company_data.get('website'),
                    founded_date=company_data.get('founded_date'),
                    investment_date=company_data.get('investment_date'),
                    exit_date=company_data.get('exit_date'),
                    status=company_data.get('status', 'active'),
                    ownership_pct=company_data.get('ownership_pct'),
                    financial_metrics=financial_metrics,
                    sustainability_metrics=sustainability_metrics,
                    team=company_data.get('team', []),
                    board_members=company_data.get('board_members', []),
                    documents=company_data.get('documents', [])
                )
                
                normalized_companies.append(company)
                
            except Exception as e:
                logger.error(f"Error normalizing company data: {str(e)}")
                continue
        
        return normalized_companies
    
    def normalize_sustainability_metrics(self, data: Union[Dict, List[Dict]]) -> List[Dict]:
        """Normalize LemonEdge sustainability metrics to TrendSense schema"""
        # This would be implemented similarly to normalize_portfolio_companies
        # but using the SustainabilityMetrics schema
        # For brevity, this is a placeholder
        return []
    
    def process(self, file_path: str) -> Dict[str, Any]:
        """Process the LemonEdge file and return normalized data"""
        try:
            raw_data = self.read_file(file_path)
            
            # Determine the type of data and normalize accordingly
            if 'portfolio_companies' in raw_data or (isinstance(raw_data, list) and len(raw_data) > 0 and 'name' in raw_data[0]):
                normalized_data = self.normalize_portfolio_companies(raw_data)
                return {
                    'type': 'portfolio_companies',
                    'data': [company.dict() for company in normalized_data]
                }
            elif 'sustainability_metrics' in raw_data or (isinstance(raw_data, list) and len(raw_data) > 0 and 'company_id' in raw_data[0]):
                normalized_data = self.normalize_sustainability_metrics(raw_data)
                return {
                    'type': 'sustainability_metrics',
                    'data': normalized_data
                }
            else:
                raise ValueError("Unrecognized data format")
                
        except Exception as e:
            logger.error(f"Error processing LemonEdge file: {str(e)}")
            raise 