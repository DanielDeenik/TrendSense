"""
Database Adapter Interface

This module defines the interface for database adapters in TrendSense.
All database adapters must implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union


class DatabaseAdapter(ABC):
    """Base interface for database adapters."""

    @abstractmethod
    def connect(self) -> bool:
        """
        Connect to the database.

        Returns:
            bool: True if connection successful, False otherwise
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the database."""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """
        Check if connected to the database.

        Returns:
            bool: True if connected, False otherwise
        """
        pass

    @abstractmethod
    def get_collection(self, collection_name: str) -> Any:
        """
        Get a collection/table from the database.

        Args:
            collection_name: Name of the collection

        Returns:
            Collection object or None if error
        """
        pass

    @abstractmethod
    def initialize_collections(self, collections: List[str]) -> None:
        """
        Initialize collections if they don't exist.

        Args:
            collections: List of collection names to initialize
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def insert_one(self, collection_name: str, document: Dict) -> Optional[str]:
        """
        Insert a document into a collection.

        Args:
            collection_name: Name of the collection
            document: Document to insert

        Returns:
            ID of the inserted document or None if error
        """
        pass

    @abstractmethod
    def insert_many(self, collection_name: str, documents: List[Dict]) -> List[str]:
        """
        Insert multiple documents into a collection.

        Args:
            collection_name: Name of the collection
            documents: Documents to insert

        Returns:
            List of inserted document IDs or empty list if error
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def delete_one(self, collection_name: str, query: Dict) -> bool:
        """
        Delete a document from a collection.

        Args:
            collection_name: Name of the collection
            query: Query filter

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def delete_many(self, collection_name: str, query: Dict) -> int:
        """
        Delete multiple documents from a collection.

        Args:
            collection_name: Name of the collection
            query: Query filter

        Returns:
            Number of documents deleted
        """
        pass

    @abstractmethod
    def count_documents(self, collection_name: str, query: Dict = None) -> int:
        """
        Count documents in a collection.

        Args:
            collection_name: Name of the collection
            query: Query filter

        Returns:
            Number of documents
        """
        pass

    @abstractmethod
    def aggregate(self, collection_name: str, pipeline: List[Dict]) -> List[Dict]:
        """
        Perform an aggregation pipeline on a collection.

        Args:
            collection_name: Name of the collection
            pipeline: Aggregation pipeline

        Returns:
            List of documents
        """
        pass

    # Common utility methods for TrendSense
    @abstractmethod
    def get_metrics(self) -> Dict:
        """
        Get sustainability metrics.

        Returns:
            Metrics document or empty dict if not found
        """
        pass

    @abstractmethod
    def get_insights(self) -> List[Dict]:
        """
        Get sustainability insights.

        Returns:
            List of insights or empty list if not found
        """
        pass

    @abstractmethod
    def get_companies(self, limit: int = 10) -> List[Dict]:
        """
        Get companies for VC dashboard.

        Args:
            limit: Maximum number of companies to return

        Returns:
            List of companies or empty list if not found
        """
        pass

    @abstractmethod
    def create_story(self, story_data: Dict) -> Optional[str]:
        """
        Create a new sustainability story.

        Args:
            story_data: Story data

        Returns:
            Story ID or None if failed
        """
        pass

    @abstractmethod
    def get_stories(self, filters: Dict = None, limit: int = 10) -> List[Dict]:
        """
        Get sustainability stories.

        Args:
            filters: Query filters
            limit: Maximum number of stories to return

        Returns:
            List of stories or empty list if not found
        """
        pass
