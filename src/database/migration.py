"""
Database Migration Utility

This module provides utilities for migrating data between different database adapters.
"""

import os
import sys
import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Import database adapters
from .adapters import get_database_adapter, MongoDBAdapter, FirebaseAdapter


class DatabaseMigration:
    """Database migration utility for TrendSense."""

    def __init__(self, source_adapter_type: str = None, target_adapter_type: str = None):
        """
        Initialize the database migration utility.

        Args:
            source_adapter_type: Source database adapter type ('firebase', 'mongodb', 'mock_firebase')
            target_adapter_type: Target database adapter type ('firebase', 'mongodb', 'mock_firebase')
        """
        # Get adapter types from environment or use defaults
        self.source_adapter_type = source_adapter_type or os.getenv('SOURCE_DATABASE_ADAPTER', 'firebase')
        self.target_adapter_type = target_adapter_type or os.getenv('TARGET_DATABASE_ADAPTER', 'mongodb')

        # Initialize adapters
        self.source_adapter = get_database_adapter(self.source_adapter_type)
        self.target_adapter = get_database_adapter(self.target_adapter_type)

        # Connect to databases
        self.source_connected = self.source_adapter.connect()
        self.target_connected = self.target_adapter.connect()

        # Initialize collections
        self.collections = [
            'companies',
            'funds',
            'trends',
            'stories',
            'insights',
            'metrics',
            'users',
            'projects',
            'documents',
            'vectors'
        ]

    def is_connected(self) -> bool:
        """
        Check if connected to both source and target databases.

        Returns:
            bool: True if connected to both databases, False otherwise
        """
        return self.source_connected and self.target_connected

    def migrate_collection(self, collection_name: str, batch_size: int = 100) -> Tuple[int, int]:
        """
        Migrate a collection from source to target database.

        Args:
            collection_name: Name of the collection to migrate
            batch_size: Number of documents to migrate in each batch

        Returns:
            Tuple[int, int]: (Number of documents migrated, Number of documents failed)
        """
        if not self.is_connected():
            logger.error("Cannot migrate collection: Not connected to databases")
            return 0, 0

        logger.info(f"Migrating collection: {collection_name}")

        # Get documents from source database
        documents = self.source_adapter.find(collection_name)
        total_documents = len(documents)

        if total_documents == 0:
            logger.info(f"No documents found in collection: {collection_name}")
            return 0, 0

        logger.info(f"Found {total_documents} documents in collection: {collection_name}")

        # Migrate documents in batches
        migrated_count = 0
        failed_count = 0
        batches = [documents[i:i + batch_size] for i in range(0, total_documents, batch_size)]

        for i, batch in enumerate(batches):
            logger.info(f"Migrating batch {i+1}/{len(batches)} of collection: {collection_name}")

            # Insert batch into target database
            try:
                # Add migration metadata
                for doc in batch:
                    if '_id' in doc and isinstance(doc['_id'], dict) and '$oid' in doc['_id']:
                        # Handle MongoDB ObjectId serialization
                        doc['_id'] = doc['_id']['$oid']

                    # Add migration timestamp
                    doc['migrated_at'] = datetime.now().isoformat()
                    doc['source_database'] = self.source_adapter_type

                # Insert documents
                result_ids = self.target_adapter.insert_many(collection_name, batch)

                if len(result_ids) > 0:
                    migrated_count += len(result_ids)
                    logger.info(f"Migrated {len(result_ids)} documents in batch {i+1}")
                else:
                    failed_count += len(batch)
                    logger.error(f"Failed to migrate batch {i+1}")
            except Exception as e:
                failed_count += len(batch)
                logger.error(f"Error migrating batch {i+1}: {str(e)}")

            # Sleep to avoid overwhelming the database
            time.sleep(0.1)

        logger.info(f"Migration of collection {collection_name} completed: {migrated_count} migrated, {failed_count} failed")
        return migrated_count, failed_count

    def migrate_all_collections(self) -> Dict[str, Tuple[int, int]]:
        """
        Migrate all collections from source to target database.

        Returns:
            Dict[str, Tuple[int, int]]: Dictionary of collection names to (migrated count, failed count)
        """
        if not self.is_connected():
            logger.error("Cannot migrate collections: Not connected to databases")
            return {}

        logger.info(f"Migrating all collections from {self.source_adapter_type} to {self.target_adapter_type}")

        # Initialize collections in target database
        self.target_adapter.initialize_collections(self.collections)

        # Migrate each collection
        results = {}
        for collection_name in self.collections:
            migrated, failed = self.migrate_collection(collection_name)
            results[collection_name] = (migrated, failed)

        logger.info("Migration of all collections completed")
        return results

    def sync_collection(self, collection_name: str, batch_size: int = 100) -> Tuple[int, int]:
        """
        Sync a collection between source and target database.
        This will update existing documents and add new ones.

        Args:
            collection_name: Name of the collection to sync
            batch_size: Number of documents to sync in each batch

        Returns:
            Tuple[int, int]: (Number of documents synced, Number of documents failed)
        """
        if not self.is_connected():
            logger.error("Cannot sync collection: Not connected to databases")
            return 0, 0

        logger.info(f"Syncing collection: {collection_name}")

        # Get documents from source database
        source_documents = self.source_adapter.find(collection_name)
        total_documents = len(source_documents)

        if total_documents == 0:
            logger.info(f"No documents found in collection: {collection_name}")
            return 0, 0

        logger.info(f"Found {total_documents} documents in collection: {collection_name}")

        # Sync documents in batches
        synced_count = 0
        failed_count = 0
        batches = [source_documents[i:i + batch_size] for i in range(0, total_documents, batch_size)]

        for i, batch in enumerate(batches):
            logger.info(f"Syncing batch {i+1}/{len(batches)} of collection: {collection_name}")

            # Sync batch with target database
            try:
                for doc in batch:
                    # Check if document exists in target database
                    doc_id = doc.get('_id')
                    if doc_id:
                        existing_doc = self.target_adapter.find_one(collection_name, {'_id': doc_id})
                        if existing_doc:
                            # Update existing document
                            doc['synced_at'] = datetime.now().isoformat()
                            doc['source_database'] = self.source_adapter_type
                            result = self.target_adapter.update_one(
                                collection_name,
                                {'_id': doc_id},
                                {'$set': doc}
                            )
                            if result:
                                synced_count += 1
                            else:
                                failed_count += 1
                        else:
                            # Insert new document
                            doc['synced_at'] = datetime.now().isoformat()
                            doc['source_database'] = self.source_adapter_type
                            result = self.target_adapter.insert_one(collection_name, doc)
                            if result:
                                synced_count += 1
                            else:
                                failed_count += 1
                    else:
                        # Document has no ID, insert as new
                        doc['synced_at'] = datetime.now().isoformat()
                        doc['source_database'] = self.source_adapter_type
                        result = self.target_adapter.insert_one(collection_name, doc)
                        if result:
                            synced_count += 1
                        else:
                            failed_count += 1
            except Exception as e:
                failed_count += len(batch)
                logger.error(f"Error syncing batch {i+1}: {str(e)}")

            # Sleep to avoid overwhelming the database
            time.sleep(0.1)

        logger.info(f"Sync of collection {collection_name} completed: {synced_count} synced, {failed_count} failed")
        return synced_count, failed_count

    def sync_all_collections(self) -> Dict[str, Tuple[int, int]]:
        """
        Sync all collections between source and target database.

        Returns:
            Dict[str, Tuple[int, int]]: Dictionary of collection names to (synced count, failed count)
        """
        if not self.is_connected():
            logger.error("Cannot sync collections: Not connected to databases")
            return {}

        logger.info(f"Syncing all collections from {self.source_adapter_type} to {self.target_adapter_type}")

        # Initialize collections in target database
        self.target_adapter.initialize_collections(self.collections)

        # Sync each collection
        results = {}
        for collection_name in self.collections:
            synced, failed = self.sync_collection(collection_name)
            results[collection_name] = (synced, failed)

        logger.info("Sync of all collections completed")
        return results

    def close(self) -> None:
        """Close database connections."""
        if self.source_adapter:
            self.source_adapter.disconnect()
        if self.target_adapter:
            self.target_adapter.disconnect()
        logger.info("Database connections closed")


