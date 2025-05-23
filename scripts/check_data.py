"""
Script to check the current state of the data in Firebase.
"""

import os
import sys
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

def check_data():
    """Check the current state of the data in Firebase."""
    print("Checking data in Firebase...")
    
    # Check collections
    companies = list(db.collection('companies').get())
    trends = list(db.collection('trends').get())
    projects = list(db.collection('projects').get())
    funds = list(db.collection('funds').get())
    graph_nodes = list(db.collection('graph_nodes').get())
    graph_edges = list(db.collection('graph_edges').get())
    
    print(f"Companies: {len(companies)}")
    print(f"Trends: {len(trends)}")
    print(f"Projects: {len(projects)}")
    print(f"Funds: {len(funds)}")
    print(f"Graph Nodes: {len(graph_nodes)}")
    print(f"Graph Edges: {len(graph_edges)}")
    
    # Check if companies have time series data
    if companies:
        company = companies[0].to_dict()
        if 'time_series' in company:
            print(f"\nCompany time series data points: {len(company['time_series'])}")
            print(f"Sample time series data: {company['time_series'][0]}")
        else:
            print("\nCompanies do not have time series data")
    
    # Check if trends have time series data
    if trends:
        trend = trends[0].to_dict()
        if 'time_series' in trend:
            print(f"\nTrend time series data points: {len(trend['time_series'])}")
            print(f"Sample time series data: {trend['time_series'][0]}")
        else:
            print("\nTrends do not have time series data")
    
    # Check if projects have time series data
    if projects:
        project = projects[0].to_dict()
        if 'time_series' in project:
            print(f"\nProject time series data points: {len(project['time_series'])}")
            print(f"Sample time series data: {project['time_series'][0]}")
        else:
            print("\nProjects do not have time series data")
    
    # Check if funds have time series data
    if funds:
        fund = funds[0].to_dict()
        if 'time_series' in fund:
            print(f"\nFund time series data points: {len(fund['time_series'])}")
            print(f"Sample time series data: {fund['time_series'][0]}")
        else:
            print("\nFunds do not have time series data")
    
    # Check if entities have embeddings
    if companies:
        company = companies[0].to_dict()
        if 'embedding' in company:
            print("\nCompanies have embeddings")
        else:
            print("\nCompanies do not have embeddings")
    
    # Check graph node data
    if graph_nodes:
        node = graph_nodes[0].to_dict()
        print(f"\nSample graph node: {node}")
    
    # Check graph edge data
    if graph_edges:
        edge = graph_edges[0].to_dict()
        print(f"\nSample graph edge: {edge}")

if __name__ == "__main__":
    check_data()
