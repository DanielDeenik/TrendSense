"""
Test cases for database adapters.
"""

import pytest
from unittest.mock import patch, MagicMock, Mock
import os


class TestDatabaseAdapterFactory:
    """Test cases for the database adapter factory."""

    def test_get_database_adapter_default(self):
        """Test getting the default database adapter."""
        from src.database.adapters import get_database_adapter
        
        adapter = get_database_adapter()
        assert adapter is not None

    def test_get_database_adapter_mongodb(self):
        """Test getting MongoDB adapter."""
        from src.database.adapters import get_database_adapter
        
        adapter = get_database_adapter('mongodb')
        assert adapter is not None
        assert adapter.__class__.__name__ == 'MongoDBAdapter'

    def test_get_database_adapter_firebase(self):
        """Test getting Firebase adapter."""
        from src.database.adapters import get_database_adapter
        
        # This will fall back to mock if firebase_admin is not available
        adapter = get_database_adapter('firebase')
        assert adapter is not None

    def test_get_database_adapter_mock_firebase(self):
        """Test getting mock Firebase adapter."""
        from src.database.adapters import get_database_adapter
        
        adapter = get_database_adapter('mock_firebase')
        assert adapter is not None
        assert adapter.__class__.__name__ == 'MockFirebaseAdapter'

    def test_get_database_adapter_dual(self):
        """Test getting dual database adapter."""
        from src.database.adapters import get_database_adapter
        
        adapter = get_database_adapter('dual')
        assert adapter is not None
        assert adapter.__class__.__name__ == 'DualDatabaseAdapter'


class TestMongoDBAdapter:
    """Test cases for MongoDB adapter."""

    @patch('src.database.adapters.mongodb_adapter.MongoClient')
    def test_mongodb_adapter_connect(self, mock_mongo_client):
        """Test MongoDB adapter connection."""
        from src.database.adapters.mongodb_adapter import MongoDBAdapter
        
        # Mock successful connection
        mock_client = MagicMock()
        mock_client.admin.command.return_value = {'ok': 1}
        mock_mongo_client.return_value = mock_client
        
        adapter = MongoDBAdapter()
        result = adapter.connect()
        
        assert result is True
        assert adapter.is_connected() is True

    @patch('src.database.adapters.mongodb_adapter.MongoClient')
    def test_mongodb_adapter_connection_failure(self, mock_mongo_client):
        """Test MongoDB adapter connection failure."""
        from src.database.adapters.mongodb_adapter import MongoDBAdapter
        from pymongo.errors import ConnectionFailure
        
        # Mock connection failure
        mock_mongo_client.side_effect = ConnectionFailure("Connection failed")
        
        adapter = MongoDBAdapter()
        result = adapter.connect()
        
        assert result is False
        assert adapter.is_connected() is False

    @patch('src.database.adapters.mongodb_adapter.MongoClient')
    def test_mongodb_adapter_get_collection(self, mock_mongo_client):
        """Test MongoDB adapter get collection."""
        from src.database.adapters.mongodb_adapter import MongoDBAdapter
        
        # Mock successful connection
        mock_client = MagicMock()
        mock_db = MagicMock()
        mock_collection = MagicMock()
        
        mock_client.admin.command.return_value = {'ok': 1}
        mock_client.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value = mock_collection
        mock_mongo_client.return_value = mock_client
        
        adapter = MongoDBAdapter()
        adapter.connect()
        
        collection = adapter.get_collection('test_collection')
        assert collection is not None

    @patch('src.database.adapters.mongodb_adapter.MongoClient')
    def test_mongodb_adapter_insert_document(self, mock_mongo_client):
        """Test MongoDB adapter insert document."""
        from src.database.adapters.mongodb_adapter import MongoDBAdapter
        
        # Mock successful connection and insertion
        mock_client = MagicMock()
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_result = MagicMock()
        mock_result.inserted_id = 'test_id'
        
        mock_client.admin.command.return_value = {'ok': 1}
        mock_client.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value = mock_collection
        mock_collection.insert_one.return_value = mock_result
        mock_mongo_client.return_value = mock_client
        
        adapter = MongoDBAdapter()
        adapter.connect()
        
        result = adapter.insert_document('test_collection', {'name': 'test'})
        assert result == 'test_id'


