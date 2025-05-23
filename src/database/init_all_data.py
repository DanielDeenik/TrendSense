"""
Initialize All Data

This script initializes the database with all necessary data for the application.
"""

import os
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import database adapter
from src.database.adapters import get_database_adapter

# Import data initialization modules
try:
    from src.database.init_lookthrough_data import init_lookthrough_data
except ImportError:
    logger.warning("Could not import init_lookthrough_data")
    init_lookthrough_data = None

def init_all_data():
    """Initialize all data for the application."""
    try:
        # Get database adapter
        db_adapter = get_database_adapter()
        
        # Connect to the database
        if not db_adapter.is_connected():
            db_adapter.connect()
        
        # Initialize collections
        collections = [
            'users',
            'trends',
            'companies',
            'funds',
            'projects',
            'products',
            'resources',
            'metrics',
            'insights',
            'stories',
            'pages'
        ]
        
        db_adapter.initialize_collections(collections)
        
        # Initialize Look Through Engine data
        if init_lookthrough_data:
            logger.info("Initializing Look Through Engine data...")
            init_lookthrough_data()
        else:
            logger.warning("Skipping Look Through Engine data initialization")
        
        logger.info("All data initialized successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error initializing data: {str(e)}")
        return False

if __name__ == "__main__":
    init_all_data()
