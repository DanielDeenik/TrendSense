"""
Data Transformer

This module provides classes and functions for transforming data in the ETL pipeline.
"""

import logging
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union, Callable
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataTransformer(ABC):
    """Abstract base class for data transformers."""
    
    @abstractmethod
    def transform(self, data: Any, options: Dict[str, Any] = None) -> Any:
        """
        Transform the data.
        
        Args:
            data: Data to transform
            options: Additional options for transformation
            
        Returns:
            Transformed data
        """
        pass

class CleaningTransformer(DataTransformer):
    """Transformer for cleaning data."""
    
    def transform(self, data: Any, options: Dict[str, Any] = None) -> Any:
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

class RAGEnrichmentTransformer(DataTransformer):
    """Transformer for enriching data using RAG AI."""
    
    def __init__(self, ai_connector=None):
        """
        Initialize the RAG enrichment transformer.
        
        Args:
            ai_connector: AI connector for RAG processing
        """
        self.ai_connector = ai_connector
    
    def transform(self, data: Any, options: Dict[str, Any] = None) -> Any:
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

class ColumnTransformer(DataTransformer):
    """Transformer for transforming columns in tabular data."""
    
    def transform(self, data: Any, options: Dict[str, Any] = None) -> Any:
        """
        Transform columns in tabular data.
        
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

class SchemaValidationTransformer(DataTransformer):
    """Transformer for validating data against a schema."""
    
    def transform(self, data: Any, options: Dict[str, Any] = None) -> Any:
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

class TransformationPipeline:
    """Pipeline for transforming data through multiple transformers."""
    
    def __init__(self, transformers: List[DataTransformer] = None):
        """
        Initialize the transformation pipeline.
        
        Args:
            transformers: List of transformers to apply
        """
        self.transformers = transformers or []
    
    def add_transformer(self, transformer: DataTransformer) -> None:
        """
        Add a transformer to the pipeline.
        
        Args:
            transformer: Transformer to add
        """
        self.transformers.append(transformer)
    
    def transform(self, data: Any, options: Dict[str, Any] = None) -> Any:
        """
        Transform the data through the pipeline.
        
        Args:
            data: Data to transform
            options: Additional options for transformation
            
        Returns:
            Transformed data
        """
        options = options or {}
        transformed_data = data
        
        # Run data through each transformer in the pipeline
        for transformer in self.transformers:
            transformed_data = transformer.transform(transformed_data, options)
        
        return transformed_data

# Factory function to create a standard transformation pipeline
def create_standard_pipeline(ai_connector=None) -> TransformationPipeline:
    """
    Create a standard transformation pipeline.
    
    Args:
        ai_connector: AI connector for RAG processing
        
    Returns:
        Transformation pipeline
    """
    pipeline = TransformationPipeline()
    
    # Add standard transformers
    pipeline.add_transformer(CleaningTransformer())
    pipeline.add_transformer(RAGEnrichmentTransformer(ai_connector))
    pipeline.add_transformer(ColumnTransformer())
    pipeline.add_transformer(SchemaValidationTransformer())
    
    return pipeline
