"""
Database Manager Module

This module provides a unified database manager for TrendSense.
It replaces the existing mongodb_manager and mongodb_service with a more flexible
adapter-based approach that supports multiple database backends.
"""

import os
import logging
from typing import Dict, List, Optional, Any, Union

from .database_service import database_service

# Configure logging
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Database manager for TrendSense."""

    _instance = None

    def __new__(cls):
        """Singleton pattern to ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the database manager."""
        if self._initialized:
            return

        # Use the database service
        self._service = database_service
        self._initialized = True

    def connect(self) -> bool:
        """
        Connect to the database.

        Returns:
            bool: True if connection successful, False otherwise
        """
        return self._service.is_connected()

    def disconnect(self) -> None:
        """Disconnect from the database."""
        self._service.disconnect()

    def is_connected(self) -> bool:
        """
        Check if connected to the database.

        Returns:
            bool: True if connected, False otherwise
        """
        return self._service.is_connected()

    def get_collection(self, collection_name: str) -> Any:
        """
        Get a collection from the database.

        Args:
            collection_name: Name of the collection

        Returns:
            Collection object or None if error
        """
        return self._service.get_collection(collection_name)

    def initialize_collections(self, collections: List[str]) -> None:
        """
        Initialize collections if they don't exist.

        Args:
            collections: List of collection names to initialize
        """
        self._service.initialize_collections(collections)

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
        return self._service.find_one(collection_name, query, projection)

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
        return self._service.find(collection_name, query, projection, sort, limit, skip)

    def insert_one(self, collection_name: str, document: Dict) -> Optional[str]:
        """
        Insert a document into a collection.

        Args:
            collection_name: Name of the collection
            document: Document to insert

        Returns:
            ID of the inserted document or None if error
        """
        return self._service.insert_one(collection_name, document)

    def insert_many(self, collection_name: str, documents: List[Dict]) -> List[str]:
        """
        Insert multiple documents into a collection.

        Args:
            collection_name: Name of the collection
            documents: Documents to insert

        Returns:
            List of inserted document IDs or empty list if error
        """
        return self._service.insert_many(collection_name, documents)

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
        return self._service.update_one(collection_name, query, update, upsert)

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
        return self._service.update_many(collection_name, query, update, upsert)

    def delete_one(self, collection_name: str, query: Dict) -> bool:
        """
        Delete a document from a collection.

        Args:
            collection_name: Name of the collection
            query: Query filter

        Returns:
            True if successful, False otherwise
        """
        return self._service.delete_one(collection_name, query)

    def delete_many(self, collection_name: str, query: Dict) -> int:
        """
        Delete multiple documents from a collection.

        Args:
            collection_name: Name of the collection
            query: Query filter

        Returns:
            Number of documents deleted
        """
        return self._service.delete_many(collection_name, query)

    def count_documents(self, collection_name: str, query: Dict = None) -> int:
        """
        Count documents in a collection.

        Args:
            collection_name: Name of the collection
            query: Query filter

        Returns:
            Number of documents
        """
        return self._service.count_documents(collection_name, query)

    def aggregate(self, collection_name: str, pipeline: List[Dict]) -> List[Dict]:
        """
        Perform an aggregation pipeline on a collection.

        Args:
            collection_name: Name of the collection
            pipeline: Aggregation pipeline

        Returns:
            List of documents
        """
        return self._service.aggregate(collection_name, pipeline)

    # Common utility methods for TrendSense
    def get_metrics(self) -> Dict:
        """
        Get sustainability metrics.

        Returns:
            Metrics document or empty dict if not found
        """
        return self._service.get_metrics()

    def get_insights(self) -> List[Dict]:
        """
        Get sustainability insights.

        Returns:
            List of insights or empty list if not found
        """
        return self._service.get_insights()

    def get_companies(self, limit: int = 10) -> List[Dict]:
        """
        Get companies for VC dashboard.

        Args:
            limit: Maximum number of companies to return

        Returns:
            List of companies or empty list if not found
        """
        return self._service.get_companies(limit)

    def create_story(self, story_data: Dict) -> Optional[str]:
        """
        Create a new sustainability story.

        Args:
            story_data: Story data

        Returns:
            Story ID or None if failed
        """
        return self._service.create_story(story_data)

    def get_stories(self, filters: Dict = None, limit: int = 10) -> List[Dict]:
        """
        Get sustainability stories.

        Args:
            filters: Query filters
            limit: Maximum number of stories to return

        Returns:
            List of stories or empty list if not found
        """
        return self._service.get_stories(filters, limit)


# Create singleton instance
db_manager = DatabaseManager()

# For backwards compatibility
def get_database():
    """Get the database instance."""
    return db_manager

def verify_connection() -> bool:
    """Verify database connection is active."""
    return db_manager.is_connected()

def close_connections():
    """Close all database connections."""
    db_manager.disconnect()
