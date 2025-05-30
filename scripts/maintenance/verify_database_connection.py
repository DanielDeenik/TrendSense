"""
Script to verify that the TrendSense database is connected.
Supports all configured adapters (MongoDB, Firebase, etc).
"""
import os
import sys

# Set up Django-like project root import if needed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.database.db_manager import get_database

def main():
    db = get_database()
    if hasattr(db, 'is_connected'):
        connected = db.is_connected()
    elif hasattr(db, 'connect'):
        connected = db.connect()
    else:
        print("[ERROR] Database manager does not have a connect or is_connected method.")
        sys.exit(1)

    if connected:
        print("[SUCCESS] Database connection verified!")
        sys.exit(0)
    else:
        print("[FAIL] Database connection failed.")
        sys.exit(2)

if __name__ == '__main__':
    main()
