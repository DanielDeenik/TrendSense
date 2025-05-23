"""
Firebase Adapter

This module provides a Firebase adapter that implements the DatabaseAdapter interface.
It uses Firebase Firestore as a free alternative to MongoDB.
"""

import os
import logging
import json
import uuid
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

# Firebase imports
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_AVAILABLE = True
    logger.info("Firebase packages successfully imported")
except ImportError as e:
    logger.error(f"Error importing Firebase packages: {str(e)}")
    FIREBASE_AVAILABLE = False

from .base_adapter import DatabaseAdapter


class FirebaseAdapter(DatabaseAdapter):
    """Firebase adapter for TrendSense."""

    def __init__(self, credentials_path: str = None, project_id: str = None):
        """
        Initialize the Firebase adapter.

        Args:
            credentials_path: Path to Firebase credentials JSON file
            project_id: Firebase project ID
        """
        if not FIREBASE_AVAILABLE:
            logger.error("Firebase packages not installed. Run 'pip install firebase-admin'")
            self.connected = False
            return

        # Get Firebase configuration from environment or use defaults
        self.credentials_path = credentials_path or os.getenv('FIREBASE_CREDENTIALS_PATH')
        self.project_id = project_id or os.getenv('FIREBASE_PROJECT_ID')

        # Initialize client and database
        self.app = None
        self.db = None
        self.connected = False
        self.collections_cache = {}
        self._using_mock = False

    def connect(self) -> bool:
        """
        Connect to Firebase.

        Returns:
            bool: True if connection successful, False otherwise
        """
        if not FIREBASE_AVAILABLE:
            logger.error("Firebase packages not installed. Run 'pip install firebase-admin'")
            return False

        try:
            # Check if Firebase app is already initialized
            try:
                self.app = firebase_admin.get_app()
                logger.info("Using existing Firebase app")
            except ValueError:
                # Initialize Firebase app
                if self.credentials_path:
                    logger.info(f"Initializing Firebase app with credentials from {self.credentials_path}")
                    try:
                        # Check if credentials file exists
                        if not os.path.exists(self.credentials_path):
                            logger.error(f"Credentials file not found: {self.credentials_path}")
                            # Fall back to mock Firebase adapter
                            logger.info("Falling back to mock Firebase adapter")
                            from .mock_firebase_adapter import MockFirebaseAdapter
                            mock_adapter = MockFirebaseAdapter(self.project_id)
                            mock_adapter.connect()
                            self.app = None
                            self.db = mock_adapter
                            self.connected = True
                            self._using_mock = True
                            logger.info(f"Connected to mock Firebase Firestore project: {self.project_id}")
                            return True
                        else:
                            # Use service account credentials
                            try:
                                cred = credentials.Certificate(self.credentials_path)
                                self.app = firebase_admin.initialize_app(cred)
                            except Exception as e:
                                logger.error(f"Error initializing Firebase app with credentials: {str(e)}")
                                # Fall back to mock Firebase adapter
                                logger.info("Falling back to mock Firebase adapter")
                                from .mock_firebase_adapter import MockFirebaseAdapter
                                mock_adapter = MockFirebaseAdapter(self.project_id)
                                mock_adapter.connect()
                                self.app = None
                                self.db = mock_adapter
                                self.connected = True
                                self._using_mock = True
                                logger.info(f"Connected to mock Firebase Firestore project: {self.project_id}")
                                return True
                    except Exception as e:
                        logger.error(f"Error initializing Firebase app with credentials: {str(e)}")
                        # Fall back to mock Firebase adapter
                        logger.info("Falling back to mock Firebase adapter")
                        from .mock_firebase_adapter import MockFirebaseAdapter
                        mock_adapter = MockFirebaseAdapter(self.project_id)
                        mock_adapter.connect()
                        self.app = None
                        self.db = mock_adapter
                        self.connected = True
                        self._using_mock = True
                        logger.info(f"Connected to mock Firebase Firestore project: {self.project_id}")
                        return True
                else:
                    # Fall back to mock Firebase adapter
                    logger.info("No credentials provided, falling back to mock Firebase adapter")
                    from .mock_firebase_adapter import MockFirebaseAdapter
                    mock_adapter = MockFirebaseAdapter(self.project_id)
                    mock_adapter.connect()
                    self.app = None
                    self.db = mock_adapter
                    self.connected = True
                    self._using_mock = True
                    logger.info(f"Connected to mock Firebase Firestore project: {self.project_id}")
                    return True

            # Initialize Firestore client
            try:
                self.db = firestore.client()
                self.connected = True
                self._using_mock = False
                logger.info(f"Connected to Firebase Firestore project: {self.project_id}")
                return True
            except Exception as e:
                logger.error(f"Error initializing Firestore client: {str(e)}")
                # Fall back to mock Firebase adapter
                logger.info("Falling back to mock Firebase adapter")
                from .mock_firebase_adapter import MockFirebaseAdapter
                mock_adapter = MockFirebaseAdapter(self.project_id)
                mock_adapter.connect()
                self.app = None
                self.db = mock_adapter
                self.connected = True
                self._using_mock = True
                logger.info(f"Connected to mock Firebase Firestore project: {self.project_id}")
                return True
        except Exception as e:
            logger.error(f"Firebase connection failed: {str(e)}")
            logger.error(f"Error details: {type(e).__name__}")
            # Fall back to mock Firebase adapter
            logger.info("Falling back to mock Firebase adapter")
            from .mock_firebase_adapter import MockFirebaseAdapter
            mock_adapter = MockFirebaseAdapter(self.project_id)
            mock_adapter.connect()
            self.app = None
            self.db = mock_adapter
            self.connected = True
            self._using_mock = True
            logger.info(f"Connected to mock Firebase Firestore project: {self.project_id}")
            return True

    def disconnect(self) -> None:
        """Disconnect from Firebase."""
        if self.app:
            try:
                firebase_admin.delete_app(self.app)
                self.app = None
                self.db = None
                self.connected = False
                logger.info("Disconnected from Firebase")
            except Exception as e:
                logger.error(f"Error disconnecting from Firebase: {str(e)}")

    def is_connected(self) -> bool:
        """
        Check if connected to Firebase.

        Returns:
            bool: True if connected, False otherwise
        """
        return self.connected and self.db is not None

    def get_collection(self, collection_name: str) -> Any:
        """
        Get a Firestore collection.

        Args:
            collection_name: Name of the collection

        Returns:
            Collection object or None if error
        """
        if not self.is_connected():
            logger.error(f"Cannot get collection {collection_name}: Not connected to Firebase")
            return None

        # If using mock adapter, delegate to it
        if self._using_mock:
            return self.db.get_collection(collection_name)

        # Cache collection reference
        if collection_name not in self.collections_cache:
            self.collections_cache[collection_name] = self.db.collection(collection_name)

        return self.collections_cache[collection_name]

    def initialize_collections(self, collections: List[str]) -> None:
        """
        Initialize collections if they don't exist.

        Args:
            collections: List of collection names to initialize
        """
        if not self.is_connected():
            if not self.connect():
                logger.error("Cannot initialize collections: Not connected to Firebase")
                return

        # If using mock adapter, delegate to it
        if self._using_mock:
            self.db.initialize_collections(collections)
            return

        # In Firestore, collections are created implicitly when documents are added
        # We'll just log the collections we're planning to use
        logger.info(f"Firestore collections will be created as needed: {', '.join(collections)}")

    def _convert_to_firestore(self, data: Dict) -> Dict:
        """
        Convert MongoDB-style data to Firestore-compatible format.

        Args:
            data: MongoDB-style document

        Returns:
            Firestore-compatible document
        """
        if not data:
            return {}

        result = {}
        for key, value in data.items():
            # Handle MongoDB ObjectId
            if key == '_id':
                result['id'] = str(value)
            # Handle nested dictionaries
            elif isinstance(value, dict):
                result[key] = self._convert_to_firestore(value)
            # Handle lists of dictionaries
            elif isinstance(value, list) and all(isinstance(item, dict) for item in value):
                result[key] = [self._convert_to_firestore(item) for item in value]
            # Handle other types
            else:
                result[key] = value

        return result

    def _convert_from_firestore(self, doc_snapshot) -> Dict:
        """
        Convert Firestore document to MongoDB-style format.

        Args:
            doc_snapshot: Firestore document snapshot

        Returns:
            MongoDB-style document
        """
        if not doc_snapshot:
            return {}

        data = doc_snapshot.to_dict()
        if not data:
            return {}

        # Add document ID as _id field to match MongoDB format
        data['_id'] = doc_snapshot.id

        return data

    def find_one(self, collection_name: str, query: Dict = None, projection: Dict = None) -> Optional[Dict]:
        """
        Find a single document in a collection.

        Args:
            collection_name: Name of the collection
            query: Query filter
            projection: Fields to include/exclude (not fully supported in Firestore)

        Returns:
            Document or None if not found
        """
        # If using mock adapter, delegate to it
        if self._using_mock:
            return self.db.find_one(collection_name, query, projection)

        collection = self.get_collection(collection_name)
        if collection is None:
            return None

        query = query or {}
        try:
            # Build query
            ref = collection
            for field, value in query.items():
                if field == '_id':
                    # If querying by ID, get the document directly
                    doc = collection.document(str(value)).get()
                    return self._convert_from_firestore(doc) if doc.exists else None
                else:
                    ref = ref.where(field, '==', value)

            # Execute query and get first result
            docs = ref.limit(1).get()
            for doc in docs:
                return self._convert_from_firestore(doc)

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
            projection: Fields to include/exclude (not fully supported in Firestore)
            sort: Sort specification
            limit: Maximum number of documents to return
            skip: Number of documents to skip (not directly supported in Firestore)

        Returns:
            List of documents
        """
        # If using mock adapter, delegate to it
        if self._using_mock:
            return self.db.find(collection_name, query, projection, sort, limit, skip)

        collection = self.get_collection(collection_name)
        if collection is None:
            return []

        query = query or {}
        try:
            # Build query
            ref = collection
            for field, value in query.items():
                if field != '_id':  # Skip _id field as it's handled differently
                    ref = ref.where(field, '==', value)

            # Apply sort if provided
            if sort:
                for sort_field, sort_dir in sort:
                    direction = firestore.Query.DESCENDING if sort_dir == -1 else firestore.Query.ASCENDING
                    ref = ref.order_by(sort_field, direction=direction)

            # Apply limit if provided
            if limit > 0:
                ref = ref.limit(limit)

            # Execute query
            docs = ref.get()

            # Convert to list of dictionaries
            results = [self._convert_from_firestore(doc) for doc in docs]

            # Apply skip manually (Firestore doesn't support skip directly)
            if skip > 0:
                results = results[skip:]

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
        # If using mock adapter, delegate to it
        if self._using_mock:
            return self.db.insert_one(collection_name, document)

        collection = self.get_collection(collection_name)
        if collection is None:
            return None

        try:
            # Convert document to Firestore format
            firestore_doc = self._convert_to_firestore(document)

            # Generate ID if not provided
            doc_id = str(document.get('_id', str(uuid.uuid4())))

            # Add timestamps
            if 'created_at' not in firestore_doc:
                firestore_doc['created_at'] = datetime.now()
            if 'updated_at' not in firestore_doc:
                firestore_doc['updated_at'] = datetime.now()

            # Insert document
            collection.document(doc_id).set(firestore_doc)
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
        # If using mock adapter, delegate to it
        if self._using_mock:
            return self.db.insert_many(collection_name, documents)

        collection = self.get_collection(collection_name)
        if collection is None:
            return []

        try:
            batch = self.db.batch()
            doc_ids = []

            for document in documents:
                # Convert document to Firestore format
                firestore_doc = self._convert_to_firestore(document)

                # Generate ID if not provided
                doc_id = str(document.get('_id', str(uuid.uuid4())))
                doc_ids.append(doc_id)

                # Add timestamps
                if 'created_at' not in firestore_doc:
                    firestore_doc['created_at'] = datetime.now()
                if 'updated_at' not in firestore_doc:
                    firestore_doc['updated_at'] = datetime.now()

                # Add to batch
                doc_ref = collection.document(doc_id)
                batch.set(doc_ref, firestore_doc)

            # Commit batch
            batch.commit()
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
        # If using mock adapter, delegate to it
        if self._using_mock:
            return self.db.update_one(collection_name, query, update, upsert)

        collection = self.get_collection(collection_name)
        if collection is None:
            return False

        try:
            # Find document to update
            doc = None
            if '_id' in query:
                doc_id = str(query['_id'])
                doc_ref = collection.document(doc_id)
                doc = doc_ref.get()
            else:
                # Build query to find document
                ref = collection
                for field, value in query.items():
                    ref = ref.where(field, '==', value)
                docs = ref.limit(1).get()
                for d in docs:
                    doc = d
                    doc_ref = collection.document(doc.id)
                    break

            if doc and doc.exists:
                # Extract update data
                update_data = {}
                if '$set' in update:
                    update_data.update(update['$set'])
                else:
                    update_data.update(update)

                # Add updated_at timestamp
                update_data['updated_at'] = datetime.now()

                # Update document
                doc_ref.update(update_data)
                return True
            elif upsert:
                # Create new document
                doc_id = str(query.get('_id', str(uuid.uuid4())))
                doc_ref = collection.document(doc_id)

                # Prepare document data
                doc_data = {}
                doc_data.update(query)  # Include query fields
                if '$set' in update:
                    doc_data.update(update['$set'])
                else:
                    doc_data.update(update)

                # Add timestamps
                doc_data['created_at'] = datetime.now()
                doc_data['updated_at'] = datetime.now()

                # Insert document
                doc_ref.set(doc_data)
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
        # If using mock adapter, delegate to it
        if self._using_mock:
            return self.db.update_many(collection_name, query, update, upsert)

        collection = self.get_collection(collection_name)
        if collection is None:
            return 0

        try:
            # Find documents to update
            ref = collection
            for field, value in query.items():
                if field != '_id':  # Skip _id field as it's handled differently
                    ref = ref.where(field, '==', value)
            docs = ref.get()

            # Extract update data
            update_data = {}
            if '$set' in update:
                update_data.update(update['$set'])
            else:
                update_data.update(update)

            # Add updated_at timestamp
            update_data['updated_at'] = datetime.now()

            # Update documents in batch
            batch = self.db.batch()
            count = 0
            for doc in docs:
                doc_ref = collection.document(doc.id)
                batch.update(doc_ref, update_data)
                count += 1

            # Commit batch if there are documents to update
            if count > 0:
                batch.commit()

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
        # If using mock adapter, delegate to it
        if self._using_mock:
            return self.db.delete_one(collection_name, query)

        collection = self.get_collection(collection_name)
        if collection is None:
            return False

        try:
            # Find document to delete
            if '_id' in query:
                doc_id = str(query['_id'])
                doc_ref = collection.document(doc_id)
                doc = doc_ref.get()
                if doc.exists:
                    doc_ref.delete()
                    return True
                return False
            else:
                # Build query to find document
                ref = collection
                for field, value in query.items():
                    ref = ref.where(field, '==', value)
                docs = ref.limit(1).get()
                for doc in docs:
                    collection.document(doc.id).delete()
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
        # If using mock adapter, delegate to it
        if self._using_mock:
            return self.db.delete_many(collection_name, query)

        collection = self.get_collection(collection_name)
        if collection is None:
            return 0

        try:
            # Find documents to delete
            ref = collection
            for field, value in query.items():
                if field != '_id':  # Skip _id field as it's handled differently
                    ref = ref.where(field, '==', value)
            docs = ref.get()

            # Delete documents in batch
            batch = self.db.batch()
            count = 0
            for doc in docs:
                doc_ref = collection.document(doc.id)
                batch.delete(doc_ref)
                count += 1

            # Commit batch if there are documents to delete
            if count > 0:
                batch.commit()

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
        # If using mock adapter, delegate to it
        if self._using_mock:
            return self.db.count_documents(collection_name, query)

        # Firestore doesn't have a direct count method, so we need to fetch all documents
        # This is not efficient for large collections
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
        # If using mock adapter, delegate to it
        if self._using_mock:
            return self.db.aggregate(collection_name, pipeline)

        logger.warning("Firestore does not support MongoDB-style aggregation pipelines. Implementing basic functionality.")

        # Basic implementation of simple aggregation operations
        collection = self.get_collection(collection_name)
        if collection is None:
            return []

        try:
            results = []

            # Process each stage in the pipeline
            for stage in pipeline:
                # Handle $match stage (basic filtering)
                if '$match' in stage:
                    match_criteria = stage['$match']
                    ref = collection

                    for field, value in match_criteria.items():
                        if isinstance(value, dict):
                            # Handle operators like $gt, $lt, etc.
                            for op, op_value in value.items():
                                if op == '$gt':
                                    ref = ref.where(field, '>', op_value)
                                elif op == '$gte':
                                    ref = ref.where(field, '>=', op_value)
                                elif op == '$lt':
                                    ref = ref.where(field, '<', op_value)
                                elif op == '$lte':
                                    ref = ref.where(field, '<=', op_value)
                                elif op == '$ne':
                                    ref = ref.where(field, '!=', op_value)
                        else:
                            ref = ref.where(field, '==', value)

                    docs = ref.get()
                    results = [self._convert_from_firestore(doc) for doc in docs]

                # Handle $sort stage
                elif '$sort' in stage:
                    sort_criteria = stage['$sort']
                    field = list(sort_criteria.keys())[0]
                    direction = firestore.Query.DESCENDING if sort_criteria[field] == -1 else firestore.Query.ASCENDING

                    ref = collection.order_by(field, direction=direction)
                    docs = ref.get()
                    results = [self._convert_from_firestore(doc) for doc in docs]

                # Handle $limit stage
                elif '$limit' in stage:
                    limit = stage['$limit']
                    ref = collection.limit(limit)
                    docs = ref.get()
                    results = [self._convert_from_firestore(doc) for doc in docs]

                # Handle $skip stage
                elif '$skip' in stage:
                    skip = stage['$skip']
                    # Firestore doesn't support skip directly, so we need to fetch all and skip manually
                    docs = collection.get()
                    all_docs = [self._convert_from_firestore(doc) for doc in docs]
                    results = all_docs[skip:]

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
