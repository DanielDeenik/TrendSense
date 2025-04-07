"""
Base Scraper
Provides common functionality for all scrapers in the system.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Abstract base class for all scrapers"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.driver = None
    
    def get_selenium_driver(self) -> webdriver.Chrome:
        """Initialize and return a Selenium WebDriver instance"""
        if self.driver is None:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        return self.driver
    
    def close_selenium_driver(self):
        """Close the Selenium WebDriver instance"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def get_page(self, url: str, use_selenium: bool = False) -> Optional[str]:
        """Fetch a webpage and return its content"""
        try:
            if use_selenium:
                driver = self.get_selenium_driver()
                driver.get(url)
                return driver.page_source
            else:
                response = self.session.get(url)
                response.raise_for_status()
                return response.text
        except Exception as e:
            logger.error(f"Error fetching page {url}: {str(e)}")
            return None
    
    def parse_html(self, html: str) -> Optional[BeautifulSoup]:
        """Parse HTML content using BeautifulSoup"""
        try:
            return BeautifulSoup(html, 'html.parser')
        except Exception as e:
            logger.error(f"Error parsing HTML: {str(e)}")
            return None
    
    @abstractmethod
    def scrape(self) -> List[Dict[str, Any]]:
        """Scrape data from the target source"""
        pass
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return ""
        return " ".join(text.strip().split())
    
    def extract_date(self, date_str: str, formats: List[str] = None) -> Optional[datetime]:
        """Extract date from string using multiple formats"""
        if formats is None:
            formats = [
                '%Y-%m-%d',
                '%d/%m/%Y',
                '%m/%d/%Y',
                '%d-%m-%Y',
                '%Y/%m/%d'
            ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        
        return None 