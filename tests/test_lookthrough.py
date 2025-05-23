"""
Tests for the Look Through Engine functionality.
"""

import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the src directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the app
from app import app

# Import Look Through Engine components
from src.lookthrough.entity_traversal import EntityTraversal
from src.lookthrough.metrics_propagator import MetricsProgagator

class TestLookThroughEngine(unittest.TestCase):
    """Test cases for the Look Through Engine functionality."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create a Flask test client
        self.app = app.test_client()
        self.app.testing = True
        
        # Create mock objects
        self.mock_db = MagicMock()
        self.mock_db.funds.find_one.return_value = {
            "_id": "fund1",
            "name": "Test Fund",
            "aum": 1000000,
            "currency": "USD",
            "portfolio_companies": ["company1", "company2"]
        }
        self.mock_db.companies.find_one.return_value = {
            "_id": "company1",
            "name": "Test Company",
            "sector": "Technology",
            "stage": "Series A",
            "projects": ["project1", "project2"]
        }
        self.mock_db.projects.find_one.return_value = {
            "_id": "project1",
            "name": "Test Project",
            "company_id": "company1",
            "status": "In Progress"
        }
        
        # Create a patch for the MongoDB service
        self.mongodb_service_patch = patch('src.lookthrough.entity_traversal.mongodb_service')
        self.mock_mongodb_service = self.mongodb_service_patch.start()
        self.mock_mongodb_service.db = self.mock_db
        
        # Create a patch for the metrics propagator
        self.metrics_propagator_patch = patch('src.lookthrough.metrics_propagator.mongodb_service')
        self.mock_metrics_propagator = self.metrics_propagator_patch.start()
        self.mock_metrics_propagator.db = self.mock_db
    
    def tearDown(self):
        """Tear down the test environment."""
        # Stop the patches
        self.mongodb_service_patch.stop()
        self.metrics_propagator_patch.stop()
    
    def test_lookthrough_routes(self):
        """Test Look Through Engine routes."""
        # Test index route
        response = self.app.get('/lookthrough/')
        self.assertEqual(response.status_code, 200)
        
        # Test fund view route
        response = self.app.get('/lookthrough/fund/fund1')
        self.assertEqual(response.status_code, 200)
        
        # Test company view route
        response = self.app.get('/lookthrough/company/company1')
        self.assertEqual(response.status_code, 200)
        
        # Test project view route
        response = self.app.get('/lookthrough/project/project1')
        self.assertEqual(response.status_code, 200)
    
    def test_entity_traversal(self):
        """Test entity traversal functionality."""
        # Create an entity traversal instance
        entity_traversal = EntityTraversal()
        
        # Test get_fund_hierarchy
        fund_hierarchy = entity_traversal.get_fund_hierarchy("fund1")
        self.assertTrue(fund_hierarchy.get('success', False))
        
        # Test get_company_hierarchy
        company_hierarchy = entity_traversal.get_company_hierarchy("company1")
        self.assertTrue(company_hierarchy.get('success', False))
        
        # Test get_project_hierarchy
        project_hierarchy = entity_traversal.get_project_hierarchy("project1")
        self.assertTrue(project_hierarchy.get('success', False))
    
    def test_metrics_propagation(self):
        """Test metrics propagation functionality."""
        # Create a metrics propagator instance
        metrics_propagator = MetricsProgagator()
        
        # Test propagate_metrics
        result = metrics_propagator.propagate_metrics("fund1")
        self.assertTrue(result.get('success', False))
    
    def test_api_endpoints(self):
        """Test API endpoints."""
        # Test get funds API
        response = self.app.get('/lookthrough/api/funds')
        self.assertEqual(response.status_code, 200)
        
        # Test get companies API
        response = self.app.get('/lookthrough/api/companies')
        self.assertEqual(response.status_code, 200)
        
        # Test get projects API
        response = self.app.get('/lookthrough/api/projects')
        self.assertEqual(response.status_code, 200)
        
        # Test get fund API
        response = self.app.get('/lookthrough/api/fund/fund1')
        self.assertEqual(response.status_code, 200)
        
        # Test get company API
        response = self.app.get('/lookthrough/api/company/company1')
        self.assertEqual(response.status_code, 200)
        
        # Test get project API
        response = self.app.get('/lookthrough/api/project/project1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
