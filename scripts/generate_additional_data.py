"""
Script to generate additional data for the database with more complex relationships and metrics.
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

# Initialize Vector Store
vector_store = VectorStore()

# Constants
NUM_ADDITIONAL_COMPANIES = 30
NUM_ADDITIONAL_TRENDS = 20
NUM_ADDITIONAL_PROJECTS = 40
NUM_ADDITIONAL_FUNDS = 15
TIME_PERIODS = 36  # 3 years of monthly data
START_DATE = datetime.datetime(2022, 1, 1)

# Lists for data generation
SECTORS = [
    "Clean Energy", "Sustainable Agriculture", "Green Transportation",
    "Circular Economy", "Water Management", "Carbon Capture",
    "Sustainable Materials", "Green Building", "Waste Management",
    "Renewable Energy", "Energy Storage", "Smart Grid", "Biodiversity",
    "Ocean Conservation", "Sustainable Fashion", "Plant-based Foods",
    "Green Hydrogen", "Climate Tech", "Sustainable Finance", "ESG Analytics"
]

TREND_CATEGORIES = [
    "Environmental", "Social", "Governance", "Technology",
    "Policy", "Market", "Consumer Behavior", "Climate Change",
    "Resource Scarcity", "Biodiversity", "Circular Economy",
    "Renewable Energy", "Sustainable Finance", "Green Buildings",
    "Sustainable Transportation", "Carbon Markets", "Climate Resilience",
    "Sustainable Supply Chain", "ESG Reporting", "Impact Investing"
]

PROJECT_TYPES = [
    "Research & Development", "Product Launch", "Infrastructure",
    "Software Development", "Community Initiative", "Policy Implementation",
    "Market Expansion", "Sustainability Initiative", "Innovation Lab",
    "Pilot Program", "Retrofit", "Certification", "Supply Chain Optimization",
    "Circular Economy Implementation", "Carbon Offset", "Renewable Energy Installation",
    "Waste Reduction", "Water Conservation", "Biodiversity Protection", "ESG Reporting"
]

FUND_TYPES = [
    "Venture Capital", "Private Equity", "Impact Fund", "ESG Fund",
    "Green Bond Fund", "Climate Tech Fund", "Sustainable Infrastructure Fund",
    "Circular Economy Fund", "Clean Energy Fund", "Water Fund",
    "Sustainable Agriculture Fund", "Green Real Estate Fund"
]

COUNTRIES = [
    "United States", "United Kingdom", "Germany", "France", "Netherlands",
    "Sweden", "Denmark", "Norway", "Canada", "Australia", "Japan",
    "Singapore", "Switzerland", "Finland", "Spain", "Italy", "Brazil",
    "India", "China", "South Africa", "Kenya", "Chile", "Mexico"
]

COMPANY_SIZES = ["Startup", "Small", "Medium", "Large", "Enterprise"]

SDG_GOALS = list(range(1, 18))  # SDGs 1-17

def generate_time_series(base_value, volatility, periods, trend_factor=0.01, seasonality=True,
                         shock_events=True, shock_magnitude=0.2, shock_recovery_periods=3):
    """Generate realistic time series data with trend, seasonality, and shock events."""
    time_series = []
    value = base_value

    # Generate random shock events
    shock_periods = []
    if shock_events:
        num_shocks = random.randint(1, 3)
        shock_periods = sorted(random.sample(range(periods), num_shocks))

    for i in range(periods):
        # Add trend component
        trend = base_value * trend_factor * i

        # Add seasonality component (if enabled)
        season = 0
        if seasonality:
            season = base_value * 0.2 * np.sin(i * np.pi / 6)  # 12-month cycle

        # Add shock component (if this is a shock period)
        shock = 0
        if i in shock_periods:
            # Negative shock
            shock = -base_value * shock_magnitude
        elif i - 1 in shock_periods:
            # First recovery period
            shock = -base_value * shock_magnitude * 0.7
        elif i - 2 in shock_periods:
            # Second recovery period
            shock = -base_value * shock_magnitude * 0.3

        # Add random component
        noise = random.normalvariate(0, volatility * base_value)

        # Calculate value for this period
        value = max(0, base_value + trend + season + shock + noise)

        # Add to time series
        time_series.append(round(value, 2))

    return time_series

def generate_mock_embedding():
    """Generate a mock embedding vector (1536 dimensions)."""
    return [random.uniform(-1, 1) for _ in range(1536)]

def generate_company_data():
    """Generate data for a company with time series metrics."""
    company_id = f"company_{random.randint(100000, 999999)}"
    sector = random.choice(SECTORS)
    founding_year = random.randint(1990, 2022)
    company_size = random.choice(COMPANY_SIZES)
    country = random.choice(COUNTRIES)

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
    market_cap_base = revenue_base * random.uniform(2, 10)

    revenue = generate_time_series(revenue_base, 0.1, TIME_PERIODS, trend_factor=0.02)
    profit_margin = generate_time_series(profit_margin_base, 0.1, TIME_PERIODS)
    market_cap = generate_time_series(market_cap_base, 0.15, TIME_PERIODS, trend_factor=0.025)

    # Generate sustainability metrics
    carbon_footprint_base = random.uniform(10000, 1000000)
    water_usage_base = random.uniform(5000, 500000)
    waste_reduction_base = random.uniform(10, 90)
    renewable_energy_pct_base = random.uniform(5, 60)

    carbon_footprint = generate_time_series(carbon_footprint_base, 0.08, TIME_PERIODS, trend_factor=-0.01)
    water_usage = generate_time_series(water_usage_base, 0.06, TIME_PERIODS, trend_factor=-0.005)
    waste_reduction = generate_time_series(waste_reduction_base, 0.07, TIME_PERIODS, trend_factor=0.02)
    renewable_energy_pct = generate_time_series(renewable_energy_pct_base, 0.05, TIME_PERIODS, trend_factor=0.03)

    # Generate innovation metrics
    r_and_d_spending_base = revenue_base * random.uniform(0.05, 0.2)
    patents_filed_base = random.uniform(1, 20)
    innovation_score_base = random.uniform(50, 90)

    r_and_d_spending = generate_time_series(r_and_d_spending_base, 0.1, TIME_PERIODS, trend_factor=0.02)
    patents_filed = [max(0, round(p)) for p in generate_time_series(patents_filed_base, 0.3, TIME_PERIODS)]
    innovation_score = generate_time_series(innovation_score_base, 0.05, TIME_PERIODS)

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
            "market_cap": market_cap[i],
            "carbon_footprint": carbon_footprint[i],
            "water_usage": water_usage[i],
            "waste_reduction": waste_reduction[i],
            "renewable_energy_percentage": renewable_energy_pct[i],
            "r_and_d_spending": r_and_d_spending[i],
            "patents_filed": patents_filed[i],
            "innovation_score": innovation_score[i]
        })

    # Create company document
    company = {
        "id": company_id,
        "name": f"{sector} {['Solutions', 'Technologies', 'Innovations', 'Group', 'Corp', 'Inc', 'Partners', 'Ventures'][random.randint(0, 7)]} {random.randint(1, 99)}",
        "sector": sector,
        "founding_year": founding_year,
        "company_size": company_size,
        "country": country,
        "description": f"A {company_size.lower()} company in the {sector} sector focused on sustainable solutions based in {country}.",
        "sustainability_metrics": {
            "environmental_score": env_scores[-1],
            "social_score": social_scores[-1],
            "governance_score": gov_scores[-1],
            "esg_score": round((env_scores[-1] + social_scores[-1] + gov_scores[-1]) / 3, 2),
            "carbon_footprint": carbon_footprint[-1],
            "water_usage": water_usage[-1],
            "waste_reduction": waste_reduction[-1],
            "renewable_energy_percentage": renewable_energy_pct[-1]
        },
        "financial_metrics": {
            "revenue": revenue[-1],
            "profit_margin": profit_margin[-1],
            "market_cap": market_cap[-1]
        },
        "innovation_metrics": {
            "r_and_d_spending": r_and_d_spending[-1],
            "patents_filed": patents_filed[-1],
            "innovation_score": innovation_score[-1]
        },
        "time_series": time_series_data,
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }

    # Generate embedding for the company
    company["embedding"] = generate_mock_embedding()

    return company

def generate_trend_data():
    """Generate data for a sustainability trend with time series metrics."""
    trend_id = f"trend_{random.randint(100000, 999999)}"
    category = random.choice(TREND_CATEGORIES)

    # Generate base metrics
    relevance_base = random.uniform(0.5, 0.9)
    growth_rate_base = random.uniform(0.1, 0.5)
    adoption_rate_base = random.uniform(0.1, 0.7)
    market_size_base = random.uniform(1000000, 10000000000)

    # Generate time series for trend metrics
    relevance = generate_time_series(relevance_base, 0.1, TIME_PERIODS, trend_factor=0.02)
    growth_rate = generate_time_series(growth_rate_base, 0.15, TIME_PERIODS)
    adoption_rate = generate_time_series(adoption_rate_base, 0.08, TIME_PERIODS, trend_factor=0.03)
    market_size = generate_time_series(market_size_base, 0.12, TIME_PERIODS, trend_factor=0.04)

    # Generate impact metrics
    carbon_impact_base = -random.uniform(10000, 1000000)  # Negative for reduction
    social_impact_base = random.uniform(50, 90)
    policy_influence_base = random.uniform(0.1, 0.9)

    carbon_impact = generate_time_series(carbon_impact_base, 0.1, TIME_PERIODS, trend_factor=-0.02)
    social_impact = generate_time_series(social_impact_base, 0.05, TIME_PERIODS)
    policy_influence = generate_time_series(policy_influence_base, 0.1, TIME_PERIODS)

    # Create time series data structure
    time_series_data = []
    for i in range(TIME_PERIODS):
        date = START_DATE + datetime.timedelta(days=30*i)
        time_series_data.append({
            "date": date.isoformat(),
            "relevance": relevance[i],
            "growth_rate": growth_rate[i],
            "adoption_rate": adoption_rate[i],
            "market_size": market_size[i],
            "momentum": round(relevance[i] * growth_rate[i], 2),
            "carbon_impact": carbon_impact[i],
            "social_impact": social_impact[i],
            "policy_influence": policy_influence[i]
        })

    # Determine maturity stage based on adoption rate
    avg_adoption = sum(adoption_rate) / len(adoption_rate)
    if avg_adoption < 0.2:
        maturity_stage = "Emerging"
    elif avg_adoption < 0.5:
        maturity_stage = "Growing"
    else:
        maturity_stage = "Mature"

    # Select random SDGs that this trend aligns with
    sdg_alignment = sorted(random.sample(SDG_GOALS, random.randint(2, 6)))

    # Create trend document
    trend = {
        "id": trend_id,
        "name": f"{category} {['Transformation', 'Revolution', 'Innovation', 'Movement', 'Shift', 'Transition', 'Evolution', 'Paradigm'][random.randint(0, 7)]}",
        "category": category,
        "description": f"A significant trend in {category} that is reshaping sustainability practices and markets.",
        "relevance_score": relevance[-1],
        "growth_rate": growth_rate[-1],
        "adoption_rate": adoption_rate[-1],
        "market_size": market_size[-1],
        "maturity_stage": maturity_stage,
        "impact_metrics": {
            "carbon_impact": carbon_impact[-1],
            "social_impact": social_impact[-1],
            "policy_influence": policy_influence[-1],
            "sdg_alignment": sdg_alignment
        },
        "time_series": time_series_data,
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }

    # Generate embedding for the trend
    trend["embedding"] = generate_mock_embedding()

    return trend

def generate_project_data(company_ids):
    """Generate data for a sustainability project with time series metrics."""
    project_id = f"project_{random.randint(100000, 999999)}"
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

    # Generate additional metrics
    roi_base = random.uniform(0.05, 0.3)
    risk_score_base = random.uniform(0.1, 0.7)
    innovation_level_base = random.uniform(0.3, 0.9)

    roi = generate_time_series(roi_base, 0.1, TIME_PERIODS)
    risk_score = generate_time_series(risk_score_base, 0.05, TIME_PERIODS, trend_factor=-0.01)
    innovation_level = generate_time_series(innovation_level_base, 0.05, TIME_PERIODS)

    # Create time series data structure
    time_series_data = []
    for i in range(TIME_PERIODS):
        date = START_DATE + datetime.timedelta(days=30*i)
        time_series_data.append({
            "date": date.isoformat(),
            "budget": budget[i],
            "progress": progress[i],
            "carbon_impact": carbon_impact[i],
            "roi": roi[i],
            "risk_score": risk_score[i],
            "innovation_level": innovation_level[i]
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
        "name": f"{project_type} {['Project', 'Initiative', 'Program', 'Venture', 'Effort', 'Implementation', 'Deployment', 'Solution'][random.randint(0, 7)]}",
        "type": project_type,
        "company_id": company_id,
        "description": f"A {project_type} project focused on sustainability innovation and impact.",
        "status": status,
        "budget": budget[-1],
        "progress": progress[-1],
        "sustainability_metrics": {
            "carbon_impact": carbon_impact[-1],
            "sdg_alignment": sdg_alignment,
            "social_score": random.uniform(50, 90)
        },
        "performance_metrics": {
            "roi": roi[-1],
            "risk_score": risk_score[-1],
            "innovation_level": innovation_level[-1]
        },
        "time_series": time_series_data,
        "start_date": (START_DATE - datetime.timedelta(days=random.randint(30, 365))).isoformat(),
        "end_date": (START_DATE + datetime.timedelta(days=random.randint(365, 1095))).isoformat(),
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }

    # Generate embedding for the project
    project["embedding"] = generate_mock_embedding()

    return project

def generate_fund_data(company_ids):
    """Generate data for a venture capital fund with time series metrics."""
    fund_id = f"fund_{random.randint(100000, 999999)}"
    fund_type = random.choice(FUND_TYPES)
    country = random.choice(COUNTRIES)

    # Generate base metrics
    aum_base = random.uniform(10000000, 1000000000)  # Assets under management
    return_base = random.uniform(0.05, 0.2)  # Annual return

    # Generate time series for fund metrics
    aum = generate_time_series(aum_base, 0.1, TIME_PERIODS, trend_factor=0.02)
    returns = generate_time_series(return_base, 0.2, TIME_PERIODS)

    # Generate additional metrics
    esg_score_base = random.uniform(60, 95)
    impact_score_base = random.uniform(50, 90)
    carbon_intensity_base = random.uniform(10, 100)

    esg_score = generate_time_series(esg_score_base, 0.05, TIME_PERIODS, trend_factor=0.01)
    impact_score = generate_time_series(impact_score_base, 0.07, TIME_PERIODS, trend_factor=0.02)
    carbon_intensity = generate_time_series(carbon_intensity_base, 0.1, TIME_PERIODS, trend_factor=-0.02)

    # Create time series data structure
    time_series_data = []
    for i in range(TIME_PERIODS):
        date = START_DATE + datetime.timedelta(days=30*i)
        time_series_data.append({
            "date": date.isoformat(),
            "aum": aum[i],
            "return": returns[i],
            "esg_score": esg_score[i],
            "impact_score": impact_score[i],
            "carbon_intensity": carbon_intensity[i]
        })

    # Select random companies in the portfolio
    portfolio_companies = random.sample(company_ids, min(len(company_ids), random.randint(5, 15)))

    # Select random sectors of focus
    sustainability_focus = random.sample(SECTORS, random.randint(3, 8))

    # Create fund document
    fund = {
        "id": fund_id,
        "name": f"{['Green', 'Sustainable', 'Impact', 'ESG', 'Climate', 'Eco', 'Future', 'Regenerative'][random.randint(0, 7)]} {fund_type}",
        "type": fund_type,
        "country": country,
        "description": f"A {fund_type} focused on sustainable investments in {', '.join(sustainability_focus[:3])} and other sectors.",
        "aum": aum[-1],  # Assets under management
        "return": returns[-1],  # Annual return
        "portfolio_companies": portfolio_companies,
        "sustainability_focus": sustainability_focus,
        "performance_metrics": {
            "esg_score": esg_score[-1],
            "impact_score": impact_score[-1],
            "carbon_intensity": carbon_intensity[-1]
        },
        "time_series": time_series_data,
        "inception_date": (START_DATE - datetime.timedelta(days=random.randint(365, 3650))).isoformat(),
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat()
    }

    # Generate embedding for the fund
    fund["embedding"] = generate_mock_embedding()

    return fund

def generate_graph_relationships(companies, trends, projects, funds, existing_nodes=None, existing_edges=None):
    """Generate graph relationships between entities."""
    nodes = []
    edges = []

    # Get existing node IDs if provided
    existing_node_ids = set()
    if existing_nodes:
        existing_node_ids = {node["id"] for node in existing_nodes}

    # Get existing edge pairs if provided
    existing_edge_pairs = set()
    if existing_edges:
        existing_edge_pairs = {(edge["source"], edge["target"]) for edge in existing_edges}

    # Add companies as nodes
    for company in companies:
        if company["id"] not in existing_node_ids:
            nodes.append({
                "id": company["id"],
                "name": company["name"],
                "type": "company",
                "sector": company["sector"],
                "country": company["country"],
                "company_size": company["company_size"],
                "sustainability_metrics": company["sustainability_metrics"],
                "financial_metrics": company["financial_metrics"],
                "innovation_metrics": company["innovation_metrics"]
            })

    # Add trends as nodes
    for trend in trends:
        if trend["id"] not in existing_node_ids:
            nodes.append({
                "id": trend["id"],
                "name": trend["name"],
                "type": "trend",
                "category": trend["category"],
                "relevance": trend["relevance_score"],
                "growth_rate": trend["growth_rate"],
                "adoption_rate": trend["adoption_rate"],
                "market_size": trend["market_size"],
                "maturity_stage": trend["maturity_stage"],
                "impact_metrics": trend["impact_metrics"]
            })

    # Add projects as nodes
    for project in projects:
        if project["id"] not in existing_node_ids:
            nodes.append({
                "id": project["id"],
                "name": project["name"],
                "type": "project",
                "project_type": project["type"],
                "status": project["status"],
                "budget": project["budget"],
                "progress": project["progress"],
                "sustainability_metrics": project["sustainability_metrics"],
                "performance_metrics": project["performance_metrics"]
            })

    # Add funds as nodes
    for fund in funds:
        if fund["id"] not in existing_node_ids:
            nodes.append({
                "id": fund["id"],
                "name": fund["name"],
                "type": "fund",
                "fund_type": fund["type"],
                "country": fund["country"],
                "aum": fund["aum"],
                "return": fund["return"],
                "performance_metrics": fund["performance_metrics"]
            })

    # Create edges between companies and trends
    for company in companies:
        # Each company is influenced by 3-7 trends
        for trend in random.sample(trends, min(random.randint(3, 7), len(trends))):
            edge_pair = (trend["id"], company["id"])
            if edge_pair not in existing_edge_pairs:
                # Calculate influence strength based on sector alignment
                base_strength = random.uniform(0.3, 1.0)
                sector_alignment = 1.0 if trend["category"].lower() in company["sector"].lower() else 0.7
                strength = round(base_strength * sector_alignment, 2)

                edges.append({
                    "source": trend["id"],
                    "target": company["id"],
                    "type": "influences",
                    "strength": strength,
                    "impact_score": round(random.uniform(0.1, 1.0), 2),
                    "time_lag": random.randint(1, 12)  # Months
                })

    # Create edges between companies and projects
    for project in projects:
        # Each project is owned by a company
        edge_pair = (project["company_id"], project["id"])
        if edge_pair not in existing_edge_pairs:
            edges.append({
                "source": project["company_id"],
                "target": project["id"],
                "type": "owns",
                "strength": 1.0,
                "ownership_percentage": 1.0,
                "investment_amount": project["budget"]
            })

    # Create edges between companies
    # Create a more complex network with partnerships, suppliers, competitors
    for i, company1 in enumerate(companies):
        for j, company2 in enumerate(companies):
            if i != j:
                # Determine relationship type based on sectors and random chance
                relationship_type = None
                if company1["sector"] == company2["sector"]:
                    # Same sector - could be partners or competitors
                    relationship_type = random.choice(["partners", "competes_with"])
                else:
                    # Different sectors - could be partners or supplier/customer
                    relationship_type = random.choice(["partners", "supplies_to"])

                # Only create some of the possible relationships to avoid too many edges
                if random.random() < 0.15:  # 15% chance of creating a relationship
                    edge_pair = (company1["id"], company2["id"])
                    if edge_pair not in existing_edge_pairs:
                        strength = round(random.uniform(0.3, 0.9), 2)

                        edge_data = {
                            "source": company1["id"],
                            "target": company2["id"],
                            "type": relationship_type,
                            "strength": strength
                        }

                        if relationship_type == "partners":
                            edge_data["partnership_duration"] = random.randint(1, 10)  # Years
                            edge_data["collaboration_score"] = round(random.uniform(0.1, 1.0), 2)
                        elif relationship_type == "competes_with":
                            edge_data["market_overlap"] = round(random.uniform(0.1, 0.9), 2)
                            edge_data["competition_intensity"] = round(random.uniform(0.1, 1.0), 2)
                        elif relationship_type == "supplies_to":
                            edge_data["supply_volume"] = round(random.uniform(100000, 10000000), 2)
                            edge_data["dependency_level"] = round(random.uniform(0.1, 0.8), 2)

                        edges.append(edge_data)

    # Create edges between funds and companies
    for fund in funds:
        for company_id in fund["portfolio_companies"]:
            edge_pair = (fund["id"], company_id)
            if edge_pair not in existing_edge_pairs:
                # Calculate investment details
                strength = round(random.uniform(0.5, 1.0), 2)
                investment_amount = round(random.uniform(1000000, 50000000), 2)
                equity_stake = round(random.uniform(0.05, 0.49), 2)

                edges.append({
                    "source": fund["id"],
                    "target": company_id,
                    "type": "invests",
                    "strength": strength,
                    "investment_amount": investment_amount,
                    "equity_stake": equity_stake,
                    "investment_date": (START_DATE - datetime.timedelta(days=random.randint(30, 1095))).isoformat()
                })

    # Create edges between trends
    for i, trend1 in enumerate(trends):
        for j, trend2 in enumerate(trends):
            if i != j:
                # Determine relationship type based on categories and random chance
                relationship_type = None
                if trend1["category"] == trend2["category"]:
                    # Same category - could be related or competing
                    relationship_type = random.choice(["related_to", "competes_with"])
                else:
                    # Different categories - could be related or enabling
                    relationship_type = random.choice(["related_to", "enables"])

                # Only create some of the possible relationships to avoid too many edges
                if random.random() < 0.1:  # 10% chance of creating a relationship
                    edge_pair = (trend1["id"], trend2["id"])
                    if edge_pair not in existing_edge_pairs:
                        strength = round(random.uniform(0.3, 0.9), 2)

                        edge_data = {
                            "source": trend1["id"],
                            "target": trend2["id"],
                            "type": relationship_type,
                            "strength": strength
                        }

                        if relationship_type == "related_to":
                            edge_data["correlation"] = round(random.uniform(0.1, 0.9), 2)
                        elif relationship_type == "competes_with":
                            edge_data["market_overlap"] = round(random.uniform(0.1, 0.9), 2)
                        elif relationship_type == "enables":
                            edge_data["enablement_factor"] = round(random.uniform(0.1, 1.0), 2)

                        edges.append(edge_data)

    # Create edges between projects and trends
    for project in projects:
        # Each project is influenced by 1-3 trends
        for trend in random.sample(trends, min(random.randint(1, 3), len(trends))):
            edge_pair = (trend["id"], project["id"])
            if edge_pair not in existing_edge_pairs:
                edges.append({
                    "source": trend["id"],
                    "target": project["id"],
                    "type": "influences",
                    "strength": round(random.uniform(0.3, 0.9), 2),
                    "impact_score": round(random.uniform(0.1, 1.0), 2)
                })

    return nodes, edges

def populate_database():
    """Populate the database with generated data."""
    print("Generating additional companies...")
    companies = [generate_company_data() for _ in tqdm(range(NUM_ADDITIONAL_COMPANIES))]

    print("Generating additional trends...")
    trends = [generate_trend_data() for _ in tqdm(range(NUM_ADDITIONAL_TRENDS))]

    print("Generating additional projects...")
    # Get all company IDs (existing + new)
    existing_companies = list(db.collection("companies").get())
    existing_company_ids = [doc.id for doc in existing_companies]
    new_company_ids = [company["id"] for company in companies]
    all_company_ids = existing_company_ids + new_company_ids

    projects = [generate_project_data(all_company_ids) for _ in tqdm(range(NUM_ADDITIONAL_PROJECTS))]

    print("Generating additional funds...")
    funds = [generate_fund_data(all_company_ids) for _ in tqdm(range(NUM_ADDITIONAL_FUNDS))]

    print("Getting existing graph nodes and edges...")
    existing_nodes = [doc.to_dict() for doc in db.collection("graph_nodes").get()]
    existing_edges = [doc.to_dict() for doc in db.collection("graph_edges").get()]

    print("Generating additional graph relationships...")
    nodes, edges = generate_graph_relationships(companies, trends, projects, funds, existing_nodes, existing_edges)

    print("Saving data to Firebase...")

    # Save companies
    for company in tqdm(companies, desc="Saving companies"):
        db.collection("companies").document(company["id"]).set(company)

        # Add to vector store
        vector_store.add_item(
            item_id=company["id"],
            embedding=company["embedding"],
            metadata={
                "id": company["id"],
                "name": company["name"],
                "type": "company",
                "sector": company["sector"],
                "country": company["country"],
                "company_size": company["company_size"],
                "environmental_score": company["sustainability_metrics"]["environmental_score"],
                "social_score": company["sustainability_metrics"]["social_score"],
                "governance_score": company["sustainability_metrics"]["governance_score"],
                "esg_score": company["sustainability_metrics"]["esg_score"],
                "revenue": company["financial_metrics"]["revenue"],
                "innovation_score": company["innovation_metrics"]["innovation_score"]
            },
            text=f"{company['name']} - {company['description']} - {company['sector']}"
        )

    # Save trends
    for trend in tqdm(trends, desc="Saving trends"):
        db.collection("trends").document(trend["id"]).set(trend)

        # Add to vector store
        vector_store.add_item(
            item_id=trend["id"],
            embedding=trend["embedding"],
            metadata={
                "id": trend["id"],
                "name": trend["name"],
                "type": "trend",
                "category": trend["category"],
                "relevance_score": trend["relevance_score"],
                "growth_rate": trend["growth_rate"],
                "maturity_stage": trend["maturity_stage"],
                "sdg_alignment": trend["impact_metrics"]["sdg_alignment"]
            },
            text=f"{trend['name']} - {trend['description']} - {trend['category']}"
        )

    # Save projects
    for project in tqdm(projects, desc="Saving projects"):
        db.collection("projects").document(project["id"]).set(project)

        # Add to vector store
        vector_store.add_item(
            item_id=project["id"],
            embedding=project["embedding"],
            metadata={
                "id": project["id"],
                "name": project["name"],
                "type": "project",
                "project_type": project["type"],
                "company_id": project["company_id"],
                "status": project["status"],
                "budget": project["budget"],
                "progress": project["progress"],
                "carbon_impact": project["sustainability_metrics"]["carbon_impact"],
                "sdg_alignment": project["sustainability_metrics"]["sdg_alignment"],
                "roi": project["performance_metrics"]["roi"]
            },
            text=f"{project['name']} - {project['description']} - {project['type']}"
        )

    # Save funds
    for fund in tqdm(funds, desc="Saving funds"):
        db.collection("funds").document(fund["id"]).set(fund)

        # Add to vector store
        vector_store.add_item(
            item_id=fund["id"],
            embedding=fund["embedding"],
            metadata={
                "id": fund["id"],
                "name": fund["name"],
                "type": "fund",
                "fund_type": fund["type"],
                "country": fund["country"],
                "aum": fund["aum"],
                "return": fund["return"],
                "esg_score": fund["performance_metrics"]["esg_score"],
                "impact_score": fund["performance_metrics"]["impact_score"],
                "sustainability_focus": fund["sustainability_focus"]
            },
            text=f"{fund['name']} - {fund['description']} - {' '.join(fund['sustainability_focus'])}"
        )

    # Save graph nodes and edges
    for node in tqdm(nodes, desc="Saving graph nodes"):
        db.collection("graph_nodes").document(node["id"]).set(node)

    for i, edge in enumerate(tqdm(edges, desc="Saving graph edges")):
        edge_id = f"edge_{random.randint(100000, 999999)}"
        db.collection("graph_edges").document(edge_id).set(edge)

    print("Data population complete!")
    print(f"Created {len(companies)} companies, {len(trends)} trends, {len(projects)} projects, {len(funds)} funds")
    print(f"Created {len(nodes)} graph nodes and {len(edges)} graph edges")

if __name__ == "__main__":
    populate_database()
