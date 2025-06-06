"""
LensIQ Narrative Builder Module

This module provides comprehensive data collection, trend analysis, and story generation
capabilities for creating compelling narratives that resonate with investors, clients, and staff.
"""

from .data_collector import DataCollector
from .trend_analyzer import TrendAnalyzer
from .story_generator import StoryGenerator
from .narrative_engine import NarrativeEngine

__all__ = [
    'DataCollector',
    'TrendAnalyzer', 
    'StoryGenerator',
    'NarrativeEngine'
]
