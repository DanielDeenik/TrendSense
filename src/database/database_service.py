"""
Database Service Module

This module provides a unified database service for TrendSense.
It uses the adapter pattern to support multiple database backends.
"""

import os
import logging
from typing import Dict, List, Optional, Any, Union

from .adapters import get_database_adapter, DatabaseAdapter

# Configure logging
logger = logging.getLogger(__name__)


class DatabaseService:
    """Database service for TrendSense."""

    _instance = None

    def __new__(cls):
        """Singleton pattern to ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the database service."""
        if self._initialized:
            return

        # Get adapter type from environment
        adapter_type = os.getenv('DATABASE_ADAPTER', 'firebase').lower()

        # Create adapter
        self._adapter = get_database_adapter(adapter_type)

        # Connect to database
        self._connect()

        self._initialized = True

    def _connect(self) -> bool:
        """
        Connect to the database (internal method).

        Returns:
            bool: True if connection successful, False otherwise
        """
        return self._adapter.connect()

    def connect(self) -> bool:
        """
        Connect to the database (public method).

        Returns:
            bool: True if connection successful, False otherwise
        """
        return self._adapter.connect()

    def disconnect(self) -> None:
        """Disconnect from the database."""
        self._adapter.disconnect()

    def is_connected(self) -> bool:
        """
        Check if connected to the database.

        Returns:
            bool: True if connected, False otherwise
        """
        return self._adapter.is_connected()

    def get_collection(self, collection_name: str) -> Any:
        """
        Get a collection from the database.

        Args:
            collection_name: Name of the collection

        Returns:
            Collection object or None if error
        """
        return self._adapter.get_collection(collection_name)

    def initialize_collections(self, collections: List[str]) -> None:
        """
        Initialize collections if they don't exist.

        Args:
            collections: List of collection names to initialize
        """
        self._adapter.initialize_collections(collections)

    def find_one(self, collection_name: str, query: Dict = None, projection: Dict = None) -> Optional[Dict]:
        """
        Find a single document in a collection.

        Args:
            collection_name: Name of the collection
            query: Query filter
            projection: Fields to include/exclude

        Returns:
            Document or None if not found
        """
        return self._adapter.find_one(collection_name, query, projection)

    def find(self, collection_name: str, query: Dict = None, projection: Dict = None,
             sort: List = None, limit: int = 0, skip: int = 0) -> List[Dict]:
        """
        Find documents in a collection.

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
        return self._adapter.find(collection_name, query, projection, sort, limit, skip)

    def insert_one(self, collection_name: str, document: Dict) -> Optional[str]:
        """
        Insert a document into a collection.

        Args:
            collection_name: Name of the collection
            document: Document to insert

        Returns:
            ID of the inserted document or None if error
        """
        return self._adapter.insert_one(collection_name, document)

    def insert_many(self, collection_name: str, documents: List[Dict]) -> List[str]:
        """
        Insert multiple documents into a collection.

        Args:
            collection_name: Name of the collection
            documents: Documents to insert

        Returns:
            List of inserted document IDs or empty list if error
        """
        return self._adapter.insert_many(collection_name, documents)

    def update_one(self, collection_name: str, query: Dict, update: Dict, upsert: bool = False) -> bool:
        """
        Update a document in a collection.

        Args:
            collection_name: Name of the collection
            query: Query filter
            update: Update operations
            upsert: Whether to insert if document doesn't exist

        Returns:
            True if successful, False otherwise
        """
        return self._adapter.update_one(collection_name, query, update, upsert)

    def update_many(self, collection_name: str, query: Dict, update: Dict, upsert: bool = False) -> int:
        """
        Update multiple documents in a collection.

        Args:
            collection_name: Name of the collection
            query: Query filter
            update: Update operations
            upsert: Whether to insert if documents don't exist

        Returns:
            Number of documents modified
        """
        return self._adapter.update_many(collection_name, query, update, upsert)

    def delete_one(self, collection_name: str, query: Dict) -> bool:
        """
        Delete a document from a collection.

        Args:
            collection_name: Name of the collection
            query: Query filter

        Returns:
            True if successful, False otherwise
        """
        return self._adapter.delete_one(collection_name, query)

    def delete_many(self, collection_name: str, query: Dict) -> int:
        """
        Delete multiple documents from a collection.

        Args:
            collection_name: Name of the collection
            query: Query filter

        Returns:
            Number of documents deleted
        """
        return self._adapter.delete_many(collection_name, query)

    def count_documents(self, collection_name: str, query: Dict = None) -> int:
        """
        Count documents in a collection.

        Args:
            collection_name: Name of the collection
            query: Query filter

        Returns:
            Number of documents
        """
        return self._adapter.count_documents(collection_name, query)

    def aggregate(self, collection_name: str, pipeline: List[Dict]) -> List[Dict]:
        """
        Perform an aggregation pipeline on a collection.

        Args:
            collection_name: Name of the collection
            pipeline: Aggregation pipeline

        Returns:
            List of documents
        """
        return self._adapter.aggregate(collection_name, pipeline)

    # Common utility methods for TrendSense
    def get_metrics(self) -> Dict:
        """
        Get sustainability metrics.

        Returns:
            Metrics document or empty dict if not found
        """
        return self._adapter.get_metrics()

    def get_insights(self) -> List[Dict]:
        """
        Get sustainability insights.

        Returns:
            List of insights or empty list if not found
        """
        return self._adapter.get_insights()

    def get_companies(self, limit: int = 10) -> List[Dict]:
        """
        Get companies for VC dashboard.

        Args:
            limit: Maximum number of companies to return

        Returns:
            List of companies or empty list if not found
        """
        return self._adapter.get_companies(limit)

    def create_story(self, story_data: Dict) -> Optional[str]:
        """
        Create a new sustainability story.

        Args:
            story_data: Story data

        Returns:
            Story ID or None if failed
        """
        return self._adapter.create_story(story_data)

    def get_stories(self, filters: Dict = None, limit: int = 10) -> List[Dict]:
        """
        Get sustainability stories.

        Args:
            filters: Query filters
            limit: Maximum number of stories to return

        Returns:
            List of stories or empty list if not found
        """
        return self._adapter.get_stories(filters, limit)


# Create singleton instance
database_service = DatabaseService()
