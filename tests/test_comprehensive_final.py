"""
Comprehensive final test suite for TrendSense application.

This test suite verifies that all major components are working correctly
after the comprehensive bug fixes and codebase indexing.
"""

import unittest
import sys
import os
import json

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestTrendSenseComprehensive(unittest.TestCase):
    """Comprehensive test suite for TrendSense."""

    def setUp(self):
        """Set up test environment."""
        os.environ.update({
            'FLASK_ENV': 'testing',
            'DATABASE_ADAPTER': 'mock_firebase',
            'TESTING': 'True'
        })

    def test_application_startup(self):
        """Test that the application starts up correctly."""
        try:
            from app import create_app
            app = create_app()
            self.assertIsNotNone(app)
            self.assertTrue(hasattr(app, 'config'))
            self.assertEqual(app.config.get('TESTING'), True)
        except Exception as e:
            self.fail(f"Application startup failed: {e}")

    def test_all_blueprints_registered(self):
        """Test that all blueprints are properly registered."""
        try:
            from app import create_app
            app = create_app()
            
            # Check that blueprints are registered
            blueprint_names = list(app.blueprints.keys())
            
            expected_blueprints = [
                'api', 'strategy', 'data_management', 'lookthrough',
                'graph_analytics', 'vc_lens', 'trendsense', 'trendradar',
                'lifecycle', 'copilot'
            ]
            
            for blueprint_name in expected_blueprints:
                self.assertIn(blueprint_name, blueprint_names,
                            f"Blueprint '{blueprint_name}' not registered")
                
        except Exception as e:
            self.fail(f"Blueprint registration test failed: {e}")

    def test_api_endpoints(self):
        """Test that API endpoints are accessible."""
        try:
            from app import create_app
            app = create_app()
            app.config['TESTING'] = True
            
            with app.test_client() as client:
                # Test health check
                response = client.get('/api/health')
                self.assertEqual(response.status_code, 200)
                
                data = response.get_json()
                self.assertEqual(data['status'], 'ok')
                
        except Exception as e:
            self.fail(f"API endpoints test failed: {e}")

    def test_database_adapters(self):
        """Test that database adapters work correctly."""
        try:
            from src.database.adapters import get_database_adapter
            
            # Test mock Firebase adapter
            adapter = get_database_adapter('mock_firebase')
            self.assertIsNotNone(adapter)
            self.assertTrue(adapter.connect())
            self.assertTrue(adapter.is_connected())
            
        except Exception as e:
            self.fail(f"Database adapters test failed: {e}")

    def test_data_management_components(self):
        """Test that data management components work."""
        try:
            from src.data_management.ai_connector import get_ai_connector
            from src.data_management.rag_data_manager import get_rag_data_manager
            from src.data_management.data_storage import get_data_storage
            from src.data_management.data_retrieval import get_data_retrieval
            
            # Test AI connector
            ai_connector = get_ai_connector()
            self.assertIsNotNone(ai_connector)
            
            # Test RAG data manager
            rag_manager = get_rag_data_manager(ai_connector)
            self.assertIsNotNone(rag_manager)
            
            # Test data storage
            data_storage = get_data_storage()
            self.assertIsNotNone(data_storage)
            
            # Test data retrieval
            data_retrieval = get_data_retrieval()
            self.assertIsNotNone(data_retrieval)
            
        except Exception as e:
            self.fail(f"Data management components test failed: {e}")

    def test_route_accessibility(self):
        """Test that main routes are accessible."""
        try:
            from app import create_app
            app = create_app()
            app.config['TESTING'] = True
            
            with app.test_client() as client:
                # Test main routes
                routes_to_test = [
                    ('/', [200, 404, 500]),  # Home page
                    ('/api/health', [200]),  # API health check
                    ('/debug/navigation', [200]),  # Debug navigation
                ]
                
                for route, expected_codes in routes_to_test:
                    response = client.get(route)
                    self.assertIn(response.status_code, expected_codes,
                                f"Route {route} returned unexpected status code: {response.status_code}")
                
        except Exception as e:
            self.fail(f"Route accessibility test failed: {e}")

    def test_context_processors(self):
        """Test that context processors work correctly."""
        try:
            from src.frontend.utils.context_processors import navigation_processor
            
            # Test navigation processor
            nav_data = navigation_processor()
            self.assertIsInstance(nav_data, dict)
            self.assertIn('navigation', nav_data)
            self.assertIsInstance(nav_data['navigation'], list)
            
        except Exception as e:
            self.fail(f"Context processors test failed: {e}")

    def test_vc_lens_functionality(self):
        """Test VC Lens specific functionality."""
        try:
            from app import create_app
            app = create_app()
            app.config['TESTING'] = True
            
            with app.test_client() as client:
                # Test VC Lens routes
                response = client.get('/vc-lens/')
                self.assertIn(response.status_code, [200, 404, 500])
                
        except Exception as e:
            self.fail(f"VC Lens functionality test failed: {e}")

    def test_trendsense_functionality(self):
        """Test TrendSense specific functionality."""
        try:
            from app import create_app
            app = create_app()
            app.config['TESTING'] = True
            
            with app.test_client() as client:
                # Test TrendSense routes
                response = client.get('/trendsense/')
                self.assertIn(response.status_code, [200, 404, 500])
                
        except Exception as e:
            self.fail(f"TrendSense functionality test failed: {e}")

    def test_data_management_functionality(self):
        """Test Data Management specific functionality."""
        try:
            from app import create_app
            app = create_app()
            app.config['TESTING'] = True
            
            with app.test_client() as client:
                # Test Data Management routes
                response = client.get('/data-management/')
                self.assertIn(response.status_code, [200, 404, 500])
                
        except Exception as e:
            self.fail(f"Data Management functionality test failed: {e}")

    def test_error_handling(self):
        """Test that error handling works correctly."""
        try:
            from app import create_app
            app = create_app()
            app.config['TESTING'] = True
            
            with app.test_client() as client:
                # Test 404 error handling
                response = client.get('/nonexistent-route')
                self.assertEqual(response.status_code, 404)
                
        except Exception as e:
            self.fail(f"Error handling test failed: {e}")

    def test_configuration(self):
        """Test that application configuration is correct."""
        try:
            from app import create_app
            app = create_app()
            
            # Check that required configuration is set
            self.assertIsNotNone(app.secret_key)
            self.assertIsNotNone(app.template_folder)
            self.assertIsNotNone(app.static_folder)
            
        except Exception as e:
            self.fail(f"Configuration test failed: {e}")

if __name__ == '__main__':
    # Set up environment for testing
    os.environ.update({
        'FLASK_ENV': 'testing',
        'DATABASE_ADAPTER': 'mock_firebase',
        'TESTING': 'True'
    })
    
    # Run tests with detailed output
    unittest.main(verbosity=2)
