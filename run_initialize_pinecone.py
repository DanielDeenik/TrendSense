"""
Run script to initialize Pinecone index for Sustainability Intelligence Platform

This script checks for the existence of the Pinecone API key and initializes
the required index for the storytelling feature if not already created.
"""
import os
import sys
import logging
from dotenv import load_dotenv
from frontend.initialize_pinecone import initialize_pinecone, test_pinecone_connection

# Configure logging
logging.basicConfig(level=logging.INFO,
                  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def check_api_key():
    """Check if Pinecone API key is set"""
    pinecone_api_key = os.getenv('PINECONE_API_KEY')
    if not pinecone_api_key:
        logger.error("PINECONE_API_KEY environment variable not set")
        print("❌ ERROR: PINECONE_API_KEY environment variable not set")
        print("Please set the PINECONE_API_KEY in your .env file or environment variables")
        print("You can get a free Pinecone API key at https://www.pinecone.io")
        return False
    return True

def main():
    """Main function to initialize Pinecone index"""
    print("\n" + "=" * 80)
    print("🌱 Initializing Pinecone for SustainaTrend™ Intelligence Platform")
    print("=" * 80)
    
    # Check if API key is set
    if not check_api_key():
        print("\nLATENT CONCEPT MODEL STATUS:")
        print("- Using fallback mode for Sustainability Storytelling")
        print("- Story generation will work but without vector-based semantic understanding")
        print("- To enable full LCM capabilities, please set up a Pinecone API key")
        print("=" * 80)
        return
    
    # Initialize Pinecone index
    print("\nInitializing Pinecone index for Latent Concept Models...")
    success = initialize_pinecone()
    
    if success:
        print("✅ Pinecone index initialized successfully")
        
        # Test connection
        print("\nTesting connection to Pinecone...")
        test_success = test_pinecone_connection()
        if test_success:
            print("✅ Pinecone connection test successful")
            print("\nLATENT CONCEPT MODEL STATUS:")
            print("- Full LCM capabilities are ENABLED")
            print("- Story generation will use vector-based semantic understanding")
            print("- Document-to-story generation with RAG capabilities is available")
        else:
            print("❌ Pinecone connection test failed")
            print("\nLATENT CONCEPT MODEL STATUS:")
            print("- Using fallback mode for Sustainability Storytelling")
            print("- Story generation will work but without vector-based semantic understanding")
    else:
        print("❌ Pinecone index initialization failed")
        print("\nLATENT CONCEPT MODEL STATUS:")
        print("- Using fallback mode for Sustainability Storytelling")
        print("- Story generation will work but without vector-based semantic understanding")
        print("- To enable full LCM capabilities, please check the logs for errors")
    
    print("=" * 80)

if __name__ == "__main__":
    main()