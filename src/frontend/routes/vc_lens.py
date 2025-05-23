"""
VC Lens™ Routes for SustainaTrend™ Platform
Provides VC look-through and trend analysis
"""

import logging
from flask import Blueprint, render_template, request, jsonify, current_app, redirect, url_for
from typing import Dict, List, Optional, Any

from .base_route import BaseRoute
from src.database.database_service import database_service

logger = logging.getLogger(__name__)

class VCLensRoute(BaseRoute):
    """VC Lens route handler."""
    
    def __init__(self):
        """Initialize the VC Lens route."""
        super().__init__(name='vc_lens')
        self.blueprint = Blueprint('vc_lens', __name__)
        self.register_routes()
        
    def register_routes(self):
        """Register all routes for the VC Lens blueprint."""
        
        @self.blueprint.route('/')
        @self.handle_errors
        def index():
            """VC Lens - Private Equity Look-Through"""
            # Initialize database connection
            if not database_service.is_connected():
                logger.info("Connecting to database...")
                database_service.connect()
            
            # Initialize collections if they don't exist
            database_service.initialize_collections([
                'funds',
                'companies',
                'projects'
            ])
            
            # Get data from Firebase
            funds = self._get_funds()
            companies = self._get_companies()
            
            # Check database connection
            firebase_available = database_service.is_connected()
            
            logger.info(f"Retrieved {len(funds)} funds from database")
            logger.info(f"Retrieved {len(companies)} companies from database")
            
            context = {
                'active_nav': 'vc_lens',
                'page_title': "VC Lens - Private Equity Look-Through",
                'funds': funds,
                'companies': companies,
                'firebase_available': firebase_available
            }
            
            return self.render_template('fin_vc_lens/fin_vc_lens.html', **context)
        
        @self.blueprint.route('/funds')
        @self.handle_errors
        def funds():
            """VC Lens - Funds view"""
            funds = self._get_funds()
            
            context = {
                'active_nav': 'vc_lens',
                'sub_nav': 'funds',
                'page_title': "VC Lens - Funds",
                'funds': funds
            }
            
            return self.render_template('fin_vc_lens/fin_funds.html', **context)
        
        @self.blueprint.route('/companies')
        @self.handle_errors
        def companies():
            """VC Lens - Companies view"""
            companies = self._get_companies()
            
            context = {
                'active_nav': 'vc_lens',
                'sub_nav': 'companies',
                'page_title': "VC Lens - Companies",
                'companies': companies
            }
            
            return self.render_template('fin_vc_lens/fin_companies.html', **context)
        
        @self.blueprint.route('/api/funds')
        @self.handle_errors
        def api_funds():
            """API endpoint for funds data"""
            funds = self._get_funds()
            return self.json_response(funds)
        
        @self.blueprint.route('/api/companies')
        @self.handle_errors
        def api_companies():
            """API endpoint for companies data"""
            companies = self._get_companies()
            return self.json_response(companies)
    
    def _get_funds(self) -> List[Dict]:
        """Get funds data from database."""
        funds = database_service.find(
            'funds', 
            sort=[('aum', -1)],
            limit=10
        )
        
        # If no data in Firebase, insert sample data
        if not funds:
            logger.info("No funds found in database, inserting sample data...")
            sample_funds = [
                {
                    "name": "Sustainable Growth Fund",
                    "aum": 1200000000,
                    "focus": "Climate Tech",
                    "year_founded": 2018,
                    "sustainability_score": 92,
                    "portfolio_companies": ["EcoTech Solutions", "ClimateAI", "GreenGrid"]
                },
                {
                    "name": "Circular Economy Partners",
                    "aum": 800000000,
                    "focus": "Circular Economy",
                    "year_founded": 2016,
                    "sustainability_score": 88,
                    "portfolio_companies": ["GreenCircle", "RecycleNow", "MaterialLoop"]
                },
                {
                    "name": "Clean Energy Ventures",
                    "aum": 650000000,
                    "focus": "Renewable Energy",
                    "year_founded": 2015,
                    "sustainability_score": 85,
                    "portfolio_companies": ["SolarPlus", "WindPower", "EnergyStorage"]
                },
                {
                    "name": "Impact Investing Group",
                    "aum": 500000000,
                    "focus": "Social Impact",
                    "year_founded": 2017,
                    "sustainability_score": 82,
                    "portfolio_companies": ["SustainFi", "EduTech", "HealthAccess"]
                },
                {
                    "name": "Green Tech Fund",
                    "aum": 450000000,
                    "focus": "Sustainable Technology",
                    "year_founded": 2019,
                    "sustainability_score": 80,
                    "portfolio_companies": ["CarbonCapture Inc.", "WaterPurify", "SmartGrid"]
                }
            ]
            database_service.insert_many('funds', sample_funds)
            funds = sample_funds
            
        return funds
    
    def _get_companies(self) -> List[Dict]:
        """Get companies data from database."""
        companies = database_service.find(
            'companies', 
            sort=[('valuation', -1)],
            limit=10
        )
        
        # If no data in Firebase, insert sample data
        if not companies:
            logger.info("No companies found in database, inserting sample data...")
            sample_companies = [
                {
                    "name": "EcoTech Solutions",
                    "sector": "Renewable Energy",
                    "valuation": 450000000,
                    "founded": 2017,
                    "sustainability_score": 92,
                    "growth_rate": 35,
                    "projects": ["Solar Panel Recycling", "Energy Storage Systems"]
                },
                {
                    "name": "GreenCircle",
                    "sector": "Circular Economy",
                    "valuation": 380000000,
                    "founded": 2018,
                    "sustainability_score": 88,
                    "growth_rate": 42,
                    "projects": ["Plastic Alternatives", "Waste Reduction Platform"]
                },
                {
                    "name": "CarbonCapture Inc.",
                    "sector": "Carbon Tech",
                    "valuation": 320000000,
                    "founded": 2019,
                    "sustainability_score": 85,
                    "growth_rate": 48,
                    "projects": ["Direct Air Capture", "Carbon Sequestration"]
                },
                {
                    "name": "SustainFi",
                    "sector": "Sustainable Finance",
                    "valuation": 280000000,
                    "founded": 2020,
                    "sustainability_score": 82,
                    "growth_rate": 30,
                    "projects": ["ESG Investment Platform", "Green Bonds Marketplace"]
                },
                {
                    "name": "ClimateAI",
                    "sector": "Climate Tech",
                    "valuation": 250000000,
                    "founded": 2018,
                    "sustainability_score": 80,
                    "growth_rate": 38,
                    "projects": ["Climate Risk Assessment", "Predictive Weather Analytics"]
                }
            ]
            database_service.insert_many('companies', sample_companies)
            companies = sample_companies
            
        return companies

# Create instance
vc_lens_route = VCLensRoute()
vc_lens_bp = vc_lens_route.blueprint
