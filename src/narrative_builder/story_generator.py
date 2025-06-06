"""
Story Generator for LensIQ Narrative Builder

Generates compelling narratives tailored for different audiences (investors, clients, staff)
based on trend analysis and collected data insights.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class StoryGenerator:
    """Generates compelling stories for different audiences based on data insights."""
    
    def __init__(self):
        """Initialize the story generator."""
        self.story_templates = self._load_story_templates()
        self.audience_preferences = self._load_audience_preferences()
        self.generated_stories = {}
    
    def generate_all_stories(self, trend_analysis: Dict[str, Any], company_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate stories for all audiences.
        
        Args:
            trend_analysis: Output from TrendAnalyzer
            company_context: Additional company context
            
        Returns:
            Dictionary containing stories for each audience
        """
        logger.info("Generating stories for all audiences")
        
        insights = trend_analysis.get('insights', [])
        narrative_themes = trend_analysis.get('narrative_themes', {})
        trends = trend_analysis.get('trends', {})
        
        # Generate audience-specific stories
        self.generated_stories = {
            'investors': self._generate_investor_story(insights, narrative_themes, trends, company_context),
            'clients': self._generate_client_story(insights, narrative_themes, trends, company_context),
            'staff': self._generate_staff_story(insights, narrative_themes, trends, company_context),
            'general': self._generate_general_story(insights, narrative_themes, trends, company_context)
        }
        
        # Add metadata
        self.generated_stories['metadata'] = {
            'generation_timestamp': datetime.now().isoformat(),
            'total_insights_used': len(insights),
            'primary_themes': list(narrative_themes.keys())[:3],
            'story_quality_score': self._calculate_story_quality()
        }
        
        logger.info(f"Generated {len(self.generated_stories)-1} audience-specific stories")
        
        return self.generated_stories
    
    def _generate_investor_story(self, insights: List[Dict], themes: Dict, trends: Dict, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate investor-focused narrative."""
        try:
            # Filter insights relevant to investors
            investor_insights = [
                insight for insight in insights 
                if insight.get('audience_relevance', {}).get('investors', 0) >= 0.7
            ]
            
            # Build narrative structure
            story_sections = {
                'executive_summary': self._build_executive_summary(investor_insights, themes),
                'financial_performance': self._build_financial_narrative(investor_insights, trends.get('financial', {})),
                'market_opportunity': self._build_market_narrative(investor_insights, trends.get('market', {})),
                'competitive_advantage': self._build_competitive_narrative(investor_insights, trends),
                'growth_strategy': self._build_growth_narrative(investor_insights, themes),
                'risk_mitigation': self._build_risk_narrative(investor_insights, trends),
                'investment_thesis': self._build_investment_thesis(investor_insights, themes)
            }
            
            # Generate key metrics for investors
            key_metrics = self._extract_investor_metrics(trends)
            
            # Create compelling headlines
            headlines = self._generate_investor_headlines(investor_insights, themes)
            
            return {
                'audience': 'investors',
                'story_type': 'investment_narrative',
                'sections': story_sections,
                'key_metrics': key_metrics,
                'headlines': headlines,
                'call_to_action': self._generate_investor_cta(themes),
                'supporting_data': [insight['insight'] for insight in investor_insights[:5]],
                'narrative_strength': len(investor_insights) * 0.1
            }
            
        except Exception as e:
            logger.error(f"Error generating investor story: {str(e)}")
            return self._generate_fallback_story('investors')
    
    def _generate_client_story(self, insights: List[Dict], themes: Dict, trends: Dict, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate client-focused narrative."""
        try:
            # Filter insights relevant to clients
            client_insights = [
                insight for insight in insights 
                if insight.get('audience_relevance', {}).get('clients', 0) >= 0.7
            ]
            
            # Build narrative structure
            story_sections = {
                'value_proposition': self._build_value_proposition(client_insights, themes),
                'solution_capabilities': self._build_solution_narrative(client_insights, trends.get('operational', {})),
                'sustainability_commitment': self._build_sustainability_narrative(client_insights, trends.get('sustainability', {})),
                'innovation_leadership': self._build_innovation_narrative(client_insights, trends.get('operational', {})),
                'client_success': self._build_success_narrative(client_insights, trends),
                'partnership_value': self._build_partnership_narrative(client_insights, themes),
                'future_roadmap': self._build_roadmap_narrative(client_insights, themes)
            }
            
            # Generate client-relevant metrics
            key_metrics = self._extract_client_metrics(trends)
            
            # Create compelling headlines
            headlines = self._generate_client_headlines(client_insights, themes)
            
            return {
                'audience': 'clients',
                'story_type': 'value_narrative',
                'sections': story_sections,
                'key_metrics': key_metrics,
                'headlines': headlines,
                'call_to_action': self._generate_client_cta(themes),
                'supporting_data': [insight['insight'] for insight in client_insights[:5]],
                'narrative_strength': len(client_insights) * 0.1
            }
            
        except Exception as e:
            logger.error(f"Error generating client story: {str(e)}")
            return self._generate_fallback_story('clients')
    
    def _generate_staff_story(self, insights: List[Dict], themes: Dict, trends: Dict, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate staff-focused narrative."""
        try:
            # Filter insights relevant to staff
            staff_insights = [
                insight for insight in insights 
                if insight.get('audience_relevance', {}).get('staff', 0) >= 0.7
            ]
            
            # Build narrative structure
            story_sections = {
                'mission_progress': self._build_mission_narrative(staff_insights, themes),
                'team_achievements': self._build_achievement_narrative(staff_insights, trends.get('operational', {})),
                'growth_opportunities': self._build_opportunity_narrative(staff_insights, trends),
                'company_culture': self._build_culture_narrative(staff_insights, trends.get('sustainability', {})),
                'innovation_impact': self._build_impact_narrative(staff_insights, trends.get('operational', {})),
                'future_vision': self._build_vision_narrative(staff_insights, themes),
                'recognition': self._build_recognition_narrative(staff_insights, trends)
            }
            
            # Generate staff-relevant metrics
            key_metrics = self._extract_staff_metrics(trends)
            
            # Create inspiring headlines
            headlines = self._generate_staff_headlines(staff_insights, themes)
            
            return {
                'audience': 'staff',
                'story_type': 'inspiration_narrative',
                'sections': story_sections,
                'key_metrics': key_metrics,
                'headlines': headlines,
                'call_to_action': self._generate_staff_cta(themes),
                'supporting_data': [insight['insight'] for insight in staff_insights[:5]],
                'narrative_strength': len(staff_insights) * 0.1
            }
            
        except Exception as e:
            logger.error(f"Error generating staff story: {str(e)}")
            return self._generate_fallback_story('staff')
    
    def _generate_general_story(self, insights: List[Dict], themes: Dict, trends: Dict, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate general audience narrative."""
        try:
            # Use all high-quality insights
            general_insights = [
                insight for insight in insights 
                if insight.get('narrative_weight', 0) >= 0.8
            ]
            
            # Build balanced narrative
            story_sections = {
                'company_overview': self._build_overview_narrative(general_insights, themes),
                'key_achievements': self._build_general_achievements(general_insights, trends),
                'sustainability_leadership': self._build_sustainability_narrative(general_insights, trends.get('sustainability', {})),
                'market_position': self._build_market_narrative(general_insights, trends.get('market', {})),
                'innovation_excellence': self._build_innovation_narrative(general_insights, trends.get('operational', {})),
                'future_outlook': self._build_outlook_narrative(general_insights, themes)
            }
            
            # Generate balanced metrics
            key_metrics = self._extract_general_metrics(trends)
            
            # Create broad appeal headlines
            headlines = self._generate_general_headlines(general_insights, themes)
            
            return {
                'audience': 'general',
                'story_type': 'comprehensive_narrative',
                'sections': story_sections,
                'key_metrics': key_metrics,
                'headlines': headlines,
                'call_to_action': self._generate_general_cta(themes),
                'supporting_data': [insight['insight'] for insight in general_insights[:5]],
                'narrative_strength': len(general_insights) * 0.1
            }
            
        except Exception as e:
            logger.error(f"Error generating general story: {str(e)}")
            return self._generate_fallback_story('general')
    
    # Narrative building methods
    def _build_executive_summary(self, insights: List[Dict], themes: Dict) -> str:
        """Build executive summary for investors."""
        top_theme = list(themes.keys())[0] if themes else 'growth'
        
        if top_theme == 'growth_story':
            return "Delivering exceptional growth through strategic market positioning and operational excellence, with strong financial performance demonstrating clear value creation for shareholders."
        elif top_theme == 'sustainability_leadership':
            return "Leading the market transformation toward sustainability while generating superior returns, positioning the company at the forefront of the green economy transition."
        elif top_theme == 'innovation_excellence':
            return "Driving industry innovation with breakthrough technologies and solutions, creating sustainable competitive advantages and expanding market opportunities."
        else:
            return "Executing a comprehensive strategy that combines financial performance, market leadership, and sustainable practices to deliver long-term shareholder value."
    
    def _build_financial_narrative(self, insights: List[Dict], financial_trends: Dict) -> str:
        """Build financial performance narrative."""
        revenue_growth = financial_trends.get('revenue_growth', {})
        growth_rate = revenue_growth.get('magnitude', 0)
        
        if growth_rate > 20:
            return f"Outstanding financial performance with {growth_rate:.0f}% revenue growth, demonstrating strong market demand and effective execution of our strategic initiatives. Profitability metrics continue to improve, with sustainability investments generating measurable returns."
        elif growth_rate > 10:
            return f"Solid financial growth of {growth_rate:.0f}% reflects our strategic focus and market positioning. Strong operational efficiency and disciplined capital allocation are driving consistent profitability improvements."
        else:
            return "Maintaining financial stability while investing in strategic growth initiatives. Our balanced approach to profitability and reinvestment positions us for sustainable long-term growth."
    
    def _build_market_narrative(self, insights: List[Dict], market_trends: Dict) -> str:
        """Build market opportunity narrative."""
        industry_growth = market_trends.get('industry_growth', {})
        growth_rate = industry_growth.get('growth_rate', 0)
        
        if growth_rate > 0.15:
            return f"Operating in a high-growth market expanding at {growth_rate*100:.0f}% annually, with strong positioning to capture disproportionate value from industry transformation. Our competitive advantages provide sustainable differentiation."
        else:
            return "Well-positioned in our target markets with clear competitive advantages and strategic initiatives to drive market share growth and value creation."
    
    def _build_value_proposition(self, insights: List[Dict], themes: Dict) -> str:
        """Build value proposition for clients."""
        top_theme = list(themes.keys())[0] if themes else 'innovation'
        
        if 'sustainability' in top_theme:
            return "Delivering innovative solutions that drive both business success and environmental impact, helping our clients achieve their sustainability goals while improving operational performance."
        elif 'innovation' in top_theme:
            return "Providing cutting-edge solutions that transform business operations, enhance efficiency, and create competitive advantages for our clients in rapidly evolving markets."
        else:
            return "Partnering with clients to deliver exceptional value through innovative solutions, deep expertise, and commitment to sustainable business practices."
    
    def _build_mission_narrative(self, insights: List[Dict], themes: Dict) -> str:
        """Build mission progress narrative for staff."""
        top_theme = list(themes.keys())[0] if themes else 'growth'
        
        return "Our team's dedication and expertise are driving meaningful progress toward our mission of creating sustainable value for all stakeholders. Together, we're building a company that makes a positive impact while achieving exceptional results."
    
    # Metric extraction methods
    def _extract_investor_metrics(self, trends: Dict) -> List[Dict[str, Any]]:
        """Extract key metrics for investors."""
        metrics = []
        
        financial = trends.get('financial', {})
        if financial:
            revenue_growth = financial.get('revenue_growth', {})
            metrics.append({
                'name': 'Revenue Growth',
                'value': f"{revenue_growth.get('magnitude', 0):.0f}%",
                'trend': revenue_growth.get('trend', 'stable'),
                'importance': 'high'
            })
            
            profitability = financial.get('profitability', {})
            metrics.append({
                'name': 'Operating Margin',
                'value': f"{profitability.get('operating_efficiency', 0)*100:.1f}%",
                'trend': profitability.get('trend_direction', 'stable'),
                'importance': 'high'
            })
        
        market = trends.get('market', {})
        if market:
            market_growth = market.get('industry_growth', {})
            metrics.append({
                'name': 'Market Growth Rate',
                'value': f"{market_growth.get('growth_rate', 0)*100:.0f}%",
                'trend': 'positive',
                'importance': 'medium'
            })
        
        return metrics
    
    def _extract_client_metrics(self, trends: Dict) -> List[Dict[str, Any]]:
        """Extract key metrics for clients."""
        metrics = []
        
        operational = trends.get('operational', {})
        if operational:
            efficiency = operational.get('efficiency', {})
            metrics.append({
                'name': 'Customer Satisfaction',
                'value': f"{efficiency.get('customer_satisfaction', 0)*100:.0f}%",
                'trend': 'positive',
                'importance': 'high'
            })
            
            metrics.append({
                'name': 'Quality Score',
                'value': f"{efficiency.get('quality_score', 0)*100:.0f}%",
                'trend': 'positive',
                'importance': 'high'
            })
        
        sustainability = trends.get('sustainability', {})
        if sustainability:
            env_score = sustainability.get('environmental', {}).get('overall_score', 0)
            metrics.append({
                'name': 'Sustainability Score',
                'value': f"{env_score*100:.0f}%",
                'trend': 'positive',
                'importance': 'medium'
            })
        
        return metrics
    
    def _extract_staff_metrics(self, trends: Dict) -> List[Dict[str, Any]]:
        """Extract key metrics for staff."""
        metrics = []
        
        operational = trends.get('operational', {})
        if operational:
            workforce = operational.get('workforce', {})
            metrics.append({
                'name': 'Employee Retention',
                'value': f"{workforce.get('retention_rate', 0)*100:.0f}%",
                'trend': 'positive',
                'importance': 'high'
            })
            
            metrics.append({
                'name': 'Internal Promotions',
                'value': f"{workforce.get('internal_promotion', 0)*100:.0f}%",
                'trend': 'positive',
                'importance': 'medium'
            })
            
            innovation = operational.get('innovation', {})
            metrics.append({
                'name': 'R&D Investment',
                'value': f"${innovation.get('rd_investment', 0)/1000000:.0f}M",
                'trend': 'positive',
                'importance': 'medium'
            })
        
        return metrics
    
    def _extract_general_metrics(self, trends: Dict) -> List[Dict[str, Any]]:
        """Extract balanced metrics for general audience."""
        metrics = []
        
        # Mix of financial, operational, and sustainability metrics
        financial = trends.get('financial', {})
        if financial:
            revenue_growth = financial.get('revenue_growth', {})
            metrics.append({
                'name': 'Revenue Growth',
                'value': f"{revenue_growth.get('magnitude', 0):.0f}%",
                'trend': revenue_growth.get('trend', 'stable'),
                'importance': 'high'
            })
        
        sustainability = trends.get('sustainability', {})
        if sustainability:
            env_score = sustainability.get('environmental', {}).get('overall_score', 0)
            metrics.append({
                'name': 'Environmental Score',
                'value': f"{env_score*100:.0f}%",
                'trend': 'positive',
                'importance': 'high'
            })
        
        operational = trends.get('operational', {})
        if operational:
            innovation = operational.get('innovation', {})
            metrics.append({
                'name': 'Innovation Investment',
                'value': f"${innovation.get('rd_investment', 0)/1000000:.0f}M",
                'trend': 'positive',
                'importance': 'medium'
            })
        
        return metrics
    
    # Headline generation methods
    def _generate_investor_headlines(self, insights: List[Dict], themes: Dict) -> List[str]:
        """Generate compelling headlines for investors."""
        headlines = []
        
        for insight in insights[:3]:
            if 'growth' in insight.get('type', ''):
                headlines.append("Exceptional Growth Trajectory Drives Shareholder Value")
            elif 'sustainability' in insight.get('type', ''):
                headlines.append("Sustainability Leadership Creates Competitive Advantage")
            elif 'market' in insight.get('type', ''):
                headlines.append("Strategic Market Position Delivers Superior Returns")
            else:
                headlines.append("Strong Performance Across Key Metrics")
        
        return headlines[:3]
    
    def _generate_client_headlines(self, insights: List[Dict], themes: Dict) -> List[str]:
        """Generate compelling headlines for clients."""
        headlines = []
        
        for insight in insights[:3]:
            if 'innovation' in insight.get('type', ''):
                headlines.append("Innovation Excellence Delivers Client Success")
            elif 'sustainability' in insight.get('type', ''):
                headlines.append("Sustainable Solutions Drive Business Value")
            elif 'quality' in insight.get('type', ''):
                headlines.append("Uncompromising Quality Standards")
            else:
                headlines.append("Trusted Partner for Business Transformation")
        
        return headlines[:3]
    
    def _generate_staff_headlines(self, insights: List[Dict], themes: Dict) -> List[str]:
        """Generate inspiring headlines for staff."""
        headlines = []
        
        for insight in insights[:3]:
            if 'growth' in insight.get('type', ''):
                headlines.append("Our Success Creates New Opportunities")
            elif 'innovation' in insight.get('type', ''):
                headlines.append("Innovation Team Drives Industry Leadership")
            elif 'sustainability' in insight.get('type', ''):
                headlines.append("Making a Positive Impact Together")
            else:
                headlines.append("Team Excellence Delivers Outstanding Results")
        
        return headlines[:3]
    
    def _generate_general_headlines(self, insights: List[Dict], themes: Dict) -> List[str]:
        """Generate broad appeal headlines."""
        headlines = [
            "Leading the Future of Sustainable Business",
            "Innovation and Excellence Drive Success",
            "Creating Value for All Stakeholders"
        ]
        return headlines
    
    # Call-to-action generation
    def _generate_investor_cta(self, themes: Dict) -> str:
        """Generate call-to-action for investors."""
        return "Join us in capitalizing on this exceptional growth opportunity and sustainable value creation story."
    
    def _generate_client_cta(self, themes: Dict) -> str:
        """Generate call-to-action for clients."""
        return "Partner with us to transform your business and achieve your sustainability goals."
    
    def _generate_staff_cta(self, themes: Dict) -> str:
        """Generate call-to-action for staff."""
        return "Continue driving our mission forward and building the future of sustainable business together."
    
    def _generate_general_cta(self, themes: Dict) -> str:
        """Generate general call-to-action."""
        return "Discover how we're creating a more sustainable and prosperous future for all."
    
    # Helper methods
    def _load_story_templates(self) -> Dict[str, Any]:
        """Load story templates for different audiences."""
        return {
            'investors': {
                'structure': ['executive_summary', 'financial_performance', 'market_opportunity', 'investment_thesis'],
                'tone': 'professional',
                'focus': 'returns'
            },
            'clients': {
                'structure': ['value_proposition', 'solution_capabilities', 'client_success', 'partnership_value'],
                'tone': 'collaborative',
                'focus': 'value'
            },
            'staff': {
                'structure': ['mission_progress', 'team_achievements', 'growth_opportunities', 'future_vision'],
                'tone': 'inspiring',
                'focus': 'purpose'
            }
        }
    
    def _load_audience_preferences(self) -> Dict[str, Any]:
        """Load audience preferences for narrative customization."""
        return {
            'investors': {
                'key_interests': ['growth', 'profitability', 'market_opportunity', 'risk_management'],
                'preferred_metrics': ['revenue_growth', 'margins', 'market_share', 'roi'],
                'communication_style': 'data_driven'
            },
            'clients': {
                'key_interests': ['value_delivery', 'innovation', 'reliability', 'sustainability'],
                'preferred_metrics': ['customer_satisfaction', 'quality', 'efficiency', 'impact'],
                'communication_style': 'solution_focused'
            },
            'staff': {
                'key_interests': ['purpose', 'growth', 'recognition', 'culture'],
                'preferred_metrics': ['employee_satisfaction', 'career_development', 'company_success'],
                'communication_style': 'motivational'
            }
        }
    
    def _calculate_story_quality(self) -> float:
        """Calculate overall story quality score."""
        total_strength = sum([
            story.get('narrative_strength', 0) 
            for story in self.generated_stories.values() 
            if isinstance(story, dict) and 'narrative_strength' in story
        ])
        return min(total_strength / 4, 1.0)  # Normalize to 0-1
    
    def _generate_fallback_story(self, audience: str) -> Dict[str, Any]:
        """Generate fallback story when main generation fails."""
        return {
            'audience': audience,
            'story_type': 'fallback_narrative',
            'sections': {
                'overview': f"A compelling story for {audience} highlighting our key strengths and achievements."
            },
            'key_metrics': [],
            'headlines': [f"Excellence in Action for {audience.title()}"],
            'call_to_action': f"Learn more about our value proposition for {audience}.",
            'supporting_data': [],
            'narrative_strength': 0.5
        }
    
    # Additional narrative building methods (simplified for brevity)
    def _build_competitive_narrative(self, insights: List[Dict], trends: Dict) -> str:
        return "Our competitive advantages are built on innovation, sustainability leadership, and deep market expertise."
    
    def _build_growth_narrative(self, insights: List[Dict], themes: Dict) -> str:
        return "Strategic growth initiatives focus on market expansion, product innovation, and operational excellence."
    
    def _build_risk_narrative(self, insights: List[Dict], trends: Dict) -> str:
        return "Comprehensive risk management and diversified strategy provide resilience and stability."
    
    def _build_investment_thesis(self, insights: List[Dict], themes: Dict) -> str:
        return "Strong fundamentals, market opportunity, and execution capability create compelling investment opportunity."
    
    def _build_solution_narrative(self, insights: List[Dict], operational_trends: Dict) -> str:
        return "Our solutions combine cutting-edge technology with deep industry expertise to deliver exceptional results."
    
    def _build_sustainability_narrative(self, insights: List[Dict], sustainability_trends: Dict) -> str:
        return "Leading sustainability practices create value for stakeholders while driving positive environmental and social impact."
    
    def _build_innovation_narrative(self, insights: List[Dict], operational_trends: Dict) -> str:
        return "Continuous innovation and R&D investment ensure we stay ahead of market trends and client needs."
    
    def _build_success_narrative(self, insights: List[Dict], trends: Dict) -> str:
        return "Client success stories demonstrate our ability to deliver measurable value and lasting partnerships."
    
    def _build_partnership_narrative(self, insights: List[Dict], themes: Dict) -> str:
        return "We build long-term partnerships based on trust, expertise, and shared commitment to success."
    
    def _build_roadmap_narrative(self, insights: List[Dict], themes: Dict) -> str:
        return "Our innovation roadmap focuses on emerging technologies and evolving client needs."
    
    def _build_achievement_narrative(self, insights: List[Dict], operational_trends: Dict) -> str:
        return "Team achievements across all areas demonstrate our collective commitment to excellence."
    
    def _build_opportunity_narrative(self, insights: List[Dict], trends: Dict) -> str:
        return "Growth opportunities provide exciting career development and professional advancement paths."
    
    def _build_culture_narrative(self, insights: List[Dict], sustainability_trends: Dict) -> str:
        return "Our culture values innovation, sustainability, and inclusive collaboration."
    
    def _build_impact_narrative(self, insights: List[Dict], operational_trends: Dict) -> str:
        return "Our work creates meaningful impact for clients, communities, and the environment."
    
    def _build_vision_narrative(self, insights: List[Dict], themes: Dict) -> str:
        return "Our vision of sustainable business leadership guides everything we do."
    
    def _build_recognition_narrative(self, insights: List[Dict], trends: Dict) -> str:
        return "Industry recognition and awards validate our commitment to excellence and innovation."
    
    def _build_overview_narrative(self, insights: List[Dict], themes: Dict) -> str:
        return "We are a leading company focused on sustainable innovation and value creation."
    
    def _build_general_achievements(self, insights: List[Dict], trends: Dict) -> str:
        return "Key achievements across financial performance, sustainability, and innovation demonstrate our comprehensive excellence."
    
    def _build_outlook_narrative(self, insights: List[Dict], themes: Dict) -> str:
        return "Strong market position and strategic initiatives position us for continued success and growth."
