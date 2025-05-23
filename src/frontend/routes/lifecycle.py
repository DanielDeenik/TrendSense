"""
Lifecycle Analysis Routes for TrendSense™ Platform
Provides sustainability lifecycle metrics and analysis
"""

import logging
from flask import Blueprint, render_template, request, jsonify, current_app
from typing import Dict, List, Optional, Any

from .base_route import BaseRoute
from src.database.database_service import database_service

logger = logging.getLogger(__name__)

class LifecycleRoute(BaseRoute):
    """Lifecycle Analysis route handler."""
    
    def __init__(self):
        """Initialize the Lifecycle Analysis route."""
        super().__init__(name='lifecycle')
        self.blueprint = Blueprint('lifecycle', __name__)
        self.register_routes()
        
    def register_routes(self):
        """Register all routes for the Lifecycle Analysis blueprint."""
        
        @self.blueprint.route('/')
        @self.handle_errors
        def index():
            """Lifecycle Analysis Dashboard"""
            # Initialize database connection
            if not database_service.is_connected():
                logger.info("Connecting to database...")
                database_service.connect()
            
            # Get sample data
            companies = self._get_companies()
            lifecycle_metrics = self._get_lifecycle_metrics()
            
            # Check database connection
            firebase_available = database_service.is_connected()
            
            context = {
                'active_nav': 'lifecycle',
                'page_title': "Lifecycle Analysis",
                'companies': companies,
                'lifecycle_metrics': lifecycle_metrics,
                'firebase_available': firebase_available
            }
            
            return self.render_template('fin_lifecycle/fin_lifecycle_dashboard.html', **context)
        
        @self.blueprint.route('/metrics/<company_id>')
        @self.handle_errors
        def company_metrics(company_id):
            """Lifecycle metrics for a specific company"""
            # Get company data
            company = self._get_company_by_id(company_id)
            metrics = self._get_company_lifecycle_metrics(company_id)
            
            context = {
                'active_nav': 'lifecycle',
                'sub_nav': 'metrics',
                'page_title': f"Lifecycle Metrics - {company['name']}",
                'company': company,
                'metrics': metrics
            }
            
            return self.render_template('fin_lifecycle/fin_company_metrics.html', **context)
        
        @self.blueprint.route('/api/metrics')
        @self.handle_errors
        def api_metrics():
            """API endpoint for lifecycle metrics data"""
            metrics = self._get_lifecycle_metrics()
            return self.json_response(metrics)
        
        @self.blueprint.route('/api/company/<company_id>/metrics')
        @self.handle_errors
        def api_company_metrics(company_id):
            """API endpoint for company lifecycle metrics data"""
            metrics = self._get_company_lifecycle_metrics(company_id)
            return self.json_response(metrics)
    
    def _get_companies(self) -> List[Dict]:
        """Get companies data from database."""
        companies = database_service.find(
            'companies', 
            sort=[('sustainability_score', -1)],
            limit=10
        )
        
        # If no data in Firebase, return sample data
        if not companies:
            logger.info("No companies found in database, using sample data...")
            companies = [
                {
                    "id": "eco-tech-solutions",
                    "name": "EcoTech Solutions",
                    "sector": "Renewable Energy",
                    "valuation": 450000000,
                    "founded": 2017,
                    "sustainability_score": 92,
                    "growth_rate": 35
                },
                {
                    "id": "green-circle",
                    "name": "GreenCircle",
                    "sector": "Circular Economy",
                    "valuation": 380000000,
                    "founded": 2018,
                    "sustainability_score": 88,
                    "growth_rate": 42
                },
                {
                    "id": "carbon-capture-inc",
                    "name": "CarbonCapture Inc.",
                    "sector": "Carbon Tech",
                    "valuation": 320000000,
                    "founded": 2019,
                    "sustainability_score": 85,
                    "growth_rate": 48
                },
                {
                    "id": "sustainfi",
                    "name": "SustainFi",
                    "sector": "Sustainable Finance",
                    "valuation": 280000000,
                    "founded": 2020,
                    "sustainability_score": 82,
                    "growth_rate": 30
                },
                {
                    "id": "climate-ai",
                    "name": "ClimateAI",
                    "sector": "Climate Tech",
                    "valuation": 250000000,
                    "founded": 2018,
                    "sustainability_score": 80,
                    "growth_rate": 38
                }
            ]
            
        return companies
    
    def _get_company_by_id(self, company_id: str) -> Dict:
        """Get company data by ID."""
        company = database_service.find_one('companies', {'id': company_id})
        
        # If no data in Firebase, return sample data
        if not company:
            logger.info(f"Company {company_id} not found in database, using sample data...")
            companies = self._get_companies()
            for c in companies:
                if c.get('id') == company_id:
                    return c
            
            # Return first company if ID not found
            return companies[0] if companies else {}
            
        return company
    
    def _get_lifecycle_metrics(self) -> List[Dict]:
        """Get lifecycle metrics data."""
        metrics = database_service.find(
            'lifecycle_metrics', 
            sort=[('company_id', 1)],
            limit=10
        )
        
        # If no data in Firebase, return sample data
        if not metrics:
            logger.info("No lifecycle metrics found in database, using sample data...")
            metrics = [
                {
                    "company_id": "eco-tech-solutions",
                    "carbon_intensity": 17.3,
                    "reuse_factor": 8.4,
                    "csrd_compliance": 83,
                    "water_usage": 43,
                    "hazardous_waste": 0,
                    "recyclable_materials": 94,
                    "closed_loop_processes": 72,
                    "social_impact": {
                        "jobs_created": 1200,
                        "fair_wage_certification": 85
                    },
                    "lp_ready": True
                },
                {
                    "company_id": "green-circle",
                    "carbon_intensity": 15.8,
                    "reuse_factor": 9.2,
                    "csrd_compliance": 87,
                    "water_usage": 38,
                    "hazardous_waste": 0,
                    "recyclable_materials": 96,
                    "closed_loop_processes": 78,
                    "social_impact": {
                        "jobs_created": 950,
                        "fair_wage_certification": 90
                    },
                    "lp_ready": True
                },
                {
                    "company_id": "carbon-capture-inc",
                    "carbon_intensity": 12.5,
                    "reuse_factor": 7.8,
                    "csrd_compliance": 79,
                    "water_usage": 52,
                    "hazardous_waste": 2,
                    "recyclable_materials": 88,
                    "closed_loop_processes": 65,
                    "social_impact": {
                        "jobs_created": 850,
                        "fair_wage_certification": 82
                    },
                    "lp_ready": True
                },
                {
                    "company_id": "sustainfi",
                    "carbon_intensity": 8.2,
                    "reuse_factor": 6.5,
                    "csrd_compliance": 92,
                    "water_usage": 28,
                    "hazardous_waste": 0,
                    "recyclable_materials": 85,
                    "closed_loop_processes": 60,
                    "social_impact": {
                        "jobs_created": 450,
                        "fair_wage_certification": 95
                    },
                    "lp_ready": True
                },
                {
                    "company_id": "climate-ai",
                    "carbon_intensity": 9.7,
                    "reuse_factor": 5.2,
                    "csrd_compliance": 88,
                    "water_usage": 35,
                    "hazardous_waste": 1,
                    "recyclable_materials": 82,
                    "closed_loop_processes": 58,
                    "social_impact": {
                        "jobs_created": 620,
                        "fair_wage_certification": 88
                    },
                    "lp_ready": True
                }
            ]
            
        return metrics
    
    def _get_company_lifecycle_metrics(self, company_id: str) -> Dict:
        """Get lifecycle metrics for a specific company."""
        metrics = database_service.find_one('lifecycle_metrics', {'company_id': company_id})
        
        # If no data in Firebase, return sample data
        if not metrics:
            logger.info(f"Lifecycle metrics for company {company_id} not found in database, using sample data...")
            all_metrics = self._get_lifecycle_metrics()
            for m in all_metrics:
                if m.get('company_id') == company_id:
                    return m
            
            # Return first metrics if company ID not found
            return all_metrics[0] if all_metrics else {}
            
        return metrics

# Create instance
lifecycle_route = LifecycleRoute()
lifecycle_bp = lifecycle_route.blueprint
