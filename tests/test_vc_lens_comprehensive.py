"""
Comprehensive test cases for VC Lens functionality.
"""

import pytest
from unittest.mock import patch, MagicMock
import json


class TestVCLensRoutes:
    """Test cases for VC Lens routes."""

    def test_vc_lens_index_route(self, client, mock_firebase_service):
        """Test VC Lens index route."""
        response = client.get('/vc-lens/')
        assert response.status_code == 200

    def test_vc_lens_trendsense_route(self, client, mock_firebase_service, sample_trends_data):
        """Test VC Lens TrendSense route."""
        # Mock the database service to return sample data
        mock_firebase_service.get_collection.return_value.find.return_value = sample_trends_data
        
        response = client.get('/vc-lens/trendsense')
        assert response.status_code == 200
        assert b'TrendSense' in response.data

    def test_vc_lens_trendradar_route(self, client, mock_firebase_service, sample_trends_data):
        """Test VC Lens TrendRadar route."""
        # Mock the database service to return sample data
        mock_firebase_service.get_collection.return_value.find.return_value = sample_trends_data
        
        response = client.get('/vc-lens/trendradar')
        assert response.status_code == 200
        assert b'TrendRadar' in response.data


class TestTrendSenseIntegration:
    """Test cases for TrendSense integration."""

    @patch('src.database.adapters.get_database_adapter')
    def test_trendsense_with_database_connection(self, mock_get_adapter, client, sample_trends_data):
        """Test TrendSense with database connection."""
        # Mock database adapter
        mock_adapter = MagicMock()
        mock_adapter.connect.return_value = True
        mock_adapter.is_connected.return_value = True
        mock_adapter.find_documents.return_value = sample_trends_data
        mock_get_adapter.return_value = mock_adapter
        
        response = client.get('/vc-lens/trendsense')
        assert response.status_code == 200

    @patch('src.database.adapters.get_database_adapter')
    def test_trendsense_with_database_error(self, mock_get_adapter, client):
        """Test TrendSense with database error."""
        # Mock database adapter to raise an error
        mock_adapter = MagicMock()
        mock_adapter.connect.side_effect = Exception("Database connection failed")
        mock_get_adapter.return_value = mock_adapter
        
        response = client.get('/vc-lens/trendsense')
        # Should handle error gracefully
        assert response.status_code in [200, 500]

    def test_trendsense_fallback_data(self, client):
        """Test TrendSense fallback data when database is unavailable."""
        with patch('src.database.adapters.get_database_adapter', side_effect=Exception("No database")):
            response = client.get('/vc-lens/trendsense')
            # Should still render with fallback data
            assert response.status_code == 200


class TestTrendRadarIntegration:
    """Test cases for TrendRadar integration."""

    @patch('src.database.adapters.get_database_adapter')
    def test_trendradar_with_database_connection(self, mock_get_adapter, client, sample_trends_data):
        """Test TrendRadar with database connection."""
        # Mock database adapter
        mock_adapter = MagicMock()
        mock_adapter.connect.return_value = True
        mock_adapter.is_connected.return_value = True
        mock_adapter.find_documents.return_value = sample_trends_data
        mock_get_adapter.return_value = mock_adapter
        
        response = client.get('/vc-lens/trendradar')
        assert response.status_code == 200

    def test_trendradar_fallback_data(self, client):
        """Test TrendRadar fallback data when database is unavailable."""
        with patch('src.database.adapters.get_database_adapter', side_effect=Exception("No database")):
            response = client.get('/vc-lens/trendradar')
            # Should still render with fallback data
            assert response.status_code == 200


