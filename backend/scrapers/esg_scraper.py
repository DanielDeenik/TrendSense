"""
ESG Data Scraper
Collects ESG and sustainability data from various sources.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import time
from .base_scraper import BaseScraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ESGScraper(BaseScraper):
    """Scraper for ESG and sustainability data"""
    
    def __init__(self):
        super().__init__()
        self.sources = {
            'yahoo_finance': {
                'base_url': 'https://finance.yahoo.com/quote/{symbol}/sustainability',
                'api_url': 'https://query2.finance.yahoo.com/v1/finance/esgChart'
            }
        }
    
    def get_yahoo_esg_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get ESG data from Yahoo Finance"""
        try:
            # Construct API URL with parameters
            params = {
                'symbol': symbol,
                'interval': '1d',
                'range': '1y'
            }
            
            url = f"{self.sources['yahoo_finance']['api_url']}?{symbol}"
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if 'esgChart' not in data or 'result' not in data['esgChart']:
                logger.warning(f"No ESG data found for {symbol}")
                return None
            
            result = data['esgChart']['result'][0]
            
            # Extract and normalize data
            esg_data = {
                'symbol': symbol,
                'timestamp': datetime.now(),
                'source': 'yahoo_finance',
                'total_esg_score': result.get('totalEsg', {}).get('raw', 0),
                'environment_score': result.get('environmentScore', {}).get('raw', 0),
                'social_score': result.get('socialScore', {}).get('raw', 0),
                'governance_score': result.get('governanceScore', {}).get('raw', 0),
                'peer_count': result.get('peerCount', 0),
                'peer_esg_score': result.get('peerEsgScore', {}).get('raw', 0),
                'peer_environment_score': result.get('peerEnvironmentScore', {}).get('raw', 0),
                'peer_social_score': result.get('peerSocialScore', {}).get('raw', 0),
                'peer_governance_score': result.get('peerGovernanceScore', {}).get('raw', 0),
                'controversy_level': result.get('controversyLevel', 0),
                'carbon_emissions': {
                    'scope1': result.get('scope1Emissions', {}).get('raw', 0),
                    'scope2': result.get('scope2Emissions', {}).get('raw', 0),
                    'scope3': result.get('scope3Emissions', {}).get('raw', 0)
                }
            }
            
            return esg_data
            
        except Exception as e:
            logger.error(f"Error fetching Yahoo Finance ESG data for {symbol}: {str(e)}")
            return None
    
    def get_company_sustainability_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get detailed sustainability data from company's sustainability page"""
        try:
            url = self.sources['yahoo_finance']['base_url'].format(symbol=symbol)
            html = self.get_page(url, use_selenium=True)
            if not html:
                return None
            
            soup = self.parse_html(html)
            if not soup:
                return None
            
            # Extract sustainability metrics
            sustainability_data = {
                'symbol': symbol,
                'timestamp': datetime.now(),
                'source': 'yahoo_finance_sustainability',
                'metrics': {}
            }
            
            # Find and extract metrics from the page
            metrics_section = soup.find('div', {'class': 'sustainability-metrics'})
            if metrics_section:
                for metric in metrics_section.find_all('div', {'class': 'metric'}):
                    name = self.clean_text(metric.find('div', {'class': 'metric-name'}).text)
                    value = self.clean_text(metric.find('div', {'class': 'metric-value'}).text)
                    sustainability_data['metrics'][name] = value
            
            return sustainability_data
            
        except Exception as e:
            logger.error(f"Error fetching sustainability data for {symbol}: {str(e)}")
            return None
    
    def scrape(self, symbols: List[str] = None) -> List[Dict[str, Any]]:
        """Scrape ESG data for a list of company symbols"""
        if symbols is None:
            symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']  # Default symbols
        
        results = []
        for symbol in symbols:
            try:
                # Get basic ESG data
                esg_data = self.get_yahoo_esg_data(symbol)
                if esg_data:
                    results.append(esg_data)
                
                # Get detailed sustainability data
                sustainability_data = self.get_company_sustainability_data(symbol)
                if sustainability_data:
                    results.append(sustainability_data)
                
                # Respect rate limits
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error processing {symbol}: {str(e)}")
                continue
        
        return results 