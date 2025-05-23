"""
TrendRadar™ Routes for SustainaTrend™ Platform
Provides AI-powered sustainability trend radar visualization
"""

import logging
from flask import Blueprint, render_template, request, jsonify, current_app
from typing import Dict, List, Optional, Any

from .base_route import BaseRoute
from src.database.database_service import database_service

logger = logging.getLogger(__name__)

class TrendRadarRoute(BaseRoute):
    """TrendRadar route handler."""

    def __init__(self):
        """Initialize the TrendRadar route."""
        super().__init__(name='trendradar')
        self.blueprint = Blueprint('trendradar', __name__)
        self.register_routes()

    def register_routes(self):
        """Register all routes for the TrendRadar blueprint."""

        @self.blueprint.route('/')
        @self.handle_errors
        def index():
            """TrendRadar - AI-powered sustainability trend radar visualization"""
            # Initialize database connection
            if not database_service.is_connected():
                logger.info("Connecting to database...")
                database_service.connect()

            # Initialize collections if they don't exist
            database_service.initialize_collections([
                'trending_categories',
                'trends',
                'startups',
                'radar_metrics'
            ])

            # Get data from Firebase
            trends_data = self._get_trends_data()
            radar_metrics = self._get_radar_metrics()

            # Check database connection
            firebase_available = database_service.is_connected()

            logger.info(f"Retrieved {len(trends_data)} trends from database")
            logger.info(f"Retrieved {len(radar_metrics)} radar metrics from database")

            context = {
                'active_nav': 'trendradar',
                'page_title': "TrendRadar - Sustainability Trend Visualization",
                'trends': trends_data,
                'radar_metrics': radar_metrics,
                'firebase_available': firebase_available
            }

            return self.render_template('fin_radar/fin_trendradar.html', **context)

        @self.blueprint.route('/api/radar-data')
        @self.handle_errors
        def api_radar_data():
            """API endpoint for radar data"""
            trends_data = self._get_trends_data()
            radar_metrics = self._get_radar_metrics()

            # Define categories and stages
            categories = list(set([trend.get('category', 'Unknown') for trend in trends_data]))
            stages = ['Watch', 'Prepare', 'Act']

            response = {
                'trends': trends_data,
                'metrics': radar_metrics,
                'categories': categories,
                'stages': stages
            }

            return self.json_response(response)

        @self.blueprint.route('/api/metrics')
        @self.handle_errors
        def api_metrics():
            """API endpoint for radar metrics"""
            metrics = self._get_radar_metrics()
            return self.json_response(metrics)

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

        return trends_data

    def _get_radar_metrics(self) -> List[Dict]:
        """Get radar metrics from database."""
        radar_metrics = database_service.find(
            'radar_metrics',
            sort=[('importance', -1)],
            limit=10
        )

        # If no data in Firebase, insert sample data
        if not radar_metrics:
            logger.info("No radar metrics found in database, inserting sample data...")
            sample_metrics = [
                {
                    "name": "environmental_impact",
                    "display_name": "Environmental Impact",
                    "description": "Measures the positive environmental effects of the trend",
                    "importance": 95,
                    "category": "Environmental"
                },
                {
                    "name": "market_potential",
                    "display_name": "Market Potential",
                    "description": "Estimates the market size and growth potential",
                    "importance": 90,
                    "category": "Financial"
                },
                {
                    "name": "innovation_level",
                    "display_name": "Innovation Level",
                    "description": "Measures the degree of innovation and technological advancement",
                    "importance": 85,
                    "category": "Technology"
                },
                {
                    "name": "regulatory_support",
                    "display_name": "Regulatory Support",
                    "description": "Assesses the level of regulatory support and policy alignment",
                    "importance": 80,
                    "category": "Policy"
                },
                {
                    "name": "investment_activity",
                    "display_name": "Investment Activity",
                    "description": "Tracks the level of investment in the trend",
                    "importance": 75,
                    "category": "Financial"
                },
                {
                    "name": "social_impact",
                    "display_name": "Social Impact",
                    "description": "Measures the positive social effects of the trend",
                    "importance": 70,
                    "category": "Social"
                },
                {
                    "name": "scalability",
                    "display_name": "Scalability",
                    "description": "Assesses how easily the trend can scale globally",
                    "importance": 65,
                    "category": "Business"
                },
                {
                    "name": "adoption_rate",
                    "display_name": "Adoption Rate",
                    "description": "Measures how quickly the trend is being adopted",
                    "importance": 60,
                    "category": "Market"
                }
            ]
            database_service.insert_many('radar_metrics', sample_metrics)
            radar_metrics = sample_metrics

        return radar_metrics

# Create instance
trendradar_route = TrendRadarRoute()
trendradar_bp = trendradar_route.blueprint
