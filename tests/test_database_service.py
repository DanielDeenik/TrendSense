import unittest
from unittest.mock import MagicMock, patch
from src.database.database_service import DatabaseService

class TestDatabaseService(unittest.TestCase):
    """Test cases for the DatabaseService class."""

    def setUp(self):
        # Patch the adapter used by DatabaseService
        patcher = patch('src.database.database_service.get_database_adapter')
        self.addCleanup(patcher.stop)
        self.mock_get_adapter = patcher.start()
        self.mock_adapter = MagicMock()
        self.mock_get_adapter.return_value = self.mock_adapter
        self.service = DatabaseService()

    def test_insert_one(self):
        self.mock_adapter.insert_one.return_value = 'mock_id'
        result = self.service.insert_one('collection', {'foo': 'bar'})
        self.assertEqual(result, 'mock_id')
        self.mock_adapter.insert_one.assert_called_once()

    def test_find(self):
        self.mock_adapter.find.return_value = [{'foo': 'bar'}]
        result = self.service.find('collection', query={'foo': 'bar'})
        self.assertEqual(result, [{'foo': 'bar'}])
        self.mock_adapter.find.assert_called_once()

    def test_update_one(self):
        self.mock_adapter.update_one.return_value = True
        result = self.service.update_one('collection', {'foo': 'bar'}, {'$set': {'foo': 'baz'}})
        self.assertTrue(result)
        self.mock_adapter.update_one.assert_called_once()

    def test_delete_one(self):
        self.mock_adapter.delete_one.return_value = True
        result = self.service.delete_one('collection', {'foo': 'bar'})
        self.assertTrue(result)
        self.mock_adapter.delete_one.assert_called_once()

    def test_count_documents(self):
        self.mock_adapter.count_documents.return_value = 42
        result = self.service.count_documents('collection', query={})
        self.assertEqual(result, 42)
        self.mock_adapter.count_documents.assert_called_once()

if __name__ == '__main__':
    unittest.main()
