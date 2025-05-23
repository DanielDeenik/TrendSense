#!/usr/bin/env python
"""
Test runner for TrendSense.

This script runs all the tests for TrendSense, including Python and JavaScript tests.
"""

import os
import sys
import unittest
import subprocess

def run_python_tests(comprehensive=False):
    """Run Python tests."""
    print("Running Python tests...")

    # Discover and run tests
    test_loader = unittest.TestLoader()

    if comprehensive:
        print("Running comprehensive test suite...")
        # Run only the comprehensive test suite
        test_suite = test_loader.discover('tests', pattern='test_comprehensive.py')
    else:
        # Run all tests
        test_suite = test_loader.discover('tests', pattern='test_*.py')

    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)

    return result.wasSuccessful()

def run_js_tests():
    """Run JavaScript tests."""
    print("Running JavaScript tests...")

    # Check if npm is installed
    try:
        subprocess.run(['npm', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: npm is not installed. Please install Node.js and npm to run JavaScript tests.")
        return False

    # Install dependencies if needed
    if not os.path.exists('node_modules'):
        print("Installing dependencies...")
        subprocess.run(['npm', 'install'], check=True)

    # Run tests
    result = subprocess.run(['npm', 'test'], check=False)

    return result.returncode == 0

def main():
    """Run all tests."""
    # Check if comprehensive flag is set
    comprehensive = '--comprehensive' in sys.argv or '-c' in sys.argv

    # Run tests
    python_success = run_python_tests(comprehensive)
    js_success = run_js_tests()

    if python_success and js_success:
        print("All tests passed!")
        return 0
    else:
        print("Some tests failed.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
