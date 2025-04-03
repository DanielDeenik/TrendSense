#!/usr/bin/env python3
"""
Test runner for the Sustainability Intelligence Platform.
Runs database, FastAPI, Flask, and integration tests.
"""
import os
import sys
import subprocess
import time
import pytest
import argparse
from datetime import datetime

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f" {text} ".center(80, "="))
    print("=" * 80 + "\n")

def check_services_running():
    """Check if services are already running"""
    try:
        # Check if FastAPI is running
        fastapi_running = subprocess.run(
            "curl -s http://localhost:8000/health > /dev/null", 
            shell=True, 
            check=False
        ).returncode == 0

        # Check if Flask is running
        flask_running = subprocess.run(
            "curl -s http://localhost:5001 > /dev/null", 
            shell=True, 
            check=False
        ).returncode == 0

        return fastapi_running, flask_running
    except Exception as e:
        print(f"Error checking services: {e}")
        return False, False

def run_services():
    """Start the required services for testing"""
    print_header("Starting Services")

    # Check if services are already running
    fastapi_running, flask_running = check_services_running()
    if fastapi_running and flask_running:
        print("Services are already running. Reusing existing services.")
        return None  # No process to track since we're reusing

    # Start the simple services using the script we've already created
    print("Starting PostgreSQL, FastAPI, and Flask...")

    # Use subprocess to run the script but don't wait for it to complete
    start_script = os.path.join(os.path.dirname(__file__), "simple-start.sh")

    # Make sure the script is executable
    os.chmod(start_script, 0o755)

    # First stop any existing services to avoid conflicts
    print("Stopping any existing services...")
    try:
        subprocess.run("pkill -f 'python simple_api.py' || true", shell=True, check=False)
        subprocess.run("pkill -f 'python simple_app.py' || true", shell=True, check=False)
        # Give time for services to stop
        time.sleep(2)
    except Exception as e:
        print(f"Error stopping services: {e}")

    # Start services in the background with a timeout
    try:
        process = subprocess.Popen(
            [start_script], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            text=True
        )

        # Give services time to start
        print("Waiting for services to start...")

        # Wait for some initial output before waiting for services
        start_time = time.time()
        service_timeout = 30  # 30 seconds timeout

        while time.time() - start_time < service_timeout:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                print(line.strip())

            # Check if services are ready
            fastapi_running, flask_running = check_services_running()
            if fastapi_running and flask_running:
                print("All services are running!")
                break

            time.sleep(1)

        if not (fastapi_running and flask_running):
            print("Warning: Not all services started successfully within the timeout period.")
            if process.poll() is not None:
                print(f"Process exited with code {process.returncode}")

        return process

    except Exception as e:
        print(f"Error starting services: {e}")
        return None

def stop_services(process):
    """Stop the services that were started for testing"""
    if process is None:
        print("No process to stop (services may have been already running)")
        return

    print_header("Stopping Services")

    # Kill the process if it's still running
    if process.poll() is None:
        print("Terminating service processes...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("Process did not terminate gracefully, forcing termination...")
            process.kill()

    # Make sure all services are stopped
    try:
        subprocess.run(
            "pkill -f 'python simple_api.py' || true", 
            shell=True, 
            check=False
        )
        subprocess.run(
            "pkill -f 'python simple_app.py' || true", 
            shell=True, 
            check=False
        )
    except Exception as e:
        print(f"Error stopping services: {e}")

    print("All services stopped.")

def run_tests(args):
    """Run the tests"""
    print_header("Running Tests")

    # Set pytest arguments
    pytest_args = ["-v"]

    # Add specific test files if provided
    if args.unit_only:
        pytest_args.extend(["tests/test_database.py", "tests/test_fastapi.py", "tests/test_flask.py"])
    elif args.integration_only:
        pytest_args.append("tests/test_integration_pytest.py")
    elif args.database_only:
        pytest_args.append("tests/test_database.py")
    elif args.fastapi_only:
        pytest_args.append("tests/test_fastapi.py")
    elif args.flask_only:
        pytest_args.append("tests/test_flask.py")
    elif args.trend_only:
        pytest_args.append("tests/test_sustainability_trend.py")
    else:
        pytest_args.append("tests")

    # Run pytest with the arguments and a timeout
    try:
        return_code = pytest.main(pytest_args)
        return return_code
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1

def main():
    """Main function to run tests"""
    parser = argparse.ArgumentParser(description="Run tests for the Sustainability Intelligence Platform")
    parser.add_argument("--no-services", action="store_true", help="Don't start/stop services")
    parser.add_argument("--unit-only", action="store_true", help="Run only unit tests")
    parser.add_argument("--integration-only", action="store_true", help="Run only integration tests")
    parser.add_argument("--database-only", action="store_true", help="Run only database tests")
    parser.add_argument("--fastapi-only", action="store_true", help="Run only FastAPI tests")
    parser.add_argument("--flask-only", action="store_true", help="Run only Flask tests")
    parser.add_argument("--trend-only", action="store_true", help="Run only sustainability trend tests")

    args = parser.parse_args()

    print_header("Sustainability Intelligence Platform Test Runner")
    print(f"Time: {datetime.now().isoformat()}")

    service_process = None

    try:
        # Start services if needed
        if not args.no_services:
            service_process = run_services()

        # Run tests
        return_code = run_tests(args)

        # Return the test result code
        return return_code

    except KeyboardInterrupt:
        print("\nTest run interrupted by user.")
        return 1
    finally:
        # Stop services if we started them
        if service_process is not None and not args.no_services:
            stop_services(service_process)

if __name__ == "__main__":
    sys.exit(main())