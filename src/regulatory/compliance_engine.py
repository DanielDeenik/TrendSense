"""
Regulatory Compliance Engine for TrendSense™

This module provides comprehensive regulatory compliance assessment
for major ESG frameworks including CSRD, SFDR, EU Taxonomy, and TCFD.
"""

import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from abc import ABC, abstractmethod

# Configure logging
logger = logging.getLogger(__name__)


class ComplianceMapper(ABC):
    """Base class for regulatory compliance mappers"""
    
    def __init__(self, framework_name: str):
        self.framework_name = framework_name
        self.requirements = {}
        self.scoring_weights = {}
        
    @abstractmethod
    def calculate_score(self, company_data: Dict[str, Any]) -> float:
        """Calculate compliance score"""
        pass
    
    @abstractmethod
    def identify_gaps(self, company_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify compliance gaps"""
        pass
    
    @abstractmethod
    def generate_recommendations(self, company_data: Dict[str, Any]) -> List[str]:
        """Generate compliance recommendations"""
        pass
    
    def create_audit_trail(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create audit trail for compliance assessment"""
        return {
            'framework': self.framework_name,
            'assessment_date': datetime.now().isoformat(),
            'company_id': company_data.get('id', 'unknown'),
            'data_sources': self._identify_data_sources(company_data),
            'methodology': f'{self.framework_name} Compliance Assessment',
            'assessor': 'TrendSense Compliance Engine'
        }
    
    def generate_report(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate compliance report"""
        score = self.calculate_score(company_data)
        gaps = self.identify_gaps(company_data)
        recommendations = self.generate_recommendations(company_data)
        audit_trail = self.create_audit_trail(company_data)
        
        return {
            'framework': self.framework_name,
            'company_id': company_data.get('id', 'unknown'),
            'company_name': company_data.get('name', 'Unknown Company'),
            'assessment_date': datetime.now().isoformat(),
            'compliance_score': score,
            'compliance_level': self._assess_compliance_level(score),
            'gaps_identified': len(gaps),
            'gaps': gaps,
            'recommendations': recommendations,
            'audit_trail': audit_trail,
            'next_assessment_due': self._calculate_next_assessment_date()
        }
    
    def _identify_data_sources(self, company_data: Dict[str, Any]) -> List[str]:
        """Identify data sources used in assessment"""
        sources = []
        
        if 'provider' in company_data:
            sources.append(company_data['provider'])
        
        if 'sustainability_metrics' in company_data:
            sources.append('Internal Sustainability Metrics')
        
        if 'financial_metrics' in company_data:
            sources.append('Financial Data')
        
        if 'esg_scores' in company_data:
            sources.append('ESG Scores')
        
        return sources
    
    def _assess_compliance_level(self, score: float) -> str:
        """Assess compliance level based on score"""
        if score >= 90:
            return "Fully Compliant"
        elif score >= 80:
            return "Largely Compliant"
        elif score >= 70:
            return "Partially Compliant"
        elif score >= 60:
            return "Minimally Compliant"
        else:
            return "Non-Compliant"
    
    def _calculate_next_assessment_date(self) -> str:
        """Calculate next assessment due date"""
        from datetime import timedelta
        next_date = datetime.now() + timedelta(days=365)  # Annual assessment
        return next_date.isoformat()


class RegulatoryComplianceEngine:
    """Comprehensive regulatory compliance framework"""
    
    def __init__(self):
        """Initialize compliance engine with framework mappers"""
        self.frameworks = {}
        self._initialize_frameworks()
    
    def _initialize_frameworks(self):
        """Initialize compliance framework mappers"""
        try:
            from .csrd_mapper import CSRDComplianceMapper
            from .sfdr_mapper import SFDRComplianceMapper
            from .eu_taxonomy_mapper import EUTaxonomyMapper
            from .tcfd_mapper import TCFDMapper
            
            self.frameworks = {
                'CSRD': CSRDComplianceMapper(),
                'SFDR': SFDRComplianceMapper(),
                'EU_TAXONOMY': EUTaxonomyMapper(),
                'TCFD': TCFDMapper()
            }
        except ImportError as e:
            logger.warning(f"Some compliance mappers not available: {str(e)}")
            # Initialize with mock mappers for development
            self.frameworks = {
                'CSRD': MockComplianceMapper('CSRD'),
                'SFDR': MockComplianceMapper('SFDR'),
                'EU_TAXONOMY': MockComplianceMapper('EU_TAXONOMY'),
                'TCFD': MockComplianceMapper('TCFD')
            }
    
    def assess_compliance(self, company_data: Dict[str, Any], 
                         framework: str) -> Dict[str, Any]:
        """
        Assess compliance with specific regulatory framework.
        
        Args:
            company_data: Company data for assessment
            framework: Regulatory framework name
            
        Returns:
            Compliance assessment results
        """
        framework = framework.upper()
        
        if framework not in self.frameworks:
            raise ValueError(f"Unsupported framework: {framework}")
        
        mapper = self.frameworks[framework]
        
        try:
            return {
                'framework': framework,
                'compliance_score': mapper.calculate_score(company_data),
                'missing_requirements': mapper.identify_gaps(company_data),
                'recommendations': mapper.generate_recommendations(company_data),
                'audit_trail': mapper.create_audit_trail(company_data),
                'reporting_template': mapper.generate_report(company_data),
                'assessment_timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error assessing {framework} compliance: {str(e)}")
            return {
                'framework': framework,
                'compliance_score': 0,
                'missing_requirements': [{'requirement': 'Assessment failed', 'severity': 'High'}],
                'recommendations': ['Review data quality and completeness'],
                'audit_trail': {'error': str(e)},
                'reporting_template': {},
                'assessment_timestamp': datetime.now().isoformat()
            }
    
    def assess_all_frameworks(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess compliance across all supported frameworks.
        
        Args:
            company_data: Company data for assessment
            
        Returns:
            Multi-framework compliance assessment
        """
        results = {}
        overall_scores = []
        
        for framework_name in self.frameworks.keys():
            try:
                assessment = self.assess_compliance(company_data, framework_name)
                results[framework_name] = assessment
                overall_scores.append(assessment['compliance_score'])
            except Exception as e:
                logger.error(f"Error assessing {framework_name}: {str(e)}")
                results[framework_name] = {
                    'error': str(e),
                    'compliance_score': 0
                }
                overall_scores.append(0)
        
        # Calculate overall compliance score
        overall_score = sum(overall_scores) / len(overall_scores) if overall_scores else 0
        
        return {
            'company_id': company_data.get('id', 'unknown'),
            'assessment_date': datetime.now().isoformat(),
            'overall_compliance_score': overall_score,
            'framework_assessments': results,
            'summary': self._generate_compliance_summary(results, overall_score)
        }
    
    def _generate_compliance_summary(self, results: Dict[str, Any], 
                                   overall_score: float) -> Dict[str, Any]:
        """Generate compliance summary"""
        compliant_frameworks = []
        non_compliant_frameworks = []
        
        for framework, assessment in results.items():
            if isinstance(assessment, dict) and 'compliance_score' in assessment:
                score = assessment['compliance_score']
                if score >= 70:  # Threshold for compliance
                    compliant_frameworks.append(framework)
                else:
                    non_compliant_frameworks.append(framework)
        
        return {
            'overall_level': self._assess_overall_compliance_level(overall_score),
            'compliant_frameworks': compliant_frameworks,
            'non_compliant_frameworks': non_compliant_frameworks,
            'priority_actions': self._identify_priority_actions(results),
            'compliance_trend': 'Stable'  # Would be calculated from historical data
        }
    
    def _assess_overall_compliance_level(self, score: float) -> str:
        """Assess overall compliance level"""
        if score >= 85:
            return "Excellent Compliance"
        elif score >= 75:
            return "Good Compliance"
        elif score >= 65:
            return "Adequate Compliance"
        elif score >= 50:
            return "Poor Compliance"
        else:
            return "Critical Compliance Issues"
    
    def _identify_priority_actions(self, results: Dict[str, Any]) -> List[str]:
        """Identify priority compliance actions"""
        actions = []
        
        for framework, assessment in results.items():
            if isinstance(assessment, dict) and 'compliance_score' in assessment:
                score = assessment['compliance_score']
                if score < 70:
                    actions.append(f"Address {framework} compliance gaps")
        
        if not actions:
            actions.append("Maintain current compliance levels")
        
        return actions
    
    def get_supported_frameworks(self) -> List[str]:
        """Get list of supported regulatory frameworks"""
        return list(self.frameworks.keys())
    
    def get_framework_requirements(self, framework: str) -> Dict[str, Any]:
        """Get requirements for a specific framework"""
        framework = framework.upper()
        
        if framework not in self.frameworks:
            raise ValueError(f"Unsupported framework: {framework}")
        
        mapper = self.frameworks[framework]
        return {
            'framework': framework,
            'requirements': getattr(mapper, 'requirements', {}),
            'scoring_weights': getattr(mapper, 'scoring_weights', {}),
            'description': f"{framework} regulatory compliance requirements"
        }


class MockComplianceMapper(ComplianceMapper):
    """Mock compliance mapper for development/testing"""
    
    def __init__(self, framework_name: str):
        super().__init__(framework_name)
        
        # Mock requirements
        self.requirements = {
            'environmental_disclosure': {
                'required': True,
                'weight': 0.3,
                'description': 'Environmental impact disclosure'
            },
            'social_metrics': {
                'required': True,
                'weight': 0.25,
                'description': 'Social impact metrics'
            },
            'governance_structure': {
                'required': True,
                'weight': 0.25,
                'description': 'Governance structure documentation'
            },
            'risk_assessment': {
                'required': True,
                'weight': 0.2,
                'description': 'ESG risk assessment'
            }
        }
        
        self.scoring_weights = {req: details['weight'] for req, details in self.requirements.items()}
    
    def calculate_score(self, company_data: Dict[str, Any]) -> float:
        """Calculate mock compliance score"""
        total_score = 0
        total_weight = 0
        
        for requirement, details in self.requirements.items():
            weight = details['weight']
            
            # Mock scoring logic
            if self._has_requirement_data(company_data, requirement):
                score = 85  # Good compliance
            else:
                score = 30  # Poor compliance
            
            total_score += score * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0
    
    def identify_gaps(self, company_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify mock compliance gaps"""
        gaps = []
        
        for requirement, details in self.requirements.items():
            if not self._has_requirement_data(company_data, requirement):
                gaps.append({
                    'requirement': requirement,
                    'description': details['description'],
                    'severity': 'High' if details['required'] else 'Medium',
                    'framework': self.framework_name
                })
        
        return gaps
    
    def generate_recommendations(self, company_data: Dict[str, Any]) -> List[str]:
        """Generate mock recommendations"""
        recommendations = []
        gaps = self.identify_gaps(company_data)
        
        for gap in gaps:
            recommendations.append(
                f"Implement {gap['description'].lower()} to meet {self.framework_name} requirements"
            )
        
        if not recommendations:
            recommendations.append(f"Maintain current {self.framework_name} compliance standards")
        
        return recommendations
    
    def _has_requirement_data(self, company_data: Dict[str, Any], requirement: str) -> bool:
        """Check if company has data for requirement"""
        # Mock logic to check data availability
        if requirement == 'environmental_disclosure':
            return 'sustainability_metrics' in company_data or 'esg_scores' in company_data
        elif requirement == 'social_metrics':
            return 'sustainability_metrics' in company_data
        elif requirement == 'governance_structure':
            return 'esg_scores' in company_data
        elif requirement == 'risk_assessment':
            return 'esg_scores' in company_data
        
        return False


def get_compliance_engine() -> RegulatoryComplianceEngine:
    """
    Get a regulatory compliance engine instance.
    
    Returns:
        Regulatory compliance engine
    """
    return RegulatoryComplianceEngine()
