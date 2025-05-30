"""
Advanced ESG Scoring Engine for TrendSense™

This module provides sophisticated quantitative ESG scoring models to replace
basic High/Medium/Low categorizations with institutional-grade analytics.
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import statistics
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import joblib
import os

# Configure logging
logger = logging.getLogger(__name__)


class QuantitativeESGModel(ABC):
    """Base class for quantitative ESG models"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_importance = {}
        
    @abstractmethod
    def train(self, training_data: pd.DataFrame, target_column: str) -> Dict[str, Any]:
        """Train the model"""
        pass
    
    @abstractmethod
    def predict(self, features: Dict[str, Any]) -> Dict[str, float]:
        """Make predictions"""
        pass
    
    def save_model(self, filepath: str) -> bool:
        """Save trained model"""
        try:
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'feature_importance': self.feature_importance,
                'is_trained': self.is_trained,
                'model_name': self.model_name
            }
            joblib.dump(model_data, filepath)
            return True
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            return False
    
    def load_model(self, filepath: str) -> bool:
        """Load trained model"""
        try:
            if os.path.exists(filepath):
                model_data = joblib.load(filepath)
                self.model = model_data['model']
                self.scaler = model_data['scaler']
                self.feature_importance = model_data['feature_importance']
                self.is_trained = model_data['is_trained']
                return True
            return False
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False


