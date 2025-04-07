"""
Ingestion Service
Coordinates data ingestion using adapters.
"""

import os
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from .adapters.adapter_factory import AdapterFactory
from ..database.mongodb_manager import MongoDBManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IngestionService:
    """Service for coordinating data ingestion"""
    
    def __init__(self, db_manager: MongoDBManager):
        self.adapter_factory = AdapterFactory()
        self.db_manager = db_manager
    
    def ingest_file(self, file_path: str) -> Dict[str, Any]:
        """Ingest a file using the appropriate adapter"""
        try:
            # Get the appropriate adapter
            adapter = self.adapter_factory.get_adapter(file_path)
            if not adapter:
                raise ValueError(f"No suitable adapter found for file: {file_path}")
            
            # Process the file
            normalized_data = adapter.process(file_path)
            
            # Validate the data
            if not adapter.validate_data(normalized_data):
                raise ValueError("Invalid data format")
            
            # Store the data in MongoDB
            result = self._store_data(normalized_data)
            
            # Log the ingestion
            self._log_ingestion(file_path, normalized_data['type'], result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error ingesting file {file_path}: {str(e)}")
            raise
    
    def _store_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Store the normalized data in MongoDB"""
        try:
            if data['type'] == 'portfolio_companies':
                return self.db_manager.insert_portfolio_companies(data['data'])
            elif data['type'] == 'sustainability_metrics':
                return self.db_manager.insert_sustainability_metrics(data['data'])
            else:
                raise ValueError(f"Unknown data type: {data['type']}")
                
        except Exception as e:
            logger.error(f"Error storing data: {str(e)}")
            raise
    
    def _log_ingestion(self, file_path: str, data_type: str, result: Dict[str, Any]) -> None:
        """Log the ingestion details"""
        try:
            log_entry = {
                'file_path': file_path,
                'data_type': data_type,
                'timestamp': datetime.now(),
                'status': 'success',
                'result': result
            }
            
            self.db_manager.insert_ingestion_log(log_entry)
            
        except Exception as e:
            logger.error(f"Error logging ingestion: {str(e)}")
    
    def get_supported_formats(self) -> Dict[str, List[str]]:
        """Get all supported file formats"""
        formats = {}
        for name, adapter_class in self.adapter_factory.list_adapters().items():
            adapter = adapter_class()
            formats[name] = adapter.get_supported_formats()
        return formats
    
    def register_adapter(self, name: str, adapter_class: Any) -> None:
        """Register a new adapter"""
        self.adapter_factory.register_adapter(name, adapter_class) 