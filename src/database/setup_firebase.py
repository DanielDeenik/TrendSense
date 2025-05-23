"""
Firebase Setup Script

This script helps set up Firebase for TrendSense.
"""

import os
import sys
import json
import logging
import subprocess
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_firebase_cli():
    """Check if Firebase CLI is installed."""
    try:
        result = subprocess.run(['firebase', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"Firebase CLI is installed: {result.stdout.strip()}")
            return True
        else:
            logger.error("Firebase CLI is not installed or not in PATH")
            return False
    except Exception as e:
        logger.error(f"Error checking Firebase CLI: {str(e)}")
        return False


def install_firebase_cli():
    """Install Firebase CLI."""
    logger.info("Installing Firebase CLI...")
    try:
        # Check if npm is installed
        npm_result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if npm_result.returncode != 0:
            logger.error("npm is not installed. Please install Node.js and npm first.")
            logger.info("Download Node.js from: https://nodejs.org/")
            return False

        # Install Firebase CLI
        result = subprocess.run(['npm', 'install', '-g', 'firebase-tools'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("Firebase CLI installed successfully")
            return True
        else:
            logger.error(f"Error installing Firebase CLI: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error installing Firebase CLI: {str(e)}")
        return False


def login_to_firebase():
    """Login to Firebase."""
    logger.info("Logging in to Firebase...")
    try:
        result = subprocess.run(['firebase', 'login'], capture_output=False)
        if result.returncode == 0:
            logger.info("Logged in to Firebase successfully")
            return True
        else:
            logger.error("Error logging in to Firebase")
            return False
    except Exception as e:
        logger.error(f"Error logging in to Firebase: {str(e)}")
        return False


def initialize_firebase_project():
    """Initialize Firebase project."""
    logger.info("Initializing Firebase project...")
    try:
        # Run Firebase init
        result = subprocess.run(['firebase', 'init', 'firestore'], capture_output=False)
        if result.returncode == 0:
            logger.info("Firebase project initialized successfully")
            return True
        else:
            logger.error("Error initializing Firebase project")
            return False
    except Exception as e:
        logger.error(f"Error initializing Firebase project: {str(e)}")
        return False


def create_service_account():
    """Create Firebase service account."""
    logger.info("Creating Firebase service account...")
    logger.info("Please follow these steps:")
    logger.info("1. Go to Firebase Console: https://console.firebase.google.com/")
    logger.info("2. Select your project")
    logger.info("3. Go to Project Settings > Service Accounts")
    logger.info("4. Click 'Generate new private key'")
    logger.info("5. Save the JSON file")

    # Ask for the path to the service account key
    key_path = input("Enter the path to the service account key JSON file: ")

    if not os.path.exists(key_path):
        logger.error(f"File not found: {key_path}")
        return False

    try:
        # Read the service account key
        with open(key_path, 'r') as f:
            key_data = json.load(f)

        # Create firebase directory if it doesn't exist
        firebase_dir = Path('firebase')
        firebase_dir.mkdir(exist_ok=True)

        # Save the service account key to firebase directory
        key_file = firebase_dir / 'service-account-key.json'
        with open(key_file, 'w') as f:
            json.dump(key_data, f, indent=2)

        logger.info(f"Service account key saved to {key_file}")

        # Update .env file
        env_file = Path('.env')
        if env_file.exists():
            with open(env_file, 'r') as f:
                env_content = f.read()

            # Update or add Firebase configuration
            if 'FIREBASE_CREDENTIALS_PATH' in env_content:
                env_content = env_content.replace(
                    'FIREBASE_CREDENTIALS_PATH=',
                    f'FIREBASE_CREDENTIALS_PATH={key_file}'
                )
            else:
                env_content += f'\nFIREBASE_CREDENTIALS_PATH={key_file}'

            if 'FIREBASE_PROJECT_ID' in env_content:
                env_content = env_content.replace(
                    'FIREBASE_PROJECT_ID=',
                    f'FIREBASE_PROJECT_ID={key_data["project_id"]}'
                )
            else:
                env_content += f'\nFIREBASE_PROJECT_ID={key_data["project_id"]}'

            # Update DATABASE_ADAPTER
            if 'DATABASE_ADAPTER' in env_content:
                env_content = env_content.replace(
                    'DATABASE_ADAPTER=mongodb',
                    'DATABASE_ADAPTER=firebase'
                )
            else:
                env_content += '\nDATABASE_ADAPTER=firebase'

            # Write updated .env file
            with open(env_file, 'w') as f:
                f.write(env_content)

            logger.info(".env file updated with Firebase configuration")
        else:
            logger.warning(".env file not found. Please create it and add Firebase configuration.")

        return True
    except Exception as e:
        logger.error(f"Error creating service account: {str(e)}")
        return False


def install_firebase_dependencies():
    """Install Firebase dependencies."""
    logger.info("Installing Firebase dependencies...")
    try:
        # Check if requirements file exists
        if not os.path.exists('firebase_requirements.txt'):
            logger.error("firebase_requirements.txt not found")
            return False

        # Install dependencies
        result = subprocess.run(['pip', 'install', '-r', 'firebase_requirements.txt'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("Firebase dependencies installed successfully")
            return True
        else:
            logger.error(f"Error installing Firebase dependencies: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error installing Firebase dependencies: {str(e)}")
        return False


def main():
    """Main entry point."""
    logger.info("Starting Firebase setup...")

    # Check if Firebase CLI is installed
    if not check_firebase_cli():
        # Install Firebase CLI
        if not install_firebase_cli():
            logger.error("Failed to install Firebase CLI. Please install it manually.")
            return

    # Login to Firebase
    if not login_to_firebase():
        logger.error("Failed to login to Firebase. Please try again.")
        return

    # Initialize Firebase project
    if not initialize_firebase_project():
        logger.error("Failed to initialize Firebase project. Please try again.")
        return

    # Create service account
    if not create_service_account():
        logger.error("Failed to create service account. Please try again.")
        return

    # Install Firebase dependencies
    if not install_firebase_dependencies():
        logger.error("Failed to install Firebase dependencies. Please install them manually.")
        return

    logger.info("Firebase setup completed successfully!")
    logger.info("You can now use Firebase as a database backend for TrendSense.")


if __name__ == '__main__':
    main()
