"""
Base Adapter
Defines the interface for all data adapters.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseAdapter(ABC):
    """Abstract base class for all data adapters"""
    
    @abstractmethod
    def can_handle(self, file_path: str) -> bool:
        """Check if this adapter can handle the given file"""
        pass
    
    @abstractmethod
    def read_file(self, file_path: str) -> Any:
        """Read and parse the file"""
        pass
    
    @abstractmethod
    def process(self, file_path: str) -> Dict[str, Any]:
        """Process the file and return normalized data"""
        pass
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate the normalized data"""
        required_keys = ['type', 'data']
        return all(key in data for key in required_keys)
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported file formats"""
        return getattr(self, 'supported_formats', []) 