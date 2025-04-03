#!/usr/bin/env python
"""
Test MongoDB Connection

This script tests MongoDB connection by using the Python MongoDB client.
It attempts to connect to MongoDB and perform a simple operation.

Usage:
    python test_mongodb_connection.py
"""

import os
import sys
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mongodb_test")

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

def test_connection():
    """
    Test connection to MongoDB
    """
    logger.info("Testing MongoDB connection...")
    
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
        
        # Create test collection if it doesn't exist
        if "test_collection" not in collections:
            logger.info("Creating test collection...")
            test_collection = db.test_collection
            
            # Insert test document
            test_doc = {
                "name": "Test Document",
                "created_at": datetime.now(),
                "test_data": {
                    "value": 123,
                    "status": "testing"
                }
            }
            
            result = test_collection.insert_one(test_doc)
            logger.info(f"Test document inserted with ID: {result.inserted_id}")
            
            # Retrieve the document to verify
            retrieved_doc = test_collection.find_one({"_id": result.inserted_id})
            if retrieved_doc:
                logger.info("Test document retrieved successfully")
                
                # Convert ObjectId to string for JSON serialization
                retrieved_doc["_id"] = str(retrieved_doc["_id"])
                # Convert datetime to string
                retrieved_doc["created_at"] = retrieved_doc["created_at"].isoformat()
                
                # Pretty print the document
                logger.info(f"Document content:\n{json.dumps(retrieved_doc, indent=2)}")
            else:
                logger.error("Failed to retrieve test document")
        else:
            logger.info("Test collection already exists")
            
            # Get first document from test collection
            test_doc = db.test_collection.find_one()
            if test_doc:
                # Convert ObjectId to string for JSON serialization
                test_doc["_id"] = str(test_doc["_id"])
                # Convert datetime to string if it exists
                if "created_at" in test_doc and isinstance(test_doc["created_at"], datetime):
                    test_doc["created_at"] = test_doc["created_at"].isoformat()
                
                # Pretty print the document
                logger.info(f"Existing document content:\n{json.dumps(test_doc, indent=2)}")
            else:
                logger.info("Test collection is empty")
        
        # Close connection
        client.close()
        logger.info("MongoDB connection closed")
        
        return True
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f"❌ MongoDB connection failed: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"❌ Error testing MongoDB connection: {str(e)}")
        return False

if __name__ == "__main__":
    if test_connection():
        logger.info("MongoDB connection test completed successfully!")
        sys.exit(0)
    else:
        logger.error("MongoDB connection test failed!")
        sys.exit(1)