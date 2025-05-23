"""
AI Connector utilities for SustainaTrend™.
Provides utility functions for AI service integration.
"""

import os
import logging
from typing import Dict, Any, Optional, List, Union
import google.generativeai as genai
from openai import OpenAI
from pinecone import Pinecone, Index

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Global clients
_openai_client = None
_gemini_client = None
_pinecone_client = None
_pinecone_index = None

def connect_to_ai_services() -> Dict[str, bool]:
    """
    Connect to AI services.
    
    Returns:
        Dict with connection status for each service
    """
    global _openai_client, _gemini_client, _pinecone_client, _pinecone_index
    
    services_status = {
        "openai": False,
        "gemini": False,
        "pinecone": False
    }
    
    # Initialize OpenAI
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            _openai_client = OpenAI(api_key=api_key)
            services_status["openai"] = True
            logger.info("OpenAI client initialized successfully")
        else:
            logger.warning("OpenAI API key not found in environment variables")
    except Exception as e:
        logger.error(f"Error initializing OpenAI: {str(e)}")
    
    # Initialize Gemini
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            _gemini_client = genai
            services_status["gemini"] = True
            logger.info("Gemini client initialized successfully")
        else:
            logger.warning("Gemini API key not found in environment variables")
    except Exception as e:
        logger.error(f"Error initializing Gemini: {str(e)}")
    
    # Initialize Pinecone
    try:
        api_key = os.getenv('PINECONE_API_KEY')
        if api_key:
            _pinecone_client = Pinecone(api_key=api_key)
            index_name = os.getenv('PINECONE_INDEX', 'sustainatrend')
            _pinecone_index = _pinecone_client.Index(index_name)
            services_status["pinecone"] = True
            logger.info("Pinecone client initialized successfully")
        else:
            logger.warning("Pinecone API key not found in environment variables")
    except Exception as e:
        logger.error(f"Error initializing Pinecone: {str(e)}")
    
    return services_status

def get_openai_client() -> Optional[OpenAI]:
    """
    Get OpenAI client.
    
    Returns:
        OpenAI client or None if not initialized
    """
    global _openai_client
    if _openai_client is None:
        try:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                _openai_client = OpenAI(api_key=api_key)
                logger.info("OpenAI client initialized successfully")
            else:
                logger.warning("OpenAI API key not found in environment variables")
        except Exception as e:
            logger.error(f"Error initializing OpenAI: {str(e)}")
    return _openai_client

def get_generative_ai() -> Optional[Any]:
    """
    Get Gemini client.
    
    Returns:
        Gemini client or None if not initialized
    """
    global _gemini_client
    if _gemini_client is None:
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
                _gemini_client = genai
                logger.info("Gemini client initialized successfully")
            else:
                logger.warning("Gemini API key not found in environment variables")
        except Exception as e:
            logger.error(f"Error initializing Gemini: {str(e)}")
    return _gemini_client

def get_rag_system() -> Optional[Index]:
    """
    Get Pinecone RAG system.
    
    Returns:
        Pinecone index or None if not initialized
    """
    global _pinecone_index
    if _pinecone_index is None:
        try:
            api_key = os.getenv('PINECONE_API_KEY')
            if api_key:
                _pinecone_client = Pinecone(api_key=api_key)
                index_name = os.getenv('PINECONE_INDEX', 'sustainatrend')
                _pinecone_index = _pinecone_client.Index(index_name)
                logger.info("Pinecone index initialized successfully")
            else:
                logger.warning("Pinecone API key not found in environment variables")
        except Exception as e:
            logger.error(f"Error initializing Pinecone: {str(e)}")
    return _pinecone_index

def is_pinecone_available() -> bool:
    """
    Check if Pinecone is available.
    
    Returns:
        True if Pinecone is available, False otherwise
    """
    return get_rag_system() is not None

def generate_embedding(text: str) -> List[float]:
    """
    Generate embeddings for text using OpenAI.
    
    Args:
        text: Text to generate embeddings for
        
    Returns:
        List of embedding values or empty list if error
    """
    client = get_openai_client()
    if not client:
        return []
    
    try:
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Error generating embedding: {str(e)}")
        return []
