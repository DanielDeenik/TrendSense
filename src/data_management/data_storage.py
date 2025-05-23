"""
Data Storage

This module provides classes and functions for storing data in the database.
"""

import logging
import uuid
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

# Import database adapters
from src.database.adapters import get_database_adapter, DatabaseAdapter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataStorage:
    """Class for storing data in the database."""
    
    def __init__(self, db_adapter: Optional[DatabaseAdapter] = None):
        """
        Initialize the data storage.
        
        Args:
            db_adapter: Database adapter for storage
        """
        self.db_adapter = db_adapter or get_database_adapter()
        
        # Connect to the database
        if not self.db_adapter.is_connected():
            self.db_adapter.connect()
    
    def store_data(self, data: Any, collection_name: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Store data in the database.
        
        Args:
            data: Data to store
            collection_name: Name of the collection
            options: Additional options for storage
            
        Returns:
            Storage result
        """
        options = options or {}
        
        try:
            # If data is a list of dictionaries
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                # Add metadata to each item
                for item in data:
                    if '_id' not in item:
                        item['_id'] = str(uuid.uuid4())
                    if 'created_at' not in item:
                        item['created_at'] = datetime.now().isoformat()
                    if 'updated_at' not in item:
                        item['updated_at'] = datetime.now().isoformat()
                
                # Insert many documents
                result = self.db_adapter.insert_many(collection_name, data)
                
                return {
                    'success': True,
                    'inserted_count': len(result) if result else 0,
                    'inserted_ids': result if result else []
                }
            
            # If data is a dictionary
            elif isinstance(data, dict):
                # Add metadata
                if '_id' not in data:
                    data['_id'] = str(uuid.uuid4())
                if 'created_at' not in data:
                    data['created_at'] = datetime.now().isoformat()
                if 'updated_at' not in data:
                    data['updated_at'] = datetime.now().isoformat()
                
                # Insert one document
                result = self.db_adapter.insert_one(collection_name, data)
                
                return {
                    'success': True,
                    'inserted_id': result
                }
            
            # Return error for other types
            return {
                'success': False,
                'error': f"Unsupported data type for storage: {type(data)}"
            }
        
        except Exception as e:
            logger.error(f"Error storing data: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_data(self, collection_name: str, document_id: str, 
                   update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a document in the database.
        
        Args:
            collection_name: Name of the collection
            document_id: ID of the document to update
            update_data: Data to update
            
        Returns:
            Update result
        """
        try:
            # Add updated_at timestamp
            update_data['updated_at'] = datetime.now().isoformat()
            
            # Update the document
            result = self.db_adapter.update_one(
                collection_name,
                {'_id': document_id},
                {'$set': update_data}
            )
            
            return {
                'success': True,
                'updated': result
            }
        
        except Exception as e:
            logger.error(f"Error updating data: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_data(self, collection_name: str, document_id: str) -> Dict[str, Any]:
        """
        Delete a document from the database.
        
        Args:
            collection_name: Name of the collection
            document_id: ID of the document to delete
            
        Returns:
            Delete result
        """
        try:
            # Delete the document
            result = self.db_adapter.delete_one(
                collection_name,
                {'_id': document_id}
            )
            
            return {
                'success': True,
                'deleted': result
            }
        
        except Exception as e:
            logger.error(f"Error deleting data: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_data(self, collection_name: str, query: Dict[str, Any] = None,
                limit: int = 0, skip: int = 0, sort: List = None) -> List[Dict[str, Any]]:
        """
        Get data from the database.
        
        Args:
            collection_name: Name of the collection
            query: Query to filter the data
            limit: Maximum number of documents to return
            skip: Number of documents to skip
            sort: List of (field, direction) tuples to sort by
            
        Returns:
            List of documents
        """
        try:
            # Query the database
            return self.db_adapter.find(collection_name, query=query, limit=limit, skip=skip, sort=sort)
        except Exception as e:
            logger.error(f"Error getting data: {str(e)}")
            return []
    
    def get_data_by_id(self, collection_name: str, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a document by ID.
        
        Args:
            collection_name: Name of the collection
            document_id: ID of the document
            
        Returns:
            Document or None if not found
        """
        try:
            # Query the database
            return self.db_adapter.find_one(collection_name, {'_id': document_id})
        except Exception as e:
            logger.error(f"Error getting document by ID: {str(e)}")
            return None
    
    def get_aggregated_data(self, collection_name: str, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Get aggregated data from the database.
        
        Args:
            collection_name: Name of the collection
            pipeline: Aggregation pipeline
            
        Returns:
            List of aggregated documents
        """
        try:
            # Query the database
            return self.db_adapter.aggregate(collection_name, pipeline)
        except Exception as e:
            logger.error(f"Error getting aggregated data: {str(e)}")
            return []

# Create a singleton instance
data_storage = None

def get_data_storage(db_adapter=None):
    """
    Get the data storage singleton instance.
    
    Args:
        db_adapter: Database adapter for storage
        
    Returns:
        Data storage instance
    """
    global data_storage
    
    if data_storage is None:
        data_storage = DataStorage(db_adapter)
    
    return data_storage
