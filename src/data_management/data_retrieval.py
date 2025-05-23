"""
Data Retrieval

This module provides classes and functions for retrieving data from the database for display in the application.
"""

import logging
from typing import Dict, List, Any, Optional, Union, Tuple
import json

# Import database adapters
from src.database.adapters import get_database_adapter, DatabaseAdapter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataRetrieval:
    """Class for retrieving data from the database for display in the application."""
    
    def __init__(self, db_adapter: Optional[DatabaseAdapter] = None):
        """
        Initialize the data retrieval.
        
        Args:
            db_adapter: Database adapter for retrieval
        """
        self.db_adapter = db_adapter or get_database_adapter()
        
        # Connect to the database
        if not self.db_adapter.is_connected():
            self.db_adapter.connect()
    
    def get_data_for_display(self, collection_name: str, query: Dict[str, Any] = None,
                            limit: int = 0, skip: int = 0, sort: List[Tuple[str, int]] = None) -> List[Dict[str, Any]]:
        """
        Get data from the database for display in the application.
        
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
            logger.error(f"Error getting data for display: {str(e)}")
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
    
    def get_data_for_chart(self, collection_name: str, query: Dict[str, Any] = None,
                          x_field: str = None, y_field: str = None, 
                          group_by: str = None) -> Dict[str, Any]:
        """
        Get data from the database formatted for charts.
        
        Args:
            collection_name: Name of the collection
            query: Query to filter the data
            x_field: Field to use for x-axis
            y_field: Field to use for y-axis
            group_by: Field to group by for multiple series
            
        Returns:
            Chart data
        """
        try:
            # Query the database
            data = self.db_adapter.find(collection_name, query=query)
            
            if not data:
                return {
                    'labels': [],
                    'datasets': []
                }
            
            # If x_field and y_field are provided, format for a chart
            if x_field and y_field:
                # If group_by is provided, create multiple datasets
                if group_by:
                    # Group data by the group_by field
                    grouped_data = {}
                    for item in data:
                        group = item.get(group_by)
                        if group not in grouped_data:
                            grouped_data[group] = []
                        grouped_data[group].append(item)
                    
                    # Create datasets for each group
                    labels = sorted(list(set(item.get(x_field) for item in data if x_field in item)))
                    datasets = []
                    
                    for group, group_data in grouped_data.items():
                        # Create a dataset for this group
                        dataset = {
                            'label': group,
                            'data': []
                        }
                        
                        # Create a map of x_field to y_field for this group
                        data_map = {item.get(x_field): item.get(y_field) for item in group_data if x_field in item and y_field in item}
                        
                        # Add data points in the order of labels
                        for label in labels:
                            dataset['data'].append(data_map.get(label, 0))
                        
                        datasets.append(dataset)
                    
                    return {
                        'labels': labels,
                        'datasets': datasets
                    }
                
                # Otherwise, create a single dataset
                else:
                    labels = [item.get(x_field) for item in data if x_field in item]
                    values = [item.get(y_field) for item in data if y_field in item]
                    
                    return {
                        'labels': labels,
                        'datasets': [{
                            'label': y_field,
                            'data': values
                        }]
                    }
            
            # Otherwise, return the raw data
            return {
                'data': data
            }
        
        except Exception as e:
            logger.error(f"Error getting data for chart: {str(e)}")
            return {
                'labels': [],
                'datasets': []
            }
    
    def get_data_for_table(self, collection_name: str, query: Dict[str, Any] = None,
                          fields: List[str] = None, limit: int = 0) -> Dict[str, Any]:
        """
        Get data from the database formatted for tables.
        
        Args:
            collection_name: Name of the collection
            query: Query to filter the data
            fields: Fields to include in the table
            limit: Maximum number of documents to return
            
        Returns:
            Table data
        """
        try:
            # Query the database
            data = self.db_adapter.find(collection_name, query=query, limit=limit)
            
            if not data:
                return {
                    'headers': [],
                    'rows': []
                }
            
            # If fields are provided, filter the data
            if fields:
                filtered_data = []
                for item in data:
                    filtered_item = {}
                    for field in fields:
                        if field in item:
                            filtered_item[field] = item[field]
                    filtered_data.append(filtered_item)
                data = filtered_data
            
            # Get headers from the first item
            headers = list(data[0].keys()) if data else []
            
            # Create rows
            rows = []
            for item in data:
                row = []
                for header in headers:
                    row.append(item.get(header, ''))
                rows.append(row)
            
            return {
                'headers': headers,
                'rows': rows
            }
        
        except Exception as e:
            logger.error(f"Error getting data for table: {str(e)}")
            return {
                'headers': [],
                'rows': []
            }
    
    def search_data(self, collection_name: str, search_text: str, 
                   fields: List[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for data in the database.
        
        Args:
            collection_name: Name of the collection
            search_text: Text to search for
            fields: Fields to search in
            limit: Maximum number of documents to return
            
        Returns:
            List of matching documents
        """
        try:
            # Create a query for text search
            query = {}
            
            # If fields are provided, search in those fields
            if fields:
                query['$or'] = []
                for field in fields:
                    query['$or'].append({field: {'$regex': search_text, '$options': 'i'}})
            # Otherwise, use text search if available
            else:
                query['$text'] = {'$search': search_text}
            
            # Query the database
            return self.db_adapter.find(collection_name, query=query, limit=limit)
        
        except Exception as e:
            logger.error(f"Error searching data: {str(e)}")
            return []

# Create a singleton instance
data_retrieval = None

def get_data_retrieval(db_adapter=None):
    """
    Get the data retrieval singleton instance.
    
    Args:
        db_adapter: Database adapter for retrieval
        
    Returns:
        Data retrieval instance
    """
    global data_retrieval
    
    if data_retrieval is None:
        data_retrieval = DataRetrieval(db_adapter)
    
    return data_retrieval
