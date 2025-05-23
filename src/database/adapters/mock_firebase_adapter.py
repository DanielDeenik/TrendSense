"""
Mock Firebase Adapter

This module provides a mock Firebase adapter that implements the DatabaseAdapter interface.
It uses an in-memory dictionary to simulate Firebase Firestore.
"""

import os
import logging
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime

from .base_adapter import DatabaseAdapter

# Configure logging
logger = logging.getLogger(__name__)


class MockFirebaseAdapter(DatabaseAdapter):
    """Mock Firebase adapter for SustainaTrend."""

    def __init__(self, project_id: str = None):
        """
        Initialize the mock Firebase adapter.

        Args:
            project_id: Firebase project ID
        """
        self.project_id = project_id or os.getenv('FIREBASE_PROJECT_ID', 'sustainatrend-demo')
        self.connected = False
        self.collections = {}
        self.app = None
        self.db = None

    def connect(self) -> bool:
        """
        Connect to the mock Firebase.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.connected = True
            logger.info(f"Connected to mock Firebase Firestore project: {self.project_id}")
            return True
        except Exception as e:
            logger.error(f"Mock Firebase connection failed: {str(e)}")
            self.connected = False
            return False

    def disconnect(self) -> None:
        """Disconnect from the mock Firebase."""
        self.connected = False
        logger.info("Disconnected from mock Firebase")

    def is_connected(self) -> bool:
        """
        Check if connected to the mock Firebase.

        Returns:
            bool: True if connected, False otherwise
        """
        return self.connected

    def get_collection(self, collection_name: str) -> Any:
        """
        Get a mock Firestore collection.

        Args:
            collection_name: Name of the collection

        Returns:
            Collection object or None if error
        """
        if not self.is_connected():
            logger.error(f"Cannot get collection {collection_name}: Not connected to mock Firebase")
            return None

        # Create collection if it doesn't exist
        if collection_name not in self.collections:
            self.collections[collection_name] = {}

        return self.collections[collection_name]

    def initialize_collections(self, collections: List[str]) -> None:
        """
        Initialize collections if they don't exist.

        Args:
            collections: List of collection names to initialize
        """
        if not self.is_connected():
            if not self.connect():
                logger.error("Cannot initialize collections: Not connected to mock Firebase")
                return

        # Create collections if they don't exist
        for collection_name in collections:
            if collection_name not in self.collections:
                self.collections[collection_name] = {}
                logger.info(f"Created collection: {collection_name}")

    def find_one(self, collection_name: str, query: Dict = None, projection: Dict = None) -> Optional[Dict]:
        """
        Find a single document in a collection.

        Args:
            collection_name: Name of the collection
            query: Query filter
            projection: Fields to include/exclude (not supported in mock)

        Returns:
            Document or None if not found
        """
        collection = self.get_collection(collection_name)
        if collection is None:
            return None

        query = query or {}
        try:
            # If querying by ID, get the document directly
            if '_id' in query:
                doc_id = str(query['_id'])
                if doc_id in collection:
                    return collection[doc_id]
                return None

            # Otherwise, find the first document that matches all query criteria
            for doc_id, doc in collection.items():
                matches = True
                for field, value in query.items():
                    if field not in doc or doc[field] != value:
                        matches = False
                        break
                if matches:
                    return doc

            return None
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
            projection: Fields to include/exclude (not supported in mock)
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
            # Find all documents that match the query
            results = []
            for doc_id, doc in collection.items():
                matches = True
                for field, value in query.items():
                    if field != '_id' and (field not in doc or doc[field] != value):
                        matches = False
                        break
                if matches:
                    results.append(doc)

            # Apply sort if provided
            if sort:
                for sort_field, sort_dir in sort:
                    reverse = sort_dir == -1
                    results.sort(key=lambda x: x.get(sort_field), reverse=reverse)

            # Apply skip and limit
            if skip > 0:
                results = results[skip:]
            if limit > 0:
                results = results[:limit]

            return results
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
            # Generate ID if not provided
            doc_id = str(document.get('_id', str(uuid.uuid4())))

            # Create a copy of the document
            doc = document.copy()

            # Add ID field
            doc['_id'] = doc_id

            # Add timestamps
            if 'created_at' not in doc:
                doc['created_at'] = datetime.now().isoformat()
            if 'updated_at' not in doc:
                doc['updated_at'] = datetime.now().isoformat()

            # Insert document
            collection[doc_id] = doc
            return doc_id
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
            doc_ids = []
            for document in documents:
                doc_id = self.insert_one(collection_name, document)
                if doc_id:
                    doc_ids.append(doc_id)
            return doc_ids
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
            # Find document to update
            doc = None
            doc_id = None

            if '_id' in query:
                doc_id = str(query['_id'])
                if doc_id in collection:
                    doc = collection[doc_id]
            else:
                # Find the first document that matches all query criteria
                for id, document in collection.items():
                    matches = True
                    for field, value in query.items():
                        if field not in document or document[field] != value:
                            matches = False
                            break
                    if matches:
                        doc = document
                        doc_id = id
                        break

            if doc:
                # Extract update data
                update_data = {}
                if '$set' in update:
                    update_data.update(update['$set'])
                else:
                    update_data.update(update)

                # Add updated_at timestamp
                update_data['updated_at'] = datetime.now().isoformat()

                # Update document
                doc.update(update_data)
                return True
            elif upsert:
                # Create new document
                doc_id = str(query.get('_id', str(uuid.uuid4())))

                # Prepare document data
                doc_data = {}
                doc_data.update(query)  # Include query fields
                if '$set' in update:
                    doc_data.update(update['$set'])
                else:
                    doc_data.update(update)

                # Add timestamps
                doc_data['created_at'] = datetime.now().isoformat()
                doc_data['updated_at'] = datetime.now().isoformat()
                doc_data['_id'] = doc_id

                # Insert document
                collection[doc_id] = doc_data
                return True
            else:
                return False
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
            # Find documents to update
            doc_ids = []
            for doc_id, doc in collection.items():
                matches = True
                for field, value in query.items():
                    if field != '_id' and (field not in doc or doc[field] != value):
                        matches = False
                        break
                if matches:
                    doc_ids.append(doc_id)

            # Extract update data
            update_data = {}
            if '$set' in update:
                update_data.update(update['$set'])
            else:
                update_data.update(update)

            # Add updated_at timestamp
            update_data['updated_at'] = datetime.now().isoformat()

            # Update documents
            count = 0
            for doc_id in doc_ids:
                collection[doc_id].update(update_data)
                count += 1

            return count
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
            # Find document to delete
            if '_id' in query:
                doc_id = str(query['_id'])
                if doc_id in collection:
                    del collection[doc_id]
                    return True
                return False
            else:
                # Find the first document that matches all query criteria
                for doc_id, doc in collection.items():
                    matches = True
                    for field, value in query.items():
                        if field not in doc or doc[field] != value:
                            matches = False
                            break
                    if matches:
                        del collection[doc_id]
                        return True
                return False
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
            # Find documents to delete
            doc_ids = []
            for doc_id, doc in collection.items():
                matches = True
                for field, value in query.items():
                    if field != '_id' and (field not in doc or doc[field] != value):
                        matches = False
                        break
                if matches:
                    doc_ids.append(doc_id)

            # Delete documents
            count = 0
            for doc_id in doc_ids:
                del collection[doc_id]
                count += 1

            return count
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
        docs = self.find(collection_name, query)
        return len(docs)

    def aggregate(self, collection_name: str, pipeline: List[Dict]) -> List[Dict]:
        """
        Perform an aggregation pipeline on a collection.

        Args:
            collection_name: Name of the collection
            pipeline: Aggregation pipeline

        Returns:
            List of documents
        """
        logger.warning("Mock Firebase does not support aggregation pipelines. Implementing basic functionality.")
        
        # Basic implementation of simple aggregation operations
        collection = self.get_collection(collection_name)
        if collection is None:
            return []

        try:
            # Start with all documents in the collection
            results = [doc for doc in collection.values()]
            
            # Process each stage in the pipeline
            for stage in pipeline:
                # Handle $match stage (basic filtering)
                if '$match' in stage:
                    match_criteria = stage['$match']
                    filtered_results = []
                    
                    for doc in results:
                        matches = True
                        for field, value in match_criteria.items():
                            if isinstance(value, dict):
                                # Handle operators like $gt, $lt, etc.
                                for op, op_value in value.items():
                                    if op == '$gt' and not (field in doc and doc[field] > op_value):
                                        matches = False
                                    elif op == '$gte' and not (field in doc and doc[field] >= op_value):
                                        matches = False
                                    elif op == '$lt' and not (field in doc and doc[field] < op_value):
                                        matches = False
                                    elif op == '$lte' and not (field in doc and doc[field] <= op_value):
                                        matches = False
                                    elif op == '$ne' and not (field in doc and doc[field] != op_value):
                                        matches = False
                            elif field not in doc or doc[field] != value:
                                matches = False
                                break
                        
                        if matches:
                            filtered_results.append(doc)
                    
                    results = filtered_results
                
                # Handle $sort stage
                elif '$sort' in stage:
                    sort_criteria = stage['$sort']
                    for field, direction in sort_criteria.items():
                        reverse = direction == -1
                        results.sort(key=lambda x: x.get(field), reverse=reverse)
                
                # Handle $limit stage
                elif '$limit' in stage:
                    limit = stage['$limit']
                    results = results[:limit]
                
                # Handle $skip stage
                elif '$skip' in stage:
                    skip = stage['$skip']
                    results = results[skip:]
                
                # Handle $project stage (basic field selection)
                elif '$project' in stage:
                    project = stage['$project']
                    projected_results = []
                    
                    for doc in results:
                        projected_doc = {}
                        for field, include in project.items():
                            if include == 1 and field in doc:
                                projected_doc[field] = doc[field]
                        projected_results.append(projected_doc)
                    
                    results = projected_results
                
                # Unsupported stages
                else:
                    logger.warning(f"Unsupported aggregation stage: {stage}")
            
            return results
        except Exception as e:
            logger.error(f"Error performing aggregation on {collection_name}: {str(e)}")
            return []

    # Common utility methods for SustainaTrend
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
