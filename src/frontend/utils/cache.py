"""
Cache module for SustainaTrend™.

This module provides caching functionality for the application, including:
- Function result caching using lru_cache
- Simple in-memory cache with TTL support
- Cache invalidation utilities
"""

from functools import lru_cache, wraps
from typing import Any, Callable, Dict, Optional, TypeVar
from datetime import datetime, timedelta
import threading
import logging
import functools
import time

logger = logging.getLogger(__name__)

# Type variable for generic function types
T = TypeVar('T')

class Cache:
    """Simple in-memory cache with TTL support."""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        
    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache."""
        with self._lock:
            if key not in self._cache:
                return None
            
            entry = self._cache[key]
            if entry['expires_at'] and entry['expires_at'] < datetime.now():
                del self._cache[key]
                return None
                
            return entry['value']
            
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value in the cache with optional TTL in seconds."""
        expires_at = datetime.now() + timedelta(seconds=ttl) if ttl else None
        
        with self._lock:
            self._cache[key] = {
                'value': value,
                'expires_at': expires_at
            }
            
    def delete(self, key: str) -> None:
        """Delete a value from the cache."""
        with self._lock:
            self._cache.pop(key, None)
            
    def clear(self) -> None:
        """Clear all values from the cache."""
        with self._lock:
            self._cache.clear()

# Global cache instance
cache = Cache()

def cached(ttl: Optional[int] = None) -> Callable:
    """
    Decorator that caches function results with optional TTL.
    
    Args:
        ttl: Time to live in seconds. If None, cache never expires.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            # Create a cache key from function name and arguments
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            result = cache.get(key)
            if result is not None:
                logger.debug(f"Cache hit for {key}")
                return result
                
            # Calculate result and store in cache
            result = func(*args, **kwargs)
            cache.set(key, result, ttl)
            logger.debug(f"Cache miss for {key}, stored result")
            return result
            
        return wrapper
    return decorator

# Convenience decorator for LRU cache with default maxsize
def lru_cached(maxsize: int = 128) -> Callable:
    """
    Decorator that applies Python's lru_cache with a default maxsize.
    
    Args:
        maxsize: Maximum size of the LRU cache.
    """
    return lru_cache(maxsize=maxsize)

def cache_with_ttl(ttl_seconds: int = 300):
    """
    Decorator that caches function results with a time-to-live (TTL).
    
    Args:
        ttl_seconds (int): Time-to-live in seconds for cached results. Defaults to 5 minutes.
    
    Returns:
        Callable: Decorated function that uses caching with TTL.
    """
    def decorator(func):
        cache = {}
        lock = threading.Lock()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str((args, frozenset(kwargs.items())))
            
            with lock:
                if key in cache:
                    result, timestamp = cache[key]
                    if time.time() - timestamp <= ttl_seconds:
                        logger.debug(f"Cache hit for {func.__name__} with key {key}")
                        return result
                    else:
                        logger.debug(f"Cache expired for {func.__name__} with key {key}")
                        del cache[key]

                result = func(*args, **kwargs)
                cache[key] = (result, time.time())
                logger.debug(f"Cache miss for {func.__name__} with key {key}")
                return result

        def clear_cache():
            """Clear the cache for this function."""
            with lock:
                cache.clear()
                logger.debug(f"Cache cleared for {func.__name__}")

        wrapper.clear_cache = clear_cache
        return wrapper

    return decorator

__all__ = ['Cache', 'cache', 'cached', 'lru_cached', 'cache_with_ttl'] 