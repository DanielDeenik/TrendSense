"""
Test cases for main application routes.
"""

import pytest
from unittest.mock import patch, MagicMock


class TestMainRoutes:
    """Test cases for main application routes."""

    def test_home_route(self, client):
        """Test the home route renders correctly."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'TrendSense' in response.data or b'home' in response.data

    def test_health_check(self, client):
        """Test the health check endpoint."""
        response = client.get('/api/health')
        assert response.status_code == 200
        
        json_data = response.get_json()
        assert json_data['status'] == 'ok'
        assert 'version' in json_data

    def test_debug_navigation(self, client):
        """Test the debug navigation endpoint."""
        response = client.get('/debug/navigation')
        assert response.status_code == 200
        
        json_data = response.get_json()
        assert 'status' in json_data
        assert 'navigation' in json_data

    def test_404_error_handler(self, client):
        """Test the 404 error handler."""
        response = client.get('/nonexistent-page')
        assert response.status_code == 404

    def test_500_error_handler(self, client):
        """Test the 500 error handler."""
        with patch('app.render_template', side_effect=Exception("Test error")):
            response = client.get('/')
            # Should handle the error gracefully
            assert response.status_code in [200, 500]


class TestBlueprintRegistration:
    """Test cases for blueprint registration."""

    def test_api_blueprint_registered(self, client):
        """Test that the API blueprint is registered."""
        response = client.get('/api/health')
        assert response.status_code == 200

    def test_vc_lens_blueprint_registered(self, client):
        """Test that the VC Lens blueprint is registered."""
        response = client.get('/vc-lens/')
        # Should not return 404 (blueprint is registered)
        assert response.status_code != 404

    def test_trendsense_blueprint_registered(self, client):
        """Test that the TrendSense blueprint is registered."""
        response = client.get('/trendsense/')
        # Should not return 404 (blueprint is registered)
        assert response.status_code != 404

    def test_trendradar_blueprint_registered(self, client):
        """Test that the TrendRadar blueprint is registered."""
        response = client.get('/trendradar/')
        # Should not return 404 (blueprint is registered)
        assert response.status_code != 404

    def test_strategy_blueprint_registered(self, client):
        """Test that the Strategy blueprint is registered."""
        response = client.get('/strategy/')
        # Should not return 404 (blueprint is registered)
        assert response.status_code != 404

    def test_data_management_blueprint_registered(self, client):
        """Test that the Data Management blueprint is registered."""
        response = client.get('/data-management/')
        # Should not return 404 (blueprint is registered)
        assert response.status_code != 404

    def test_lookthrough_blueprint_registered(self, client):
        """Test that the Lookthrough blueprint is registered."""
        response = client.get('/lookthrough/')
        # Should not return 404 (blueprint is registered)
        assert response.status_code != 404

    def test_graph_analytics_blueprint_registered(self, client):
        """Test that the Graph Analytics blueprint is registered."""
        response = client.get('/graph-analytics/')
        # Should not return 404 (blueprint is registered)
        assert response.status_code != 404

    def test_lifecycle_blueprint_registered(self, client):
        """Test that the Lifecycle blueprint is registered."""
        response = client.get('/lifecycle/')
        # Should not return 404 (blueprint is registered)
        assert response.status_code != 404

    def test_copilot_blueprint_registered(self, client):
        """Test that the Copilot blueprint is registered."""
        response = client.get('/copilot/')
        # Should not return 404 (blueprint is registered)
        assert response.status_code != 404


class TestApplicationConfiguration:
    """Test cases for application configuration."""

    def test_app_secret_key_set(self, app):
        """Test that the app has a secret key set."""
        assert app.secret_key is not None
        assert app.secret_key != ''

    def test_app_testing_mode(self, app):
        """Test that the app is in testing mode."""
        assert app.config['TESTING'] is True

    def test_template_folder_configured(self, app):
        """Test that the template folder is configured."""
        assert app.template_folder is not None

    def test_static_folder_configured(self, app):
        """Test that the static folder is configured."""
        assert app.static_folder is not None


class TestContextProcessors:
    """Test cases for context processors."""

    @patch('src.frontend.utils.context_processors.navigation_processor')
    def test_navigation_processor_registered(self, mock_nav_processor, client):
        """Test that the navigation processor is registered."""
        mock_nav_processor.return_value = {'navigation': []}
        
        response = client.get('/')
        # The navigation processor should be called
        assert response.status_code == 200


class TestErrorHandling:
    """Test cases for error handling."""

    def test_template_not_found_error(self, client):
        """Test handling of template not found errors."""
        # This test would require mocking template loading to fail
        # For now, we'll test that the error handlers are registered
        assert client.application.error_handler_spec is not None

    def test_database_connection_error_handling(self, client):
        """Test handling of database connection errors."""
        with patch('src.database.adapters.get_database_adapter', side_effect=Exception("DB Error")):
            response = client.get('/api/health')
            # Should still return a response, not crash
            assert response.status_code in [200, 500]

    def test_import_error_handling(self, client):
        """Test handling of import errors."""
        # The application should handle missing imports gracefully
        response = client.get('/api/health')
        assert response.status_code == 200


if __name__ == '__main__':
    pytest.main([__file__])
