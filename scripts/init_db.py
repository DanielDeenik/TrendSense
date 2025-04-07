"""
Database Initialization Script
Creates necessary collections and indexes in MongoDB.
"""

import os
import sys
import logging
from datetime import datetime
from typing import Dict, Any

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config.mongodb_config import MONGODB_CONFIG, COLLECTIONS, INDEXES
from backend.database.mongodb_manager import MongoDBManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def init_database() -> None:
    """Initialize the database with collections and indexes"""
    try:
        # Create MongoDB manager instance
        db_manager = MongoDBManager(
            uri=MONGODB_CONFIG['uri'],
            database_name=MONGODB_CONFIG['database']
        )
        
        logger.info("Connected to MongoDB")
        
        # Create collections
        for collection_name in COLLECTIONS.values():
            if collection_name not in db_manager.db.list_collection_names():
                db_manager.db.create_collection(collection_name)
                logger.info(f"Created collection: {collection_name}")
        
        # Create indexes
        for collection_name, indexes in INDEXES.items():
            collection = db_manager.db[COLLECTIONS[collection_name]]
            for index in indexes:
                try:
                    collection.create_index(**index)
                    logger.info(f"Created index in {collection_name}: {index}")
                except Exception as e:
                    logger.error(f"Error creating index in {collection_name}: {str(e)}")
        
        # Insert sample data if collections are empty
        if db_manager.portfolio_companies.count_documents({}) == 0:
            sample_companies = [
                {
                    'id': '1',
                    'name': 'Sample Company 1',
                    'legal_name': 'Sample Company 1 Ltd.',
                    'country': 'Netherlands',
                    'region': 'Europe',
                    'sector': 'Technology',
                    'subsector': 'Software',
                    'description': 'A sample company for testing',
                    'website': 'https://example.com',
                    'founded_date': datetime(2020, 1, 1),
                    'investment_date': datetime(2021, 1, 1),
                    'status': 'active',
                    'ownership_pct': 25.0,
                    'team': [],
                    'board_members': [],
                    'documents': []
                }
            ]
            db_manager.insert_portfolio_companies(sample_companies)
            logger.info("Inserted sample portfolio companies")
        
        if db_manager.sustainability_metrics.count_documents({}) == 0:
            sample_metrics = [
                {
                    'company_id': '1',
                    'reporting_period': datetime(2024, 1, 1),
                    'carbon_emissions': {
                        'scope1_emissions': 100.0,
                        'scope2_emissions': 200.0,
                        'scope3_emissions': 300.0,
                        'total_emissions': 600.0,
                        'emission_intensity': 0.5,
                        'reduction_target': 20.0,
                        'reduction_achieved': 10.0,
                        'carbon_offsets': 50.0,
                        'net_emissions': 550.0
                    },
                    'energy_metrics': {
                        'total_energy_consumption': 1000.0,
                        'renewable_energy_consumption': 400.0,
                        'energy_intensity': 0.8,
                        'efficiency_improvements': 15.0
                    },
                    'water_metrics': {
                        'water_withdrawal': 500.0,
                        'water_consumption': 400.0,
                        'water_intensity': 0.3,
                        'recycling_rate': 80.0,
                        'water_stressed_area': False
                    },
                    'waste_metrics': {
                        'total_waste': 200.0,
                        'hazardous_waste': 20.0,
                        'recycling_rate': 75.0,
                        'circular_economy_score': 85.0
                    },
                    'sdg_alignment': {
                        'sdgs': [7, 9, 13],
                        'primary_sdg': 13,
                        'contribution_score': 90.0,
                        'impact_metrics': {
                            'carbon_reduction': 100.0,
                            'renewable_energy': 40.0
                        }
                    },
                    'esg_score': 85.0,
                    'verification_status': 'verified',
                    'verification_date': datetime(2024, 1, 15),
                    'last_updated': datetime.now()
                }
            ]
            db_manager.insert_sustainability_metrics(sample_metrics)
            logger.info("Inserted sample sustainability metrics")
        
        logger.info("Database initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise
    finally:
        if 'db_manager' in locals():
            db_manager.close()

if __name__ == '__main__':
    init_database() 