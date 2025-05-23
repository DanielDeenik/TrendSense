"""
AI Connector

This module provides a connector for AI services used in RAG processing.
"""

import logging
import os
import json
from typing import Dict, List, Any, Optional, Union
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIConnector:
    """Base class for AI connectors."""

    def __init__(self):
        """Initialize the AI connector."""
        self.available = False

    def is_available(self) -> bool:
        """
        Check if the AI service is available.

        Returns:
            True if available, False otherwise
        """
        return self.available

    def generate_text(self, prompt: str, options: Dict[str, Any] = None) -> str:
        """
        Generate text using the AI service.

        Args:
            prompt: Prompt for the AI
            options: Additional options for generation

        Returns:
            Generated text
        """
        raise NotImplementedError("Subclasses must implement generate_text")

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding for the text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        raise NotImplementedError("Subclasses must implement generate_embedding")

class OpenAIConnector(AIConnector):
    """Connector for OpenAI services."""

    def __init__(self, api_key: str = None):
        """
        Initialize the OpenAI connector.

        Args:
            api_key: OpenAI API key
        """
        super().__init__()
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')

        # Check if OpenAI is available
        try:
            import openai
            self.openai = openai
            self.openai.api_key = self.api_key
            self.available = True
            logger.info("OpenAI connector initialized successfully")
        except ImportError:
            logger.warning("OpenAI package not installed")
            self.openai = None
            self.available = False

    def generate_text(self, prompt: str, options: Dict[str, Any] = None) -> str:
        """
        Generate text using OpenAI.

        Args:
            prompt: Prompt for the AI
            options: Additional options for generation

        Returns:
            Generated text
        """
        if not self.is_available():
            logger.error("OpenAI is not available")
            return "AI service is not available"

        options = options or {}

        try:
            # Set up parameters
            model = options.get('model', 'gpt-3.5-turbo')
            max_tokens = options.get('max_tokens', 1000)
            temperature = options.get('temperature', 0.7)

            # Create messages
            messages = [
                {"role": "system", "content": options.get('system_prompt', "You are a helpful assistant.")},
                {"role": "user", "content": prompt}
            ]

            # Generate response
            response = self.openai.ChatCompletion.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )

            # Extract text from response
            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Error generating text with OpenAI: {str(e)}")
            logger.error(traceback.format_exc())
            return f"Error generating text: {str(e)}"

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding for the text using OpenAI.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        if not self.is_available():
            logger.error("OpenAI is not available")
            return []

        try:
            # Generate embedding
            response = self.openai.Embedding.create(
                input=text,
                model="text-embedding-ada-002"
            )

            # Extract embedding from response
            return response.data[0].embedding

        except Exception as e:
            logger.error(f"Error generating embedding with OpenAI: {str(e)}")
            logger.error(traceback.format_exc())
            return []

