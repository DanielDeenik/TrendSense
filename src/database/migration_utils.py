"""
Database Migration Utilities

This module provides utilities for migrating data between different database backends.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from .adapters import MongoDBAdapter, FirebaseAdapter

# Configure logging
logger = logging.getLogger(__name__)


def export_mongodb_to_json(collections: List[str] = None, output_dir: str = 'data_export') -> bool:
    """
    Export MongoDB collections to JSON files.

    Args:
        collections: List of collection names to export (None for all)
        output_dir: Directory to save JSON files

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create MongoDB adapter
        mongodb = MongoDBAdapter()
        if not mongodb.connect():
            logger.error("Failed to connect to MongoDB")
            return False

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Get all collections if not specified
        if collections is None:
            # This is a simplified approach - in a real application, you would
            # get the list of collections from MongoDB
            collections = [
                'users',
                'trends',
                'companies',
                'products',
                'resources',
                'metrics',
                'insights',
                'stories',
                'pages'
            ]

        # Export each collection
        for collection_name in collections:
            # Get documents from collection
            documents = mongodb.find(collection_name)
            if not documents:
                logger.warning(f"No documents found in collection: {collection_name}")
                continue

            # Convert ObjectId to string for JSON serialization
            for doc in documents:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])

            # Save to JSON file
            output_file = os.path.join(output_dir, f"{collection_name}.json")
            with open(output_file, 'w') as f:
                json.dump(documents, f, default=str, indent=2)

            logger.info(f"Exported {len(documents)} documents from {collection_name} to {output_file}")

        mongodb.disconnect()
        return True
    except Exception as e:
        logger.error(f"Error exporting MongoDB to JSON: {str(e)}")
        return False


def import_json_to_firebase(input_dir: str = 'data_export') -> bool:
    """
    Import JSON files to Firebase.

    Args:
        input_dir: Directory containing JSON files

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create Firebase adapter
        firebase = FirebaseAdapter()
        if not firebase.connect():
            logger.error("Failed to connect to Firebase")
            return False

        # Get list of JSON files
        json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
        if not json_files:
            logger.error(f"No JSON files found in {input_dir}")
            return False

        # Import each file
        for json_file in json_files:
            # Get collection name from filename
            collection_name = os.path.splitext(json_file)[0]

            # Load documents from JSON file
            input_file = os.path.join(input_dir, json_file)
            with open(input_file, 'r') as f:
                documents = json.load(f)

            if not documents:
                logger.warning(f"No documents found in {input_file}")
                continue

            # Insert documents into Firebase
            doc_ids = firebase.insert_many(collection_name, documents)
            logger.info(f"Imported {len(doc_ids)} documents to {collection_name} in Firebase")

        firebase.disconnect()
        return True
    except Exception as e:
        logger.error(f"Error importing JSON to Firebase: {str(e)}")
        return False


def migrate_mongodb_to_firebase(collections: List[str] = None) -> bool:
    """
    Migrate data directly from MongoDB to Firebase.

    Args:
        collections: List of collection names to migrate (None for all)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create MongoDB adapter
        mongodb = MongoDBAdapter()
        if not mongodb.connect():
            logger.error("Failed to connect to MongoDB")
            return False

        # Create Firebase adapter
        firebase = FirebaseAdapter()
        if not firebase.connect():
            logger.error("Failed to connect to Firebase")
            mongodb.disconnect()
            return False

        # Get all collections if not specified
        if collections is None:
            # This is a simplified approach - in a real application, you would
            # get the list of collections from MongoDB
            collections = [
                'users',
                'trends',
                'companies',
                'products',
                'resources',
                'metrics',
                'insights',
                'stories',
                'pages'
            ]

        # Migrate each collection
        for collection_name in collections:
            # Get documents from MongoDB
            documents = mongodb.find(collection_name)
            if not documents:
                logger.warning(f"No documents found in collection: {collection_name}")
                continue

            # Convert ObjectId to string for Firebase
            for doc in documents:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])

            # Insert documents into Firebase
            doc_ids = firebase.insert_many(collection_name, documents)
            logger.info(f"Migrated {len(doc_ids)} documents from MongoDB to Firebase for collection: {collection_name}")

        mongodb.disconnect()
        firebase.disconnect()
        return True
    except Exception as e:
        logger.error(f"Error migrating MongoDB to Firebase: {str(e)}")
        return False


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Export MongoDB to JSON
    export_mongodb_to_json()

    # Import JSON to Firebase
    import_json_to_firebase()

    # Or migrate directly
    # migrate_mongodb_to_firebase()
