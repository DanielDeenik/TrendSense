"""
Entity Traversal

This module provides functionality for traversing the Fund → Company → Project structure.
"""

import logging
from typing import Dict, List, Any, Optional

# Import database adapter
from src.database.adapters import get_database_adapter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EntityTraversal:
    """Class for traversing the Fund → Company → Project structure."""
    
    def __init__(self):
        """Initialize the entity traversal."""
        self.db_adapter = get_database_adapter()
        
        # Ensure database connection
        if not self.db_adapter.is_connected():
            self.db_adapter.connect()
    
    def get_fund_hierarchy(self, fund_id: str) -> Dict[str, Any]:
        """
        Get a fund's hierarchy.
        
        Args:
            fund_id: ID of the fund
            
        Returns:
            Dictionary with fund, companies, and projects
        """
        try:
            # Get fund
            fund = self.db_adapter.find_one('funds', {'_id': fund_id})
            
            if not fund:
                return {
                    'success': False,
                    'error': f"Fund not found: {fund_id}"
                }
            
            # Get companies
            companies = []
            if 'portfolio_companies' in fund:
                for company_id in fund['portfolio_companies']:
                    company = self.db_adapter.find_one('companies', {'_id': company_id})
                    if company:
                        companies.append(company)
            
            # Get projects
            projects = []
            for company in companies:
                if 'projects' in company:
                    for project_id in company['projects']:
                        project = self.db_adapter.find_one('projects', {'_id': project_id})
                        if project:
                            projects.append(project)
            
            return {
                'success': True,
                'fund': fund,
                'companies': companies,
                'projects': projects
            }
        
        except Exception as e:
            logger.error(f"Error getting fund hierarchy: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_company_hierarchy(self, company_id: str) -> Dict[str, Any]:
        """
        Get a company's hierarchy.
        
        Args:
            company_id: ID of the company
            
        Returns:
            Dictionary with company, projects, and funds
        """
        try:
            # Get company
            company = self.db_adapter.find_one('companies', {'_id': company_id})
            
            if not company:
                return {
                    'success': False,
                    'error': f"Company not found: {company_id}"
                }
            
            # Get projects
            projects = []
            if 'projects' in company:
                for project_id in company['projects']:
                    project = self.db_adapter.find_one('projects', {'_id': project_id})
                    if project:
                        projects.append(project)
            
            # Get funds
            funds = []
            fund_list = self.db_adapter.find('funds', {'portfolio_companies': company_id})
            funds.extend(fund_list)
            
            return {
                'success': True,
                'company': company,
                'projects': projects,
                'funds': funds
            }
        
        except Exception as e:
            logger.error(f"Error getting company hierarchy: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_project_hierarchy(self, project_id: str) -> Dict[str, Any]:
        """
        Get a project's hierarchy.
        
        Args:
            project_id: ID of the project
            
        Returns:
            Dictionary with project, company, and funds
        """
        try:
            # Get project
            project = self.db_adapter.find_one('projects', {'_id': project_id})
            
            if not project:
                return {
                    'success': False,
                    'error': f"Project not found: {project_id}"
                }
            
            # Get company
            company = None
            if 'company_id' in project:
                company = self.db_adapter.find_one('companies', {'_id': project['company_id']})
            
            # Get funds
            funds = []
            if company:
                fund_list = self.db_adapter.find('funds', {'portfolio_companies': company['_id']})
                funds.extend(fund_list)
            
            return {
                'success': True,
                'project': project,
                'company': company,
                'funds': funds
            }
        
        except Exception as e:
            logger.error(f"Error getting project hierarchy: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_all_companies(self, sector: Optional[str] = None) -> Dict[str, Any]:
        """
        Get all companies, optionally filtered by sector.
        
        Args:
            sector: Sector to filter by
            
        Returns:
            Dictionary with companies
        """
        try:
            # Create query
            query = {}
            if sector:
                query['sector'] = sector
            
            # Get companies
            companies = self.db_adapter.find('companies', query)
            
            return {
                'success': True,
                'companies': companies,
                'count': len(companies)
            }
        
        except Exception as e:
            logger.error(f"Error getting companies: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_all_projects(self, status: Optional[str] = None) -> Dict[str, Any]:
        """
        Get all projects, optionally filtered by status.
        
        Args:
            status: Status to filter by
            
        Returns:
            Dictionary with projects
        """
        try:
            # Create query
            query = {}
            if status:
                query['status'] = status
            
            # Get projects
            projects = self.db_adapter.find('projects', query)
            
            return {
                'success': True,
                'projects': projects,
                'count': len(projects)
            }
        
        except Exception as e:
            logger.error(f"Error getting projects: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
