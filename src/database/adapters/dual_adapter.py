"""
Dual Database Adapter

This module provides a dual database adapter that writes to both Firebase and MongoDB.
"""

import os
import logging
from typing import Dict, List, Optional, Any, Union

from .base_adapter import DatabaseAdapter
from .firebase_adapter import FirebaseAdapter
from .mongodb_adapter import MongoDBAdapter

# Configure logging
logger = logging.getLogger(__name__)


class DualDatabaseAdapter(DatabaseAdapter):
    """Dual database adapter that writes to both Firebase and MongoDB."""

    def __init__(self, primary_adapter_type: str = 'firebase', secondary_adapter_type: str = 'mongodb'):
        """
        Initialize the dual database adapter.

        Args:
            primary_adapter_type: Primary database adapter type ('firebase' or 'mongodb')
            secondary_adapter_type: Secondary database adapter type ('firebase' or 'mongodb')
        """
        # Initialize adapters
        if primary_adapter_type == 'firebase':
            self.primary_adapter = FirebaseAdapter()
            self.secondary_adapter = MongoDBAdapter()
        else:
            self.primary_adapter = MongoDBAdapter()
            self.secondary_adapter = FirebaseAdapter()

        # Set adapter types
        self.primary_adapter_type = primary_adapter_type
        self.secondary_adapter_type = secondary_adapter_type

        # Initialize connection status
        self.primary_connected = False
        self.secondary_connected = False

    def connect(self) -> bool:
        """
        Connect to both databases.

        Returns:
            bool: True if connection to primary database successful, False otherwise
        """
        # Connect to primary database
        self.primary_connected = self.primary_adapter.connect()
        if not self.primary_connected:
            logger.error(f"Failed to connect to primary database ({self.primary_adapter_type})")
            return False

        # Connect to secondary database
        self.secondary_connected = self.secondary_adapter.connect()
        if not self.secondary_connected:
            logger.warning(f"Failed to connect to secondary database ({self.secondary_adapter_type})")
            # Continue even if secondary connection fails

        logger.info(f"Connected to primary database ({self.primary_adapter_type})")
        if self.secondary_connected:
            logger.info(f"Connected to secondary database ({self.secondary_adapter_type})")

        return self.primary_connected

    def disconnect(self) -> None:
        """Disconnect from both databases."""
        if self.primary_adapter:
            self.primary_adapter.disconnect()
            self.primary_connected = False
        if self.secondary_adapter:
            self.secondary_adapter.disconnect()
            self.secondary_connected = False
        logger.info("Disconnected from databases")

    def is_connected(self) -> bool:
        """
        Check if connected to primary database.

        Returns:
            bool: True if connected to primary database, False otherwise
        """
        return self.primary_connected and self.primary_adapter.is_connected()

    def initialize_collections(self, collections: List[str]) -> None:
        """
        Initialize collections in both databases.

        Args:
            collections: List of collection names to initialize
        """
        # Initialize collections in primary database
        if self.primary_connected:
            self.primary_adapter.initialize_collections(collections)

        # Initialize collections in secondary database
        if self.secondary_connected:
            self.secondary_adapter.initialize_collections(collections)

    def find_one(self, collection_name: str, query: Dict = None, projection: Dict = None) -> Optional[Dict]:
        """
        Find a single document in a collection from primary database.

        Args:
            collection_name: Name of the collection
            query: Query filter
            projection: Fields to include/exclude

        Returns:
            Document or None if not found
        """
        # Read from primary database
        if self.primary_connected:
            return self.primary_adapter.find_one(collection_name, query, projection)
        return None

    def find(self, collection_name: str, query: Dict = None, projection: Dict = None,
             sort: List = None, limit: int = 0, skip: int = 0) -> List[Dict]:
        """
        Find documents in a collection from primary database.

        Args:
            collection_name: Name of the collection
            query: Query filter
            projection: Fields to include/exclude
            sort: Sort specification
            limit: Maximum number of documents to return
            skip: Number of documents to skip

        Returns:
            List of documents
        """
        # Read from primary database
        if self.primary_connected:
            return self.primary_adapter.find(collection_name, query, projection, sort, limit, skip)
        return []

    def insert_one(self, collection_name: str, document: Dict) -> Optional[str]:
        """
        Insert a document into a collection in both databases.

        Args:
            collection_name: Name of the collection
            document: Document to insert

        Returns:
            ID of the inserted document from primary database or None if error
        """
        primary_id = None

        # Insert into primary database
        if self.primary_connected:
            primary_id = self.primary_adapter.insert_one(collection_name, document)
            if not primary_id:
                logger.error(f"Failed to insert document into primary database ({self.primary_adapter_type})")
                return None

        # Insert into secondary database
        if self.secondary_connected:
            # If primary insert was successful, use the same ID
            if primary_id and '_id' not in document:
                document['_id'] = primary_id

            secondary_id = self.secondary_adapter.insert_one(collection_name, document)
            if not secondary_id:
                logger.warning(f"Failed to insert document into secondary database ({self.secondary_adapter_type})")
                # Continue even if secondary insert fails

        return primary_id

    def insert_many(self, collection_name: str, documents: List[Dict]) -> List[str]:
        """
        Insert multiple documents into a collection in both databases.

        Args:
            collection_name: Name of the collection
            documents: Documents to insert

        Returns:
            List of inserted document IDs from primary database or empty list if error
        """
        primary_ids = []

        # Insert into primary database
        if self.primary_connected:
            primary_ids = self.primary_adapter.insert_many(collection_name, documents)
            if not primary_ids:
                logger.error(f"Failed to insert documents into primary database ({self.primary_adapter_type})")
                return []

        # Insert into secondary database
        if self.secondary_connected:
            # If primary insert was successful, use the same IDs
            if primary_ids and len(primary_ids) == len(documents):
                for i, doc in enumerate(documents):
                    if '_id' not in doc:
                        doc['_id'] = primary_ids[i]

            secondary_ids = self.secondary_adapter.insert_many(collection_name, documents)
            if not secondary_ids:
                logger.warning(f"Failed to insert documents into secondary database ({self.secondary_adapter_type})")
                # Continue even if secondary insert fails

        return primary_ids

    def update_one(self, collection_name: str, query: Dict, update: Dict, upsert: bool = False) -> bool:
        """
        Update a document in a collection in both databases.

        Args:
            collection_name: Name of the collection
            query: Query filter
            update: Update operations
            upsert: Whether to insert if document doesn't exist

        Returns:
            True if update successful in primary database, False otherwise
        """
        primary_result = False

        # Update in primary database
        if self.primary_connected:
            primary_result = self.primary_adapter.update_one(collection_name, query, update, upsert)
            if not primary_result:
                logger.error(f"Failed to update document in primary database ({self.primary_adapter_type})")
                return False

        # Update in secondary database
        if self.secondary_connected:
            secondary_result = self.secondary_adapter.update_one(collection_name, query, update, upsert)
            if not secondary_result:
                logger.warning(f"Failed to update document in secondary database ({self.secondary_adapter_type})")
                # Continue even if secondary update fails

        return primary_result

    def update_many(self, collection_name: str, query: Dict, update: Dict, upsert: bool = False) -> int:
        """
        Update multiple documents in a collection in both databases.

        Args:
            collection_name: Name of the collection
            query: Query filter
            update: Update operations
            upsert: Whether to insert if documents don't exist

        Returns:
            Number of documents modified in primary database
        """
        primary_count = 0

        # Update in primary database
        if self.primary_connected:
            primary_count = self.primary_adapter.update_many(collection_name, query, update, upsert)
            if primary_count == 0:
                logger.warning(f"No documents updated in primary database ({self.primary_adapter_type})")

        # Update in secondary database
        if self.secondary_connected:
            secondary_count = self.secondary_adapter.update_many(collection_name, query, update, upsert)
            if secondary_count == 0:
                logger.warning(f"No documents updated in secondary database ({self.secondary_adapter_type})")
                # Continue even if secondary update fails

        return primary_count

    def delete_one(self, collection_name: str, query: Dict) -> bool:
        """
        Delete a document from a collection in both databases.

        Args:
            collection_name: Name of the collection
            query: Query filter

        Returns:
            True if deletion successful in primary database, False otherwise
        """
        primary_result = False

        # Delete from primary database
        if self.primary_connected:
            primary_result = self.primary_adapter.delete_one(collection_name, query)
            if not primary_result:
                logger.error(f"Failed to delete document from primary database ({self.primary_adapter_type})")
                return False

        # Delete from secondary database
        if self.secondary_connected:
            secondary_result = self.secondary_adapter.delete_one(collection_name, query)
            if not secondary_result:
                logger.warning(f"Failed to delete document from secondary database ({self.secondary_adapter_type})")
                # Continue even if secondary delete fails

        return primary_result

    def delete_many(self, collection_name: str, query: Dict) -> int:
        """
        Delete multiple documents from a collection in both databases.

        Args:
            collection_name: Name of the collection
            query: Query filter

        Returns:
            Number of documents deleted from primary database
        """
        primary_count = 0

        # Delete from primary database
        if self.primary_connected:
            primary_count = self.primary_adapter.delete_many(collection_name, query)
            if primary_count == 0:
                logger.warning(f"No documents deleted from primary database ({self.primary_adapter_type})")

        # Delete from secondary database
        if self.secondary_connected:
            secondary_count = self.secondary_adapter.delete_many(collection_name, query)
            if secondary_count == 0:
                logger.warning(f"No documents deleted from secondary database ({self.secondary_adapter_type})")
                # Continue even if secondary delete fails

        return primary_count

    def count_documents(self, collection_name: str, query: Dict = None) -> int:
        """
        Count documents in a collection in primary database.

        Args:
            collection_name: Name of the collection
            query: Query filter

        Returns:
            Number of documents
        """
        # Count in primary database
        if self.primary_connected:
            return self.primary_adapter.count_documents(collection_name, query)
        return 0

    def aggregate(self, collection_name: str, pipeline: List[Dict]) -> List[Dict]:
        """
        Perform an aggregation pipeline on a collection in primary database.

        Args:
            collection_name: Name of the collection
            pipeline: Aggregation pipeline

        Returns:
            List of documents
        """
        # Aggregate in primary database
        if self.primary_connected:
            return self.primary_adapter.aggregate(collection_name, pipeline)
        return []

    def get_collection(self, collection_name: str) -> Any:
        """
        Get a collection from the primary database.

        Args:
            collection_name: Name of the collection

        Returns:
            Collection object or None if error
        """
        if self.primary_connected:
            return self.primary_adapter.get_collection(collection_name)
        return None

    # Common utility methods for TrendSense
    def get_metrics(self) -> Dict:
        """
        Get sustainability metrics from primary database.

        Returns:
            Metrics document or empty dict if not found
        """
        if self.primary_connected:
            return self.primary_adapter.get_metrics()
        return {}

    def get_insights(self) -> List[Dict]:
        """
        Get sustainability insights from primary database.

        Returns:
            List of insights or empty list if not found
        """
        if self.primary_connected:
            return self.primary_adapter.get_insights()
        return []

    def get_companies(self, limit: int = 10) -> List[Dict]:
        """
        Get companies for VC dashboard from primary database.

        Args:
            limit: Maximum number of companies to return

        Returns:
            List of companies or empty list if not found
        """
        if self.primary_connected:
            return self.primary_adapter.get_companies(limit)
        return []

    def create_story(self, story_data: Dict) -> Optional[str]:
        """
        Create a new sustainability story in both databases.

        Args:
            story_data: Story data

        Returns:
            Story ID from primary database or None if failed
        """
        primary_id = None

        # Insert into primary database
        if self.primary_connected:
            primary_id = self.primary_adapter.create_story(story_data)
            if not primary_id:
                logger.error(f"Failed to create story in primary database ({self.primary_adapter_type})")
                return None

        # Insert into secondary database
        if self.secondary_connected:
            # If primary insert was successful, use the same ID
            if primary_id and '_id' not in story_data:
                story_data['_id'] = primary_id

            secondary_id = self.secondary_adapter.create_story(story_data)
            if not secondary_id:
                logger.warning(f"Failed to create story in secondary database ({self.secondary_adapter_type})")
                # Continue even if secondary insert fails

        return primary_id

    def get_stories(self, filters: Dict = None, limit: int = 10) -> List[Dict]:
        """
        Get sustainability stories from primary database.

        Args:
            filters: Query filters
            limit: Maximum number of stories to return

        Returns:
            List of stories or empty list if not found
        """
        if self.primary_connected:
            return self.primary_adapter.get_stories(filters, limit)
        return []
