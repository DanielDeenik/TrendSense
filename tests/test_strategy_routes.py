"""
Test cases for Strategy Hub routes.

This module contains test cases for the Strategy Hub routes.
"""

import unittest
import sys
import os
import json

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class TestStrategyRoutes(unittest.TestCase):
    """Test cases for Strategy Hub routes."""

    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True

    def test_strategy_hub_route(self):
        """Test Strategy Hub main route."""
        response = self.app.get('/strategy')
        self.assertEqual(response.status_code, 200)

    def test_framework_detail_route(self):
        """Test framework detail route."""
        # Test with a valid framework ID
        response = self.app.get('/strategy/framework/porters')
        self.assertEqual(response.status_code, 200)

        # Test with an invalid framework ID
        response = self.app.get('/strategy/framework/nonexistent')
        self.assertEqual(response.status_code, 404)

    def test_strategy_detail_route(self):
        """Test strategy detail route."""
        # Test with a valid strategy ID
        response = self.app.get('/strategy/strategy/1')
        self.assertEqual(response.status_code, 200)

        # Test with an invalid strategy ID
        response = self.app.get('/strategy/strategy/999')
        self.assertEqual(response.status_code, 404)

    def test_strategy_edit_route(self):
        """Test strategy edit route."""
        # Test with a valid strategy ID
        response = self.app.get('/strategy/strategy/1/edit')
        self.assertEqual(response.status_code, 200)

        # Test with an invalid strategy ID
        response = self.app.get('/strategy/strategy/999/edit')
        self.assertEqual(response.status_code, 404)

    def test_strategy_execute_route(self):
        """Test strategy execute route."""
        response = self.app.get('/strategy/execute')
        self.assertEqual(response.status_code, 200)

    def test_strategy_storytelling_route(self):
        """Test strategy storytelling route."""
        response = self.app.get('/strategy/storytelling')
        self.assertEqual(response.status_code, 200)

    def test_shared_story_route(self):
        """Test shared story route."""
        response = self.app.get('/strategy/story/test123')
        self.assertEqual(response.status_code, 200)

    def test_api_frameworks_route(self):
        """Test API frameworks route."""
        response = self.app.get('/strategy/api/frameworks')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('porters', data)
        self.assertIn('swot', data)
        self.assertIn('bcg', data)

    def test_api_strategies_route(self):
        """Test API strategies route."""
        response = self.app.get('/strategy/api/strategies')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))
        self.assertGreater(len(data), 0)
        self.assertIn('id', data[0])
        self.assertIn('name', data[0])
        self.assertIn('framework', data[0])

    def test_execute_strategy_api(self):
        """Test execute strategy API."""
        # Prepare test data
        test_data = {
            'strategy_id': 1,
            'data_source': 'sustainability_metrics',
            'time_period': '1y',
            'visualization_type': 'bar'
        }

        # Send POST request
        response = self.app.post(
            '/strategy/execute-api',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        # Check response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('summary', data)
        self.assertIn('primary_chart', data)
        self.assertIn('secondary_chart', data)
        self.assertIn('table_data', data)
        self.assertIn('insights', data)

    def test_storytelling_api(self):
        """Test storytelling API."""
        # Prepare test data
        test_data = {
            'strategy_id': 1,
            'data_source': 'sustainability_metrics',
            'narrative_type': 'impact',
            'audience': 'stakeholders'
        }

        # Send POST request
        response = self.app.post(
            '/strategy/storytelling-api',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        # Check response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('narrative', data)
        self.assertIn('viral_potential', data)
        self.assertIn('story_chart', data)
        self.assertIn('contagious_chart', data)
        self.assertIn('benchmarks', data)
        self.assertIn('data', data['benchmarks'])
        self.assertIn('insights', data['benchmarks'])
        self.assertIn('recommendations', data)

if __name__ == '__main__':
    unittest.main()
