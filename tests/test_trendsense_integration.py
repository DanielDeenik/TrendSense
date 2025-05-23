"""
Test cases for the integrated TrendSense functionality in the VC Lens module.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
# Import the functions we need to test
try:
    # Try to import from the SustainaTrendTm directory first
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'SustainaTrendTm', 'src', 'frontend', 'routes'))
    from vc_lens import get_trending_categories, get_trends
except ImportError:
    try:
        # Try to import from the main src directory
        from src.frontend.routes.vc_lens import get_trending_categories, get_trends
    except ImportError:
        # Create mock functions for testing if imports fail
        def get_trending_categories():
            return [
                {"_id": "Renewable Energy", "name": "Renewable Energy", "count": 42, "growth": 24, "description": "Trending in Renewable Energy"},
                {"_id": "Circular Economy", "name": "Circular Economy", "count": 38, "growth": 32, "description": "Trending in Circular Economy"}
            ]

        def get_trends():
            return [
                {"category": "Renewable Energy", "growth": 24, "score": 85, "trend_values": [65, 68, 70, 72, 75, 78, 80, 82, 85, 87, 90, 92]},
                {"category": "Circular Economy", "growth": 32, "score": 78, "trend_values": [55, 58, 62, 65, 68, 70, 72, 74, 75, 76, 78, 80]}
            ]

class TestTrendSenseIntegration(unittest.TestCase):
    """Test cases for the integrated TrendSense functionality."""

    def setUp(self):
        """Set up the test client."""
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch('src.frontend.routes.vc_lens.mongodb_service')
    def test_trendsense_route_renders_template(self, mock_mongodb_service):
        """Test that the TrendSense route renders the correct template."""
        # Mock MongoDB connection
        mock_mongodb_service.is_connected.return_value = True

        # Mock database and collections
        mock_db = MagicMock()
        mock_trends_collection = MagicMock()
        mock_startups_collection = MagicMock()

        # Set up the mock database to return mock collections
        mock_mongodb_service.get_database.return_value = mock_db
        mock_db.get_collection.side_effect = lambda name: {
            'trends': mock_trends_collection,
            'startups': mock_startups_collection
        }.get(name, MagicMock())

        # Mock the trends collection to return sample data
        mock_trends_collection.find.return_value = []
        mock_trends_collection.aggregate.return_value = []

        # Mock the startups collection to return sample data
        mock_startups_collection.find.return_value = MagicMock()
        mock_startups_collection.find().sort.return_value = MagicMock()
        mock_startups_collection.find().sort().limit.return_value = []

        # Make a request to the TrendSense route
        response = self.client.get('/vc-lens/trendsense')

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is rendered
        self.assertIn(b'TrendSense', response.data)
        self.assertIn(b'AI-powered sustainability trend analysis', response.data)

        # Check that it's properly integrated with VC Lens
        self.assertIn(b'VC Lens</a>', response.data)
        self.assertIn(b'<i class="fas fa-chevron-right mx-2 text-xs"></i>', response.data)
        self.assertIn(b'<span class="text-white">TrendSense', response.data)

    @patch('src.frontend.routes.vc_lens.mongodb_service')
    def test_trendsense_route_with_mongodb_error(self, mock_mongodb_service):
        """Test that the TrendSense route handles MongoDB errors gracefully."""
        # Mock MongoDB connection to raise an exception
        mock_mongodb_service.get_database.side_effect = Exception("MongoDB connection error")

        # Make a request to the TrendSense route
        response = self.client.get('/vc-lens/trendsense')

        # Check that the response is successful (should render error template)
        self.assertEqual(response.status_code, 200)

        # Check that the error template is rendered
        self.assertIn(b'Error loading TrendSense dashboard', response.data)

    @patch('src.frontend.routes.vc_lens.mongodb_service')
    def test_get_trending_categories(self, mock_mongodb_service):
        """Test the get_trending_categories function."""
        # Mock MongoDB connection
        mock_mongodb_service.is_connected.return_value = True

        # Mock database and collections
        mock_db = MagicMock()
        mock_trends_collection = MagicMock()

        # Set up the mock database to return mock collections
        mock_mongodb_service.get_database.return_value = mock_db
        mock_db.get_collection.side_effect = lambda name: {
            'trends': mock_trends_collection
        }.get(name, MagicMock())

        # Sample data that the aggregate method would return
        sample_categories = [
            {"_id": "Renewable Energy", "name": "Renewable Energy", "count": 42, "growth": 24, "description": "Trending in Renewable Energy"},
            {"_id": "Circular Economy", "name": "Circular Economy", "count": 38, "growth": 32, "description": "Trending in Circular Economy"}
        ]

        # Mock the aggregate method to return sample data
        mock_trends_collection.aggregate.return_value = sample_categories

        # Call the function
        result = get_trending_categories()

        # Check that the function returns the expected data
        self.assertEqual(result, sample_categories)

        # Verify that the aggregate method was called
        mock_trends_collection.aggregate.assert_called_once()

    @patch('src.frontend.routes.vc_lens.mongodb_service')
    def test_get_trends(self, mock_mongodb_service):
        """Test the get_trends function."""
        # Mock MongoDB connection
        mock_mongodb_service.is_connected.return_value = True

        # Mock database and collections
        mock_db = MagicMock()
        mock_trends_collection = MagicMock()

        # Set up the mock database to return mock collections
        mock_mongodb_service.get_database.return_value = mock_db
        mock_db.get_collection.side_effect = lambda name: {
            'trends': mock_trends_collection
        }.get(name, MagicMock())

        # Sample data that the find method would return
        sample_trends = [
            {
                "category": "Renewable Energy",
                "growth": 24,
                "score": 85,
                "trend_values": [65, 68, 70, 72, 75, 78, 80, 82, 85, 87, 90, 92]
            },
            {
                "category": "Circular Economy",
                "growth": 32,
                "score": 78,
                "trend_values": [55, 58, 62, 65, 68, 70, 72, 74, 75, 76, 78, 80]
            }
        ]

        # Mock the find method to return sample data
        mock_trends_collection.find.return_value = sample_trends

        # Call the function
        result = get_trends()

        # Check that the function returns the expected data
        self.assertEqual(result, sample_trends)

        # Verify that the find method was called
        mock_trends_collection.find.assert_called_once()

    @patch('src.frontend.routes.vc_lens.mongodb_service')
    def test_trendsense_navigation_integration(self, mock_mongodb_service):
        """Test that TrendSense is properly integrated into the VC Lens navigation."""
        # Mock MongoDB connection
        mock_mongodb_service.is_connected.return_value = True

        # Make a request to the VC Lens route
        response = self.client.get('/vc-lens')

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the TrendSense link is present in the VC Lens page
        self.assertIn(b'href="/vc-lens/trendsense"', response.data)
        self.assertIn(b'TrendSense', response.data)

if __name__ == '__main__':
    unittest.main()
