"""
Firebase Connection Verification Script

This script verifies the connection to Firebase and checks if data is properly stored.
It also provides information about the collections and documents in the database.
"""

import os
import sys
import logging
import json
from datetime import datetime
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def verify_firebase_connection():
    """Verify connection to Firebase."""
    try:
        # Import the database adapter
        from src.database.adapters import get_database_adapter
        logger.info("Successfully imported get_database_adapter")

        # Get the database adapter
        adapter = get_database_adapter()
        logger.info(f"Created database adapter instance: {type(adapter).__name__}")

        # Check if we're using a mock adapter
        if hasattr(adapter, '_using_mock') and adapter._using_mock:
            logger.warning("Using mock Firebase adapter - not connected to real Firebase!")
            return False

        # Connect to Firebase
        connection_result = adapter.connect()
        logger.info(f"Connection result: {connection_result}")

        if connection_result:
            logger.info("Successfully connected to Firebase!")
            return True
        else:
            logger.error("Failed to connect to Firebase")
            return False
    except Exception as e:
        logger.error(f"Error verifying Firebase connection: {str(e)}")
        return False

def check_firebase_collections():
    """Check Firebase collections and their contents."""
    try:
        # Import the database adapter
        from src.database.adapters import get_database_adapter

        # Get the database adapter
        adapter = get_database_adapter()

        # Connect to Firebase if not already connected
        if not adapter.is_connected():
            adapter.connect()

        # List of collections to check
        collections_to_check = [
            'companies',
            'funds',
            'trends',
            'stories',
            'insights',
            'metrics',
            'chart_data',
            'vc_lens_data',
            'trend_radar_data',
            'test_collection'  # Add any other collections you want to check
        ]

        # Check each collection
        for collection_name in collections_to_check:
            try:
                # Get collection
                collection = adapter.get_collection(collection_name)

                # Count documents
                count = adapter.count_documents(collection_name, {})
                logger.info(f"Collection '{collection_name}' has {count} documents")

                # Get sample document if collection has documents
                if count > 0:
                    sample = adapter.find_one(collection_name, {})
                    if sample:
                        # Convert ObjectId to string for display
                        if '_id' in sample and not isinstance(sample['_id'], str):
                            sample['_id'] = str(sample['_id'])

                        logger.info(f"Sample document from '{collection_name}':")
                        logger.info(json.dumps(sample, indent=2, default=str))
            except Exception as e:
                logger.warning(f"Error checking collection '{collection_name}': {str(e)}")

        return True
    except Exception as e:
        logger.error(f"Error checking Firebase collections: {str(e)}")
        return False

def test_firebase_operations():
    """Test basic Firebase operations (create, read, update, delete)."""
    try:
        # Import the database adapter
        from src.database.adapters import get_database_adapter

        # Get the database adapter
        adapter = get_database_adapter()

        # Connect to Firebase if not already connected
        if not adapter.is_connected():
            adapter.connect()

        # Test collection name
        test_collection = 'test_collection'

        # Create a test document
        test_doc = {
            'name': 'Test Document',
            'description': 'This is a test document created by verify_firebase_connection.py',
            'timestamp': datetime.now().isoformat()
        }

        logger.info(f"Creating test document in '{test_collection}'...")
        doc_id = adapter.insert_one(test_collection, test_doc)

        if not doc_id:
            logger.error("Failed to create test document")
            return False

        logger.info(f"Created test document with ID: {doc_id}")

        # Read the document
        logger.info(f"Reading test document with ID: {doc_id}...")
        read_doc = adapter.find_one(test_collection, {'_id': doc_id})

        if not read_doc:
            logger.error(f"Failed to read test document with ID: {doc_id}")
            return False

        logger.info(f"Successfully read test document: {json.dumps(read_doc, default=str)}")

        # Update the document
        update_data = {'updated': True, 'update_timestamp': datetime.now().isoformat()}
        logger.info(f"Updating test document with ID: {doc_id}...")
        update_result = adapter.update_one(test_collection, {'_id': doc_id}, {'$set': update_data})

        if not update_result:
            logger.error(f"Failed to update test document with ID: {doc_id}")
            return False

        logger.info(f"Successfully updated test document")

        # Read the updated document
        updated_doc = adapter.find_one(test_collection, {'_id': doc_id})
        logger.info(f"Updated document: {json.dumps(updated_doc, default=str)}")

        # Delete the document
        logger.info(f"Deleting test document with ID: {doc_id}...")
        delete_result = adapter.delete_one(test_collection, {'_id': doc_id})

        if not delete_result:
            logger.error(f"Failed to delete test document with ID: {doc_id}")
            return False

        logger.info(f"Successfully deleted test document")

        return True
    except Exception as e:
        logger.error(f"Error testing Firebase operations: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Starting Firebase verification...")

    # Check Firebase credentials
    credentials_path = os.getenv('FIREBASE_CREDENTIALS_PATH')
    project_id = os.getenv('FIREBASE_PROJECT_ID')

    logger.info(f"Firebase credentials path: {credentials_path}")
    logger.info(f"Firebase project ID: {project_id}")

    if not os.path.exists(credentials_path):
        logger.error(f"Firebase credentials file not found: {credentials_path}")
        sys.exit(1)

    # Verify Firebase connection
    if not verify_firebase_connection():
        logger.error("Firebase connection verification failed")
        sys.exit(1)

    # Check Firebase collections
    logger.info("\nChecking Firebase collections...")
    check_firebase_collections()

    # Test Firebase operations
    logger.info("\nTesting Firebase operations...")
    if test_firebase_operations():
        logger.info("Firebase operations test passed")
    else:
        logger.error("Firebase operations test failed")

    logger.info("\nFirebase verification completed")
