"""
Real Estate Sustainability Module

This module provides functions for real estate sustainability metrics and analysis.
"""

import json
import random
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

# Define categories for real estate sustainability
REALESTATE_CATEGORIES = [
    "office_buildings",
    "retail_spaces",
    "industrial",
    "residential",
    "mixed_use",
    "all"
]

class NumPyJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for NumPy types."""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        return super(NumPyJSONEncoder, self).default(obj)

def get_real_estate_metrics() -> Dict[str, Any]:
    """
    Get mock real estate sustainability metrics.
    
    Returns:
        Dict[str, Any]: Real estate sustainability metrics
    """
    return {
        "portfolio": {
            "total_properties": 15,
            "energy_rating": "A",
            "carbon_footprint": 450,
            "water_usage": 1200,
            "waste_reduction": 35,
            "renewable_energy": 40,
            "green_certifications": 8
        },
        "property_categories": {
            "office_buildings": {
                "energy_rating_a": 5,
                "energy_rating_b": 3,
                "energy_rating_c": 2,
                "total": 10
            },
            "retail_spaces": {
                "energy_rating_a": 3,
                "energy_rating_b": 2,
                "energy_rating_c": 1,
                "total": 6
            },
            "industrial": {
                "energy_rating_a": 2,
                "energy_rating_b": 4,
                "energy_rating_c": 1,
                "total": 7
            },
            "residential": {
                "energy_rating_a": 4,
                "energy_rating_b": 3,
                "energy_rating_c": 2,
                "total": 9
            },
            "mixed_use": {
                "energy_rating_a": 3,
                "energy_rating_b": 2,
                "energy_rating_c": 1,
                "total": 6
            }
        },
        "recent_assessments": [
            {
                "property": "Office Building A",
                "type": "Energy Efficiency Assessment",
                "date": "2024-04-08",
                "score": 85,
                "recommendations": 3
            },
            {
                "property": "Retail Space B",
                "type": "Water Usage Analysis",
                "date": "2024-04-01",
                "score": 78,
                "recommendations": 2
            },
            {
                "property": "Industrial Complex C",
                "type": "Carbon Footprint Assessment",
                "date": "2024-03-25",
                "score": 72,
                "recommendations": 4
            },
            {
                "property": "Residential Tower D",
                "type": "Waste Management Review",
                "date": "2024-03-18",
                "score": 88,
                "recommendations": 1
            }
        ],
        "sustainability_trends": {
            "energy_efficiency": {
                "current": 82,
                "previous": 75,
                "change": 7,
                "trend": "up"
            },
            "water_conservation": {
                "current": 78,
                "previous": 70,
                "change": 8,
                "trend": "up"
            },
            "waste_reduction": {
                "current": 65,
                "previous": 60,
                "change": 5,
                "trend": "up"
            },
            "carbon_reduction": {
                "current": 70,
                "previous": 68,
                "change": 2,
                "trend": "up"
            }
        }
    }

def calculate_realestate_trends(metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Calculate real estate sustainability trends from metrics.
    
    Args:
        metrics: Real estate sustainability metrics
        
    Returns:
        List[Dict[str, Any]]: Calculated trends
    """
    # Extract sustainability trends from metrics
    sustainability_trends = metrics.get("sustainability_trends", {})
    
    # Convert to list format for the template
    trends = []
    for key, value in sustainability_trends.items():
        trend_name = key.replace("_", " ").title()
        trend_value = value.get("current", 0)
        trend_change = value.get("change", 0)
        trend_direction = value.get("trend", "neutral")
        
        # Determine trend color based on direction
        if trend_direction == "up":
            trend_color = "green"
        elif trend_direction == "down":
            trend_color = "red"
        else:
            trend_color = "yellow"
        
        trends.append({
            "name": trend_name,
            "value": trend_value,
            "change": trend_change,
            "direction": trend_direction,
            "color": trend_color
        })
    
    return trends

def get_realestate_trend_analysis(category: Optional[str] = None) -> Dict[str, Any]:
    """
    Get real estate sustainability trend analysis.
    
    Args:
        category: Optional category filter
        
    Returns:
        Dict[str, Any]: Trend analysis data
    """
    # Generate mock trend data
    categories = REALESTATE_CATEGORIES if category == "all" or category is None else [category]
    
    # Generate dates for the last 12 months
    end_date = datetime.now()
    dates = [(end_date - timedelta(days=30*i)).strftime("%Y-%m") for i in range(12)]
    dates.reverse()  # Oldest to newest
    
    # Generate chart data
    chart_data = {
        "labels": dates,
        "datasets": []
    }
    
    # Generate datasets for each category
    colors = {
        "office_buildings": "#4CAF50",
        "retail_spaces": "#2196F3",
        "industrial": "#FF9800",
        "residential": "#9C27B0",
        "mixed_use": "#E91E63"
    }
    
    for cat in categories:
        if cat == "all":
            continue
            
        # Generate random data points with an upward trend
        base_value = random.randint(60, 80)
        data_points = []
        
        for i in range(12):
            # Add some randomness but maintain an upward trend
            value = base_value + (i * 1.5) + random.uniform(-2, 2)
            data_points.append(round(value, 1))
        
        chart_data["datasets"].append({
            "label": cat.replace("_", " ").title(),
            "data": data_points,
            "borderColor": colors.get(cat, "#607D8B"),
            "backgroundColor": "rgba(0,0,0,0)",
            "borderWidth": 2,
            "pointRadius": 3
        })
    
    # Generate trend items
    trends = []
    for cat in categories:
        if cat == "all":
            continue
            
        # Generate random virality score
        virality = random.randint(50, 100)
        
        # Generate random sentiment
        sentiment_options = ["positive", "neutral", "negative"]
        sentiment = random.choice(sentiment_options)
        
        # Generate random impact score
        impact = random.randint(60, 95)
        
        # Generate random confidence
        confidence = random.randint(70, 95)
        
        # Generate random source count
        source_count = random.randint(5, 20)
        
        # Generate random date within the last 30 days
        days_ago = random.randint(0, 30)
        date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        # Generate title based on category
        category_name = cat.replace("_", " ").title()
        titles = [
            f"New {category_name} Sustainability Standards Announced",
            f"{category_name} Energy Efficiency Improvements",
            f"Water Conservation in {category_name}",
            f"Carbon Reduction Strategies for {category_name}",
            f"{category_name} Green Building Certifications on the Rise"
        ]
        title = random.choice(titles)
        
        # Generate description
        descriptions = [
            f"Recent developments in {cat.replace('_', ' ')} sustainability practices show promising results.",
            f"New technologies are improving the environmental impact of {cat.replace('_', ' ')}.",
            f"Regulatory changes are driving sustainability improvements in {cat.replace('_', ' ')}.",
            f"Market demand is increasing for sustainable {cat.replace('_', ' ')} options.",
            f"Investment in {cat.replace('_', ' ')} sustainability is growing rapidly."
        ]
        description = random.choice(descriptions)
        
        trends.append({
            "id": f"trend-{cat}-{random.randint(1000, 9999)}",
            "title": title,
            "description": description,
            "category": cat,
            "virality": virality,
            "sentiment": sentiment,
            "impact": impact,
            "confidence": confidence,
            "source_count": source_count,
            "date": date
        })
    
    # Sort trends by virality (highest first)
    trends.sort(key=lambda x: x["virality"], reverse=True)
    
    return {
        "trends": trends,
        "chart_data": chart_data
    } 