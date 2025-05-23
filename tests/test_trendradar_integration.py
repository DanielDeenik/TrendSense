"""
Test cases for the TrendRadar feature in the VC Lens module.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class TestTrendRadarIntegration(unittest.TestCase):
    """Test cases for the TrendRadar feature."""

    def setUp(self):
        """Set up the test client."""
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch('src.frontend.routes.vc_lens.mongodb_service')
    def test_trendradar_route_renders_template(self, mock_mongodb_service):
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
        response = self.client.get('/vc-lens/trendradar')

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is rendered
        self.assertIn(b'TrendRadar', response.data)
        self.assertIn(b'AI-powered VC/PE innovation trend analysis', response.data)

        # Check that it's properly integrated with VC Lens
        self.assertIn(b'VC Lens</a>', response.data)
        self.assertIn(b'<i class="fas fa-chevron-right mx-2 text-xs"></i>', response.data)
        self.assertIn(b'<span class="text-white">TrendRadar', response.data)

    @patch('src.frontend.routes.vc_lens.mongodb_service')
    def test_trendradar_route_with_mongodb_error(self, mock_mongodb_service):
        """Test that the TrendRadar route handles MongoDB errors gracefully."""
        # Mock MongoDB connection to raise an exception
        mock_mongodb_service.get_database.side_effect = Exception("MongoDB connection error")

        # Make a request to the TrendRadar route
        response = self.client.get('/vc-lens/trendradar')

        # Check that the response is successful (should render error template)
        self.assertEqual(response.status_code, 200)

        # Check that the error template is rendered
        self.assertIn(b'Error loading TrendRadar dashboard', response.data)

    @patch('src.frontend.routes.vc_lens.mongodb_service')
    def test_trendradar_navigation_integration(self, mock_mongodb_service):
        """Test that TrendRadar is properly integrated into the VC Lens navigation."""
        # Mock MongoDB connection
        mock_mongodb_service.is_connected.return_value = True

        # Make a request to the VC Lens route
        response = self.client.get('/vc-lens')

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the TrendRadar link is present in the VC Lens page
        self.assertIn(b'href="/vc-lens/trendradar"', response.data)
        self.assertIn(b'TrendRadar', response.data)

if __name__ == '__main__':
    unittest.main()
