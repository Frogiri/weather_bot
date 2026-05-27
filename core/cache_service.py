from typing import Optional, Any
from datetime import datetime, timedelta
import json
from loguru import logger

class MemoryCache:
    """Простой in-memory кеш"""
    def __init__(self):
        self._cache = {}
    
    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            data, expires = self._cache[key]
            if datetime.now() < expires:
                return data
            del self._cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl_seconds: int):
        expires = datetime.now() + timedelta(seconds=ttl_seconds)
        self._cache[key] = (value, expires)
    
    def clear(self):
        self._cache.clear()
        logger.info("Memory cache cleared")

class CacheService:
    """Сервис кеширования"""
    def __init__(self, use_redis: bool = False):
        self.use_redis = use_redis
        self.memory_cache = MemoryCache()
        if use_redis:
            try:
                import redis
                logger.info("Redis support enabled (but not configured yet)")
            except ImportError:
                logger.warning("Redis not installed, using memory cache")
                self.use_redis = False
    
    def get(self, key: str) -> Optional[Any]:
        return self.memory_cache.get(key)
    
    def set(self, key: str, value: Any, ttl_seconds: int):
        self.memory_cache.set(key, value, ttl_seconds)
    
    def clear(self):
        self.memory_cache.clear()