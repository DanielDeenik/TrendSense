"""
ESG Data Scraping Script
Scrapes ESG data from various sources and stores it in MongoDB.
"""

import os
import sys
import logging
from datetime import datetime
from typing import List, Dict, Any

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.scrapers.esg_scraper import ESGScraper
from backend.database.mongodb_manager import MongoDBManager
from backend.config.mongodb_config import MONGODB_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def scrape_and_store_data(symbols: List[str] = None) -> None:
    """Scrape ESG data and store it in MongoDB"""
    try:
        # Initialize scraper and database manager
        scraper = ESGScraper()
        db_manager = MongoDBManager(
            uri=MONGODB_CONFIG['uri'],
            database_name=MONGODB_CONFIG['database']
        )
        
        logger.info("Starting ESG data scraping...")
        
        # Scrape data
        results = scraper.scrape(symbols)
        
        if not results:
            logger.warning("No data was scraped")
            return
        
        # Store data in MongoDB
        for data in results:
            try:
                if data['source'] == 'yahoo_finance':
                    # Store basic ESG data
                    db_manager.insert_esg_data(data)
                    logger.info(f"Stored ESG data for {data['symbol']}")
                elif data['source'] == 'yahoo_finance_sustainability':
                    # Store sustainability metrics
                    db_manager.insert_sustainability_metrics(data)
                    logger.info(f"Stored sustainability metrics for {data['symbol']}")
            except Exception as e:
                logger.error(f"Error storing data for {data.get('symbol', 'unknown')}: {str(e)}")
                continue
        
        logger.info("Data scraping and storage completed successfully")
        
    except Exception as e:
        logger.error(f"Error in scrape_and_store_data: {str(e)}")
        raise
    finally:
        if 'scraper' in locals():
            scraper.close_selenium_driver()
        if 'db_manager' in locals():
            db_manager.close()

if __name__ == '__main__':
    # Example usage
    symbols = [
        'AAPL',  # Apple
        'MSFT',  # Microsoft
        'GOOGL', # Google
        'AMZN',  # Amazon
        'META',  # Meta (Facebook)
        'TSLA',  # Tesla
        'NVDA',  # NVIDIA
        'JPM',   # JPMorgan Chase
        'JNJ',   # Johnson & Johnson
        'PG'     # Procter & Gamble
    ]
    
    scrape_and_store_data(symbols) 