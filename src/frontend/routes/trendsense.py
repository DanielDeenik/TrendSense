"""
TrendSense™ Routes for SustainaTrend™ Platform
Provides AI-powered sustainability trend analysis
"""

import logging
from flask import Blueprint, render_template, request, jsonify, current_app
from typing import Dict, List, Optional, Any

from .base_route import BaseRoute
from src.database.database_service import database_service

logger = logging.getLogger(__name__)

class TrendSenseRoute(BaseRoute):
    """TrendSense route handler."""

    def __init__(self):
        """Initialize the TrendSense route."""
        super().__init__(name='trendsense')
        self.blueprint = Blueprint('trendsense', __name__)
        self.register_routes()

    def register_routes(self):
        """Register all routes for the TrendSense blueprint."""

        @self.blueprint.route('/')
        @self.handle_errors
        def index():
            """TrendSense - AI-powered sustainability trend analysis"""
            # Initialize database connection
            if not database_service.is_connected():
                logger.info("Connecting to database...")
                database_service.connect()

            # Initialize collections if they don't exist
            database_service.initialize_collections([
                'trending_categories',
                'trends',
                'startups'
            ])

            # Get data from Firebase
            trending_categories = self._get_trending_categories()
            trends_data = self._get_trends_data()
            startup_radar = self._get_startup_radar()

            # Check database connection
            firebase_available = database_service.is_connected()

            logger.info(f"Retrieved {len(trending_categories)} trending categories from database")
            logger.info(f"Retrieved {len(trends_data)} trends from database")
            logger.info(f"Retrieved {len(startup_radar)} startups from database")

            context = {
                'active_nav': 'trendsense',
                'page_title': "TrendSense - Sustainability Trend Analysis",
                'trending_categories': trending_categories,
                'trends': trends_data,
                'startup_radar': startup_radar,
                'firebase_available': firebase_available
            }

            return self.render_template('fin_vc_lens/fin_trendsense.html', **context)

        @self.blueprint.route('/api/trends')
        @self.handle_errors
        def api_trends():
            """API endpoint for trends data"""
            trends_data = self._get_trends_data()
            return self.json_response(trends_data)

        @self.blueprint.route('/api/categories')
        @self.handle_errors
        def api_categories():
            """API endpoint for trending categories"""
            categories = self._get_trending_categories()
            return self.json_response(categories)

        @self.blueprint.route('/api/startups')
        @self.handle_errors
        def api_startups():
            """API endpoint for startup radar"""
            startups = self._get_startup_radar()
            return self.json_response(startups)

    def _get_trending_categories(self) -> List[Dict]:
        """Get trending categories from database."""
        trending_categories = database_service.find(
            'trending_categories',
            sort=[('growth', -1)],
            limit=10
        )

        # If no data in Firebase, insert sample data
        if not trending_categories:
            logger.info("No trending categories found in database, inserting sample data...")
            sample_categories = [
                {"name": "Renewable Energy", "count": 42, "growth": 24, "description": "Trending in Renewable Energy"},
                {"name": "Circular Economy", "count": 38, "growth": 32, "description": "Trending in Circular Economy"},
                {"name": "Carbon Tech", "count": 35, "growth": 45, "description": "Trending in Carbon Tech"},
                {"name": "Sustainable Finance", "count": 30, "growth": 18, "description": "Trending in Sustainable Finance"},
                {"name": "Climate Tech", "count": 28, "growth": 28, "description": "Trending in Climate Tech"},
                {"name": "Sustainable Agriculture", "count": 25, "growth": 15, "description": "Trending in Sustainable Agriculture"}
            ]
            database_service.insert_many('trending_categories', sample_categories)
            trending_categories = sample_categories

        return trending_categories

    def _get_trends_data(self) -> List[Dict]:
        """Get trends data from database."""
        trends_data = database_service.find(
            'trends',
            sort=[('score', -1)],
            limit=10
        )

        # If no data in Firebase, insert sample data
        if not trends_data:
            logger.info("No trends data found in database, inserting sample data...")
            sample_trends = [
                {
                    "category": "Renewable Energy",
                    "growth": 24,
                    "score": 85,
                    "trend_values": [65, 68, 70, 72, 75, 78, 80, 82, 85, 87, 90, 92],
                    "metrics": {
                        "environmental_impact": 88,
                        "market_potential": 82,
                        "innovation_level": 76,
                        "regulatory_support": 70,
                        "investment_activity": 85
                    }
                },
                {
                    "category": "Circular Economy",
                    "growth": 32,
                    "score": 78,
                    "trend_values": [55, 58, 62, 65, 68, 70, 72, 74, 75, 76, 78, 80],
                    "metrics": {
                        "environmental_impact": 90,
                        "market_potential": 75,
                        "innovation_level": 80,
                        "regulatory_support": 65,
                        "investment_activity": 72
                    }
                },
                {
                    "category": "Carbon Tech",
                    "growth": 45,
                    "score": 92,
                    "trend_values": [40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 88, 92],
                    "metrics": {
                        "environmental_impact": 95,
                        "market_potential": 88,
                        "innovation_level": 92,
                        "regulatory_support": 78,
                        "investment_activity": 90
                    }
                },
                {
                    "category": "Sustainable Finance",
                    "growth": 18,
                    "score": 65,
                    "trend_values": [40, 42, 45, 48, 50, 52, 55, 58, 60, 62, 64, 65],
                    "metrics": {
                        "environmental_impact": 60,
                        "market_potential": 72,
                        "innovation_level": 65,
                        "regulatory_support": 68,
                        "investment_activity": 70
                    }
                },
                {
                    "category": "Climate Tech",
                    "growth": 28,
                    "score": 82,
                    "trend_values": [50, 55, 58, 62, 65, 68, 70, 72, 75, 78, 80, 82],
                    "metrics": {
                        "environmental_impact": 85,
                        "market_potential": 80,
                        "innovation_level": 88,
                        "regulatory_support": 72,
                        "investment_activity": 78
                    }
                },
                {
                    "category": "Sustainable Agriculture",
                    "growth": 15,
                    "score": 70,
                    "trend_values": [45, 48, 50, 52, 55, 58, 60, 62, 65, 68, 70, 70],
                    "metrics": {
                        "environmental_impact": 82,
                        "market_potential": 68,
                        "innovation_level": 72,
                        "regulatory_support": 65,
                        "investment_activity": 60
                    }
                }
            ]
            database_service.insert_many('trends', sample_trends)
            trends_data = sample_trends

        # Ensure all trends have a metrics field
        default_metrics = {
            "environmental_impact": 75,
            "market_potential": 70,
            "innovation_level": 65,
            "regulatory_support": 60,
            "investment_activity": 65
        }

        for trend in trends_data:
            if 'metrics' not in trend or not trend['metrics']:
                logger.warning(f"Adding default metrics to trend: {trend.get('category', 'Unknown')}")
                trend['metrics'] = default_metrics

            # Ensure trend_values exists
            if 'trend_values' not in trend:
                trend['trend_values'] = [60, 62, 65, 68, 70, 72, 75, 78, 80, 82, 85, trend.get('score', 80)]

            # Ensure growth exists
            if 'growth' not in trend:
                trend['growth'] = 20

        return trends_data

    def _get_startup_radar(self) -> List[Dict]:
        """Get startup radar data from database."""
        startup_radar = database_service.find(
            'startups',
            sort=[('growth_score', -1)],
            limit=5
        )

        # If no data in Firebase, insert sample data
        if not startup_radar:
            logger.info("No startup data found in database, inserting sample data...")
            sample_startups = [
                {
                    "name": "EcoTech Solutions",
                    "sector": "Renewable Energy",
                    "growth_score": 92
                },
                {
                    "name": "GreenCircle",
                    "sector": "Circular Economy",
                    "growth_score": 88
                },
                {
                    "name": "CarbonCapture Inc.",
                    "sector": "Carbon Tech",
                    "growth_score": 85
                },
                {
                    "name": "SustainFi",
                    "sector": "Sustainable Finance",
                    "growth_score": 82
                },
                {
                    "name": "ClimateAI",
                    "sector": "Climate Tech",
                    "growth_score": 80
                }
            ]
            database_service.insert_many('startups', sample_startups)
            startup_radar = sample_startups

        return startup_radar

# Create instance
trendsense_route = TrendSenseRoute()
trendsense_bp = trendsense_route.blueprint
