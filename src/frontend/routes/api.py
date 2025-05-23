"""
API Routes for TrendSense

This module provides API endpoints for the TrendSense application.
These endpoints serve data from the Firebase database and provide AI-generated insights.
"""

import logging
import json
from flask import Blueprint, jsonify, request
from src.database.adapters import get_database_adapter
from src.data_management.ai_connector import get_ai_connector

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
api_bp = Blueprint('api', __name__)

# Get database adapter
db_adapter = get_database_adapter()

@api_bp.route('/health')
def health_check():
    """API health check endpoint."""
    return jsonify({
        'status': 'ok',
        'database': 'connected' if db_adapter.is_connected() else 'disconnected'
    })

@api_bp.route('/vc-lens/data')
def vc_lens_data():
    """Get VC Lens data for visualizations."""
    try:
        # Connect to database if not already connected
        if not db_adapter.is_connected():
            db_adapter.connect()

        # Get VC Lens data from database
        data = db_adapter.find_one('vc_lens_data')

        if not data:
            logger.warning("No VC Lens data found in database, using sample data")
            # Use the sample data provided by the user
            data = {
                "_id": "01c9304f-a8e5-49fa-aab9-b9b143fde02c",
                "created_at": "Sun, 04 May 2025 09:00:54 GMT",
                "microtrends_data": {
                    "Biodegradable Packaging": [12.4, 12.4, 13.8, 14.9, 14.9, 11.6, 16.7, 17.7, 10.8, 14.6, 16.8, 9.2],
                    "Carbon Credits": [27.2, 27.1, 28.4, 29.1, 28.0, 28.0, 29.9, 29.0, 25.8, 26.9, 27.6, 33.0],
                    "Green Hydrogen": [20.9, 21.3, 21.2, 21.7, 24.2, 24.2, 24.8, 25.7, 22.9, 18.5, 17.4, 20.2],
                    "Regenerative Agriculture": [15.2, 15.1, 16.5, 16.6, 15.5, 13.1, 14.2, 15.8, 12.7, 13.5, 17.7, 21.0]
                },
                "sankey_data": {
                    "links": [
                        {"source": 0, "target": 1, "value": 50},
                        {"source": 0, "target": 2, "value": 30},
                        {"source": 0, "target": 3, "value": 20},
                        {"source": 1, "target": 4, "value": 30},
                        {"source": 1, "target": 5, "value": 20},
                        {"source": 2, "target": 5, "value": 20},
                        {"source": 2, "target": 6, "value": 10},
                        {"source": 3, "target": 6, "value": 20},
                        {"source": 4, "target": 7, "value": 15},
                        {"source": 4, "target": 8, "value": 15},
                        {"source": 5, "target": 9, "value": 20},
                        {"source": 5, "target": 10, "value": 20},
                        {"source": 6, "target": 11, "value": 30}
                    ],
                    "nodes": [
                        {"name": "LP Capital"},
                        {"name": "Fund A"},
                        {"name": "Fund B"},
                        {"name": "Fund C"},
                        {"name": "Climate Tech"},
                        {"name": "Clean Energy"},
                        {"name": "Sustainable Ag"},
                        {"name": "Company 1"},
                        {"name": "Company 2"},
                        {"name": "Company 3"},
                        {"name": "Company 4"},
                        {"name": "Company 5"}
                    ]
                },
                "trend_line_data": {
                    "Biodiversity": [
                        {"date": "2024-06-01T09:00:49.812539", "value": 63.5},
                        {"date": "2024-07-01T09:00:49.812539", "value": 63.4},
                        {"date": "2024-08-01T09:00:49.812539", "value": 64.6},
                        {"date": "2024-09-01T09:00:49.812539", "value": 64.0},
                        {"date": "2024-10-01T09:00:49.812539", "value": 64.4},
                        {"date": "2024-11-01T09:00:49.812539", "value": 63.8},
                        {"date": "2024-12-01T09:00:49.812539", "value": 71.6},
                        {"date": "2025-01-01T09:00:49.812539", "value": 71.2},
                        {"date": "2025-02-01T09:00:49.812539", "value": 62.5},
                        {"date": "2025-03-01T09:00:49.812539", "value": 66.1},
                        {"date": "2025-04-01T09:00:49.812539", "value": 66.5},
                        {"date": "2025-05-01T09:00:49.812539", "value": 60.7}
                    ],
                    "Circular Economy": [
                        {"date": "2024-06-01T09:00:49.812539", "value": 69.8},
                        {"date": "2024-07-01T09:00:49.812539", "value": 70.6},
                        {"date": "2024-08-01T09:00:49.812539", "value": 70.5},
                        {"date": "2024-09-01T09:00:49.812539", "value": 71.0},
                        {"date": "2024-10-01T09:00:49.812539", "value": 71.4},
                        {"date": "2024-11-01T09:00:49.812539", "value": 71.7},
                        {"date": "2024-12-01T09:00:49.812539", "value": 67.2},
                        {"date": "2025-01-01T09:00:49.812539", "value": 73.5},
                        {"date": "2025-02-01T09:00:49.812539", "value": 69.1},
                        {"date": "2025-03-01T09:00:49.812539", "value": 81.2},
                        {"date": "2025-04-01T09:00:49.812539", "value": 83.2},
                        {"date": "2025-05-01T09:00:49.812539", "value": 68.7}
                    ],
                    "Climate Tech": [
                        {"date": "2024-06-01T09:00:49.812539", "value": 62.3},
                        {"date": "2024-07-01T09:00:49.812539", "value": 63.4},
                        {"date": "2024-08-01T09:00:49.812539", "value": 63.8},
                        {"date": "2024-09-01T09:00:49.812539", "value": 65.3},
                        {"date": "2024-10-01T09:00:49.812539", "value": 67.7},
                        {"date": "2024-11-01T09:00:49.812539", "value": 62.8},
                        {"date": "2024-12-01T09:00:49.812539", "value": 60.3},
                        {"date": "2025-01-01T09:00:49.812539", "value": 64.2},
                        {"date": "2025-02-01T09:00:49.812539", "value": 71.4},
                        {"date": "2025-03-01T09:00:49.812539", "value": 71.2},
                        {"date": "2025-04-01T09:00:49.812539", "value": 73.0},
                        {"date": "2025-05-01T09:00:49.812539", "value": 62.8}
                    ],
                    "ESG Integration": [
                        {"date": "2024-06-01T09:00:49.811534", "value": 69.1},
                        {"date": "2024-07-01T09:00:49.811534", "value": 68.9},
                        {"date": "2024-08-01T09:00:49.811534", "value": 71.8},
                        {"date": "2024-09-01T09:00:49.811534", "value": 72.1},
                        {"date": "2024-10-01T09:00:49.811534", "value": 69.2},
                        {"date": "2024-11-01T09:00:49.811534", "value": 70.6},
                        {"date": "2024-12-01T09:00:49.811534", "value": 73.4},
                        {"date": "2025-01-01T09:00:49.811534", "value": 68.9},
                        {"date": "2025-02-01T09:00:49.811534", "value": 75.6},
                        {"date": "2025-03-01T09:00:49.811534", "value": 65.8},
                        {"date": "2025-04-01T09:00:49.811534", "value": 74.0},
                        {"date": "2025-05-01T09:00:49.812539", "value": 67.2}
                    ],
                    "Sustainable Agriculture": [
                        {"date": "2024-06-01T09:00:49.812539", "value": 58.0},
                        {"date": "2024-07-01T09:00:49.812539", "value": 59.1},
                        {"date": "2024-08-01T09:00:49.812539", "value": 57.7},
                        {"date": "2024-09-01T09:00:49.812539", "value": 57.9},
                        {"date": "2024-10-01T09:00:49.812539", "value": 60.4},
                        {"date": "2024-11-01T09:00:49.812539", "value": 59.8},
                        {"date": "2024-12-01T09:00:49.812539", "value": 56.0},
                        {"date": "2025-01-01T09:00:49.812539", "value": 66.9},
                        {"date": "2025-02-01T09:00:49.812539", "value": 55.9},
                        {"date": "2025-03-01T09:00:49.812539", "value": 56.4},
                        {"date": "2025-04-01T09:00:49.812539", "value": 70.6},
                        {"date": "2025-05-01T09:00:49.812539", "value": 58.9}
                    ]
                },
                "trend_strength_data": {
                    "Biodiversity": {"average": 65.65, "current": 79.72},
                    "Circular Economy": {"average": 70.07, "current": 79.13},
                    "Climate Tech": {"average": 76.82, "current": 77.80},
                    "ESG Integration": {"average": 64.66, "current": 86.05},
                    "Sustainable Agriculture": {"average": 78.13, "current": 77.70}
                },
                "updated_at": "Sun, 04 May 2025 09:00:54 GMT"
            }

            # Save the sample data to the database for future use
            db_adapter.insert_one('vc_lens_data', data)

        # Ensure the data is a dictionary
        if not isinstance(data, dict):
            logger.warning(f"VC Lens data is not a dictionary: {type(data)}")
            data = {"error": "Invalid data format"}

        return jsonify(data)
    except Exception as e:
        logger.error(f"Error getting VC Lens data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/trend-radar/data')
def trend_radar_data():
    """Get Trend Radar data for visualizations."""
    try:
        # Connect to database if not already connected
        if not db_adapter.is_connected():
            db_adapter.connect()

        # Get Trend Radar data from database
        data = db_adapter.find_one('trend_radar_data')

        if not data:
            logger.warning("No Trend Radar data found in database, using sample data")
            # Sample data for TrendRadar
            data = {
                "trends": [
                    {
                        "name": "AI-Powered Due Diligence",
                        "category": "Due Diligence Tech",
                        "stage": "Act",
                        "impact_area": "Investment Process",
                        "description": "Using artificial intelligence to automate and enhance the due diligence process, enabling faster and more thorough evaluation of potential investments.",
                        "use_cases": [
                            "Automated financial statement analysis",
                            "Market sentiment analysis from unstructured data",
                            "Competitive landscape mapping"
                        ],
                        "tags": ["AI", "Machine Learning", "Due Diligence", "Automation"],
                        "source_docs": [
                            { "title": "McKinsey Report: AI in Private Equity", "url": "#" },
                            { "title": "Harvard Business Review: The Future of Due Diligence", "url": "#" }
                        ],
                        "score": 85
                    },
                    {
                        "name": "ESG Data Integration",
                        "category": "Sustainability & ESG",
                        "stage": "Prepare",
                        "impact_area": "Risk Management",
                        "description": "Incorporating environmental, social, and governance data into investment decision-making processes to better assess risks and opportunities.",
                        "use_cases": [
                            "Carbon footprint assessment of portfolio companies",
                            "Supply chain sustainability analysis",
                            "Regulatory compliance monitoring"
                        ],
                        "tags": ["ESG", "Sustainability", "Data Analytics", "Risk Management"],
                        "source_docs": [
                            { "title": "PwC: ESG Integration in Private Markets", "url": "#" },
                            { "title": "BlackRock: Sustainable Investing Report", "url": "#" }
                        ],
                        "score": 78
                    },
                    {
                        "name": "Digital LP Portals",
                        "category": "Fund Ops & LP Reporting",
                        "stage": "Act",
                        "impact_area": "Investor Relations",
                        "description": "Secure digital platforms that provide limited partners with real-time access to fund performance data, documents, and interactive analytics.",
                        "use_cases": [
                            "Real-time portfolio performance dashboards",
                            "Secure document sharing and e-signatures",
                            "Automated capital call and distribution notices"
                        ],
                        "tags": ["Investor Relations", "Digital Transformation", "Reporting", "Analytics"],
                        "source_docs": [
                            { "title": "Deloitte: Digital Transformation in PE", "url": "#" },
                            { "title": "EY: LP Expectations Survey", "url": "#" }
                        ],
                        "score": 92
                    },
                    {
                        "name": "Quantum Computing for Portfolio Optimization",
                        "category": "Deep Tech & Frontier Bets",
                        "stage": "Watch",
                        "impact_area": "Investment Strategy",
                        "description": "Leveraging quantum computing to solve complex portfolio optimization problems that are intractable for classical computers.",
                        "use_cases": [
                            "Multi-factor portfolio optimization",
                            "Risk-return scenario analysis at scale",
                            "Complex correlation analysis across asset classes"
                        ],
                        "tags": ["Quantum Computing", "Portfolio Management", "Advanced Analytics"],
                        "source_docs": [
                            { "title": "IBM: Quantum Computing in Finance", "url": "#" },
                            { "title": "Nature: Quantum Advantage in Portfolio Optimization", "url": "#" }
                        ],
                        "score": 65
                    }
                ],
                "categories": [
                    "Deal Flow & Sourcing",
                    "Due Diligence Tech",
                    "Portfolio Value Creation",
                    "Fund Ops & LP Reporting",
                    "Sustainability & ESG",
                    "Exit Intelligence",
                    "Market Sensing",
                    "Deep Tech & Frontier Bets"
                ],
                "stages": [
                    "Watch",
                    "Prepare",
                    "Act"
                ]
            }

            # Save the sample data to the database for future use
            db_adapter.insert_one('trend_radar_data', data)

        return jsonify(data)
    except Exception as e:
        logger.error(f"Error getting Trend Radar data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/chart-data')
def chart_data():
    """Get chart data for dashboard visualizations."""
    try:
        # Connect to database if not already connected
        if not db_adapter.is_connected():
            db_adapter.connect()

        # Get chart data from database
        data = db_adapter.find_one('chart_data')

        if not data:
            logger.warning("No chart data found in database")
            return jsonify({'error': 'No data found'}), 404

        return jsonify(data)
    except Exception as e:
        logger.error(f"Error getting chart data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/companies')
def companies():
    """Get companies data."""
    try:
        # Connect to database if not already connected
        if not db_adapter.is_connected():
            db_adapter.connect()

        # Get limit parameter from query string
        limit = request.args.get('limit', default=10, type=int)

        # Get companies from database
        companies_data = db_adapter.find('companies', limit=limit)

        if not companies_data:
            logger.warning("No companies found in database")
            return jsonify({'error': 'No data found'}), 404

        return jsonify(companies_data)
    except Exception as e:
        logger.error(f"Error getting companies data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/funds')
def funds():
    """Get funds data."""
    try:
        # Connect to database if not already connected
        if not db_adapter.is_connected():
            db_adapter.connect()

        # Get limit parameter from query string
        limit = request.args.get('limit', default=10, type=int)

        # Get funds from database
        funds_data = db_adapter.find('funds', limit=limit)

        if not funds_data:
            logger.warning("No funds found in database")
            return jsonify({'error': 'No data found'}), 404

        return jsonify(funds_data)
    except Exception as e:
        logger.error(f"Error getting funds data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/trends')
def trends():
    """Get trends data."""
    try:
        # Connect to database if not already connected
        if not db_adapter.is_connected():
            db_adapter.connect()

        # Get limit parameter from query string
        limit = request.args.get('limit', default=15, type=int)

        # Get trends from database
        trends_data = db_adapter.find('trends', limit=limit)

        if not trends_data:
            logger.warning("No trends found in database")
            return jsonify({'error': 'No data found'}), 404

        return jsonify(trends_data)
    except Exception as e:
        logger.error(f"Error getting trends data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/insights')
def insights():
    """Get insights data."""
    try:
        # Connect to database if not already connected
        if not db_adapter.is_connected():
            db_adapter.connect()

        # Get limit parameter from query string
        limit = request.args.get('limit', default=10, type=int)

        # Get insights from database
        insights_data = db_adapter.find('insights', limit=limit)

        if not insights_data:
            logger.warning("No insights found in database")
            return jsonify({'error': 'No data found'}), 404

        return jsonify(insights_data)
    except Exception as e:
        logger.error(f"Error getting insights data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/stories')
def stories():
    """Get stories data."""
    try:
        # Connect to database if not already connected
        if not db_adapter.is_connected():
            db_adapter.connect()

        # Get limit parameter from query string
        limit = request.args.get('limit', default=10, type=int)

        # Get stories from database
        stories_data = db_adapter.find('stories', limit=limit)

        if not stories_data:
            logger.warning("No stories found in database")
            return jsonify({'error': 'No data found'}), 404

        return jsonify(stories_data)
    except Exception as e:
        logger.error(f"Error getting stories data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/metrics')
def metrics():
    """Get metrics data."""
    try:
        # Connect to database if not already connected
        if not db_adapter.is_connected():
            db_adapter.connect()

        # Get limit parameter from query string
        limit = request.args.get('limit', default=20, type=int)

        # Get metrics from database
        metrics_data = db_adapter.find('metrics', limit=limit)

        if not metrics_data:
            logger.warning("No metrics found in database")
            return jsonify({'error': 'No data found'}), 404

        return jsonify(metrics_data)
    except Exception as e:
        logger.error(f"Error getting metrics data: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Sample trend data for fallback
SAMPLE_TREND_DATA = [
    {
        "category": "Renewable Energy",
        "growth": 24,
        "score": 85,
        "metrics": {
            "environmental_impact": 88,
            "market_potential": 82,
            "innovation_level": 76
        }
    },
    {
        "category": "Circular Economy",
        "growth": 32,
        "score": 78,
        "metrics": {
            "environmental_impact": 90,
            "market_potential": 75,
            "innovation_level": 80
        }
    },
    {
        "category": "Carbon Tech",
        "growth": 45,
        "score": 92,
        "metrics": {
            "environmental_impact": 95,
            "market_potential": 88,
            "innovation_level": 92
        }
    }
]

def get_ai_connector_with_fallback(preferred_type='perplexity'):
    """Get AI connector with fallback to mock if preferred is not available."""
    try:
        ai_connector = get_ai_connector(preferred_type)
        if not ai_connector.is_available():
            logger.warning(f"{preferred_type} not available, falling back to mock")
            ai_connector = get_ai_connector('mock')
    except Exception as e:
        logger.warning(f"Error getting {preferred_type} connector: {str(e)}")
        ai_connector = get_ai_connector('mock')

    return ai_connector

@api_bp.route('/generate-insights', methods=['POST'])
def generate_insights():
    """Generate insights using AI."""
    try:
        # Get request data
        data = request.json or {}
        target = data.get('target', 'market')

        # Get trend data
        trends_data = db_adapter.find('trends', limit=10) or SAMPLE_TREND_DATA

        # Format trend data for the AI prompt
        trend_summary = "\n".join([
            f"- {trend.get('category', 'Unknown')}: Score {trend.get('score', 0)}, Growth {trend.get('growth', 0)}%"
            for trend in trends_data
        ])

        # Create prompt for AI
        prompt = f"""
        Based on the following market trend data:

        {trend_summary}

        Generate 3-5 key insights about {target} trends. For each insight:
        1. Provide a concise headline
        2. Include supporting data points
        3. Suggest potential implications for investors

        Format the response as JSON with an array of insight objects, each containing:
        - headline: The main insight title
        - description: Supporting data and explanation
        - implications: What this means for investors

        Example format:
        {{
            "insights": [
                {{
                    "headline": "Insight Title",
                    "description": "Supporting data and explanation",
                    "implications": "What this means for investors"
                }}
            ]
        }}
        """

        # Get AI connector with fallback
        ai_connector = get_ai_connector_with_fallback('perplexity')

        # Generate insights
        system_prompt = "You are an expert market analyst specializing in trend analysis and investment insights."
        response = ai_connector.generate_text(prompt, {
            'system_prompt': system_prompt,
            'model': 'pplx-7b-online'  # or another appropriate model
        })

        logger.info(f"AI response: {response[:100]}...")

        # Try to parse response as JSON
        try:
            insights = json.loads(response)
            return jsonify(insights)
        except json.JSONDecodeError:
            # If response is not valid JSON, return as text
            logger.warning("AI response is not valid JSON, returning as text")
            return jsonify({
                'insights': [
                    {'headline': 'AI Generated Insight', 'description': response}
                ]
            })

    except Exception as e:
        logger.error(f"Error generating insights: {str(e)}")
        logger.exception("Exception details:")
        return jsonify({'error': str(e)}), 500
