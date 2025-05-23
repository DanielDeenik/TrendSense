"""
MongoDB Adapter

This module provides a MongoDB adapter that implements the DatabaseAdapter interface.
"""

import os
import logging
import traceback
from typing import Dict, List, Optional, Any, Union

from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, DuplicateKeyError
import urllib.parse

from .base_adapter import DatabaseAdapter

# Configure logging
logger = logging.getLogger(__name__)


class MongoDBAdapter(DatabaseAdapter):
    """MongoDB adapter for TrendSense."""

    def __init__(self, uri: str = None, db_name: str = None):
        """
        Initialize the MongoDB adapter.

        Args:
            uri: MongoDB connection URI
            db_name: MongoDB database name
        """
        # Get MongoDB configuration from environment or use defaults
        self.uri = uri or os.getenv('MONGODB_URI', 'mongodb://localhost:27017/sustainatrend')
        self.db_name = db_name or os.getenv('MONGODB_DB', 'sustainatrend')

        # Try to use MongoDB Atlas if credentials are provided
        username = os.getenv('MONGODB_USERNAME')
        password = os.getenv('MONGODB_PASSWORD')

        if username and password:
            # Construct MongoDB Atlas URI
            atlas_uri = f"mongodb+srv://{urllib.parse.quote_plus(username)}:{urllib.parse.quote_plus(password)}@trendsense.m0vdz.mongodb.net/{self.db_name}?retryWrites=true&w=majority&authSource=admin"
            self.uri = atlas_uri
            logger.info(f"Using MongoDB Atlas with username: {username}")

        # Initialize client and database
        self.client = None
        self.db = None
        self.connected = False

    def connect(self) -> bool:
        """
        Connect to MongoDB.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Initialize MongoDB client with connection pooling
            self.client = MongoClient(
                self.uri,
                maxPoolSize=50,
                serverSelectionTimeoutMS=5000
            )

            # Test connection
            self.client.admin.command('ping')

            # Get database
            self.db = self.client[self.db_name]

            self.connected = True
            logger.info(f"Connected to MongoDB: {self.uri}")
            return True
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"MongoDB connection failed: {str(e)}")
            self.connected = False
            return False
        except Exception as e:
            logger.error(f"Unexpected error connecting to MongoDB: {str(e)}")
            logger.error(traceback.format_exc())
            self.connected = False
            return False

    def disconnect(self) -> None:
        """Disconnect from MongoDB."""
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
            self.connected = False
            logger.info("Disconnected from MongoDB")

    def is_connected(self) -> bool:
        """
        Check if connected to MongoDB.

        Returns:
            bool: True if connected, False otherwise
        """
        if not self.connected or not self.client:
            return False

        try:
            # Check if connection is still alive
            self.client.admin.command('ping')
            return True
        except Exception:
            self.connected = False
            return False

    def get_collection(self, collection_name: str) -> Optional[Collection]:
        """
        Get a MongoDB collection.

        Args:
            collection_name: Name of the collection

        Returns:
            Collection object or None if error
        """
        if not self.is_connected():
            logger.error(f"Cannot get collection {collection_name}: Not connected to MongoDB")
            return None

        return self.db[collection_name]

    def initialize_collections(self, collections: List[str]) -> None:
        """
        Initialize collections if they don't exist.

        Args:
            collections: List of collection names to initialize
        """
        if not self.is_connected():
            if not self.connect():
                logger.error("Cannot initialize collections: Not connected to MongoDB")
                return

        try:
            # Get existing collections
            existing_collections = self.db.list_collection_names()

            # Create collections that don't exist
            for collection_name in collections:
                if collection_name not in existing_collections:
                    self.db.create_collection(collection_name)
                    logger.info(f"Created collection: {collection_name}")

        except Exception as e:
            logger.error(f"Error initializing collections: {str(e)}")

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
        collection = self.get_collection(collection_name)
        if collection is None:
            return None

        query = query or {}
        try:
            return collection.find_one(query, projection)
        except Exception as e:
            logger.error(f"Error finding document in {collection_name}: {str(e)}")
            return None

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
        collection = self.get_collection(collection_name)
        if collection is None:
            return []

        query = query or {}
        try:
            cursor = collection.find(query, projection)

            if sort:
                cursor = cursor.sort(sort)

            if skip:
                cursor = cursor.skip(skip)

            if limit:
                cursor = cursor.limit(limit)

            return list(cursor)
        except Exception as e:
            logger.error(f"Error finding documents in {collection_name}: {str(e)}")
            return []

    def insert_one(self, collection_name: str, document: Dict) -> Optional[str]:
        """
        Insert a document into a collection.

        Args:
            collection_name: Name of the collection
            document: Document to insert

        Returns:
            ID of the inserted document or None if error
        """
        collection = self.get_collection(collection_name)
        if collection is None:
            return None

        try:
            result = collection.insert_one(document)
            return str(result.inserted_id)
        except DuplicateKeyError:
            logger.error(f"Duplicate key error inserting document into {collection_name}")
            return None
        except Exception as e:
            logger.error(f"Error inserting document into {collection_name}: {str(e)}")
            return None

    def insert_many(self, collection_name: str, documents: List[Dict]) -> List[str]:
        """
        Insert multiple documents into a collection.

        Args:
            collection_name: Name of the collection
            documents: Documents to insert

        Returns:
            List of inserted document IDs or empty list if error
        """
        collection = self.get_collection(collection_name)
        if collection is None:
            return []

        try:
            result = collection.insert_many(documents)
            return [str(id) for id in result.inserted_ids]
        except DuplicateKeyError:
            logger.error(f"Duplicate key error inserting documents into {collection_name}")
            return []
        except Exception as e:
            logger.error(f"Error inserting documents into {collection_name}: {str(e)}")
            return []

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
        collection = self.get_collection(collection_name)
        if collection is None:
            return False

        try:
            result = collection.update_one(query, update, upsert=upsert)
            return result.modified_count > 0 or (upsert and result.upserted_id is not None)
        except Exception as e:
            logger.error(f"Error updating document in {collection_name}: {str(e)}")
            return False

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
        collection = self.get_collection(collection_name)
        if collection is None:
            return 0

        try:
            result = collection.update_many(query, update, upsert=upsert)
            return result.modified_count
        except Exception as e:
            logger.error(f"Error updating documents in {collection_name}: {str(e)}")
            return 0

    def delete_one(self, collection_name: str, query: Dict) -> bool:
        """
        Delete a document from a collection.

        Args:
            collection_name: Name of the collection
            query: Query filter

        Returns:
            True if successful, False otherwise
        """
        collection = self.get_collection(collection_name)
        if collection is None:
            return False

        try:
            result = collection.delete_one(query)
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting document from {collection_name}: {str(e)}")
            return False

    def delete_many(self, collection_name: str, query: Dict) -> int:
        """
        Delete multiple documents from a collection.

        Args:
            collection_name: Name of the collection
            query: Query filter

        Returns:
            Number of documents deleted
        """
        collection = self.get_collection(collection_name)
        if collection is None:
            return 0

        try:
            result = collection.delete_many(query)
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error deleting documents from {collection_name}: {str(e)}")
            return 0

    def count_documents(self, collection_name: str, query: Dict = None) -> int:
        """
        Count documents in a collection.

        Args:
            collection_name: Name of the collection
            query: Query filter

        Returns:
            Number of documents
        """
        collection = self.get_collection(collection_name)
        if collection is None:
            return 0

        query = query or {}
        try:
            return collection.count_documents(query)
        except Exception as e:
            logger.error(f"Error counting documents in {collection_name}: {str(e)}")
            return 0

    def aggregate(self, collection_name: str, pipeline: List[Dict]) -> List[Dict]:
        """
        Perform an aggregation pipeline on a collection.

        Args:
            collection_name: Name of the collection
            pipeline: Aggregation pipeline

        Returns:
            List of documents
        """
        collection = self.get_collection(collection_name)
        if collection is None:
            return []

        try:
            return list(collection.aggregate(pipeline))
        except Exception as e:
            logger.error(f"Error performing aggregation on {collection_name}: {str(e)}")
            return []

    # Common utility methods for TrendSense
    def get_metrics(self) -> Dict:
        """
        Get sustainability metrics.

        Returns:
            Metrics document or empty dict if not found
        """
        metrics = self.find_one('metrics')
        return metrics or {}

    def get_insights(self) -> List[Dict]:
        """
        Get sustainability insights.

        Returns:
            List of insights or empty list if not found
        """
        insights = self.find('insights')
        return insights or []

    def get_companies(self, limit: int = 10) -> List[Dict]:
        """
        Get companies for VC dashboard.

        Args:
            limit: Maximum number of companies to return

        Returns:
            List of companies or empty list if not found
        """
        companies = self.find('companies', limit=limit)
        return companies or []

    def create_story(self, story_data: Dict) -> Optional[str]:
        """
        Create a new sustainability story.

        Args:
            story_data: Story data

        Returns:
            Story ID or None if failed
        """
        return self.insert_one('stories', story_data)

    def get_stories(self, filters: Dict = None, limit: int = 10) -> List[Dict]:
        """
        Get sustainability stories.

        Args:
            filters: Query filters
            limit: Maximum number of stories to return

        Returns:
            List of stories or empty list if not found
        """
        stories = self.find('stories', filters, limit=limit)
        return stories or []
