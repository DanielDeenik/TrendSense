"""
Graph Analytics Routes for SustainaTrend™

This module provides routes for graph-based visualizations and analytics,
including the Venture Signal Graph with Life Cycle Analysis.
"""

import logging
from typing import Dict, List, Any, Optional
from flask import Blueprint, request, jsonify, render_template, current_app
from flask.views import MethodView

# Import services
from src.backend.services.venture_signal_graph import VentureSignalGraph
from src.database.graph_manager import mongodb_graph_manager

# Configure logging
logger = logging.getLogger(__name__)

class GraphAnalyticsRoute(MethodView):
    """
    Class-based route handler for Graph Analytics functionality.
    """
    
    def __init__(self):
        """Initialize the Graph Analytics route handler."""
        self.blueprint = Blueprint('graph_analytics', __name__, url_prefix='/graph-analytics')
        self.venture_signal_template = 'fin_graph_analytics/fin_venture_signal_graph.html'
        self.network_template = 'fin_graph_analytics/fin_network_graph.html'
        self.supply_chain_template = 'fin_graph_analytics/fin_supply_chain_graph.html'
        self.impact_template = 'fin_graph_analytics/fin_impact_graph.html'
        
        # Initialize services
        self.venture_signal_service = VentureSignalGraph()
        
        # Register routes
        self.register_routes()
    
    def register_routes(self):
        """Register all routes for the Graph Analytics blueprint."""
        
        # Main dashboard route
        @self.blueprint.route('/')
        def index():
            """Render the Graph Analytics dashboard."""
            return render_template(
                'fin_graph_analytics/fin_graph_dashboard.html',
                active_nav='graph_analytics'
            )
        
        # Venture Signal Graph route
        @self.blueprint.route('/venture-signal')
        def venture_signal():
            """Render the Venture Signal Graph page."""
            return render_template(
                self.venture_signal_template,
                active_nav='graph_analytics',
                sub_nav='venture_signal',
                prompt_template=self.venture_signal_service.get_prompt_template()
            )
        
        # Network Graph route
        @self.blueprint.route('/network')
        def network():
            """Render the Network Graph page."""
            return render_template(
                self.network_template,
                active_nav='graph_analytics',
                sub_nav='network'
            )
        
        # Supply Chain Graph route
        @self.blueprint.route('/supply-chain')
        def supply_chain():
            """Render the Supply Chain Graph page."""
            return render_template(
                self.supply_chain_template,
                active_nav='graph_analytics',
                sub_nav='supply_chain'
            )
        
        # Impact Graph route
        @self.blueprint.route('/impact')
        def impact():
            """Render the Impact Graph page."""
            return render_template(
                self.impact_template,
                active_nav='graph_analytics',
                sub_nav='impact'
            )
        
        # API Routes
        
        # Venture Signal Graph API
        @self.blueprint.route('/api/venture-signal/analyze', methods=['POST'])
        def analyze_venture_signal():
            """
            API endpoint to analyze company data and generate the Venture Signal Graph.
            
            Expected JSON payload:
            {
                "companies": [
                    {
                        "id": "company1",
                        "name": "GreenTechX",
                        "sector": "CleanTech",
                        "influencers": ["@climateleader", "@greentechfounder"],
                        "sentiment": "Positive"
                    },
                    ...
                ],
                "trends": [
                    {
                        "id": "trend1",
                        "name": "Climate Action",
                        "category": "Environmental"
                    },
                    ...
                ],
                "relationships": [
                    {
                        "source": "trend1",
                        "target": "company1",
                        "type": "influences",
                        "strength": 0.8
                    },
                    ...
                ],
                "lca_data": {
                    "company1": {
                        "carbon_footprint": "Low",
                        "resource_efficiency": "Good",
                        "circularity_potential": "High",
                        "csrd_ready": True,
                        "sfdr_ready": False
                    },
                    ...
                }
            }
            """
            try:
                data = request.get_json()
                
                if not data:
                    return jsonify({"error": "No data provided"}), 400
                
                # Extract data from request
                companies = data.get('companies', [])
                trends = data.get('trends', [])
                relationships = data.get('relationships', [])
                lca_data = data.get('lca_data', {})
                
                # Load data into service
                self.venture_signal_service.load_data(companies, trends, relationships, lca_data)
                
                # Generate analysis
                graph_data = self.venture_signal_service.get_graph_data()
                social_signals = self.venture_signal_service.analyze_social_signals()
                life_cycle_impacts = self.venture_signal_service.analyze_life_cycle_impacts()
                investor_summaries = self.venture_signal_service.generate_investor_summaries()
                
                # Return results
                return jsonify({
                    "graph_data": graph_data,
                    "social_signals": social_signals,
                    "life_cycle_impacts": life_cycle_impacts,
                    "investor_summaries": investor_summaries
                })
                
            except Exception as e:
                logger.exception("Error analyzing venture signal graph data")
                return jsonify({"error": str(e)}), 500
        
        @self.blueprint.route('/api/venture-signal/prompt-template')
        def get_prompt_template():
            """Get the GPT-4.1 prompt template for Venture Signal Graph analysis."""
            return jsonify({
                "template": self.venture_signal_service.get_prompt_template()
            })
        
        @self.blueprint.route('/api/venture-signal/sample-data')
        def get_venture_signal_sample_data():
            """Get sample data for Venture Signal Graph demonstration."""
            sample_data = {
                "companies": [
                    {
                        "id": "company1",
                        "name": "GreenTechX",
                        "sector": "CleanTech",
                        "influencers": ["@climateleader", "@greentechfounder"],
                        "sentiment": "Positive"
                    },
                    {
                        "id": "company2",
                        "name": "EthicsAI",
                        "sector": "AI",
                        "influencers": ["@aiethicist", "@techforgood"],
                        "sentiment": "Neutral"
                    },
                    {
                        "id": "company3",
                        "name": "CircularCo",
                        "sector": "Manufacturing",
                        "influencers": ["@zerowaste", "@circulareconomy"],
                        "sentiment": "Positive"
                    },
                    {
                        "id": "company4",
                        "name": "TrustAI",
                        "sector": "AI",
                        "influencers": ["@responsibleai", "@ethicaltech"],
                        "sentiment": "Positive"
                    },
                    {
                        "id": "company5",
                        "name": "ReCircle",
                        "sector": "Waste Management",
                        "influencers": ["@recycling", "@wastetech"],
                        "sentiment": "Positive"
                    }
                ],
                "trends": [
                    {
                        "id": "trend1",
                        "name": "Climate Action",
                        "category": "Environmental"
                    },
                    {
                        "id": "trend2",
                        "name": "AI Ethics",
                        "category": "Technology"
                    },
                    {
                        "id": "trend3",
                        "name": "Circular Economy",
                        "category": "Environmental"
                    }
                ],
                "relationships": [
                    {
                        "source": "trend1",
                        "target": "company1",
                        "type": "influences",
                        "strength": 0.8
                    },
                    {
                        "source": "trend3",
                        "target": "company1",
                        "type": "influences",
                        "strength": 0.6
                    },
                    {
                        "source": "trend2",
                        "target": "company2",
                        "type": "influences",
                        "strength": 0.9
                    },
                    {
                        "source": "trend3",
                        "target": "company3",
                        "type": "influences",
                        "strength": 0.9
                    },
                    {
                        "source": "trend2",
                        "target": "company4",
                        "type": "influences",
                        "strength": 0.7
                    },
                    {
                        "source": "trend3",
                        "target": "company5",
                        "type": "influences",
                        "strength": 0.8
                    },
                    {
                        "source": "company1",
                        "target": "company3",
                        "type": "collaborates",
                        "strength": 0.7
                    },
                    {
                        "source": "company1",
                        "target": "company5",
                        "type": "collaborates",
                        "strength": 0.6
                    },
                    {
                        "source": "company2",
                        "target": "company4",
                        "type": "competes",
                        "strength": 0.5
                    }
                ],
                "lca_data": {
                    "company1": {
                        "carbon_footprint": "Low",
                        "resource_efficiency": "Good",
                        "circularity_potential": "High",
                        "csrd_ready": True,
                        "sfdr_ready": False
                    },
                    "company2": {
                        "carbon_footprint": "High",
                        "resource_efficiency": "Poor",
                        "circularity_potential": "Low",
                        "csrd_ready": False,
                        "sfdr_ready": False
                    },
                    "company3": {
                        "carbon_footprint": "Medium",
                        "resource_efficiency": "Good",
                        "circularity_potential": "High",
                        "csrd_ready": True,
                        "sfdr_ready": True
                    },
                    "company4": {
                        "carbon_footprint": "Medium",
                        "resource_efficiency": "Moderate",
                        "circularity_potential": "Medium",
                        "csrd_ready": False,
                        "sfdr_ready": False
                    },
                    "company5": {
                        "carbon_footprint": "Low",
                        "resource_efficiency": "Good",
                        "circularity_potential": "High",
                        "csrd_ready": True,
                        "sfdr_ready": True
                    }
                }
            }
            
            return jsonify(sample_data)
        
        # Network Graph API
        @self.blueprint.route('/api/network/graph-data')
        def get_network_graph_data():
            """Get network graph data."""
            try:
                # Get graph data from MongoDB
                nodes = list(mongodb_graph_manager.mongodb.find('graph_nodes', {}))
                edges = list(mongodb_graph_manager.mongodb.find('graph_edges', {}))
                
                # Format for visualization
                for node in nodes:
                    node['id'] = node.pop('_id', node.get('id', f"node_{nodes.index(node)}"))
                
                for edge in edges:
                    edge['id'] = edge.pop('_id', edge.get('id', f"edge_{edges.index(edge)}"))
                    edge['source'] = edge.get('source_id', edge.get('source', ''))
                    edge['target'] = edge.get('target_id', edge.get('target', ''))
                
                return jsonify({
                    "nodes": nodes,
                    "links": edges
                })
            except Exception as e:
                logger.exception("Error getting network graph data")
                return jsonify({"error": str(e)}), 500
        
        # Supply Chain Graph API
        @self.blueprint.route('/api/supply-chain/<company_id>')
        def get_supply_chain_graph(company_id):
            """Get supply chain graph data for a company."""
            try:
                max_depth = request.args.get('max_depth', default=3, type=int)
                graph_data = mongodb_graph_manager.supply_chain_graph(company_id, max_depth)
                return jsonify(graph_data)
            except Exception as e:
                logger.exception(f"Error getting supply chain graph for {company_id}")
                return jsonify({"error": str(e)}), 500
        
        # Impact Graph API
        @self.blueprint.route('/api/impact/<company_id>')
        def get_impact_graph(company_id):
            """Get impact graph data for a company."""
            try:
                graph_data = mongodb_graph_manager.initiative_impact_graph(company_id)
                return jsonify(graph_data)
            except Exception as e:
                logger.exception(f"Error getting impact graph for {company_id}")
                return jsonify({"error": str(e)}), 500

# Create blueprint instance
graph_analytics_bp = GraphAnalyticsRoute().blueprint
