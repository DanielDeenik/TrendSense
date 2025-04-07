"""
TrendsenseClient - Client for interacting with Trendsense API

This module provides a client for interacting with the Trendsense API
for sustainability intelligence and analysis.
"""

import os
import json
import logging
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TrendsenseClient:
    """Client for interacting with Trendsense API for sustainability intelligence"""
    
    def __init__(self):
        """Initialize the Trendsense client with API credentials"""
        self.api_key = os.environ.get("TRENDSENSE_API_KEY")
        self.base_url = os.environ.get("TRENDSENSE_API_URL", "https://api.trendsense.io/v1")
        self.logger = logging.getLogger(__name__)
        self.is_connected = self.validate_connection()
        
    def validate_connection(self):
        """Validate Trendsense API connection"""
        if not self.api_key:
            self.logger.warning("Trendsense API key not found in environment variables")
            return False
            
        try:
            response = requests.get(
                f"{self.base_url}/health",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Failed to connect to Trendsense API: {str(e)}")
            return False
    
    def submit_document_analysis(self, document_data, document_text, metadata):
        """
        Submit document data to Trendsense for advanced analysis
        
        Args:
            document_data (dict): Extracted structured data from the document
            document_text (str): Full text of the document
            metadata (dict): Document metadata
            
        Returns:
            dict: Analysis results from Trendsense
        """
        if not self.is_connected:
            self.logger.warning("Trendsense connection not available")
            return {'success': False, 'reason': 'connection_unavailable'}
            
        try:
            # Format data for Trendsense
            payload = {
                'document_data': document_data,
                'document_text': document_text[:5000],  # Send sample for context
                'metadata': metadata,
                'source': 'sustainatrend_platform'
            }
            
            response = requests.post(
                f"{self.base_url}/analyze/document",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return {'success': True, 'data': response.json()}
            else:
                self.logger.error(f"Trendsense API error: {response.status_code} - {response.text}")
                return {'success': False, 'reason': f"api_error_{response.status_code}"}
                
        except Exception as e:
            self.logger.error(f"Error submitting document to Trendsense: {str(e)}")
            return {'success': False, 'reason': 'request_failed', 'error': str(e)}
    
    def get_sustainability_score(self, company_data):
        """
        Get sustainability score for a company
        
        Args:
            company_data (dict): Company information and metrics
            
        Returns:
            dict: Sustainability score and analysis
        """
        if not self.is_connected:
            self.logger.warning("Trendsense connection not available")
            return {'success': False, 'reason': 'connection_unavailable'}
            
        try:
            response = requests.post(
                f"{self.base_url}/analyze/company",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=company_data,
                timeout=15
            )
            
            if response.status_code == 200:
                return {'success': True, 'data': response.json()}
            else:
                self.logger.error(f"Trendsense API error: {response.status_code} - {response.text}")
                return {'success': False, 'reason': f"api_error_{response.status_code}"}
                
        except Exception as e:
            self.logger.error(f"Error getting sustainability score: {str(e)}")
            return {'success': False, 'reason': 'request_failed', 'error': str(e)}
    
    def get_industry_benchmarks(self, sector, metrics=None):
        """
        Get industry benchmarks for sustainability metrics
        
        Args:
            sector (str): Industry sector
            metrics (list, optional): Specific metrics to benchmark
            
        Returns:
            dict: Industry benchmark data
        """
        if not self.is_connected:
            self.logger.warning("Trendsense connection not available")
            return {'success': False, 'reason': 'connection_unavailable'}
            
        try:
            payload = {'sector': sector}
            if metrics:
                payload['metrics'] = metrics
                
            response = requests.post(
                f"{self.base_url}/benchmarks/industry",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                return {'success': True, 'data': response.json()}
            else:
                self.logger.error(f"Trendsense API error: {response.status_code} - {response.text}")
                return {'success': False, 'reason': f"api_error_{response.status_code}"}
                
        except Exception as e:
            self.logger.error(f"Error getting industry benchmarks: {str(e)}")
            return {'success': False, 'reason': 'request_failed', 'error': str(e)}
    
    def get_trend_analysis(self, sector, timeframe="1y"):
        """
        Get trend analysis for a sector
        
        Args:
            sector (str): Industry sector
            timeframe (str): Analysis timeframe (e.g., "1m", "3m", "6m", "1y")
            
        Returns:
            dict: Trend analysis data
        """
        if not self.is_connected:
            self.logger.warning("Trendsense connection not available")
            return {'success': False, 'reason': 'connection_unavailable'}
            
        try:
            response = requests.get(
                f"{self.base_url}/trends/sector/{sector}",
                headers={"Authorization": f"Bearer {self.api_key}"},
                params={"timeframe": timeframe},
                timeout=15
            )
            
            if response.status_code == 200:
                return {'success': True, 'data': response.json()}
            else:
                self.logger.error(f"Trendsense API error: {response.status_code} - {response.text}")
                return {'success': False, 'reason': f"api_error_{response.status_code}"}
                
        except Exception as e:
            self.logger.error(f"Error getting trend analysis: {str(e)}")
            return {'success': False, 'reason': 'request_failed', 'error': str(e)} 