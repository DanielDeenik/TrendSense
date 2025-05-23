"""
MongoDB Graph Manager for SustainaTrend™

This module provides graph database capabilities using MongoDB's $graphLookup
and other graph-related features.
"""

import logging
from typing import Dict, List, Any, Optional, Union
from pymongo import MongoClient
from pymongo.errors import OperationFailure

from .mongodb_manager import mongodb_manager

# Configure logging
logger = logging.getLogger(__name__)

class MongoDBGraphManager:
    """
    MongoDB Graph Manager for SustainaTrend™.
    
    This class extends the functionality of the MongoDB Manager with
    graph-specific operations using MongoDB's $graphLookup and other
    graph-related features.
    """
    
    def __init__(self):
        """Initialize the MongoDB Graph Manager."""
        self.mongodb = mongodb_manager
    
    def supply_chain_graph(self, company_id: str, max_depth: int = 3) -> List[Dict]:
        """
        Get the supply chain graph for a company.
        
        Args:
            company_id: The ID of the company
            max_depth: Maximum depth of the supply chain to traverse
            
        Returns:
            List of nodes and edges in the supply chain graph
        """
        if not self.mongodb.is_connected():
            logger.error("Cannot get supply chain graph: Not connected to MongoDB")
            return []
        
        try:
            # Use $graphLookup to traverse the supply chain
            pipeline = [
                {"$match": {"_id": company_id}},
                {"$graphLookup": {
                    "from": "companies",
                    "startWith": "$supplier_ids",
                    "connectFromField": "supplier_ids",
                    "connectToField": "_id",
                    "as": "supply_chain",
                    "maxDepth": max_depth,
                    "depthField": "depth"
                }},
                {"$project": {
                    "name": 1,
                    "industry": 1,
                    "sustainability_score": 1,
                    "supply_chain": {
                        "$map": {
                            "input": "$supply_chain",
                            "as": "supplier",
                            "in": {
                                "_id": "$$supplier._id",
                                "name": "$$supplier.name",
                                "industry": "$$supplier.industry",
                                "sustainability_score": "$$supplier.sustainability_score",
                                "depth": "$$supplier.depth"
                            }
                        }
                    }
                }}
            ]
            
            result = list(self.mongodb.db.companies.aggregate(pipeline))
            
            if not result:
                logger.warning(f"No supply chain found for company {company_id}")
                return []
            
            # Transform the result into a graph format with nodes and edges
            company = result[0]
            nodes = [{
                "id": company["_id"],
                "name": company["name"],
                "type": "company",
                "industry": company.get("industry", "Unknown"),
                "sustainability_score": company.get("sustainability_score", 0),
                "depth": 0
            }]
            
            edges = []
            
            # Add supplier nodes and edges
            for supplier in company.get("supply_chain", []):
                supplier_id = supplier["_id"]
                nodes.append({
                    "id": supplier_id,
                    "name": supplier["name"],
                    "type": "supplier",
                    "industry": supplier.get("industry", "Unknown"),
                    "sustainability_score": supplier.get("sustainability_score", 0),
                    "depth": supplier.get("depth", 1)
                })
                
                # Find the parent in the supply chain
                parent_id = self._find_parent_supplier(company_id, supplier_id, result[0])
                
                edges.append({
                    "source": parent_id,
                    "target": supplier_id,
                    "type": "supplies"
                })
            
            return {"nodes": nodes, "edges": edges}
        
        except OperationFailure as e:
            logger.error(f"Error getting supply chain graph: {str(e)}")
            return []
    
    def _find_parent_supplier(self, company_id: str, supplier_id: str, company_data: Dict) -> str:
        """
        Find the parent supplier in the supply chain.
        
        Args:
            company_id: The ID of the main company
            supplier_id: The ID of the supplier to find the parent for
            company_data: The company data with supply chain information
            
        Returns:
            The ID of the parent supplier or the company ID if not found
        """
        # Check if the supplier is directly connected to the company
        if supplier_id in company_data.get("supplier_ids", []):
            return company_id
        
        # Otherwise, find the supplier with the lowest depth that has this supplier as a direct connection
        suppliers = sorted(company_data.get("supply_chain", []), key=lambda x: x.get("depth", 0))
        
        for potential_parent in suppliers:
            if supplier_id in potential_parent.get("supplier_ids", []):
                return potential_parent["_id"]
        
        # If no parent found, default to the company
        return company_id
    
    def product_material_graph(self, product_id: str) -> Dict:
        """
        Get the product-material graph for a product.
        
        Args:
            product_id: The ID of the product
            
        Returns:
            Graph of product and its materials
        """
        if not self.mongodb.is_connected():
            logger.error("Cannot get product-material graph: Not connected to MongoDB")
            return {}
        
        try:
            # Get the product and its materials
            product = self.mongodb.find_one("products", {"_id": product_id})
            
            if not product:
                logger.warning(f"Product {product_id} not found")
                return {}
            
            # Get all materials used in the product
            material_ids = product.get("material_ids", [])
            materials = list(self.mongodb.find("materials", {"_id": {"$in": material_ids}}))
            
            # Create graph nodes and edges
            nodes = [{
                "id": product["_id"],
                "name": product["name"],
                "type": "product",
                "category": product.get("category", "Unknown"),
                "sustainability_score": product.get("sustainability_score", 0)
            }]
            
            edges = []
            
            for material in materials:
                material_id = material["_id"]
                nodes.append({
                    "id": material_id,
                    "name": material["name"],
                    "type": "material",
                    "category": material.get("category", "Unknown"),
                    "sustainability_score": material.get("sustainability_score", 0),
                    "renewable": material.get("renewable", False)
                })
                
                edges.append({
                    "source": product_id,
                    "target": material_id,
                    "type": "contains",
                    "percentage": product.get("material_percentages", {}).get(material_id, 0)
                })
            
            return {"nodes": nodes, "edges": edges}
        
        except Exception as e:
            logger.error(f"Error getting product-material graph: {str(e)}")
            return {}
    
    def initiative_impact_graph(self, company_id: str) -> Dict:
        """
        Get the initiative-impact graph for a company.
        
        Args:
            company_id: The ID of the company
            
        Returns:
            Graph of initiatives and their impacts
        """
        if not self.mongodb.is_connected():
            logger.error("Cannot get initiative-impact graph: Not connected to MongoDB")
            return {}
        
        try:
            # Get the company and its initiatives
            company = self.mongodb.find_one("companies", {"_id": company_id})
            
            if not company:
                logger.warning(f"Company {company_id} not found")
                return {}
            
            # Get all initiatives for the company
            initiative_ids = company.get("initiative_ids", [])
            initiatives = list(self.mongodb.find("initiatives", {"_id": {"$in": initiative_ids}}))
            
            # Get all metrics related to these initiatives
            metric_ids = []
            for initiative in initiatives:
                metric_ids.extend(initiative.get("metric_ids", []))
            
            metrics = list(self.mongodb.find("metrics", {"_id": {"$in": metric_ids}}))
            
            # Create graph nodes and edges
            nodes = [{
                "id": company["_id"],
                "name": company["name"],
                "type": "company",
                "industry": company.get("industry", "Unknown"),
                "sustainability_score": company.get("sustainability_score", 0)
            }]
            
            edges = []
            
            # Add initiative nodes and edges
            for initiative in initiatives:
                initiative_id = initiative["_id"]
                nodes.append({
                    "id": initiative_id,
                    "name": initiative["name"],
                    "type": "initiative",
                    "category": initiative.get("category", "Unknown"),
                    "status": initiative.get("status", "Unknown"),
                    "impact_score": initiative.get("impact_score", 0)
                })
                
                edges.append({
                    "source": company_id,
                    "target": initiative_id,
                    "type": "implements"
                })
                
                # Add metric nodes and edges for this initiative
                for metric_id in initiative.get("metric_ids", []):
                    # Find the metric in our list
                    metric = next((m for m in metrics if m["_id"] == metric_id), None)
                    
                    if metric:
                        nodes.append({
                            "id": metric_id,
                            "name": metric["name"],
                            "type": "metric",
                            "category": metric.get("category", "Unknown"),
                            "unit": metric.get("unit", ""),
                            "value": metric.get("value", 0),
                            "target": metric.get("target", 0)
                        })
                        
                        edges.append({
                            "source": initiative_id,
                            "target": metric_id,
                            "type": "measures"
                        })
            
            return {"nodes": nodes, "edges": edges}
        
        except Exception as e:
            logger.error(f"Error getting initiative-impact graph: {str(e)}")
            return {}
    
    def sustainability_network(self, industry: str = None, min_score: float = None) -> Dict:
        """
        Get the sustainability network across companies.
        
        Args:
            industry: Filter by industry (optional)
            min_score: Minimum sustainability score (optional)
            
        Returns:
            Network graph of companies and their relationships
        """
        if not self.mongodb.is_connected():
            logger.error("Cannot get sustainability network: Not connected to MongoDB")
            return {}
        
        try:
            # Build the query
            query = {}
            if industry:
                query["industry"] = industry
            if min_score is not None:
                query["sustainability_score"] = {"$gte": min_score}
            
            # Get companies matching the criteria
            companies = list(self.mongodb.find("companies", query))
            
            if not companies:
                logger.warning(f"No companies found matching the criteria")
                return {}
            
            # Create graph nodes and edges
            nodes = []
            edges = []
            
            # Add company nodes
            for company in companies:
                company_id = company["_id"]
                nodes.append({
                    "id": company_id,
                    "name": company["name"],
                    "type": "company",
                    "industry": company.get("industry", "Unknown"),
                    "sustainability_score": company.get("sustainability_score", 0),
                    "size": len(company.get("supplier_ids", [])) + len(company.get("customer_ids", []))
                })
                
                # Add edges to suppliers
                for supplier_id in company.get("supplier_ids", []):
                    if any(c["_id"] == supplier_id for c in companies):
                        edges.append({
                            "source": supplier_id,
                            "target": company_id,
                            "type": "supplies"
                        })
                
                # Add edges to customers
                for customer_id in company.get("customer_ids", []):
                    if any(c["_id"] == customer_id for c in companies):
                        edges.append({
                            "source": company_id,
                            "target": customer_id,
                            "type": "supplies"
                        })
                
                # Add edges to partners
                for partner_id in company.get("partner_ids", []):
                    if any(c["_id"] == partner_id for c in companies):
                        edges.append({
                            "source": company_id,
                            "target": partner_id,
                            "type": "partners_with"
                        })
            
            return {"nodes": nodes, "edges": edges}
        
        except Exception as e:
            logger.error(f"Error getting sustainability network: {str(e)}")
            return {}
    
    def find_paths(self, start_id: str, end_id: str, collection: str, 
                  connection_field: str, max_depth: int = 5) -> List[List[str]]:
        """
        Find all paths between two nodes in a graph.
        
        Args:
            start_id: The ID of the starting node
            end_id: The ID of the ending node
            collection: The collection containing the nodes
            connection_field: The field containing connections
            max_depth: Maximum path depth
            
        Returns:
            List of paths, where each path is a list of node IDs
        """
        if not self.mongodb.is_connected():
            logger.error("Cannot find paths: Not connected to MongoDB")
            return []
        
        try:
            # Use $graphLookup to find all paths
            pipeline = [
                {"$match": {"_id": start_id}},
                {"$graphLookup": {
                    "from": collection,
                    "startWith": f"${connection_field}",
                    "connectFromField": connection_field,
                    "connectToField": "_id",
                    "as": "paths",
                    "maxDepth": max_depth,
                    "depthField": "depth"
                }},
                {"$project": {
                    "paths": {
                        "$filter": {
                            "input": "$paths",
                            "as": "node",
                            "cond": {"$eq": ["$$node._id", end_id]}
                        }
                    }
                }}
            ]
            
            result = list(self.mongodb.db[collection].aggregate(pipeline))
            
            if not result or not result[0].get("paths"):
                logger.warning(f"No paths found between {start_id} and {end_id}")
                return []
            
            # Reconstruct the paths
            paths = []
            for path_node in result[0]["paths"]:
                # We need to find the actual path from start to end
                path = self._reconstruct_path(start_id, end_id, path_node["depth"], collection, connection_field)
                if path:
                    paths.append(path)
            
            return paths
        
        except Exception as e:
            logger.error(f"Error finding paths: {str(e)}")
            return []
    
    def _reconstruct_path(self, start_id: str, end_id: str, depth: int, 
                         collection: str, connection_field: str) -> List[str]:
        """
        Reconstruct a path between two nodes.
        
        Args:
            start_id: The ID of the starting node
            end_id: The ID of the ending node
            depth: The depth of the path
            collection: The collection containing the nodes
            connection_field: The field containing connections
            
        Returns:
            The path as a list of node IDs
        """
        # For depth 1, it's a direct connection
        if depth == 1:
            return [start_id, end_id]
        
        # For deeper paths, we need to find intermediate nodes
        path = [start_id]
        current_id = start_id
        
        for _ in range(depth):
            # Find the next node in the path
            node = self.mongodb.find_one(collection, {"_id": current_id})
            if not node:
                return []
            
            connections = node.get(connection_field, [])
            
            # If we can reach the end directly, do so
            if end_id in connections:
                path.append(end_id)
                return path
            
            # Otherwise, find a node that can lead to the end
            for conn_id in connections:
                conn_node = self.mongodb.find_one(collection, {"_id": conn_id})
                if conn_node and end_id in conn_node.get(connection_field, []):
                    path.append(conn_id)
                    path.append(end_id)
                    return path
            
            # If no direct path found, just take the first connection
            if connections:
                next_id = connections[0]
                path.append(next_id)
                current_id = next_id
            else:
                # No more connections, path is incomplete
                return []
        
        return path

# Create a singleton instance
mongodb_graph_manager = MongoDBGraphManager()
