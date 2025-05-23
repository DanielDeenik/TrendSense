"""
MongoDB Service for SustainaTrend™

This module provides a unified MongoDB service for the SustainaTrend™ application.
It handles connection management, data initialization, and CRUD operations.
"""

import os
import logging
import urllib.parse
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import traceback

from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, DuplicateKeyError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/mongodb.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MongoDBService:
    """MongoDB service for SustainaTrend™."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Singleton pattern to ensure only one instance of the service exists."""
        if cls._instance is None:
            cls._instance = super(MongoDBService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, uri: str = None, db_name: str = None):
        """
        Initialize the MongoDB service.

        Args:
            uri: MongoDB connection URI
            db_name: MongoDB database name
        """
        if self._initialized:
            return

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

        # Initialize connection properties
        self.client = None
        self.db = None
        self.connected = False

        # Connect to MongoDB
        self.connect()

        # Create indexes if connected
        if self.connected:
            self._create_indexes()

        self._initialized = True

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
            # Test connection
            self.client.admin.command('ping')
            return True
        except Exception as e:
            logger.error(f"MongoDB connection lost: {str(e)}")
            self.connected = False
            return False

    def verify_connection(self) -> bool:
        """
        Verify connection to MongoDB.

        Returns:
            bool: True if connected, False otherwise
        """
        if self.is_connected():
            return True
        else:
            return self.connect()

    def _create_indexes(self) -> None:
        """Create necessary indexes for collections."""
        try:
            # Define all indexes we want to create
            indexes = {
                'users': [
                    ([("email", ASCENDING)], {"unique": True})
                ],
                'trends': [
                    ([("category", ASCENDING)], {}),
                    ([("created_at", DESCENDING)], {})
                ],
                'companies': [
                    ([("sector", ASCENDING)], {}),
                    ([("name", ASCENDING)], {"unique": True})
                ],
                'products': [
                    ([("id", ASCENDING)], {"unique": True})
                ],
                'resources': [
                    ([("id", ASCENDING)], {"unique": True})
                ],
                'metrics': [
                    ([("property_id", ASCENDING)], {}),
                    ([("date", DESCENDING)], {})
                ],
                'insights': [
                    ([("category", ASCENDING)], {}),
                    ([("created_at", DESCENDING)], {})
                ],
                'stories': [
                    ([("category", ASCENDING)], {}),
                    ([("created_at", DESCENDING)], {})
                ],
                'pages': [
                    ([("id", ASCENDING)], {"unique": True})
                ]
            }

            # Create indexes for each collection
            for collection_name, collection_indexes in indexes.items():
                collection = self.db[collection_name]

                for index_fields, index_options in collection_indexes:
                    try:
                        # Try to create the index
                        collection.create_index(index_fields, **index_options)

                        # Log index creation
                        index_names = [f"{field[0]}" for field in index_fields]
                        logger.info(f"Created index on {collection_name}: {', '.join(index_names)}")
                    except DuplicateKeyError as e:
                        # Index already exists with a different name
                        logger.warning(f"Index already exists on {collection_name}: {', '.join([f[0] for f in index_fields])}")
                    except Exception as e:
                        logger.error(f"Error creating index on {collection_name}: {str(e)}")

        except Exception as e:
            logger.error(f"Error creating indexes: {str(e)}")

    def initialize_collections(self, collections: List[str]) -> None:
        """
        Initialize collections if they don't exist.

        Args:
            collections: List of collection names to initialize
        """
        if not self.is_connected():
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

    def get_collection(self, collection_name: str):
        """
        Get a MongoDB collection.

        Args:
            collection_name: Name of the collection

        Returns:
            Collection object or None if not connected
        """
        if not self.is_connected():
            if not self.connect():
                logger.error(f"Cannot get collection {collection_name}: Not connected to MongoDB")
                return None

        return self.db[collection_name]

    def find_one(self, collection_name: str, query: Dict = None, projection: Dict = None) -> Optional[Dict]:
        """
        Find a single document in a collection.

        Args:
            collection_name: Name of the collection
            query: Query filter
            projection: Fields to include or exclude

        Returns:
            Document or None if not found
        """
        collection = self.get_collection(collection_name)
        if collection is None:
            return None

        try:
            return collection.find_one(query or {}, projection)
        except Exception as e:
            logger.error(f"Error finding document in {collection_name}: {str(e)}")
            return None

    def find(self, collection_name: str, query: Dict = None, projection: Dict = None,
             sort: List = None, limit: int = 0, skip: int = 0):
        """
        Find documents in a collection.

        Args:
            collection_name: Name of the collection
            query: Query filter
            projection: Fields to include or exclude
            sort: Sort specification
            limit: Maximum number of documents to return
            skip: Number of documents to skip

        Returns:
            Cursor to the documents or None if error
        """
        collection = self.get_collection(collection_name)
        if collection is None:
            return None

        try:
            cursor = collection.find(query or {}, projection)

            if sort:
                cursor = cursor.sort(sort)

            if skip:
                cursor = cursor.skip(skip)

            if limit:
                cursor = cursor.limit(limit)

            return cursor
        except Exception as e:
            logger.error(f"Error finding documents in {collection_name}: {str(e)}")
            return None

    def count_documents(self, collection_name: str, query: Dict = None) -> int:
        """
        Count documents in a collection.

        Args:
            collection_name: Name of the collection
            query: Query filter

        Returns:
            Number of documents or 0 if error
        """
        collection = self.get_collection(collection_name)
        if collection is None:
            return 0

        try:
            return collection.count_documents(query or {})
        except Exception as e:
            logger.error(f"Error counting documents in {collection_name}: {str(e)}")
            return 0

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

    def insert_many(self, collection_name: str, documents: List[Dict]) -> Optional[List[str]]:
        """
        Insert multiple documents into a collection.

        Args:
            collection_name: Name of the collection
            documents: Documents to insert

        Returns:
            List of IDs of the inserted documents or None if error
        """
        collection = self.get_collection(collection_name)
        if collection is None:
            return None

        try:
            result = collection.insert_many(documents)
            return [str(id) for id in result.inserted_ids]
        except DuplicateKeyError:
            logger.error(f"Duplicate key error inserting documents into {collection_name}")
            return None
        except Exception as e:
            logger.error(f"Error inserting documents into {collection_name}: {str(e)}")
            return None

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
            Number of documents modified or 0 if error
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
            Number of documents deleted or 0 if error
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

    # Domain-specific methods

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
        insights = list(self.find('insights'))
        return insights or []

    def get_companies(self, limit: int = 10) -> List[Dict]:
        """
        Get companies for VC dashboard.

        Args:
            limit: Maximum number of companies to return

        Returns:
            List of companies or empty list if not found
        """
        companies = list(self.find('companies', limit=limit))
        return companies or []

    def get_trends(self, category: str = None, limit: int = 10) -> List[Dict]:
        """
        Get sustainability trends.

        Args:
            category: Category filter
            limit: Maximum number of trends to return

        Returns:
            List of trends or empty list if not found
        """
        query = {"category": category} if category else {}
        sort = [("created_at", DESCENDING)]
        trends = list(self.find('trends', query=query, sort=sort, limit=limit))
        return trends or []

    def create_story(self, story_data: Dict) -> Optional[str]:
        """
        Create a new sustainability story.

        Args:
            story_data: Story data

        Returns:
            Story ID or None if failed
        """
        # Add created_at timestamp if not present
        if 'created_at' not in story_data:
            story_data['created_at'] = datetime.now()

        return self.insert_one('stories', story_data)

    def get_stories(self, category: str = None, limit: int = 10) -> List[Dict]:
        """
        Get sustainability stories.

        Args:
            category: Category filter
            limit: Maximum number of stories to return

        Returns:
            List of stories or empty list if not found
        """
        query = {"category": category} if category else {}
        sort = [("created_at", DESCENDING)]
        stories = list(self.find('stories', query=query, sort=sort, limit=limit))
        return stories or []

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """
        Get a user by email.

        Args:
            email: User email

        Returns:
            User document or None if not found
        """
        return self.find_one('users', {"email": email})

    def get_product_by_id(self, product_id: str) -> Optional[Dict]:
        """
        Get a product by ID.

        Args:
            product_id: Product ID

        Returns:
            Product document or None if not found
        """
        return self.find_one('products', {"id": product_id})

    def get_resource_by_id(self, resource_id: str) -> Optional[Dict]:
        """
        Get a resource by ID.

        Args:
            resource_id: Resource ID

        Returns:
            Resource document or None if not found
        """
        return self.find_one('resources', {"id": resource_id})

    def get_page_by_id(self, page_id: str) -> Optional[Dict]:
        """
        Get a page by ID.

        Args:
            page_id: Page ID

        Returns:
            Page document or None if not found
        """
        return self.find_one('pages', {"id": page_id})

# Create a singleton instance
mongodb_service = MongoDBService()
