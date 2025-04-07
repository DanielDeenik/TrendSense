"""
VC/PE Data Module for SustainaTrend™
This module provides data access functions for VC/PE specific features.
"""

import os
import random
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection settings
MONGODB_URI = os.getenv('MONGODB_URI')
MONGODB_DB_NAME = os.getenv('MONGODB_DB_NAME', 'sustainatrend')

# Initialize MongoDB client
try:
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB_NAME]
    print(f"Connected to MongoDB: {MONGODB_URI}")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    client = None
    db = None

def get_mongodb_data():
    """Get data from MongoDB or fall back to generated data if connection fails."""
    if db is None:
        return None
    return db

def generate_portfolio_metrics():
    """Generate portfolio-level sustainability metrics."""
    # Try to get data from MongoDB first
    if db is not None:
        try:
            # Get all companies
            companies = list(db.companies.find({}, {'_id': 0}))
            
            if companies:
                # Calculate portfolio metrics
                total_companies = len(companies)
                total_arr = sum(company.get('metrics', {}).get('ARR', 0) for company in companies)
                total_burn_rate = sum(company.get('metrics', {}).get('BurnRate', 0) for company in companies)
                avg_cac = sum(company.get('metrics', {}).get('CAC', 0) for company in companies) / total_companies
                avg_ltv = sum(company.get('metrics', {}).get('LTV', 0) for company in companies) / total_companies
                avg_runway = sum(company.get('metrics', {}).get('RunwayMonths', 0) for company in companies) / total_companies
                
                # Calculate sustainability metrics
                avg_carbon_reduction = sum(company.get('sustainability_metrics', {}).get('carbon_reduction', 0) for company in companies) / total_companies
                avg_water_savings = sum(company.get('sustainability_metrics', {}).get('water_savings', 0) for company in companies) / total_companies
                avg_waste_reduction = sum(company.get('sustainability_metrics', {}).get('waste_reduction', 0) for company in companies) / total_companies
                avg_renewable_energy = sum(company.get('sustainability_metrics', {}).get('renewable_energy_usage', 0) for company in companies) / total_companies
                avg_supply_chain = sum(company.get('sustainability_metrics', {}).get('supply_chain_sustainability', 0) for company in companies) / total_companies
                
                # Calculate sentiment and virality
                avg_sentiment = sum(company.get('sentimentScore', 0) for company in companies) / total_companies
                avg_virality = sum(company.get('viralityScore', 0) for company in companies) / total_companies
                
                return {
                    "portfolio": {
                        "total_companies": total_companies,
                        "total_arr": total_arr,
                        "total_burn_rate": total_burn_rate,
                        "avg_cac": avg_cac,
                        "avg_ltv": avg_ltv,
                        "avg_runway": avg_runway
                    },
                    "sustainability": {
                        "carbon_reduction": avg_carbon_reduction,
                        "water_savings": avg_water_savings,
                        "waste_reduction": avg_waste_reduction,
                        "renewable_energy_usage": avg_renewable_energy,
                        "supply_chain_sustainability": avg_supply_chain
                    },
                    "sentiment": {
                        "avg_sentiment": avg_sentiment,
                        "avg_virality": avg_virality
                    },
                    "last_updated": datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Error getting portfolio metrics from MongoDB: {e}")
    
    # Fall back to generated data if MongoDB fails
    return {
        "portfolio": {
            "total_companies": 5,
            "total_arr": 12000000,
            "total_burn_rate": 425000,
            "avg_cac": 420,
            "avg_ltv": 3000,
            "avg_runway": 12
        },
        "sustainability": {
            "carbon_reduction": 35,
            "water_savings": 45,
            "waste_reduction": 55,
            "renewable_energy_usage": 65,
            "supply_chain_sustainability": 75
        },
        "sentiment": {
            "avg_sentiment": 0.7,
            "avg_virality": 0.85
        },
        "last_updated": datetime.now().isoformat()
    }

def generate_company_benchmarks():
    """Generate company-level sustainability benchmarks."""
    # Try to get data from MongoDB first
    if db is not None:
        try:
            # Get all companies
            companies = list(db.companies.find({}, {'_id': 0}))
            
            if companies:
                return companies
        except Exception as e:
            print(f"Error getting company benchmarks from MongoDB: {e}")
    
    # Fall back to generated data if MongoDB fails
    return [
        {
            "name": "CleanSpark Ventures",
            "sector": "CleanTech",
            "stage": "Series A",
            "fund_id": "fund_alpha",
            "metrics": {
                "ARR": 1200000,
                "BurnRate": 85000,
                "CAC": 420,
                "LTV": 3000,
                "RunwayMonths": 12
            },
            "sustainability_metrics": {
                "carbon_reduction": 35,
                "water_savings": 45,
                "waste_reduction": 55,
                "renewable_energy_usage": 65,
                "supply_chain_sustainability": 75
            },
            "sentimentScore": 0.7,
            "viralityScore": 0.85,
            "esgRiskCluster": ["governance", "supply_chain"],
            "impactNarrative": "Revolutionizing waste management through AI-driven sorting systems",
            "last_updated": datetime.now().isoformat()
        },
        {
            "name": "EcoTech Solutions",
            "sector": "Renewable Energy",
            "stage": "Series B",
            "fund_id": "fund_beta",
            "metrics": {
                "ARR": 2500000,
                "BurnRate": 120000,
                "CAC": 380,
                "LTV": 3500,
                "RunwayMonths": 18
            },
            "sustainability_metrics": {
                "carbon_reduction": 40,
                "water_savings": 50,
                "waste_reduction": 60,
                "renewable_energy_usage": 70,
                "supply_chain_sustainability": 80
            },
            "sentimentScore": 0.75,
            "viralityScore": 0.9,
            "esgRiskCluster": ["environmental", "social"],
            "impactNarrative": "Developing next-generation solar technology with 40% higher efficiency",
            "last_updated": datetime.now().isoformat()
        }
    ]

def generate_sustainability_insights():
    """Generate AI-powered sustainability insights."""
    # Try to get data from MongoDB first
    if db is not None:
        try:
            # Get all companies
            companies = list(db.companies.find({}, {'_id': 0}))
            
            if companies:
                # Generate insights based on company data
                insights = []
                
                for company in companies:
                    # Create insight based on company data
                    insight = {
                        "title": f"Sustainability Analysis: {company['name']}",
                        "content": f"Based on our analysis, {company['name']} shows strong potential in {company['sector']} with a focus on {company['impactNarrative']}. The company has achieved a {company['sustainability_metrics']['carbon_reduction']}% reduction in carbon emissions and {company['sustainability_metrics']['water_savings']}% in water savings.",
                        "impact": "High",
                        "recommendation": f"Consider increasing investment in {company['name']} to accelerate their sustainability initiatives.",
                        "timestamp": datetime.now().isoformat()
                    }
                    insights.append(insight)
                
                # Add some general portfolio insights
                portfolio_metrics = generate_portfolio_metrics()
                
                insights.append({
                    "title": "Portfolio Sustainability Overview",
                    "content": f"The portfolio shows an average carbon reduction of {portfolio_metrics['sustainability']['carbon_reduction']}% and water savings of {portfolio_metrics['sustainability']['water_savings']}%. Overall sentiment is {portfolio_metrics['sentiment']['avg_sentiment']} with a virality score of {portfolio_metrics['sentiment']['avg_virality']}.",
                    "impact": "Medium",
                    "recommendation": "Focus on improving supply chain sustainability across the portfolio.",
                    "timestamp": datetime.now().isoformat()
                })
                
                return insights
        except Exception as e:
            print(f"Error getting sustainability insights from MongoDB: {e}")
    
    # Fall back to generated data if MongoDB fails
    return [
        {
            "title": "CleanTech Sector Growth",
            "content": "The CleanTech sector shows strong growth potential with increasing investment in sustainable technologies.",
            "impact": "High",
            "recommendation": "Consider increasing allocation to CleanTech startups.",
            "timestamp": datetime.now().isoformat()
        },
        {
            "title": "Carbon Reduction Opportunities",
            "content": "Portfolio companies have identified significant opportunities for carbon reduction through innovative technologies.",
            "impact": "Medium",
            "recommendation": "Implement standardized carbon measurement across portfolio.",
            "timestamp": datetime.now().isoformat()
        },
        {
            "title": "Supply Chain Sustainability",
            "content": "Supply chain sustainability remains a key challenge for portfolio companies.",
            "impact": "High",
            "recommendation": "Develop a supply chain sustainability framework for portfolio companies.",
            "timestamp": datetime.now().isoformat()
        }
    ] 