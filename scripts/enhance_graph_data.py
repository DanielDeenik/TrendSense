"""
Script to enhance the graph data with more meaningful relationships and metadata.
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

# Initialize Firebase
try:
    firebase_app = firebase_admin.get_app()
except ValueError:
    cred_path = os.path.join(os.path.dirname(__file__), '..', 'firebase', 'service-account-key.json')
    cred = credentials.Certificate(cred_path)
    firebase_app = firebase_admin.initialize_app(cred)

db = firestore.client()

# Constants
TIME_PERIODS = 24  # 2 years of monthly data
START_DATE = datetime.datetime(2023, 1, 1)

def generate_time_series(base_value, volatility, periods, trend_factor=0.01, seasonality=True):
    """Generate realistic time series data with trend and seasonality."""
    time_series = []
    value = base_value
    
    for i in range(periods):
        # Add trend component
        trend = base_value * trend_factor * i
        
        # Add seasonality component (if enabled)
        season = 0
        if seasonality:
            season = base_value * 0.2 * np.sin(i * np.pi / 6)  # 12-month cycle
        
        # Add random component
        noise = random.normalvariate(0, volatility * base_value)
        
        # Calculate value for this period
        value = max(0, base_value + trend + season + noise)
        
        # Add to time series
        time_series.append(round(value, 2))
    
    return time_series

def generate_mock_embedding():
    """Generate a mock embedding vector (1536 dimensions)."""
    return [random.uniform(-1, 1) for _ in range(1536)]

def enhance_companies():
    """Enhance company data with time series and embeddings."""
    print("Enhancing company data...")
    companies = list(db.collection('companies').get())
    
    for company_doc in tqdm(companies):
        company = company_doc.to_dict()
        company_id = company_doc.id
        
        # Generate time series data if not present
        if 'time_series' not in company:
            # Generate base ESG scores
            env_base = company.get('sustainability_metrics', {}).get('environmental_score', random.uniform(50, 90))
            social_base = company.get('sustainability_metrics', {}).get('social_score', random.uniform(50, 90))
            gov_base = company.get('sustainability_metrics', {}).get('governance_score', random.uniform(50, 90))
            
            # Generate time series for ESG metrics
            env_scores = generate_time_series(env_base, 0.05, TIME_PERIODS)
            social_scores = generate_time_series(social_base, 0.04, TIME_PERIODS)
            gov_scores = generate_time_series(gov_base, 0.03, TIME_PERIODS)
            
            # Generate financial metrics
            revenue_base = random.uniform(1000000, 100000000)
            profit_margin_base = random.uniform(0.05, 0.25)
            
            revenue = generate_time_series(revenue_base, 0.1, TIME_PERIODS, trend_factor=0.02)
            profit_margin = generate_time_series(profit_margin_base, 0.1, TIME_PERIODS)
            
            # Generate sustainability metrics
            carbon_footprint_base = company.get('sustainability_metrics', {}).get('carbon_footprint', random.uniform(10000, 1000000))
            water_usage_base = company.get('sustainability_metrics', {}).get('water_usage', random.uniform(5000, 500000))
            waste_reduction_base = company.get('sustainability_metrics', {}).get('waste_reduction', random.uniform(10, 90))
            
            carbon_footprint = generate_time_series(carbon_footprint_base, 0.08, TIME_PERIODS, trend_factor=-0.01)
            water_usage = generate_time_series(water_usage_base, 0.06, TIME_PERIODS, trend_factor=-0.005)
            waste_reduction = generate_time_series(waste_reduction_base, 0.07, TIME_PERIODS, trend_factor=0.02)
            
            # Create time series data structure
            time_series_data = []
            for i in range(TIME_PERIODS):
                date = START_DATE + datetime.timedelta(days=30*i)
                time_series_data.append({
                    "date": date.isoformat(),
                    "environmental_score": env_scores[i],
                    "social_score": social_scores[i],
                    "governance_score": gov_scores[i],
                    "esg_score": round((env_scores[i] + social_scores[i] + gov_scores[i]) / 3, 2),
                    "revenue": revenue[i],
                    "profit_margin": profit_margin[i],
                    "carbon_footprint": carbon_footprint[i],
                    "water_usage": water_usage[i],
                    "waste_reduction": waste_reduction[i]
                })
            
            company['time_series'] = time_series_data
        
        # Add embedding if not present
        if 'embedding' not in company:
            company['embedding'] = generate_mock_embedding()
        
        # Update company in Firestore
        db.collection('companies').document(company_id).set(company)

def enhance_trends():
    """Enhance trend data with time series and embeddings."""
    print("Enhancing trend data...")
    trends = list(db.collection('trends').get())
    
    for trend_doc in tqdm(trends):
        trend = trend_doc.to_dict()
        trend_id = trend_doc.id
        
        # Generate time series data if not present
        if 'time_series' not in trend:
            # Generate base metrics
            relevance_base = trend.get('relevance', random.uniform(0.5, 0.9))
            growth_rate_base = random.uniform(0.1, 0.5)
            
            # Generate time series for trend metrics
            relevance = generate_time_series(relevance_base, 0.1, TIME_PERIODS, trend_factor=0.02)
            growth_rate = generate_time_series(growth_rate_base, 0.15, TIME_PERIODS)
            
            # Create time series data structure
            time_series_data = []
            for i in range(TIME_PERIODS):
                date = START_DATE + datetime.timedelta(days=30*i)
                time_series_data.append({
                    "date": date.isoformat(),
                    "relevance": relevance[i],
                    "growth_rate": growth_rate[i],
                    "momentum": round(relevance[i] * growth_rate[i], 2)
                })
            
            trend['time_series'] = time_series_data
        
        # Add embedding if not present
        if 'embedding' not in trend:
            trend['embedding'] = generate_mock_embedding()
        
        # Update trend in Firestore
        db.collection('trends').document(trend_id).set(trend)

def enhance_funds():
    """Enhance fund data with time series and embeddings."""
    print("Enhancing fund data...")
    funds = list(db.collection('funds').get())
    
    for fund_doc in tqdm(funds):
        fund = fund_doc.to_dict()
        fund_id = fund_doc.id
        
        # Generate time series data if not present
        if 'time_series' not in fund:
            # Generate base metrics
            aum_base = fund.get('aum', random.uniform(10000000, 1000000000))  # Assets under management
            return_base = fund.get('return', random.uniform(0.05, 0.2))  # Annual return
            
            # Generate time series for fund metrics
            aum = generate_time_series(aum_base, 0.1, TIME_PERIODS, trend_factor=0.02)
            returns = generate_time_series(return_base, 0.2, TIME_PERIODS)
            
            # Create time series data structure
            time_series_data = []
            for i in range(TIME_PERIODS):
                date = START_DATE + datetime.timedelta(days=30*i)
                time_series_data.append({
                    "date": date.isoformat(),
                    "aum": aum[i],
                    "return": returns[i]
                })
            
            fund['time_series'] = time_series_data
        
        # Add embedding if not present
        if 'embedding' not in fund:
            fund['embedding'] = generate_mock_embedding()
        
        # Update fund in Firestore
        db.collection('funds').document(fund_id).set(fund)

def enhance_graph_nodes():
    """Enhance graph nodes with additional metadata."""
    print("Enhancing graph nodes...")
    nodes = list(db.collection('graph_nodes').get())
    
    for node_doc in tqdm(nodes):
        node = node_doc.to_dict()
        node_id = node_doc.id
        
        # Add additional metadata based on node type
        if node['type'] == 'company':
            # Add industry influence score
            if 'industry_influence' not in node:
                node['industry_influence'] = round(random.uniform(0.1, 1.0), 2)
            
            # Add innovation score
            if 'innovation_score' not in node:
                node['innovation_score'] = round(random.uniform(0.1, 1.0), 2)
            
            # Add market share
            if 'market_share' not in node:
                node['market_share'] = round(random.uniform(0.01, 0.3), 2)
        
        elif node['type'] == 'trend':
            # Add adoption rate
            if 'adoption_rate' not in node:
                node['adoption_rate'] = round(random.uniform(0.1, 0.9), 2)
            
            # Add disruption potential
            if 'disruption_potential' not in node:
                node['disruption_potential'] = round(random.uniform(0.1, 1.0), 2)
            
            # Add time to mainstream
            if 'time_to_mainstream' not in node:
                node['time_to_mainstream'] = random.randint(1, 10)
        
        elif node['type'] == 'project':
            # Add ROI
            if 'roi' not in node:
                node['roi'] = round(random.uniform(0.05, 0.5), 2)
            
            # Add risk score
            if 'risk_score' not in node:
                node['risk_score'] = round(random.uniform(0.1, 0.9), 2)
            
            # Add innovation level
            if 'innovation_level' not in node:
                node['innovation_level'] = round(random.uniform(0.1, 1.0), 2)
        
        # Update node in Firestore
        db.collection('graph_nodes').document(node_id).set(node)

def enhance_graph_edges():
    """Enhance graph edges with additional metadata."""
    print("Enhancing graph edges...")
    edges = list(db.collection('graph_edges').get())
    
    for edge_doc in tqdm(edges):
        edge = edge_doc.to_dict()
        edge_id = edge_doc.id
        
        # Add additional metadata based on edge type
        if edge['type'] == 'influences':
            # Add impact score
            if 'impact_score' not in edge:
                edge['impact_score'] = round(random.uniform(0.1, 1.0), 2)
            
            # Add time lag
            if 'time_lag' not in edge:
                edge['time_lag'] = random.randint(1, 12)  # Months
        
        elif edge['type'] == 'owns':
            # Add ownership percentage
            if 'ownership_percentage' not in edge:
                edge['ownership_percentage'] = round(random.uniform(0.51, 1.0), 2)
            
            # Add investment amount
            if 'investment_amount' not in edge:
                edge['investment_amount'] = round(random.uniform(100000, 10000000), 2)
        
        elif edge['type'] == 'partners':
            # Add partnership duration
            if 'partnership_duration' not in edge:
                edge['partnership_duration'] = random.randint(1, 10)  # Years
            
            # Add collaboration score
            if 'collaboration_score' not in edge:
                edge['collaboration_score'] = round(random.uniform(0.1, 1.0), 2)
        
        elif edge['type'] == 'invests':
            # Add investment amount
            if 'investment_amount' not in edge:
                edge['investment_amount'] = round(random.uniform(1000000, 50000000), 2)
            
            # Add equity stake
            if 'equity_stake' not in edge:
                edge['equity_stake'] = round(random.uniform(0.05, 0.49), 2)
        
        # Update edge in Firestore
        db.collection('graph_edges').document(edge_id).set(edge)

def enhance_data():
    """Enhance all data in the database."""
    enhance_companies()
    enhance_trends()
    enhance_funds()
    enhance_graph_nodes()
    enhance_graph_edges()
    
    print("Data enhancement complete!")

if __name__ == "__main__":
    enhance_data()