class TestFirebaseAdapter:
    """Test cases for Firebase adapter."""

    def test_firebase_adapter_import_fallback(self):
        """Test Firebase adapter falls back to mock when firebase_admin not available."""
        from src.database.adapters import get_database_adapter
        
        # This should work regardless of whether firebase_admin is installed
        adapter = get_database_adapter('firebase')
        assert adapter is not None


class TestMockFirebaseAdapter:
    """Test cases for mock Firebase adapter."""

    def test_mock_firebase_adapter_connect(self):
        """Test mock Firebase adapter connection."""
        from src.database.adapters.mock_firebase_adapter import MockFirebaseAdapter
        
        adapter = MockFirebaseAdapter()
        result = adapter.connect()
        
        assert result is True
        assert adapter.is_connected() is True

    def test_mock_firebase_adapter_get_collection(self):
        """Test mock Firebase adapter get collection."""
        from src.database.adapters.mock_firebase_adapter import MockFirebaseAdapter
        
        adapter = MockFirebaseAdapter()
        adapter.connect()
        
        collection = adapter.get_collection('test_collection')
        assert collection is not None

    def test_mock_firebase_adapter_insert_document(self):
        """Test mock Firebase adapter insert document."""
        from src.database.adapters.mock_firebase_adapter import MockFirebaseAdapter
        
        adapter = MockFirebaseAdapter()
        adapter.connect()
        
        result = adapter.insert_document('test_collection', {'name': 'test'})
        assert result is not None

    def test_mock_firebase_adapter_find_documents(self):
        """Test mock Firebase adapter find documents."""
        from src.database.adapters.mock_firebase_adapter import MockFirebaseAdapter
        
        adapter = MockFirebaseAdapter()
        adapter.connect()
        
        # Insert a document first
        adapter.insert_document('test_collection', {'name': 'test'})
        
        # Find documents
        results = adapter.find_documents('test_collection', {})
        assert isinstance(results, list)


class TestDualDatabaseAdapter:
    """Test cases for dual database adapter."""

    @patch('src.database.adapters.dual_adapter.get_database_adapter')
    def test_dual_adapter_initialization(self, mock_get_adapter):
        """Test dual adapter initialization."""
        from src.database.adapters.dual_adapter import DualDatabaseAdapter
        
        # Mock primary and secondary adapters
        mock_primary = MagicMock()
        mock_secondary = MagicMock()
        mock_get_adapter.side_effect = [mock_primary, mock_secondary]
        
        adapter = DualDatabaseAdapter()
        assert adapter.primary_adapter == mock_primary
        assert adapter.secondary_adapter == mock_secondary

    @patch('src.database.adapters.dual_adapter.get_database_adapter')
    def test_dual_adapter_connect(self, mock_get_adapter):
        """Test dual adapter connection."""
        from src.database.adapters.dual_adapter import DualDatabaseAdapter
        
        # Mock primary and secondary adapters
        mock_primary = MagicMock()
        mock_secondary = MagicMock()
        mock_primary.connect.return_value = True
        mock_secondary.connect.return_value = True
        mock_get_adapter.side_effect = [mock_primary, mock_secondary]
        
        adapter = DualDatabaseAdapter()
        result = adapter.connect()
        
        assert result is True
        mock_primary.connect.assert_called_once()
        mock_secondary.connect.assert_called_once()


class TestDatabaseService:
    """Test cases for database service."""

    @patch('src.database.database_service.get_database_adapter')
    def test_database_service_singleton(self, mock_get_adapter):
        """Test database service singleton pattern."""
        from src.database.database_service import DatabaseService
        
        mock_adapter = MagicMock()
        mock_adapter.connect.return_value = True
        mock_get_adapter.return_value = mock_adapter
        
        service1 = DatabaseService()
        service2 = DatabaseService()
        
        assert service1 is service2

    @patch('src.database.database_service.get_database_adapter')
    def test_database_service_connection(self, mock_get_adapter):
        """Test database service connection."""
        from src.database.database_service import DatabaseService
        
        mock_adapter = MagicMock()
        mock_adapter.connect.return_value = True
        mock_get_adapter.return_value = mock_adapter
        
        service = DatabaseService()
        assert service.is_connected() is True


if __name__ == '__main__':
    pytest.main([__file__])
