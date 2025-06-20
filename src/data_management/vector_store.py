"""
Vector store implementation for LensIQ.
"""

import os
import logging
from typing import Dict, List, Any, Optional
from pinecone import Pinecone, ServerlessSpec

# Logging setup
logger = logging.getLogger("VectorStore")
logging.basicConfig(level=logging.INFO)

# Configuration from environment
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENV = os.environ.get("PINECONE_ENVIRONMENT", "us-west1-gcp")
PINECONE_INDEX = os.environ.get("PINECONE_INDEX_NAME", "lensiq-vectors")

# Initialize Pinecone client
_pinecone_client = None
if PINECONE_API_KEY:
    try:
        _pinecone_client = Pinecone(api_key=PINECONE_API_KEY)
        logger.info("Pinecone client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Pinecone client: {str(e)}")
        _pinecone_client = None
else:
    logger.warning("Pinecone API key not found in environment variables")


class VectorStore:
    """
    Vector store implementation for LensIQ using Pinecone.
    """
    def __init__(self, index_name: Optional[str] = None):
        self.index_name = index_name or PINECONE_INDEX
        self.client = _pinecone_client

        if not self.client:
            raise RuntimeError(
                "Pinecone client not initialized. "
                "Please set PINECONE_API_KEY environment variable."
            )

        # Check if index exists, create if it doesn't
        existing_indexes = [idx.name for idx in self.client.list_indexes()]
        if self.index_name not in existing_indexes:
            # Create index with serverless spec
            self.client.create_index(
                name=self.index_name,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region=PINECONE_ENV
                )
            )
            logger.info(f"Created new Pinecone index '{self.index_name}'")

        self.index = self.client.Index(self.index_name)
        logger.info(f"Pinecone index '{self.index_name}' initialized.")

    def add_item(
        self,
        item_id: str,
        embedding: List[float],
        metadata: Dict[str, Any],
        text: str
    ) -> None:
        """
        Upsert a vector and its metadata into Pinecone.
        """
        vector = {
            "id": item_id,
            "values": embedding,
            "metadata": {**metadata, "text": text}
        }
        self.index.upsert(vectors=[vector])
        logger.info(f"Upserted item {item_id} into Pinecone.")

    def get_item(self, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch a vector and its metadata by ID.
        """
        response = self.index.fetch(ids=[item_id])
        vectors = response.get("vectors", {})
        if item_id in vectors:
            return vectors[item_id]
        return None

    def delete_item(self, item_id: str) -> None:
        """
        Delete a vector by ID.
        """
        self.index.delete(ids=[item_id])
        logger.info(f"Deleted item {item_id} from Pinecone.")

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter_criteria: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Query Pinecone for similar vectors.
        """
        query_args = {
            "vector": query_embedding,
            "top_k": top_k,
            "include_metadata": True
        }
        if filter_criteria:
            query_args["filter"] = filter_criteria
        response = self.index.query(**query_args)
        results = []
        for match in response.get("matches", []):
            results.append({
                "id": match["id"],
                "score": match["score"],
                "metadata": match.get("metadata", {})
            })
        return results

    def count_items(self) -> int:
        """
        Return the number of vectors in the index.
        """
        stats = self.index.describe_index_stats()
        return stats.get("total_vector_count", 0)

    def clear(self) -> None:
        """
        Delete all vectors in the index (dangerous!).
        """
        self.index.delete(delete_all=True)
        logger.warning(
            f"Cleared all items from Pinecone index '{self.index_name}'."
        )


# --- TESTS ---
if __name__ == "__main__":
    import random
    import string

    def random_id():
        return ''.join(
            random.choices(string.ascii_lowercase + string.digits, k=8)
        )

    store = VectorStore()
    test_id = random_id()
    embedding = [random.random() for _ in range(1536)]
    metadata = {"type": "test", "owner": "unittest"}
    text = "This is a test vector."

    # Add
    store.add_item(test_id, embedding, metadata, text)

    # Get
    item = store.get_item(test_id)
    assert item is not None, "Failed to fetch inserted item."

    # Search
    results = store.search(embedding, top_k=1)
    assert (
        results and results[0]["id"] == test_id
    ), "Search did not return the inserted item."

    # Count
    assert store.count_items() > 0, "Count should be > 0 after insert."

    # Delete
    store.delete_item(test_id)
    assert store.get_item(test_id) is None, "Item should be deleted."
    print("All VectorStore tests passed.")
