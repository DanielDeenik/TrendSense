"""
Database Command-Line Interface

This module provides a command-line interface for database operations.
"""

import os
import sys
import argparse
import logging
from typing import List

from .adapters import MongoDBAdapter, FirebaseAdapter
from .migration_utils import export_mongodb_to_json, import_json_to_firebase, migrate_mongodb_to_firebase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_firebase():
    """Set up Firebase project."""
    try:
        # Check if Firebase CLI is installed
        import subprocess
        result = subprocess.run(['firebase', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            logger.error("Firebase CLI not installed. Please install it first.")
            logger.info("Run: npm install -g firebase-tools")
            return False

        # Login to Firebase
        logger.info("Logging in to Firebase...")
        subprocess.run(['firebase', 'login'])

        # Initialize Firebase project
        logger.info("Initializing Firebase project...")
        subprocess.run(['firebase', 'init', 'firestore'])

        logger.info("Firebase setup complete.")
        return True
    except Exception as e:
        logger.error(f"Error setting up Firebase: {str(e)}")
        return False


def test_connection(adapter_type: str) -> bool:
    """
    Test connection to database.

    Args:
        adapter_type: Type of adapter to use ('mongodb' or 'firebase')

    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        if adapter_type == 'mongodb':
            adapter = MongoDBAdapter()
        else:
            adapter = FirebaseAdapter()

        if adapter.connect():
            logger.info(f"Successfully connected to {adapter_type}")
            adapter.disconnect()
            return True
        else:
            logger.error(f"Failed to connect to {adapter_type}")
            return False
    except Exception as e:
        logger.error(f"Error testing connection to {adapter_type}: {str(e)}")
        return False


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description='TrendSense Database CLI')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Set up database')
    setup_parser.add_argument('--adapter', choices=['mongodb', 'firebase'], default='firebase',
                             help='Database adapter to set up')

    # Test command
    test_parser = subparsers.add_parser('test', help='Test database connection')
    test_parser.add_argument('--adapter', choices=['mongodb', 'firebase'], default='firebase',
                            help='Database adapter to test')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export MongoDB to JSON')
    export_parser.add_argument('--collections', nargs='+', help='Collections to export (default: all)')
    export_parser.add_argument('--output-dir', default='data_export', help='Output directory')

    # Import command
    import_parser = subparsers.add_parser('import', help='Import JSON to Firebase')
    import_parser.add_argument('--input-dir', default='data_export', help='Input directory')

    # Migrate command
    migrate_parser = subparsers.add_parser('migrate', help='Migrate MongoDB to Firebase')
    migrate_parser.add_argument('--collections', nargs='+', help='Collections to migrate (default: all)')

    # Parse arguments
    args = parser.parse_args()

    # Execute command
    if args.command == 'setup':
        if args.adapter == 'firebase':
            setup_firebase()
        else:
            logger.info("MongoDB setup is manual. Please ensure MongoDB is installed and running.")
    elif args.command == 'test':
        test_connection(args.adapter)
    elif args.command == 'export':
        export_mongodb_to_json(args.collections, args.output_dir)
    elif args.command == 'import':
        import_json_to_firebase(args.input_dir)
    elif args.command == 'migrate':
        migrate_mongodb_to_firebase(args.collections)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
