"""
Mock Graph Data Generator for TrendSense

This module generates mock data for the graph analytics feature.
"""

import uuid
import random
import datetime
from typing import Dict, List, Any

# Constants for generating realistic data
COMPANY_NAMES = [
    "GreenTech Solutions", "EcoInnovate", "SustainableFuture", "CleanEnergy Systems",
    "CircularEconomy", "EthicalAI", "BiodiversityTech", "CarbonCapture Inc",
    "RenewableVentures", "OceanCleanup Technologies", "SmartGrid Solutions",
    "SustainableAgriculture", "WaterConservation Systems", "ZeroWaste Solutions"
]

SECTORS = [
    "CleanTech", "RenewableEnergy", "CircularEconomy", "SustainableAgriculture",
    "GreenBuilding", "WaterTech", "WasteManagement", "ClimateFintech",
    "SustainableMobility", "CarbonCapture", "BiodiversityTech", "EthicalAI"
]

TREND_NAMES = [
    "Carbon Neutrality", "Circular Business Models", "Regenerative Agriculture",
    "Green Hydrogen", "Sustainable Aviation", "Plant-based Alternatives",
    "Biodiversity Credits", "Climate Fintech", "ESG Data Analytics",
    "Sustainable Supply Chains", "Carbon Capture", "Renewable Energy Storage",
    "Water Conservation", "Zero Waste Manufacturing", "Ethical AI"
]

TREND_CATEGORIES = [
    "Environmental", "Social", "Governance", "Technology", "Policy", "Market"
]

PROJECT_TYPES = [
    "Product Development", "Research", "Infrastructure", "Software", "Service",
    "Policy Initiative", "Community Program", "Supply Chain Optimization"
]

INITIATIVE_CATEGORIES = [
    "Carbon Reduction", "Waste Reduction", "Water Conservation", "Renewable Energy",
    "Biodiversity", "Social Impact", "Governance", "Supply Chain", "Circular Economy"
]

METRIC_CATEGORIES = [
    "Carbon Emissions", "Energy Usage", "Water Usage", "Waste Generation",
    "Biodiversity Impact", "Social Impact", "Governance", "Supply Chain Sustainability"
]

METRIC_UNITS = {
    "Carbon Emissions": "tCO2e",
    "Energy Usage": "kWh",
    "Water Usage": "m³",
    "Waste Generation": "kg",
    "Biodiversity Impact": "score",
    "Social Impact": "score",
    "Governance": "score",
    "Supply Chain Sustainability": "score"
}

def generate_id() -> str:
    """Generate a unique ID."""
    return str(uuid.uuid4())

def generate_date(days_ago: int = 0) -> str:
    """Generate a date string."""
    date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
    return date.isoformat()

def generate_companies(count: int = 10) -> List[Dict[str, Any]]:
    """Generate mock company data."""
    companies = []
    for i in range(count):
        company_id = generate_id()
        sector = random.choice(SECTORS)

        # Generate sustainability metrics
        environmental_score = random.uniform(50, 95)
        social_score = random.uniform(50, 95)
        governance_score = random.uniform(50, 95)
        esg_score = (environmental_score + social_score + governance_score) / 3

        company = {
            "_id": company_id,
            "name": COMPANY_NAMES[i % len(COMPANY_NAMES)],
            "description": f"A leading company in {sector} focused on sustainability.",
            "sector": sector,
            "sub_sectors": random.sample(SECTORS, k=min(3, len(SECTORS))),
            "founded_year": random.randint(2000, 2022),
            "headquarters": "Global",
            "website": f"https://www.{COMPANY_NAMES[i % len(COMPANY_NAMES)].lower().replace(' ', '')}.com",
            "sustainability_metrics": {
                "environmental_score": environmental_score,
                "social_score": social_score,
                "governance_score": governance_score,
                "esg_score": esg_score,
                "carbon_emissions": {
                    "scope1": random.uniform(100, 1000),
                    "scope2": random.uniform(500, 5000),
                    "scope3": random.uniform(1000, 10000),
                    "total": random.uniform(2000, 15000)
                },
                "sustainable_revenue_percentage": random.uniform(10, 80),
                "renewable_energy_percentage": random.uniform(20, 90)
            },
            "created_at": generate_date(random.randint(30, 365)),
            "updated_at": generate_date(random.randint(0, 30))
        }
        companies.append(company)

    return companies

def generate_trends(count: int = 15) -> List[Dict[str, Any]]:
    """Generate mock trend data."""
    trends = []
    for i in range(count):
        trend_id = generate_id()
        category = random.choice(TREND_CATEGORIES)

        trend = {
            "_id": trend_id,
            "name": TREND_NAMES[i % len(TREND_NAMES)],
            "description": f"A significant trend in {category} sustainability.",
            "category": category,
            "relevance_score": random.uniform(0.5, 1.0),
            "growth_rate": random.uniform(0.1, 0.5),
            "maturity_stage": random.choice(["Emerging", "Growing", "Mature"]),
            "sectors": random.sample(SECTORS, k=min(4, len(SECTORS))),
            "created_at": generate_date(random.randint(30, 365)),
            "updated_at": generate_date(random.randint(0, 30))
        }
        trends.append(trend)

    return trends

