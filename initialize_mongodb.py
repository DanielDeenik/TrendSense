#!/usr/bin/env python
"""
MongoDB Initialization Utility for SustainaTrend™ Platform

This script verifies MongoDB connection, sets up collections and indexes,
and provides utility commands for the SustainaTrend™ platform.

Usage:
    python initialize_mongodb.py --verify
    python initialize_mongodb.py --setup
    python initialize_mongodb.py --test-data
"""

import os
import sys
import logging
import argparse
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

try:
    from pymongo import MongoClient, ASCENDING, TEXT
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
except ImportError:
    print("ERROR: pymongo package is not installed. Please install it with:")
    print("  pip install pymongo")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mongodb_init")

# Default connection settings
DEFAULT_MONGO_URI = "mongodb://localhost:27017/"
DEFAULT_DB_NAME = "trendsense_vc"

# Get MongoDB URI from environment (prefer MONGODB_URI for Atlas connections)
if "MONGODB_URI" in os.environ:
    MONGO_URI = os.environ.get("MONGODB_URI")
    logger.info("Using MongoDB Atlas connection from MONGODB_URI")
else:
    MONGO_URI = os.environ.get("MONGO_URI", DEFAULT_MONGO_URI)
    logger.info(f"Using standard MongoDB connection: {MONGO_URI}")

DB_NAME = os.environ.get("MONGO_DB_NAME", DEFAULT_DB_NAME)
logger.info(f"Using database name: {DB_NAME}")

# Collection names
COLLECTIONS = {
    "documents": {
        "indexes": [
            [("title", TEXT), ("content", TEXT), ("tags", TEXT)],
            [("company_id", ASCENDING)],
            [("fund_id", ASCENDING)],
            [("created_at", ASCENDING)]
        ]
    },
    "patterns": {
        "indexes": [
            [("name", TEXT), ("description", TEXT)],
            [("sector", ASCENDING)],
            [("confidence", ASCENDING)],
            [("created_at", ASCENDING)]
        ]
    },
    "stories": {
        "indexes": [
            [("title", TEXT), ("content", TEXT)],
            [("company_id", ASCENDING)],
            [("views", ASCENDING)],
            [("created_at", ASCENDING)]
        ]
    },
    "theses": {
        "indexes": [
            [("name", TEXT), ("content", TEXT)],
            [("fund_id", ASCENDING)],
            [("sector", ASCENDING)],
            [("created_at", ASCENDING)]
        ]
    }
}

def verify_mongodb_connection():
    """
    Verify MongoDB connection is working
    """
    logger.info("Verifying MongoDB connection...")
    
    try:
        # Try connecting to MongoDB
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        # Verify connection is working with ping
        client.admin.command('ping')
        
        logger.info("✅ MongoDB connection successful!")
        
        # Get database
        db = client[DB_NAME]
        
        # Get collection list
        collections = db.list_collection_names()
        logger.info(f"Collections: {', '.join(collections) if collections else 'No collections'}")
        
        # Close connection
        client.close()
        logger.info("MongoDB connection closed")
        
        return True
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f"❌ MongoDB connection failed: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"❌ Error verifying MongoDB connection: {str(e)}")
        return False

def setup_collections_and_indexes():
    """
    Set up collections and indexes for the SustainaTrend™ platform
    """
    logger.info("Setting up collections and indexes...")
    
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        
        # Create collections and indexes
        for collection_name, config in COLLECTIONS.items():
            logger.info(f"Setting up collection: {collection_name}")
            
            # Create collection if it doesn't exist
            if collection_name not in db.list_collection_names():
                db.create_collection(collection_name)
                logger.info(f"Created collection: {collection_name}")
            
            # Create indexes
            collection = db[collection_name]
            for index_spec in config["indexes"]:
                index_name = "_".join([f"{field[0]}_{field[1]}" for field in index_spec])
                collection.create_index(index_spec, name=index_name)
                logger.info(f"Created index: {index_name} on {collection_name}")
        
        logger.info("✅ Collections and indexes setup complete!")
        
        # Close connection
        client.close()
        logger.info("MongoDB connection closed")
        
        return True
    except Exception as e:
        logger.error(f"❌ Error setting up collections and indexes: {str(e)}")
        return False

