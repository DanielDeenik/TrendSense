"""
MongoDB Connection Manager for SustainaTrend

This module provides a centralized way to manage MongoDB connections
and operations across the application.
"""

import os
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from typing import Dict, List, Any, Optional, Union

# Configure logging
logger = logging.getLogger(__name__)

class MongoDBManager:
    """MongoDB connection manager for SustainaTrend."""
    
    def __init__(self, uri: str = None, db_name: str = None):
        """
        Initialize the MongoDB connection manager.
        
        Args:
            uri: MongoDB connection URI
            db_name: MongoDB database name
        """
        self.uri = uri or os.getenv('MONGODB_URI', 'mongodb://localhost:27017/sustainatrend')
        self.db_name = db_name or os.getenv('MONGODB_DB', 'sustainatrend')
        self.client = None
        self.db = None
        self.connected = False
        
        # Try to connect to MongoDB
        self.connect()
    
    def connect(self) -> bool:
        """
        Connect to MongoDB.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.client = MongoClient(self.uri)
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            self.connected = True
            logger.info(f"Connected to MongoDB: {self.uri}")
            return True
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"MongoDB connection failed: {str(e)}")
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
        except Exception:
            self.connected = False
            return False
    
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
        
        existing_collections = self.db.list_collection_names()
        for collection in collections:
            if collection not in existing_collections:
                self.db.create_collection(collection)
                logger.info(f"Created collection: {collection}")
    
    # Generic CRUD operations
    
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
        if not collection:
            return None
        
        return collection.find_one(query or {}, projection)
    
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
            Cursor to the documents
        """
        collection = self.get_collection(collection_name)
        if not collection:
            return []
        
        cursor = collection.find(query or {}, projection)
        
        if sort:
            cursor = cursor.sort(sort)
        
        if skip:
            cursor = cursor.skip(skip)
        
        if limit:
            cursor = cursor.limit(limit)
        
        return cursor
    
    def insert_one(self, collection_name: str, document: Dict) -> Optional[str]:
        """
        Insert a document into a collection.
        
        Args:
            collection_name: Name of the collection
            document: Document to insert
            
        Returns:
            ID of the inserted document or None if failed
        """
        collection = self.get_collection(collection_name)
        if not collection:
            return None
        
        result = collection.insert_one(document)
        return str(result.inserted_id) if result.acknowledged else None
    
    def insert_many(self, collection_name: str, documents: List[Dict]) -> Optional[List[str]]:
        """
        Insert multiple documents into a collection.
        
        Args:
            collection_name: Name of the collection
            documents: Documents to insert
            
        Returns:
            List of IDs of the inserted documents or None if failed
        """
        collection = self.get_collection(collection_name)
        if not collection:
            return None
        
        result = collection.insert_many(documents)
        return [str(id) for id in result.inserted_ids] if result.acknowledged else None
    
    def update_one(self, collection_name: str, query: Dict, update: Dict, upsert: bool = False) -> bool:
        """
        Update a document in a collection.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            update: Update operations
            upsert: Whether to insert if not exists
            
        Returns:
            True if successful, False otherwise
        """
        collection = self.get_collection(collection_name)
        if not collection:
            return False
        
        result = collection.update_one(query, update, upsert=upsert)
        return result.acknowledged
    
    def update_many(self, collection_name: str, query: Dict, update: Dict, upsert: bool = False) -> bool:
        """
        Update multiple documents in a collection.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            update: Update operations
            upsert: Whether to insert if not exists
            
        Returns:
            True if successful, False otherwise
        """
        collection = self.get_collection(collection_name)
        if not collection:
            return False
        
        result = collection.update_many(query, update, upsert=upsert)
        return result.acknowledged
    
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
        if not collection:
            return False
        
        result = collection.delete_one(query)
        return result.acknowledged
    
    def delete_many(self, collection_name: str, query: Dict) -> bool:
        """
        Delete multiple documents from a collection.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            
        Returns:
            True if successful, False otherwise
        """
        collection = self.get_collection(collection_name)
        if not collection:
            return False
        
        result = collection.delete_many(query)
        return result.acknowledged
    
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
        if not collection:
            return 0
        
        return collection.count_documents(query or {})
    
    # Domain-specific operations
    
    def get_user(self, email: str) -> Optional[Dict]:
        """
        Get a user by email.
        
        Args:
            email: User email
            
        Returns:
            User document or None if not found
        """
        return self.find_one('users', {'email': email})
    
    def create_user(self, user_data: Dict) -> Optional[str]:
        """
        Create a new user.
        
        Args:
            user_data: User data
            
        Returns:
            User ID or None if failed
        """
        return self.insert_one('users', user_data)
    
    def get_product(self, product_id: str) -> Optional[Dict]:
        """
        Get a product by ID.
        
        Args:
            product_id: Product ID
            
        Returns:
            Product document or None if not found
        """
        return self.find_one('products', {'id': product_id})
    
    def get_resource(self, resource_id: str) -> Optional[Dict]:
        """
        Get a resource by ID.
        
        Args:
            resource_id: Resource ID
            
        Returns:
            Resource document or None if not found
        """
        return self.find_one('resources', {'id': resource_id})
    
    def get_page(self, page_id: str) -> Optional[Dict]:
        """
        Get a page by ID.
        
        Args:
            page_id: Page ID
            
        Returns:
            Page document or None if not found
        """
        return self.find_one('pages', {'id': page_id})
    
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
        stories = list(self.find('stories', filters, limit=limit))
        return stories or []

# Create a singleton instance
mongodb_manager = MongoDBManager()
