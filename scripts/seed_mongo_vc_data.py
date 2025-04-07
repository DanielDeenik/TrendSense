#!/usr/bin/env python3
"""
MongoDB Seeder Script for SustainaTrend VC/PE Data
This script populates MongoDB with sample VC/PE sustainability data.
"""

import os
import random
import json
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection settings
MONGODB_URI = os.getenv('MONGODB_URI')
MONGODB_DB_NAME = os.getenv('MONGODB_DB_NAME', 'sustainatrend')

def connect_to_mongodb():
    """Connect to MongoDB and return the client and database."""
    try:
        client = MongoClient(MONGODB_URI)
        db = client[MONGODB_DB_NAME]
        print(f"Connected to MongoDB: {MONGODB_URI}")
        return client, db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None, None

def generate_company_data():
    """Generate sample VC/PE company data."""
    company_names = [
        "CleanSpark Ventures", 
        "EcoTech Solutions", 
        "GreenEnergy Innovations", 
        "Sustainable Materials Co", 
        "Circular Economy Labs"
    ]
    
    sectors = ["CleanTech", "Renewable Energy", "Sustainable Materials", "Circular Economy", "AgTech"]
    stages = ["Seed", "Series A", "Series B", "Series C", "Growth"]
    fund_ids = ["fund_alpha", "fund_beta", "fund_gamma", "fund_delta", "fund_epsilon"]
    
    esg_risk_clusters = [
        ["governance", "supply_chain"],
        ["environmental", "social"],
        ["carbon_emissions", "water_usage"],
        ["waste_management", "biodiversity"],
        ["labor_practices", "community_impact"]
    ]
    
    impact_narratives = [
        "Revolutionizing waste management through AI-driven sorting systems",
        "Developing next-generation solar technology with 40% higher efficiency",
        "Creating biodegradable packaging alternatives to reduce plastic waste",
        "Implementing circular economy principles in manufacturing processes",
        "Transforming agriculture with sustainable farming technologies"
    ]
    
    companies = []
    
    for i in range(5):
        company = {
            "name": company_names[i],
            "sector": sectors[i],
            "stage": stages[i],
            "fund_id": fund_ids[i],
            "metrics": {
                "ARR": random.randint(500000, 5000000),
                "BurnRate": random.randint(50000, 200000),
                "CAC": random.randint(300, 800),
                "LTV": random.randint(2000, 5000),
                "RunwayMonths": random.randint(6, 24)
            },
            "sustainability_metrics": {
                "carbon_reduction": random.randint(10, 50),
                "water_savings": random.randint(15, 60),
                "waste_reduction": random.randint(20, 70),
                "renewable_energy_usage": random.randint(30, 90),
                "supply_chain_sustainability": random.randint(40, 95)
            },
            "sentimentScore": round(random.uniform(0.5, 0.9), 2),
            "viralityScore": round(random.uniform(0.6, 0.95), 2),
            "esgRiskCluster": esg_risk_clusters[i],
            "impactNarrative": impact_narratives[i],
            "last_updated": datetime.now().isoformat()
        }
        companies.append(company)
    
    return companies

def generate_document_data(companies):
    """Generate sample document data for companies."""
    documents = []
    
    document_types = [
        "sustainability_report", 
        "esg_assessment", 
        "impact_measurement", 
        "carbon_footprint", 
        "supply_chain_analysis"
    ]
    
    for company in companies:
        for doc_type in document_types:
            doc = {
                "company_id": company["name"],
                "document_type": doc_type,
                "title": f"{company['name']} - {doc_type.replace('_', ' ').title()}",
                "content": f"Sample content for {company['name']} {doc_type}",
                "upload_date": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
                "metadata": {
                    "pages": random.randint(10, 50),
                    "file_size_kb": random.randint(100, 5000),
                    "language": "en",
                    "version": f"1.{random.randint(0, 9)}"
                },
                "sustainability_metrics": {
                    "carbon_reduction": random.randint(5, 40),
                    "water_savings": random.randint(10, 50),
                    "waste_reduction": random.randint(15, 60),
                    "renewable_energy_usage": random.randint(25, 85),
                    "supply_chain_sustainability": random.randint(35, 90)
                }
            }
            documents.append(doc)
    
    return documents

def seed_database():
    """Seed the MongoDB database with sample data."""
    client, db = connect_to_mongodb()
    
    if not client or not db:
        return False
    
    try:
        # Clear existing data
        db.companies.delete_many({})
        db.documents.delete_many({})
        
        # Generate and insert company data
        companies = generate_company_data()
        result = db.companies.insert_many(companies)
        print(f"Inserted {len(result.inserted_ids)} companies")
        
        # Generate and insert document data
        documents = generate_document_data(companies)
        result = db.documents.insert_many(documents)
        print(f"Inserted {len(result.inserted_ids)} documents")
        
        # Create indexes
        db.companies.create_index("name")
        db.companies.create_index("sector")
        db.companies.create_index("fund_id")
        db.documents.create_index("company_id")
        db.documents.create_index("document_type")
        
        print("Database seeded successfully!")
        return True
    
    except Exception as e:
        print(f"Error seeding database: {e}")
        return False
    
    finally:
        client.close()

if __name__ == "__main__":
    seed_database() 