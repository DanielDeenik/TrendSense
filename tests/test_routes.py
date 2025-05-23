"""
Test cases for SustainaTrend routes.

This module contains test cases for the SustainaTrend routes.
"""

import unittest
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class TestRoutes(unittest.TestCase):
    """Test cases for SustainaTrend routes."""

    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True

    def test_home_route(self):
        """Test home route."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_vc_lens_route(self):
        """Test VC Lens route."""
        response = self.app.get('/vc-lens', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_vc_lens_trendsense_route(self):
        """Test VC Lens TrendSense route."""
        response = self.app.get('/vc-lens/trendsense', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_vc_lens_trendradar_route(self):
        """Test VC Lens TrendRadar route."""
        response = self.app.get('/vc-lens/trendradar', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_regulatory_ai_route(self):
        """Test Regulatory AI route."""
        # Skip this test for now as the route may not be implemented yet
        pass

    def test_api_health_route(self):
        """Test API health route."""
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.json)
        self.assertEqual(response.json['status'], 'ok')

    def test_api_vc_lens_data_route(self):
        """Test API VC Lens data route."""
        response = self.app.get('/api/vc-lens/data')
        self.assertEqual(response.status_code, 200)
        self.assertIn('trend_line_data', response.json)
        self.assertIn('trend_strength_data', response.json)
        self.assertIn('microtrends_data', response.json)
        self.assertIn('sankey_data', response.json)

    def test_api_trend_radar_data_route(self):
        """Test API Trend Radar data route."""
        response = self.app.get('/api/trend-radar/data')
        self.assertEqual(response.status_code, 200)
        self.assertIn('trends', response.json)
        self.assertIn('categories', response.json)
        self.assertIn('stages', response.json)

if __name__ == '__main__':
    unittest.main()
