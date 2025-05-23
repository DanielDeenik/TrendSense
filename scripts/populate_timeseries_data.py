"""
Script to populate the database with extensive time series data and vector embeddings.
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
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import project modules
from src.database.adapters.firebase_adapter import FirebaseAdapter
from src.data_management.ai_connector import OpenAIConnector
from src.database.graph_manager import GraphManager

# Load environment variables
load_dotenv()

# Initialize Firebase
try:
    firebase_app = firebase_admin.get_app()
except ValueError:
    cred_path = os.path.join(os.path.dirname(__file__), '..', 'firebase', 'service-account-key.json')
    cred = credentials.Certificate(cred_path)
    firebase_app = firebase_admin.initialize_app(cred)

db = firestore.client()

# Initialize OpenAI connector for embeddings
openai_connector = OpenAIConnector()

# Initialize Firebase adapter
firebase_adapter = FirebaseAdapter()

# Initialize Graph Manager
graph_manager = GraphManager()

# Constants
NUM_COMPANIES = 20
NUM_TRENDS = 15
NUM_PROJECTS = 30
NUM_FUNDS = 10
TIME_PERIODS = 24  # 2 years of monthly data
START_DATE = datetime.datetime(2023, 1, 1)

# Lists for data generation
SECTORS = [
    "Clean Energy", "Sustainable Agriculture", "Green Transportation",
    "Circular Economy", "Water Management", "Carbon Capture",
    "Sustainable Materials", "Green Building", "Waste Management",
    "Renewable Energy"
]

TREND_CATEGORIES = [
    "Environmental", "Social", "Governance", "Technology",
    "Policy", "Market", "Consumer Behavior", "Climate Change",
    "Resource Scarcity", "Biodiversity"
]

PROJECT_TYPES = [
    "Research & Development", "Product Launch", "Infrastructure",
    "Software Development", "Community Initiative", "Policy Implementation",
    "Market Expansion", "Sustainability Initiative", "Innovation Lab"
]

SDG_GOALS = list(range(1, 18))  # SDGs 1-17

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

def generate_company_data():
    """Generate data for a company with time series metrics."""
    company_id = f"company_{random.randint(10000, 99999)}"
    sector = random.choice(SECTORS)
    founding_year = random.randint(1990, 2020)

    # Generate base ESG scores
    env_base = random.uniform(50, 90)
    social_base = random.uniform(50, 90)
    gov_base = random.uniform(50, 90)

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
    carbon_footprint_base = random.uniform(10000, 1000000)
    water_usage_base = random.uniform(5000, 500000)
    waste_reduction_base = random.uniform(10, 90)

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

    # Create company document
    company = {
        "id": company_id,
        "name": f"{sector} {['Solutions', 'Technologies', 'Innovations', 'Group', 'Corp'][random.randint(0, 4)]} {random.randint(1, 99)}",
        "sector": sector,
        "founding_year": founding_year,
        "description": f"A leading company in the {sector} sector focused on sustainable solutions.",
        "sustainability_metrics": {
            "environmental_score": env_scores[-1],
            "social_score": social_scores[-1],
            "governance_score": gov_scores[-1],
            "esg_score": round((env_scores[-1] + social_scores[-1] + gov_scores[-1]) / 3, 2),
            "carbon_footprint": carbon_footprint[-1],
            "water_usage": water_usage[-1],
            "waste_reduction": waste_reduction[-1]
        },
        "financial_metrics": {
            "revenue": revenue[-1],
            "profit_margin": profit_margin[-1],
            "market_cap": round(revenue[-1] * random.uniform(2, 10), 2)
        },
        "time_series": time_series_data,
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }

    # Generate embedding for the company
    text_for_embedding = f"{company['name']} {company['description']} {company['sector']}"
    company["embedding"] = openai_connector.generate_embedding(text_for_embedding)

    return company

def generate_trend_data():
    """Generate data for a sustainability trend with time series metrics."""
    trend_id = f"trend_{random.randint(10000, 99999)}"
    category = random.choice(TREND_CATEGORIES)

    # Generate base metrics
    relevance_base = random.uniform(0.5, 0.9)
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

    # Determine maturity stage based on growth rate
    avg_growth = sum(growth_rate) / len(growth_rate)
    if avg_growth > 0.3:
        maturity_stage = "Emerging"
    elif avg_growth > 0.15:
        maturity_stage = "Growing"
    else:
        maturity_stage = "Mature"

    # Create trend document
    trend = {
        "id": trend_id,
        "name": f"{category} {['Transformation', 'Revolution', 'Innovation', 'Movement', 'Shift'][random.randint(0, 4)]}",
        "category": category,
        "description": f"A significant trend in {category} that is reshaping sustainability practices.",
        "relevance_score": relevance[-1],
        "growth_rate": growth_rate[-1],
        "maturity_stage": maturity_stage,
        "time_series": time_series_data,
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }

    # Generate embedding for the trend
    text_for_embedding = f"{trend['name']} {trend['description']} {trend['category']}"
    trend["embedding"] = openai_connector.generate_embedding(text_for_embedding)

    return trend

def generate_project_data(company_ids):
    """Generate data for a sustainability project with time series metrics."""
    project_id = f"project_{random.randint(10000, 99999)}"
    project_type = random.choice(PROJECT_TYPES)
    company_id = random.choice(company_ids)

    # Generate base metrics
    budget_base = random.uniform(100000, 10000000)
    progress_base = random.uniform(0.1, 0.9)
    carbon_impact_base = -random.uniform(1000, 100000)  # Negative for reduction

    # Generate time series for project metrics
    budget = generate_time_series(budget_base, 0.05, TIME_PERIODS)
    progress = [min(1.0, p/100) for p in generate_time_series(progress_base*100, 2, TIME_PERIODS, trend_factor=0.05)]
    carbon_impact = generate_time_series(carbon_impact_base, 0.1, TIME_PERIODS, trend_factor=-0.02)

    # Create time series data structure
    time_series_data = []
    for i in range(TIME_PERIODS):
        date = START_DATE + datetime.timedelta(days=30*i)
        time_series_data.append({
            "date": date.isoformat(),
            "budget": budget[i],
            "progress": progress[i],
            "carbon_impact": carbon_impact[i]
        })

    # Determine status based on progress
    if progress[-1] < 0.3:
        status = "Planning"
    elif progress[-1] < 0.7:
        status = "In Progress"
    elif progress[-1] < 1.0:
        status = "Final Stages"
    else:
        status = "Completed"

    # Select random SDGs that this project aligns with
    sdg_alignment = sorted(random.sample(SDG_GOALS, random.randint(1, 5)))

    # Create project document
    project = {
        "id": project_id,
        "name": f"{project_type} {['Project', 'Initiative', 'Program', 'Venture', 'Effort'][random.randint(0, 4)]}",
        "type": project_type,
        "company_id": company_id,
        "description": f"A {project_type} project focused on sustainability innovation.",
        "status": status,
        "budget": budget[-1],
        "progress": progress[-1],
        "sustainability_metrics": {
            "carbon_impact": carbon_impact[-1],
            "sdg_alignment": sdg_alignment,
            "social_score": random.uniform(50, 90)
        },
        "time_series": time_series_data,
        "start_date": (START_DATE - datetime.timedelta(days=random.randint(30, 365))).isoformat(),
        "end_date": (START_DATE + datetime.timedelta(days=random.randint(365, 730))).isoformat(),
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }

    # Generate embedding for the project
    text_for_embedding = f"{project['name']} {project['description']} {project['type']}"
    project["embedding"] = openai_connector.generate_embedding(text_for_embedding)

    return project

def generate_fund_data(company_ids):
    """Generate data for a venture capital fund with time series metrics."""
    fund_id = f"fund_{random.randint(10000, 99999)}"

    # Generate base metrics
    aum_base = random.uniform(10000000, 1000000000)  # Assets under management
    return_base = random.uniform(0.05, 0.2)  # Annual return

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

    # Select random companies in the portfolio
    portfolio_companies = random.sample(company_ids, min(len(company_ids), random.randint(3, 10)))

    # Create fund document
    fund = {
        "id": fund_id,
        "name": f"{['Green', 'Sustainable', 'Impact', 'ESG', 'Climate'][random.randint(0, 4)]} {['Ventures', 'Capital', 'Partners', 'Investments', 'Fund'][random.randint(0, 4)]}",
        "description": "A venture capital fund focused on sustainable investments.",
        "aum": aum[-1],  # Assets under management
        "return": returns[-1],  # Annual return
        "portfolio_companies": portfolio_companies,
        "sustainability_focus": random.sample(SECTORS, random.randint(2, 5)),
        "time_series": time_series_data,
        "inception_date": (START_DATE - datetime.timedelta(days=random.randint(365, 3650))).isoformat(),
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }

    # Generate embedding for the fund
    text_for_embedding = f"{fund['name']} {fund['description']} {' '.join(fund['sustainability_focus'])}"
    fund["embedding"] = openai_connector.generate_embedding(text_for_embedding)

    return fund

def generate_graph_relationships(companies, trends, projects, funds):
    """Generate graph relationships between entities."""
    nodes = []
    edges = []

    # Add companies as nodes
    for company in companies:
        nodes.append({
            "id": company["id"],
            "name": company["name"],
            "type": "company",
            "sector": company["sector"],
            "sustainability_metrics": company["sustainability_metrics"]
        })

    # Add trends as nodes
    for trend in trends:
        nodes.append({
            "id": trend["id"],
            "name": trend["name"],
            "type": "trend",
            "category": trend["category"],
            "relevance": trend["relevance_score"],
            "growth_rate": trend["growth_rate"],
            "maturity_stage": trend["maturity_stage"]
        })

    # Add projects as nodes
    for project in projects:
        nodes.append({
            "id": project["id"],
            "name": project["name"],
            "type": "project",
            "status": project["status"],
            "sustainability_metrics": project["sustainability_metrics"]
        })

    # Add funds as nodes
    for fund in funds:
        nodes.append({
            "id": fund["id"],
            "name": fund["name"],
            "type": "fund",
            "aum": fund["aum"],
            "return": fund["return"]
        })

    # Create edges between companies and trends
    for company in companies:
        # Each company is influenced by 2-5 trends
        for trend_id in random.sample([t["id"] for t in trends], random.randint(2, min(5, len(trends)))):
            edges.append({
                "source": trend_id,
                "target": company["id"],
                "type": "influences",
                "strength": round(random.uniform(0.3, 1.0), 2)
            })

    # Create edges between companies and projects
    for project in projects:
        # Each project is owned by a company
        edges.append({
            "source": project["company_id"],
            "target": project["id"],
            "type": "owns",
            "strength": 1.0
        })

    # Create edges between companies
    for i in range(len(companies) * 2):  # Create approximately 2 partnerships per company
        company1 = random.choice(companies)
        company2 = random.choice(companies)
        if company1["id"] != company2["id"]:
            edges.append({
                "source": company1["id"],
                "target": company2["id"],
                "type": "partners",
                "strength": round(random.uniform(0.3, 0.9), 2)
            })

    # Create edges between funds and companies
    for fund in funds:
        for company_id in fund["portfolio_companies"]:
            edges.append({
                "source": fund["id"],
                "target": company_id,
                "type": "invests",
                "strength": round(random.uniform(0.5, 1.0), 2)
            })

    return nodes, edges

def populate_database():
    """Populate the database with generated data."""
    print("Generating companies...")
    companies = [generate_company_data() for _ in tqdm(range(NUM_COMPANIES))]

    print("Generating trends...")
    trends = [generate_trend_data() for _ in tqdm(range(NUM_TRENDS))]

    print("Generating projects...")
    company_ids = [company["id"] for company in companies]
    projects = [generate_project_data(company_ids) for _ in tqdm(range(NUM_PROJECTS))]

    print("Generating funds...")
    funds = [generate_fund_data(company_ids) for _ in tqdm(range(NUM_FUNDS))]

    print("Generating graph relationships...")
    nodes, edges = generate_graph_relationships(companies, trends, projects, funds)

    print("Saving data to Firebase...")

    # Save companies
    for company in tqdm(companies, desc="Saving companies"):
        db.collection("companies").document(company["id"]).set(company)

    # Save trends
    for trend in tqdm(trends, desc="Saving trends"):
        db.collection("trends").document(trend["id"]).set(trend)

    # Save projects
    for project in tqdm(projects, desc="Saving projects"):
        db.collection("projects").document(project["id"]).set(project)

    # Save funds
    for fund in tqdm(funds, desc="Saving funds"):
        db.collection("funds").document(fund["id"]).set(fund)

    # Save graph nodes and edges
    for node in tqdm(nodes, desc="Saving graph nodes"):
        db.collection("graph_nodes").document(node["id"]).set(node)

    for i, edge in enumerate(tqdm(edges, desc="Saving graph edges")):
        edge_id = f"edge_{i}"
        db.collection("graph_edges").document(edge_id).set(edge)

    print("Data population complete!")
    print(f"Created {len(companies)} companies, {len(trends)} trends, {len(projects)} projects, {len(funds)} funds")
    print(f"Created {len(nodes)} graph nodes and {len(edges)} graph edges")

if __name__ == "__main__":
    populate_database()