class EnvironmentalScoreModel(QuantitativeESGModel):
    """Advanced environmental score model"""
    
    def __init__(self):
        super().__init__("Environmental Score Model")
        self.feature_weights = {
            'carbon_intensity': 0.25,
            'energy_efficiency': 0.20,
            'water_usage': 0.15,
            'waste_management': 0.15,
            'renewable_energy_pct': 0.15,
            'biodiversity_impact': 0.10
        }
    
    def train(self, training_data: pd.DataFrame, target_column: str = 'environmental_score') -> Dict[str, Any]:
        """Train environmental score model"""
        try:
            # Prepare features
            feature_columns = list(self.feature_weights.keys())
            available_features = [col for col in feature_columns if col in training_data.columns]
            
            if len(available_features) < 3:
                logger.warning("Insufficient features for training environmental model")
                return {'success': False, 'error': 'Insufficient features'}
            
            X = training_data[available_features].fillna(training_data[available_features].median())
            y = training_data[target_column].fillna(training_data[target_column].median())
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train Random Forest model
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                min_samples_split=5
            )
            self.model.fit(X_scaled, y)
            
            # Calculate feature importance
            self.feature_importance = dict(zip(available_features, self.model.feature_importances_))
            self.is_trained = True
            
            # Calculate training metrics
            train_score = self.model.score(X_scaled, y)
            
            return {
                'success': True,
                'training_score': train_score,
                'feature_importance': self.feature_importance,
                'features_used': available_features
            }
            
        except Exception as e:
            logger.error(f"Error training environmental model: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def predict(self, features: Dict[str, Any]) -> Dict[str, float]:
        """Predict environmental score"""
        if not self.is_trained:
            return self._fallback_prediction(features)
        
        try:
            # Prepare feature vector
            feature_vector = []
            used_features = []
            
            for feature in self.feature_importance.keys():
                if feature in features and features[feature] is not None:
                    feature_vector.append(float(features[feature]))
                    used_features.append(feature)
                else:
                    # Use median value for missing features
                    feature_vector.append(50.0)  # Assume 50 as median
                    used_features.append(feature)
            
            if not feature_vector:
                return self._fallback_prediction(features)
            
            # Scale and predict
            feature_array = np.array(feature_vector).reshape(1, -1)
            scaled_features = self.scaler.transform(feature_array)
            prediction = self.model.predict(scaled_features)[0]
            
            # Calculate confidence based on feature availability
            available_features = sum(1 for f in self.feature_importance.keys() if f in features and features[f] is not None)
            confidence = (available_features / len(self.feature_importance)) * 100
            
            return {
                'environmental_score': max(0, min(100, prediction)),
                'confidence': confidence,
                'features_used': used_features,
                'model_used': 'RandomForest'
            }
            
        except Exception as e:
            logger.error(f"Error predicting environmental score: {str(e)}")
            return self._fallback_prediction(features)
    
    def _fallback_prediction(self, features: Dict[str, Any]) -> Dict[str, float]:
        """Fallback prediction using weighted average"""
        total_score = 0
        total_weight = 0
        
        for feature, weight in self.feature_weights.items():
            if feature in features and features[feature] is not None:
                # Normalize feature value to 0-100 scale
                normalized_value = self._normalize_feature(feature, features[feature])
                total_score += normalized_value * weight
                total_weight += weight
        
        if total_weight > 0:
            score = total_score / total_weight
        else:
            score = 50.0  # Default neutral score
        
        return {
            'environmental_score': score,
            'confidence': (total_weight / sum(self.feature_weights.values())) * 100,
            'features_used': list(features.keys()),
            'model_used': 'Weighted Average (Fallback)'
        }
    
    def _normalize_feature(self, feature_name: str, value: float) -> float:
        """Normalize feature value to 0-100 scale"""
        # Feature-specific normalization logic
        if feature_name == 'carbon_intensity':
            # Lower is better for carbon intensity
            return max(0, min(100, 100 - (value / 10)))  # Assuming max 1000 units
        elif feature_name == 'energy_efficiency':
            # Higher is better for efficiency
            return max(0, min(100, value))
        elif feature_name == 'renewable_energy_pct':
            # Already in percentage
            return max(0, min(100, value))
        else:
            # Default normalization
            return max(0, min(100, value))


class SocialScoreModel(QuantitativeESGModel):
    """Advanced social score model"""
    
    def __init__(self):
        super().__init__("Social Score Model")
        self.feature_weights = {
            'employee_satisfaction': 0.20,
            'diversity_index': 0.18,
            'safety_record': 0.15,
            'community_investment': 0.12,
            'labor_practices': 0.15,
            'human_rights_score': 0.20
        }
    
    def train(self, training_data: pd.DataFrame, target_column: str = 'social_score') -> Dict[str, Any]:
        """Train social score model"""
        try:
            feature_columns = list(self.feature_weights.keys())
            available_features = [col for col in feature_columns if col in training_data.columns]
            
            if len(available_features) < 3:
                logger.warning("Insufficient features for training social model")
                return {'success': False, 'error': 'Insufficient features'}
            
            X = training_data[available_features].fillna(training_data[available_features].median())
            y = training_data[target_column].fillna(training_data[target_column].median())
            
            X_scaled = self.scaler.fit_transform(X)
            
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                min_samples_split=5
            )
            self.model.fit(X_scaled, y)
            
            self.feature_importance = dict(zip(available_features, self.model.feature_importances_))
            self.is_trained = True
            
            train_score = self.model.score(X_scaled, y)
            
            return {
                'success': True,
                'training_score': train_score,
                'feature_importance': self.feature_importance,
                'features_used': available_features
            }
            
        except Exception as e:
            logger.error(f"Error training social model: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def predict(self, features: Dict[str, Any]) -> Dict[str, float]:
        """Predict social score"""
        if not self.is_trained:
            return self._fallback_prediction(features)
        
        try:
            feature_vector = []
            used_features = []
            
            for feature in self.feature_importance.keys():
                if feature in features and features[feature] is not None:
                    feature_vector.append(float(features[feature]))
                    used_features.append(feature)
                else:
                    feature_vector.append(50.0)
                    used_features.append(feature)
            
            if not feature_vector:
                return self._fallback_prediction(features)
            
            feature_array = np.array(feature_vector).reshape(1, -1)
            scaled_features = self.scaler.transform(feature_array)
            prediction = self.model.predict(scaled_features)[0]
            
            available_features = sum(1 for f in self.feature_importance.keys() if f in features and features[f] is not None)
            confidence = (available_features / len(self.feature_importance)) * 100
            
            return {
                'social_score': max(0, min(100, prediction)),
                'confidence': confidence,
                'features_used': used_features,
                'model_used': 'RandomForest'
            }
            
        except Exception as e:
            logger.error(f"Error predicting social score: {str(e)}")
            return self._fallback_prediction(features)
    
    def _fallback_prediction(self, features: Dict[str, Any]) -> Dict[str, float]:
        """Fallback prediction using weighted average"""
        total_score = 0
        total_weight = 0
        
        for feature, weight in self.feature_weights.items():
            if feature in features and features[feature] is not None:
                normalized_value = max(0, min(100, float(features[feature])))
                total_score += normalized_value * weight
                total_weight += weight
        
        if total_weight > 0:
            score = total_score / total_weight
        else:
            score = 50.0
        
        return {
            'social_score': score,
            'confidence': (total_weight / sum(self.feature_weights.values())) * 100,
            'features_used': list(features.keys()),
            'model_used': 'Weighted Average (Fallback)'
        }


class GovernanceScoreModel(QuantitativeESGModel):
    """Advanced governance score model"""
    
    def __init__(self):
        super().__init__("Governance Score Model")
        self.feature_weights = {
            'board_independence': 0.25,
            'executive_compensation': 0.15,
            'audit_quality': 0.20,
            'transparency_score': 0.15,
            'ethics_compliance': 0.15,
            'shareholder_rights': 0.10
        }
    
    def train(self, training_data: pd.DataFrame, target_column: str = 'governance_score') -> Dict[str, Any]:
        """Train governance score model"""
        try:
            feature_columns = list(self.feature_weights.keys())
            available_features = [col for col in feature_columns if col in training_data.columns]
            
            if len(available_features) < 3:
                logger.warning("Insufficient features for training governance model")
                return {'success': False, 'error': 'Insufficient features'}
            
            X = training_data[available_features].fillna(training_data[available_features].median())
            y = training_data[target_column].fillna(training_data[target_column].median())
            
            X_scaled = self.scaler.fit_transform(X)
            
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                min_samples_split=5
            )
            self.model.fit(X_scaled, y)
            
            self.feature_importance = dict(zip(available_features, self.model.feature_importances_))
            self.is_trained = True
            
            train_score = self.model.score(X_scaled, y)
            
            return {
                'success': True,
                'training_score': train_score,
                'feature_importance': self.feature_importance,
                'features_used': available_features
            }
            
        except Exception as e:
            logger.error(f"Error training governance model: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def predict(self, features: Dict[str, Any]) -> Dict[str, float]:
        """Predict governance score"""
        if not self.is_trained:
            return self._fallback_prediction(features)
        
        try:
            feature_vector = []
            used_features = []
            
            for feature in self.feature_importance.keys():
                if feature in features and features[feature] is not None:
                    feature_vector.append(float(features[feature]))
                    used_features.append(feature)
                else:
                    feature_vector.append(50.0)
                    used_features.append(feature)
            
            if not feature_vector:
                return self._fallback_prediction(features)
            
            feature_array = np.array(feature_vector).reshape(1, -1)
            scaled_features = self.scaler.transform(feature_array)
            prediction = self.model.predict(scaled_features)[0]
            
            available_features = sum(1 for f in self.feature_importance.keys() if f in features and features[f] is not None)
            confidence = (available_features / len(self.feature_importance)) * 100
            
            return {
                'governance_score': max(0, min(100, prediction)),
                'confidence': confidence,
                'features_used': used_features,
                'model_used': 'RandomForest'
            }
            
        except Exception as e:
            logger.error(f"Error predicting governance score: {str(e)}")
            return self._fallback_prediction(features)
    
    def _fallback_prediction(self, features: Dict[str, Any]) -> Dict[str, float]:
        """Fallback prediction using weighted average"""
        total_score = 0
        total_weight = 0
        
        for feature, weight in self.feature_weights.items():
            if feature in features and features[feature] is not None:
                normalized_value = max(0, min(100, float(features[feature])))
                total_score += normalized_value * weight
                total_weight += weight
        
        if total_weight > 0:
            score = total_score / total_weight
        else:
            score = 50.0
        
        return {
            'governance_score': score,
            'confidence': (total_weight / sum(self.feature_weights.values())) * 100,
            'features_used': list(features.keys()),
            'model_used': 'Weighted Average (Fallback)'
        }


class AdvancedESGScoring:
    """Advanced ESG scoring system using quantitative models"""
    
    def __init__(self, models_dir: str = None):
        """
        Initialize advanced ESG scoring system.
        
        Args:
            models_dir: Directory to save/load trained models
        """
        self.models_dir = models_dir or 'models'
        os.makedirs(self.models_dir, exist_ok=True)
        
        # Initialize component models
        self.environmental_model = EnvironmentalScoreModel()
        self.social_model = SocialScoreModel()
        self.governance_model = GovernanceScoreModel()
        
        # Try to load pre-trained models
        self._load_models()
    
    def _load_models(self):
        """Load pre-trained models if available"""
        env_path = os.path.join(self.models_dir, 'environmental_model.joblib')
        social_path = os.path.join(self.models_dir, 'social_model.joblib')
        gov_path = os.path.join(self.models_dir, 'governance_model.joblib')
        
        self.environmental_model.load_model(env_path)
        self.social_model.load_model(social_path)
        self.governance_model.load_model(gov_path)
    
    def train_models(self, training_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Train all ESG component models.
        
        Args:
            training_data: Training dataset with ESG scores and features
            
        Returns:
            Training results for all models
        """
        results = {}
        
        # Train environmental model
        env_result = self.environmental_model.train(training_data, 'environmental_score')
        results['environmental'] = env_result
        
        # Train social model
        social_result = self.social_model.train(training_data, 'social_score')
        results['social'] = social_result
        
        # Train governance model
        gov_result = self.governance_model.train(training_data, 'governance_score')
        results['governance'] = gov_result
        
        # Save trained models
        if env_result.get('success'):
            env_path = os.path.join(self.models_dir, 'environmental_model.joblib')
            self.environmental_model.save_model(env_path)
        
        if social_result.get('success'):
            social_path = os.path.join(self.models_dir, 'social_model.joblib')
            self.social_model.save_model(social_path)
        
        if gov_result.get('success'):
            gov_path = os.path.join(self.models_dir, 'governance_model.joblib')
            self.governance_model.save_model(gov_path)
        
        return results
    
    def calculate_esg_score(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate sophisticated ESG scores using quantitative models.
        
        Args:
            company_data: Company data with ESG metrics
            
        Returns:
            Comprehensive ESG scoring results
        """
        try:
            # Extract features from company data
            features = self._extract_features(company_data)
            
            # Calculate component scores
            env_result = self.environmental_model.predict(features)
            social_result = self.social_model.predict(features)
            gov_result = self.governance_model.predict(features)
            
            # Calculate composite score with confidence weighting
            env_score = env_result['environmental_score']
            social_score = social_result['social_score']
            gov_score = gov_result['governance_score']
            
            env_confidence = env_result['confidence'] / 100
            social_confidence = social_result['confidence'] / 100
            gov_confidence = gov_result['confidence'] / 100
            
            # Weighted composite score
            total_weight = env_confidence + social_confidence + gov_confidence
            if total_weight > 0:
                composite_score = (
                    env_score * env_confidence +
                    social_score * social_confidence +
                    gov_score * gov_confidence
                ) / total_weight
            else:
                composite_score = (env_score + social_score + gov_score) / 3
            
            # Calculate overall confidence
            overall_confidence = (env_confidence + social_confidence + gov_confidence) / 3 * 100
            
            # Calculate trend momentum if historical data available
            trend_momentum = self._calculate_momentum(company_data)
            
            # Calculate confidence interval
            confidence_interval = self._calculate_confidence_interval(
                composite_score, overall_confidence
            )
            
            return {
                'environmental': {
                    'score': round(env_score, 2),
                    'confidence': round(env_result['confidence'], 2),
                    'model_used': env_result['model_used']
                },
                'social': {
                    'score': round(social_score, 2),
                    'confidence': round(social_result['confidence'], 2),
                    'model_used': social_result['model_used']
                },
                'governance': {
                    'score': round(gov_score, 2),
                    'confidence': round(gov_result['confidence'], 2),
                    'model_used': gov_result['model_used']
                },
                'composite': {
                    'score': round(composite_score, 2),
                    'confidence': round(overall_confidence, 2),
                    'confidence_interval': confidence_interval
                },
                'trend_momentum': trend_momentum,
                'calculation_timestamp': datetime.now().isoformat(),
                'methodology': 'Advanced Quantitative Models'
            }
            
        except Exception as e:
            logger.error(f"Error calculating ESG scores: {str(e)}")
            return self._fallback_scoring(company_data)
    
    def _extract_features(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from company data"""
        features = {}
        
        # Extract from metrics if available
        if 'metrics' in company_data and isinstance(company_data['metrics'], dict):
            metrics = company_data['metrics']
            
            # Environmental features
            features.update({
                'carbon_intensity': metrics.get('carbon_intensity'),
                'energy_efficiency': metrics.get('energy_efficiency'),
                'water_usage': metrics.get('water_usage'),
                'waste_management': metrics.get('waste_management'),
                'renewable_energy_pct': metrics.get('renewable_energy_percentage'),
                'biodiversity_impact': metrics.get('biodiversity_impact')
            })
            
            # Social features
            features.update({
                'employee_satisfaction': metrics.get('employee_satisfaction'),
                'diversity_index': metrics.get('diversity_index'),
                'safety_record': metrics.get('safety_record'),
                'community_investment': metrics.get('community_investment'),
                'labor_practices': metrics.get('labor_practices'),
                'human_rights_score': metrics.get('human_rights_score')
            })
            
            # Governance features
            features.update({
                'board_independence': metrics.get('board_independence'),
                'executive_compensation': metrics.get('executive_compensation'),
                'audit_quality': metrics.get('audit_quality'),
                'transparency_score': metrics.get('transparency_score'),
                'ethics_compliance': metrics.get('ethics_compliance'),
                'shareholder_rights': metrics.get('shareholder_rights')
            })
        
        # Extract from sustainability_metrics if available
        if 'sustainability_metrics' in company_data:
            sustainability = company_data['sustainability_metrics']
            features.update({
                'carbon_footprint': sustainability.get('carbon_footprint'),
                'water_usage': sustainability.get('water_usage'),
                'waste_reduction': sustainability.get('waste_reduction'),
                'renewable_energy_pct': sustainability.get('renewable_energy_percentage')
            })
        
        return features
    
    def _calculate_momentum(self, company_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate trend momentum from historical data"""
        momentum = {
            'environmental': 0.0,
            'social': 0.0,
            'governance': 0.0,
            'overall': 0.0
        }
        
        # Check for time series data
        if 'time_series' in company_data and isinstance(company_data['time_series'], list):
            time_series = company_data['time_series']
            
            if len(time_series) >= 3:  # Need at least 3 points for trend
                # Calculate momentum for each component
                for component in ['environmental_score', 'social_score', 'governance_score']:
                    scores = [point.get(component, 0) for point in time_series[-6:]]  # Last 6 periods
                    if len(scores) >= 3:
                        # Simple linear trend
                        x = list(range(len(scores)))
                        if len(set(scores)) > 1:  # Avoid division by zero
                            slope = np.polyfit(x, scores, 1)[0]
                            momentum[component.replace('_score', '')] = slope
                
                # Calculate overall momentum
                momentum['overall'] = (
                    momentum['environmental'] + 
                    momentum['social'] + 
                    momentum['governance']
                ) / 3
        
        return momentum
    
    def _calculate_confidence_interval(self, score: float, confidence: float) -> Tuple[float, float]:
        """Calculate confidence interval for the score"""
        # Simple confidence interval based on confidence level
        margin = (100 - confidence) / 100 * 10  # Max 10-point margin for low confidence
        
        lower_bound = max(0, score - margin)
        upper_bound = min(100, score + margin)
        
        return (round(lower_bound, 2), round(upper_bound, 2))
    
    def _fallback_scoring(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback scoring when advanced models fail"""
        # Use existing scores if available
        if 'esg_scores' in company_data:
            scores = company_data['esg_scores']
            return {
                'environmental': {
                    'score': scores.get('environmental', 50),
                    'confidence': 60,
                    'model_used': 'Fallback'
                },
                'social': {
                    'score': scores.get('social', 50),
                    'confidence': 60,
                    'model_used': 'Fallback'
                },
                'governance': {
                    'score': scores.get('governance', 50),
                    'confidence': 60,
                    'model_used': 'Fallback'
                },
                'composite': {
                    'score': scores.get('combined', 50),
                    'confidence': 60,
                    'confidence_interval': (40, 60)
                },
                'trend_momentum': {
                    'environmental': 0.0,
                    'social': 0.0,
                    'governance': 0.0,
                    'overall': 0.0
                },
                'calculation_timestamp': datetime.now().isoformat(),
                'methodology': 'Fallback Scoring'
            }
        
        # Default neutral scores
        return {
            'environmental': {'score': 50, 'confidence': 50, 'model_used': 'Default'},
            'social': {'score': 50, 'confidence': 50, 'model_used': 'Default'},
            'governance': {'score': 50, 'confidence': 50, 'model_used': 'Default'},
            'composite': {'score': 50, 'confidence': 50, 'confidence_interval': (40, 60)},
            'trend_momentum': {'environmental': 0.0, 'social': 0.0, 'governance': 0.0, 'overall': 0.0},
            'calculation_timestamp': datetime.now().isoformat(),
            'methodology': 'Default Scoring'
        }


def get_advanced_esg_scorer(models_dir: str = None) -> AdvancedESGScoring:
    """
    Get an advanced ESG scoring instance.
    
    Args:
        models_dir: Directory for model storage
        
    Returns:
        Advanced ESG scoring instance
    """
    return AdvancedESGScoring(models_dir)
