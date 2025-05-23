"""
Data Providers for SustainaTrend™

This module provides mock data for the application.
"""

from typing import Dict, Any, List
import random
from datetime import datetime, timedelta

def get_metrics() -> Dict[str, Any]:
    """
    Get mock metrics data.
    
    Returns:
        Dict[str, Any]: Mock metrics data
    """
    return {
        'total_companies': 35,
        'growth_rate': 15,
        'avg_esg_score': 82.5,
        'esg_score_percentage': 82,
        'carbon_intensity': 125.4,
        'carbon_reduction': 12.3,
        'top_sector': 'Clean Energy',
        'sector_market_share': 28.5
    }

def get_trends() -> List[Dict[str, Any]]:
    """
    Get mock trends data.
    
    Returns:
        List[Dict[str, Any]]: Mock trends data
    """
    return [
        {
            'name': 'Clean Energy',
            'growth': 25.5,
            'market_size': 150000000000,
            'companies': 12
        },
        {
            'name': 'Sustainable Transport',
            'growth': 18.2,
            'market_size': 85000000000,
            'companies': 8
        },
        {
            'name': 'Circular Economy',
            'growth': 22.8,
            'market_size': 95000000000,
            'companies': 15
        }
    ]

def get_stories() -> List[Dict[str, Any]]:
    """
    Get mock stories data.
    
    Returns:
        List[Dict[str, Any]]: Mock stories data
    """
    return [
        {
            'title': 'EcoTech Solutions Raises Series B',
            'date': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
            'summary': 'EcoTech Solutions secures $50M in Series B funding...',
            'impact_score': 85
        },
        {
            'title': 'GreenMobile Expands to Europe',
            'date': (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
            'summary': 'GreenMobile announces European expansion...',
            'impact_score': 78
        }
    ]

def get_portfolio_companies() -> List[Dict[str, Any]]:
    """
    Get mock portfolio companies data.
    
    Returns:
        List[Dict[str, Any]]: Mock portfolio companies data
    """
    return [
        {
            'name': 'EcoTech Solutions',
            'ticker': 'ECTS',
            'logo_url': '/static/img/company-logos/default.png',
            'sector': 'Clean Energy',
            'esg_score': 85,
            'esg_score_percentage': 85,
            'carbon_intensity': 45.2,
            'lifecycle_phase': 'Growth',
            'supply_chain_risk': 'Low'
        },
        {
            'name': 'GreenMobile',
            'ticker': 'GRMB',
            'logo_url': '/static/img/company-logos/default.png',
            'sector': 'Transportation',
            'esg_score': 78,
            'esg_score_percentage': 78,
            'carbon_intensity': 62.8,
            'lifecycle_phase': 'Early',
            'supply_chain_risk': 'Medium'
        }
    ]

def get_market_trends() -> List[Dict[str, Any]]:
    """
    Get mock market trends data.
    
    Returns:
        List[Dict[str, Any]]: Mock market trends data
    """
    return [
        {
            'sector': 'Clean Energy',
            'growth_rate': 25.5,
            'market_size': 150000000000,
            'trend_direction': 'up'
        },
        {
            'sector': 'Sustainable Transport',
            'growth_rate': 18.2,
            'market_size': 85000000000,
            'trend_direction': 'up'
        }
    ]

def get_sustainability_scores() -> List[Dict[str, Any]]:
    """
    Get mock sustainability scores data.
    
    Returns:
        List[Dict[str, Any]]: Mock sustainability scores data
    """
    return [
        {
            'company': 'EcoTech Solutions',
            'esg_score': 85,
            'carbon_score': 92,
            'social_score': 78
        },
        {
            'company': 'GreenMobile',
            'esg_score': 78,
            'carbon_score': 85,
            'social_score': 72
        }
    ]

def get_properties() -> List[Dict[str, Any]]:
    """
    Get mock properties data.
    
    Returns:
        List[Dict[str, Any]]: Mock properties data
    """
    return [
        {
            'name': 'Green Office Tower',
            'location': 'New York, NY',
            'type': 'Commercial',
            'size': 50000,
            'breeam_score': 85,
            'energy_rating': 'A',
            'carbon_intensity': 45.2
        },
        {
            'name': 'Eco Residential Complex',
            'location': 'San Francisco, CA',
            'type': 'Residential',
            'size': 35000,
            'breeam_score': 92,
            'energy_rating': 'A+',
            'carbon_intensity': 38.5
        }
    ]

def get_market_data() -> Dict[str, Any]:
    """
    Get mock market data.
    
    Returns:
        Dict[str, Any]: Mock market data
    """
    return {
        'avg_price_per_sqft': 450,
        'avg_cap_rate': 5.2,
        'market_growth': 8.5,
        'transaction_volume': 2500000000
    }

def get_benchmarks() -> List[Dict[str, Any]]:
    """
    Get mock benchmarks data.
    
    Returns:
        List[Dict[str, Any]]: Mock benchmarks data
    """
    return [
        {
            'metric': 'Energy Efficiency',
            'industry_avg': 65,
            'property_avg': 78,
            'difference': 13
        },
        {
            'metric': 'Water Usage',
            'industry_avg': 70,
            'property_avg': 82,
            'difference': 12
        }
    ]

def get_monetization_strategies() -> List[Dict[str, Any]]:
    """
    Get mock monetization strategies data.
    
    Returns:
        List[Dict[str, Any]]: Mock monetization strategies data
    """
    strategies = [
        {
            "name": "Carbon Credits Trading",
            "description": "Monetize carbon reduction through verified carbon credits trading on global markets.",
            "potential_revenue": 25000000,
            "implementation_time": "6-12 months",
            "risk_level": "Medium",
            "risk_level_color": "yellow"
        },
        {
            "name": "Renewable Energy Certificates",
            "description": "Generate and sell renewable energy certificates to utilities and corporations.",
            "potential_revenue": 15000000,
            "implementation_time": "3-6 months",
            "risk_level": "Low",
            "risk_level_color": "green"
        },
        {
            "name": "Sustainable Product Lines",
            "description": "Develop and market eco-friendly product lines with premium pricing.",
            "potential_revenue": 50000000,
            "implementation_time": "12-18 months",
            "risk_level": "High",
            "risk_level_color": "red"
        },
        {
            "name": "Green Bonds",
            "description": "Issue green bonds to finance sustainability projects with favorable terms.",
            "potential_revenue": 100000000,
            "implementation_time": "9-12 months",
            "risk_level": "Medium",
            "risk_level_color": "yellow"
        },
        {
            "name": "Impact Investing Funds",
            "description": "Create specialized investment funds focused on sustainability metrics.",
            "potential_revenue": 75000000,
            "implementation_time": "12-24 months",
            "risk_level": "Medium",
            "risk_level_color": "yellow"
        }
    ]
    
    return strategies

def get_sustainability_trends() -> List[Dict[str, Any]]:
    """
    Get mock sustainability trends data.
    
    Returns:
        List[Dict[str, Any]]: Mock sustainability trends data
    """
    return [
        {
            'category': 'Environmental',
            'name': 'Carbon Neutrality',
            'growth_rate': 28.5,
            'adoption_rate': 45.2,
            'impact_score': 85,
            'virality': 92,
            'timeline': '2023-2025',
            'description': 'Companies committing to carbon neutrality targets',
            'key_drivers': [
                'Regulatory pressure',
                'Consumer demand',
                'Investor expectations'
            ]
        },
        {
            'category': 'Social',
            'name': 'Supply Chain Ethics',
            'growth_rate': 22.3,
            'adoption_rate': 38.7,
            'impact_score': 78,
            'virality': 85,
            'timeline': '2023-2024',
            'description': 'Enhanced focus on ethical supply chain practices',
            'key_drivers': [
                'Consumer awareness',
                'Regulatory compliance',
                'Brand reputation'
            ]
        },
        {
            'category': 'Governance',
            'name': 'ESG Integration',
            'growth_rate': 35.2,
            'adoption_rate': 52.8,
            'impact_score': 92,
            'virality': 88,
            'timeline': '2023-2026',
            'description': 'Integration of ESG metrics in business strategy',
            'key_drivers': [
                'Investor demands',
                'Risk management',
                'Competitive advantage'
            ]
        }
    ]

def get_sustainability_metrics() -> Dict[str, Any]:
    """
    Get mock sustainability metrics data.
    
    Returns:
        Dict[str, Any]: Mock sustainability metrics data
    """
    return {
        "carbon_reduction": 15.2,
        "energy_efficiency": 78.5,
        "water_conservation": 62.3,
        "waste_reduction": 45.8,
        "renewable_energy_usage": 32.7,
        "sustainable_sourcing": 58.9,
        "employee_engagement": 82.1,
        "community_impact": 75.4,
        "overall_sustainability_score": 71.3,
        "year_over_year_improvement": 8.5
    } 