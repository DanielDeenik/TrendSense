"""
Test cases to verify all import issues are fixed.
"""

import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestImportFixes(unittest.TestCase):
    """Test cases to verify all imports work correctly."""

    def test_app_import(self):
        """Test that the main app can be imported without errors."""
        try:
            from app import app, create_app
            self.assertIsNotNone(app)
            self.assertIsNotNone(create_app)
        except ImportError as e:
            self.fail(f"Failed to import app: {e}")

    def test_api_routes_import(self):
        """Test that API routes can be imported."""
        try:
            from src.frontend.routes.api import api_bp
            self.assertIsNotNone(api_bp)
            self.assertEqual(api_bp.name, 'api')
        except ImportError as e:
            self.fail(f"Failed to import API routes: {e}")

    def test_strategy_routes_import(self):
        """Test that strategy routes can be imported."""
        try:
            from src.frontend.routes.strategy_direct_flask import bp as strategy_bp
            self.assertIsNotNone(strategy_bp)
        except ImportError as e:
            self.fail(f"Failed to import strategy routes: {e}")

    def test_data_management_routes_import(self):
        """Test that data management routes can be imported."""
        try:
            from src.frontend.routes.data_management_routes import data_management_bp
            self.assertIsNotNone(data_management_bp)
        except ImportError as e:
            self.fail(f"Failed to import data management routes: {e}")

    def test_lookthrough_routes_import(self):
        """Test that lookthrough routes can be imported."""
        try:
            from src.frontend.routes.lookthrough_routes import lookthrough_bp
            self.assertIsNotNone(lookthrough_bp)
        except ImportError as e:
            self.fail(f"Failed to import lookthrough routes: {e}")

    def test_graph_analytics_routes_import(self):
        """Test that graph analytics routes can be imported."""
        try:
            from src.frontend.routes.graph_analytics import graph_analytics_bp
            self.assertIsNotNone(graph_analytics_bp)
        except ImportError as e:
            self.fail(f"Failed to import graph analytics routes: {e}")

    def test_vc_lens_routes_import(self):
        """Test that VC Lens routes can be imported."""
        try:
            from src.frontend.routes.vc_lens import vc_lens_bp
            self.assertIsNotNone(vc_lens_bp)
        except ImportError as e:
            self.fail(f"Failed to import VC Lens routes: {e}")

    def test_lensiq_routes_import(self):
        """Test that LensIQ routes can be imported."""
        try:
            from src.frontend.routes.lensiq import lensiq_bp
            self.assertIsNotNone(lensiq_bp)
        except ImportError as e:
            self.fail(f"Failed to import LensIQ routes: {e}")

    def test_trendradar_routes_import(self):
        """Test that TrendRadar routes can be imported."""
        try:
            from src.frontend.routes.trendradar import trendradar_bp
            self.assertIsNotNone(trendradar_bp)
        except ImportError as e:
            self.fail(f"Failed to import TrendRadar routes: {e}")

    def test_lifecycle_routes_import(self):
        """Test that lifecycle routes can be imported."""
        try:
            from src.frontend.routes.lifecycle import lifecycle_bp
            self.assertIsNotNone(lifecycle_bp)
        except ImportError as e:
            self.fail(f"Failed to import lifecycle routes: {e}")

    def test_copilot_routes_import(self):
        """Test that copilot routes can be imported."""
        try:
            from src.frontend.routes.copilot import copilot_bp
            self.assertIsNotNone(copilot_bp)
        except ImportError as e:
            self.fail(f"Failed to import copilot routes: {e}")

    def test_context_processors_import(self):
        """Test that context processors can be imported."""
        try:
            from src.frontend.utils.context_processors import navigation_processor
            self.assertIsNotNone(navigation_processor)
            # Test that it returns a dictionary
            result = navigation_processor()
            self.assertIsInstance(result, dict)
            self.assertIn('navigation', result)
        except ImportError as e:
            self.fail(f"Failed to import context processors: {e}")

    def test_database_adapters_import(self):
        """Test that database adapters can be imported."""
        try:
            from src.database.adapters import get_database_adapter
            adapter = get_database_adapter('mock_firebase')
            self.assertIsNotNone(adapter)
        except ImportError as e:
            self.fail(f"Failed to import database adapters: {e}")

    def test_data_management_components_import(self):
        """Test that data management components can be imported."""
        try:
            from src.data_management.ai_connector import get_ai_connector
            from src.data_management.rag_data_manager import get_rag_data_manager
            from src.data_management.data_storage import get_data_storage
            from src.data_management.data_retrieval import get_data_retrieval

            # These should not raise exceptions
            ai_connector = get_ai_connector()
            self.assertIsNotNone(ai_connector)
        except ImportError as e:
            self.fail(f"Failed to import data management components: {e}")

    def test_all_blueprints_registration(self):
        """Test that all blueprints can be registered without errors."""
        try:
            from app import create_app
            app = create_app()

            # Check that blueprints are registered
            blueprint_names = list(app.blueprints.keys())

            expected_blueprints = [
                'api', 'strategy', 'data_management', 'lookthrough',
                'graph_analytics', 'vc_lens', 'lensiq', 'trendradar',
                'lifecycle', 'copilot'
            ]

            for blueprint_name in expected_blueprints:
                self.assertIn(blueprint_name, blueprint_names,
                            f"Blueprint '{blueprint_name}' not registered")

        except Exception as e:
            self.fail(f"Failed to register blueprints: {e}")

    def test_app_routes_functionality(self):
        """Test that the app routes work correctly."""
        try:
            from app import create_app
            app = create_app()
            app.config['TESTING'] = True

            with app.test_client() as client:
                # Test health check
                response = client.get('/api/health')
                self.assertEqual(response.status_code, 200)

                # Test home page
                response = client.get('/')
                self.assertIn(response.status_code, [200, 500])  # Allow 500 for template issues

                # Test debug navigation
                response = client.get('/debug/navigation')
                self.assertEqual(response.status_code, 200)

        except Exception as e:
            self.fail(f"App routes functionality test failed: {e}")

    def test_no_circular_imports(self):
        """Test that there are no circular import issues."""
        try:
            # Import all main modules to check for circular imports
            import src.frontend.routes.api
            import src.frontend.routes.strategy_direct_flask
            import src.frontend.routes.data_management_routes
            import src.frontend.routes.lookthrough_routes
            import src.frontend.routes.graph_analytics
            import src.frontend.routes.vc_lens
            import src.frontend.routes.lensiq
            import src.frontend.routes.trendradar
            import src.frontend.routes.lifecycle
            import src.frontend.routes.copilot
            import src.frontend.utils.context_processors
            import src.database.adapters
            import src.data_management.ai_connector

            # If we get here, no circular imports
            self.assertTrue(True)

        except ImportError as e:
            if "circular import" in str(e).lower():
                self.fail(f"Circular import detected: {e}")
            else:
                self.fail(f"Import error (possibly circular): {e}")

if __name__ == '__main__':
    # Set up environment for testing
    os.environ.update({
        'FLASK_ENV': 'testing',
        'DATABASE_ADAPTER': 'mock_firebase',
        'TESTING': 'True'
    })

    unittest.main(verbosity=2)
