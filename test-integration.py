#!/usr/bin/env python3
"""
Test script to verify the PostgreSQL/FastAPI/Flask integration
"""
import sys
import os
import requests
import psycopg2
from datetime import datetime
import time

def test_database_connection():
    """Test direct connection to PostgreSQL database"""
    print("Testing database connection...")
    try:
        # Connect to database using environment variables
        if os.getenv('DATABASE_URL'):
            conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        else:
            conn = psycopg2.connect(
                dbname=os.getenv('PGDATABASE'),
                user=os.getenv('PGUSER'),
                password=os.getenv('PGPASSWORD'),
                host=os.getenv('PGHOST'),
                port=os.getenv('PGPORT', '5432')
            )
        
        # Execute a simple query to verify connection
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM metrics")
            result = cur.fetchone()
            metric_count = result[0]
            
        conn.close()
        print(f"✓ Database connection successful! Found {metric_count} metrics")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {str(e)}")
        return False

def test_fastapi_health():
    """Test FastAPI health endpoint"""
    print("Testing FastAPI health endpoint...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✓ FastAPI is healthy: {health_data}")
            return True
        else:
            print(f"✗ FastAPI health check failed with status code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ FastAPI health check failed: {str(e)}")
        return False

def test_fastapi_metrics():
    """Test FastAPI metrics endpoint"""
    print("Testing FastAPI metrics endpoint...")
    try:
        response = requests.get("http://localhost:8000/api/metrics", timeout=5)
        if response.status_code == 200:
            metrics = response.json()
            print(f"✓ FastAPI returned {len(metrics)} metrics")
            if metrics:
                print(f"  Sample metric: {metrics[0]}")
            return True
        else:
            print(f"✗ FastAPI metrics endpoint failed with status code {response.status_code}")
            try:
                error_details = response.json()
                print(f"  Error details: {error_details}")
            except:
                print(f"  Response body: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ FastAPI metrics request failed: {str(e)}")
        return False

def test_flask_frontend():
    """Test Flask frontend is accessible"""
    print("Testing Flask frontend...")
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        if response.status_code == 200:
            print(f"✓ Flask frontend is accessible")
            return True
        else:
            print(f"✗ Flask frontend check failed with status code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Flask frontend request failed: {str(e)}")
        return False

def test_flask_dashboard():
    """Test Flask dashboard is loading metrics data"""
    print("Testing Flask dashboard...")
    try:
        response = requests.get("http://localhost:5000/dashboard", timeout=5)
        if response.status_code == 200:
            # Check if the page contains key dashboard elements
            if "Sustainability Intelligence Dashboard" in response.text and \
               "Carbon Emissions" in response.text and \
               "metrics-time-series" in response.text:
                print(f"✓ Flask dashboard is rendering correctly with metrics data")
                return True
            else:
                print(f"✗ Flask dashboard is accessible but may not be properly rendering metrics data")
                return False
        else:
            print(f"✗ Flask dashboard check failed with status code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Flask dashboard request failed: {str(e)}")
        return False

def run_all_tests():
    """Run all integration tests"""
    print("\n=== PostgreSQL/FastAPI/Flask Integration Test ===")
    print(f"Time: {datetime.now().isoformat()}")
    print("================================================\n")
    
    # Run tests with proper spacing
    db_ok = test_database_connection()
    print("")
    
    fastapi_health_ok = test_fastapi_health()
    print("")
    
    fastapi_metrics_ok = test_fastapi_metrics()
    print("")
    
    flask_frontend_ok = test_flask_frontend()
    print("")
    
    flask_dashboard_ok = test_flask_dashboard()
    print("")
    
    # Print summary
    print("\n=== Test Summary ===")
    print(f"PostgreSQL Connection: {'✓' if db_ok else '✗'}")
    print(f"FastAPI Health Check: {'✓' if fastapi_health_ok else '✗'}")
    print(f"FastAPI Metrics Endpoint: {'✓' if fastapi_metrics_ok else '✗'}")
    print(f"Flask Frontend: {'✓' if flask_frontend_ok else '✗'}")
    print(f"Flask Dashboard: {'✓' if flask_dashboard_ok else '✗'}")
    
    all_tests_passed = db_ok and fastapi_health_ok and fastapi_metrics_ok and flask_frontend_ok and flask_dashboard_ok
    print(f"\nOverall Integration: {'✓ SUCCESS' if all_tests_passed else '✗ FAILED'}")
    
    return all_tests_passed

if __name__ == "__main__":
    # Wait a moment to ensure services have time to start
    if len(sys.argv) > 1 and sys.argv[1] == "--wait":
        print("Waiting 5 seconds for services to start...")
        time.sleep(5)
    
    success = run_all_tests()
    sys.exit(0 if success else 1)
