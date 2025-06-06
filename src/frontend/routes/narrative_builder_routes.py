"""
Narrative Builder Routes for LensIQ

Routes for the Narrative Builder functionality that creates compelling stories
for investors, clients, and staff based on data analysis and trends.
"""

import logging
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from typing import Dict, List, Any, Optional

from .base_route import BaseRoute
from src.narrative_builder.narrative_engine import NarrativeEngine
from src.database.database_service import database_service

logger = logging.getLogger(__name__)

class NarrativeBuilderRoute(BaseRoute):
    """Narrative Builder route handler."""
    
    def __init__(self):
        """Initialize the Narrative Builder route."""
        super().__init__(name='narrative_builder')
        self.blueprint = Blueprint('narrative_builder', __name__)
        self.narrative_engine = NarrativeEngine()
        self.register_routes()
        
    def register_routes(self):
        """Register all routes for the Narrative Builder blueprint."""
        
        @self.blueprint.route('/')
        @self.handle_errors
        def index():
            """Narrative Builder dashboard."""
            # Initialize database connection
            if not database_service.is_connected():
                logger.info("Connecting to database...")
                database_service.connect()
            
            # Get recent narratives
            recent_narratives = self._get_recent_narratives()
            
            # Get narrative statistics
            stats = self._get_narrative_statistics()
            
            context = {
                'active_nav': 'narrative_builder',
                'page_title': "LensIQ Narrative Builder",
                'recent_narratives': recent_narratives,
                'stats': stats,
                'database_available': database_service.is_connected()
            }
            
            return self.render_template('narrative_builder/dashboard.html', **context)
        
        @self.blueprint.route('/create')
        @self.handle_errors
        def create_narrative():
            """Create new narrative form."""
            context = {
                'active_nav': 'narrative_builder',
                'sub_nav': 'create',
                'page_title': "Create New Narrative"
            }
            
            return self.render_template('narrative_builder/create.html', **context)
        
        @self.blueprint.route('/generate', methods=['POST'])
        @self.handle_errors
        def generate_narrative():
            """Generate new narrative based on form data."""
            try:
                # Get form data
                data = request.json or request.form.to_dict()
                company_id = data.get('company_id')
                audience_focus = data.get('audience_focus')
                custom_context = data.get('custom_context', {})
                
                logger.info(f"Generating narrative for company: {company_id}, audience: {audience_focus}")
                
                # Generate narrative
                if audience_focus and audience_focus != 'all':
                    narrative = self.narrative_engine.generate_audience_specific_narrative(
                        audience_focus, company_id, custom_context
                    )
                else:
                    narrative = self.narrative_engine.generate_complete_narrative(
                        company_id, audience_focus, custom_context
                    )
                
                # Return JSON response for AJAX requests
                if request.is_json:
                    return self.json_response({
                        'success': True,
                        'narrative_id': narrative.get('narrative_id'),
                        'message': 'Narrative generated successfully'
                    })
                
                # Redirect to view narrative
                return redirect(url_for('narrative_builder.view_narrative', 
                                      narrative_id=narrative.get('narrative_id')))
                
            except Exception as e:
                logger.error(f"Error generating narrative: {str(e)}")
                if request.is_json:
                    return self.json_response({'success': False, 'error': str(e)}, 500)
                return redirect(url_for('narrative_builder.create_narrative'))
        
        @self.blueprint.route('/narrative/<narrative_id>')
        @self.handle_errors
        def view_narrative(narrative_id):
            """View specific narrative."""
            try:
                # Load narrative from database
                narrative = database_service.find_one('narratives', {'narrative_id': narrative_id})
                
                if not narrative:
                    return self.render_template('narrative_builder/not_found.html'), 404
                
                # Get narrative insights
                insights = self.narrative_engine.get_narrative_insights(narrative_id)
                
                context = {
                    'active_nav': 'narrative_builder',
                    'sub_nav': 'view',
                    'page_title': f"Narrative: {narrative_id}",
                    'narrative': narrative,
                    'insights': insights
                }
                
                return self.render_template('narrative_builder/view.html', **context)
                
            except Exception as e:
                logger.error(f"Error viewing narrative: {str(e)}")
                return self.render_template('narrative_builder/error.html', error=str(e)), 500
        
        @self.blueprint.route('/narrative/<narrative_id>/audience/<audience>')
        @self.handle_errors
        def view_audience_narrative(narrative_id, audience):
            """View audience-specific narrative."""
            try:
                # Load complete narrative
                complete_narrative = database_service.find_one('narratives', {'narrative_id': narrative_id})
                
                if not complete_narrative:
                    return self.render_template('narrative_builder/not_found.html'), 404
                
                # Extract audience-specific content
                audience_narrative = self.narrative_engine._extract_audience_narrative(
                    complete_narrative, audience
                )
                
                # Enhance for audience
                enhanced_narrative = self.narrative_engine._enhance_audience_narrative(
                    audience_narrative, audience
                )
                
                context = {
                    'active_nav': 'narrative_builder',
                    'sub_nav': 'audience',
                    'page_title': f"{audience.title()} Narrative",
                    'narrative': enhanced_narrative,
                    'audience': audience
                }
                
                return self.render_template('narrative_builder/audience_view.html', **context)
                
            except Exception as e:
                logger.error(f"Error viewing audience narrative: {str(e)}")
                return self.render_template('narrative_builder/error.html', error=str(e)), 500
        
        @self.blueprint.route('/narratives')
        @self.handle_errors
        def list_narratives():
            """List all narratives."""
            try:
                # Get all narratives
                narratives = database_service.find('narratives', sort=[('generation_timestamp', -1)])
                
                context = {
                    'active_nav': 'narrative_builder',
                    'sub_nav': 'list',
                    'page_title': "All Narratives",
                    'narratives': narratives
                }
                
                return self.render_template('narrative_builder/list.html', **context)
                
            except Exception as e:
                logger.error(f"Error listing narratives: {str(e)}")
                return self.render_template('narrative_builder/error.html', error=str(e)), 500
        
        @self.blueprint.route('/api/generate', methods=['POST'])
        @self.handle_errors
        def api_generate_narrative():
            """API endpoint to generate narrative."""
            try:
                data = request.json or {}
                company_id = data.get('company_id')
                audience_focus = data.get('audience_focus')
                custom_context = data.get('custom_context', {})
                
                # Generate narrative
                if audience_focus and audience_focus != 'all':
                    narrative = self.narrative_engine.generate_audience_specific_narrative(
                        audience_focus, company_id, custom_context
                    )
                else:
                    narrative = self.narrative_engine.generate_complete_narrative(
                        company_id, audience_focus, custom_context
                    )
                
                return self.json_response({
                    'success': True,
                    'narrative': narrative,
                    'narrative_id': narrative.get('narrative_id')
                })
                
            except Exception as e:
                logger.error(f"API error generating narrative: {str(e)}")
                return self.json_response({'success': False, 'error': str(e)}, 500)
        
        @self.blueprint.route('/api/narrative/<narrative_id>')
        @self.handle_errors
        def api_get_narrative(narrative_id):
            """API endpoint to get narrative."""
            try:
                narrative = database_service.find_one('narratives', {'narrative_id': narrative_id})
                
                if not narrative:
                    return self.json_response({'error': 'Narrative not found'}, 404)
                
                return self.json_response(narrative)
                
            except Exception as e:
                logger.error(f"API error getting narrative: {str(e)}")
                return self.json_response({'error': str(e)}, 500)
        
        @self.blueprint.route('/api/narrative/<narrative_id>/export/<format_type>')
        @self.handle_errors
        def api_export_narrative(narrative_id, format_type):
            """API endpoint to export narrative."""
            try:
                audience = request.args.get('audience')
                
                exported = self.narrative_engine.export_narrative(
                    format_type, audience, narrative_id
                )
                
                if format_type == 'json':
                    return self.json_response({'exported_data': exported})
                else:
                    return exported
                
            except Exception as e:
                logger.error(f"API error exporting narrative: {str(e)}")
                return self.json_response({'error': str(e)}, 500)
        
        @self.blueprint.route('/api/insights/<narrative_id>')
        @self.handle_errors
        def api_get_insights(narrative_id):
            """API endpoint to get narrative insights."""
            try:
                insights = self.narrative_engine.get_narrative_insights(narrative_id)
                return self.json_response(insights)
                
            except Exception as e:
                logger.error(f"API error getting insights: {str(e)}")
                return self.json_response({'error': str(e)}, 500)
        
        @self.blueprint.route('/api/update/<narrative_id>', methods=['POST'])
        @self.handle_errors
        def api_update_narrative(narrative_id):
            """API endpoint to update narrative with new data."""
            try:
                new_data = request.json or {}
                
                updated_narrative = self.narrative_engine.update_narrative_with_new_data(
                    new_data, narrative_id
                )
                
                return self.json_response({
                    'success': True,
                    'narrative': updated_narrative
                })
                
            except Exception as e:
                logger.error(f"API error updating narrative: {str(e)}")
                return self.json_response({'success': False, 'error': str(e)}, 500)
    
    def _get_recent_narratives(self) -> List[Dict[str, Any]]:
        """Get recent narratives for dashboard."""
        try:
            narratives = database_service.find(
                'narratives',
                sort=[('generation_timestamp', -1)],
                limit=5
            )
            
            # If no narratives, create sample data
            if not narratives:
                sample_narratives = [
                    {
                        'narrative_id': 'sample_001',
                        'generation_timestamp': '2024-01-15T10:00:00',
                        'company_id': 'demo_company',
                        'metadata': {
                            'story_quality_score': 0.85,
                            'total_insights': 12,
                            'narrative_themes': ['growth_story', 'sustainability_leadership', 'innovation_excellence']
                        },
                        'executive_summary': {
                            'overview': 'Strong performance across all metrics with compelling growth story'
                        }
                    },
                    {
                        'narrative_id': 'sample_002',
                        'generation_timestamp': '2024-01-14T15:30:00',
                        'company_id': 'demo_company',
                        'metadata': {
                            'story_quality_score': 0.78,
                            'total_insights': 9,
                            'narrative_themes': ['sustainability_leadership', 'market_leadership', 'brand_strength']
                        },
                        'executive_summary': {
                            'overview': 'Sustainability leadership driving market differentiation'
                        }
                    }
                ]
                narratives = sample_narratives
            
            return narratives
            
        except Exception as e:
            logger.error(f"Error getting recent narratives: {str(e)}")
            return []
    
    def _get_narrative_statistics(self) -> Dict[str, Any]:
        """Get narrative statistics for dashboard."""
        try:
            # Get total count
            total_narratives = len(database_service.find('narratives'))
            
            # Calculate average quality score
            narratives = database_service.find('narratives')
            if narratives:
                quality_scores = [
                    n.get('metadata', {}).get('story_quality_score', 0) 
                    for n in narratives
                ]
                avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
            else:
                avg_quality = 0.82  # Sample value
                total_narratives = 2  # Sample value
            
            return {
                'total_narratives': total_narratives,
                'average_quality_score': avg_quality,
                'narratives_this_month': total_narratives,  # Simplified
                'top_themes': ['growth_story', 'sustainability_leadership', 'innovation_excellence']
            }
            
        except Exception as e:
            logger.error(f"Error getting narrative statistics: {str(e)}")
            return {
                'total_narratives': 0,
                'average_quality_score': 0,
                'narratives_this_month': 0,
                'top_themes': []
            }

# Create instance
narrative_builder_route = NarrativeBuilderRoute()
narrative_builder_bp = narrative_builder_route.blueprint