class HuggingFaceConnector(AIConnector):
    """Connector for Hugging Face services."""

    def __init__(self, api_key: str = None):
        """
        Initialize the Hugging Face connector.

        Args:
            api_key: Hugging Face API key
        """
        super().__init__()
        self.api_key = api_key or os.getenv('HUGGINGFACE_API_KEY')

        # Check if Hugging Face is available
        try:
            from transformers import pipeline
            import torch
            import numpy as np

            self.pipeline = pipeline
            self.torch = torch
            self.np = np
            self.available = True

            # Initialize text generation pipeline
            self.text_generator = None
            self.embedding_model = None

            logger.info("Hugging Face connector initialized successfully")
        except ImportError:
            logger.warning("Hugging Face packages not installed")
            self.pipeline = None
            self.torch = None
            self.np = None
            self.available = False

    def generate_text(self, prompt: str, options: Dict[str, Any] = None) -> str:
        """
        Generate text using Hugging Face.

        Args:
            prompt: Prompt for the AI
            options: Additional options for generation

        Returns:
            Generated text
        """
        if not self.is_available():
            logger.error("Hugging Face is not available")
            return "AI service is not available"

        options = options or {}

        try:
            # Initialize text generation pipeline if not already initialized
            if self.text_generator is None:
                model_name = options.get('model', 'gpt2')
                self.text_generator = self.pipeline('text-generation', model=model_name)

            # Set up parameters
            max_length = options.get('max_length', 100)
            temperature = options.get('temperature', 0.7)

            # Generate response
            response = self.text_generator(
                prompt,
                max_length=max_length,
                temperature=temperature,
                num_return_sequences=1
            )

            # Extract text from response
            return response[0]['generated_text'].strip()

        except Exception as e:
            logger.error(f"Error generating text with Hugging Face: {str(e)}")
            logger.error(traceback.format_exc())
            return f"Error generating text: {str(e)}"

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding for the text using Hugging Face.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        if not self.is_available():
            logger.error("Hugging Face is not available")
            return []

        try:
            # Initialize embedding model if not already initialized
            if self.embedding_model is None:
                from sentence_transformers import SentenceTransformer
                model_name = 'all-MiniLM-L6-v2'
                self.embedding_model = SentenceTransformer(model_name)

            # Generate embedding
            embedding = self.embedding_model.encode(text)

            # Convert to list
            return embedding.tolist()

        except Exception as e:
            logger.error(f"Error generating embedding with Hugging Face: {str(e)}")
            logger.error(traceback.format_exc())
            return []

