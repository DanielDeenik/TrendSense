"""
Premium ESG Data Connectors for TrendSense™

This module provides connectors to premium ESG data providers to replace
mock data dependency and provide institutional-grade data reliability.
"""

import os
import logging
import requests
import json
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import time

# Configure logging
logger = logging.getLogger(__name__)


class ESGDataProvider(ABC):
    """Base class for premium ESG data providers"""
    
    def __init__(self, api_key: str, base_url: str, rate_limit: int = 100):
        """
        Initialize ESG data provider.
        
        Args:
            api_key: API key for the provider
            base_url: Base URL for the provider's API
            rate_limit: Requests per minute limit
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.rate_limit = rate_limit
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'TrendSense/1.0'
        })
        
        # Rate limiting
        self.last_request_time = 0
        self.request_interval = 60.0 / rate_limit  # seconds between requests
    
    def _rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.request_interval:
            sleep_time = self.request_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict[str, Any]:
        """
        Make a rate-limited request to the API.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            API response data
        """
        self._rate_limit()
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for {self.__class__.__name__}: {str(e)}")
            raise
    
    @abstractmethod
    def get_company_esg_data(self, company_id: str) -> Dict[str, Any]:
        """Fetch real-time ESG data for a company"""
        pass
    
    @abstractmethod
    def get_regulatory_data(self, framework: str) -> Dict[str, Any]:
        """Fetch regulatory framework data"""
        pass
    
    @abstractmethod
    def search_companies(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for companies by name or identifier"""
        pass
    
    @abstractmethod
    def get_industry_benchmarks(self, industry: str) -> Dict[str, Any]:
        """Get industry ESG benchmarks"""
        pass


