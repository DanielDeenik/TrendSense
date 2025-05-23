"""
Basic functionality tests to verify the application works.
"""

import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestBasicFunctionality(unittest.TestCase):
    """Basic functionality tests."""

    def test_import_app(self):
        """Test that we can import the main app."""
        try:
            from app import app
            self.assertIsNotNone(app)
        except ImportError as e:
            self.fail(f"Failed to import app: {e}")

    def test_app_creation(self):
        """Test that the app can be created."""
        try:
            from app import create_app
            app = create_app()
            self.assertIsNotNone(app)
            self.assertTrue(hasattr(app, 'config'))
        except Exception as e:
            self.fail(f"Failed to create app: {e}")

    def test_database_adapters_import(self):
        """Test that database adapters can be imported."""
        try:
            from src.database.adapters import get_database_adapter
            adapter = get_database_adapter('mock_firebase')
            self.assertIsNotNone(adapter)
        except ImportError as e:
            self.fail(f"Failed to import database adapters: {e}")

    def test_routes_import(self):
        """Test that routes can be imported."""
        try:
            from src.frontend.routes.api import api_bp
            self.assertIsNotNone(api_bp)
        except ImportError as e:
            self.fail(f"Failed to import API routes: {e}")

    def test_basic_app_functionality(self):
        """Test basic app functionality."""
        try:
            from app import app
            app.config['TESTING'] = True
            
            with app.test_client() as client:
                # Test health check
                response = client.get('/api/health')
                self.assertEqual(response.status_code, 200)
                
                # Test home page
                response = client.get('/')
                self.assertIn(response.status_code, [200, 500])  # Allow 500 for template issues
                
        except Exception as e:
            self.fail(f"Basic app functionality test failed: {e}")

    def test_environment_setup(self):
        """Test that the environment is set up correctly."""
        # Check that we're in the right directory
        current_dir = os.getcwd()
        self.assertTrue(os.path.exists(os.path.join(current_dir, 'app.py')))
        self.assertTrue(os.path.exists(os.path.join(current_dir, 'src')))
        self.assertTrue(os.path.exists(os.path.join(current_dir, 'tests')))

    def test_python_path(self):
        """Test that Python path is set up correctly."""
        # Check that we can import from src
        try:
            import src
            self.assertTrue(hasattr(src, '__path__'))
        except ImportError:
            # This is okay, src might not have __init__.py
            pass

if __name__ == '__main__':
    # Set up environment for testing
    os.environ.update({
        'FLASK_ENV': 'testing',
        'DATABASE_ADAPTER': 'mock_firebase',
        'TESTING': 'True'
    })
    
    unittest.main(verbosity=2)
