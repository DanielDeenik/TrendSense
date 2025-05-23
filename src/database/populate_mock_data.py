"""
Populate Mock Data Script for TrendSense

This script populates MongoDB and Pinecone with mock data for the graph analytics feature.
"""

import os
import sys
import logging
import time
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import necessary modules
from src.database.mock_graph_data import generate_all_mock_data
try:
    from src.database.adapters import get_database_adapter
except ImportError:
    logger.warning("Could not import get_database_adapter, will skip MongoDB population")
    get_database_adapter = None

try:
    from src.database.graph_manager import mongodb_graph_manager
except ImportError:
    logger.warning("Could not import mongodb_graph_manager, will skip graph manager operations")
    mongodb_graph_manager = None
try:
    from src.database.vc_pinecone_service import VCPineconeService
except ImportError:
    try:
        from TrendSense.src.database.vc_pinecone_service import VCPineconeService
    except ImportError:
        logger.warning("Could not import VCPineconeService, will skip Pinecone population")
        VCPineconeService = None

try:
    from src.embedding.pinecone_service import PineconeService
except ImportError:
    try:
        from TrendSense.src.embedding.pinecone_service import PineconeService
    except ImportError:
        logger.warning("Could not import PineconeService, will skip Pinecone population")
        PineconeService = None
from sentence_transformers import SentenceTransformer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def populate_mongodb(mock_data: Dict[str, List[Dict[str, Any]]]) -> bool:
    """
    Populate MongoDB with mock data.

    Args:
        mock_data: Dictionary containing mock data

    Returns:
        True if successful, False otherwise
    """
    if get_database_adapter is None:
        logger.error("Database adapter not available. Skipping MongoDB population.")
        return False

    try:
        # Get database adapter
        db_adapter = get_database_adapter()
        if not db_adapter.connect():
            logger.error("Failed to connect to database")
            return False

        # Store companies
        for company in mock_data["companies"]:
            db_adapter.create("companies", company)
        logger.info(f"Stored {len(mock_data['companies'])} companies in MongoDB")

        # Store trends
        for trend in mock_data["trends"]:
            db_adapter.create("trends", trend)
        logger.info(f"Stored {len(mock_data['trends'])} trends in MongoDB")

        # Store projects
        for project in mock_data["projects"]:
            db_adapter.create("projects", project)
        logger.info(f"Stored {len(mock_data['projects'])} projects in MongoDB")

        # Store graph nodes
        for node in mock_data["graph_nodes"]:
            db_adapter.create("graph_nodes", node)
        logger.info(f"Stored {len(mock_data['graph_nodes'])} graph nodes in MongoDB")

        # Store graph edges
        for edge in mock_data["graph_edges"]:
            db_adapter.create("graph_edges", edge)
        logger.info(f"Stored {len(mock_data['graph_edges'])} graph edges in MongoDB")

        return True

    except Exception as e:
        logger.error(f"Error populating MongoDB: {str(e)}")
        return False

def populate_pinecone(mock_data: Dict[str, List[Dict[str, Any]]]) -> bool:
    """
    Populate Pinecone with mock data.

    Args:
        mock_data: Dictionary containing mock data

    Returns:
        True if successful, False otherwise
    """
    if VCPineconeService is None:
        logger.warning("VCPineconeService not available. Skipping Pinecone population.")
        return False

    try:
        # Initialize VC Pinecone service
        vc_pinecone_service = VCPineconeService()
        if not vc_pinecone_service.is_available:
            logger.warning("Pinecone service is not available. Skipping vector storage.")
            return False

        # Store companies
        companies_stored = 0
        for company in mock_data["companies"]:
            if vc_pinecone_service.store_company(company):
                companies_stored += 1
        logger.info(f"Stored {companies_stored} companies in Pinecone")

        # Store projects
        projects_stored = 0
        for project in mock_data["projects"]:
            if vc_pinecone_service.store_project(project):
                projects_stored += 1
        logger.info(f"Stored {projects_stored} projects in Pinecone")

        # Store trends using the general PineconeService
        if PineconeService is None:
            logger.warning("PineconeService not available. Skipping trend vector storage.")
            return True  # Return True because we already stored companies and projects

        try:
            # Initialize embedding model
            model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

            # Initialize Pinecone service
            pinecone_service = PineconeService()
            if not pinecone_service.is_connected():
                logger.warning("General Pinecone service is not available. Skipping trend vector storage.")
                return True  # Return True because we already stored companies and projects

            # Store trends
            trends_stored = 0
            for trend in mock_data["trends"]:
                # Generate embedding
                text_to_embed = f"{trend['name']} {trend['description']} {trend['category']}"
                embedding = model.encode(text_to_embed).tolist()

                # Store in Pinecone
                metadata = {
                    "name": trend["name"],
                    "description": trend["description"],
                    "category": trend["category"],
                    "relevance_score": trend["relevance_score"],
                    "growth_rate": trend["growth_rate"],
                    "maturity_stage": trend["maturity_stage"],
                    "sectors": trend["sectors"]
                }

                if pinecone_service.store_vector(embedding, metadata, trend["_id"]):
                    trends_stored += 1

            logger.info(f"Stored {trends_stored} trends in Pinecone")

        except Exception as e:
            logger.error(f"Error storing trends in Pinecone: {str(e)}")
            # Continue because we already stored companies and projects

        return True

    except Exception as e:
        logger.error(f"Error populating Pinecone: {str(e)}")
        return False

def main():
    """Main function to populate mock data."""
    logger.info("Generating mock data...")
    mock_data = generate_all_mock_data()
    logger.info(f"Generated mock data: {len(mock_data['companies'])} companies, {len(mock_data['trends'])} trends, {len(mock_data['projects'])} projects")

    # Populate MongoDB
    logger.info("Populating MongoDB...")
    mongodb_success = populate_mongodb(mock_data)
    if mongodb_success:
        logger.info("Successfully populated MongoDB with mock data")
    else:
        logger.error("Failed to populate MongoDB with mock data")

    # Populate Pinecone
    logger.info("Populating Pinecone...")
    pinecone_success = populate_pinecone(mock_data)
    if pinecone_success:
        logger.info("Successfully populated Pinecone with mock data")
    else:
        logger.error("Failed to populate Pinecone with mock data")

    # Final status
    if mongodb_success and pinecone_success:
        logger.info("Successfully populated all data stores with mock data")
    elif mongodb_success:
        logger.info("Successfully populated MongoDB, but failed to populate Pinecone")
    elif pinecone_success:
        logger.info("Successfully populated Pinecone, but failed to populate MongoDB")
    else:
        logger.error("Failed to populate any data stores with mock data")

if __name__ == "__main__":
    main()
