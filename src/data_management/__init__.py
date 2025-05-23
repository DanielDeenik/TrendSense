"""
Data Management Package

This package provides a comprehensive data management system for SustainaTrend.
It includes:
1. RAG Data Manager for orchestrating the data flow
2. Data Source Connectors for reading data from various sources
3. Data Transformers for processing and enriching data
4. Data Storage for storing data in the database
5. Data Retrieval for retrieving data for display in the application
6. AI Connector for RAG processing
"""

from .rag_data_manager import RAGDataManager, get_rag_data_manager
from .data_source_connector import (
    DataSourceConnector, JSONConnector, CSVConnector, 
    ExcelConnector, APIConnector, DatabaseConnector,
    get_data_source_connector
)
from .data_transformer import (
    DataTransformer, CleaningTransformer, RAGEnrichmentTransformer,
    ColumnTransformer, SchemaValidationTransformer,
    TransformationPipeline, create_standard_pipeline
)
from .data_storage import DataStorage, get_data_storage
from .data_retrieval import DataRetrieval, get_data_retrieval
from .ai_connector import (
    AIConnector, OpenAIConnector, HuggingFaceConnector,
    MockAIConnector, get_ai_connector
)

__all__ = [
    'RAGDataManager', 'get_rag_data_manager',
    'DataSourceConnector', 'JSONConnector', 'CSVConnector',
    'ExcelConnector', 'APIConnector', 'DatabaseConnector',
    'get_data_source_connector',
    'DataTransformer', 'CleaningTransformer', 'RAGEnrichmentTransformer',
    'ColumnTransformer', 'SchemaValidationTransformer',
    'TransformationPipeline', 'create_standard_pipeline',
    'DataStorage', 'get_data_storage',
    'DataRetrieval', 'get_data_retrieval',
    'AIConnector', 'OpenAIConnector', 'HuggingFaceConnector',
    'MockAIConnector', 'get_ai_connector'
]