class PerplexityConnector(AIConnector):
    """Connector for Perplexity API services."""

    def __init__(self, api_key: str = None):
        """
        Initialize the Perplexity connector.

        Args:
            api_key: Perplexity API key
        """
        super().__init__()
        self.api_key = api_key or os.getenv('PERPLEXITY_API_KEY')

        # Check if requests library is available
        try:
            import requests
            self.requests = requests
            self.available = bool(self.api_key)
            if self.available:
                logger.info("Perplexity connector initialized successfully")
            else:
                logger.warning("Perplexity API key not found")
        except ImportError:
            logger.warning("Requests package not installed")
            self.requests = None
            self.available = False

    def generate_text(self, prompt: str, options: Dict[str, Any] = None) -> str:
        """
        Generate text using Perplexity API.

        Args:
            prompt: Prompt for the AI
            options: Additional options for generation

        Returns:
            Generated text
        """
        if not self.is_available():
            logger.error("Perplexity API is not available")
            return "AI service is not available"

        options = options or {}

        try:
            # Set up parameters
            model = options.get('model', 'pplx-7b-online')  # or another Perplexity model

            # Create API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": options.get('system_prompt', "You are a helpful assistant.")},
                    {"role": "user", "content": prompt}
                ]
            }

            # Send request to Perplexity API
            response = self.requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json=data
            )

            # Check for successful response
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                logger.error(f"Perplexity API error: {response.status_code} - {response.text}")
                return f"Error: {response.status_code}"

        except Exception as e:
            logger.error(f"Error generating text with Perplexity: {str(e)}")
            logger.error(traceback.format_exc())
            return f"Error generating text: {str(e)}"

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding for the text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector (not implemented for Perplexity)
        """
        logger.warning("Embedding generation not implemented for Perplexity")
        return []

class MockAIConnector(AIConnector):
    """Mock AI connector for testing."""

    def __init__(self):
        """Initialize the mock AI connector."""
        super().__init__()
        self.available = True
        logger.info("Mock AI connector initialized successfully")

    def generate_text(self, prompt: str, options: Dict[str, Any] = None) -> str:
        """
        Generate text using a mock implementation.

        Args:
            prompt: Prompt for the AI
            options: Additional options for generation

        Returns:
            Generated text
        """
        options = options or {}

        # Check if the prompt is asking for market insights
        if 'market' in prompt.lower() and 'insight' in prompt.lower():
            # Generate mock market insights
            return json.dumps({
                "insights": [
                    {
                        "headline": "Renewable Energy Growth Accelerating",
                        "description": "Renewable energy trends show a 24% growth rate, significantly outpacing traditional energy sectors. This acceleration is particularly notable in solar and wind technologies.",
                        "implications": "Investors should consider increasing allocation to renewable energy portfolios, especially those with strong solar and wind components."
                    },
                    {
                        "headline": "ESG Integration Becoming Standard Practice",
                        "description": "ESG metrics are increasingly being integrated into investment decision-making, with a 32% growth in adoption across funds.",
                        "implications": "Portfolio companies without strong ESG frameworks may face increased scrutiny and potential devaluation."
                    },
                    {
                        "headline": "Circular Economy Creating New Market Opportunities",
                        "description": "Circular economy business models show 28% growth with particularly strong performance in packaging and consumer goods sectors.",
                        "implications": "Early-stage investments in circular economy startups could yield significant returns as the model becomes mainstream."
                    }
                ]
            }, indent=2)

        # Check if the prompt is asking for JSON
        elif 'json' in prompt.lower() or 'JSON' in prompt:
            # Generate a mock JSON response
            return json.dumps({
                "analysis": {
                    "sustainability_score": 75,
                    "esg_rating": "B+",
                    "carbon_footprint": 120,
                    "renewable_energy_percentage": 45,
                    "sustainability_risks": [
                        "Supply chain transparency",
                        "Water usage"
                    ],
                    "sustainability_opportunities": [
                        "Renewable energy adoption",
                        "Circular economy initiatives"
                    ],
                    "tags": [
                        "renewable energy",
                        "carbon reduction",
                        "sustainable supply chain"
                    ]
                },
                "assessment": "The company shows good progress in sustainability initiatives but has room for improvement in supply chain transparency and water usage."
            }, indent=2)

        # Otherwise, generate a mock text response
        return f"This is a mock response to: {prompt[:50]}..."

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate a mock embedding for the text.

        Args:
            text: Text to embed

        Returns:
            Mock embedding vector
        """
        # Generate a deterministic but unique embedding based on the text
        import hashlib

        # Create a hash of the text
        hash_object = hashlib.md5(text.encode())
        hash_hex = hash_object.hexdigest()

        # Convert the hash to a list of floats
        embedding = []
        for i in range(0, len(hash_hex), 2):
            # Convert each pair of hex digits to a float between -1 and 1
            value = int(hash_hex[i:i+2], 16) / 127.5 - 1
            embedding.append(value)

        # Pad or truncate to 10 dimensions
        embedding = embedding[:10] if len(embedding) > 10 else embedding + [0] * (10 - len(embedding))

        return embedding

# Factory function to get the appropriate AI connector
def get_ai_connector(connector_type: str = None) -> AIConnector:
    """
    Get an AI connector for the specified type.

    Args:
        connector_type: Type of AI connector ('openai', 'huggingface', 'perplexity', 'mock')

    Returns:
        AI connector
    """
    # Map of connector types to their environment variables and connector classes
    connector_map = {
        'openai': {'env_var': 'OPENAI_API_KEY', 'class': OpenAIConnector},
        'perplexity': {'env_var': 'PERPLEXITY_API_KEY', 'class': PerplexityConnector},
        'huggingface': {'env_var': 'HUGGINGFACE_API_KEY', 'class': HuggingFaceConnector},
        'mock': {'env_var': None, 'class': MockAIConnector}
    }

    # If connector_type is not specified, try to determine from environment
    if connector_type is None:
        for conn_type, config in connector_map.items():
            if config['env_var'] and os.getenv(config['env_var']):
                connector_type = conn_type
                break
        else:  # No environment variables found
            connector_type = 'mock'

    connector_type = connector_type.lower()

    # Get the connector class from the map
    if connector_type in connector_map:
        return connector_map[connector_type]['class']()
    else:
        logger.warning(f"Unsupported AI connector type: {connector_type}, falling back to mock")
        return MockAIConnector()
