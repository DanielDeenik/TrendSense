"""
MongoDB Configuration
Configuration settings for MongoDB connection.
"""

import os
from typing import Dict, Any

# MongoDB connection settings
MONGODB_CONFIG: Dict[str, Any] = {
    'uri': os.getenv('MONGODB_URI', 'mongodb://localhost:27017'),
    'database': os.getenv('MONGODB_DATABASE', 'trendsense'),
    'options': {
        'connectTimeoutMS': 5000,
        'socketTimeoutMS': 5000,
        'serverSelectionTimeoutMS': 5000,
        'maxPoolSize': 50,
        'minPoolSize': 10
    }
}

# Collection names
COLLECTIONS = {
    'portfolio_companies': 'portfolio_companies',
    'sustainability_metrics': 'sustainability_metrics',
    'ingestion_logs': 'ingestion_logs'
}

# Index configurations
INDEXES = {
    'portfolio_companies': [
        {'key': [('id', 1)], 'unique': True},
        {'key': [('name', 1)]},
        {'key': [('sector', 1)]},
        {'key': [('status', 1)]}
    ],
    'sustainability_metrics': [
        {'key': [('company_id', 1), ('reporting_period', 1)], 'unique': True},
        {'key': [('reporting_period', 1)]}
    ],
    'ingestion_logs': [
        {'key': [('timestamp', 1)]},
        {'key': [('data_type', 1)]}
    ]
} 