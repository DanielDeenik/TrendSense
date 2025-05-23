"""
RAG Data Manager

This module provides a comprehensive data management system that uses a RAG (Retrieval-Augmented Generation)
AI agent to read in data from various sources, store and transform it, and then make it available for display
in the application.
"""

import os
import logging
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime
import uuid
import traceback

# Import database adapters
from src.database.adapters import get_database_adapter, DatabaseAdapter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGDataManager:
    """
    RAG Data Manager for SustainaTrend.
    
    This class:
    1. Orchestrates the data flow from various sources
    2. Uses RAG AI to process and enrich the data
    3. Stores the data in the database
    4. Provides methods to retrieve and transform the data for display
    """
    
    def __init__(self, ai_connector=None, db_adapter: Optional[DatabaseAdapter] = None):
        """
        Initialize the RAG Data Manager.
        
        Args:
            ai_connector: AI connector for RAG processing
            db_adapter: Database adapter for storage
        """
        self.ai_connector = ai_connector
        self.db_adapter = db_adapter or get_database_adapter()
        
        # Connect to the database
        if not self.db_adapter.is_connected():
            self.db_adapter.connect()
        
        # Initialize data source connectors
        self.data_source_connectors = {
            'json': self._read_json_data,
            'csv': self._read_csv_data,
            'excel': self._read_excel_data,
            'api': self._read_api_data,
            'database': self._read_database_data
        }
        
        # Initialize data transformation pipeline
        self.transformation_pipeline = [
            self._clean_data,
            self._enrich_data_with_rag,
            self._transform_data,
            self._validate_data
        ]
        
        logger.info("RAG Data Manager initialized")
    
    def process_data_source(self, source_type: str, source_path: str, 
                           options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a data source from start to finish.
        
        Args:
            source_type: Type of data source ('json', 'csv', 'excel', 'api', 'database')
            source_path: Path or URL to the data source
            options: Additional options for processing
            
        Returns:
            Dictionary with processing results
        """
        try:
            # 1. Read data from source
            logger.info(f"Reading data from {source_type} source: {source_path}")
            raw_data = self._read_data(source_type, source_path, options)
            
            if raw_data is None or (isinstance(raw_data, list) and len(raw_data) == 0):
                logger.error(f"No data read from {source_type} source: {source_path}")
                return {
                    'success': False,
                    'error': f"No data read from {source_type} source: {source_path}",
                    'timestamp': datetime.now().isoformat()
                }
            
            # 2. Process data through transformation pipeline
            logger.info(f"Processing data through transformation pipeline")
            processed_data = self._process_data_pipeline(raw_data, options)
            
            # 3. Store data in database
            logger.info(f"Storing processed data in database")
            storage_result = self._store_data(processed_data, options)
            
            # 4. Return results
            return {
                'success': True,
                'source_type': source_type,
                'source_path': source_path,
                'records_processed': len(processed_data) if isinstance(processed_data, list) else 1,
                'storage_result': storage_result,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing data source: {str(e)}")
            logger.error(traceback.format_exc())
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _read_data(self, source_type: str, source_path: str, 
                  options: Dict[str, Any] = None) -> Any:
        """
        Read data from a source.
        
        Args:
            source_type: Type of data source
            source_path: Path or URL to the data source
            options: Additional options for reading
            
        Returns:
            Raw data from the source
        """
        options = options or {}
        
        # Get the appropriate connector
        connector = self.data_source_connectors.get(source_type.lower())
        if connector is None:
            raise ValueError(f"Unsupported data source type: {source_type}")
        
        # Read data using the connector
        return connector(source_path, options)
    
    def _read_json_data(self, source_path: str, options: Dict[str, Any] = None) -> Any:
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
                with open(source_path, 'r', encoding='utf-8') as f:
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
    
    def _read_csv_data(self, source_path: str, options: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Read data from a CSV file.
        
        Args:
            source_path: Path to the CSV file
            options: Additional options for reading
            
        Returns:
            Pandas DataFrame with the CSV data
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
    
    def _read_excel_data(self, source_path: str, options: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Read data from an Excel file.
        
        Args:
            source_path: Path to the Excel file
            options: Additional options for reading
            
        Returns:
            Pandas DataFrame with the Excel data
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
    
    def _read_api_data(self, source_path: str, options: Dict[str, Any] = None) -> Any:
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
            import requests
            
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
    
    def _read_database_data(self, source_path: str, options: Dict[str, Any] = None) -> Any:
        """
        Read data from a database.
        
        Args:
            source_path: Collection or table name
            options: Additional options for reading
            
        Returns:
            Data from the database
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
    
    def _process_data_pipeline(self, data: Any, options: Dict[str, Any] = None) -> Any:
        """
        Process data through the transformation pipeline.
        
        Args:
            data: Raw data to process
            options: Additional options for processing
            
        Returns:
            Processed data
        """
        options = options or {}
        processed_data = data
        
        # Run data through each step in the pipeline
        for step in self.transformation_pipeline:
            processed_data = step(processed_data, options)
        
        return processed_data
    
    def _clean_data(self, data: Any, options: Dict[str, Any] = None) -> Any:
        """
        Clean the data by removing nulls, duplicates, etc.
        
        Args:
            data: Data to clean
            options: Additional options for cleaning
            
        Returns:
            Cleaned data
        """
        options = options or {}
        
        try:
            # If data is a list of dictionaries
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                # Convert to DataFrame for easier cleaning
                df = pd.DataFrame(data)
                
                # Remove duplicates if specified
                if options.get('remove_duplicates', True):
                    df = df.drop_duplicates()
                
                # Handle missing values
                if options.get('drop_nulls', False):
                    df = df.dropna()
                elif options.get('fill_nulls', True):
                    fill_value = options.get('fill_value', '')
                    df = df.fillna(fill_value)
                
                # Convert back to list of dictionaries
                return df.to_dict('records')
            
            # If data is a dictionary
            elif isinstance(data, dict):
                # Handle missing values
                if options.get('fill_nulls', True):
                    fill_value = options.get('fill_value', '')
                    return {k: v if v is not None else fill_value for k, v in data.items()}
                return data
            
            # Return data as is for other types
            return data
        
        except Exception as e:
            logger.error(f"Error cleaning data: {str(e)}")
            # Return original data if cleaning fails
            return data
    
    def _enrich_data_with_rag(self, data: Any, options: Dict[str, Any] = None) -> Any:
        """
        Enrich the data using RAG AI.
        
        Args:
            data: Data to enrich
            options: Additional options for enrichment
            
        Returns:
            Enriched data
        """
        options = options or {}
        
        # Skip if AI connector is not available or enrichment is disabled
        if self.ai_connector is None or not options.get('enrich_with_rag', True):
            logger.info("Skipping RAG enrichment: AI connector not available or enrichment disabled")
            return data
        
        try:
            # If data is a list of dictionaries
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                enriched_data = []
                
                for item in data:
                    # Create a prompt for the AI
                    prompt = self._create_enrichment_prompt(item, options)
                    
                    # Get AI response
                    ai_response = self.ai_connector.generate_text(prompt)
                    
                    # Parse AI response
                    enriched_item = self._parse_ai_response(item, ai_response, options)
                    
                    # Add to enriched data
                    enriched_data.append(enriched_item)
                
                return enriched_data
            
            # If data is a dictionary
            elif isinstance(data, dict):
                # Create a prompt for the AI
                prompt = self._create_enrichment_prompt(data, options)
                
                # Get AI response
                ai_response = self.ai_connector.generate_text(prompt)
                
                # Parse AI response
                return self._parse_ai_response(data, ai_response, options)
            
            # Return data as is for other types
            return data
        
        except Exception as e:
            logger.error(f"Error enriching data with RAG: {str(e)}")
            # Return original data if enrichment fails
            return data
    
    def _create_enrichment_prompt(self, data: Dict[str, Any], options: Dict[str, Any]) -> str:
        """
        Create a prompt for RAG AI enrichment.
        
        Args:
            data: Data to enrich
            options: Additional options for enrichment
            
        Returns:
            Prompt for the AI
        """
        # Get enrichment type
        enrichment_type = options.get('enrichment_type', 'sustainability')
        
        # Create prompt based on enrichment type
        if enrichment_type == 'sustainability':
            return f"""
            Analyze the following data and enrich it with sustainability insights:
            
            DATA:
            {json.dumps(data, indent=2)}
            
            TASK:
            1. Identify any sustainability metrics or indicators in the data
            2. Calculate or estimate ESG scores based on the data
            3. Identify potential sustainability risks and opportunities
            4. Add relevant sustainability tags or categories
            5. Provide a brief sustainability assessment
            
            Return the enriched data as a JSON object with the original data plus new fields for the enrichments.
            """
        elif enrichment_type == 'financial':
            return f"""
            Analyze the following data and enrich it with financial insights:
            
            DATA:
            {json.dumps(data, indent=2)}
            
            TASK:
            1. Identify any financial metrics or indicators in the data
            2. Calculate or estimate financial ratios based on the data
            3. Identify potential financial risks and opportunities
            4. Add relevant financial tags or categories
            5. Provide a brief financial assessment
            
            Return the enriched data as a JSON object with the original data plus new fields for the enrichments.
            """
        else:
            return f"""
            Analyze the following data and enrich it with additional insights:
            
            DATA:
            {json.dumps(data, indent=2)}
            
            TASK:
            1. Identify any important metrics or indicators in the data
            2. Calculate or estimate relevant scores based on the data
            3. Identify potential risks and opportunities
            4. Add relevant tags or categories
            5. Provide a brief assessment
            
            Return the enriched data as a JSON object with the original data plus new fields for the enrichments.
            """
    
    def _parse_ai_response(self, original_data: Dict[str, Any], ai_response: str, 
                          options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse the AI response and merge with original data.
        
        Args:
            original_data: Original data
            ai_response: AI response
            options: Additional options for parsing
            
        Returns:
            Merged data
        """
        try:
            # Try to parse AI response as JSON
            enriched_data = json.loads(ai_response)
            
            # If AI returned a complete object, use it
            if isinstance(enriched_data, dict):
                # Ensure original data is preserved
                for key, value in original_data.items():
                    if key not in enriched_data:
                        enriched_data[key] = value
                
                return enriched_data
            else:
                logger.warning("AI response is not a dictionary, using original data")
                return original_data
        except json.JSONDecodeError:
            logger.warning("Failed to parse AI response as JSON, extracting structured data")
            
            # Try to extract structured data from the response
            enriched_data = original_data.copy()
            
            # Look for key-value pairs in the response
            lines = ai_response.split('\n')
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower().replace(' ', '_')
                    value = value.strip()
                    
                    # Add to enriched data
                    enriched_data[key] = value
            
            return enriched_data
        except Exception as e:
            logger.error(f"Error parsing AI response: {str(e)}")
            return original_data
    
    def _transform_data(self, data: Any, options: Dict[str, Any] = None) -> Any:
        """
        Transform the data based on specified transformations.
        
        Args:
            data: Data to transform
            options: Additional options for transformation
            
        Returns:
            Transformed data
        """
        options = options or {}
        transformations = options.get('transformations', [])
        
        if not transformations:
            return data
        
        try:
            # If data is a list of dictionaries
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                # Convert to DataFrame for easier transformation
                df = pd.DataFrame(data)
                
                # Apply transformations
                for transformation in transformations:
                    transform_type = transformation.get('type')
                    
                    if transform_type == 'rename_columns':
                        # Rename columns
                        column_map = transformation.get('column_map', {})
                        df = df.rename(columns=column_map)
                    
                    elif transform_type == 'filter_rows':
                        # Filter rows
                        condition = transformation.get('condition', {})
                        for column, value in condition.items():
                            if column in df.columns:
                                df = df[df[column] == value]
                    
                    elif transform_type == 'calculate_column':
                        # Calculate a new column
                        column_name = transformation.get('column_name')
                        expression = transformation.get('expression')
                        
                        if column_name and expression:
                            # Use eval to calculate the expression
                            df[column_name] = df.eval(expression)
                    
                    elif transform_type == 'aggregate':
                        # Aggregate data
                        group_by = transformation.get('group_by', [])
                        aggregations = transformation.get('aggregations', {})
                        
                        if group_by and aggregations:
                            df = df.groupby(group_by).agg(aggregations).reset_index()
                
                # Convert back to list of dictionaries
                return df.to_dict('records')
            
            # Return data as is for other types
            return data
        
        except Exception as e:
            logger.error(f"Error transforming data: {str(e)}")
            # Return original data if transformation fails
            return data
    
    def _validate_data(self, data: Any, options: Dict[str, Any] = None) -> Any:
        """
        Validate the data against a schema.
        
        Args:
            data: Data to validate
            options: Additional options for validation
            
        Returns:
            Validated data
        """
        options = options or {}
        schema = options.get('schema')
        
        if not schema:
            return data
        
        try:
            from jsonschema import validate, ValidationError
            
            # If data is a list of dictionaries
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                validated_data = []
                
                for item in data:
                    try:
                        # Validate against schema
                        validate(instance=item, schema=schema)
                        validated_data.append(item)
                    except ValidationError as e:
                        logger.warning(f"Validation error: {str(e)}")
                        # Skip invalid items if specified
                        if not options.get('skip_invalid', False):
                            validated_data.append(item)
                
                return validated_data
            
            # If data is a dictionary
            elif isinstance(data, dict):
                try:
                    # Validate against schema
                    validate(instance=data, schema=schema)
                    return data
                except ValidationError as e:
                    logger.warning(f"Validation error: {str(e)}")
                    return data if not options.get('skip_invalid', False) else None
            
            # Return data as is for other types
            return data
        
        except ImportError:
            logger.warning("jsonschema not installed, skipping validation")
            return data
        except Exception as e:
            logger.error(f"Error validating data: {str(e)}")
            # Return original data if validation fails
            return data
    
    def _store_data(self, data: Any, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Store the data in the database.
        
        Args:
            data: Data to store
            options: Additional options for storage
            
        Returns:
            Storage result
        """
        options = options or {}
        collection_name = options.get('collection_name')
        
        if not collection_name:
            logger.error("No collection name specified for storage")
            return {
                'success': False,
                'error': "No collection name specified for storage"
            }
        
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


# Create a singleton instance
rag_data_manager = None

def get_rag_data_manager(ai_connector=None, db_adapter=None):
    """
    Get the RAG Data Manager singleton instance.
    
    Args:
        ai_connector: AI connector for RAG processing
        db_adapter: Database adapter for storage
        
    Returns:
        RAG Data Manager instance
    """
    global rag_data_manager
    
    if rag_data_manager is None:
        rag_data_manager = RAGDataManager(ai_connector, db_adapter)
    
    return rag_data_manager
