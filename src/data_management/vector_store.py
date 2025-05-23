"""
Vector store implementation for SustainaTrend.
"""

import os
import json
import numpy as np
from typing import Dict, List, Any, Optional, Union
import firebase_admin
from firebase_admin import credentials, firestore

class VectorStore:
    """
    Vector store implementation for SustainaTrend.
    Uses Firebase as the backend storage.
    """
    
    def __init__(self):
        """Initialize the vector store."""
        # Initialize Firebase if not already initialized
        try:
            self.app = firebase_admin.get_app()
        except ValueError:
            cred_path = os.path.join(os.path.dirname(__file__), '..', '..', 'firebase', 'service-account-key.json')
            cred = credentials.Certificate(cred_path)
            self.app = firebase_admin.initialize_app(cred)
        
        # Get Firestore client
        self.db = firestore.client()
        
        # Collection name for vector store
        self.collection_name = "vector_store"
    
    def add_item(self, item_id: str, embedding: List[float], metadata: Dict[str, Any], text: str) -> None:
        """
        Add an item to the vector store.
        
        Args:
            item_id: Unique identifier for the item
            embedding: Vector embedding for the item
            metadata: Additional metadata for the item
            text: Text content of the item
        """
        # Create document data
        doc_data = {
            "id": item_id,
            "embedding": embedding,
            "metadata": metadata,
            "text": text,
            "created_at": firestore.SERVER_TIMESTAMP,
            "updated_at": firestore.SERVER_TIMESTAMP
        }
        
        # Add to Firestore
        self.db.collection(self.collection_name).document(item_id).set(doc_data)
    
    def get_item(self, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Get an item from the vector store by ID.
        
        Args:
            item_id: Unique identifier for the item
            
        Returns:
            Item data or None if not found
        """
        doc_ref = self.db.collection(self.collection_name).document(item_id)
        doc = doc_ref.get()
        
        if doc.exists:
            return doc.to_dict()
        else:
            return None
    
    def delete_item(self, item_id: str) -> None:
        """
        Delete an item from the vector store.
        
        Args:
            item_id: Unique identifier for the item
        """
        self.db.collection(self.collection_name).document(item_id).delete()
    
    def search(self, query_embedding: List[float], top_k: int = 5, filter_criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Search for similar items in the vector store.
        
        Args:
            query_embedding: Vector embedding for the query
            top_k: Number of results to return
            filter_criteria: Optional filter criteria for the search
            
        Returns:
            List of similar items with similarity scores
        """
        # Get all items from the vector store
        items = list(self.db.collection(self.collection_name).get())
        
        # Convert to dictionaries
        items = [item.to_dict() for item in items]
        
        # Apply filter criteria if provided
        if filter_criteria:
            filtered_items = []
            for item in items:
                match = True
                for key, value in filter_criteria.items():
                    if key in item["metadata"]:
                        if isinstance(value, list):
                            # Check if any value in the list matches
                            if item["metadata"][key] not in value:
                                match = False
                                break
                        else:
                            # Direct comparison
                            if item["metadata"][key] != value:
                                match = False
                                break
                    else:
                        match = False
                        break
                
                if match:
                    filtered_items.append(item)
            
            items = filtered_items
        
        # Calculate similarity scores
        results = []
        for item in items:
            # Calculate cosine similarity
            item_embedding = item["embedding"]
            similarity = self._cosine_similarity(query_embedding, item_embedding)
            
            # Add to results
            results.append({
                "id": item["id"],
                "metadata": item["metadata"],
                "text": item["text"],
                "similarity": similarity
            })
        
        # Sort by similarity (descending)
        results.sort(key=lambda x: x["similarity"], reverse=True)
        
        # Return top-k results
        return results[:top_k]
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score
        """
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        
        if norm_vec1 == 0 or norm_vec2 == 0:
            return 0.0
        
        return dot_product / (norm_vec1 * norm_vec2)
    
    def get_all_items(self) -> List[Dict[str, Any]]:
        """
        Get all items from the vector store.
        
        Returns:
            List of all items
        """
        items = list(self.db.collection(self.collection_name).get())
        return [item.to_dict() for item in items]
    
    def count_items(self) -> int:
        """
        Count the number of items in the vector store.
        
        Returns:
            Number of items
        """
        return len(list(self.db.collection(self.collection_name).get()))
    
    def clear(self) -> None:
        """Clear all items from the vector store."""
        items = list(self.db.collection(self.collection_name).get())
        
        for item in items:
            item.reference.delete()
