"""
Data Manager for TrendSense Platform
Handles data import processes and MongoDB integration
"""

import os
import logging
from typing import Dict, List, Optional, Union
from datetime import datetime
from pymongo import MongoClient
from .data_import import ESGDataImporter, CarbonDataImporter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataManager:
    """Manages data import processes and database operations"""
    
    def __init__(self, mongodb_uri: str, db_name: str = 'trendsense'):
        self.mongodb_uri = mongodb_uri
        self.db_name = db_name
        self.client = None
        self.db = None
        self.connect_db()

    def connect_db(self) -> bool:
        """Establish MongoDB connection"""
        try:
            self.client = MongoClient(self.mongodb_uri)
            self.db = self.client[self.db_name]
            logger.info(f"Successfully connected to MongoDB database: {self.db_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            return False

    def import_esg_data(self, file_path: str) -> Dict:
        """Import ESG data from file"""
        try:
            logger.info(f"Starting ESG data import from {file_path}")
            importer = ESGDataImporter(file_path)
            
            logger.info("Reading ESG data file")
            if not importer.read_file():
                logger.error("Failed to read ESG data file")
                return {'success': False, 'message': 'Failed to read ESG data file'}

            logger.info("Processing ESG data")
            processed_data = importer.process_data()
            if not processed_data:
                logger.error("Failed to process ESG data")
                return {'success': False, 'message': 'Failed to process ESG data'}

            # Store in MongoDB
            logger.info("Storing ESG data in MongoDB")
            result = self.db.esg_data.insert_one({
                'import_date': datetime.now(),
                'source_file': file_path,
                'data': processed_data
            })
            logger.info(f"ESG data stored with ID: {result.inserted_id}")

            return {
                'success': True,
                'message': 'ESG data imported successfully',
                'import_id': str(result.inserted_id),
                'metrics': processed_data['metrics']
            }

        except Exception as e:
            logger.error(f"Error importing ESG data: {str(e)}")
            return {'success': False, 'message': f"Error importing ESG data: {str(e)}"}

    def import_carbon_data(self, file_path: str) -> Dict:
        """Import carbon emissions data from file"""
        try:
            logger.info(f"Starting carbon data import from {file_path}")
            importer = CarbonDataImporter(file_path)
            
            logger.info("Reading carbon data file")
            if not importer.read_file():
                logger.error("Failed to read carbon data file")
                return {'success': False, 'message': 'Failed to read carbon data file'}

            logger.info("Processing carbon data")
            processed_data = importer.process_data()
            if not processed_data:
                logger.error("Failed to process carbon data")
                return {'success': False, 'message': 'Failed to process carbon data'}

            # Store in MongoDB
            logger.info("Storing carbon data in MongoDB")
            result = self.db.carbon_data.insert_one({
                'import_date': datetime.now(),
                'source_file': file_path,
                'data': processed_data
            })
            logger.info(f"Carbon data stored with ID: {result.inserted_id}")

            return {
                'success': True,
                'message': 'Carbon data imported successfully',
                'import_id': str(result.inserted_id),
                'emissions': processed_data['emissions'],
                'benchmarks': processed_data['benchmarks']
            }

        except Exception as e:
            logger.error(f"Error importing carbon data: {str(e)}")
            return {'success': False, 'message': f"Error importing carbon data: {str(e)}"}

    def get_latest_esg_data(self, company_name: Optional[str] = None) -> Dict:
        """Retrieve latest ESG data from MongoDB"""
        try:
            query = {}
            if company_name:
                query['data.companies'] = company_name

            latest_data = self.db.esg_data.find_one(
                query,
                sort=[('import_date', -1)]
            )

            if not latest_data:
                return {'success': False, 'message': 'No ESG data found'}

            return {
                'success': True,
                'data': latest_data['data'],
                'import_date': latest_data['import_date']
            }

        except Exception as e:
            logger.error(f"Error retrieving ESG data: {str(e)}")
            return {'success': False, 'message': f"Error retrieving ESG data: {str(e)}"}

    def get_latest_carbon_data(self, company_name: Optional[str] = None) -> Dict:
        """Retrieve latest carbon emissions data from MongoDB"""
        try:
            query = {}
            if company_name:
                query['data.companies'] = company_name

            latest_data = self.db.carbon_data.find_one(
                query,
                sort=[('import_date', -1)]
            )

            if not latest_data:
                return {'success': False, 'message': 'No carbon data found'}

            return {
                'success': True,
                'data': latest_data['data'],
                'import_date': latest_data['import_date']
            }

        except Exception as e:
            logger.error(f"Error retrieving carbon data: {str(e)}")
            return {'success': False, 'message': f"Error retrieving carbon data: {str(e)}"}

    def get_company_sustainability_profile(self, company_name: str) -> Dict:
        """Get comprehensive sustainability profile for a company"""
        try:
            esg_data = self.get_latest_esg_data(company_name)
            carbon_data = self.get_latest_carbon_data(company_name)

            if not esg_data['success'] and not carbon_data['success']:
                return {'success': False, 'message': 'No data found for company'}

            profile = {
                'success': True,
                'company_name': company_name,
                'last_updated': datetime.now().isoformat(),
                'esg_metrics': esg_data.get('data', {}).get('metrics', {}),
                'emissions_data': carbon_data.get('data', {}).get('emissions', {}).get(company_name, {}),
                'benchmarks': {
                    'esg': esg_data.get('data', {}).get('benchmarks', {}),
                    'emissions': carbon_data.get('data', {}).get('benchmarks', {})
                }
            }

            return profile

        except Exception as e:
            logger.error(f"Error retrieving company profile: {str(e)}")
            return {'success': False, 'message': f"Error retrieving company profile: {str(e)}"}

    def get_portfolio_overview(self) -> Dict:
        """Get overview of entire portfolio sustainability metrics"""
        try:
            esg_data = self.get_latest_esg_data()
            carbon_data = self.get_latest_carbon_data()

            if not esg_data['success'] and not carbon_data['success']:
                return {'success': False, 'message': 'No portfolio data found'}

            overview = {
                'success': True,
                'last_updated': datetime.now().isoformat(),
                'companies_count': len(esg_data.get('data', {}).get('companies', [])),
                'average_metrics': {
                    'esg_score': sum(
                        score['mean'] for score in 
                        esg_data.get('data', {}).get('metrics', {}).get('esg_scores', {}).values()
                    ) / len(esg_data.get('data', {}).get('companies', [])),
                    'total_emissions': sum(
                        emissions['total_emissions'] for emissions in 
                        carbon_data.get('data', {}).get('emissions', {}).values()
                    )
                },
                'top_performers': self._get_top_performers(esg_data.get('data', {})),
                'risk_factors': self._analyze_risk_factors(esg_data.get('data', {}), carbon_data.get('data', {}))
            }

            return overview

        except Exception as e:
            logger.error(f"Error generating portfolio overview: {str(e)}")
            return {'success': False, 'message': f"Error generating portfolio overview: {str(e)}"}

    def _get_top_performers(self, esg_data: Dict) -> List[Dict]:
        """Identify top performing companies based on ESG scores"""
        try:
            scores = esg_data.get('metrics', {}).get('esg_scores', {})
            sorted_companies = sorted(
                scores.items(),
                key=lambda x: x[1]['mean'],
                reverse=True
            )[:5]

            return [
                {
                    'company_name': company,
                    'esg_score': scores['mean'],
                    'trend': 'positive' if scores['mean'] > scores['min'] else 'neutral'
                }
                for company, scores in sorted_companies
            ]
        except Exception:
            return []

    def _analyze_risk_factors(self, esg_data: Dict, carbon_data: Dict) -> List[Dict]:
        """Analyze sustainability risk factors across the portfolio"""
        try:
            risks = []
            
            # ESG Score Risk
            esg_scores = esg_data.get('metrics', {}).get('esg_scores', {})
            low_esg_companies = [
                company for company, scores in esg_scores.items()
                if scores['mean'] < 50
            ]
            if low_esg_companies:
                risks.append({
                    'type': 'esg_score',
                    'severity': 'high' if len(low_esg_companies) > 3 else 'medium',
                    'description': f"{len(low_esg_companies)} companies have ESG scores below 50"
                })

            # Emissions Risk
            emissions_data = carbon_data.get('emissions', {})
            high_emitters = [
                company for company, data in emissions_data.items()
                if data['total_emissions'] > carbon_data.get('benchmarks', {}).get('average_emissions', {}).get('total', 0) * 1.5
            ]
            if high_emitters:
                risks.append({
                    'type': 'emissions',
                    'severity': 'high' if len(high_emitters) > 2 else 'medium',
                    'description': f"{len(high_emitters)} companies exceed emissions benchmarks by 50%+"
                })

            return risks
        except Exception:
            return [] 