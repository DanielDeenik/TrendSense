"""
Narrative Engine for LensIQ Narrative Builder

Main orchestrator that coordinates data collection, trend analysis, and story generation
to create compelling narratives for different audiences.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

from .data_collector import DataCollector
from .trend_analyzer import TrendAnalyzer
from .story_generator import StoryGenerator
from src.database.database_service import database_service

logger = logging.getLogger(__name__)


class NarrativeEngine:
    """Main engine that orchestrates the narrative building process."""
    
    def __init__(self):
        """Initialize the narrative engine."""
        self.data_collector = DataCollector()
        self.trend_analyzer = TrendAnalyzer()
        self.story_generator = StoryGenerator()
        self.database = database_service
        
        self.current_narrative = None
        self.narrative_history = []
    
    def generate_complete_narrative(self, 
                                  company_id: Optional[str] = None,
                                  audience_focus: Optional[str] = None,
                                  custom_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate complete narrative for all audiences.
        
        Args:
            company_id: Optional company identifier
            audience_focus: Optional specific audience to focus on
            custom_context: Additional context for narrative generation
            
        Returns:
            Complete narrative package with stories for all audiences
        """
        logger.info(f"Starting complete narrative generation for company: {company_id}")
        
        try:
            # Step 1: Collect all data
            logger.info("Step 1: Collecting data...")
            collected_data = self.data_collector.collect_all_data(company_id)
            
            # Step 2: Analyze trends
            logger.info("Step 2: Analyzing trends...")
            trend_analysis = self.trend_analyzer.analyze_all_trends(collected_data)
            
            # Step 3: Generate stories
            logger.info("Step 3: Generating stories...")
            stories = self.story_generator.generate_all_stories(trend_analysis, custom_context)
            
            # Step 4: Create complete narrative package
            narrative_package = self._create_narrative_package(
                collected_data, trend_analysis, stories, company_id, custom_context
            )
            
            # Step 5: Save narrative
            self._save_narrative(narrative_package)
            
            # Step 6: Generate recommendations
            recommendations = self._generate_recommendations(narrative_package)
            narrative_package['recommendations'] = recommendations
            
            self.current_narrative = narrative_package
            
            logger.info("Complete narrative generation finished successfully")
            
            return narrative_package
            
        except Exception as e:
            logger.error(f"Error in narrative generation: {str(e)}")
            return self._generate_error_narrative(str(e))
    
    def generate_audience_specific_narrative(self, 
                                           audience: str,
                                           company_id: Optional[str] = None,
                                           custom_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate narrative focused on specific audience.
        
        Args:
            audience: Target audience ('investors', 'clients', 'staff')
            company_id: Optional company identifier
            custom_context: Additional context
            
        Returns:
            Audience-specific narrative
        """
        logger.info(f"Generating {audience}-focused narrative")
        
        try:
            # Generate complete narrative first
            complete_narrative = self.generate_complete_narrative(company_id, audience, custom_context)
            
            # Extract audience-specific content
            audience_narrative = self._extract_audience_narrative(complete_narrative, audience)
            
            # Enhance for specific audience
            enhanced_narrative = self._enhance_audience_narrative(audience_narrative, audience)
            
            return enhanced_narrative
            
        except Exception as e:
            logger.error(f"Error generating {audience} narrative: {str(e)}")
            return self._generate_error_narrative(str(e), audience)
    
    def update_narrative_with_new_data(self, 
                                     new_data: Dict[str, Any],
                                     narrative_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Update existing narrative with new data.
        
        Args:
            new_data: New data to incorporate
            narrative_id: ID of narrative to update
            
        Returns:
            Updated narrative
        """
        logger.info("Updating narrative with new data")
        
        try:
            # Get existing narrative
            if narrative_id:
                existing_narrative = self._load_narrative(narrative_id)
            else:
                existing_narrative = self.current_narrative
            
            if not existing_narrative:
                logger.warning("No existing narrative found, generating new one")
                return self.generate_complete_narrative()
            
            # Merge new data with existing
            updated_data = self._merge_data(existing_narrative.get('data', {}), new_data)
            
            # Re-analyze trends with updated data
            trend_analysis = self.trend_analyzer.analyze_all_trends(updated_data)
            
            # Re-generate stories
            stories = self.story_generator.generate_all_stories(trend_analysis)
            
            # Create updated narrative
            updated_narrative = self._create_narrative_package(
                updated_data, trend_analysis, stories,
                existing_narrative.get('company_id'),
                existing_narrative.get('custom_context')
            )
            
            # Save updated narrative
            self._save_narrative(updated_narrative)
            
            self.current_narrative = updated_narrative
            
            return updated_narrative
            
        except Exception as e:
            logger.error(f"Error updating narrative: {str(e)}")
            return self._generate_error_narrative(str(e))
    
    def get_narrative_insights(self, narrative_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get insights and analytics about a narrative.
        
        Args:
            narrative_id: Optional narrative ID
            
        Returns:
            Narrative insights and analytics
        """
        try:
            narrative = self._load_narrative(narrative_id) if narrative_id else self.current_narrative
            
            if not narrative:
                return {'error': 'No narrative found'}
            
            insights = {
                'narrative_quality': self._assess_narrative_quality(narrative),
                'audience_effectiveness': self._assess_audience_effectiveness(narrative),
                'data_completeness': self._assess_data_completeness(narrative),
                'trend_strength': self._assess_trend_strength(narrative),
                'story_coherence': self._assess_story_coherence(narrative),
                'recommendations': self._generate_improvement_recommendations(narrative)
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Error getting narrative insights: {str(e)}")
            return {'error': str(e)}
    
    def export_narrative(self, 
                        format_type: str = 'json',
                        audience: Optional[str] = None,
                        narrative_id: Optional[str] = None) -> Any:
        """
        Export narrative in specified format.
        
        Args:
            format_type: Export format ('json', 'pdf', 'html', 'presentation')
            audience: Optional specific audience to export
            narrative_id: Optional narrative ID
            
        Returns:
            Exported narrative in specified format
        """
        try:
            narrative = self._load_narrative(narrative_id) if narrative_id else self.current_narrative
            
            if not narrative:
                return {'error': 'No narrative found'}
            
            if audience:
                narrative = self._extract_audience_narrative(narrative, audience)
            
            if format_type == 'json':
                return json.dumps(narrative, indent=2, default=str)
            elif format_type == 'html':
                return self._export_to_html(narrative)
            elif format_type == 'presentation':
                return self._export_to_presentation(narrative)
            elif format_type == 'pdf':
                return self._export_to_pdf(narrative)
            else:
                return narrative
                
        except Exception as e:
            logger.error(f"Error exporting narrative: {str(e)}")
            return {'error': str(e)}
    
    def _create_narrative_package(self, 
                                data: Dict[str, Any],
                                trends: Dict[str, Any], 
                                stories: Dict[str, Any],
                                company_id: Optional[str],
                                custom_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Create complete narrative package."""
        
        narrative_id = f"narrative_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        package = {
            'narrative_id': narrative_id,
            'company_id': company_id,
            'generation_timestamp': datetime.now().isoformat(),
            'data': data,
            'trends': trends,
            'stories': stories,
            'custom_context': custom_context,
            'metadata': {
                'data_quality_score': data.get('metadata', {}).get('data_quality_score', 0),
                'total_insights': len(trends.get('insights', [])),
                'story_quality_score': stories.get('metadata', {}).get('story_quality_score', 0),
                'narrative_themes': list(trends.get('narrative_themes', {}).keys())[:3],
                'generation_duration': 'calculated_in_production'
            },
            'executive_summary': self._create_executive_summary(trends, stories),
            'key_messages': self._extract_key_messages(stories),
            'supporting_evidence': self._compile_supporting_evidence(data, trends)
        }
        
        return package
    
    def _create_executive_summary(self, trends: Dict[str, Any], stories: Dict[str, Any]) -> Dict[str, Any]:
        """Create executive summary of the narrative."""
        
        top_insights = sorted(
            trends.get('insights', []),
            key=lambda x: x.get('narrative_weight', 0),
            reverse=True
        )[:3]
        
        return {
            'overview': "Comprehensive narrative analysis reveals strong performance across key metrics with clear opportunities for stakeholder engagement.",
            'key_themes': list(trends.get('narrative_themes', {}).keys())[:3],
            'top_insights': [insight['insight'] for insight in top_insights],
            'audience_readiness': {
                'investors': len([s for s in stories.get('investors', {}).get('supporting_data', [])]) > 3,
                'clients': len([s for s in stories.get('clients', {}).get('supporting_data', [])]) > 3,
                'staff': len([s for s in stories.get('staff', {}).get('supporting_data', [])]) > 3
            },
            'narrative_strength': stories.get('metadata', {}).get('story_quality_score', 0)
        }
    
    def _extract_key_messages(self, stories: Dict[str, Any]) -> Dict[str, List[str]]:
        """Extract key messages for each audience."""
        
        key_messages = {}
        
        for audience in ['investors', 'clients', 'staff', 'general']:
            story = stories.get(audience, {})
            messages = []
            
            # Extract headlines as key messages
            headlines = story.get('headlines', [])
            messages.extend(headlines)
            
            # Extract call-to-action
            cta = story.get('call_to_action', '')
            if cta:
                messages.append(cta)
            
            key_messages[audience] = messages
        
        return key_messages
    
    def _compile_supporting_evidence(self, data: Dict[str, Any], trends: Dict[str, Any]) -> Dict[str, Any]:
        """Compile supporting evidence for narratives."""
        
        return {
            'data_sources': data.get('metadata', {}).get('sources', []),
            'key_metrics': self._extract_all_key_metrics(trends),
            'trend_evidence': [
                insight['insight'] for insight in trends.get('insights', [])
                if insight.get('narrative_weight', 0) >= 0.8
            ],
            'data_quality_indicators': {
                'completeness': data.get('metadata', {}).get('data_quality_score', 0),
                'recency': data.get('metadata', {}).get('collection_timestamp'),
                'source_diversity': len(data.get('metadata', {}).get('sources', []))
            }
        }
    
    def _extract_all_key_metrics(self, trends: Dict[str, Any]) -> Dict[str, Any]:
        """Extract all key metrics from trends."""
        
        metrics = {}
        
        for category, trend_data in trends.get('trends', {}).items():
            if isinstance(trend_data, dict):
                for metric_name, metric_value in trend_data.items():
                    if isinstance(metric_value, (int, float)):
                        metrics[f"{category}_{metric_name}"] = metric_value
        
        return metrics
    
    def _save_narrative(self, narrative: Dict[str, Any]) -> str:
        """Save narrative to database."""
        try:
            narrative_id = self.database.insert('narratives', narrative)
            self.narrative_history.append(narrative_id)
            logger.info(f"Narrative saved with ID: {narrative_id}")
            return narrative_id
        except Exception as e:
            logger.error(f"Error saving narrative: {str(e)}")
            return ""
    
    def _load_narrative(self, narrative_id: str) -> Optional[Dict[str, Any]]:
        """Load narrative from database."""
        try:
            return self.database.find_one('narratives', {'narrative_id': narrative_id})
        except Exception as e:
            logger.error(f"Error loading narrative: {str(e)}")
            return None
    
    def _extract_audience_narrative(self, complete_narrative: Dict[str, Any], audience: str) -> Dict[str, Any]:
        """Extract audience-specific content from complete narrative."""
        
        audience_narrative = {
            'narrative_id': complete_narrative.get('narrative_id'),
            'audience': audience,
            'generation_timestamp': complete_narrative.get('generation_timestamp'),
            'story': complete_narrative.get('stories', {}).get(audience, {}),
            'relevant_trends': self._filter_trends_for_audience(
                complete_narrative.get('trends', {}), audience
            ),
            'key_messages': complete_narrative.get('key_messages', {}).get(audience, []),
            'supporting_evidence': self._filter_evidence_for_audience(
                complete_narrative.get('supporting_evidence', {}), audience
            )
        }
        
        return audience_narrative
    
    def _filter_trends_for_audience(self, trends: Dict[str, Any], audience: str) -> Dict[str, Any]:
        """Filter trends relevant to specific audience."""
        
        relevant_insights = [
            insight for insight in trends.get('insights', [])
            if insight.get('audience_relevance', {}).get(audience, 0) >= 0.7
        ]
        
        return {
            'insights': relevant_insights,
            'narrative_themes': trends.get('narrative_themes', {}),
            'trends': trends.get('trends', {})
        }
    
    def _filter_evidence_for_audience(self, evidence: Dict[str, Any], audience: str) -> Dict[str, Any]:
        """Filter supporting evidence for specific audience."""
        
        # This would be more sophisticated in production
        return evidence
    
    def _enhance_audience_narrative(self, narrative: Dict[str, Any], audience: str) -> Dict[str, Any]:
        """Enhance narrative for specific audience."""
        
        # Add audience-specific enhancements
        narrative['enhanced_content'] = {
            'personalized_insights': self._generate_personalized_insights(narrative, audience),
            'recommended_actions': self._generate_recommended_actions(narrative, audience),
            'next_steps': self._generate_next_steps(narrative, audience)
        }
        
        return narrative
    
    def _generate_personalized_insights(self, narrative: Dict[str, Any], audience: str) -> List[str]:
        """Generate personalized insights for audience."""
        
        insights = []
        story = narrative.get('story', {})
        
        if audience == 'investors':
            insights.append("Strong financial metrics indicate excellent investment opportunity")
            insights.append("Market positioning provides sustainable competitive advantage")
        elif audience == 'clients':
            insights.append("Proven track record of delivering client value")
            insights.append("Innovation capabilities ensure future-ready solutions")
        elif audience == 'staff':
            insights.append("Company success creates growth opportunities for all team members")
            insights.append("Mission-driven culture attracts and retains top talent")
        
        return insights
    
    def _generate_recommended_actions(self, narrative: Dict[str, Any], audience: str) -> List[str]:
        """Generate recommended actions for audience."""
        
        actions = []
        
        if audience == 'investors':
            actions.append("Schedule investor presentation to discuss growth strategy")
            actions.append("Provide detailed financial projections and market analysis")
        elif audience == 'clients':
            actions.append("Arrange solution demonstration and case study review")
            actions.append("Discuss partnership opportunities and value creation")
        elif audience == 'staff':
            actions.append("Share company achievements and future vision")
            actions.append("Discuss career development and growth opportunities")
        
        return actions
    
    def _generate_next_steps(self, narrative: Dict[str, Any], audience: str) -> List[str]:
        """Generate next steps for audience engagement."""
        
        next_steps = []
        
        if audience == 'investors':
            next_steps.append("Prepare detailed due diligence materials")
            next_steps.append("Schedule management presentations")
        elif audience == 'clients':
            next_steps.append("Develop customized proposal")
            next_steps.append("Plan pilot project or proof of concept")
        elif audience == 'staff':
            next_steps.append("Organize all-hands meeting to share progress")
            next_steps.append("Launch employee recognition program")
        
        return next_steps
    
    def _generate_recommendations(self, narrative: Dict[str, Any]) -> Dict[str, Any]:
        """Generate recommendations for narrative improvement and usage."""
        
        recommendations = {
            'narrative_optimization': [],
            'data_enhancement': [],
            'audience_engagement': [],
            'content_distribution': []
        }
        
        # Analyze narrative quality and suggest improvements
        data_quality = narrative.get('metadata', {}).get('data_quality_score', 0)
        if data_quality < 0.8:
            recommendations['data_enhancement'].append("Improve data collection completeness")
        
        story_quality = narrative.get('metadata', {}).get('story_quality_score', 0)
        if story_quality < 0.8:
            recommendations['narrative_optimization'].append("Enhance story coherence and impact")
        
        # Audience-specific recommendations
        for audience in ['investors', 'clients', 'staff']:
            story = narrative.get('stories', {}).get(audience, {})
            if story.get('narrative_strength', 0) < 0.7:
                recommendations['audience_engagement'].append(f"Strengthen {audience} narrative")
        
        # Content distribution recommendations
        recommendations['content_distribution'].extend([
            "Create executive summary for quick consumption",
            "Develop presentation materials for each audience",
            "Prepare social media content highlighting key achievements"
        ])
        
        return recommendations
    
    def _assess_narrative_quality(self, narrative: Dict[str, Any]) -> float:
        """Assess overall narrative quality."""
        
        scores = []
        
        # Data quality
        scores.append(narrative.get('metadata', {}).get('data_quality_score', 0))
        
        # Story quality
        scores.append(narrative.get('metadata', {}).get('story_quality_score', 0))
        
        # Insight strength
        insights = narrative.get('trends', {}).get('insights', [])
        strong_insights = [i for i in insights if i.get('narrative_weight', 0) >= 0.8]
        insight_score = len(strong_insights) / max(len(insights), 1)
        scores.append(insight_score)
        
        return sum(scores) / len(scores) if scores else 0
    
    def _assess_audience_effectiveness(self, narrative: Dict[str, Any]) -> Dict[str, float]:
        """Assess effectiveness for each audience."""
        
        effectiveness = {}
        
        for audience in ['investors', 'clients', 'staff']:
            story = narrative.get('stories', {}).get(audience, {})
            effectiveness[audience] = story.get('narrative_strength', 0)
        
        return effectiveness
    
    def _assess_data_completeness(self, narrative: Dict[str, Any]) -> float:
        """Assess data completeness."""
        return narrative.get('metadata', {}).get('data_quality_score', 0)
    
    def _assess_trend_strength(self, narrative: Dict[str, Any]) -> float:
        """Assess strength of identified trends."""
        
        insights = narrative.get('trends', {}).get('insights', [])
        if not insights:
            return 0
        
        avg_weight = sum(i.get('narrative_weight', 0) for i in insights) / len(insights)
        return avg_weight
    
    def _assess_story_coherence(self, narrative: Dict[str, Any]) -> float:
        """Assess coherence of generated stories."""
        
        stories = narrative.get('stories', {})
        coherence_scores = []
        
        for audience, story in stories.items():
            if isinstance(story, dict) and 'narrative_strength' in story:
                coherence_scores.append(story['narrative_strength'])
        
        return sum(coherence_scores) / len(coherence_scores) if coherence_scores else 0
    
    def _generate_improvement_recommendations(self, narrative: Dict[str, Any]) -> List[str]:
        """Generate recommendations for narrative improvement."""
        
        recommendations = []
        
        # Check data quality
        if self._assess_data_completeness(narrative) < 0.8:
            recommendations.append("Enhance data collection to improve narrative foundation")
        
        # Check trend strength
        if self._assess_trend_strength(narrative) < 0.7:
            recommendations.append("Strengthen trend analysis with additional data sources")
        
        # Check story coherence
        if self._assess_story_coherence(narrative) < 0.7:
            recommendations.append("Improve story structure and narrative flow")
        
        # Check audience effectiveness
        effectiveness = self._assess_audience_effectiveness(narrative)
        for audience, score in effectiveness.items():
            if score < 0.7:
                recommendations.append(f"Enhance {audience}-specific narrative content")
        
        return recommendations
    
    def _merge_data(self, existing_data: Dict[str, Any], new_data: Dict[str, Any]) -> Dict[str, Any]:
        """Merge new data with existing data."""
        
        # Simple merge - in production this would be more sophisticated
        merged = existing_data.copy()
        
        for key, value in new_data.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key].update(value)
            else:
                merged[key] = value
        
        return merged
    
    def _export_to_html(self, narrative: Dict[str, Any]) -> str:
        """Export narrative to HTML format."""
        
        html = f"""
        <html>
        <head><title>LensIQ Narrative Report</title></head>
        <body>
        <h1>Narrative Report</h1>
        <p>Generated: {narrative.get('generation_timestamp', 'Unknown')}</p>
        <h2>Executive Summary</h2>
        <p>{narrative.get('executive_summary', {}).get('overview', 'No summary available')}</p>
        </body>
        </html>
        """
        
        return html
    
    def _export_to_presentation(self, narrative: Dict[str, Any]) -> Dict[str, Any]:
        """Export narrative to presentation format."""
        
        return {
            'slides': [
                {
                    'title': 'Executive Summary',
                    'content': narrative.get('executive_summary', {}).get('overview', '')
                },
                {
                    'title': 'Key Messages',
                    'content': narrative.get('key_messages', {})
                }
            ]
        }
    
    def _export_to_pdf(self, narrative: Dict[str, Any]) -> str:
        """Export narrative to PDF format (placeholder)."""
        return "PDF export would be implemented with a PDF library"
    
    def _generate_error_narrative(self, error_message: str, audience: Optional[str] = None) -> Dict[str, Any]:
        """Generate error narrative when main process fails."""
        
        return {
            'error': True,
            'message': error_message,
            'audience': audience,
            'fallback_narrative': {
                'overview': 'Unable to generate complete narrative due to technical issues.',
                'recommendation': 'Please try again or contact support for assistance.'
            },
            'timestamp': datetime.now().isoformat()
        }
