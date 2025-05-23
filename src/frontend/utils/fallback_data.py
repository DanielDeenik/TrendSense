"""
Fallback Data Module for SustainaTrend™

This module provides fallback data when AI services are unavailable.
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
import random

def get_fallback_trends_data() -> Dict[str, Any]:
    """
    Get fallback trends data.
    
    Returns:
        Dict[str, Any]: Fallback trends data
    """
    current_year = datetime.now().year
    
    return {
        "total_companies": 1250,
        "growth_rate": 18.5,
        "avg_esg_score": 72.3,
        "carbon_reduction": 15.2,
        "market_trends": [
            {
                "name": "Renewable Energy Adoption",
                "growth": 24.5,
                "momentum": "Increasing",
                "description": "Companies are increasingly adopting renewable energy sources to reduce carbon footprint."
            },
            {
                "name": "Circular Economy",
                "growth": 18.2,
                "momentum": "Stable",
                "description": "Implementation of circular economy principles in product design and manufacturing."
            },
            {
                "name": "ESG Reporting",
                "growth": 32.7,
                "momentum": "Rapidly Increasing",
                "description": "More companies are publishing comprehensive ESG reports to meet stakeholder expectations."
            },
            {
                "name": "Sustainable Supply Chain",
                "growth": 15.8,
                "momentum": "Increasing",
                "description": "Companies are focusing on sustainability throughout their supply chains."
            },
            {
                "name": "Carbon Neutrality Pledges",
                "growth": 28.3,
                "momentum": "Increasing",
                "description": "Growing number of companies committing to carbon neutrality by 2030-2050."
            }
        ],
        "historical_data": {
            "total_companies": [
                {"year": current_year-4, "value": 850},
                {"year": current_year-3, "value": 950},
                {"year": current_year-2, "value": 1050},
                {"year": current_year-1, "value": 1150},
                {"year": current_year, "value": 1250}
            ],
            "avg_esg_score": [
                {"year": current_year-4, "value": 65.2},
                {"year": current_year-3, "value": 67.8},
                {"year": current_year-2, "value": 69.5},
                {"year": current_year-1, "value": 71.0},
                {"year": current_year, "value": 72.3}
            ],
            "carbon_reduction": [
                {"year": current_year-4, "value": 8.5},
                {"year": current_year-3, "value": 10.2},
                {"year": current_year-2, "value": 12.1},
                {"year": current_year-1, "value": 13.8},
                {"year": current_year, "value": 15.2}
            ]
        },
        "industry_breakdown": [
            {"industry": "Technology", "companies": 320, "avg_esg_score": 75.2},
            {"industry": "Finance", "companies": 280, "avg_esg_score": 73.8},
            {"industry": "Healthcare", "companies": 210, "avg_esg_score": 71.5},
            {"industry": "Manufacturing", "companies": 180, "avg_esg_score": 68.2},
            {"industry": "Energy", "companies": 150, "avg_esg_score": 65.7},
            {"industry": "Other", "companies": 110, "avg_esg_score": 70.1}
        ],
        "top_performers": [
            {"company": "EcoTech Solutions", "esg_score": 92.5, "industry": "Technology"},
            {"company": "GreenFinance Group", "esg_score": 90.2, "industry": "Finance"},
            {"company": "SustainHealth", "esg_score": 89.7, "industry": "Healthcare"},
            {"company": "CleanEnergy Corp", "esg_score": 88.3, "industry": "Energy"},
            {"company": "CircularManufacturing", "esg_score": 87.1, "industry": "Manufacturing"}
        ],
        "regulatory_landscape": [
            {
                "region": "European Union",
                "frameworks": ["CSRD", "EU Taxonomy", "SFDR"],
                "impact_level": "High",
                "description": "Comprehensive regulatory framework with mandatory reporting requirements."
            },
            {
                "region": "United States",
                "frameworks": ["SEC Climate Disclosure", "TCFD"],
                "impact_level": "Medium",
                "description": "Evolving regulatory landscape with increasing disclosure requirements."
            },
            {
                "region": "Asia-Pacific",
                "frameworks": ["HKEX ESG Reporting", "TCFD Japan"],
                "impact_level": "Medium",
                "description": "Varied regulatory approaches across countries with increasing standardization."
            }
        ]
    }

def get_fallback_regulatory_assessment() -> Dict[str, Any]:
    """
    Get fallback regulatory assessment data.
    
    Returns:
        Dict[str, Any]: Fallback regulatory assessment data
    """
    return {
        "framework": "Corporate Sustainability Reporting Directive (CSRD)",
        "framework_id": "CSRD",
        "date": datetime.now().isoformat(),
        "overall_score": 68,
        "categories": {
            "environmental": {
                "score": 72,
                "compliance_level": "Moderate Compliance",
                "findings": [
                    "Good disclosure of carbon emissions data",
                    "Limited information on biodiversity impact",
                    "Comprehensive water usage reporting"
                ],
                "recommendations": [
                    "Enhance biodiversity impact assessment",
                    "Include more details on environmental risk management",
                    "Expand scope 3 emissions reporting"
                ]
            },
            "social": {
                "score": 65,
                "compliance_level": "Moderate Compliance",
                "findings": [
                    "Strong human rights policy",
                    "Limited disclosure on supply chain labor practices",
                    "Good community engagement reporting"
                ],
                "recommendations": [
                    "Improve supply chain labor practice transparency",
                    "Enhance diversity and inclusion metrics",
                    "Provide more quantitative social impact data"
                ]
            },
            "governance": {
                "score": 78,
                "compliance_level": "Good Compliance",
                "findings": [
                    "Robust board oversight of sustainability",
                    "Clear sustainability governance structure",
                    "Comprehensive ethics policies"
                ],
                "recommendations": [
                    "Link executive compensation to sustainability metrics",
                    "Enhance disclosure of lobbying activities",
                    "Improve transparency of tax practices"
                ]
            }
        },
        "overall_findings": [
            "The report demonstrates moderate compliance with CSRD requirements",
            "Environmental reporting is stronger than social reporting",
            "Governance disclosures are the strongest area",
            "Some required metrics are missing or incomplete"
        ],
        "overall_recommendations": [
            "Enhance social impact reporting with more quantitative metrics",
            "Improve biodiversity and nature-related disclosures",
            "Strengthen supply chain sustainability reporting",
            "Develop more forward-looking sustainability targets"
        ]
    }

def get_fallback_rag_response(query: str) -> Dict[str, Any]:
    """
    Get fallback RAG response data.
    
    Args:
        query: User query
        
    Returns:
        Dict[str, Any]: Fallback RAG response data
    """
    return {
        "query": query,
        "response": "I'm sorry, but I don't have access to the specific information needed to answer your query accurately. When our AI services are back online, I'll be able to provide you with a more detailed and accurate response based on the regulatory documents in our database.",
        "sources": [],
        "confidence": 0,
        "fallback": True
    }

def get_fallback_service_status() -> Dict[str, Any]:
    """
    Get fallback service status data.
    
    Returns:
        Dict[str, Any]: Fallback service status data
    """
    return {
        "services": {
            "openai": {
                "available": False,
                "error": "Service status check failed"
            },
            "gemini": {
                "available": False,
                "error": "Service status check failed"
            },
            "pinecone": {
                "available": False,
                "error": "Service status check failed"
            }
        },
        "best_available_service": "none",
        "any_ai_available": False,
        "rag_available": False
    }
