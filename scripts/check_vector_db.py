"""
Script to check the vector database.
"""

import os
import sys
import json
import random
from tqdm import tqdm

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import project modules
from src.data_management.vector_store import VectorStore

def check_vector_db():
    """Check the vector database."""
    print("Checking vector database...")
    
    # Initialize Vector Store
    vector_store = VectorStore()
    
    # Count items
    count = vector_store.count_items()
    print(f"Vector store contains {count} items")
    
    # Get all items
    items = vector_store.get_all_items()
    
    # Count by type
    company_count = sum(1 for item in items if item["metadata"]["type"] == "company")
    trend_count = sum(1 for item in items if item["metadata"]["type"] == "trend")
    project_count = sum(1 for item in items if item["metadata"]["type"] == "project")
    fund_count = sum(1 for item in items if item["metadata"]["type"] == "fund")
    
    print(f"Companies: {company_count}")
    print(f"Trends: {trend_count}")
    print(f"Projects: {project_count}")
    print(f"Funds: {fund_count}")
    
    # Check if items have embeddings
    embedding_count = sum(1 for item in items if "embedding" in item and item["embedding"])
    print(f"Items with embeddings: {embedding_count}")
    
    # Perform a sample search
    if items:
        # Get a random item
        random_item = random.choice(items)
        
        # Get the embedding
        embedding = random_item["embedding"]
        
        # Perform a search
        print("\nPerforming a sample search...")
        results = vector_store.search(embedding, top_k=5)
        
        # Print results
        print(f"Search results for {random_item['metadata']['name']} ({random_item['metadata']['type']}):")
        for i, result in enumerate(results):
            print(f"{i+1}. {result['metadata']['name']} ({result['metadata']['type']}) - Similarity: {result['similarity']:.4f}")
        
        # Perform a filtered search
        print("\nPerforming a filtered search...")
        filter_criteria = {"type": random_item["metadata"]["type"]}
        filtered_results = vector_store.search(embedding, top_k=5, filter_criteria=filter_criteria)
        
        # Print results
        print(f"Filtered search results for {random_item['metadata']['name']} (type={random_item['metadata']['type']}):")
        for i, result in enumerate(filtered_results):
            print(f"{i+1}. {result['metadata']['name']} ({result['metadata']['type']}) - Similarity: {result['similarity']:.4f}")

if __name__ == "__main__":
    check_vector_db()
