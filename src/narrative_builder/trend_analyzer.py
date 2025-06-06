"""
Trend Analyzer for LensIQ Narrative Builder

Analyzes collected data to identify trends, patterns, and insights that can be used
for strategic storytelling across different audiences.
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import re

logger = logging.getLogger(__name__)


class TrendAnalyzer:
    """Analyzes data to identify trends and patterns for narrative building."""
    
    def __init__(self):
        """Initialize the trend analyzer."""
        self.trends = {
            'financial': {},
            'market': {},
            'sustainability': {},
            'operational': {},
            'sentiment': {},
            'strategic': {}
        }
        self.insights = []
        self.narrative_themes = {}
    
    def analyze_all_trends(self, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze all trends from collected data.
        
        Args:
            collected_data: Data from DataCollector
            
        Returns:
            Dictionary containing all trend analyses
        """
        logger.info("Starting comprehensive trend analysis")
        
        # Analyze structured data trends
        self._analyze_financial_trends(collected_data.get('structured', {}).get('financial', {}))
        self._analyze_market_trends(collected_data.get('structured', {}).get('market', {}))
        self._analyze_sustainability_trends(collected_data.get('structured', {}).get('sustainability', {}))
        self._analyze_operational_trends(collected_data.get('structured', {}).get('operational', {}))
        
        # Analyze unstructured data trends
        self._analyze_sentiment_trends(collected_data.get('unstructured', {}))
        
        # Generate strategic insights
        self._generate_strategic_insights()
        
        # Identify narrative themes
        self._identify_narrative_themes()
        
        logger.info(f"Trend analysis completed. Generated {len(self.insights)} insights")
        
        return {
            'trends': self.trends,
            'insights': self.insights,
            'narrative_themes': self.narrative_themes,
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _analyze_financial_trends(self, financial_data: Dict[str, Any]) -> None:
        """Analyze financial performance trends."""
        try:
            if not financial_data:
                return
            
            revenue_data = financial_data.get('revenue', {})
            profitability_data = financial_data.get('profitability', {})
            sustainability_investments = financial_data.get('sustainability_investments', {})
            
            # Revenue growth analysis
            current_revenue = revenue_data.get('current_year', 0)
            previous_revenue = revenue_data.get('previous_year', 0)
            growth_rate = revenue_data.get('growth_rate', 0)
            
            self.trends['financial']['revenue_growth'] = {
                'trend': 'positive' if growth_rate > 0 else 'negative',
                'magnitude': abs(growth_rate),
                'trajectory': self._calculate_trajectory(revenue_data.get('quarterly_breakdown', [])),
                'sustainability_correlation': sustainability_investments.get('roi_on_sustainability', 0)
            }
            
            # Profitability trends
            self.trends['financial']['profitability'] = {
                'gross_margin': profitability_data.get('gross_margin', 0),
                'operating_efficiency': profitability_data.get('operating_margin', 0),
                'net_profitability': profitability_data.get('net_margin', 0),
                'trend_direction': 'improving' if profitability_data.get('operating_margin', 0) > 0.15 else 'stable'
            }
            
            # Sustainability investment impact
            self.trends['financial']['sustainability_impact'] = {
                'investment_percentage': sustainability_investments.get('percentage_of_revenue', 0),
                'roi': sustainability_investments.get('roi_on_sustainability', 0),
                'strategic_priority': 'high' if sustainability_investments.get('percentage_of_revenue', 0) > 0.08 else 'medium'
            }
            
            # Generate financial insights
            if growth_rate > 20:
                self.insights.append({
                    'category': 'financial',
                    'type': 'growth',
                    'insight': f"Exceptional revenue growth of {growth_rate}% demonstrates strong market demand and execution",
                    'audience_relevance': {
                        'investors': 0.95,
                        'clients': 0.70,
                        'staff': 0.80
                    },
                    'narrative_weight': 0.90
                })
            
            if sustainability_investments.get('roi_on_sustainability', 0) > 0.20:
                self.insights.append({
                    'category': 'financial',
                    'type': 'sustainability_roi',
                    'insight': f"Sustainability investments generating {sustainability_investments.get('roi_on_sustainability', 0)*100:.1f}% ROI, proving business case for green initiatives",
                    'audience_relevance': {
                        'investors': 0.90,
                        'clients': 0.85,
                        'staff': 0.75
                    },
                    'narrative_weight': 0.85
                })
            
        except Exception as e:
            logger.error(f"Error analyzing financial trends: {str(e)}")
    
    def _analyze_market_trends(self, market_data: Dict[str, Any]) -> None:
        """Analyze market position and industry trends."""
        try:
            if not market_data:
                return
            
            industry_trends = market_data.get('industry_trends', {})
            competitive_landscape = market_data.get('competitive_landscape', {})
            macro_trends = market_data.get('macro_trends', {})
            
            # Market growth analysis
            self.trends['market']['industry_growth'] = {
                'market_size': industry_trends.get('market_size', 0),
                'growth_rate': industry_trends.get('growth_rate', 0),
                'key_drivers': industry_trends.get('key_drivers', []),
                'opportunity_score': industry_trends.get('growth_rate', 0) * 10
            }
            
            # Competitive positioning
            self.trends['market']['competitive_position'] = {
                'market_position': competitive_landscape.get('market_position', 'Unknown'),
                'market_share': competitive_landscape.get('market_share', 0),
                'competitive_advantages': competitive_landscape.get('competitive_advantages', []),
                'differentiation_strength': len(competitive_landscape.get('competitive_advantages', []))
            }
            
            # Macro trend alignment
            self.trends['market']['macro_alignment'] = {
                'sustainability_focus': macro_trends.get('sustainability_focus', 0),
                'digital_transformation': macro_trends.get('digital_transformation', 0),
                'regulatory_compliance': macro_trends.get('regulatory_compliance', 0),
                'overall_alignment': np.mean(list(macro_trends.values())) if macro_trends else 0
            }
            
            # Generate market insights
            if industry_trends.get('growth_rate', 0) > 0.10:
                self.insights.append({
                    'category': 'market',
                    'type': 'opportunity',
                    'insight': f"Operating in high-growth market with {industry_trends.get('growth_rate', 0)*100:.0f}% annual growth rate",
                    'audience_relevance': {
                        'investors': 0.95,
                        'clients': 0.60,
                        'staff': 0.70
                    },
                    'narrative_weight': 0.85
                })
            
            if competitive_landscape.get('market_position') == 'Top 3':
                self.insights.append({
                    'category': 'market',
                    'type': 'leadership',
                    'insight': "Established market leadership position with strong competitive advantages",
                    'audience_relevance': {
                        'investors': 0.90,
                        'clients': 0.95,
                        'staff': 0.85
                    },
                    'narrative_weight': 0.80
                })
            
        except Exception as e:
            logger.error(f"Error analyzing market trends: {str(e)}")
    
    def _analyze_sustainability_trends(self, sustainability_data: Dict[str, Any]) -> None:
        """Analyze sustainability and ESG trends."""
        try:
            if not sustainability_data:
                return
            
            environmental = sustainability_data.get('environmental', {})
            social = sustainability_data.get('social', {})
            governance = sustainability_data.get('governance', {})
            certifications = sustainability_data.get('certifications', [])
            
            # Environmental performance
            self.trends['sustainability']['environmental'] = {
                'carbon_reduction': environmental.get('carbon_footprint_reduction', 0),
                'renewable_energy': environmental.get('renewable_energy_usage', 0),
                'waste_reduction': environmental.get('waste_reduction', 0),
                'water_conservation': environmental.get('water_conservation', 0),
                'overall_score': np.mean(list(environmental.values())) if environmental else 0
            }
            
            # Social impact
            self.trends['sustainability']['social'] = {
                'employee_satisfaction': social.get('employee_satisfaction', 0),
                'diversity_index': social.get('diversity_index', 0),
                'community_investment': social.get('community_investment', 0),
                'safety_record': social.get('safety_record', 0),
                'overall_score': np.mean([v for v in social.values() if isinstance(v, (int, float)) and v <= 1]) if social else 0
            }
            
            # Governance strength
            self.trends['sustainability']['governance'] = {
                'board_diversity': governance.get('board_diversity', 0),
                'transparency_score': governance.get('transparency_score', 0),
                'ethics_compliance': governance.get('ethics_compliance', 0),
                'stakeholder_engagement': governance.get('stakeholder_engagement', 0),
                'overall_score': np.mean(list(governance.values())) if governance else 0
            }
            
            # Certification value
            self.trends['sustainability']['certifications'] = {
                'count': len(certifications),
                'types': certifications,
                'credibility_score': len(certifications) * 0.2  # Simple scoring
            }
            
            # Generate sustainability insights
            env_score = self.trends['sustainability']['environmental']['overall_score']
            if env_score > 0.7:
                self.insights.append({
                    'category': 'sustainability',
                    'type': 'environmental_leadership',
                    'insight': f"Leading environmental performance with {env_score*100:.0f}% average score across key metrics",
                    'audience_relevance': {
                        'investors': 0.85,
                        'clients': 0.90,
                        'staff': 0.80
                    },
                    'narrative_weight': 0.85
                })
            
            if len(certifications) >= 3:
                self.insights.append({
                    'category': 'sustainability',
                    'type': 'certification_strength',
                    'insight': f"Strong sustainability credentials with {len(certifications)} major certifications",
                    'audience_relevance': {
                        'investors': 0.75,
                        'clients': 0.95,
                        'staff': 0.70
                    },
                    'narrative_weight': 0.75
                })
            
        except Exception as e:
            logger.error(f"Error analyzing sustainability trends: {str(e)}")
    
    def _analyze_operational_trends(self, operational_data: Dict[str, Any]) -> None:
        """Analyze operational efficiency and innovation trends."""
        try:
            if not operational_data:
                return
            
            efficiency = operational_data.get('efficiency_metrics', {})
            innovation = operational_data.get('innovation', {})
            workforce = operational_data.get('workforce', {})
            
            # Operational efficiency
            self.trends['operational']['efficiency'] = {
                'productivity_improvement': efficiency.get('productivity_improvement', 0),
                'cost_reduction': efficiency.get('cost_reduction', 0),
                'quality_score': efficiency.get('quality_score', 0),
                'customer_satisfaction': efficiency.get('customer_satisfaction', 0),
                'overall_efficiency': np.mean(list(efficiency.values())) if efficiency else 0
            }
            
            # Innovation capacity
            self.trends['operational']['innovation'] = {
                'rd_investment': innovation.get('rd_investment', 0),
                'patents_filed': innovation.get('patents_filed', 0),
                'new_products': innovation.get('new_products_launched', 0),
                'pipeline_value': innovation.get('innovation_pipeline_value', 0),
                'innovation_intensity': innovation.get('rd_investment', 0) / 100000000  # Normalize
            }
            
            # Workforce strength
            self.trends['operational']['workforce'] = {
                'employee_count': workforce.get('employee_count', 0),
                'retention_rate': workforce.get('retention_rate', 0),
                'training_investment': workforce.get('training_hours_per_employee', 0),
                'internal_promotion': workforce.get('internal_promotion_rate', 0),
                'workforce_health': np.mean([
                    workforce.get('retention_rate', 0),
                    workforce.get('internal_promotion_rate', 0)
                ])
            }
            
            # Generate operational insights
            if efficiency.get('productivity_improvement', 0) > 0.20:
                self.insights.append({
                    'category': 'operational',
                    'type': 'efficiency_gains',
                    'insight': f"Significant productivity improvements of {efficiency.get('productivity_improvement', 0)*100:.0f}% demonstrate operational excellence",
                    'audience_relevance': {
                        'investors': 0.85,
                        'clients': 0.75,
                        'staff': 0.90
                    },
                    'narrative_weight': 0.80
                })
            
            if innovation.get('patents_filed', 0) > 10:
                self.insights.append({
                    'category': 'operational',
                    'type': 'innovation_strength',
                    'insight': f"Strong innovation pipeline with {innovation.get('patents_filed', 0)} patents filed and significant R&D investment",
                    'audience_relevance': {
                        'investors': 0.90,
                        'clients': 0.85,
                        'staff': 0.80
                    },
                    'narrative_weight': 0.85
                })
            
        except Exception as e:
            logger.error(f"Error analyzing operational trends: {str(e)}")
    
    def _analyze_sentiment_trends(self, unstructured_data: Dict[str, Any]) -> None:
        """Analyze sentiment and perception trends from unstructured data."""
        try:
            news_data = unstructured_data.get('news', {})
            social_data = unstructured_data.get('social_media', {})
            
            # News sentiment analysis
            news_sentiment = news_data.get('sentiment_analysis', {})
            self.trends['sentiment']['news'] = {
                'overall_sentiment': news_sentiment.get('overall_sentiment', 0),
                'positive_ratio': news_sentiment.get('positive_mentions', 0) / max(sum([
                    news_sentiment.get('positive_mentions', 0),
                    news_sentiment.get('neutral_mentions', 0),
                    news_sentiment.get('negative_mentions', 0)
                ]), 1),
                'key_themes': news_data.get('key_themes', {}),
                'media_coverage_quality': 'high' if news_sentiment.get('overall_sentiment', 0) > 0.7 else 'medium'
            }
            
            # Social media sentiment
            if social_data:
                platforms = social_data.get('platforms', {})
                avg_sentiment = np.mean([
                    platform.get('sentiment', 0) for platform in platforms.values()
                ]) if platforms else 0
                
                self.trends['sentiment']['social_media'] = {
                    'average_sentiment': avg_sentiment,
                    'engagement_quality': 'high' if avg_sentiment > 0.75 else 'medium',
                    'trending_topics': social_data.get('trending_topics', []),
                    'influencer_support': len(social_data.get('influencer_mentions', []))
                }
            
            # Generate sentiment insights
            if news_sentiment.get('overall_sentiment', 0) > 0.75:
                self.insights.append({
                    'category': 'sentiment',
                    'type': 'positive_perception',
                    'insight': f"Strong positive media sentiment ({news_sentiment.get('overall_sentiment', 0)*100:.0f}%) indicates excellent brand reputation",
                    'audience_relevance': {
                        'investors': 0.80,
                        'clients': 0.95,
                        'staff': 0.85
                    },
                    'narrative_weight': 0.75
                })
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment trends: {str(e)}")
    
    def _generate_strategic_insights(self) -> None:
        """Generate high-level strategic insights from all trend analyses."""
        try:
            # Cross-trend analysis
            financial_strength = self.trends.get('financial', {}).get('revenue_growth', {}).get('magnitude', 0)
            market_opportunity = self.trends.get('market', {}).get('industry_growth', {}).get('growth_rate', 0)
            sustainability_score = self.trends.get('sustainability', {}).get('environmental', {}).get('overall_score', 0)
            
            # Strategic positioning insight
            if financial_strength > 15 and market_opportunity > 0.10 and sustainability_score > 0.7:
                self.insights.append({
                    'category': 'strategic',
                    'type': 'market_leadership',
                    'insight': "Uniquely positioned to capitalize on market growth with strong financial performance and sustainability leadership",
                    'audience_relevance': {
                        'investors': 0.95,
                        'clients': 0.90,
                        'staff': 0.85
                    },
                    'narrative_weight': 0.95
                })
            
            # Future readiness insight
            innovation_strength = self.trends.get('operational', {}).get('innovation', {}).get('innovation_intensity', 0)
            if innovation_strength > 0.10 and sustainability_score > 0.6:
                self.insights.append({
                    'category': 'strategic',
                    'type': 'future_readiness',
                    'insight': "Strong innovation capabilities and sustainability focus position company for long-term success",
                    'audience_relevance': {
                        'investors': 0.90,
                        'clients': 0.85,
                        'staff': 0.90
                    },
                    'narrative_weight': 0.85
                })
            
        except Exception as e:
            logger.error(f"Error generating strategic insights: {str(e)}")
    
    def _identify_narrative_themes(self) -> None:
        """Identify key narrative themes for different audiences."""
        try:
            # Analyze insights to identify themes
            theme_scores = defaultdict(float)
            
            for insight in self.insights:
                category = insight.get('category', '')
                insight_type = insight.get('type', '')
                weight = insight.get('narrative_weight', 0)
                
                # Map insights to narrative themes
                if category in ['financial', 'market'] and 'growth' in insight_type:
                    theme_scores['growth_story'] += weight
                
                if category == 'sustainability' or 'sustainability' in insight_type:
                    theme_scores['sustainability_leadership'] += weight
                
                if category == 'operational' and 'innovation' in insight_type:
                    theme_scores['innovation_excellence'] += weight
                
                if 'leadership' in insight_type or 'position' in insight_type:
                    theme_scores['market_leadership'] += weight
                
                if category == 'sentiment' or 'perception' in insight_type:
                    theme_scores['brand_strength'] += weight
            
            # Normalize and rank themes
            max_score = max(theme_scores.values()) if theme_scores else 1
            self.narrative_themes = {
                theme: score / max_score for theme, score in theme_scores.items()
            }
            
            # Sort by strength
            self.narrative_themes = dict(sorted(
                self.narrative_themes.items(), 
                key=lambda x: x[1], 
                reverse=True
            ))
            
        except Exception as e:
            logger.error(f"Error identifying narrative themes: {str(e)}")
    
    def _calculate_trajectory(self, quarterly_data: List[float]) -> str:
        """Calculate trend trajectory from quarterly data."""
        if len(quarterly_data) < 2:
            return 'insufficient_data'
        
        # Simple linear trend calculation
        x = np.arange(len(quarterly_data))
        y = np.array(quarterly_data)
        slope = np.polyfit(x, y, 1)[0]
        
        if slope > 0.05:
            return 'accelerating'
        elif slope > 0:
            return 'growing'
        elif slope > -0.05:
            return 'stable'
        else:
            return 'declining'
    
    def get_audience_specific_insights(self, audience: str) -> List[Dict[str, Any]]:
        """
        Get insights tailored for specific audience.
        
        Args:
            audience: Target audience ('investors', 'clients', 'staff')
            
        Returns:
            List of relevant insights for the audience
        """
        audience_insights = []
        
        for insight in self.insights:
            relevance = insight.get('audience_relevance', {}).get(audience, 0)
            if relevance >= 0.7:  # High relevance threshold
                audience_insights.append({
                    **insight,
                    'audience_relevance_score': relevance
                })
        
        # Sort by relevance and narrative weight
        audience_insights.sort(
            key=lambda x: (x['audience_relevance_score'], x['narrative_weight']), 
            reverse=True
        )
        
        return audience_insights
    
    def get_trend_summary(self) -> Dict[str, Any]:
        """Get a summary of all identified trends."""
        return {
            'total_insights': len(self.insights),
            'trend_categories': list(self.trends.keys()),
            'top_narrative_themes': list(self.narrative_themes.keys())[:3],
            'strongest_trends': [
                insight for insight in self.insights 
                if insight.get('narrative_weight', 0) >= 0.85
            ]
        }