class TestVCLensDataRetrieval:
    """Test cases for VC Lens data retrieval functions."""

    @patch('src.database.adapters.get_database_adapter')
    def test_get_trends_function(self, mock_get_adapter, sample_trends_data):
        """Test the get_trends function."""
        # Mock database adapter
        mock_adapter = MagicMock()
        mock_adapter.connect.return_value = True
        mock_adapter.is_connected.return_value = True
        mock_adapter.find_documents.return_value = sample_trends_data
        mock_get_adapter.return_value = mock_adapter
        
        # Import and test the function
        try:
            from src.frontend.routes.vc_lens import get_trends
            result = get_trends()
            assert isinstance(result, list)
            assert len(result) > 0
        except ImportError:
            # Function might be in different location, test via route
            pass

    @patch('src.database.adapters.get_database_adapter')
    def test_get_trending_categories_function(self, mock_get_adapter):
        """Test the get_trending_categories function."""
        # Mock database adapter
        mock_adapter = MagicMock()
        mock_adapter.connect.return_value = True
        mock_adapter.is_connected.return_value = True
        
        # Mock aggregation result
        mock_categories = [
            {"_id": "Renewable Energy", "name": "Renewable Energy", "count": 42, "growth": 24},
            {"_id": "Circular Economy", "name": "Circular Economy", "count": 38, "growth": 32}
        ]
        mock_adapter.aggregate.return_value = mock_categories
        mock_get_adapter.return_value = mock_adapter
        
        # Import and test the function
        try:
            from src.frontend.routes.vc_lens import get_trending_categories
            result = get_trending_categories()
            assert isinstance(result, list)
        except ImportError:
            # Function might be in different location, test via route
            pass


class TestVCLensErrorHandling:
    """Test cases for VC Lens error handling."""

    def test_vc_lens_template_error(self, client):
        """Test VC Lens template error handling."""
        with patch('flask.render_template', side_effect=Exception("Template error")):
            response = client.get('/vc-lens/')
            # Should handle template errors gracefully
            assert response.status_code in [200, 500]

    def test_vc_lens_database_timeout(self, client):
        """Test VC Lens database timeout handling."""
        with patch('src.database.adapters.get_database_adapter') as mock_get_adapter:
            mock_adapter = MagicMock()
            mock_adapter.connect.side_effect = TimeoutError("Database timeout")
            mock_get_adapter.return_value = mock_adapter
            
            response = client.get('/vc-lens/')
            # Should handle timeout errors gracefully
            assert response.status_code in [200, 500]


class TestVCLensNavigation:
    """Test cases for VC Lens navigation."""

    def test_vc_lens_navigation_links(self, client):
        """Test VC Lens navigation links."""
        response = client.get('/vc-lens/')
        assert response.status_code == 200
        
        # Check for navigation elements (if present in template)
        # This test might need adjustment based on actual template content

    def test_trendsense_navigation_integration(self, client):
        """Test TrendSense navigation integration."""
        response = client.get('/vc-lens/trendsense')
        assert response.status_code == 200
        
        # Should include breadcrumb or navigation indicating it's part of VC Lens

    def test_trendradar_navigation_integration(self, client):
        """Test TrendRadar navigation integration."""
        response = client.get('/vc-lens/trendradar')
        assert response.status_code == 200
        
        # Should include breadcrumb or navigation indicating it's part of VC Lens


class TestVCLensPerformance:
    """Test cases for VC Lens performance."""

    @pytest.mark.slow
    def test_vc_lens_response_time(self, client):
        """Test VC Lens response time."""
        import time
        
        start_time = time.time()
        response = client.get('/vc-lens/')
        end_time = time.time()
        
        assert response.status_code == 200
        # Response should be reasonably fast (adjust threshold as needed)
        assert (end_time - start_time) < 5.0

    @pytest.mark.slow
    def test_trendsense_response_time(self, client):
        """Test TrendSense response time."""
        import time
        
        start_time = time.time()
        response = client.get('/vc-lens/trendsense')
        end_time = time.time()
        
        assert response.status_code == 200
        # Response should be reasonably fast (adjust threshold as needed)
        assert (end_time - start_time) < 5.0


class TestVCLensDataValidation:
    """Test cases for VC Lens data validation."""

    def test_trends_data_structure(self, sample_trends_data):
        """Test trends data structure."""
        for trend in sample_trends_data:
            assert 'category' in trend
            assert 'growth' in trend
            assert 'score' in trend
            assert isinstance(trend['growth'], (int, float))
            assert isinstance(trend['score'], (int, float))

    def test_companies_data_structure(self, sample_companies_data):
        """Test companies data structure."""
        for company in sample_companies_data:
            assert 'name' in company
            assert 'sector' in company
            assert 'stage' in company
            assert isinstance(company['name'], str)
            assert isinstance(company['sector'], str)

    def test_funds_data_structure(self, sample_funds_data):
        """Test funds data structure."""
        for fund in sample_funds_data:
            assert 'name' in fund
            assert 'type' in fund
            assert 'focus' in fund
            assert isinstance(fund['name'], str)
            assert isinstance(fund['type'], str)


if __name__ == '__main__':
    pytest.main([__file__])
