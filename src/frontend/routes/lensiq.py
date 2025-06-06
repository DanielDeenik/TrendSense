"""
LensIQ™ Routes for LensIQ Intelligence Platform
Provides AI-powered sustainability trend analysis and storytelling
"""

import logging
from flask import Blueprint, render_template, request, jsonify, current_app, redirect, url_for
from typing import Dict, List, Optional, Any

from .base_route import BaseRoute
from src.database.database_service import database_service

logger = logging.getLogger(__name__)

class LensIQRoute(BaseRoute):
    """LensIQ route handler for storytelling functionality."""
    
    def __init__(self):
        """Initialize the LensIQ route."""
        super().__init__(name='lensiq')
        self.blueprint = Blueprint('lensiq', __name__)
        self.register_routes()
        
    def register_routes(self):
        """Register all routes for the LensIQ blueprint."""
        
        @self.blueprint.route('/')
        @self.handle_errors
        def index():
            """LensIQ - AI-powered sustainability storytelling"""
            # Initialize database connection
            if not database_service.is_connected():
                logger.info("Connecting to database...")
                database_service.connect()
            
            # Initialize collections if they don't exist
            database_service.initialize_collections([
                'stories',
                'insights',
                'trends',
                'narratives'
            ])
            
            # Get data from database
            stories = self._get_stories()
            insights = self._get_insights()
            trends = self._get_trending_data()
            
            # Check database connection
            database_available = database_service.is_connected()
            
            logger.info(f"Retrieved {len(stories)} stories from database")
            logger.info(f"Retrieved {len(insights)} insights from database")
            logger.info(f"Retrieved {len(trends)} trends from database")
            
            context = {
                'active_nav': 'lensiq',
                'page_title': "LensIQ - AI-Powered Sustainability Storytelling",
                'stories': stories,
                'insights': insights,
                'trends': trends,
                'database_available': database_available
            }
            
            return self.render_template('lensiq/storytelling.html', **context)
        
        @self.blueprint.route('/storytelling')
        @self.handle_errors
        def storytelling():
            """LensIQ Storytelling - Main storytelling interface"""
            stories = self._get_stories()
            
            context = {
                'active_nav': 'lensiq',
                'sub_nav': 'storytelling',
                'page_title': "LensIQ - Sustainability Storytelling",
                'stories': stories
            }
            
            return self.render_template('lensiq/storytelling.html', **context)
        
        @self.blueprint.route('/insights')
        @self.handle_errors
        def insights():
            """LensIQ Insights - AI-generated insights"""
            insights = self._get_insights()
            
            context = {
                'active_nav': 'lensiq',
                'sub_nav': 'insights',
                'page_title': "LensIQ - AI Insights",
                'insights': insights
            }
            
            return self.render_template('lensiq/insights.html', **context)
        
        @self.blueprint.route('/narratives')
        @self.handle_errors
        def narratives():
            """LensIQ Narratives - Trend narratives"""
            narratives = self._get_narratives()
            
            context = {
                'active_nav': 'lensiq',
                'sub_nav': 'narratives',
                'page_title': "LensIQ - Trend Narratives",
                'narratives': narratives
            }
            
            return self.render_template('lensiq/narratives.html', **context)
        
        @self.blueprint.route('/api/stories')
        @self.handle_errors
        def api_stories():
            """API endpoint for stories data"""
            stories = self._get_stories()
            return self.json_response(stories)
        
        @self.blueprint.route('/api/insights')
        @self.handle_errors
        def api_insights():
            """API endpoint for insights data"""
            insights = self._get_insights()
            return self.json_response(insights)
        
        @self.blueprint.route('/api/generate-story', methods=['POST'])
        @self.handle_errors
        def api_generate_story():
            """API endpoint to generate a new story"""
            data = request.json or {}
            topic = data.get('topic', 'sustainability trends')
            
            # Generate story using AI (placeholder implementation)
            story = self._generate_story(topic)
            
            # Save to database
            story_id = database_service.insert('stories', story)
            story['_id'] = story_id
            
            return self.json_response(story)
    
    def _get_stories(self) -> List[Dict]:
        """Get stories data from database."""
        stories = database_service.find(
            'stories', 
            sort=[('created_at', -1)],
            limit=10
        )
        
        # If no data in database, insert sample data
        if not stories:
            logger.info("No stories found in database, inserting sample data...")
            sample_stories = [
                {
                    "title": "The Rise of Circular Economy in Tech",
                    "summary": "How technology companies are embracing circular economy principles to reduce waste and create sustainable value chains.",
                    "content": "The technology sector is undergoing a fundamental transformation as companies recognize the urgent need to move beyond the traditional linear 'take-make-dispose' model...",
                    "category": "Circular Economy",
                    "author": "LensIQ AI",
                    "created_at": "2024-01-15",
                    "tags": ["circular economy", "technology", "sustainability", "waste reduction"],
                    "engagement_score": 92,
                    "trend_relevance": 88
                },
                {
                    "title": "Green Hydrogen: The Energy Revolution",
                    "summary": "Exploring how green hydrogen is becoming the cornerstone of the clean energy transition and its impact on global sustainability goals.",
                    "content": "Green hydrogen, produced through electrolysis powered by renewable energy, represents one of the most promising pathways to decarbonize heavy industry...",
                    "category": "Clean Energy",
                    "author": "LensIQ AI",
                    "created_at": "2024-01-14",
                    "tags": ["green hydrogen", "renewable energy", "decarbonization", "clean tech"],
                    "engagement_score": 89,
                    "trend_relevance": 95
                },
                {
                    "title": "Regenerative Agriculture: Beyond Sustainability",
                    "summary": "How regenerative farming practices are not just sustaining but actively improving soil health, biodiversity, and carbon sequestration.",
                    "content": "Regenerative agriculture represents a paradigm shift from conventional farming methods, focusing on rebuilding soil organic matter and restoring degraded soil biodiversity...",
                    "category": "Agriculture",
                    "author": "LensIQ AI",
                    "created_at": "2024-01-13",
                    "tags": ["regenerative agriculture", "soil health", "carbon sequestration", "biodiversity"],
                    "engagement_score": 85,
                    "trend_relevance": 82
                },
                {
                    "title": "Carbon Credits: Market Evolution and Impact",
                    "summary": "Analyzing the rapid evolution of carbon credit markets and their role in achieving global climate targets.",
                    "content": "The carbon credit market has experienced unprecedented growth, evolving from a niche environmental tool to a mainstream financial instrument...",
                    "category": "Carbon Markets",
                    "author": "LensIQ AI",
                    "created_at": "2024-01-12",
                    "tags": ["carbon credits", "climate finance", "carbon markets", "net zero"],
                    "engagement_score": 87,
                    "trend_relevance": 90
                },
                {
                    "title": "Biodegradable Packaging Innovation",
                    "summary": "The breakthrough innovations in biodegradable packaging that are transforming the consumer goods industry.",
                    "content": "The packaging industry is experiencing a revolution as companies develop innovative biodegradable materials that maintain product integrity while minimizing environmental impact...",
                    "category": "Packaging",
                    "author": "LensIQ AI",
                    "created_at": "2024-01-11",
                    "tags": ["biodegradable packaging", "sustainable materials", "consumer goods", "waste reduction"],
                    "engagement_score": 83,
                    "trend_relevance": 78
                }
            ]
            database_service.insert_many('stories', sample_stories)
            stories = sample_stories
            
        return stories
    
    def _get_insights(self) -> List[Dict]:
        """Get insights data from database."""
        insights = database_service.find(
            'insights', 
            sort=[('relevance_score', -1)],
            limit=10
        )
        
        # If no data in database, insert sample data
        if not insights:
            logger.info("No insights found in database, inserting sample data...")
            sample_insights = [
                {
                    "title": "Circular Economy Adoption Accelerating",
                    "description": "Companies implementing circular economy principles are seeing 23% higher profitability compared to traditional linear models.",
                    "category": "Market Intelligence",
                    "relevance_score": 95,
                    "confidence": 88,
                    "data_sources": ["Industry Reports", "Financial Analysis", "Company Filings"],
                    "created_at": "2024-01-15",
                    "impact_level": "High"
                },
                {
                    "title": "Green Hydrogen Investment Surge",
                    "description": "Global investment in green hydrogen projects increased by 180% in 2023, with $45B committed to new projects.",
                    "category": "Investment Trends",
                    "relevance_score": 92,
                    "confidence": 91,
                    "data_sources": ["Investment Databases", "Government Reports", "Industry Analysis"],
                    "created_at": "2024-01-14",
                    "impact_level": "High"
                },
                {
                    "title": "Regenerative Agriculture Scaling",
                    "description": "Regenerative agriculture practices are being adopted across 15M hectares globally, with 35% yield improvements reported.",
                    "category": "Agricultural Innovation",
                    "relevance_score": 89,
                    "confidence": 85,
                    "data_sources": ["Agricultural Studies", "Satellite Data", "Farm Reports"],
                    "created_at": "2024-01-13",
                    "impact_level": "Medium"
                },
                {
                    "title": "Carbon Credit Market Maturation",
                    "description": "Voluntary carbon markets reached $2B in 2023, with improved verification standards driving quality improvements.",
                    "category": "Carbon Markets",
                    "relevance_score": 87,
                    "confidence": 89,
                    "data_sources": ["Market Data", "Registry Reports", "Verification Bodies"],
                    "created_at": "2024-01-12",
                    "impact_level": "High"
                },
                {
                    "title": "Biodegradable Packaging Breakthrough",
                    "description": "New bio-based packaging materials show 90% decomposition within 6 months while maintaining product protection.",
                    "category": "Material Science",
                    "relevance_score": 84,
                    "confidence": 82,
                    "data_sources": ["Research Papers", "Lab Studies", "Industry Tests"],
                    "created_at": "2024-01-11",
                    "impact_level": "Medium"
                }
            ]
            database_service.insert_many('insights', sample_insights)
            insights = sample_insights
            
        return insights
    
    def _get_narratives(self) -> List[Dict]:
        """Get narratives data from database."""
        narratives = database_service.find(
            'narratives', 
            sort=[('impact_score', -1)],
            limit=10
        )
        
        # If no data in database, insert sample data
        if not narratives:
            logger.info("No narratives found in database, inserting sample data...")
            sample_narratives = [
                {
                    "title": "The Circular Economy Transformation",
                    "narrative": "We are witnessing a fundamental shift from linear to circular business models across industries. This transformation is driven by resource scarcity, regulatory pressure, and consumer demand for sustainable products.",
                    "key_trends": ["Circular Design", "Waste-to-Resource", "Product-as-a-Service"],
                    "impact_score": 94,
                    "time_horizon": "2024-2027",
                    "sectors": ["Manufacturing", "Consumer Goods", "Technology"],
                    "created_at": "2024-01-15"
                },
                {
                    "title": "The Green Hydrogen Economy",
                    "narrative": "Green hydrogen is emerging as the missing link in the clean energy transition, enabling decarbonization of hard-to-abate sectors like steel, cement, and shipping.",
                    "key_trends": ["Electrolyzer Scale-up", "Hydrogen Infrastructure", "Industrial Decarbonization"],
                    "impact_score": 91,
                    "time_horizon": "2024-2030",
                    "sectors": ["Energy", "Manufacturing", "Transportation"],
                    "created_at": "2024-01-14"
                },
                {
                    "title": "Regenerative Systems Thinking",
                    "narrative": "Beyond sustainability, regenerative approaches are gaining traction as businesses recognize the need to actively restore and enhance natural and social systems.",
                    "key_trends": ["Regenerative Agriculture", "Nature-based Solutions", "Ecosystem Restoration"],
                    "impact_score": 88,
                    "time_horizon": "2024-2028",
                    "sectors": ["Agriculture", "Real Estate", "Finance"],
                    "created_at": "2024-01-13"
                },
                {
                    "title": "Climate Finance Evolution",
                    "narrative": "Climate finance is evolving from niche impact investing to mainstream financial markets, with new instruments and standards driving capital allocation toward sustainable solutions.",
                    "key_trends": ["Green Bonds", "Carbon Markets", "Climate Risk Assessment"],
                    "impact_score": 86,
                    "time_horizon": "2024-2026",
                    "sectors": ["Financial Services", "Insurance", "Investment"],
                    "created_at": "2024-01-12"
                },
                {
                    "title": "Sustainable Materials Revolution",
                    "narrative": "A materials revolution is underway as companies develop bio-based, recyclable, and biodegradable alternatives to traditional materials, reshaping supply chains and product design.",
                    "key_trends": ["Bio-based Materials", "Recyclable Design", "Material Traceability"],
                    "impact_score": 83,
                    "time_horizon": "2024-2029",
                    "sectors": ["Packaging", "Textiles", "Construction"],
                    "created_at": "2024-01-11"
                }
            ]
            database_service.insert_many('narratives', sample_narratives)
            narratives = sample_narratives
            
        return narratives
    
    def _get_trending_data(self) -> List[Dict]:
        """Get trending data for storytelling context."""
        trends = database_service.find(
            'trends', 
            sort=[('score', -1)],
            limit=5
        )
        
        # If no data, return sample trends
        if not trends:
            trends = [
                {"category": "Circular Economy", "score": 92, "growth": 24},
                {"category": "Green Hydrogen", "score": 89, "growth": 35},
                {"category": "Regenerative Agriculture", "score": 85, "growth": 18},
                {"category": "Carbon Credits", "score": 83, "growth": 42},
                {"category": "Biodegradable Packaging", "score": 80, "growth": 28}
            ]
            
        return trends
    
    def _generate_story(self, topic: str) -> Dict:
        """Generate a new story based on topic (placeholder implementation)."""
        return {
            "title": f"AI-Generated Story: {topic}",
            "summary": f"An AI-generated analysis of {topic} and its implications for sustainability.",
            "content": f"This is a placeholder story about {topic}. In a full implementation, this would use AI to generate comprehensive content.",
            "category": "AI Generated",
            "author": "LensIQ AI",
            "created_at": "2024-01-15",
            "tags": [topic.lower().replace(" ", "_"), "ai_generated", "sustainability"],
            "engagement_score": 75,
            "trend_relevance": 80
        }

# Create instance
lensiq_route = LensIQRoute()
lensiq_bp = lensiq_route.blueprint
