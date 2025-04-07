"""
Data Import System for TrendSense Platform
Handles importing and processing sustainability data from various sources
"""

import os
import json
import pandas as pd
import logging
from datetime import datetime
from typing import Dict, List, Union, Optional
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataImporter(ABC):
    """Abstract base class for data importers"""
    
    def __init__(self, source_path: str):
        self.source_path = source_path
        self.data = None
        self.metadata = {
            'import_date': datetime.now().isoformat(),
            'source': source_path,
            'status': 'pending'
        }

    @abstractmethod
    def validate_data(self) -> bool:
        """Validate the imported data"""
        pass

    @abstractmethod
    def process_data(self) -> Dict:
        """Process the imported data into standardized format"""
        pass

    def log_import_status(self, success: bool, message: str):
        """Log import status and details"""
        self.metadata.update({
            'status': 'success' if success else 'failed',
            'message': message,
            'completion_time': datetime.now().isoformat()
        })
        logger.info(f"Data import {self.metadata['status']}: {message}")

class ESGDataImporter(DataImporter):
    """Handles ESG data imports from CSV/Excel files"""
    
    REQUIRED_COLUMNS = [
        'company_name',
        'date',
        'esg_score',
        'environmental_score',
        'social_score',
        'governance_score'
    ]

    def __init__(self, source_path: str):
        super().__init__(source_path)
        self.file_extension = os.path.splitext(source_path)[1].lower()

    def read_file(self) -> bool:
        """Read the data file based on its extension"""
        try:
            if self.file_extension == '.csv':
                self.data = pd.read_csv(self.source_path)
            elif self.file_extension in ['.xlsx', '.xls']:
                self.data = pd.read_excel(self.source_path)
            else:
                raise ValueError(f"Unsupported file format: {self.file_extension}")
            
            # Handle column name differences
            if 'company' in self.data.columns and 'company_name' not in self.data.columns:
                self.data = self.data.rename(columns={'company': 'company_name'})
                
            return True
        except Exception as e:
            self.log_import_status(False, f"Error reading file: {str(e)}")
            return False

    def validate_data(self) -> bool:
        """Validate ESG data structure and content"""
        if self.data is None:
            return False

        # Check required columns
        missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in self.data.columns]
        if missing_columns:
            self.log_import_status(False, f"Missing required columns: {missing_columns}")
            return False

        # Validate data types
        try:
            self.data['date'] = pd.to_datetime(self.data['date'])
            numeric_columns = [col for col in self.data.columns if 'score' in col]
            self.data[numeric_columns] = self.data[numeric_columns].apply(pd.to_numeric)
            return True
        except Exception as e:
            self.log_import_status(False, f"Data validation error: {str(e)}")
            return False

    def process_data(self) -> Dict:
        """Process ESG data into standardized format"""
        if not self.validate_data():
            return {}

        try:
            processed_data = {
                'metadata': self.metadata,
                'companies': self.data['company_name'].unique().tolist(),
                'time_range': {
                    'start': self.data['date'].min().isoformat(),
                    'end': self.data['date'].max().isoformat()
                },
                'metrics': {
                    'esg_scores': self.data.groupby('company_name')['esg_score'].agg(['mean', 'min', 'max']).to_dict('index'),
                    'environmental_scores': self.data.groupby('company_name')['environmental_score'].mean().to_dict(),
                    'social_scores': self.data.groupby('company_name')['social_score'].mean().to_dict(),
                    'governance_scores': self.data.groupby('company_name')['governance_score'].mean().to_dict()
                },
                'trends': {
                    company: self.data[self.data['company_name'] == company][['date', 'esg_score']].values.tolist()
                    for company in self.data['company_name'].unique()
                }
            }
            self.log_import_status(True, "Data processed successfully")
            return processed_data
        except Exception as e:
            self.log_import_status(False, f"Error processing data: {str(e)}")
            return {}

class CarbonDataImporter(DataImporter):
    """Handles carbon emissions and environmental impact data imports"""
    
    REQUIRED_COLUMNS = [
        'company_name',
        'date',
        'scope1_emissions',
        'scope2_emissions',
        'scope3_emissions',
        'energy_consumption',
        'renewable_energy_percentage'
    ]

    def __init__(self, source_path: str):
        super().__init__(source_path)
        self.file_extension = os.path.splitext(source_path)[1].lower()

    def read_file(self) -> bool:
        """Read the carbon data file"""
        try:
            if self.file_extension == '.csv':
                self.data = pd.read_csv(self.source_path)
            elif self.file_extension in ['.xlsx', '.xls']:
                self.data = pd.read_excel(self.source_path)
            else:
                raise ValueError(f"Unsupported file format: {self.file_extension}")
            
            # Handle column name differences
            if 'company' in self.data.columns and 'company_name' not in self.data.columns:
                self.data = self.data.rename(columns={'company': 'company_name'})
                
            if 'renewable_energy_pct' in self.data.columns and 'renewable_energy_percentage' not in self.data.columns:
                self.data = self.data.rename(columns={'renewable_energy_pct': 'renewable_energy_percentage'})
                
            return True
        except Exception as e:
            self.log_import_status(False, f"Error reading file: {str(e)}")
            return False

    def validate_data(self) -> bool:
        """Validate carbon data structure and content"""
        if self.data is None:
            return False

        # Check required columns
        missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in self.data.columns]
        if missing_columns:
            self.log_import_status(False, f"Missing required columns: {missing_columns}")
            return False

        # Validate data types and ranges
        try:
            numeric_columns = ['scope1_emissions', 'scope2_emissions', 'scope3_emissions', 
                             'energy_consumption', 'renewable_energy_percentage']
            self.data[numeric_columns] = self.data[numeric_columns].apply(pd.to_numeric)
            
            # Validate percentage range
            if not all(self.data['renewable_energy_percentage'].between(0, 100)):
                self.log_import_status(False, "Renewable energy percentage must be between 0 and 100")
                return False
                
            return True
        except Exception as e:
            self.log_import_status(False, f"Data validation error: {str(e)}")
            return False

    def process_data(self) -> Dict:
        """Process carbon data into standardized format"""
        if not self.validate_data():
            return {}

        try:
            processed_data = {
                'metadata': self.metadata,
                'companies': self.data['company_name'].unique().tolist(),
                'emissions': {
                    company: {
                        'total_emissions': row['scope1_emissions'] + row['scope2_emissions'] + row['scope3_emissions'],
                        'scope1': row['scope1_emissions'],
                        'scope2': row['scope2_emissions'],
                        'scope3': row['scope3_emissions'],
                        'energy_consumption': row['energy_consumption'],
                        'renewable_percentage': row['renewable_energy_percentage']
                    }
                    for company, row in self.data.groupby('company_name').agg({
                        'scope1_emissions': 'sum',
                        'scope2_emissions': 'sum',
                        'scope3_emissions': 'sum',
                        'energy_consumption': 'sum',
                        'renewable_energy_percentage': 'mean'
                    }).iterrows()
                },
                'benchmarks': {
                    'average_emissions': {
                        'scope1': self.data['scope1_emissions'].mean(),
                        'scope2': self.data['scope2_emissions'].mean(),
                        'scope3': self.data['scope3_emissions'].mean()
                    },
                    'average_renewable': self.data['renewable_energy_percentage'].mean()
                }
            }
            self.log_import_status(True, "Carbon data processed successfully")
            return processed_data
        except Exception as e:
            self.log_import_status(False, f"Error processing carbon data: {str(e)}")
            return {} 