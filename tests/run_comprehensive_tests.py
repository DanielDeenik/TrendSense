#!/usr/bin/env python3
"""
Comprehensive test runner for TrendSense application.

This script runs all tests and generates coverage reports.
"""

import os
import sys
import subprocess
import argparse
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_command(command, description):
    """Run a command and return the result."""
    logger.info(f"Running: {description}")
    logger.info(f"Command: {' '.join(command)}")
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=project_root
        )
        
        if result.returncode == 0:
            logger.info(f"✓ {description} completed successfully")
            if result.stdout:
                logger.info(f"Output: {result.stdout}")
        else:
            logger.error(f"✗ {description} failed")
            logger.error(f"Error: {result.stderr}")
            if result.stdout:
                logger.error(f"Output: {result.stdout}")
        
        return result.returncode == 0, result.stdout, result.stderr
    
    except Exception as e:
        logger.error(f"✗ Failed to run {description}: {str(e)}")
        return False, "", str(e)

def clean_cache():
    """Clean Python cache files."""
    logger.info("Cleaning Python cache files...")
    
    # Remove __pycache__ directories
    for root, dirs, files in os.walk(project_root):
        for dir_name in dirs[:]:  # Use slice to avoid modifying list while iterating
            if dir_name == '__pycache__':
                cache_path = os.path.join(root, dir_name)
                try:
                    import shutil
                    shutil.rmtree(cache_path)
                    logger.info(f"Removed: {cache_path}")
                except Exception as e:
                    logger.warning(f"Could not remove {cache_path}: {e}")
    
    # Remove .pyc files
    for root, dirs, files in os.walk(project_root):
        for file_name in files:
            if file_name.endswith('.pyc'):
                pyc_path = os.path.join(root, file_name)
                try:
                    os.remove(pyc_path)
                    logger.info(f"Removed: {pyc_path}")
                except Exception as e:
                    logger.warning(f"Could not remove {pyc_path}: {e}")

def install_dependencies():
    """Install test dependencies."""
    logger.info("Installing test dependencies...")
    
    dependencies = [
        'pytest>=7.0.0',
        'pytest-cov>=4.0.0',
        'pytest-asyncio>=0.21.0',
        'pytest-mock>=3.10.0',
        'coverage>=7.0.0'
    ]
    
    for dep in dependencies:
        success, stdout, stderr = run_command(
            [sys.executable, '-m', 'pip', 'install', dep],
            f"Installing {dep}"
        )
        if not success:
            logger.warning(f"Failed to install {dep}, continuing...")

def run_unit_tests():
    """Run unit tests."""
    test_files = [
        'test_app_routes.py',
        'test_database_adapters.py',
        'test_vc_lens_comprehensive.py'
    ]
    
    for test_file in test_files:
        test_path = project_root / 'tests' / test_file
        if test_path.exists():
            success, stdout, stderr = run_command(
                [sys.executable, '-m', 'pytest', str(test_path), '-v'],
                f"Running unit tests in {test_file}"
            )
            if not success:
                logger.error(f"Unit tests failed in {test_file}")
        else:
            logger.warning(f"Test file not found: {test_file}")

def run_integration_tests():
    """Run integration tests."""
    success, stdout, stderr = run_command(
        [sys.executable, '-m', 'pytest', 'tests/', '-m', 'integration', '-v'],
        "Running integration tests"
    )
    return success

def run_all_tests_with_coverage():
    """Run all tests with coverage."""
    success, stdout, stderr = run_command(
        [
            sys.executable, '-m', 'pytest',
            'tests/',
            '--cov=src',
            '--cov=app',
            '--cov-report=html',
            '--cov-report=term-missing',
            '--cov-report=xml',
            '-v'
        ],
        "Running all tests with coverage"
    )
    return success

def generate_test_report():
    """Generate a comprehensive test report."""
    logger.info("Generating test report...")
    
    # Run tests with JUnit XML output
    success, stdout, stderr = run_command(
        [
            sys.executable, '-m', 'pytest',
            'tests/',
            '--junitxml=test-results.xml',
            '--cov=src',
            '--cov=app',
            '--cov-report=xml',
            '-v'
        ],
        "Generating test report"
    )
    
    if success:
        logger.info("Test report generated successfully")
        logger.info("Coverage report: htmlcov/index.html")
        logger.info("JUnit XML: test-results.xml")
        logger.info("Coverage XML: coverage.xml")
    
    return success

def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description='Run TrendSense comprehensive tests')
    parser.add_argument('--clean', action='store_true', help='Clean cache before running tests')
    parser.add_argument('--install-deps', action='store_true', help='Install test dependencies')
    parser.add_argument('--unit-only', action='store_true', help='Run only unit tests')
    parser.add_argument('--integration-only', action='store_true', help='Run only integration tests')
    parser.add_argument('--coverage', action='store_true', help='Run tests with coverage')
    parser.add_argument('--report', action='store_true', help='Generate comprehensive test report')
    parser.add_argument('--all', action='store_true', help='Run all tests and generate reports')
    
    args = parser.parse_args()
    
    # Default to running all if no specific option is provided
    if not any([args.unit_only, args.integration_only, args.coverage, args.report]):
        args.all = True
    
    logger.info("Starting TrendSense comprehensive test suite")
    logger.info(f"Project root: {project_root}")
    
    # Clean cache if requested
    if args.clean or args.all:
        clean_cache()
    
    # Install dependencies if requested
    if args.install_deps or args.all:
        install_dependencies()
    
    # Set environment variables for testing
    os.environ.update({
        'FLASK_ENV': 'testing',
        'DATABASE_ADAPTER': 'mock_firebase',
        'TESTING': 'True'
    })
    
    success = True
    
    # Run tests based on arguments
    if args.unit_only:
        run_unit_tests()
    elif args.integration_only:
        success = run_integration_tests()
    elif args.coverage:
        success = run_all_tests_with_coverage()
    elif args.report or args.all:
        success = generate_test_report()
    
    if success:
        logger.info("✓ All tests completed successfully!")
        return 0
    else:
        logger.error("✗ Some tests failed!")
        return 1

if __name__ == '__main__':
    sys.exit(main())
