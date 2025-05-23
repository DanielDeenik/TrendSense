"""
Data Source Connector

This module provides interfaces and implementations for connecting to various data sources.
"""

import os
import logging
import json
import pandas as pd
from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataSourceConnector(ABC):
    """Abstract base class for data source connectors."""
    
    @abstractmethod
    def read_data(self, source_path: str, options: Dict[str, Any] = None) -> Any:
        """
        Read data from the source.
        
        Args:
            source_path: Path or URL to the data source
            options: Additional options for reading
            
        Returns:
            Data from the source
        """
        pass

class JSONConnector(DataSourceConnector):
    """Connector for JSON data sources."""
    
    def read_data(self, source_path: str, options: Dict[str, Any] = None) -> Any:
        """
        Read data from a JSON file or string.
        
        Args:
            source_path: Path to the JSON file or JSON string
            options: Additional options for reading
            
        Returns:
            Parsed JSON data
        """
        options = options or {}
        
        try:
            # Check if source_path is a file path or a JSON string
            if os.path.exists(source_path):
                # Read from file
                with open(source_path, 'r', encoding=options.get('encoding', 'utf-8')) as f:
                    return json.load(f)
            else:
                # Try to parse as JSON string
                return json.loads(source_path)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error reading JSON data: {str(e)}")
            raise

class CSVConnector(DataSourceConnector):
    """Connector for CSV data sources."""
    
    def read_data(self, source_path: str, options: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Read data from a CSV file.
        
        Args:
            source_path: Path to the CSV file
            options: Additional options for reading
            
        Returns:
            List of dictionaries with the CSV data
        """
        options = options or {}
        
        try:
            # Read CSV file
            df = pd.read_csv(
                source_path,
                encoding=options.get('encoding', 'utf-8'),
                sep=options.get('separator', ','),
                header=options.get('header', 0),
                index_col=options.get('index_col', None)
            )
            
            # Convert DataFrame to list of dictionaries
            return df.to_dict('records')
        except Exception as e:
            logger.error(f"Error reading CSV data: {str(e)}")
            raise

class ExcelConnector(DataSourceConnector):
    """Connector for Excel data sources."""
    
    def read_data(self, source_path: str, options: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Read data from an Excel file.
        
        Args:
            source_path: Path to the Excel file
            options: Additional options for reading
            
        Returns:
            List of dictionaries with the Excel data
        """
        options = options or {}
        
        try:
            # Read Excel file
            df = pd.read_excel(
                source_path,
                sheet_name=options.get('sheet_name', 0),
                header=options.get('header', 0),
                index_col=options.get('index_col', None)
            )
            
            # Convert DataFrame to list of dictionaries
            return df.to_dict('records')
        except Exception as e:
            logger.error(f"Error reading Excel data: {str(e)}")
            raise

class APIConnector(DataSourceConnector):
    """Connector for API data sources."""
    
    def read_data(self, source_path: str, options: Dict[str, Any] = None) -> Any:
        """
        Read data from an API endpoint.
        
        Args:
            source_path: URL of the API endpoint
            options: Additional options for reading
            
        Returns:
            Data from the API
        """
        options = options or {}
        
        try:
            # Set up request parameters
            method = options.get('method', 'GET')
            headers = options.get('headers', {})
            params = options.get('params', {})
            data = options.get('data', None)
            auth = options.get('auth', None)
            timeout = options.get('timeout', 30)
            
            # Make the request
            response = requests.request(
                method=method,
                url=source_path,
                headers=headers,
                params=params,
                data=data,
                auth=auth,
                timeout=timeout
            )
            
            # Check if request was successful
            response.raise_for_status()
            
            # Parse response based on content type
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                return response.json()
            else:
                return response.text
        except Exception as e:
            logger.error(f"Error reading API data: {str(e)}")
            raise

class DatabaseConnector(DataSourceConnector):
    """Connector for database data sources."""
    
    def __init__(self, db_adapter=None):
        """
        Initialize the database connector.
        
        Args:
            db_adapter: Database adapter for querying
        """
        self.db_adapter = db_adapter
        
        # Import database adapter if not provided
        if self.db_adapter is None:
            from src.database.adapters import get_database_adapter
            self.db_adapter = get_database_adapter()
            
            # Connect to the database
            if not self.db_adapter.is_connected():
                self.db_adapter.connect()
    
    def read_data(self, source_path: str, options: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Read data from a database.
        
        Args:
            source_path: Collection or table name
            options: Additional options for reading
            
        Returns:
            List of documents from the database
        """
        options = options or {}
        
        try:
            # Get query parameters
            query = options.get('query', {})
            limit = options.get('limit', 0)
            skip = options.get('skip', 0)
            sort = options.get('sort', None)
            
            # Query the database
            return self.db_adapter.find(source_path, query=query, limit=limit, skip=skip, sort=sort)
        except Exception as e:
            logger.error(f"Error reading database data: {str(e)}")
            raise

# Factory function to get the appropriate connector
def get_data_source_connector(source_type: str, db_adapter=None) -> DataSourceConnector:
    """
    Get a data source connector for the specified type.
    
    Args:
        source_type: Type of data source ('json', 'csv', 'excel', 'api', 'database')
        db_adapter: Database adapter for database connector
        
    Returns:
        Data source connector
    """
    source_type = source_type.lower()
    
    if source_type == 'json':
        return JSONConnector()
    elif source_type == 'csv':
        return CSVConnector()
    elif source_type == 'excel':
        return ExcelConnector()
    elif source_type == 'api':
        return APIConnector()
    elif source_type == 'database':
        return DatabaseConnector(db_adapter)
    else:
        raise ValueError(f"Unsupported data source type: {source_type}")