def generate_projects(companies: List[Dict[str, Any]], count_per_company: int = 3) -> List[Dict[str, Any]]:
    """Generate mock project data for companies."""
    projects = []
    for company in companies:
        for _ in range(count_per_company):
            project_id = generate_id()
            project_type = random.choice(PROJECT_TYPES)

            # Generate sustainability metrics
            environmental_score = random.uniform(50, 95)
            social_score = random.uniform(50, 95)
            governance_score = random.uniform(50, 95)

            project = {
                "_id": project_id,
                "name": f"{project_type} Project",
                "description": f"A {project_type.lower()} project focused on sustainability.",
                "company_id": company["_id"],
                "type": project_type,
                "status": random.choice(["Planned", "In Progress", "Completed"]),
                "start_date": generate_date(random.randint(100, 500)),
                "end_date": generate_date(random.randint(0, 100)),
                "budget": random.uniform(100000, 5000000),
                "sustainability_metrics": {
                    "environmental_score": environmental_score,
                    "social_score": social_score,
                    "governance_score": governance_score,
                    "carbon_impact": -random.uniform(1000, 10000),  # Negative means reduction
                    "sdg_alignment": random.sample(range(1, 18), k=random.randint(1, 5))
                },
                "created_at": generate_date(random.randint(30, 365)),
                "updated_at": generate_date(random.randint(0, 30))
            }
            projects.append(project)

    return projects

def generate_graph_nodes(companies: List[Dict[str, Any]], trends: List[Dict[str, Any]], projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate graph nodes from entities."""
    nodes = []

    # Add company nodes
    for company in companies:
        nodes.append({
            "_id": company["_id"],
            "name": company["name"],
            "type": "company",
            "sector": company["sector"],
            "size": 30,
            "esg_score": company["sustainability_metrics"]["esg_score"],
            "color": "#3b82f6"  # Blue
        })

    # Add trend nodes
    for trend in trends:
        nodes.append({
            "_id": trend["_id"],
            "name": trend["name"],
            "type": "trend",
            "category": trend["category"],
            "size": 25,
            "relevance": trend["relevance_score"],
            "color": "#10b981"  # Green
        })

    # Add project nodes
    for project in projects:
        nodes.append({
            "_id": project["_id"],
            "name": project["name"],
            "type": "project",
            "project_type": project["type"],
            "size": 20,
            "status": project["status"],
            "color": "#f59e0b"  # Amber
        })

    return nodes

def generate_graph_edges(companies: List[Dict[str, Any]], trends: List[Dict[str, Any]], projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate graph edges between entities."""
    edges = []

    # Connect trends to companies (influences)
    for trend in trends:
        # Each trend influences 2-5 random companies
        for company in random.sample(companies, k=random.randint(2, min(5, len(companies)))):
            edges.append({
                "_id": generate_id(),
                "source": trend["_id"],
                "target": company["_id"],
                "type": "influences",
                "strength": random.uniform(0.3, 0.9)
            })

    # Connect companies to projects (owns)
    for project in projects:
        edges.append({
            "_id": generate_id(),
            "source": project["company_id"],
            "target": project["_id"],
            "type": "owns",
            "strength": 1.0
        })

    # Connect companies to companies (partnerships)
    for i in range(len(companies)):
        # Each company partners with 1-3 other companies
        for j in random.sample([k for k in range(len(companies)) if k != i], k=random.randint(1, min(3, len(companies) - 1))):
            edges.append({
                "_id": generate_id(),
                "source": companies[i]["_id"],
                "target": companies[j]["_id"],
                "type": "partners",
                "strength": random.uniform(0.4, 0.8)
            })

    return edges

def generate_all_mock_data() -> Dict[str, List[Dict[str, Any]]]:
    """Generate all mock data for graph analytics."""
    companies = generate_companies(10)
    trends = generate_trends(15)
    projects = generate_projects(companies, 3)

    nodes = generate_graph_nodes(companies, trends, projects)
    edges = generate_graph_edges(companies, trends, projects)

    return {
        "companies": companies,
        "trends": trends,
        "projects": projects,
        "graph_nodes": nodes,
        "graph_edges": edges
    }

if __name__ == "__main__":
    # Generate mock data
    mock_data = generate_all_mock_data()
    print(f"Generated {len(mock_data['companies'])} companies")
    print(f"Generated {len(mock_data['trends'])} trends")
    print(f"Generated {len(mock_data['projects'])} projects")
    print(f"Generated {len(mock_data['graph_nodes'])} graph nodes")
    print(f"Generated {len(mock_data['graph_edges'])} graph edges")
