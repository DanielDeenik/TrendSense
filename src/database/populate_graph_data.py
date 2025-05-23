"""
Populate Graph Data Script for TrendSense

This script directly populates the graph data in the database for the graph analytics feature.
"""

import os
import sys
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import mock data generator
from src.database.mock_graph_data import generate_all_mock_data

def save_mock_data_to_json(mock_data, output_dir="src/database/mock_data"):
    """
    Save mock data to JSON files.

    Args:
        mock_data: Dictionary containing mock data
        output_dir: Directory to save JSON files
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Save each data type to a separate JSON file
    for data_type, data in mock_data.items():
        file_path = os.path.join(output_dir, f"{data_type}.json")
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved {len(data)} {data_type} to {file_path}")

def create_graph_data_js(mock_data, output_file="src/frontend/static/js/graph_data.js"):
    """
    Create a JavaScript file with graph data for direct use in the frontend.

    Args:
        mock_data: Dictionary containing mock data
        output_file: Path to the output JavaScript file
    """
    # Extract nodes and edges
    nodes = mock_data["graph_nodes"]
    edges = mock_data["graph_edges"]

    # Create JavaScript content
    js_content = """/**
 * Graph Data for TrendSense
 *
 * This file contains mock graph data for the graph analytics feature.
 * Generated automatically by the populate_graph_data.py script.
 */

// Graph nodes
const graphNodes = %s;

// Graph edges
const graphEdges = %s;

// Export data
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        nodes: graphNodes,
        edges: graphEdges
    };
}
""" % (json.dumps(nodes, indent=2), json.dumps(edges, indent=2))

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write to file
    with open(output_file, 'w') as f:
        f.write(js_content)

    logger.info(f"Created graph data JavaScript file at {output_file}")
    logger.info(f"Added {len(nodes)} nodes and {len(edges)} edges to the graph data")

def main():
    """Main function to populate graph data."""
    logger.info("Generating mock data...")
    mock_data = generate_all_mock_data()
    logger.info(f"Generated mock data: {len(mock_data['companies'])} companies, {len(mock_data['trends'])} trends, {len(mock_data['projects'])} projects")

    # Save mock data to JSON files
    save_mock_data_to_json(mock_data)

    # Create graph data JavaScript file
    create_graph_data_js(mock_data)

    logger.info("Successfully populated graph data")

if __name__ == "__main__":
    main()