def migrate_firebase_to_mongodb():
    """Migrate data from Firebase to MongoDB."""
    migration = DatabaseMigration(source_adapter_type='firebase', target_adapter_type='mongodb')
    if migration.is_connected():
        results = migration.migrate_all_collections()
        for collection_name, (migrated, failed) in results.items():
            print(f"{collection_name}: {migrated} migrated, {failed} failed")
    else:
        print("Failed to connect to databases")
    migration.close()


def migrate_mongodb_to_firebase():
    """Migrate data from MongoDB to Firebase."""
    migration = DatabaseMigration(source_adapter_type='mongodb', target_adapter_type='firebase')
    if migration.is_connected():
        results = migration.migrate_all_collections()
        for collection_name, (migrated, failed) in results.items():
            print(f"{collection_name}: {migrated} migrated, {failed} failed")
    else:
        print("Failed to connect to databases")
    migration.close()


def sync_firebase_to_mongodb():
    """Sync data from Firebase to MongoDB."""
    migration = DatabaseMigration(source_adapter_type='firebase', target_adapter_type='mongodb')
    if migration.is_connected():
        results = migration.sync_all_collections()
        for collection_name, (synced, failed) in results.items():
            print(f"{collection_name}: {synced} synced, {failed} failed")
    else:
        print("Failed to connect to databases")
    migration.close()


def sync_mongodb_to_firebase():
    """Sync data from MongoDB to Firebase."""
    migration = DatabaseMigration(source_adapter_type='mongodb', target_adapter_type='firebase')
    if migration.is_connected():
        results = migration.sync_all_collections()
        for collection_name, (synced, failed) in results.items():
            print(f"{collection_name}: {synced} synced, {failed} failed")
    else:
        print("Failed to connect to databases")
    migration.close()


if __name__ == '__main__':
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Database Migration Utility')
    parser.add_argument('--source', choices=['firebase', 'mongodb', 'mock_firebase'], default='firebase',
                        help='Source database adapter type')
    parser.add_argument('--target', choices=['firebase', 'mongodb', 'mock_firebase'], default='mongodb',
                        help='Target database adapter type')
    parser.add_argument('--action', choices=['migrate', 'sync'], default='migrate',
                        help='Action to perform')
    args = parser.parse_args()

    # Create migration utility
    migration = DatabaseMigration(source_adapter_type=args.source, target_adapter_type=args.target)

    if migration.is_connected():
        if args.action == 'migrate':
            results = migration.migrate_all_collections()
        else:
            results = migration.sync_all_collections()

        for collection_name, (count, failed) in results.items():
            print(f"{collection_name}: {count} {args.action}d, {failed} failed")
    else:
        print("Failed to connect to databases")

    migration.close()
