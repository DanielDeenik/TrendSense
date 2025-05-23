"""
Metrics Propagator

This module provides functionality for propagating metrics through the Fund → Company → Project structure.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

# Import database adapter
from src.database.adapters import get_database_adapter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetricsProgagator:
    """Class for propagating metrics through the Fund → Company → Project structure."""
    
    def __init__(self):
        """Initialize the metrics propagator."""
        self.db_adapter = get_database_adapter()
        
        # Ensure database connection
        if not self.db_adapter.is_connected():
            self.db_adapter.connect()
    
    def propagate_metrics(self, fund_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Propagate metrics through the Fund → Company → Project structure.
        
        Args:
            fund_id: ID of the fund to propagate metrics for, or None for all funds
            
        Returns:
            Dictionary with propagation results
        """
        try:
            # Get funds
            if fund_id:
                funds = [self.db_adapter.find_one('funds', {'_id': fund_id})]
                if not funds[0]:
                    return {
                        'success': False,
                        'error': f"Fund not found: {fund_id}"
                    }
            else:
                funds = self.db_adapter.find('funds')
            
            # Process each fund
            funds_processed = 0
            for fund in funds:
                if self._process_fund(fund):
                    funds_processed += 1
            
            return {
                'success': True,
                'funds_processed': funds_processed
            }
        
        except Exception as e:
            logger.error(f"Error propagating metrics: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _process_fund(self, fund: Dict[str, Any]) -> bool:
        """
        Process a fund by aggregating metrics from its portfolio companies.
        
        Args:
            fund: Fund document
            
        Returns:
            True if successful, False otherwise
        """
        try:
            fund_id = fund['_id']
            fund_name = fund.get('name', 'Unknown Fund')
            portfolio_companies = fund.get('portfolio_companies', [])
            
            logger.info(f"Processing fund: {fund_name} ({fund_id})")
            
            # Get companies
            companies = []
            for company_id in portfolio_companies:
                company = self.db_adapter.find_one('companies', {'_id': company_id})
                if company:
                    companies.append(company)
            
            if not companies:
                logger.warning(f"No companies found for fund: {fund_name}")
                return False
            
            # Process each company
            company_metrics = []
            for company in companies:
                company_result = self._process_company(company)
                if company_result:
                    company_metrics.append(company_result)
            
            if not company_metrics:
                logger.warning(f"No company metrics found for fund: {fund_name}")
                return False
            
            # Aggregate company metrics
            env_scores = [m.get('environmental_score', 0) for m in company_metrics]
            social_scores = [m.get('social_score', 0) for m in company_metrics]
            gov_scores = [m.get('governance_score', 0) for m in company_metrics]
            esg_scores = [m.get('esg_score', 0) for m in company_metrics]
            carbon_impacts = [m.get('carbon_impact', 0) for m in company_metrics]
            
            # Calculate average scores
            avg_env_score = sum(env_scores) / len(env_scores) if env_scores else 0
            avg_social_score = sum(social_scores) / len(social_scores) if social_scores else 0
            avg_gov_score = sum(gov_scores) / len(gov_scores) if gov_scores else 0
            avg_esg_score = sum(esg_scores) / len(esg_scores) if esg_scores else 0
            total_carbon_impact = sum(carbon_impacts) if carbon_impacts else 0
            
            # Update fund metrics
            self.db_adapter.update_one(
                'funds',
                {'_id': fund_id},
                {'$set': {
                    'sustainability_metrics.environmental_score': avg_env_score,
                    'sustainability_metrics.social_score': avg_social_score,
                    'sustainability_metrics.governance_score': avg_gov_score,
                    'sustainability_metrics.esg_score': avg_esg_score,
                    'sustainability_metrics.carbon_impact': total_carbon_impact,
                    'updated_at': datetime.now().isoformat()
                }}
            )
            
            logger.info(f"Updated metrics for fund: {fund_name}")
            return True
        
        except Exception as e:
            logger.error(f"Error processing fund: {str(e)}")
            return False
    
    def _process_company(self, company: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a company by aggregating metrics from its projects.
        
        Args:
            company: Company document
            
        Returns:
            Dictionary with company metrics, or None if unsuccessful
        """
        try:
            company_id = company['_id']
            company_name = company.get('name', 'Unknown Company')
            company_projects = company.get('projects', [])
            
            logger.info(f"Processing company: {company_name} ({company_id})")
            
            # Get projects
            projects = []
            for project_id in company_projects:
                project = self.db_adapter.find_one('projects', {'_id': project_id})
                if project:
                    projects.append(project)
            
            if not projects:
                logger.warning(f"No projects found for company: {company_name}")
                return self._estimate_missing_metrics(company)
            
            # Process each project
            project_metrics = []
            for project in projects:
                project_result = self._process_project(project)
                if project_result:
                    project_metrics.append(project_result)
            
            if not project_metrics:
                logger.warning(f"No project metrics found for company: {company_name}")
                return self._estimate_missing_metrics(company)
            
            # Aggregate project metrics
            env_scores = [m.get('environmental_score', 0) for m in project_metrics]
            social_scores = [m.get('social_score', 0) for m in project_metrics]
            gov_scores = [m.get('governance_score', 0) for m in project_metrics]
            carbon_impacts = [m.get('carbon_impact', 0) for m in project_metrics]
            
            # Calculate average scores
            avg_env_score = sum(env_scores) / len(env_scores) if env_scores else 0
            avg_social_score = sum(social_scores) / len(social_scores) if social_scores else 0
            avg_gov_score = sum(gov_scores) / len(gov_scores) if gov_scores else 0
            total_carbon_impact = sum(carbon_impacts) if carbon_impacts else 0
            
            # Calculate overall ESG score
            esg_score = (avg_env_score + avg_social_score + avg_gov_score) / 3
            
            # Update company metrics
            self.db_adapter.update_one(
                'companies',
                {'_id': company_id},
                {'$set': {
                    'sustainability_metrics.environmental_score': avg_env_score,
                    'sustainability_metrics.social_score': avg_social_score,
                    'sustainability_metrics.governance_score': avg_gov_score,
                    'sustainability_metrics.esg_score': esg_score,
                    'sustainability_metrics.carbon_impact': total_carbon_impact,
                    'updated_at': datetime.now().isoformat()
                }}
            )
            
            logger.info(f"Updated metrics for company: {company_name}")
            
            # Return company metrics
            return {
                'company_id': company_id,
                'environmental_score': avg_env_score,
                'social_score': avg_social_score,
                'governance_score': avg_gov_score,
                'esg_score': esg_score,
                'carbon_impact': total_carbon_impact
            }
        
        except Exception as e:
            logger.error(f"Error processing company: {str(e)}")
            return None
    
    def _process_project(self, project: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a project by extracting its metrics.
        
        Args:
            project: Project document
            
        Returns:
            Dictionary with project metrics, or None if unsuccessful
        """
        try:
            project_id = project['_id']
            project_name = project.get('name', 'Unknown Project')
            
            logger.info(f"Processing project: {project_name} ({project_id})")
            
            # Get sustainability metrics
            metrics = project.get('sustainability_metrics', {})
            
            # Extract metrics
            env_score = metrics.get('environmental_score', 0)
            social_score = metrics.get('social_score', 0)
            gov_score = metrics.get('governance_score', 0)
            carbon_impact = metrics.get('carbon_impact', 0)
            
            # Return project metrics
            return {
                'project_id': project_id,
                'environmental_score': env_score,
                'social_score': social_score,
                'governance_score': gov_score,
                'carbon_impact': carbon_impact
            }
        
        except Exception as e:
            logger.error(f"Error processing project: {str(e)}")
            return None
    
    def _estimate_missing_metrics(self, entity: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Estimate missing metrics based on sector and similar entities.
        
        Args:
            entity: Entity document
            
        Returns:
            Dictionary with estimated metrics, or None if unsuccessful
        """
        try:
            entity_id = entity['_id']
            entity_name = entity.get('name', 'Unknown Entity')
            entity_type = 'company' if 'sector' in entity else 'fund'
            
            logger.info(f"Estimating metrics for {entity_type}: {entity_name} ({entity_id})")
            
            # Get existing metrics
            metrics = entity.get('sustainability_metrics', {})
            
            # Extract metrics
            env_score = metrics.get('environmental_score', 0)
            social_score = metrics.get('social_score', 0)
            gov_score = metrics.get('governance_score', 0)
            esg_score = metrics.get('esg_score', 0)
            carbon_impact = metrics.get('carbon_impact', 0)
            
            # If no metrics, estimate based on sector or similar entities
            if entity_type == 'company' and (env_score == 0 and social_score == 0 and gov_score == 0):
                sector = entity.get('sector')
                
                if sector:
                    # Get similar companies
                    similar_companies = self.db_adapter.find(
                        'companies',
                        {'sector': sector, '_id': {'$ne': entity_id}}
                    )
                    
                    # Aggregate metrics
                    sector_env_scores = []
                    sector_social_scores = []
                    sector_gov_scores = []
                    sector_carbon_impacts = []
                    
                    for company in similar_companies:
                        company_metrics = company.get('sustainability_metrics', {})
                        
                        if 'environmental_score' in company_metrics:
                            sector_env_scores.append(company_metrics['environmental_score'])
                        
                        if 'social_score' in company_metrics:
                            sector_social_scores.append(company_metrics['social_score'])
                        
                        if 'governance_score' in company_metrics:
                            sector_gov_scores.append(company_metrics['governance_score'])
                        
                        if 'carbon_impact' in company_metrics:
                            sector_carbon_impacts.append(company_metrics['carbon_impact'])
                    
                    # Calculate average scores
                    if sector_env_scores:
                        env_score = sum(sector_env_scores) / len(sector_env_scores)
                    
                    if sector_social_scores:
                        social_score = sum(sector_social_scores) / len(sector_social_scores)
                    
                    if sector_gov_scores:
                        gov_score = sum(sector_gov_scores) / len(sector_gov_scores)
                    
                    if sector_carbon_impacts:
                        carbon_impact = sum(sector_carbon_impacts) / len(sector_carbon_impacts)
                    
                    # Calculate overall ESG score
                    esg_score = (env_score + social_score + gov_score) / 3
                    
                    # Update company metrics
                    self.db_adapter.update_one(
                        'companies',
                        {'_id': entity_id},
                        {'$set': {
                            'sustainability_metrics.environmental_score': env_score,
                            'sustainability_metrics.social_score': social_score,
                            'sustainability_metrics.governance_score': gov_score,
                            'sustainability_metrics.esg_score': esg_score,
                            'sustainability_metrics.carbon_impact': carbon_impact,
                            'updated_at': datetime.now().isoformat()
                        }}
                    )
                    
                    logger.info(f"Estimated metrics for company: {entity_name} based on sector: {sector}")
            
            # Return entity metrics
            return {
                'entity_id': entity_id,
                'environmental_score': env_score,
                'social_score': social_score,
                'governance_score': gov_score,
                'esg_score': esg_score,
                'carbon_impact': carbon_impact
            }
        
        except Exception as e:
            logger.error(f"Error estimating metrics: {str(e)}")
            return None
