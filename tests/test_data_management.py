"""
Tests for the data management functionality.
"""

import unittest
import json
import os
import sys
from unittest.mock import patch, MagicMock

# Add the src directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the app
from app import app

# Import data management components
from src.data_management import (
    RAGDataManager, get_rag_data_manager,
    JSONConnector, CSVConnector, ExcelConnector, APIConnector,
    CleaningTransformer, RAGEnrichmentTransformer, ColumnTransformer,
    DataStorage, DataRetrieval, MockAIConnector
)

class TestDataManagement(unittest.TestCase):
    """Test cases for the data management functionality."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create a Flask test client
        self.app = app.test_client()
        self.app.testing = True
        
        # Create a mock AI connector
        self.mock_ai_connector = MockAIConnector()
        
        # Create a mock database adapter
        self.mock_db_adapter = MagicMock()
        self.mock_db_adapter.is_connected.return_value = True
        self.mock_db_adapter.connect.return_value = True
        self.mock_db_adapter.find.return_value = []
        self.mock_db_adapter.find_one.return_value = None
        self.mock_db_adapter.insert_one.return_value = "test_id"
        self.mock_db_adapter.insert_many.return_value = ["test_id_1", "test_id_2"]
        
        # Create a RAG data manager with mock components
        self.rag_data_manager = RAGDataManager(
            ai_connector=self.mock_ai_connector,
            db_adapter=self.mock_db_adapter
        )
    
    def test_data_management_routes(self):
        """Test data management routes."""
        # Test index route
        response = self.app.get('/data-management/')
        self.assertEqual(response.status_code, 200)
        
        # Test upload route
        response = self.app.get('/data-management/upload')
        self.assertEqual(response.status_code, 200)
        
        # Test API route
        response = self.app.get('/data-management/api')
        self.assertEqual(response.status_code, 200)
    
    def test_json_connector(self):
        """Test JSON connector."""
        # Create a JSON connector
        json_connector = JSONConnector()
        
        # Create a temporary JSON file
        test_data = {"test": "data", "number": 123}
        test_file = "test_data.json"
        
        with open(test_file, "w") as f:
            json.dump(test_data, f)
        
        try:
            # Test reading from file
            result = json_connector.read_data(test_file)
            self.assertEqual(result, test_data)
            
            # Test reading from string
            result = json_connector.read_data(json.dumps(test_data))
            self.assertEqual(result, test_data)
        finally:
            # Clean up
            if os.path.exists(test_file):
                os.remove(test_file)
    
    def test_cleaning_transformer(self):
        """Test cleaning transformer."""
        # Create a cleaning transformer
        cleaning_transformer = CleaningTransformer()
        
        # Test cleaning a list of dictionaries
        test_data = [
            {"name": "Test 1", "value": None},
            {"name": "Test 2", "value": 123},
            {"name": "Test 1", "value": None}  # Duplicate
        ]
        
        # Clean with default options (remove duplicates, fill nulls)
        result = cleaning_transformer.transform(test_data)
        
        # Check that duplicates were removed
        self.assertEqual(len(result), 2)
        
        # Check that nulls were filled
        self.assertEqual(result[0]["value"], "")
    
    def test_rag_enrichment_transformer(self):
        """Test RAG enrichment transformer."""
        # Create a RAG enrichment transformer with mock AI connector
        rag_transformer = RAGEnrichmentTransformer(self.mock_ai_connector)
        
        # Test enriching a dictionary
        test_data = {"name": "Test", "value": 123}
        
        # Enrich with default options
        result = rag_transformer.transform(test_data)
        
        # Check that the result is a dictionary
        self.assertIsInstance(result, dict)
        
        # Check that the original data is preserved
        self.assertEqual(result["name"], "Test")
        self.assertEqual(result["value"], 123)
    
    def test_rag_data_manager(self):
        """Test RAG data manager."""
        # Test processing a JSON data source
        test_data = {"test": "data", "number": 123}
        test_file = "test_data.json"
        
        with open(test_file, "w") as f:
            json.dump(test_data, f)
        
        try:
            # Process the JSON data source
            result = self.rag_data_manager.process_data_source(
                "json",
                test_file,
                {"collection_name": "test_collection"}
            )
            
            # Check that the result is successful
            self.assertTrue(result["success"])
            
            # Check that the database adapter was called
            self.mock_db_adapter.insert_one.assert_called_once()
        finally:
            # Clean up
            if os.path.exists(test_file):
                os.remove(test_file)
    
    def test_data_storage(self):
        """Test data storage."""
        # Create a data storage with mock database adapter
        data_storage = DataStorage(self.mock_db_adapter)
        
        # Test storing a dictionary
        test_data = {"name": "Test", "value": 123}
        
        # Store the data
        result = data_storage.store_data(test_data, "test_collection")
        
        # Check that the result is successful
        self.assertTrue(result["success"])
        
        # Check that the database adapter was called
        self.mock_db_adapter.insert_one.assert_called_once()
    
    def test_data_retrieval(self):
        """Test data retrieval."""
        # Create a data retrieval with mock database adapter
        data_retrieval = DataRetrieval(self.mock_db_adapter)
        
        # Test getting data for display
        result = data_retrieval.get_data_for_display("test_collection")
        
        # Check that the result is a list
        self.assertIsInstance(result, list)
        
        # Check that the database adapter was called
        self.mock_db_adapter.find.assert_called_once()

if __name__ == '__main__':
    unittest.main()
