#!/usr/bin/env python3
"""
Script to set up and verify Pinecone vector database for LensIQ.
"""

import os
import sys
import logging
from typing import Optional

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_management.vector_store import VectorStore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_environment() -> bool:
    """
    Check if required environment variables are set.
    
    Returns:
        True if environment is properly configured, False otherwise
    """
    required_vars = [
        'PINECONE_API_KEY',
        'PINECONE_ENVIRONMENT',
        'PINECONE_INDEX_NAME'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        logger.info("Please set the following in your .env file:")
        logger.info("PINECONE_API_KEY=your-pinecone-api-key")
        logger.info("PINECONE_ENVIRONMENT=us-west1-gcp")
        logger.info("PINECONE_INDEX_NAME=lensiq-vectors")
        return False
    
    return True


def setup_pinecone() -> Optional[VectorStore]:
    """
    Set up Pinecone vector store.
    
    Returns:
        VectorStore instance if successful, None otherwise
    """
    try:
        logger.info("Initializing Pinecone vector store...")
        vector_store = VectorStore()
        logger.info("✅ Pinecone vector store initialized successfully")
        return vector_store
    except Exception as e:
        logger.error(f"❌ Failed to initialize Pinecone vector store: {str(e)}")
        return None


def test_vector_store(vector_store: VectorStore) -> bool:
    """
    Test basic vector store operations.
    
    Args:
        vector_store: VectorStore instance to test
        
    Returns:
        True if all tests pass, False otherwise
    """
    try:
        logger.info("Testing vector store operations...")
        
        # Test data
        test_id = "test-vector-001"
        test_embedding = [0.1] * 1536  # Simple test embedding
        test_metadata = {
            "type": "test",
            "category": "setup_verification",
            "name": "Test Vector"
        }
        test_text = "This is a test vector for setup verification."
        
        # Test 1: Add item
        logger.info("Testing add_item...")
        vector_store.add_item(test_id, test_embedding, test_metadata, test_text)
        logger.info("✅ add_item test passed")
        
        # Test 2: Get item
        logger.info("Testing get_item...")
        retrieved_item = vector_store.get_item(test_id)
        if retrieved_item is None:
            logger.error("❌ get_item test failed: item not found")
            return False
        logger.info("✅ get_item test passed")
        
        # Test 3: Search
        logger.info("Testing search...")
        search_results = vector_store.search(test_embedding, top_k=1)
        if not search_results or search_results[0]["id"] != test_id:
            logger.error("❌ search test failed: item not found in search results")
            return False
        logger.info("✅ search test passed")
        
        # Test 4: Count items
        logger.info("Testing count_items...")
        count = vector_store.count_items()
        if count < 1:
            logger.error("❌ count_items test failed: count is less than 1")
            return False
        logger.info(f"✅ count_items test passed (count: {count})")
        
        # Test 5: Delete item
        logger.info("Testing delete_item...")
        vector_store.delete_item(test_id)
        deleted_item = vector_store.get_item(test_id)
        if deleted_item is not None:
            logger.error("❌ delete_item test failed: item still exists")
            return False
        logger.info("✅ delete_item test passed")
        
        logger.info("🎉 All vector store tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Vector store test failed: {str(e)}")
        return False


def main():
    """Main setup function."""
    logger.info("🚀 Starting Pinecone setup for LensIQ...")
    
    # Check environment
    if not check_environment():
        logger.error("❌ Environment check failed")
        sys.exit(1)
    
    # Setup Pinecone
    vector_store = setup_pinecone()
    if not vector_store:
        logger.error("❌ Pinecone setup failed")
        sys.exit(1)
    
    # Test vector store
    if not test_vector_store(vector_store):
        logger.error("❌ Vector store tests failed")
        sys.exit(1)
    
    logger.info("🎉 Pinecone setup completed successfully!")
    logger.info("Your Pinecone vector database is ready for use.")


if __name__ == "__main__":
    main()
