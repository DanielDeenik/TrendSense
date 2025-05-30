"""
Advanced Analytics Package for TrendSense™

This package provides sophisticated analytics capabilities to replace
basic scoring mechanisms with quantitative models and predictive analytics.
"""

from .advanced_scoring import (
    AdvancedESGScoring, QuantitativeESGModel, get_advanced_esg_scorer
)
from .trend_analyzer import (
    TrendAnalyzer, TimeSeriesAnalyzer, PredictiveAnalyzer, get_trend_analyzer
)
from .benchmark_engine import (
    BenchmarkEngine, IndustryBenchmarker, get_benchmark_engine
)
from .risk_assessor import (
    RiskAssessor, ESGRiskAnalyzer, get_risk_assessor
)

__all__ = [
    'AdvancedESGScoring', 'QuantitativeESGModel', 'get_advanced_esg_scorer',
    'TrendAnalyzer', 'TimeSeriesAnalyzer', 'PredictiveAnalyzer', 'get_trend_analyzer',
    'BenchmarkEngine', 'IndustryBenchmarker', 'get_benchmark_engine',
    'RiskAssessor', 'ESGRiskAnalyzer', 'get_risk_assessor'
]
