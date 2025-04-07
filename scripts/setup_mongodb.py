#!/usr/bin/env python3
"""
MongoDB Setup Script for SustainaTrend
This script sets up MongoDB for the SustainaTrend platform by:
1. Testing the connection
2. Seeding the database with sample data
3. Verifying the data was seeded correctly
"""

import os
import sys
import time
from dotenv import load_dotenv

# Add parent directory to path to import scripts
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import scripts
from scripts.seed_mongo_vc_data import seed_database
from scripts.test_mongo_connection import test_mongodb_connection

def setup_mongodb():
    """Set up MongoDB for SustainaTrend."""
    print("🔧 Setting up MongoDB for SustainaTrend...")
    
    # Load environment variables
    load_dotenv()
    
    # Check if MongoDB URI is set
    if not os.getenv('MONGODB_URI'):
        print("❌ Error: MONGODB_URI environment variable is not set.")
        print("Please set it in your .env file or environment.")
        return False
    
    # Test connection
    print("\n🔍 Testing MongoDB connection...")
    if not test_mongodb_connection():
        print("❌ Failed to connect to MongoDB. Please check your connection settings.")
        return False
    
    # Seed database
    print("\n🌱 Seeding database with sample data...")
    if not seed_database():
        print("❌ Failed to seed database. Please check the logs for errors.")
        return False
    
    # Wait a moment for the database to update
    time.sleep(1)
    
    # Verify data was seeded
    print("\n✅ Database setup completed successfully!")
    print("\n📊 Verifying seeded data...")
    test_mongodb_connection()
    
    return True

if __name__ == "__main__":
    setup_mongodb() 