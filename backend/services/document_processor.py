"""
Document Processor with Trendsense Integration

This module handles document processing and analysis with integration
with the Trendsense API for enhanced sustainability insights.
"""

import os
import re
import json
import logging
import openai
from datetime import datetime
from dotenv import load_dotenv
from .trendsense_client import TrendsenseClient

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Process sustainability documents with AI extraction and Trendsense integration"""
    
    def __init__(self):
        """Initialize the document processor"""
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.trendsense_client = TrendsenseClient()
        self.logger = logging.getLogger(__name__)
        
        # Initialize OpenAI if API key is available
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
            self.ai_available = True
        else:
            self.ai_available = False
            self.logger.warning("OpenAI API key not found. AI extraction will not be available.")
    
    def process_document(self, file_path, document_type, metadata=None):
        """
        Process a document and extract sustainability information
        
        Args:
            file_path (str): Path to the document file
            document_type (str): Type of document (e.g., 'sustainability_report', 'esg_disclosure')
            metadata (dict, optional): Additional metadata about the document
            
        Returns:
            dict: Extracted data and analysis results
        """
        try:
            # Read document content
            with open(file_path, 'r', encoding='utf-8') as file:
                document_text = file.read()
            
            # Extract structured fields
            extracted_fields = self.extract_structured_fields(document_text, document_type)
            
            # Prepare metadata
            if metadata is None:
                metadata = {}
            
            metadata.update({
                'document_type': document_type,
                'file_name': os.path.basename(file_path),
                'file_size': os.path.getsize(file_path),
                'processed_at': datetime.now().isoformat()
            })
            
            # Send to Trendsense for enhanced analysis
            trendsense_result = self.send_to_trendsense(extracted_fields, document_text, metadata)
            
            # Combine results
            result = {
                'success': True,
                'extracted_fields': extracted_fields,
                'metadata': metadata,
                'trendsense_analysis': trendsense_result.get('data', {}) if trendsense_result.get('success') else None,
                'trendsense_status': 'success' if trendsense_result.get('success') else 'unavailable'
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing document: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def extract_structured_fields(self, document_text, document_type):
        """
        Extract structured fields from document text
        
        Args:
            document_text (str): Text content of the document
            document_type (str): Type of document
            
        Returns:
            dict: Extracted structured fields
        """
        # Try AI extraction if available
        if self.ai_available:
            try:
                return self._extract_with_ai(document_text, document_type)
            except Exception as e:
                self.logger.warning(f"AI extraction failed: {str(e)}. Falling back to regex.")
        
        # Fallback to regex extraction
        return self._extract_with_regex(document_text, document_type)
    
    def _extract_with_ai(self, document_text, document_type):
        """
        Extract fields using OpenAI API
        
        Args:
            document_text (str): Text content of the document
            document_type (str): Type of document
            
        Returns:
            dict: Extracted structured fields
        """
        # Define extraction prompt based on document type
        if document_type == 'sustainability_report':
            prompt = """
            Extract the following information from this sustainability report:
            - Company name
            - Reporting year
            - Carbon emissions (scope 1, 2, 3)
            - Water usage
            - Renewable energy percentage
            - Waste management metrics
            - Sustainability goals
            - ESG score if available
            
            Format the response as a JSON object with these fields.
            """
        elif document_type == 'esg_disclosure':
            prompt = """
            Extract the following information from this ESG disclosure:
            - Company name
            - Disclosure year
            - Environmental metrics
            - Social metrics
            - Governance metrics
            - Risk factors
            - Compliance status
            
            Format the response as a JSON object with these fields.
            """
        else:
            prompt = """
            Extract key sustainability information from this document.
            Include company name, metrics, goals, and compliance information.
            Format the response as a JSON object.
            """
        
        # Truncate document text if too long
        max_tokens = 4000
        truncated_text = document_text[:max_tokens] if len(document_text) > max_tokens else document_text
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a sustainability data extraction assistant."},
                {"role": "user", "content": f"{prompt}\n\nDocument:\n{truncated_text}"}
            ],
            temperature=0.2,
            max_tokens=1000
        )
        
        # Parse response
        try:
            extracted_text = response.choices[0].message.content
            # Find JSON in the response
            json_match = re.search(r'\{.*\}', extracted_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            else:
                # If no JSON found, create a structured response
                return {
                    'extracted_text': extracted_text,
                    'document_type': document_type
                }
        except Exception as e:
            self.logger.error(f"Error parsing AI response: {str(e)}")
            return {
                'error': f"Failed to parse AI response: {str(e)}",
                'document_type': document_type
            }
    
    def _extract_with_regex(self, document_text, document_type):
        """
        Extract fields using regex patterns
        
        Args:
            document_text (str): Text content of the document
            document_type (str): Type of document
            
        Returns:
            dict: Extracted structured fields
        """
        # Define regex patterns based on document type
        patterns = {
            'company_name': r'Company\s+Name:?\s*([^\n]+)',
            'reporting_year': r'(?:Report|Year|FY|Fiscal Year)[\s:]+(\d{4})',
            'carbon_emissions': r'Carbon\s+emissions:?\s*([\d,.]+)\s*(?:tCO2e|tons|tonnes)',
            'water_usage': r'Water\s+usage:?\s*([\d,.]+)\s*(?:m³|cubic meters|gallons)',
            'renewable_energy': r'Renewable\s+energy:?\s*([\d,.]+)\s*%',
            'esg_score': r'ESG\s+score:?\s*([\d,.]+)'
        }
        
        # Extract fields using regex
        extracted_fields = {}
        for field, pattern in patterns.items():
            match = re.search(pattern, document_text, re.IGNORECASE)
            if match:
                extracted_fields[field] = match.group(1).strip()
        
        # Add document type
        extracted_fields['document_type'] = document_type
        
        return extracted_fields
    
    def send_to_trendsense(self, extracted_fields, document_text, metadata):
        """
        Send extracted document data to Trendsense for enhanced analysis
        
        Args:
            extracted_fields (dict): Extracted structured data
            document_text (str): Full text of the document
            metadata (dict): Document metadata
            
        Returns:
            dict: Analysis results from Trendsense
        """
        return self.trendsense_client.submit_document_analysis(
            extracted_fields, 
            document_text, 
            metadata
        ) 