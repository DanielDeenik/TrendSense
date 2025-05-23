"""
Script to update the vector database with the enhanced data.
"""

import os
import sys
import json
import random
import datetime
import numpy as np
from tqdm import tqdm
import firebase_admin
from firebase_admin import credentials, firestore

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import project modules
from src.database.adapters.firebase_adapter import FirebaseAdapter
from src.data_management.vector_store import VectorStore

# Initialize Firebase
try:
    firebase_app = firebase_admin.get_app()
except ValueError:
    cred_path = os.path.join(os.path.dirname(__file__), '..', 'firebase', 'service-account-key.json')
    cred = credentials.Certificate(cred_path)
    firebase_app = firebase_admin.initialize_app(cred)

db = firestore.client()

# Initialize Firebase adapter
firebase_adapter = FirebaseAdapter()

# Initialize Vector Store
vector_store = VectorStore()

def update_vector_db():
    """Update the vector database with the enhanced data."""
    print("Updating vector database...")
    
    # Get all companies
    companies = list(db.collection('companies').get())
    print(f"Found {len(companies)} companies")
    
    # Get all trends
    trends = list(db.collection('trends').get())
    print(f"Found {len(trends)} trends")
    
    # Get all projects
    projects = list(db.collection('projects').get())
    print(f"Found {len(projects)} projects")
    
    # Get all funds
    funds = list(db.collection('funds').get())
    print(f"Found {len(funds)} funds")
    
    # Update vector database with companies
    print("Updating companies in vector database...")
    for company_doc in tqdm(companies):
        company = company_doc.to_dict()
        company_id = company_doc.id
        
        # Create metadata for vector store
        metadata = {
            "id": company_id,
            "name": company.get("name", f"Company {company_id}"),
            "type": "company",
            "sector": company.get("sector", "Unknown"),
            "founding_year": company.get("founding_year", 2000),
            "environmental_score": company.get("sustainability_metrics", {}).get("environmental_score", 0),
            "social_score": company.get("sustainability_metrics", {}).get("social_score", 0),
            "governance_score": company.get("sustainability_metrics", {}).get("governance_score", 0),
            "esg_score": company.get("sustainability_metrics", {}).get("esg_score", 0),
            "carbon_footprint": company.get("sustainability_metrics", {}).get("carbon_footprint", 0),
            "revenue": company.get("financial_metrics", {}).get("revenue", 0),
            "profit_margin": company.get("financial_metrics", {}).get("profit_margin", 0),
            "market_cap": company.get("financial_metrics", {}).get("market_cap", 0),
        }
        
        # Create text for vector store
        text = f"{company.get('name', '')} - {company.get('description', '')} - {company.get('sector', '')}"
        
        # Get embedding
        embedding = company.get("embedding")
        
        if embedding:
            # Add to vector store
            vector_store.add_item(
                item_id=company_id,
                embedding=embedding,
                metadata=metadata,
                text=text
            )
    
    # Update vector database with trends
    print("Updating trends in vector database...")
    for trend_doc in tqdm(trends):
        trend = trend_doc.to_dict()
        trend_id = trend_doc.id
        
        # Create metadata for vector store
        metadata = {
            "id": trend_id,
            "name": trend.get("name", f"Trend {trend_id}"),
            "type": "trend",
            "category": trend.get("category", "Unknown"),
            "relevance_score": trend.get("relevance_score", 0),
            "growth_rate": trend.get("growth_rate", 0),
            "maturity_stage": trend.get("maturity_stage", "Unknown"),
        }
        
        # Create text for vector store
        text = f"{trend.get('name', '')} - {trend.get('description', '')} - {trend.get('category', '')}"
        
        # Get embedding
        embedding = trend.get("embedding")
        
        if embedding:
            # Add to vector store
            vector_store.add_item(
                item_id=trend_id,
                embedding=embedding,
                metadata=metadata,
                text=text
            )
    
    # Update vector database with projects
    print("Updating projects in vector database...")
    for project_doc in tqdm(projects):
        project = project_doc.to_dict()
        project_id = project_doc.id
        
        # Create metadata for vector store
        metadata = {
            "id": project_id,
            "name": project.get("name", f"Project {project_id}"),
            "type": "project",
            "project_type": project.get("type", "Unknown"),
            "company_id": project.get("company_id", ""),
            "status": project.get("status", "Unknown"),
            "budget": project.get("budget", 0),
            "progress": project.get("progress", 0),
            "carbon_impact": project.get("sustainability_metrics", {}).get("carbon_impact", 0),
            "sdg_alignment": project.get("sustainability_metrics", {}).get("sdg_alignment", []),
            "social_score": project.get("sustainability_metrics", {}).get("social_score", 0),
        }
        
        # Create text for vector store
        text = f"{project.get('name', '')} - {project.get('description', '')} - {project.get('type', '')}"
        
        # Get embedding
        embedding = project.get("embedding")
        
        if embedding:
            # Add to vector store
            vector_store.add_item(
                item_id=project_id,
                embedding=embedding,
                metadata=metadata,
                text=text
            )
    
    # Update vector database with funds
    print("Updating funds in vector database...")
    for fund_doc in tqdm(funds):
        fund = fund_doc.to_dict()
        fund_id = fund_doc.id
        
        # Create metadata for vector store
        metadata = {
            "id": fund_id,
            "name": fund.get("name", f"Fund {fund_id}"),
            "type": "fund",
            "aum": fund.get("aum", 0),
            "return": fund.get("return", 0),
            "portfolio_companies": fund.get("portfolio_companies", []),
            "sustainability_focus": fund.get("sustainability_focus", []),
        }
        
        # Create text for vector store
        text = f"{fund.get('name', '')} - {fund.get('description', '')} - {' '.join(fund.get('sustainability_focus', []))}"
        
        # Get embedding
        embedding = fund.get("embedding")
        
        if embedding:
            # Add to vector store
            vector_store.add_item(
                item_id=fund_id,
                embedding=embedding,
                metadata=metadata,
                text=text
            )
    
    print("Vector database update complete!")

if __name__ == "__main__":
    update_vector_db()
