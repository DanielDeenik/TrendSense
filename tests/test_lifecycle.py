"""
Test cases for Lifecycle Analysis feature.

This module contains test cases for the Lifecycle Analysis feature in TrendSense,
including routes, database integration, and UI components.
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from src.frontend.routes.lifecycle import LifecycleRoute

class TestLifecycleRoute(unittest.TestCase):
    """Test cases for Lifecycle Analysis route."""

    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True

    def test_lifecycle_route_exists(self):
        """Test that the lifecycle route exists."""
        response = self.app.get('/lifecycle')
        self.assertEqual(response.status_code, 200)

    def test_lifecycle_api_metrics_route(self):
        """Test the lifecycle API metrics route."""
        response = self.app.get('/lifecycle/api/metrics')
        self.assertEqual(response.status_code, 200)

    def test_lifecycle_company_metrics_route(self):
        """Test the lifecycle company metrics route."""
        response = self.app.get('/lifecycle/metrics/eco-tech-solutions')
        self.assertEqual(response.status_code, 200)

    @patch('src.database.database_service.database_service.find')
    def test_get_companies(self, mock_find):
        """Test the _get_companies method."""
        # Mock the database find method
        mock_find.return_value = [
            {
                "id": "test-company",
                "name": "Test Company",
                "sector": "Test Sector",
                "valuation": 100000000,
                "founded": 2020,
                "sustainability_score": 90,
                "growth_rate": 30
            }
        ]
        
        # Create an instance of LifecycleRoute
        lifecycle_route = LifecycleRoute()
        
        # Call the method
        companies = lifecycle_route._get_companies()
        
        # Verify the result
        self.assertEqual(len(companies), 1)
        self.assertEqual(companies[0]['id'], 'test-company')
        self.assertEqual(companies[0]['name'], 'Test Company')
        
        # Verify the database method was called
        mock_find.assert_called_once_with('companies', sort=[('sustainability_score', -1)], limit=10)

    @patch('src.database.database_service.database_service.find_one')
    def test_get_company_by_id(self, mock_find_one):
        """Test the _get_company_by_id method."""
        # Mock the database find_one method
        mock_find_one.return_value = {
            "id": "test-company",
            "name": "Test Company",
            "sector": "Test Sector",
            "valuation": 100000000,
            "founded": 2020,
            "sustainability_score": 90,
            "growth_rate": 30
        }
        
        # Create an instance of LifecycleRoute
        lifecycle_route = LifecycleRoute()
        
        # Call the method
        company = lifecycle_route._get_company_by_id('test-company')
        
        # Verify the result
        self.assertEqual(company['id'], 'test-company')
        self.assertEqual(company['name'], 'Test Company')
        
        # Verify the database method was called
        mock_find_one.assert_called_once_with('companies', {'id': 'test-company'})

    @patch('src.database.database_service.database_service.find')
    def test_get_lifecycle_metrics(self, mock_find):
        """Test the _get_lifecycle_metrics method."""
        # Mock the database find method
        mock_find.return_value = [
            {
                "company_id": "test-company",
                "carbon_intensity": 15.0,
                "reuse_factor": 8.0,
                "csrd_compliance": 85,
                "water_usage": 40,
                "hazardous_waste": 0,
                "recyclable_materials": 95,
                "closed_loop_processes": 75,
                "social_impact": {
                    "jobs_created": 1000,
                    "fair_wage_certification": 90
                },
                "lp_ready": True
            }
        ]
        
        # Create an instance of LifecycleRoute
        lifecycle_route = LifecycleRoute()
        
        # Call the method
        metrics = lifecycle_route._get_lifecycle_metrics()
        
        # Verify the result
        self.assertEqual(len(metrics), 1)
        self.assertEqual(metrics[0]['company_id'], 'test-company')
        self.assertEqual(metrics[0]['carbon_intensity'], 15.0)
        
        # Verify the database method was called
        mock_find.assert_called_once_with('lifecycle_metrics', sort=[('company_id', 1)], limit=10)

    @patch('src.database.database_service.database_service.find_one')
    def test_get_company_lifecycle_metrics(self, mock_find_one):
        """Test the _get_company_lifecycle_metrics method."""
        # Mock the database find_one method
        mock_find_one.return_value = {
            "company_id": "test-company",
            "carbon_intensity": 15.0,
            "reuse_factor": 8.0,
            "csrd_compliance": 85,
            "water_usage": 40,
            "hazardous_waste": 0,
            "recyclable_materials": 95,
            "closed_loop_processes": 75,
            "social_impact": {
                "jobs_created": 1000,
                "fair_wage_certification": 90
            },
            "lp_ready": True
        }
        
        # Create an instance of LifecycleRoute
        lifecycle_route = LifecycleRoute()
        
        # Call the method
        metrics = lifecycle_route._get_company_lifecycle_metrics('test-company')
        
        # Verify the result
        self.assertEqual(metrics['company_id'], 'test-company')
        self.assertEqual(metrics['carbon_intensity'], 15.0)
        
        # Verify the database method was called
        mock_find_one.assert_called_once_with('lifecycle_metrics', {'company_id': 'test-company'})

    def test_lifecycle_template_rendering(self):
        """Test that the lifecycle template is rendered correctly."""
        with patch('flask.render_template') as mock_render:
            mock_render.return_value = "Mocked template"
            
            # Test lifecycle dashboard
            self.app.get('/lifecycle')
            mock_render.assert_called()
            
            # Verify that the correct template was used
            self.assertTrue(any('fin_lifecycle/fin_lifecycle_dashboard.html' in call[0][0] for call in mock_render.call_args_list))

    def test_lifecycle_api_response(self):
        """Test the lifecycle API response."""
        with patch('src.frontend.routes.lifecycle.LifecycleRoute._get_lifecycle_metrics') as mock_get_metrics:
            # Mock the metrics
            mock_get_metrics.return_value = [
                {
                    "company_id": "test-company",
                    "carbon_intensity": 15.0,
                    "reuse_factor": 8.0,
                    "csrd_compliance": 85
                }
            ]
            
            # Test API response
            response = self.app.get('/lifecycle/api/metrics')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.is_json)
            
            # Verify the response data
            data = response.get_json()
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['company_id'], 'test-company')

if __name__ == '__main__':
    unittest.main()
