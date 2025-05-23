"""
Comprehensive test suite for TrendSense application.

This module contains a comprehensive test suite that tests all routes, features,
and functionality of the TrendSense application.
"""

import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class TestComprehensive(unittest.TestCase):
    """Comprehensive test suite for TrendSense application."""

    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        """Clean up after tests."""
        pass

    # Core Routes Tests
    def test_all_core_routes(self):
        """Test all core routes of the application."""
        routes = [
            '/',                        # Home
            '/vc-lens',                 # VC Lens
            '/trendsense',              # TrendSense
            '/trendradar',              # TrendRadar
            '/graph-analytics',         # Graph Analytics
            '/strategy',                # Strategy
            '/data-management',         # Data Management
            '/lookthrough',             # Lookthrough
            '/lifecycle',               # Lifecycle Analysis
            '/copilot',                 # Copilot
        ]
        
        for route in routes:
            response = self.app.get(route, follow_redirects=True)
            self.assertEqual(response.status_code, 200, f"Route {route} failed with status code {response.status_code}")
    
    # API Routes Tests
    def test_all_api_routes(self):
        """Test all API routes of the application."""
        api_routes = [
            '/api/health',                      # Health check
            '/api/vc-lens/data',                # VC Lens data
            '/api/trend-radar/data',            # Trend Radar data
            '/api/trendsense/data',             # TrendSense data
            '/api/graph-analytics/data',        # Graph Analytics data
            '/api/strategy/data',               # Strategy data
            '/api/lookthrough/data',            # Lookthrough data
            '/api/lifecycle/metrics',           # Lifecycle metrics
            '/api/copilot/examples',            # Copilot examples
        ]
        
        for route in api_routes:
            response = self.app.get(route)
            self.assertEqual(response.status_code, 200, f"API route {route} failed with status code {response.status_code}")
            self.assertTrue(response.is_json, f"API route {route} did not return JSON")
    
    # Database Integration Tests
    @patch('src.database.database_service.database_service.connect')
    @patch('src.database.database_service.database_service.find')
    def test_database_integration(self, mock_find, mock_connect):
        """Test database integration."""
        # Mock database connection
        mock_connect.return_value = True
        
        # Mock database find method
        mock_find.return_value = [
            {"id": "test-company", "name": "Test Company", "sustainability_score": 85}
        ]
        
        # Test route that uses database
        response = self.app.get('/lifecycle')
        self.assertEqual(response.status_code, 200)
        
        # Verify database methods were called
        mock_connect.assert_called_once()
        mock_find.assert_called()
    
    # Firebase Integration Tests
    @patch('src.database.adapters.firebase_adapter.FirebaseAdapter.connect')
    @patch('src.database.adapters.firebase_adapter.FirebaseAdapter.find')
    def test_firebase_integration(self, mock_find, mock_connect):
        """Test Firebase integration."""
        # Mock Firebase connection
        mock_connect.return_value = True
        
        # Mock Firebase find method
        mock_find.return_value = [
            {"id": "test-trend", "name": "Test Trend", "strength": 85}
        ]
        
        # Test route that uses Firebase
        response = self.app.get('/trendsense')
        self.assertEqual(response.status_code, 200)
        
        # Verify Firebase methods were called
        mock_connect.assert_called_once()
        mock_find.assert_called()
    
    # TourMode Integration Tests
    def test_tourmode_integration(self):
        """Test TourMode integration with all routes."""
        routes = [
            '/',
            '/vc-lens',
            '/trendsense',
            '/trendradar',
            '/graph-analytics',
            '/strategy',
            '/lifecycle',
            '/copilot',
        ]
        
        for route in routes:
            response = self.app.get(f"{route}?tour=true", follow_redirects=True)
            self.assertEqual(response.status_code, 200, f"Route {route} with tour=true failed with status code {response.status_code}")
    
    # Form Submission Tests
    def test_form_submissions(self):
        """Test form submissions."""
        # Test data management form
        response = self.app.post('/data-management/upload', data={
            'file': (io.BytesIO(b'test data'), 'test.csv'),
            'type': 'csv'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Test strategy form
        response = self.app.post('/strategy/create', data={
            'name': 'Test Strategy',
            'description': 'Test Description'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Test help form
        response = self.app.post('/api/help', json={
            'issue': 'Test Issue',
            'context': 'Test Context'
        })
        self.assertEqual(response.status_code, 200)
    
    # Error Handling Tests
    def test_error_handling(self):
        """Test error handling."""
        # Test 404 error
        response = self.app.get('/nonexistent-route')
        self.assertEqual(response.status_code, 404)
        
        # Test 500 error (by triggering an exception)
        with patch('app.render_template', side_effect=Exception('Test exception')):
            response = self.app.get('/')
            self.assertEqual(response.status_code, 500)
    
    # JavaScript Integration Tests
    def test_javascript_files_exist(self):
        """Test that all JavaScript files exist."""
        js_files = [
            '/static/js/tour-configs.js',
            '/static/js/tour-mode.js',
            '/static/js/tour_config.js',
            '/static/js/tour-help-logger.js',
            '/static/js/tour-copilot-responses.js',
            '/static/js/navigation-helper.js',
            '/static/js/ai-tooltips.js',
            '/static/js/chart-helpers.js',
            '/static/js/data-visualization.js',
            '/static/js/graph-analytics.js',
            '/static/js/trend-radar.js',
            '/static/js/vc-lens.js',
            '/static/js/lifecycle-analysis.js',
            '/static/js/copilot.js',
        ]
        
        for js_file in js_files:
            response = self.app.get(js_file)
            self.assertEqual(response.status_code, 200, f"JavaScript file {js_file} not found")
    
    # Template Integration Tests
    def test_template_inheritance(self):
        """Test template inheritance."""
        with patch('flask.render_template') as mock_render:
            mock_render.return_value = "Mocked template"
            
            # Test home page
            self.app.get('/')
            mock_render.assert_called_with('fin_home.html', active_nav='home', navigation=unittest.mock.ANY)
            
            # Test VC Lens page
            self.app.get('/vc-lens')
            self.assertTrue(any('fin_vc_lens/fin_vc_lens.html' in call[0][0] for call in mock_render.call_args_list))
    
    # Component Integration Tests
    def test_component_inclusion(self):
        """Test component inclusion."""
        with patch('flask.render_template') as mock_render:
            mock_render.return_value = "Mocked template"
            
            # Test help modal inclusion
            self.app.get('/?tour=true')
            self.assertTrue(any('components/help_modal.html' in str(call) for call in mock_render.mock_calls))
            
            # Test tour button inclusion
            self.app.get('/?tour=true')
            self.assertTrue(any('components/tour_button.html' in str(call) for call in mock_render.mock_calls))
    
    # Data Visualization Tests
    def test_data_visualization(self):
        """Test data visualization."""
        # Test chart.js integration
        response = self.app.get('/static/js/chart-helpers.js')
        self.assertEqual(response.status_code, 200)
        
        # Test d3.js integration
        response = self.app.get('/static/js/graph-analytics.js')
        self.assertEqual(response.status_code, 200)
        
        # Test plotly integration
        response = self.app.get('/static/js/data-visualization.js')
        self.assertEqual(response.status_code, 200)
    
    # Navigation Tests
    def test_navigation(self):
        """Test navigation."""
        # Test navigation links
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Check for navigation links in the response
        self.assertIn(b'href="/vc-lens"', response.data)
        self.assertIn(b'href="/trendsense"', response.data)
        self.assertIn(b'href="/trendradar"', response.data)
        self.assertIn(b'href="/graph-analytics"', response.data)
        self.assertIn(b'href="/strategy"', response.data)
        self.assertIn(b'href="/data-management"', response.data)
        self.assertIn(b'href="/lifecycle"', response.data)
        self.assertIn(b'href="/copilot"', response.data)
    
    # Theme Tests
    def test_theme(self):
        """Test theme functionality."""
        # Test dark theme
        response = self.app.get('/?theme=dark')
        self.assertEqual(response.status_code, 200)
        
        # Test light theme
        response = self.app.get('/?theme=light')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
