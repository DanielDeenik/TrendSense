"""
Database Adapters Package

This package provides database adapters for SustainaTrend.
"""

from .base_adapter import DatabaseAdapter
from .mongodb_adapter import MongoDBAdapter
from .firebase_adapter import FirebaseAdapter
from .mock_firebase_adapter import MockFirebaseAdapter
from .dual_adapter import DualDatabaseAdapter

__all__ = [
    'DatabaseAdapter',
    'MongoDBAdapter',
    'FirebaseAdapter',
    'MockFirebaseAdapter',
    'DualDatabaseAdapter',
    'get_database_adapter'
]


def get_database_adapter(adapter_type: str = None) -> DatabaseAdapter:
    """
    Get a database adapter based on configuration.

    Args:
        adapter_type: Type of adapter to use ('mongodb', 'firebase', 'mock_firebase', or 'dual')

    Returns:
        DatabaseAdapter instance
    """
    import os
    import logging

    logger = logging.getLogger(__name__)

    # Get adapter type from environment if not provided
    if adapter_type is None:
        adapter_type = os.getenv('DATABASE_ADAPTER', 'mock_firebase').lower()

    # Create and return the appropriate adapter
    if adapter_type == 'mongodb':
        logger.info("Using MongoDB adapter")
        return MongoDBAdapter()
    elif adapter_type == 'firebase':
        # Try to import firebase_admin to check if it's available
        try:
            import firebase_admin  # noqa: F401
            logger.info("Using Firebase adapter")
            return FirebaseAdapter()
        except ImportError:
            logger.warning("Firebase packages not installed, falling back to mock Firebase adapter")
            return MockFirebaseAdapter()
    elif adapter_type == 'mock_firebase':
        logger.info("Using mock Firebase adapter")
        return MockFirebaseAdapter()
    elif adapter_type == 'dual':
        # Get primary adapter type from environment
        primary_adapter_type = os.getenv('PRIMARY_DATABASE_ADAPTER', 'firebase').lower()
        secondary_adapter_type = os.getenv('SECONDARY_DATABASE_ADAPTER', 'mongodb').lower()
        logger.info(f"Using dual database adapter (primary: {primary_adapter_type}, secondary: {secondary_adapter_type})")
        return DualDatabaseAdapter(primary_adapter_type, secondary_adapter_type)
    else:
        logger.warning(f"Unknown adapter type: {adapter_type}, falling back to mock Firebase")
        return MockFirebaseAdapter()
