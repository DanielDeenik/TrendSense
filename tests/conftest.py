"""
Pytest configuration and fixtures for TrendSense tests.
"""

import os
import sys
import pytest
import tempfile
import shutil
from unittest.mock import MagicMock, patch

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Also add the SustainaTrendTm directory to the path
sustainatrend_path = os.path.join(project_root, 'SustainaTrendTm')
if os.path.exists(sustainatrend_path):
    sys.path.insert(0, sustainatrend_path)

# Configure asyncio for pytest-asyncio
pytest_plugins = ('pytest_asyncio',)

@pytest.fixture(scope="session")
def app():
    """Create and configure a test Flask application."""
    from app import create_app

    # Create a temporary directory for test data
    test_dir = tempfile.mkdtemp()

    app = create_app()
    app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'test-secret-key',
        'DATABASE_ADAPTER': 'mock_firebase',
        'MONGODB_URI': 'mongodb://localhost:27017/test_trendsense',
        'FIREBASE_PROJECT_ID': 'test-project',
        'TEST_DATA_DIR': test_dir
    })

    yield app

    # Cleanup
    shutil.rmtree(test_dir, ignore_errors=True)

@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test runner for the Flask application."""
    return app.test_cli_runner()

@pytest.fixture
def mock_database():
    """Mock database adapter for testing."""
    mock_db = MagicMock()
    mock_db.connect.return_value = True
    mock_db.is_connected.return_value = True
    mock_db.get_collection.return_value = MagicMock()
    return mock_db

@pytest.fixture
def mock_mongodb_service():
    """Mock MongoDB service for testing."""
    with patch('src.database.adapters.mongodb_adapter.MongoDBAdapter') as mock:
        mock_instance = MagicMock()
        mock_instance.connect.return_value = True
        mock_instance.is_connected.return_value = True
        mock_instance.get_database.return_value = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_firebase_service():
    """Mock Firebase service for testing."""
    with patch('src.database.adapters.firebase_adapter.FirebaseAdapter') as mock:
        mock_instance = MagicMock()
        mock_instance.connect.return_value = True
        mock_instance.is_connected.return_value = True
        mock_instance.get_collection.return_value = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def sample_trends_data():
    """Sample trends data for testing."""
    return [
        {
            "category": "Renewable Energy",
            "growth": 24,
            "score": 85,
            "trend_values": [65, 68, 70, 72, 75, 78, 80, 82, 85, 87, 90, 92]
        },
        {
            "category": "Circular Economy",
            "growth": 32,
            "score": 78,
            "trend_values": [55, 58, 62, 65, 68, 70, 72, 74, 75, 76, 78, 80]
        },
        {
            "category": "Carbon Tech",
            "growth": 45,
            "score": 92,
            "trend_values": [40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 88, 92]
        }
    ]

@pytest.fixture
def sample_companies_data():
    """Sample companies data for testing."""
    return [
        {
            "_id": "company1",
            "name": "GreenTech Solutions",
            "sector": "Renewable Energy",
            "stage": "Series A",
            "sustainability_score": 85,
            "growth_score": 78
        },
        {
            "_id": "company2",
            "name": "CircularCorp",
            "sector": "Circular Economy",
            "stage": "Seed",
            "sustainability_score": 72,
            "growth_score": 65
        }
    ]

@pytest.fixture
def sample_funds_data():
    """Sample funds data for testing."""
    return [
        {
            "_id": "fund1",
            "name": "Green Ventures Fund",
            "type": "VC",
            "focus": "Sustainability",
            "aum": 500000000,
            "companies": ["company1", "company2"]
        }
    ]

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment variables."""
    os.environ.update({
        'FLASK_ENV': 'testing',
        'DATABASE_ADAPTER': 'mock_firebase',
        'TESTING': 'True'
    })
    yield
    # Cleanup is automatic

# Configure pytest-asyncio
def pytest_configure(config):
    """Configure pytest with custom settings."""
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )

# Set asyncio event loop scope
@pytest.fixture(scope="session")
def event_loop_policy():
    """Set the event loop policy for async tests."""
    import asyncio
    return asyncio.DefaultEventLoopPolicy()

# Configure asyncio mode
pytest_asyncio_mode = "auto"
