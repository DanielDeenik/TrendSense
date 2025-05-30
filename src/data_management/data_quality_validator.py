"""
Data Quality Validator for TrendSense™

This module provides comprehensive data quality validation to ensure
institutional-grade data reliability and accuracy.
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import statistics

# Configure logging
logger = logging.getLogger(__name__)


class DataQualityValidator(ABC):
    """Base class for data quality validation"""
    
    def __init__(self, quality_thresholds: Dict[str, float] = None):
        """
        Initialize data quality validator.
        
        Args:
            quality_thresholds: Minimum quality thresholds for different metrics
        """
        self.quality_thresholds = quality_thresholds or {
            'completeness': 0.8,  # 80% data completeness
            'accuracy': 0.9,      # 90% accuracy
            'consistency': 0.85,  # 85% consistency
            'timeliness': 0.9,    # 90% timeliness
            'validity': 0.95      # 95% validity
        }
    
    @abstractmethod
    def validate_data(self, data: Any) -> Dict[str, Any]:
        """Validate data quality"""
        pass
    
    def calculate_overall_quality_score(self, quality_metrics: Dict[str, float]) -> float:
        """
        Calculate overall data quality score.
        
        Args:
            quality_metrics: Individual quality metrics
            
        Returns:
            Overall quality score (0-100)
        """
        weights = {
            'completeness': 0.25,
            'accuracy': 0.30,
            'consistency': 0.20,
            'timeliness': 0.15,
            'validity': 0.10
        }
        
        weighted_score = 0
        total_weight = 0
        
        for metric, score in quality_metrics.items():
            if metric in weights:
                weighted_score += score * weights[metric]
                total_weight += weights[metric]
        
        return (weighted_score / total_weight) * 100 if total_weight > 0 else 0
    
    def assess_quality_level(self, quality_score: float) -> str:
        """
        Assess quality level based on score.
        
        Args:
            quality_score: Overall quality score
            
        Returns:
            Quality level description
        """
        if quality_score >= 90:
            return "Excellent"
        elif quality_score >= 80:
            return "Good"
        elif quality_score >= 70:
            return "Acceptable"
        elif quality_score >= 60:
            return "Poor"
        else:
            return "Unacceptable"


class ESGDataValidator(DataQualityValidator):
    """ESG-specific data quality validator"""
    
    def __init__(self, quality_thresholds: Dict[str, float] = None):
        super().__init__(quality_thresholds)
        
        # ESG-specific validation rules
        self.esg_score_ranges = {
            'environmental': (0, 100),
            'social': (0, 100),
            'governance': (0, 100),
            'combined': (0, 100),
            'percentile_rank': (0, 100)
        }
        
        self.required_fields = [
            'company_id',
            'timestamp',
            'esg_scores',
            'data_quality'
        ]
        
        # Maximum age for data to be considered timely (in days)
        self.max_data_age_days = 90
    
    def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate ESG data quality.
        
        Args:
            data: ESG data to validate
            
        Returns:
            Validation results with quality metrics
        """
        validation_results = {
            'is_valid': True,
            'quality_metrics': {},
            'issues': [],
            'recommendations': [],
            'overall_score': 0,
            'quality_level': 'Unknown'
        }
        
        try:
            # Validate completeness
            completeness_score = self._validate_completeness(data)
            validation_results['quality_metrics']['completeness'] = completeness_score
            
            # Validate accuracy
            accuracy_score = self._validate_accuracy(data)
            validation_results['quality_metrics']['accuracy'] = accuracy_score
            
            # Validate consistency
            consistency_score = self._validate_consistency(data)
            validation_results['quality_metrics']['consistency'] = consistency_score
            
            # Validate timeliness
            timeliness_score = self._validate_timeliness(data)
            validation_results['quality_metrics']['timeliness'] = timeliness_score
            
            # Validate validity
            validity_score = self._validate_validity(data)
            validation_results['quality_metrics']['validity'] = validity_score
            
            # Calculate overall quality score
            overall_score = self.calculate_overall_quality_score(
                validation_results['quality_metrics']
            )
            validation_results['overall_score'] = overall_score
            validation_results['quality_level'] = self.assess_quality_level(overall_score)
            
            # Determine if data meets minimum quality standards
            validation_results['is_valid'] = all(
                score >= self.quality_thresholds.get(metric, 0.8)
                for metric, score in validation_results['quality_metrics'].items()
            )
            
            # Generate recommendations
            validation_results['recommendations'] = self._generate_recommendations(
                validation_results['quality_metrics']
            )
            
        except Exception as e:
            logger.error(f"Error validating ESG data: {str(e)}")
            validation_results['is_valid'] = False
            validation_results['issues'].append(f"Validation error: {str(e)}")
        
        return validation_results
    
    def _validate_completeness(self, data: Dict[str, Any]) -> float:
        """Validate data completeness"""
        total_fields = 0
        complete_fields = 0
        
        # Check required fields
        for field in self.required_fields:
            total_fields += 1
            if field in data and data[field] is not None:
                complete_fields += 1
        
        # Check ESG scores completeness
        if 'esg_scores' in data and isinstance(data['esg_scores'], dict):
            for score_type in self.esg_score_ranges.keys():
                total_fields += 1
                if score_type in data['esg_scores'] and data['esg_scores'][score_type] is not None:
                    complete_fields += 1
        
        # Check metrics completeness if present
        if 'metrics' in data and isinstance(data['metrics'], dict):
            metrics_count = len(data['metrics'])
            if metrics_count > 0:
                non_null_metrics = sum(1 for v in data['metrics'].values() if v is not None)
                total_fields += metrics_count
                complete_fields += non_null_metrics
        
        return complete_fields / total_fields if total_fields > 0 else 0
    
    def _validate_accuracy(self, data: Dict[str, Any]) -> float:
        """Validate data accuracy"""
        accuracy_score = 1.0
        issues = []
        
        # Check ESG score ranges
        if 'esg_scores' in data and isinstance(data['esg_scores'], dict):
            for score_type, (min_val, max_val) in self.esg_score_ranges.items():
                if score_type in data['esg_scores']:
                    score = data['esg_scores'][score_type]
                    if isinstance(score, (int, float)):
                        if not (min_val <= score <= max_val):
                            accuracy_score -= 0.1
                            issues.append(f"{score_type} score {score} out of range [{min_val}, {max_val}]")
        
        # Check for logical consistency in scores
        if 'esg_scores' in data:
            scores = data['esg_scores']
            if all(key in scores for key in ['environmental', 'social', 'governance', 'combined']):
                calculated_combined = (
                    scores['environmental'] + scores['social'] + scores['governance']
                ) / 3
                actual_combined = scores['combined']
                
                if abs(calculated_combined - actual_combined) > 5:  # Allow 5-point tolerance
                    accuracy_score -= 0.15
                    issues.append("Combined ESG score inconsistent with component scores")
        
        # Check data quality indicators
        if 'data_quality' in data and isinstance(data['data_quality'], dict):
            confidence = data['data_quality'].get('confidence_score', 0)
            if isinstance(confidence, (int, float)) and confidence < 70:
                accuracy_score -= 0.1
                issues.append("Low confidence score from data provider")
        
        return max(0, accuracy_score)
    
    def _validate_consistency(self, data: Dict[str, Any]) -> float:
        """Validate data consistency"""
        consistency_score = 1.0
        
        # Check provider consistency
        provider = data.get('provider', '')
        if not provider:
            consistency_score -= 0.2
        
        # Check timestamp format consistency
        timestamp = data.get('timestamp', '')
        if timestamp:
            try:
                datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except ValueError:
                consistency_score -= 0.1
        
        # Check data structure consistency
        if 'esg_scores' in data:
            if not isinstance(data['esg_scores'], dict):
                consistency_score -= 0.3
        
        if 'metrics' in data:
            if not isinstance(data['metrics'], dict):
                consistency_score -= 0.2
        
        return max(0, consistency_score)
    
    def _validate_timeliness(self, data: Dict[str, Any]) -> float:
        """Validate data timeliness"""
        timeliness_score = 1.0
        
        # Check main timestamp
        timestamp = data.get('timestamp')
        if timestamp:
            try:
                data_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                age_days = (datetime.now() - data_time.replace(tzinfo=None)).days
                
                if age_days > self.max_data_age_days:
                    # Gradual degradation based on age
                    excess_days = age_days - self.max_data_age_days
                    timeliness_score -= min(0.5, excess_days / 365)  # Max 50% penalty for very old data
            except ValueError:
                timeliness_score -= 0.3
        else:
            timeliness_score -= 0.4
        
        # Check data quality last_updated if available
        if 'data_quality' in data and isinstance(data['data_quality'], dict):
            last_updated = data['data_quality'].get('last_updated')
            if last_updated:
                try:
                    update_time = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
                    age_days = (datetime.now() - update_time.replace(tzinfo=None)).days
                    
                    if age_days > self.max_data_age_days:
                        timeliness_score -= 0.2
                except ValueError:
                    timeliness_score -= 0.1
        
        return max(0, timeliness_score)
    
    def _validate_validity(self, data: Dict[str, Any]) -> float:
        """Validate data validity"""
        validity_score = 1.0
        
        # Check for required fields
        for field in self.required_fields:
            if field not in data:
                validity_score -= 0.2
        
        # Check company_id format
        company_id = data.get('company_id', '')
        if not company_id or len(company_id) < 2:
            validity_score -= 0.1
        
        # Check for error indicators
        if 'error' in data:
            validity_score -= 0.3
        
        # Check if data is marked as mock/test data
        if data.get('is_mock', False):
            validity_score -= 0.2
        
        return max(0, validity_score)
    
    def _generate_recommendations(self, quality_metrics: Dict[str, float]) -> List[str]:
        """Generate recommendations based on quality metrics"""
        recommendations = []
        
        for metric, score in quality_metrics.items():
            threshold = self.quality_thresholds.get(metric, 0.8)
            
            if score < threshold:
                if metric == 'completeness':
                    recommendations.append(
                        "Improve data completeness by ensuring all required ESG metrics are provided"
                    )
                elif metric == 'accuracy':
                    recommendations.append(
                        "Verify ESG score calculations and ensure values are within expected ranges"
                    )
                elif metric == 'consistency':
                    recommendations.append(
                        "Standardize data formats and ensure consistent data structure across sources"
                    )
                elif metric == 'timeliness':
                    recommendations.append(
                        "Update data more frequently to ensure timeliness of ESG information"
                    )
                elif metric == 'validity':
                    recommendations.append(
                        "Validate data sources and ensure all required fields are properly populated"
                    )
        
        return recommendations
    
    def validate_multiple_sources(self, data_sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate data from multiple ESG providers and identify discrepancies.
        
        Args:
            data_sources: List of ESG data from different providers
            
        Returns:
            Cross-validation results
        """
        if len(data_sources) < 2:
            return {
                'cross_validation_possible': False,
                'reason': 'Need at least 2 data sources for cross-validation'
            }
        
        # Extract ESG scores from all sources
        all_scores = {}
        for i, source in enumerate(data_sources):
            provider = source.get('provider', f'Provider_{i}')
            if 'esg_scores' in source:
                all_scores[provider] = source['esg_scores']
        
        # Calculate score variations
        score_variations = {}
        for score_type in ['environmental', 'social', 'governance', 'combined']:
            scores = []
            for provider_scores in all_scores.values():
                if score_type in provider_scores and isinstance(provider_scores[score_type], (int, float)):
                    scores.append(provider_scores[score_type])
            
            if len(scores) >= 2:
                score_variations[score_type] = {
                    'mean': statistics.mean(scores),
                    'std_dev': statistics.stdev(scores) if len(scores) > 1 else 0,
                    'min': min(scores),
                    'max': max(scores),
                    'range': max(scores) - min(scores),
                    'coefficient_of_variation': statistics.stdev(scores) / statistics.mean(scores) if statistics.mean(scores) > 0 else 0
                }
        
        # Assess cross-validation quality
        avg_cv = statistics.mean([
            var['coefficient_of_variation'] for var in score_variations.values()
        ]) if score_variations else 1.0
        
        cross_validation_score = max(0, 1 - avg_cv)  # Lower CV = higher quality
        
        return {
            'cross_validation_possible': True,
            'cross_validation_score': cross_validation_score,
            'score_variations': score_variations,
            'consensus_scores': {
                score_type: var['mean'] for score_type, var in score_variations.items()
            },
            'reliability_assessment': self._assess_cross_validation_reliability(cross_validation_score),
            'discrepancy_flags': self._identify_discrepancies(score_variations)
        }
    
    def _assess_cross_validation_reliability(self, cv_score: float) -> str:
        """Assess reliability based on cross-validation score"""
        if cv_score >= 0.9:
            return "High reliability - strong consensus across providers"
        elif cv_score >= 0.8:
            return "Good reliability - reasonable consensus across providers"
        elif cv_score >= 0.7:
            return "Moderate reliability - some variation across providers"
        elif cv_score >= 0.6:
            return "Low reliability - significant variation across providers"
        else:
            return "Poor reliability - major discrepancies across providers"
    
    def _identify_discrepancies(self, score_variations: Dict[str, Dict[str, float]]) -> List[str]:
        """Identify significant discrepancies in scores"""
        discrepancies = []
        
        for score_type, variation in score_variations.items():
            if variation['range'] > 30:  # More than 30-point difference
                discrepancies.append(
                    f"Large discrepancy in {score_type} scores (range: {variation['range']:.1f} points)"
                )
            elif variation['coefficient_of_variation'] > 0.3:  # High relative variation
                discrepancies.append(
                    f"High variation in {score_type} scores (CV: {variation['coefficient_of_variation']:.2f})"
                )
        
        return discrepancies


def get_data_quality_validator(validator_type: str = 'esg') -> DataQualityValidator:
    """
    Get a data quality validator.
    
    Args:
        validator_type: Type of validator ('esg', 'general')
        
    Returns:
        Data quality validator instance
    """
    if validator_type.lower() == 'esg':
        return ESGDataValidator()
    else:
        # For now, return ESG validator as default
        # Can be extended with other validator types
        return ESGDataValidator()
