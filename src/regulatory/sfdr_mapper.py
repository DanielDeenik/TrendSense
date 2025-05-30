"""
SFDR (Sustainable Finance Disclosure Regulation) Compliance Mapper

This module provides comprehensive SFDR compliance assessment based on
the European Union's Sustainable Finance Disclosure Regulation requirements.
"""

import logging
from typing import Dict, List, Any
from .compliance_engine import ComplianceMapper

# Configure logging
logger = logging.getLogger(__name__)


class SFDRComplianceMapper(ComplianceMapper):
    """SFDR-specific compliance mapping and assessment"""
    
    def __init__(self):
        super().__init__("SFDR")
        
        # SFDR requirements based on Articles 6, 8, and 9
        self.requirements = {
            # Article 6 - Entity Level Disclosures
            'sustainability_risk_integration': {
                'required': True,
                'weight': 0.20,
                'description': 'Integration of sustainability risks in investment decisions',
                'article': 'Article 6',
                'sub_requirements': [
                    'sustainability_risk_policy',
                    'risk_assessment_procedures',
                    'investment_decision_integration',
                    'due_diligence_processes'
                ]
            },
            
            'adverse_sustainability_impacts': {
                'required': True,
                'weight': 0.25,
                'description': 'Principal adverse impacts on sustainability factors',
                'article': 'Article 4',
                'sub_requirements': [
                    'pai_statement',
                    'pai_indicators',
                    'engagement_policies',
                    'adherence_standards'
                ]
            },
            
            # Article 8 - Light Green Products
            'environmental_social_promotion': {
                'required': False,  # Only for Article 8 products
                'weight': 0.20,
                'description': 'Environmental or social characteristics promotion',
                'article': 'Article 8',
                'sub_requirements': [
                    'environmental_characteristics',
                    'social_characteristics',
                    'investment_strategy',
                    'proportion_investments',
                    'monitoring_characteristics'
                ]
            },
            
            # Article 9 - Dark Green Products
            'sustainable_investment_objective': {
                'required': False,  # Only for Article 9 products
                'weight': 0.20,
                'description': 'Sustainable investment as objective',
                'article': 'Article 9',
                'sub_requirements': [
                    'sustainable_investment_definition',
                    'sustainability_indicators',
                    'investment_strategy_alignment',
                    'designated_index',
                    'no_significant_harm'
                ]
            },
            
            # Taxonomy Regulation Integration
            'taxonomy_alignment': {
                'required': True,
                'weight': 0.15,
                'description': 'EU Taxonomy alignment disclosures',
                'article': 'Taxonomy Regulation',
                'sub_requirements': [
                    'taxonomy_eligible_activities',
                    'taxonomy_aligned_activities',
                    'do_no_significant_harm',
                    'minimum_safeguards'
                ]
            }
        }
        
        # Principal Adverse Impact (PAI) indicators
        self.pai_indicators = {
            # Climate and environment
            'ghg_emissions': {'mandatory': True, 'category': 'Climate'},
            'carbon_footprint': {'mandatory': True, 'category': 'Climate'},
            'ghg_intensity': {'mandatory': True, 'category': 'Climate'},
            'fossil_fuel_exposure': {'mandatory': True, 'category': 'Climate'},
            'energy_consumption_intensity': {'mandatory': True, 'category': 'Environment'},
            'biodiversity_impact': {'mandatory': True, 'category': 'Environment'},
            'water_emissions': {'mandatory': True, 'category': 'Environment'},
            'hazardous_waste': {'mandatory': True, 'category': 'Environment'},
            
            # Social and governance
            'ungc_compliance': {'mandatory': True, 'category': 'Social'},
            'board_gender_diversity': {'mandatory': True, 'category': 'Social'},
            'controversial_weapons': {'mandatory': True, 'category': 'Social'},
            'human_rights_violations': {'mandatory': True, 'category': 'Social'},
            'corruption_bribery': {'mandatory': True, 'category': 'Governance'},
            'excessive_ceo_pay': {'mandatory': True, 'category': 'Governance'}
        }
        
        # Scoring weights for each requirement
        self.scoring_weights = {req: details['weight'] for req, details in self.requirements.items()}
    
    def calculate_score(self, company_data: Dict[str, Any]) -> float:
        """
        Calculate SFDR compliance score.
        
        Args:
            company_data: Company data for assessment
            
        Returns:
            SFDR compliance score (0-100)
        """
        total_score = 0
        total_weight = 0
        
        # Determine product classification
        product_type = self._determine_product_type(company_data)
        
        for requirement, details in self.requirements.items():
            # Skip Article 8/9 requirements if not applicable
            if not details['required'] and not self._is_requirement_applicable(requirement, product_type):
                continue
            
            weight = details['weight']
            requirement_score = self._assess_requirement(company_data, requirement, details)
            
            total_score += requirement_score * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0
    
    def _determine_product_type(self, company_data: Dict[str, Any]) -> str:
        """Determine SFDR product classification"""
        # This would typically be provided in the data
        # For now, we'll infer from available data
        
        if 'sfdr_classification' in company_data:
            return company_data['sfdr_classification']
        
        # Infer from ESG scores and sustainability focus
        esg_scores = company_data.get('esg_scores', {})
        combined_score = esg_scores.get('combined', 0)
        
        if combined_score >= 80:
            return 'Article 9'  # Dark green
        elif combined_score >= 60:
            return 'Article 8'  # Light green
        else:
            return 'Article 6'  # Basic
    
    def _is_requirement_applicable(self, requirement: str, product_type: str) -> bool:
        """Check if requirement is applicable to product type"""
        if requirement == 'environmental_social_promotion':
            return product_type in ['Article 8', 'Article 9']
        elif requirement == 'sustainable_investment_objective':
            return product_type == 'Article 9'
        
        return True
    
    def _assess_requirement(self, company_data: Dict[str, Any], 
                          requirement: str, details: Dict[str, Any]) -> float:
        """Assess individual SFDR requirement"""
        
        if requirement == 'sustainability_risk_integration':
            return self._assess_sustainability_risk_integration(company_data)
        elif requirement == 'adverse_sustainability_impacts':
            return self._assess_adverse_impacts(company_data)
        elif requirement == 'environmental_social_promotion':
            return self._assess_environmental_social_promotion(company_data)
        elif requirement == 'sustainable_investment_objective':
            return self._assess_sustainable_investment_objective(company_data)
        elif requirement == 'taxonomy_alignment':
            return self._assess_taxonomy_alignment(company_data)
        
        return 0
    
    def _assess_sustainability_risk_integration(self, company_data: Dict[str, Any]) -> float:
        """Assess sustainability risk integration (Article 6)"""
        score = 0
        
        # Check for ESG risk assessment
        if 'esg_scores' in company_data:
            score += 30
        
        # Check for sustainability metrics
        if 'sustainability_metrics' in company_data:
            score += 25
        
        # Check for risk management processes
        if 'risk_assessment' in company_data:
            score += 25
        
        # Check for investment policy
        if 'investment_policy' in company_data or 'strategy' in company_data:
            score += 20
        
        return score
    
    def _assess_adverse_impacts(self, company_data: Dict[str, Any]) -> float:
        """Assess principal adverse impacts assessment"""
        score = 0
        total_indicators = len(self.pai_indicators)
        covered_indicators = 0
        
        # Check coverage of mandatory PAI indicators
        for indicator, details in self.pai_indicators.items():
            if self._has_pai_indicator_data(company_data, indicator):
                covered_indicators += 1
        
        # Score based on PAI indicator coverage
        coverage_score = (covered_indicators / total_indicators) * 70
        score += coverage_score
        
        # Check for PAI statement
        if 'pai_statement' in company_data:
            score += 15
        
        # Check for engagement policies
        if 'engagement_policy' in company_data:
            score += 15
        
        return score
    
    def _assess_environmental_social_promotion(self, company_data: Dict[str, Any]) -> float:
        """Assess environmental/social characteristics promotion (Article 8)"""
        score = 0
        
        # Check for environmental characteristics
        env_score = company_data.get('esg_scores', {}).get('environmental', 0)
        if env_score >= 70:
            score += 40
        elif env_score >= 50:
            score += 25
        
        # Check for social characteristics
        social_score = company_data.get('esg_scores', {}).get('social', 0)
        if social_score >= 70:
            score += 40
        elif social_score >= 50:
            score += 25
        
        # Check for investment strategy alignment
        if 'investment_strategy' in company_data:
            score += 20
        
        return min(100, score)
    
    def _assess_sustainable_investment_objective(self, company_data: Dict[str, Any]) -> float:
        """Assess sustainable investment objective (Article 9)"""
        score = 0
        
        # Check for high ESG scores
        combined_score = company_data.get('esg_scores', {}).get('combined', 0)
        if combined_score >= 80:
            score += 50
        elif combined_score >= 70:
            score += 30
        
        # Check for sustainability indicators
        if 'sustainability_indicators' in company_data:
            score += 25
        
        # Check for do no significant harm assessment
        if 'dnsh_assessment' in company_data:
            score += 25
        
        return score
    
    def _assess_taxonomy_alignment(self, company_data: Dict[str, Any]) -> float:
        """Assess EU Taxonomy alignment"""
        score = 0
        
        # Check for taxonomy-eligible activities
        if 'taxonomy_eligible' in company_data:
            score += 30
        
        # Check for taxonomy-aligned activities
        if 'taxonomy_aligned' in company_data:
            score += 40
        
        # Check for DNSH compliance
        if 'dnsh_compliance' in company_data:
            score += 15
        
        # Check for minimum safeguards
        if 'minimum_safeguards' in company_data:
            score += 15
        
        return score
    
    def _has_pai_indicator_data(self, company_data: Dict[str, Any], indicator: str) -> bool:
        """Check if company has data for specific PAI indicator"""
        metrics = company_data.get('metrics', {})
        sustainability_metrics = company_data.get('sustainability_metrics', {})
        
        # Map indicators to data fields
        indicator_mapping = {
            'ghg_emissions': ['carbon_emissions', 'ghg_emissions', 'scope_1_emissions'],
            'carbon_footprint': ['carbon_footprint', 'carbon_intensity'],
            'ghg_intensity': ['carbon_intensity', 'ghg_intensity'],
            'fossil_fuel_exposure': ['fossil_fuel_exposure', 'fossil_fuel_revenue'],
            'energy_consumption_intensity': ['energy_intensity', 'energy_consumption'],
            'biodiversity_impact': ['biodiversity_impact', 'biodiversity_score'],
            'water_emissions': ['water_pollutants', 'water_discharge'],
            'hazardous_waste': ['hazardous_waste', 'waste_hazardous'],
            'ungc_compliance': ['ungc_compliance', 'global_compact'],
            'board_gender_diversity': ['board_diversity', 'gender_diversity'],
            'controversial_weapons': ['controversial_weapons', 'weapons_involvement'],
            'human_rights_violations': ['human_rights_score', 'human_rights_violations'],
            'corruption_bribery': ['corruption_score', 'bribery_incidents'],
            'excessive_ceo_pay': ['executive_compensation', 'ceo_pay_ratio']
        }
        
        fields_to_check = indicator_mapping.get(indicator, [indicator])
        
        for field in fields_to_check:
            if field in metrics or field in sustainability_metrics:
                return True
        
        return False
    
    def identify_gaps(self, company_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Identify SFDR compliance gaps.
        
        Args:
            company_data: Company data for assessment
            
        Returns:
            List of compliance gaps
        """
        gaps = []
        product_type = self._determine_product_type(company_data)
        
        for requirement, details in self.requirements.items():
            # Skip non-applicable requirements
            if not details['required'] and not self._is_requirement_applicable(requirement, product_type):
                continue
            
            score = self._assess_requirement(company_data, requirement, details)
            
            if score < 70:  # Threshold for compliance
                severity = 'High' if score < 40 else 'Medium'
                
                gaps.append({
                    'requirement': requirement,
                    'description': details['description'],
                    'article': details['article'],
                    'current_score': score,
                    'target_score': 70,
                    'gap_size': 70 - score,
                    'severity': severity,
                    'framework': 'SFDR',
                    'product_type': product_type,
                    'sub_requirements': details.get('sub_requirements', [])
                })
        
        # Check PAI indicator gaps
        missing_pai_indicators = []
        for indicator, details in self.pai_indicators.items():
            if not self._has_pai_indicator_data(company_data, indicator):
                missing_pai_indicators.append(indicator)
        
        if missing_pai_indicators:
            gaps.append({
                'requirement': 'pai_indicators',
                'description': 'Missing Principal Adverse Impact indicators',
                'article': 'Article 4',
                'current_score': 0,
                'target_score': 100,
                'gap_size': 100,
                'severity': 'High',
                'framework': 'SFDR',
                'missing_indicators': missing_pai_indicators
            })
        
        return gaps
    
    def generate_recommendations(self, company_data: Dict[str, Any]) -> List[str]:
        """
        Generate SFDR compliance recommendations.
        
        Args:
            company_data: Company data for assessment
            
        Returns:
            List of recommendations
        """
        recommendations = []
        gaps = self.identify_gaps(company_data)
        product_type = self._determine_product_type(company_data)
        
        # Product classification recommendation
        recommendations.append(
            f"Current SFDR classification: {product_type}. "
            f"Consider alignment with appropriate disclosure requirements."
        )
        
        # Priority recommendations based on gaps
        high_priority_gaps = [gap for gap in gaps if gap['severity'] == 'High']
        
        if high_priority_gaps:
            recommendations.append(
                "Priority: Address high-severity SFDR compliance gaps immediately"
            )
        
        # PAI-specific recommendations
        pai_gaps = [gap for gap in gaps if gap['requirement'] == 'pai_indicators']
        if pai_gaps:
            missing_indicators = pai_gaps[0].get('missing_indicators', [])
            recommendations.append(
                f"Implement data collection for {len(missing_indicators)} missing PAI indicators"
            )
            
            # Specific PAI recommendations
            if 'ghg_emissions' in missing_indicators:
                recommendations.append(
                    "Establish comprehensive GHG emissions tracking (Scope 1, 2, 3)"
                )
            
            if 'board_gender_diversity' in missing_indicators:
                recommendations.append(
                    "Implement board diversity monitoring and reporting"
                )
        
        # Article-specific recommendations
        if product_type == 'Article 8':
            recommendations.append(
                "Enhance environmental and social characteristics documentation and monitoring"
            )
        elif product_type == 'Article 9':
            recommendations.append(
                "Strengthen sustainable investment objective evidence and measurement"
            )
        
        # Taxonomy alignment recommendations
        if not company_data.get('taxonomy_eligible'):
            recommendations.append(
                "Assess and document EU Taxonomy eligibility of business activities"
            )
        
        # General recommendations
        recommendations.append(
            "Establish regular SFDR compliance monitoring and reporting processes"
        )
        
        if len(gaps) > 3:
            recommendations.append(
                "Consider engaging SFDR compliance specialists for comprehensive assessment"
            )
        
        if not recommendations:
            recommendations.append(
                "Maintain current SFDR compliance standards and monitor regulatory updates"
            )
        
        return recommendations
    
    def get_pai_indicator_coverage(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get detailed PAI indicator coverage analysis.
        
        Args:
            company_data: Company data for assessment
            
        Returns:
            PAI coverage analysis
        """
        coverage = {
            'total_indicators': len(self.pai_indicators),
            'covered_indicators': 0,
            'missing_indicators': [],
            'coverage_by_category': {},
            'coverage_percentage': 0
        }
        
        # Analyze coverage by category
        categories = set(details['category'] for details in self.pai_indicators.values())
        for category in categories:
            coverage['coverage_by_category'][category] = {
                'total': 0,
                'covered': 0,
                'missing': []
            }
        
        # Check each indicator
        for indicator, details in self.pai_indicators.items():
            category = details['category']
            coverage['coverage_by_category'][category]['total'] += 1
            
            if self._has_pai_indicator_data(company_data, indicator):
                coverage['covered_indicators'] += 1
                coverage['coverage_by_category'][category]['covered'] += 1
            else:
                coverage['missing_indicators'].append(indicator)
                coverage['coverage_by_category'][category]['missing'].append(indicator)
        
        # Calculate percentages
        coverage['coverage_percentage'] = (
            coverage['covered_indicators'] / coverage['total_indicators'] * 100
        )
        
        for category in coverage['coverage_by_category']:
            cat_data = coverage['coverage_by_category'][category]
            cat_data['percentage'] = (
                cat_data['covered'] / cat_data['total'] * 100 if cat_data['total'] > 0 else 0
            )
        
        return coverage
