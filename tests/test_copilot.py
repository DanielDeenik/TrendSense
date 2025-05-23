"""
Test cases for AI Copilot feature.

This module contains test cases for the AI Copilot feature in TrendSense,
including routes, query processing, and UI components.
"""

import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from src.frontend.routes.copilot import CopilotRoute

class TestCopilotRoute(unittest.TestCase):
    """Test cases for AI Copilot route."""

    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True

    def test_copilot_route_exists(self):
        """Test that the copilot route exists."""
        response = self.app.get('/copilot')
        self.assertEqual(response.status_code, 200)

    def test_copilot_api_examples_route(self):
        """Test the copilot API examples route."""
        response = self.app.get('/copilot/api/examples')
        self.assertEqual(response.status_code, 200)

    def test_copilot_api_insights_route(self):
        """Test the copilot API insights route."""
        response = self.app.get('/copilot/api/insights')
        self.assertEqual(response.status_code, 200)

    def test_copilot_api_query_route(self):
        """Test the copilot API query route."""
        response = self.app.post('/copilot/api/query', json={
            'query': 'Test query'
        })
        self.assertEqual(response.status_code, 200)

    def test_copilot_api_query_route_missing_query(self):
        """Test the copilot API query route with missing query."""
        response = self.app.post('/copilot/api/query', json={})
        self.assertEqual(response.status_code, 400)

    @patch('src.database.database_service.database_service.find')
    def test_get_example_queries(self, mock_find):
        """Test the _get_example_queries method."""
        # Mock the database find method
        mock_find.return_value = [
            {
                "category": "Test Category",
                "query": "Test query",
                "description": "Test description"
            }
        ]
        
        # Create an instance of CopilotRoute
        copilot_route = CopilotRoute()
        
        # Call the method
        examples = copilot_route._get_example_queries()
        
        # Verify the result
        self.assertEqual(len(examples), 1)
        self.assertEqual(examples[0]['category'], 'Test Category')
        self.assertEqual(examples[0]['query'], 'Test query')
        
        # Verify the database method was called
        mock_find.assert_called_once_with('copilot_examples', sort=[('category', 1)], limit=10)

    @patch('src.database.database_service.database_service.find')
    def test_get_recent_insights(self, mock_find):
        """Test the _get_recent_insights method."""
        # Mock the database find method
        mock_find.return_value = [
            {
                "title": "Test Insight",
                "description": "Test description",
                "timestamp": "2023-05-21T12:00:00Z",
                "confidence": 90
            }
        ]
        
        # Create an instance of CopilotRoute
        copilot_route = CopilotRoute()
        
        # Call the method
        insights = copilot_route._get_recent_insights()
        
        # Verify the result
        self.assertEqual(len(insights), 1)
        self.assertEqual(insights[0]['title'], 'Test Insight')
        self.assertEqual(insights[0]['confidence'], 90)
        
        # Verify the database method was called
        mock_find.assert_called_once_with('copilot_insights', sort=[('timestamp', -1)], limit=5)

    def test_process_query(self):
        """Test the _process_query method."""
        # Create an instance of CopilotRoute
        copilot_route = CopilotRoute()
        
        # Test different query types
        query_types = {
            'compare': 'Compare A and B',
            'summarize': 'Summarize the trends',
            'predict': 'Predict future trends',
            'recommend': 'Recommend top companies'
        }
        
        for query_type, query in query_types.items():
            # Call the method
            response = copilot_route._process_query(query)
            
            # Verify the result
            self.assertIn('thinking', response)
            self.assertIn('response', response)
            self.assertIn('chart_type', response)
            self.assertEqual(response['query'], query)
            self.assertIn('timestamp', response)

    @patch('src.database.database_service.database_service.insert_one')
    def test_store_query(self, mock_insert_one):
        """Test the _store_query method."""
        # Create an instance of CopilotRoute
        copilot_route = CopilotRoute()
        
        # Create test data
        query = 'Test query'
        response = {
            'thinking': 'Test thinking',
            'response': 'Test response',
            'chart_type': 'bar',
            'query': query,
            'timestamp': '2023-05-21T12:00:00Z'
        }
        
        # Call the method
        copilot_route._store_query(query, response)
        
        # Verify the database method was called
        mock_insert_one.assert_called_once()
        args, kwargs = mock_insert_one.call_args
        self.assertEqual(args[0], 'copilot_queries')
        self.assertEqual(args[1]['query'], query)
        self.assertEqual(args[1]['response'], response)

    def test_copilot_template_rendering(self):
        """Test that the copilot template is rendered correctly."""
        with patch('flask.render_template') as mock_render:
            mock_render.return_value = "Mocked template"
            
            # Test copilot dashboard
            self.app.get('/copilot')
            mock_render.assert_called()
            
            # Verify that the correct template was used
            self.assertTrue(any('copilot.html' in call[0][0] for call in mock_render.call_args_list))

    def test_copilot_api_response(self):
        """Test the copilot API response."""
        with patch('src.frontend.routes.copilot.CopilotRoute._process_query') as mock_process_query:
            # Mock the query processing
            mock_process_query.return_value = {
                'thinking': 'Test thinking',
                'response': 'Test response',
                'chart_type': 'bar',
                'query': 'Test query',
                'timestamp': '2023-05-21T12:00:00Z'
            }
            
            # Test API response
            response = self.app.post('/copilot/api/query', json={
                'query': 'Test query'
            })
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.is_json)
            
            # Verify the response data
            data = response.get_json()
            self.assertEqual(data['thinking'], 'Test thinking')
            self.assertEqual(data['response'], 'Test response')
            self.assertEqual(data['chart_type'], 'bar')

if __name__ == '__main__':
    unittest.main()
