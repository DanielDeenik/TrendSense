"""
Initialize Look Through Engine Data

This script initializes the database with sample data for the Look Through Engine.
"""

import os
import logging
import json
import random
from datetime import datetime, timedelta
import uuid

# Import database adapter
from src.database.adapters import get_database_adapter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get database adapter
db_adapter = get_database_adapter()

def init_lookthrough_data():
    """Initialize the database with sample data for the Look Through Engine."""
    try:
        # Connect to the database
        if not db_adapter.is_connected():
            db_adapter.connect()
        
        # Initialize collections
        db_adapter.initialize_collections(['funds', 'companies', 'projects'])
        
        # Check if data already exists
        funds = db_adapter.find('funds')
        if len(funds) > 0:
            logger.info("Look Through Engine data already exists")
            return True
        
        # Create sample data
        create_sample_funds()
        create_sample_companies()
        create_sample_projects()
        
        # Link entities
        link_entities()
        
        # Propagate metrics
        propagate_metrics()
        
        logger.info("Look Through Engine data initialized successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error initializing Look Through Engine data: {str(e)}")
        return False

def create_sample_funds():
    """Create sample funds."""
    logger.info("Creating sample funds...")
    
    funds = [
        {
            "_id": str(uuid.uuid4()),
            "name": "Sustainable Growth Fund",
            "description": "A fund focused on sustainable growth investments",
            "aum": 500000000,
            "currency": "USD",
            "manager": "Green Capital Partners",
            "inception_date": "2018-01-01",
            "portfolio_companies": [],
            "sustainability_metrics": {
                "esg_score": 85,
                "environmental_score": 90,
                "social_score": 80,
                "governance_score": 85,
                "carbon_footprint": 1200,
                "carbon_intensity": 24,
                "renewable_energy_percentage": 75,
                "net_zero_target": "2030"
            },
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        },
        {
            "_id": str(uuid.uuid4()),
            "name": "Tech Innovation Fund",
            "description": "A fund focused on innovative technology investments",
            "aum": 750000000,
            "currency": "USD",
            "manager": "Future Ventures",
            "inception_date": "2019-03-15",
            "portfolio_companies": [],
            "sustainability_metrics": {
                "esg_score": 70,
                "environmental_score": 65,
                "social_score": 75,
                "governance_score": 70,
                "carbon_footprint": 2500,
                "carbon_intensity": 33,
                "renewable_energy_percentage": 50,
                "net_zero_target": "2035"
            },
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        },
        {
            "_id": str(uuid.uuid4()),
            "name": "Climate Action Fund",
            "description": "A fund focused on climate action investments",
            "aum": 300000000,
            "currency": "USD",
            "manager": "Climate Capital",
            "inception_date": "2020-06-30",
            "portfolio_companies": [],
            "sustainability_metrics": {
                "esg_score": 95,
                "environmental_score": 98,
                "social_score": 90,
                "governance_score": 92,
                "carbon_footprint": 500,
                "carbon_intensity": 16,
                "renewable_energy_percentage": 95,
                "net_zero_target": "2025"
            },
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    ]
    
    # Insert funds
    for fund in funds:
        db_adapter.insert_one('funds', fund)
    
    logger.info(f"Created {len(funds)} sample funds")

def create_sample_companies():
    """Create sample companies."""
    logger.info("Creating sample companies...")
    
    sectors = ["Technology", "Energy", "Healthcare", "Finance", "Consumer Goods"]
    stages = ["Seed", "Series A", "Series B", "Series C", "Growth"]
    maturity_levels = ["Emerging", "Scaling", "Mature"]
    
    companies = []
    
    for i in range(15):
        sector = random.choice(sectors)
        stage = random.choice(stages)
        maturity = random.choice(maturity_levels)
        
        # Adjust ESG scores based on sector and maturity
        base_esg = random.randint(50, 90)
        if sector == "Energy":
            env_score = base_esg - 10
        elif sector == "Technology":
            env_score = base_esg + 5
        else:
            env_score = base_esg
        
        if maturity == "Mature":
            gov_score = base_esg + 10
        elif maturity == "Emerging":
            gov_score = base_esg - 10
        else:
            gov_score = base_esg
        
        social_score = base_esg + random.randint(-5, 5)
        
        # Ensure scores are within bounds
        env_score = max(0, min(100, env_score))
        social_score = max(0, min(100, social_score))
        gov_score = max(0, min(100, gov_score))
        
        # Calculate overall ESG score
        esg_score = (env_score + social_score + gov_score) / 3
        
        company = {
            "_id": str(uuid.uuid4()),
            "name": f"Company {i+1}",
            "description": f"A {sector.lower()} company in the {stage.lower()} stage",
            "sector": sector,
            "sub_sectors": [f"{sector} Subsector {j+1}" for j in range(random.randint(1, 3))],
            "stage": stage,
            "sustainability_maturity": maturity,
            "founding_year": random.randint(2000, 2020),
            "headquarters": random.choice(["New York", "San Francisco", "London", "Berlin", "Tokyo"]),
            "website": f"https://company{i+1}.com",
            "funding_rounds": [],
            "investors": [],
            "projects": [],
            "sustainability_metrics": {
                "esg_score": esg_score,
                "environmental_score": env_score,
                "social_score": social_score,
                "governance_score": gov_score,
                "carbon_emissions": {
                    "scope1": random.randint(100, 1000),
                    "scope2": random.randint(500, 2000),
                    "scope3": random.randint(1000, 5000)
                },
                "renewable_energy_percentage": random.randint(10, 90),
                "water_usage": random.randint(1000, 10000),
                "waste_generated": random.randint(100, 1000)
            },
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        companies.append(company)
    
    # Insert companies
    for company in companies:
        db_adapter.insert_one('companies', company)
    
    logger.info(f"Created {len(companies)} sample companies")

def create_sample_projects():
    """Create sample projects."""
    logger.info("Creating sample projects...")
    
    project_types = ["Product Development", "Infrastructure", "Research", "Marketing", "Expansion"]
    statuses = ["Planned", "In Progress", "Completed"]
    
    projects = []
    
    # Get all companies
    companies = db_adapter.find('companies')
    
    for company in companies:
        # Create 2-5 projects per company
        for i in range(random.randint(2, 5)):
            project_type = random.choice(project_types)
            status = random.choice(statuses)
            
            # Generate random dates
            start_date = datetime.now() - timedelta(days=random.randint(30, 365))
            if status == "Completed":
                end_date = start_date + timedelta(days=random.randint(30, 180))
            elif status == "In Progress":
                end_date = start_date + timedelta(days=random.randint(180, 365))
            else:
                start_date = datetime.now() + timedelta(days=random.randint(30, 90))
                end_date = start_date + timedelta(days=random.randint(90, 365))
            
            # Adjust sustainability metrics based on project type and company sector
            base_env_score = random.randint(50, 90)
            if project_type == "Infrastructure" and company["sector"] == "Energy":
                env_score = base_env_score - 20
            elif project_type == "Research" and company["sector"] == "Technology":
                env_score = base_env_score + 10
            else:
                env_score = base_env_score
            
            social_score = random.randint(50, 90)
            gov_score = random.randint(50, 90)
            
            # Ensure scores are within bounds
            env_score = max(0, min(100, env_score))
            social_score = max(0, min(100, social_score))
            gov_score = max(0, min(100, gov_score))
            
            project = {
                "_id": str(uuid.uuid4()),
                "name": f"{company['name']} {project_type} Project {i+1}",
                "description": f"A {project_type.lower()} project for {company['name']}",
                "company_id": company["_id"],
                "company_name": company["name"],
                "type": project_type,
                "status": status,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "budget": random.randint(100000, 1000000),
                "currency": "USD",
                "initiatives": [],
                "sustainability_metrics": {
                    "carbon_impact": random.randint(-1000, 500),
                    "environmental_score": env_score,
                    "social_score": social_score,
                    "governance_score": gov_score,
                    "innovation_score": random.randint(50, 90),
                    "resilience_score": random.randint(50, 90),
                    "water_usage": random.randint(100, 1000),
                    "waste_generated": random.randint(10, 100),
                    "impact": {
                        "sdg_alignment": f"SDG {random.randint(1, 17)}",
                        "category": random.choice(["Climate Action", "Clean Energy", "Sustainable Cities", "Responsible Consumption"]),
                        "beneficiaries": random.randint(1000, 100000),
                        "score": random.randint(50, 90)
                    }
                },
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            projects.append(project)
    
    # Insert projects
    for project in projects:
        db_adapter.insert_one('projects', project)
    
    logger.info(f"Created {len(projects)} sample projects")

def link_entities():
    """Link entities together."""
    logger.info("Linking entities...")
    
    # Get all funds, companies, and projects
    funds = db_adapter.find('funds')
    companies = db_adapter.find('companies')
    projects = db_adapter.find('projects')
    
    # Link companies to funds
    for company in companies:
        # Randomly assign 1-2 funds to each company
        num_funds = random.randint(1, min(2, len(funds)))
        selected_funds = random.sample(funds, num_funds)
        
        for fund in selected_funds:
            # Add company to fund's portfolio_companies
            if company["_id"] not in fund["portfolio_companies"]:
                fund["portfolio_companies"].append(company["_id"])
                db_adapter.update_one('funds', {"_id": fund["_id"]}, {"$set": {"portfolio_companies": fund["portfolio_companies"]}})
            
            # Add fund to company's investors
            if fund["_id"] not in company["investors"]:
                company["investors"].append(fund["_id"])
                db_adapter.update_one('companies', {"_id": company["_id"]}, {"$set": {"investors": company["investors"]}})
    
    # Link projects to companies
    for project in projects:
        company_id = project["company_id"]
        
        # Find the company
        company = next((c for c in companies if c["_id"] == company_id), None)
        
        if company:
            # Add project to company's projects
            if project["_id"] not in company["projects"]:
                company["projects"].append(project["_id"])
                db_adapter.update_one('companies', {"_id": company["_id"]}, {"$set": {"projects": company["projects"]}})
    
    logger.info("Entities linked successfully")

def propagate_metrics():
    """Propagate metrics through the Fund → Company → Project structure."""
    logger.info("Propagating metrics...")
    
    # Get all funds, companies, and projects
    funds = db_adapter.find('funds')
    companies = db_adapter.find('companies')
    projects = db_adapter.find('projects')
    
    # Process each fund
    for fund in funds:
        fund_id = fund["_id"]
        fund_name = fund["name"]
        portfolio_companies = fund["portfolio_companies"]
        
        logger.info(f"Processing fund: {fund_name} ({fund_id})")
        
        # Get companies
        fund_companies = [c for c in companies if c["_id"] in portfolio_companies]
        
        if not fund_companies:
            logger.warning(f"No companies found for fund: {fund_name}")
            continue
        
        # Process each company
        company_metrics = []
        for company in fund_companies:
            company_id = company["_id"]
            company_name = company["name"]
            company_projects = company["projects"]
            
            logger.info(f"Processing company: {company_name} ({company_id})")
            
            # Get projects
            company_project_list = [p for p in projects if p["_id"] in company_projects]
            
            if not company_project_list:
                logger.warning(f"No projects found for company: {company_name}")
                continue
            
            # Aggregate project metrics
            env_scores = []
            social_scores = []
            gov_scores = []
            carbon_impacts = []
            
            for project in company_project_list:
                metrics = project.get("sustainability_metrics", {})
                
                if "environmental_score" in metrics:
                    env_scores.append(metrics["environmental_score"])
                
                if "social_score" in metrics:
                    social_scores.append(metrics["social_score"])
                
                if "governance_score" in metrics:
                    gov_scores.append(metrics["governance_score"])
                
                if "carbon_impact" in metrics:
                    carbon_impacts.append(metrics["carbon_impact"])
            
            # Calculate average scores
            avg_env_score = sum(env_scores) / len(env_scores) if env_scores else 0
            avg_social_score = sum(social_scores) / len(social_scores) if social_scores else 0
            avg_gov_score = sum(gov_scores) / len(gov_scores) if gov_scores else 0
            total_carbon_impact = sum(carbon_impacts) if carbon_impacts else 0
            
            # Calculate overall ESG score
            esg_score = (avg_env_score + avg_social_score + avg_gov_score) / 3
            
            # Update company metrics
            company_metrics.append({
                "company_id": company_id,
                "environmental_score": avg_env_score,
                "social_score": avg_social_score,
                "governance_score": avg_gov_score,
                "esg_score": esg_score,
                "carbon_impact": total_carbon_impact
            })
            
            # Update company in database
            db_adapter.update_one(
                'companies',
                {"_id": company_id},
                {"$set": {
                    "sustainability_metrics.environmental_score": avg_env_score,
                    "sustainability_metrics.social_score": avg_social_score,
                    "sustainability_metrics.governance_score": avg_gov_score,
                    "sustainability_metrics.esg_score": esg_score,
                    "sustainability_metrics.carbon_impact": total_carbon_impact,
                    "updated_at": datetime.now().isoformat()
                }}
            )
        
        # Aggregate company metrics
        env_scores = [m["environmental_score"] for m in company_metrics]
        social_scores = [m["social_score"] for m in company_metrics]
        gov_scores = [m["governance_score"] for m in company_metrics]
        esg_scores = [m["esg_score"] for m in company_metrics]
        carbon_impacts = [m["carbon_impact"] for m in company_metrics]
        
        # Calculate average scores
        avg_env_score = sum(env_scores) / len(env_scores) if env_scores else 0
        avg_social_score = sum(social_scores) / len(social_scores) if social_scores else 0
        avg_gov_score = sum(gov_scores) / len(gov_scores) if gov_scores else 0
        avg_esg_score = sum(esg_scores) / len(esg_scores) if esg_scores else 0
        total_carbon_impact = sum(carbon_impacts) if carbon_impacts else 0
        
        # Update fund metrics
        db_adapter.update_one(
            'funds',
            {"_id": fund_id},
            {"$set": {
                "sustainability_metrics.environmental_score": avg_env_score,
                "sustainability_metrics.social_score": avg_social_score,
                "sustainability_metrics.governance_score": avg_gov_score,
                "sustainability_metrics.esg_score": avg_esg_score,
                "sustainability_metrics.carbon_impact": total_carbon_impact,
                "updated_at": datetime.now().isoformat()
            }}
        )
    
    logger.info("Metrics propagated successfully")

if __name__ == "__main__":
    init_lookthrough_data()
