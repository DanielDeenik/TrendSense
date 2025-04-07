"""
MongoDB Manager
Handles database operations for the application.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBManager:
    """Manager for MongoDB operations"""
    
    def __init__(self, uri: str, database_name: str = 'trendsense'):
        self.client = MongoClient(uri)
        self.db: Database = self.client[database_name]
        
        # Initialize collections
        self.portfolio_companies: Collection = self.db['portfolio_companies']
        self.sustainability_metrics: Collection = self.db['sustainability_metrics']
        self.ingestion_logs: Collection = self.db['ingestion_logs']
        
        # Create indexes
        self._create_indexes()
    
    def _create_indexes(self) -> None:
        """Create necessary indexes for collections"""
        try:
            # Portfolio companies indexes
            self.portfolio_companies.create_index('id', unique=True)
            self.portfolio_companies.create_index('name')
            self.portfolio_companies.create_index('sector')
            self.portfolio_companies.create_index('status')
            
            # Sustainability metrics indexes
            self.sustainability_metrics.create_index([('company_id', 1), ('reporting_period', 1)], unique=True)
            self.sustainability_metrics.create_index('reporting_period')
            
            # Ingestion logs indexes
            self.ingestion_logs.create_index('timestamp')
            self.ingestion_logs.create_index('data_type')
            
        except Exception as e:
            logger.error(f"Error creating indexes: {str(e)}")
            raise
    
    def insert_portfolio_companies(self, companies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Insert portfolio companies into the database"""
        try:
            result = self.portfolio_companies.insert_many(companies)
            return {
                'inserted_count': len(result.inserted_ids),
                'inserted_ids': [str(id) for id in result.inserted_ids]
            }
        except Exception as e:
            logger.error(f"Error inserting portfolio companies: {str(e)}")
            raise
    
    def insert_sustainability_metrics(self, metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Insert sustainability metrics into the database"""
        try:
            result = self.sustainability_metrics.insert_many(metrics)
            return {
                'inserted_count': len(result.inserted_ids),
                'inserted_ids': [str(id) for id in result.inserted_ids]
            }
        except Exception as e:
            logger.error(f"Error inserting sustainability metrics: {str(e)}")
            raise
    
    def insert_ingestion_log(self, log_entry: Dict[str, Any]) -> str:
        """Insert an ingestion log entry"""
        try:
            result = self.ingestion_logs.insert_one(log_entry)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error inserting ingestion log: {str(e)}")
            raise
    
    def get_portfolio_companies(self, 
                              filters: Optional[Dict[str, Any]] = None,
                              limit: int = 100,
                              skip: int = 0) -> List[Dict[str, Any]]:
        """Get portfolio companies with optional filters"""
        try:
            cursor = self.portfolio_companies.find(filters or {})
            return list(cursor.skip(skip).limit(limit))
        except Exception as e:
            logger.error(f"Error getting portfolio companies: {str(e)}")
            raise
    
    def get_sustainability_metrics(self,
                                 company_id: Optional[str] = None,
                                 start_date: Optional[datetime] = None,
                                 end_date: Optional[datetime] = None,
                                 limit: int = 100,
                                 skip: int = 0) -> List[Dict[str, Any]]:
        """Get sustainability metrics with optional filters"""
        try:
            filters = {}
            if company_id:
                filters['company_id'] = company_id
            if start_date or end_date:
                filters['reporting_period'] = {}
                if start_date:
                    filters['reporting_period']['$gte'] = start_date
                if end_date:
                    filters['reporting_period']['$lte'] = end_date
            
            cursor = self.sustainability_metrics.find(filters)
            return list(cursor.skip(skip).limit(limit))
        except Exception as e:
            logger.error(f"Error getting sustainability metrics: {str(e)}")
            raise
    
    def get_ingestion_logs(self,
                          data_type: Optional[str] = None,
                          start_date: Optional[datetime] = None,
                          end_date: Optional[datetime] = None,
                          limit: int = 100,
                          skip: int = 0) -> List[Dict[str, Any]]:
        """Get ingestion logs with optional filters"""
        try:
            filters = {}
            if data_type:
                filters['data_type'] = data_type
            if start_date or end_date:
                filters['timestamp'] = {}
                if start_date:
                    filters['timestamp']['$gte'] = start_date
                if end_date:
                    filters['timestamp']['$lte'] = end_date
            
            cursor = self.ingestion_logs.find(filters)
            return list(cursor.skip(skip).limit(limit))
        except Exception as e:
            logger.error(f"Error getting ingestion logs: {str(e)}")
            raise
    
    def update_portfolio_company(self, company_id: str, update_data: Dict[str, Any]) -> bool:
        """Update a portfolio company"""
        try:
            result = self.portfolio_companies.update_one(
                {'id': company_id},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating portfolio company: {str(e)}")
            raise
    
    def update_sustainability_metrics(self,
                                    company_id: str,
                                    reporting_period: datetime,
                                    update_data: Dict[str, Any]) -> bool:
        """Update sustainability metrics"""
        try:
            result = self.sustainability_metrics.update_one(
                {
                    'company_id': company_id,
                    'reporting_period': reporting_period
                },
                {'$set': update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating sustainability metrics: {str(e)}")
            raise
    
    def delete_portfolio_company(self, company_id: str) -> bool:
        """Delete a portfolio company"""
        try:
            result = self.portfolio_companies.delete_one({'id': company_id})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting portfolio company: {str(e)}")
            raise
    
    def delete_sustainability_metrics(self,
                                    company_id: str,
                                    reporting_period: datetime) -> bool:
        """Delete sustainability metrics"""
        try:
            result = self.sustainability_metrics.delete_one({
                'company_id': company_id,
                'reporting_period': reporting_period
            })
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting sustainability metrics: {str(e)}")
            raise
    
    def close(self) -> None:
        """Close the MongoDB connection"""
        try:
            self.client.close()
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {str(e)}")
            raise 