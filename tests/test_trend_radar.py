"""
Test cases for the standalone TrendRadar route.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class TestTrendRadar(unittest.TestCase):
    """Test cases for the TrendRadar route."""

    def setUp(self):
        """Set up the test client."""
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch('src.frontend.routes.trend_radar.mongodb_service')
    def test_trend_radar_route_renders_template(self, mock_mongodb_service):
        """Test that the TrendRadar route renders the correct template."""
        # Mock MongoDB connection
        mock_mongodb_service.is_connected.return_value = True

        # Mock database and collections
        mock_db = MagicMock()
        mock_trends_collection = MagicMock()

        # Set up the mock database to return mock collections
        mock_mongodb_service.get_database.return_value = mock_db
        mock_db.get_collection.side_effect = lambda name: {
            'radar_trends': mock_trends_collection
        }.get(name, MagicMock())

        # Mock the trends collection to return sample data
        mock_trends_collection.find.return_value = []

        # Make a request to the TrendRadar route
        response = self.client.get('/trend-radar')

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is rendered
        self.assertIn(b'TrendRadar', response.data)
        self.assertIn(b'AI-powered VC/PE innovation trend analysis', response.data)

    @patch('src.frontend.routes.trend_radar.mongodb_service')
    def test_trend_radar_route_with_mongodb_error(self, mock_mongodb_service):
        """Test that the TrendRadar route handles MongoDB errors gracefully."""
        # Mock MongoDB connection to raise an exception
        mock_mongodb_service.get_database.side_effect = Exception("MongoDB connection error")

        # Make a request to the TrendRadar route
        response = self.client.get('/trend-radar')

        # Check that the response is successful (should render error template)
        self.assertEqual(response.status_code, 200)

        # Check that the error template is rendered
        self.assertIn(b'Error loading TrendRadar dashboard', response.data)

    @patch('src.frontend.routes.trend_radar.mongodb_service')
    def test_trend_radar_api_query_trends(self, mock_mongodb_service):
        """Test the API endpoint for querying trends."""
        # Mock MongoDB connection
        mock_mongodb_service.is_connected.return_value = True

        # Mock database and collections
        mock_db = MagicMock()
        mock_trends_collection = MagicMock()

        # Set up the mock database to return mock collections
        mock_mongodb_service.get_database.return_value = mock_db
        mock_db.get_collection.side_effect = lambda name: {
            'radar_trends': mock_trends_collection
        }.get(name, MagicMock())

        # Mock the trends collection to return sample data
        mock_trends_collection.find.return_value = [
            {
                "_id": "123",
                "name": "Test Trend",
                "category": "Test Category",
                "stage": "Watch",
                "description": "Test description"
            }
        ]

        # Make a request to the API endpoint
        response = self.client.post('/trend-radar/api/query-trends', 
                                   json={"query": "test"})

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the expected data
        data = response.get_json()
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['name'], 'Test Trend')

if __name__ == '__main__':
    unittest.main()