class RefinitivESGConnector(ESGDataProvider):
    """Refinitiv ESG data connector"""
    
    def __init__(self, api_key: str = None):
        api_key = api_key or os.getenv('REFINITIV_API_KEY')
        if not api_key:
            raise ValueError("Refinitiv API key is required")
        
        super().__init__(
            api_key=api_key,
            base_url='https://api.refinitiv.com/data/esg/v1',
            rate_limit=60  # 60 requests per minute
        )
    
    def get_company_esg_data(self, company_id: str) -> Dict[str, Any]:
        """
        Fetch ESG data from Refinitiv.
        
        Args:
            company_id: Company identifier (RIC, ISIN, etc.)
            
        Returns:
            Comprehensive ESG data
        """
        try:
            # Get ESG scores
            scores_data = self._make_request(f'companies/{company_id}/scores')
            
            # Get ESG metrics
            metrics_data = self._make_request(f'companies/{company_id}/metrics')
            
            # Get controversies
            controversies_data = self._make_request(f'companies/{company_id}/controversies')
            
            return {
                'provider': 'Refinitiv',
                'company_id': company_id,
                'timestamp': datetime.now().isoformat(),
                'esg_scores': {
                    'environmental': scores_data.get('environmental_score', 0),
                    'social': scores_data.get('social_score', 0),
                    'governance': scores_data.get('governance_score', 0),
                    'combined': scores_data.get('esg_score', 0),
                    'percentile_rank': scores_data.get('percentile_rank', 0)
                },
                'metrics': {
                    'carbon_emissions': metrics_data.get('carbon_emissions', {}),
                    'water_usage': metrics_data.get('water_usage', {}),
                    'waste_management': metrics_data.get('waste_management', {}),
                    'energy_efficiency': metrics_data.get('energy_efficiency', {}),
                    'employee_metrics': metrics_data.get('employee_metrics', {}),
                    'board_diversity': metrics_data.get('board_diversity', {})
                },
                'controversies': controversies_data.get('controversies', []),
                'data_quality': {
                    'completeness': scores_data.get('data_completeness', 0),
                    'last_updated': scores_data.get('last_updated'),
                    'confidence_score': scores_data.get('confidence_score', 0)
                }
            }
        except Exception as e:
            logger.error(f"Error fetching Refinitiv ESG data for {company_id}: {str(e)}")
            return self._get_fallback_data(company_id)
    
    def get_regulatory_data(self, framework: str) -> Dict[str, Any]:
        """Fetch regulatory framework data"""
        try:
            return self._make_request(f'regulatory/{framework.lower()}')
        except Exception as e:
            logger.error(f"Error fetching regulatory data for {framework}: {str(e)}")
            return {}
    
    def search_companies(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for companies"""
        try:
            params = {'q': query, 'limit': limit}
            return self._make_request('companies/search', params).get('companies', [])
        except Exception as e:
            logger.error(f"Error searching companies: {str(e)}")
            return []
    
    def get_industry_benchmarks(self, industry: str) -> Dict[str, Any]:
        """Get industry ESG benchmarks"""
        try:
            return self._make_request(f'benchmarks/industry/{industry}')
        except Exception as e:
            logger.error(f"Error fetching industry benchmarks for {industry}: {str(e)}")
            return {}
    
    def _get_fallback_data(self, company_id: str) -> Dict[str, Any]:
        """Provide fallback data when API fails"""
        return {
            'provider': 'Refinitiv',
            'company_id': company_id,
            'timestamp': datetime.now().isoformat(),
            'esg_scores': {
                'environmental': 0,
                'social': 0,
                'governance': 0,
                'combined': 0,
                'percentile_rank': 0
            },
            'metrics': {},
            'controversies': [],
            'data_quality': {
                'completeness': 0,
                'last_updated': None,
                'confidence_score': 0
            },
            'error': 'API unavailable - using fallback data'
        }


class BloombergESGConnector(ESGDataProvider):
    """Bloomberg ESG data connector"""
    
    def __init__(self, api_key: str = None):
        api_key = api_key or os.getenv('BLOOMBERG_API_KEY')
        if not api_key:
            raise ValueError("Bloomberg API key is required")
        
        super().__init__(
            api_key=api_key,
            base_url='https://api.bloomberg.com/esg/v1',
            rate_limit=120  # 120 requests per minute
        )
    
    def get_company_esg_data(self, company_id: str) -> Dict[str, Any]:
        """Fetch ESG data from Bloomberg"""
        try:
            # Bloomberg uses different endpoint structure
            data = self._make_request(f'companies/{company_id}/esg-scores')
            
            return {
                'provider': 'Bloomberg',
                'company_id': company_id,
                'timestamp': datetime.now().isoformat(),
                'esg_scores': {
                    'environmental': data.get('environmental_disclosure_score', 0),
                    'social': data.get('social_disclosure_score', 0),
                    'governance': data.get('governance_disclosure_score', 0),
                    'combined': data.get('esg_disclosure_score', 0),
                    'percentile_rank': data.get('esg_percentile', 0)
                },
                'metrics': {
                    'carbon_intensity': data.get('carbon_intensity', 0),
                    'energy_intensity': data.get('energy_intensity', 0),
                    'water_intensity': data.get('water_intensity', 0),
                    'waste_intensity': data.get('waste_intensity', 0),
                    'employee_turnover': data.get('employee_turnover', 0),
                    'board_independence': data.get('board_independence', 0)
                },
                'data_quality': {
                    'completeness': data.get('data_availability', 0),
                    'last_updated': data.get('as_of_date'),
                    'confidence_score': data.get('quality_score', 0)
                }
            }
        except Exception as e:
            logger.error(f"Error fetching Bloomberg ESG data for {company_id}: {str(e)}")
            return self._get_fallback_data(company_id)
    
    def get_regulatory_data(self, framework: str) -> Dict[str, Any]:
        """Fetch regulatory framework data"""
        try:
            return self._make_request(f'regulatory-frameworks/{framework.lower()}')
        except Exception as e:
            logger.error(f"Error fetching regulatory data for {framework}: {str(e)}")
            return {}
    
    def search_companies(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for companies"""
        try:
            params = {'query': query, 'limit': limit}
            return self._make_request('search/companies', params).get('results', [])
        except Exception as e:
            logger.error(f"Error searching companies: {str(e)}")
            return []
    
    def get_industry_benchmarks(self, industry: str) -> Dict[str, Any]:
        """Get industry ESG benchmarks"""
        try:
            return self._make_request(f'benchmarks/{industry}')
        except Exception as e:
            logger.error(f"Error fetching industry benchmarks for {industry}: {str(e)}")
            return {}
    
    def _get_fallback_data(self, company_id: str) -> Dict[str, Any]:
        """Provide fallback data when API fails"""
        return {
            'provider': 'Bloomberg',
            'company_id': company_id,
            'timestamp': datetime.now().isoformat(),
            'esg_scores': {
                'environmental': 0,
                'social': 0,
                'governance': 0,
                'combined': 0,
                'percentile_rank': 0
            },
            'metrics': {},
            'data_quality': {
                'completeness': 0,
                'last_updated': None,
                'confidence_score': 0
            },
            'error': 'API unavailable - using fallback data'
        }


class MSCIESGConnector(ESGDataProvider):
    """MSCI ESG data connector"""
    
    def __init__(self, api_key: str = None):
        api_key = api_key or os.getenv('MSCI_API_KEY')
        if not api_key:
            raise ValueError("MSCI API key is required")
        
        super().__init__(
            api_key=api_key,
            base_url='https://api.msci.com/esg/v1',
            rate_limit=100  # 100 requests per minute
        )
    
    def get_company_esg_data(self, company_id: str) -> Dict[str, Any]:
        """Fetch ESG data from MSCI"""
        try:
            data = self._make_request(f'companies/{company_id}/ratings')
            
            return {
                'provider': 'MSCI',
                'company_id': company_id,
                'timestamp': datetime.now().isoformat(),
                'esg_scores': {
                    'environmental': data.get('environmental_score', 0),
                    'social': data.get('social_score', 0),
                    'governance': data.get('governance_score', 0),
                    'combined': data.get('esg_rating_score', 0),
                    'rating': data.get('esg_rating', 'Not Rated'),
                    'percentile_rank': data.get('industry_percentile', 0)
                },
                'key_issues': data.get('key_issues', []),
                'opportunities': data.get('opportunities', []),
                'data_quality': {
                    'completeness': data.get('coverage_ratio', 0),
                    'last_updated': data.get('last_update_date'),
                    'confidence_score': data.get('rating_confidence', 0)
                }
            }
        except Exception as e:
            logger.error(f"Error fetching MSCI ESG data for {company_id}: {str(e)}")
            return self._get_fallback_data(company_id)
    
    def get_regulatory_data(self, framework: str) -> Dict[str, Any]:
        """Fetch regulatory framework data"""
        try:
            return self._make_request(f'frameworks/{framework.lower()}')
        except Exception as e:
            logger.error(f"Error fetching regulatory data for {framework}: {str(e)}")
            return {}
    
    def search_companies(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for companies"""
        try:
            params = {'name': query, 'limit': limit}
            return self._make_request('companies/search', params).get('companies', [])
        except Exception as e:
            logger.error(f"Error searching companies: {str(e)}")
            return []
    
    def get_industry_benchmarks(self, industry: str) -> Dict[str, Any]:
        """Get industry ESG benchmarks"""
        try:
            return self._make_request(f'industries/{industry}/benchmarks')
        except Exception as e:
            logger.error(f"Error fetching industry benchmarks for {industry}: {str(e)}")
            return {}
    
    def _get_fallback_data(self, company_id: str) -> Dict[str, Any]:
        """Provide fallback data when API fails"""
        return {
            'provider': 'MSCI',
            'company_id': company_id,
            'timestamp': datetime.now().isoformat(),
            'esg_scores': {
                'environmental': 0,
                'social': 0,
                'governance': 0,
                'combined': 0,
                'rating': 'Not Rated',
                'percentile_rank': 0
            },
            'key_issues': [],
            'opportunities': [],
            'data_quality': {
                'completeness': 0,
                'last_updated': None,
                'confidence_score': 0
            },
            'error': 'API unavailable - using fallback data'
        }


class SustainalyticsConnector(ESGDataProvider):
    """Sustainalytics ESG data connector"""
    
    def __init__(self, api_key: str = None):
        api_key = api_key or os.getenv('SUSTAINALYTICS_API_KEY')
        if not api_key:
            raise ValueError("Sustainalytics API key is required")
        
        super().__init__(
            api_key=api_key,
            base_url='https://api.sustainalytics.com/v1',
            rate_limit=80  # 80 requests per minute
        )
    
    def get_company_esg_data(self, company_id: str) -> Dict[str, Any]:
        """Fetch ESG data from Sustainalytics"""
        try:
            data = self._make_request(f'companies/{company_id}/esg-risk')
            
            return {
                'provider': 'Sustainalytics',
                'company_id': company_id,
                'timestamp': datetime.now().isoformat(),
                'esg_scores': {
                    'esg_risk_score': data.get('esg_risk_score', 0),
                    'risk_category': data.get('risk_category', 'Unknown'),
                    'industry_percentile': data.get('industry_percentile', 0),
                    'global_percentile': data.get('global_percentile', 0)
                },
                'risk_breakdown': {
                    'material_esg_issues': data.get('material_esg_issues', []),
                    'management_score': data.get('management_score', 0),
                    'exposure_score': data.get('exposure_score', 0)
                },
                'controversies': data.get('controversies', []),
                'data_quality': {
                    'coverage': data.get('coverage_percentage', 0),
                    'last_updated': data.get('last_update'),
                    'confidence_score': data.get('assessment_confidence', 0)
                }
            }
        except Exception as e:
            logger.error(f"Error fetching Sustainalytics ESG data for {company_id}: {str(e)}")
            return self._get_fallback_data(company_id)
    
    def get_regulatory_data(self, framework: str) -> Dict[str, Any]:
        """Fetch regulatory framework data"""
        try:
            return self._make_request(f'regulatory/{framework.lower()}')
        except Exception as e:
            logger.error(f"Error fetching regulatory data for {framework}: {str(e)}")
            return {}
    
    def search_companies(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for companies"""
        try:
            params = {'q': query, 'limit': limit}
            return self._make_request('search', params).get('results', [])
        except Exception as e:
            logger.error(f"Error searching companies: {str(e)}")
            return []
    
    def get_industry_benchmarks(self, industry: str) -> Dict[str, Any]:
        """Get industry ESG benchmarks"""
        try:
            return self._make_request(f'benchmarks/industry/{industry}')
        except Exception as e:
            logger.error(f"Error fetching industry benchmarks for {industry}: {str(e)}")
            return {}
    
    def _get_fallback_data(self, company_id: str) -> Dict[str, Any]:
        """Provide fallback data when API fails"""
        return {
            'provider': 'Sustainalytics',
            'company_id': company_id,
            'timestamp': datetime.now().isoformat(),
            'esg_scores': {
                'esg_risk_score': 0,
                'risk_category': 'Unknown',
                'industry_percentile': 0,
                'global_percentile': 0
            },
            'risk_breakdown': {
                'material_esg_issues': [],
                'management_score': 0,
                'exposure_score': 0
            },
            'controversies': [],
            'data_quality': {
                'coverage': 0,
                'last_updated': None,
                'confidence_score': 0
            },
            'error': 'API unavailable - using fallback data'
        }


class MockPremiumESGConnector(ESGDataProvider):
    """Mock premium ESG connector for development/testing"""
    
    def __init__(self):
        super().__init__(
            api_key='mock_key',
            base_url='https://mock.esg.api',
            rate_limit=1000
        )
    
    def get_company_esg_data(self, company_id: str) -> Dict[str, Any]:
        """Generate realistic mock ESG data"""
        import random
        
        # Generate realistic scores with some correlation
        base_score = random.randint(40, 90)
        env_score = max(0, min(100, base_score + random.randint(-15, 15)))
        social_score = max(0, min(100, base_score + random.randint(-10, 10)))
        gov_score = max(0, min(100, base_score + random.randint(-12, 12)))
        combined_score = (env_score + social_score + gov_score) / 3
        
        return {
            'provider': 'Mock Premium',
            'company_id': company_id,
            'timestamp': datetime.now().isoformat(),
            'esg_scores': {
                'environmental': env_score,
                'social': social_score,
                'governance': gov_score,
                'combined': round(combined_score, 2),
                'percentile_rank': random.randint(10, 95)
            },
            'metrics': {
                'carbon_intensity': random.uniform(50, 200),
                'water_intensity': random.uniform(10, 100),
                'waste_intensity': random.uniform(5, 50),
                'energy_efficiency': random.uniform(60, 95),
                'employee_satisfaction': random.uniform(70, 95),
                'board_diversity': random.uniform(20, 60)
            },
            'data_quality': {
                'completeness': random.uniform(75, 98),
                'last_updated': (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                'confidence_score': random.uniform(80, 95)
            },
            'is_mock': True
        }
    
    def get_regulatory_data(self, framework: str) -> Dict[str, Any]:
        """Generate mock regulatory data"""
        return {
            'framework': framework,
            'compliance_requirements': [
                'Environmental disclosure',
                'Social impact reporting',
                'Governance structure documentation'
            ],
            'is_mock': True
        }
    
    def search_companies(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Generate mock company search results"""
        companies = []
        for i in range(min(limit, 5)):
            companies.append({
                'id': f'mock_{query}_{i}',
                'name': f'{query} Company {i+1}',
                'ticker': f'{query.upper()}{i+1}',
                'industry': 'Technology',
                'is_mock': True
            })
        return companies
    
    def get_industry_benchmarks(self, industry: str) -> Dict[str, Any]:
        """Generate mock industry benchmarks"""
        import random
        
        return {
            'industry': industry,
            'benchmarks': {
                'environmental_score': random.randint(60, 80),
                'social_score': random.randint(65, 85),
                'governance_score': random.randint(70, 90),
                'combined_score': random.randint(65, 85)
            },
            'sample_size': random.randint(50, 200),
            'is_mock': True
        }
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict[str, Any]:
        """Override to avoid actual HTTP requests"""
        return {'mock': True, 'endpoint': endpoint, 'params': params}


def get_premium_data_connector(provider: str = None) -> ESGDataProvider:
    """
    Get a premium ESG data connector.
    
    Args:
        provider: Provider name ('refinitiv', 'bloomberg', 'msci', 'sustainalytics', 'mock')
        
    Returns:
        ESG data provider instance
    """
    # Map of providers to their environment variables and classes
    provider_map = {
        'refinitiv': {'env_var': 'REFINITIV_API_KEY', 'class': RefinitivESGConnector},
        'bloomberg': {'env_var': 'BLOOMBERG_API_KEY', 'class': BloombergESGConnector},
        'msci': {'env_var': 'MSCI_API_KEY', 'class': MSCIESGConnector},
        'sustainalytics': {'env_var': 'SUSTAINALYTICS_API_KEY', 'class': SustainalyticsConnector},
        'mock': {'env_var': None, 'class': MockPremiumESGConnector}
    }
    
    # If provider is not specified, try to determine from environment
    if provider is None:
        for prov_name, config in provider_map.items():
            if config['env_var'] and os.getenv(config['env_var']):
                provider = prov_name
                break
        else:  # No environment variables found
            provider = 'mock'
    
    provider = provider.lower()
    
    # Get the provider class from the map
    if provider in provider_map:
        try:
            return provider_map[provider]['class']()
        except ValueError as e:
            logger.warning(f"Failed to initialize {provider} connector: {str(e)}, falling back to mock")
            return MockPremiumESGConnector()
    else:
        logger.warning(f"Unsupported ESG data provider: {provider}, falling back to mock")
        return MockPremiumESGConnector()
