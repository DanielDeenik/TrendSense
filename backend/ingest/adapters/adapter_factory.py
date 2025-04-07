"""
Adapter Factory
Manages and provides access to all data adapters.
"""

import logging
from typing import Dict, Type, Optional
from .base_adapter import BaseAdapter
from .lemonedge_adapter import LemonEdgeAdapter
from .excel_adapter import ExcelAdapter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdapterFactory:
    """Factory class for managing data adapters"""
    
    def __init__(self):
        self._adapters: Dict[str, Type[BaseAdapter]] = {
            'lemonedge': LemonEdgeAdapter,
            'excel': ExcelAdapter
        }
    
    def get_adapter(self, file_path: str) -> Optional[BaseAdapter]:
        """Get the appropriate adapter for the given file"""
        for adapter_class in self._adapters.values():
            adapter = adapter_class()
            if adapter.can_handle(file_path):
                return adapter
        
        logger.warning(f"No suitable adapter found for file: {file_path}")
        return None
    
    def register_adapter(self, name: str, adapter_class: Type[BaseAdapter]) -> None:
        """Register a new adapter"""
        if not issubclass(adapter_class, BaseAdapter):
            raise ValueError(f"Adapter class must inherit from BaseAdapter")
        
        self._adapters[name] = adapter_class
        logger.info(f"Registered new adapter: {name}")
    
    def list_adapters(self) -> Dict[str, Type[BaseAdapter]]:
        """List all registered adapters"""
        return self._adapters.copy() 