def create_test_data():
    """
    Create test data for the SustainaTrend™ platform
    """
    logger.info("Creating test data...")
    
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        
        # Sample data for each collection
        test_data = {
            "documents": [
                {
                    "title": "2023 Sustainability Report",
                    "content": "This report outlines our company's commitment to sustainability...",
                    "company_id": 1,
                    "fund_id": 1,
                    "tags": ["sustainability", "ESG", "annual-report"],
                    "created_at": datetime.now(),
                    "metadata": {
                        "author": "Sustainability Team",
                        "pages": 42,
                        "format": "PDF"
                    }
                },
                {
                    "title": "Carbon Reduction Strategy",
                    "content": "Our strategy for reducing carbon emissions across operations...",
                    "company_id": 2,
                    "fund_id": 1,
                    "tags": ["carbon", "emissions", "strategy"],
                    "created_at": datetime.now(),
                    "metadata": {
                        "author": "Climate Action Team",
                        "pages": 28,
                        "format": "PDF"
                    }
                }
            ],
            "patterns": [
                {
                    "name": "Early Sustainability Adoption",
                    "description": "Companies that implement sustainability initiatives early show better long-term profitability",
                    "sector": "Technology",
                    "confidence": 0.87,
                    "supporting_data": {
                        "company_count": 12,
                        "avg_roi": 18.5,
                        "timeframe": "3 years"
                    },
                    "created_at": datetime.now()
                },
                {
                    "name": "Carbon Trading Advantage",
                    "description": "Companies participating in carbon markets outperform sector peers",
                    "sector": "Energy",
                    "confidence": 0.79,
                    "supporting_data": {
                        "company_count": 8,
                        "avg_roi": 12.3,
                        "timeframe": "2 years"
                    },
                    "created_at": datetime.now()
                }
            ],
            "stories": [
                {
                    "title": "From Carbon Intensive to Climate Positive",
                    "content": "The journey of transforming a manufacturing company's operations...",
                    "company_id": 3,
                    "metrics": {
                        "carbon_reduced": 12500,
                        "water_saved": 1800000,
                        "renewable_energy": 78
                    },
                    "views": 156,
                    "created_at": datetime.now()
                },
                {
                    "title": "Creating a Circular Supply Chain",
                    "content": "How implementing circular economy principles transformed logistics...",
                    "company_id": 4,
                    "metrics": {
                        "waste_reduced": 85,
                        "materials_recycled": 92,
                        "cost_savings": 1200000
                    },
                    "views": 98,
                    "created_at": datetime.now()
                }
            ],
            "theses": [
                {
                    "name": "Climate Tech 2.0",
                    "content": "Investment thesis focused on next-generation climate technologies...",
                    "fund_id": 2,
                    "sector": "CleanTech",
                    "key_criteria": [
                        "Carbon impact measurement",
                        "Scalable technology",
                        "Unit economics viability"
                    ],
                    "created_at": datetime.now()
                },
                {
                    "name": "Sustainable Food Systems",
                    "content": "Investment approach for transforming food production and distribution...",
                    "fund_id": 3,
                    "sector": "AgriTech",
                    "key_criteria": [
                        "Water usage efficiency",
                        "Land use reduction",
                        "Carbon footprint"
                    ],
                    "created_at": datetime.now()
                }
            ]
        }
        
        # Insert test data into collections
        for collection_name, documents in test_data.items():
            collection = db[collection_name]
            
            # Check if collection already has data
            if collection.count_documents({}) > 0:
                logger.info(f"Collection {collection_name} already has data. Skipping...")
                continue
            
            # Insert documents
            result = collection.insert_many(documents)
            logger.info(f"Inserted {len(result.inserted_ids)} documents into {collection_name}")
        
        logger.info("✅ Test data creation complete!")
        
        # Close connection
        client.close()
        logger.info("MongoDB connection closed")
        
        return True
    except Exception as e:
        logger.error(f"❌ Error creating test data: {str(e)}")
        return False

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="MongoDB Initialization Utility")
    parser.add_argument("--verify", action="store_true", help="Verify MongoDB connection")
    parser.add_argument("--setup", action="store_true", help="Set up collections and indexes")
    parser.add_argument("--test-data", action="store_true", help="Create test data")
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if not (args.verify or args.setup or args.test_data):
        parser.print_help()
        return
    
    # Verify MongoDB connection
    if args.verify:
        if not verify_mongodb_connection():
            sys.exit(1)
    
    # Set up collections and indexes
    if args.setup:
        if not setup_collections_and_indexes():
            sys.exit(1)
    
    # Create test data
    if args.test_data:
        if not create_test_data():
            sys.exit(1)

if __name__ == "__main__":
    main()