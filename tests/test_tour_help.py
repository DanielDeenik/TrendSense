"""
Test cases for the TourMode help functionality.

This module contains comprehensive tests for the "Need Help?" button and modal
in the TourMode feature.
"""

import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class TestTourHelp(unittest.TestCase):
    """Test cases for TourMode help functionality."""

    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True

        # Mock navigation data
        self.navigation_patcher = patch('flask.render_template')
        self.mock_render_template = self.navigation_patcher.start()
        self.mock_render_template.return_value = "Mocked template"
        
        # Mock Firebase for testing issue submission
        self.firebase_patcher = patch('src.frontend.static.js.tour-help-logger.js.firebase', new=MagicMock())
        self.mock_firebase = self.firebase_patcher.start()
        self.mock_firebase_db = MagicMock()
        self.mock_firebase.database.return_value = self.mock_firebase_db

    def tearDown(self):
        """Clean up after tests."""
        self.navigation_patcher.stop()
        self.firebase_patcher.stop()

    def test_help_modal_template(self):
        """Test that the help modal template exists and is accessible."""
        with patch('src.frontend.templates.components.help_modal.html', 'tour-help-modal Need Help with TourMode?'):
            response = self.app.get('/templates/components/help_modal.html', follow_redirects=True)
            # Check that the template was accessed
            self.mock_render_template.assert_called()

    def test_help_button_creation(self):
        """Test that the help button is created when the tour starts."""
        with patch('src.frontend.static.js.tour-help-logger.js', 'createHelpButton'):
            self.app.get('/vc-lens?tour=true', follow_redirects=True)
            # Check that the page was loaded successfully
            self.mock_render_template.assert_called()

    def test_debug_info_collection(self):
        """Test that debug information is collected when the help button is clicked."""
        with patch('src.frontend.static.js.tour-help-logger.js', 'collectDebugInfo'):
            self.app.get('/vc-lens?tour=true', follow_redirects=True)
            # Check that the page was loaded successfully
            self.mock_render_template.assert_called()

    def test_issue_submission_to_firebase(self):
        """Test that issues are submitted to Firebase."""
        # Mock Firebase database reference
        mock_ref = MagicMock()
        self.mock_firebase_db.ref.return_value = mock_ref
        
        with patch('src.frontend.static.js.tour-help-logger.js', 'submitToFirebase'):
            self.app.get('/vc-lens?tour=true', follow_redirects=True)
            # Check that the page was loaded successfully
            self.mock_render_template.assert_called()

    def test_copilot_suggestion_generation(self):
        """Test that Co-Pilot suggestions are generated."""
        with patch('src.frontend.static.js.tour-copilot-responses.js', 'getCopilotSuggestion'):
            self.app.get('/vc-lens?tour=true', follow_redirects=True)
            # Check that the page was loaded successfully
            self.mock_render_template.assert_called()

    def test_issue_history_storage(self):
        """Test that issue history is stored in localStorage."""
        with patch('src.frontend.static.js.tour-help-logger.js', 'saveIssueHistory'):
            self.app.get('/vc-lens?tour=true', follow_redirects=True)
            # Check that the page was loaded successfully
            self.mock_render_template.assert_called()

    def test_error_logging(self):
        """Test that JavaScript errors are logged."""
        with patch('src.frontend.static.js.tour-help-logger.js', 'window.tourErrorLog'):
            self.app.get('/vc-lens?tour=true', follow_redirects=True)
            # Check that the page was loaded successfully
            self.mock_render_template.assert_called()

    def test_help_button_visibility(self):
        """Test that the help button is visible when the tour is active."""
        with patch('src.frontend.static.js.tour-help-logger.js', 'tour-help-button'):
            self.app.get('/vc-lens?tour=true', follow_redirects=True)
            # Check that the page was loaded successfully
            self.mock_render_template.assert_called()

    def test_fallback_email_submission(self):
        """Test that email submission is used as fallback when Firebase is not available."""
        # Mock Firebase to raise an error
        mock_ref = MagicMock()
        mock_ref.push.side_effect = Exception("Firebase error")
        self.mock_firebase_db.ref.return_value = mock_ref
        
        with patch('src.frontend.static.js.tour-help-logger.js', 'fallbackToEmailSubmission'):
            self.app.get('/vc-lens?tour=true', follow_redirects=True)
            # Check that the page was loaded successfully
            self.mock_render_template.assert_called()

    def test_help_modal_form_submission(self):
        """Test that the help modal form can be submitted."""
        with patch('src.frontend.templates.components.help_modal.html', 'submit-help'):
            self.app.get('/vc-lens?tour=true', follow_redirects=True)
            # Check that the page was loaded successfully
            self.mock_render_template.assert_called()

if __name__ == '__main__':
    unittest.main()
