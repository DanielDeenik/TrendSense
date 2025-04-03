#!/usr/bin/env python3
import os
import sys
import time
import psycopg2
from urllib.parse import urlparse

def get_db_config():
    """Get database configuration from environment variables"""
    # Get connection string from environment variable
    db_url = os.environ.get('DATABASE_URL')
    
    if not db_url:
        print("ERROR: DATABASE_URL environment variable not set")
        sys.exit(1)
    
    # Parse connection string
    parsed = urlparse(db_url)
    return {
        'dbname': parsed.path[1:],
        'user': parsed.username,
        'password': parsed.password,
        'host': parsed.hostname,
        'port': parsed.port or 5432
    }

def check_db_connection(max_retries=5, retry_delay=2):
    """Check database connection with retries"""
    config = get_db_config()
    retries = 0
    
    while retries < max_retries:
        try:
            print(f"Connecting to PostgreSQL... (Attempt {retries + 1}/{max_retries})")
            conn = psycopg2.connect(**config)
            conn.close()
            print("Database connection successful!")
            return True
        except Exception as e:
            print(f"Connection failed: {str(e)}")
            retries += 1
            if retries < max_retries:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
    
    print("ERROR: Failed to connect to the database after multiple attempts")
    return False

if __name__ == "__main__":
    if check_db_connection():
        sys.exit(0)
    else:
        sys.exit(1)